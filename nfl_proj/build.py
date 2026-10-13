"""Parse every cached page for a season into tidy tables (SQLite + pandas).

Tables written to ``data/nfl_<season>.db``:
  games         one row per scheduled game (played or not)
  player_games  box score line per player per game (plus snaps / position)
  plays         one row per play with offense/defense, bucket, EPA, success
  team_defense  PFR advanced defense (blitz / pressure) season totals
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from .parse_pfr import parse_boxscore, parse_schedule, parse_team_defense
from .playparse import is_success, parse_detail
from .scrape import Fetcher


def _yardline_100(location: str, offense: str | None) -> float | None:
    """Distance from the offense to the opponent's goal line."""
    if not location:
        return None
    parts = location.split()
    if len(parts) == 1 and parts[0] == "50":
        return 50.0
    if len(parts) != 2 or not parts[1].isdigit():
        return None
    side, yd = parts[0], float(parts[1])
    if offense is None:
        return None
    return 100 - yd if side == offense else yd


def build_game_plays(game: dict, box: dict) -> pd.DataFrame:
    team_of = {}
    for s in box["snaps"]:
        if s["off_snaps"] > 0:
            team_of[s["player_id"]] = s["team"]
    for p in box["player_offense"]:
        team_of[p["player_id"]] = p["team"]

    rows = []
    prev_off = None
    prev_away, prev_home = 0.0, 0.0
    for raw in box["pbp"]:
        parsed = parse_detail(raw["detail"], raw["detail_html"])
        key = parsed["passer_id"] or parsed["rusher_id"] or parsed["first_player_id"]
        offense = team_of.get(key) if key else None
        if parsed["play_type"] in ("pass", "run", "sack", "scramble", "kneel", "spike"):
            if offense is None:
                offense = prev_off
            prev_off = offense
        else:
            offense = offense if offense in (game["home"], game["away"]) else prev_off
        defense = None
        if offense:
            defense = game["home"] if offense == game["away"] else game["away"]

        off_score = prev_home if offense == game["home"] else prev_away
        def_score = prev_away if offense == game["home"] else prev_home
        epa = (raw["ep_after"] - raw["ep_before"]
               if raw["ep_after"] is not None and raw["ep_before"] is not None else None)
        rows.append({
            "boxscore_id": game["boxscore_id"], "season": game["season"],
            "week": game["week"], "seq": raw["seq"], "quarter": raw["quarter"],
            "clock": raw["clock"], "down": raw["down"], "ytg": raw["ytg"],
            "yardline_100": _yardline_100(raw["location"], offense),
            "offense": offense, "defense": defense,
            "score_diff": off_score - def_score if offense else None,
            "detail": raw["detail"], "epa": epa,
            "success": is_success(raw["down"], raw["ytg"], parsed["yards"])
            if parsed["play_type"] in ("pass", "run", "sack", "scramble") else None,
            **{k: v for k, v in parsed.items() if k != "first_player_id"},
        })
        if raw["score_away"] is not None:
            prev_away = raw["score_away"]
        if raw["score_home"] is not None:
            prev_home = raw["score_home"]
    return pd.DataFrame(rows)


def build_season(season: int, cache_dir: Path, db_path: Path, log=print) -> dict[str, pd.DataFrame]:
    fetcher = Fetcher(cache_dir)
    sched_path = fetcher.cache_path(f"/years/{season}/games.htm")
    if not sched_path.exists():
        raise FileNotFoundError(f"No cached schedule at {sched_path}; run `scrape` first.")
    games = parse_schedule(sched_path.read_text(encoding="utf-8"), season)

    play_frames, player_rows = [], []
    for g in games:
        if not g["boxscore_id"]:
            continue
        path = fetcher.cache_path(f"/boxscores/{g['boxscore_id']}.htm")
        if not path.exists():
            log(f"warning: {g['boxscore_id']} not cached, skipping")
            continue
        box = parse_boxscore(path.read_text(encoding="utf-8"), g["boxscore_id"], g)
        if not box["pbp"]:
            log(f"warning: {g['boxscore_id']} has no play-by-play table")
        play_frames.append(build_game_plays(g, box))

        snaps = {(s["player_id"], s["team"]): s for s in box["snaps"]}
        seen = set()
        for p in box["player_offense"]:
            s = snaps.get((p["player_id"], p["team"]), {})
            seen.add((p["player_id"], p["team"]))
            player_rows.append({**p, "boxscore_id": g["boxscore_id"], "week": g["week"],
                                "pos": s.get("pos", ""), "off_snaps": s.get("off_snaps", 0.0),
                                "off_pct": s.get("off_pct", 0.0)})
        # Players who played offensive snaps but recorded no stats still
        # matter for usage, so keep them with zero stat lines.
        for (pid, team), s in snaps.items():
            if (pid, team) not in seen and s["off_snaps"] > 0:
                player_rows.append({"player_id": pid, "player": s["player"], "team": team,
                                    "boxscore_id": g["boxscore_id"], "week": g["week"],
                                    "pos": s["pos"], "off_snaps": s["off_snaps"],
                                    "off_pct": s["off_pct"]})

    tables = {
        "games": pd.DataFrame(games),
        "plays": pd.concat(play_frames, ignore_index=True) if play_frames else pd.DataFrame(),
        "player_games": pd.DataFrame(player_rows).fillna(0) if player_rows else pd.DataFrame(),
    }
    opp_path = fetcher.cache_path(f"/years/{season}/opp.htm")
    tables["team_defense"] = (pd.DataFrame(parse_team_defense(opp_path.read_text(encoding="utf-8")))
                              if opp_path.exists() else pd.DataFrame())

    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as con:
        for name, df in tables.items():
            if not df.empty:
                df.to_sql(name, con, if_exists="replace", index=False)
    n_plays = len(tables["plays"])
    log(f"built {db_path}: {len(play_frames)} games, {n_plays} plays, "
        f"{len(tables['player_games'])} player-game rows")
    return tables


def load_season(db_path: Path) -> dict[str, pd.DataFrame]:
    with sqlite3.connect(db_path) as con:
        names = [r[0] for r in con.execute("select name from sqlite_master where type='table'")]
        return {n: pd.read_sql(f"select * from {n}", con) for n in names}
