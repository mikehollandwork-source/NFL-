"""One week's projection, live or replayed as of a past week.

``run_week(tables, cfg, paths, week)`` projects ``week`` using the full
database (the live run). ``run_week(..., asof=True)`` first cuts every table
down to what was known before that week kicked off, so a past week can be
replayed for the backtest:

  plays, player stats, defenders, kickers, coverage, snaps   weeks < W
  games                                                       results / box score ids
                                                              hidden for weeks >= W
  injury report                                               weeks <= W (published pre-game)
  depth charts                                                the snapshot before W's first game

Left out of replays because they were gathered later: the Sharp scheme
scrape, the researched defensive personnel file and your manual overrides.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from . import adaptation


def as_of(tables: dict, week: int) -> dict:
    t = dict(tables)
    for name in ("plays", "player_games", "defenders", "kickers", "coverage", "def_snaps"):
        if name in t and t[name] is not None and not t[name].empty and "week" in t[name]:
            t[name] = t[name][t[name]["week"] < week].copy()
    g = t["games"].copy()
    later = g["week"] >= week
    g.loc[later, "boxscore_id"] = None
    for c in ("home_score", "away_score"):
        if c in g:
            g.loc[later, c] = np.nan
    t["games"] = g
    if "injuries" in t:
        t["injuries"] = t["injuries"][t["injuries"]["week"] <= week]
    return t


def run_week(tables: dict, cfg: dict, paths: dict, week: int, asof: bool = False,
             n_sims: int | None = None, log=print) -> dict:
    from .availability import auto_overrides, merge_overrides
    from .corners import Corners, load_personnel
    from .profiles import (combined_labels, defense_profile, load_manual_labels, matchup_splits,
                           offense_style, prep_plays)
    from .project import Projector
    from .sim import Simulator, wide_means

    t = as_of(tables, week) if asof else tables
    plays = prep_plays(t["plays"], cfg)
    style = offense_style(plays, t["plays"])
    team_def = t.get("team_defense")
    if asof:
        from .nflverse import team_defense
        team_def = team_defense(t["plays"], None)
    dprof = defense_profile(plays, team_def)
    tags = load_manual_labels(paths["tags"]) if not asof else load_manual_labels(paths["tags"]).iloc[0:0]
    labels = combined_labels(dprof, tags, cfg["matchup"]["defense_labels"])
    splits = matchup_splits(plays, labels)

    scheme, coach = None, None
    from .cli import _scheme_and_coach
    sch, coach = _scheme_and_coach(cfg, paths, plays, labels)
    if not asof:
        scheme = sch
    est = adaptation.estimate(plays, cfg["adaptation"]["min_plays"])
    strength = adaptation.effective_strength(est, cfg)

    games = t["games"]
    wk = games[games["week"] == week]
    teams = sorted(set(wk["home"]) | set(wk["away"]))

    def for_week(df):
        if df is None or df.empty or "for_week" not in df:
            return df
        return df[df["for_week"] == week]

    manual = None
    if not asof and paths["overrides"].exists():
        manual = pd.read_csv(paths["overrides"], dtype=str).fillna("")
    auto, flags = auto_overrides(week, t.get("injuries"), for_week(t.get("depth_qb")), t["player_games"],
                                 teams, cfg)
    overrides = merge_overrides(manual, auto)

    outs = overrides[overrides["status"].str.lower() == "out"] if not overrides.empty else overrides
    personnel = load_personnel(paths["personnel"]) if not asof else None
    corners = Corners(t.get("coverage"), for_week(t.get("depth_db")), personnel,
                      set(outs.get("player_id", pd.Series(dtype=str))) - {""},
                      set(outs.get("player", pd.Series(dtype=str))), cfg)

    from .priors import Priors, load_prev_plays
    prev = cfg.get("priors", {}).get("season")
    priors = Priors(load_prev_plays(paths["db"].parent / f"nfl_{int(prev)}.db", cfg) if prev else None, cfg, coach)
    t = dict(t)
    t["_streaks"] = streak_persistence(paths, cfg)
    proj = Projector(plays, t["player_games"], games, cfg, labels, overrides, scheme, coach,
                     corners=corners, tables=t, priors=priors)
    _context_effects(proj, t, cfg, paths, week, teams, overrides, asof, log)
    n = n_sims or cfg["sim"]["n_sims"]

    # Pass 1: model team totals from the simulation (no game script, no market)
    proj.base_mode = True
    sim0 = Simulator(proj, t["player_games"], t.get("defenders"), t.get("kickers"),
                     n_sims=max(n // 3, 1000), seed=cfg["sim"]["seed"] + 1)
    sim0.run_week(week)
    proj.pts_override = dict(sim0.team_points)
    proj.base_mode = False
    proj.reset_adjustments()

    # Pass 2: full projection
    _, ctx = proj.project_week(week)
    sim = Simulator(proj, t["player_games"], t.get("defenders"), t.get("kickers"),
                    n_sims=n, seed=cfg["sim"]["seed"])
    props = sim.run_week(week)
    wide = wide_means(props)
    totals = pd.DataFrame([{"week": week, "team": tm, "opp": op, "model_points": proj.pts_override.get((tm, op)),
                            "final_points": v, **{f"proj_{k}": x for k, x in sim.team_components[(tm, op)].items()}}
                           for (tm, op), v in sim.team_points.items()])

    from .picks import pick_week
    picks = pick_week(proj, props, t["player_games"], week, cfg)

    return {"tables": t, "plays": plays, "style": style, "dprof": dprof, "labels": labels, "splits": splits,
            "scheme": scheme, "coach": coach, "est": est, "strength": strength, "overrides": overrides,
            "auto_overrides": auto, "flags": flags, "corners": corners, "proj": proj, "ctx": ctx,
            "props": props, "wide": wide, "totals": totals, "picks": picks, "sim": sim}


def _prev_tables(paths, cfg):
    import sqlite3
    prev = cfg.get("priors", {}).get("season")
    if not prev:
        return None
    db = paths["db"].parent / f"nfl_{int(prev)}.db"
    if not db.exists():
        return None
    with sqlite3.connect(db) as con:
        return {n: pd.read_sql(f"select * from {n}", con) for n in ("plays", "games", "player_games")}


def _context_effects(proj, t, cfg, paths, week, teams, overrides, asof, log):
    """Weather and offensive-line injuries for this week's games."""
    from . import oline, weather
    prev = _prev_tables(paths, cfg)
    plays_all = [t["plays"]] + ([prev["plays"]] if prev else [])
    games_all = [t["games"]] + ([prev["games"]] if prev else [])
    # Weather: effects estimated from past games; forecasts (live) or the
    # recorded game-day weather (replays) for this week
    if cfg.get("weather", {}).get("enabled", True):
        eff = weather.estimate_effects(pd.concat(plays_all, ignore_index=True), pd.concat(games_all, ignore_index=True))
        proj.weather_effects = eff
        g = t["games"][t["games"]["week"] == week]
        if asof:
            full = proj.games  # results hidden; weather columns are kept
            wx = {}
            for r in g.itertuples():
                roof = str(getattr(r, "roof", "") or getattr(r, "sched_roof", "") or "")
                if roof in weather.INDOOR_ROOFS:
                    wx[r.home] = {"indoor": True}
                elif pd.notna(getattr(r, "wind", np.nan)):
                    wx[r.home] = {"temp": r.temp, "wind": r.wind, "rain": weather._rain(getattr(r, "weather", ""))}
        else:
            wx = weather.forecast_week(t["games"], week, paths["nflverse"].parent / "weather", log)
        for r in g.itertuples():
            m = weather.multipliers(eff, wx.get(r.home))
            proj.weather[r.home] = m
            proj.weather[r.away] = m
    # Offensive line: starters listed out this week
    if cfg.get("oline", {}).get("enabled", True):
        est = oline.estimate([(t["plays"], t["player_games"])] + ([(prev["plays"], prev["player_games"])] if prev else []))
        proj.oline_effects = est
        outs = overrides[overrides["status"].str.lower() == "out"] if not overrides.empty else overrides
        out_ids = set(outs.get("player_id", pd.Series(dtype=str))) - {""}
        out_names = set(outs.get("player", pd.Series(dtype=str)))
        for team in teams:
            st = oline.starters(t["player_games"], team)
            miss = st[st["player_id"].isin(out_ids) | st["player"].isin(out_names)]
            m = oline.effect(est, len(miss))
            m["missing"] = list(miss["player"])
            proj.oline[team] = m



def streak_persistence(paths, cfg) -> dict:
    """Share of a two-game streak that persists, measured on last season
    (so replays of this season use nothing from the future). Cached."""
    import json
    import sqlite3
    if not cfg.get("streaks", {}).get("enabled", True):
        return {}
    prev = cfg.get("priors", {}).get("season")
    if not prev:
        return {}
    cache = paths["nflverse"].parent / f"streaks_{int(prev)}.json"
    if cache.exists():
        return json.loads(cache.read_text())
    db = paths["db"].parent / f"nfl_{int(prev)}.db"
    if not db.exists():
        return {}
    from .streaks import measure
    with sqlite3.connect(db) as con:
        plays = pd.read_sql("select * from plays", con)
    plays["season"] = int(prev)
    res = measure(plays)
    cache.write_text(json.dumps(res, indent=1))
    return res
