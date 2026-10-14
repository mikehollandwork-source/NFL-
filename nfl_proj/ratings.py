"""Strength of schedule: opponent-adjusted offense and defense ratings.

A defense that faced three top offenses looks worse in raw allowed stats
than it is; an offense that feasted on bad defenses looks better. Each
observation (a play's yards, or a team's points in a game) is modelled as

    value = league mean + offense rating + defense rating + noise

and solved by alternating ridge updates, so every rating is measured against
the opponents actually faced. ``lam`` is the ridge penalty in observation
units (plays or games): small samples stay near zero.

``sos_factors`` turns raw-vs-adjusted into multipliers the projector applies
to its raw-stat inputs: an offense whose adjusted rating is below its raw
rating (soft schedule) is scaled down, a defense that faced strong offenses
is scaled toward better.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def fit_additive(df: pd.DataFrame, value: str, off: str = "offense", dfn: str = "defense",
                 weight: str | None = None, lam: float = 40.0, iters: int = 50) -> dict:
    d = df[[off, dfn, value] + ([weight] if weight else [])].dropna(subset=[off, dfn, value])
    w = d[weight].to_numpy(float) if weight else np.ones(len(d))
    y = d[value].to_numpy(float)
    mu = float(np.average(y, weights=w))
    oi, ot = pd.factorize(d[off])
    di, dt = pd.factorize(d[dfn])
    o, de = np.zeros(len(ot)), np.zeros(len(dt))
    wsum_o = np.bincount(oi, w, len(ot))
    wsum_d = np.bincount(di, w, len(dt))
    for _ in range(iters):
        o = np.bincount(oi, w * (y - mu - de[di]), len(ot)) / (wsum_o + lam)
        de = np.bincount(di, w * (y - mu - o[oi]), len(dt)) / (wsum_d + lam)
    raw_o = np.bincount(oi, w * (y - mu), len(ot)) / (wsum_o + lam)
    raw_d = np.bincount(di, w * (y - mu), len(dt)) / (wsum_d + lam)
    # Average opponent strength faced (positive = faced good offenses / bad defenses)
    sched_o = np.bincount(oi, w * de[di], len(ot)) / np.maximum(wsum_o, 1e-9)
    sched_d = np.bincount(di, w * o[oi], len(dt)) / np.maximum(wsum_d, 1e-9)
    return {
        "mu": mu,
        "off": pd.DataFrame({"raw": raw_o, "adj": o, "opp_faced": sched_o}, index=ot),
        "def": pd.DataFrame({"raw": raw_d, "adj": de, "opp_faced": sched_d}, index=dt),
    }


def game_points(games: pd.DataFrame) -> pd.DataFrame:
    g = games.dropna(subset=["boxscore_id", "home_score", "away_score"])
    return pd.concat([
        pd.DataFrame({"offense": g["home"], "defense": g["away"], "points": g["home_score"], "week": g["week"]}),
        pd.DataFrame({"offense": g["away"], "defense": g["home"], "points": g["away_score"], "week": g["week"]}),
    ], ignore_index=True)


class Schedule:
    """SOS-adjusted ratings for pass yards/play, run yards/play and points/game."""

    FAMILIES = ("pass", "run", "points")

    def __init__(self, plays: pd.DataFrame, games: pd.DataFrame, cfg: dict):
        c = cfg.get("sos", {})
        self.enabled = c.get("enabled", True)
        self.clip = (c.get("min_factor", 0.85), c.get("max_factor", 1.15))
        live = plays[~plays["garbage"]]
        drop = live[live["dropback"]]
        self.fits = {
            "pass": fit_additive(drop, "yards", weight="w", lam=c.get("shrink_plays", 60.0)),
            "run": fit_additive(live[live["is_run"]], "yards", weight="w", lam=c.get("shrink_plays", 60.0)),
        }
        if {"home_score", "away_score"} <= set(games.columns):
            gp = game_points(games)
            if len(gp):
                self.fits["points"] = fit_additive(gp, "points", lam=c.get("shrink_games", 3.0))

    def factor(self, fam: str, side: str, team: str) -> float:
        """Multiplier that turns a raw-stat input into a schedule-adjusted one."""
        if not self.enabled or fam not in self.fits:
            return 1.0
        f = self.fits[fam]
        t = f[side]
        if team not in t.index:
            return 1.0
        mu = f["mu"]
        raw, adj = t.at[team, "raw"], t.at[team, "adj"]
        if mu + raw <= 0:
            return 1.0
        return float(np.clip((mu + adj) / (mu + raw), *self.clip))

    def table(self) -> pd.DataFrame:
        """One row per team: raw vs adjusted ratings and schedule faced."""
        rows = {}
        for fam, f in self.fits.items():
            for side in ("off", "def"):
                t = f[side]
                for team, r in t.iterrows():
                    x = rows.setdefault(team, {"team": team})
                    x[f"{side}_{fam}_raw"] = r["raw"]
                    x[f"{side}_{fam}_adj"] = r["adj"]
                    x[f"{side}_{fam}_sched"] = r["opp_faced"]
        return pd.DataFrame(rows.values()).sort_values("team")
