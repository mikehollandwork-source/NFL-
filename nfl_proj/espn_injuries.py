"""Live injury statuses from ESPN's public injury feed and Sleeper's public
API (both free, no key).

nflverse's injury file updates about once a day and often lags the final
report and game-day decisions; ESPN updates within minutes but its
league-wide feed keeps only 25 entries per team (players drop off), and
Sleeper lists every injured player. The more recently updated feed wins. Statuses for
the projected week are merged over the nflverse report: Out, Doubtful and
Questionable as reported; Injured Reserve, PUP and suspensions count as Out;
"Active" clears the player. ESPN athlete ids map to nflverse ids through the
weekly roster's espn_id.
"""

from __future__ import annotations

import pandas as pd
import requests

URL = "https://site.web.api.espn.com/apis/site/v2/sports/football/nfl/injuries"
AS_OUT = {"Injured Reserve", "Physically Unable to Perform", "Suspension", "Non-Football Injury",
          "Out For Season"}


def fetch(roster: pd.DataFrame | None, log=print) -> pd.DataFrame:
    from .nflverse import team as nv_team
    d = requests.get(URL, timeout=30).json()
    from .odds import norm_name
    ids, by_name = {}, {}
    if roster is not None and {"espn_id", "gsis_id"} <= set(roster.columns):
        r = roster.dropna(subset=["espn_id"]).drop_duplicates("espn_id", keep="last")
        ids = {str(int(e)): g for e, g in zip(r["espn_id"], r["gsis_id"])}
        rr = roster.dropna(subset=["gsis_id"]).drop_duplicates(["team", "full_name"], keep="last")
        by_name = {(nv_team(t), norm_name(n)): g for t, n, g in zip(rr["team"], rr["full_name"], rr["gsis_id"])}
    rows = []
    for t in d.get("injuries", []):
        for x in t.get("injuries", []):
            a = x.get("athlete", {})
            href = (a.get("links") or [{}])[0].get("href", "")
            eid = href.split("/id/")[1].split("/")[0] if "/id/" in href else ""
            team = nv_team(a.get("team", {}).get("abbreviation", "")) if a.get("team") else None
            status = x.get("status", "")
            rows.append({"team": team, "player": a.get("displayName"), "espn_id": eid,
                         "player_id": ids.get(eid) or by_name.get((team, norm_name(a.get("displayName", ""))), ""), "pos": a.get("position", {}).get("abbreviation"),
                         "espn_status": status,
                         "report_status": "Out" if status in AS_OUT else (status if status in
                                                                          {"Out", "Doubtful", "Questionable"} else None),
                         "injury": (x.get("details") or {}).get("type") or "", "updated": x.get("date"),
                         "comment": x.get("shortComment", "")})
    out = pd.DataFrame(rows)
    log(f"ESPN injuries: {len(out)} entries, {out['report_status'].notna().sum() if len(out) else 0} not active")
    return out


SLEEPER = "https://api.sleeper.app/v1/players/nfl"
SLEEPER_OUT = {"IR", "PUP", "Sus", "NFI", "DNR"}


def fetch_sleeper(roster: pd.DataFrame | None, log=print) -> pd.DataFrame:
    """Sleeper's player file (about 15 MB; their docs ask for at most one
    pull a day per app, so it's used only on lock runs)."""
    from .nflverse import team as nv_team
    from .odds import norm_name
    d = requests.get(SLEEPER, timeout=60).json()
    by_name, by_espn = {}, {}
    if roster is not None and {"gsis_id", "full_name"} <= set(roster.columns):
        rr = roster.dropna(subset=["gsis_id"]).drop_duplicates(["team", "full_name"], keep="last")
        by_name = {(nv_team(t), norm_name(n)): g for t, n, g in zip(rr["team"], rr["full_name"], rr["gsis_id"])}
        re_ = roster.dropna(subset=["espn_id", "gsis_id"]).drop_duplicates("espn_id", keep="last")
        by_espn = {str(int(e)): g for e, g in zip(re_["espn_id"], re_["gsis_id"])}
    rows = []
    for v in d.values():
        st = v.get("injury_status")
        if not v.get("team") or v.get("position") in (None, "DEF"):
            continue
        team = nv_team(v["team"])
        name = v.get("full_name") or f"{v.get('first_name', '')} {v.get('last_name', '')}"
        pid = v.get("gsis_id") or by_espn.get(str(v.get("espn_id") or "")) or by_name.get((team, norm_name(name)), "")
        upd = pd.to_datetime(v.get("news_updated"), unit="ms", utc=True) if v.get("news_updated") else pd.NaT
        rows.append({"team": team, "player": name, "player_id": (pid or "").strip(), "pos": v.get("position"),
                     "sleeper_status": st, "long_term": st in SLEEPER_OUT,
                     "report_status": "Out" if st in SLEEPER_OUT else (st if st in {"Out", "Doubtful", "Questionable"} else None),
                     "injury": v.get("injury_body_part") or "", "updated": upd})
    out = pd.DataFrame(rows)
    log(f"Sleeper: {len(out)} players, {out['report_status'].notna().sum()} not active")
    return out


def combine(espn: pd.DataFrame, sleeper: pd.DataFrame) -> pd.DataFrame:
    """One status per player: the more recently updated feed wins; a player
    only one feed lists keeps that feed's status."""
    frames = []
    for src, df in (("espn", espn), ("sleeper", sleeper)):
        if df is None or df.empty:
            continue
        x = df[df["player_id"].fillna("") != ""].copy()
        x["updated"] = pd.to_datetime(x["updated"], utc=True, errors="coerce")
        x["source"] = src
        frames.append(x[["team", "player", "player_id", "pos", "report_status", "injury", "updated", "source"]])
    if not frames:
        return pd.DataFrame(columns=["team", "player", "player_id", "pos", "report_status", "injury", "updated", "source"])
    allf = pd.concat(frames, ignore_index=True)
    # Sleeper lists every rostered player; only its injury entries carry news
    allf = allf[(allf["source"] == "espn") | allf["report_status"].notna()]
    # A Sleeper-only Out/Questionable that is stale (player recovered and dropped off ESPN's list)
    # must not sit a healthy player: keep it only if recent or a long-term list (IR / PUP / suspended)
    if sleeper is not None and not sleeper.empty:
        lt = set(sleeper.loc[sleeper.get("long_term", False) == True, "player_id"])  # noqa: E712
        espn_ids = set(allf.loc[allf["source"] == "espn", "player_id"])
        fresh = allf["updated"] >= pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=10)
        allf = allf[(allf["source"] == "espn") | allf["player_id"].isin(espn_ids) | fresh | allf["player_id"].isin(lt)]
    allf = allf.sort_values("updated", na_position="first")
    return allf.drop_duplicates("player_id", keep="last").reset_index(drop=True)


def live(roster: pd.DataFrame | None, log=print) -> pd.DataFrame:
    """ESPN + Sleeper combined; either feed failing leaves the other."""
    parts = {}
    for name, fn in (("espn", fetch), ("sleeper", fetch_sleeper)):
        try:
            parts[name] = fn(roster, log=log)
        except Exception as e:
            log(f"{name} injury feed unavailable: {e}")
            parts[name] = pd.DataFrame()
    return combine(parts["espn"], parts["sleeper"])


def merge(injuries: pd.DataFrame | None, live: pd.DataFrame, week: int) -> pd.DataFrame:
    """nflverse injuries with this week's rows replaced/added from ESPN."""
    inj = injuries.copy() if injuries is not None else pd.DataFrame(
        columns=["week", "team", "player_id", "player", "pos", "report_status", "injury", "practice_status"])
    if live is None or live.empty:
        return inj
    lv = live[live["player_id"].fillna("") != ""].copy()
    known = set(lv["player_id"])
    keep = inj[~((inj["week"] == week) & inj["player_id"].isin(known))]
    add = lv.assign(week=week)[["week", "team", "player_id", "player", "pos", "report_status", "injury"]]
    return pd.concat([keep, add], ignore_index=True)
