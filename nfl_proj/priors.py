"""Last season as the starting point for this season's team rates.

Every rate the projector shrinks (an offense's yards per play in a play
type, a defense's yards allowed, TD rates, plays per game) used to be
pulled toward the league average when the sample is small. With priors on,
it is pulled toward the team's own 2025 rate instead, regressed toward the
league by ``priors.regress`` (``priors.regress_new_caller`` for offenses
with a new play-caller). This season's plays take over at the same pace as
before: the shrinkage constants are unchanged, only the target moves.

Rates are stored as ratios to the 2025 league average, so a team that was
10% better than league in 2025 starts 10% x regress better than this
season's league average.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


class Priors:
    def __init__(self, plays_prev: pd.DataFrame | None, cfg: dict, coach: pd.DataFrame | None = None):
        c = cfg.get("priors", {})
        self.enabled = c.get("enabled", True) and plays_prev is not None and not plays_prev.empty
        self.r_off = c.get("regress", 0.5)
        self.r_new = c.get("regress_new_caller", 0.3)
        self.r_def = c.get("regress_defense", 0.4)
        self.k_games = c.get("volume_prior_games", 3.0)
        self.new_caller = set()
        if coach is not None and not coach.empty:
            self.new_caller = set(coach[coach["new_caller_2026"].astype(bool)]["team"])
        self.plays_prev = plays_prev
        if not self.enabled:
            return
        p = plays_prev[~plays_prev["garbage"]]
        drop, runs, passes = p[p["dropback"]], p[p["is_run"]], p[p["is_pass"]]
        lg = {"pass": drop["yards"].mean(), "run": runs["yards"].mean(),
              "pass_td": passes["touchdown"].astype(float).mean(), "run_td": runs["touchdown"].astype(float).mean()}
        self.lg = lg
        rows = {}
        for side, key in (("off", "offense"), ("def", "defense")):
            for t, g in p.groupby(key):
                d, r, ps = g[g["dropback"]], g[g["is_run"]], g[g["is_pass"]]
                rows[(side, t)] = {
                    "pass": d["yards"].mean() / lg["pass"], "run": r["yards"].mean() / lg["run"],
                    "pass_td": ps["touchdown"].astype(float).mean() / lg["pass_td"],
                    "run_td": r["touchdown"].astype(float).mean() / lg["run_td"]}
        self.ratio = rows
        allp = plays_prev
        per_game = allp.groupby(["offense", "boxscore_id"]).size().groupby(level=0).mean()
        self.plays_pg = (per_game / per_game.mean()).to_dict()

    def _regress(self, side: str, team: str) -> float:
        if side == "def":
            return self.r_def
        return self.r_new if team in self.new_caller else self.r_off

    def factor(self, side: str, team: str, stat: str) -> float:
        """Multiplier on this season's league rate to use as the shrink target."""
        if not self.enabled or (side, team) not in self.ratio:
            return 1.0
        v = self.ratio[(side, team)].get(stat, 1.0)
        if not np.isfinite(v):
            return 1.0
        return float(1 + self._regress(side, team) * (v - 1))

    def plays_factor(self, team: str) -> float:
        if not self.enabled or team not in self.plays_pg:
            return 1.0
        return float(1 + self._regress("off", team) * (self.plays_pg[team] - 1))


def load_prev_plays(db_path: Path, cfg: dict) -> pd.DataFrame | None:
    if not Path(db_path).exists():
        return None
    import sqlite3
    from .profiles import prep_plays
    with sqlite3.connect(db_path) as con:
        plays = pd.read_sql("select * from plays", con)
    return prep_plays(plays, cfg)
