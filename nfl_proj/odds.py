"""Player prop lines and prices (for grading paper trades only).

Source: The Odds API (https://the-odds-api.com), key in ODDS_API_KEY. Lines
are saved per week and snapshot ("lock" when picks are locked, "close"
shortly before kickoff, to measure closing-line value). Without a key, put
lines in data/manual/prop_lines.csv with columns
player, stat, line, over_odds, under_odds.

The market never feeds a projection.
"""

from __future__ import annotations

import os
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
