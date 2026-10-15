"""Live injury statuses from ESPN's public injury feed (no key).

nflverse's injury file updates about once a day and often lags the final
report and game-day decisions; ESPN updates within minutes. Statuses for
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
