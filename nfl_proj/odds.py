"""Player prop lines and prices (for grading paper trades only).

Sources (``[odds] source``; "auto" = The Odds API when ODDS_API_KEY is set,
else ESPN):

- ESPN's public odds feed (no key). DraftKings player-prop lines, current and
  opening, for every game. It carries no prices, so both sides get
  ``[odds] assumed_price`` (default -115, a little worse than the usual
  DraftKings prop price) and every row is marked price_source = "assumed".
  ROI graded at assumed prices is an estimate; line movement (CLV) is real.
- The Odds API (https://the-odds-api.com), key in ODDS_API_KEY: real prices.
- data/manual/prop_lines.csv (player, stat, line, over_odds, under_odds).

Lines are saved per week and snapshot ("lock" when picks are locked,
"close" shortly before kickoff, to measure closing-line value).

The market never feeds a projection.
"""

from __future__ import annotations

import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

API = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl"
MARKET_TO_STAT = {
    "player_pass_yds": "pass_yds", "player_pass_completions": "completions",
    "player_receptions": "receptions", "player_reception_yds": "rec_yds",
    "player_rush_yds": "rush_yds", "player_rush_attempts": "carries",
    "player_pass_attempts": "pass_att",
}


def norm_name(s: str) -> str:
    s = str(s).lower().replace(".", "").replace("'", "").replace("-", " ")
    for suf in (" jr", " sr", " iii", " ii", " iv"):
        s = s.removesuffix(suf)
    return " ".join(s.split())


def american_to_decimal(odds: float) -> float:
    return 1 + (odds / 100 if odds > 0 else 100 / -odds)


def fetch_props(games: pd.DataFrame, week: int, cfg: dict, key: str | None = None, log=print) -> pd.DataFrame:
    """Lines for every game in ``week``. One row per player / stat / book."""
    key = key or os.environ.get("ODDS_API_KEY")
    if not key:
        raise RuntimeError("No ODDS_API_KEY set. Get a free key at https://the-odds-api.com "
                           "or enter lines in data/manual/prop_lines.csv.")
    c = cfg.get("odds", {})
    events = requests.get(f"{API}/events", params={"apiKey": key}, timeout=30).json()
    want = games[games["week"] == week]
    from .nflverse import team as nv_team
    full = {  # The Odds API uses full team names
        "Arizona Cardinals": "ARI", "Atlanta Falcons": "ATL", "Baltimore Ravens": "BAL", "Buffalo Bills": "BUF",
        "Carolina Panthers": "CAR", "Chicago Bears": "CHI", "Cincinnati Bengals": "CIN", "Cleveland Browns": "CLE",
        "Dallas Cowboys": "DAL", "Denver Broncos": "DEN", "Detroit Lions": "DET", "Green Bay Packers": "GNB",
        "Houston Texans": "HOU", "Indianapolis Colts": "IND", "Jacksonville Jaguars": "JAX", "Kansas City Chiefs": "KAN",
        "Las Vegas Raiders": "LVR", "Los Angeles Chargers": "LAC", "Los Angeles Rams": "LAR", "Miami Dolphins": "MIA",
        "Minnesota Vikings": "MIN", "New England Patriots": "NWE", "New Orleans Saints": "NOR", "New York Giants": "NYG",
        "New York Jets": "NYJ", "Philadelphia Eagles": "PHI", "Pittsburgh Steelers": "PIT", "San Francisco 49ers": "SFO",
        "Seattle Seahawks": "SEA", "Tampa Bay Buccaneers": "TAM", "Tennessee Titans": "TEN", "Washington Commanders": "WAS"}
    pairs = {(r.home, r.away) for r in want.itertuples()}
    rows = []
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for ev in events:
        h, a = full.get(ev.get("home_team")), full.get(ev.get("away_team"))
        if (h, a) not in pairs:
            continue
        r = requests.get(f"{API}/events/{ev['id']}/odds", timeout=30, params={
            "apiKey": key, "regions": c.get("regions", "us"), "oddsFormat": "american",
            "markets": ",".join(c.get("markets", list(MARKET_TO_STAT)))})
        if r.status_code != 200:
            log(f"odds: {a}@{h} failed ({r.status_code}): {r.text[:120]}")
            continue
        remaining = r.headers.get("x-requests-remaining")
        for bk in r.json().get("bookmakers", []):
            for mk in bk.get("markets", []):
                stat = MARKET_TO_STAT.get(mk["key"])
                if not stat:
                    continue
                by_player = {}
                for o in mk.get("outcomes", []):
                    d = by_player.setdefault((o.get("description"), o.get("point")), {})
                    d[o["name"].lower()] = o.get("price")
                for (player, point), d in by_player.items():
                    if point is None or "over" not in d or "under" not in d:
                        continue
                    rows.append({"week": week, "home": h, "away": a, "player": player, "stat": stat,
                                 "line": float(point), "over_odds": d["over"], "under_odds": d["under"],
                                 "book": bk["key"], "fetched_at": now})
        log(f"odds: {a}@{h} ok (credits left: {remaining})")
    return pd.DataFrame(rows)


ESPN_SCOREBOARD = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
ESPN_CORE = "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl"
ESPN_TYPE_TO_STAT = {  # main over/under markets only (milestones and alt lines are skipped)
    "total passing yards": "pass_yds", "total pass completions": "completions",
    "total passing attempts": "pass_att", "total receptions": "receptions",
    "total receiving yards": "rec_yds", "total rushing yards": "rush_yds", "total carries": "carries"}
ESPN_TEAM = {"WSH": "WAS"}  # ESPN codes that differ from nflverse before the PFR mapping


def _espn_stat(type_name: str) -> str | None:
    return ESPN_TYPE_TO_STAT.get(type_name.split("(")[0].strip().lower())


def fetch_espn(games: pd.DataFrame, week: int, cfg: dict, roster: pd.DataFrame | None = None,
               log=print) -> pd.DataFrame:
    """DraftKings lines from ESPN's public odds feed. Prices are assumed (see module doc)."""
    from .nflverse import team as nv_team
    c = cfg.get("odds", {})
    price = float(c.get("assumed_price", -115))
    provider = c.get("espn_provider", 100)  # 100 = DraftKings
    season = int(games["season"].max()) if "season" in games else datetime.now().year
    want = games[games["week"] == week]
    pairs = {(r.home, r.away) for r in want.itertuples()}
    sb = requests.get(ESPN_SCOREBOARD, params={"seasontype": 2, "week": week, "dates": season}, timeout=30).json()
    ids = {}
    if roster is not None and {"espn_id", "gsis_id", "full_name"} <= set(roster.columns):
        rr = roster.dropna(subset=["espn_id"]).drop_duplicates("espn_id", keep="last")
        ids = {str(int(e)): (g, n) for e, g, n in zip(rr["espn_id"], rr["gsis_id"], rr["full_name"])}
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    rows = []
    for ev in sb.get("events", []):
        comp = ev["competitions"][0]
        side = {t["homeAway"]: nv_team(ESPN_TEAM.get(t["team"]["abbreviation"], t["team"]["abbreviation"]))
                for t in comp["competitors"]}
        h, a = side.get("home"), side.get("away")
        if (h, a) not in pairs:
            continue
        url = f"{ESPN_CORE}/events/{ev['id']}/competitions/{comp['id']}/odds/{provider}/propBets"
        items, page, pages = [], 1, 1
        while page <= pages:
            r = requests.get(url, params={"limit": 1000, "page": page}, timeout=30)
            if r.status_code != 200:
                log(f"odds(espn): {a}@{h} page {page} failed ({r.status_code})")
                break
            d = r.json()
            items += d.get("items", [])
            pages = d.get("pageCount", 1)
            page += 1
            time.sleep(1)
        n0 = len(rows)
        for it in items:
            stat = _espn_stat(it.get("type", {}).get("name", ""))
            ref = it.get("athlete", {}).get("$ref", "")
            m = re.search(r"/athletes/(\d+)", ref)
            line = it.get("current", {}).get("target", {}).get("value")
            if not stat or not m or line is None:
                continue
            gsis, name = ids.get(m.group(1), (None, None))
            if name is None:
                try:
                    name = requests.get(ref.replace("http://", "https://"), timeout=30).json().get("fullName")
                except Exception:
                    name = None
                ids[m.group(1)] = (None, name)
            if not name:
                continue
            rows.append({"week": week, "home": h, "away": a, "player": name, "player_id": gsis,
                         "espn_id": m.group(1), "stat": stat, "line": float(line),
                         "open_line": it.get("open", {}).get("target", {}).get("value"),
                         "over_odds": price, "under_odds": price, "price_source": "assumed",
                         "book": "draftkings", "line_updated": it.get("lastUpdated"), "fetched_at": now})
        log(f"odds(espn): {a}@{h} {len(rows) - n0} lines")
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    # Each over/under appears twice (one item per side); keep the newest line per player and stat
    return out.sort_values("line_updated", ascending=False).drop_duplicates(["espn_id", "stat"]) \
              .sort_values(["home", "player", "stat"]).reset_index(drop=True)


def fetch(games: pd.DataFrame, week: int, cfg: dict, roster: pd.DataFrame | None = None, log=print) -> pd.DataFrame:
    src = cfg.get("odds", {}).get("source", "auto")
    if src == "the_odds_api" or (src == "auto" and os.environ.get("ODDS_API_KEY")):
        out = fetch_props(games, week, cfg, log=log)
        return out.assign(price_source="book") if not out.empty else out
    return fetch_espn(games, week, cfg, roster, log=log)


def pick_book(lines: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """One line per player / stat: the configured book, else the first book offering it."""
    if lines.empty or "book" not in lines:
        return lines
    pref = cfg.get("odds", {}).get("book", "draftkings")
    lines = lines.assign(_pref=(lines["book"] != pref).astype(int))
    return lines.sort_values(["_pref", "book"]).drop_duplicates(["player", "stat"]).drop(columns="_pref")


def save(lines: pd.DataFrame, out_dir: Path, week: int, label: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    p = out_dir / f"week_{week:02d}_{label}.csv"
    lines.to_csv(p, index=False)
    return p


def load_lines(out_dir: Path, week: int, label: str, manual: Path | None = None) -> pd.DataFrame:
    p = out_dir / f"week_{week:02d}_{label}.csv"
    if p.exists():
        return pd.read_csv(p)
    if manual is not None and Path(manual).exists():
        m = pd.read_csv(manual)
        if {"over_odds", "under_odds"} <= set(m.columns):
            return m.assign(book="manual", fetched_at=datetime.now(timezone.utc).isoformat(timespec="seconds"))
    return pd.DataFrame()
