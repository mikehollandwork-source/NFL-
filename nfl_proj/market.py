"""Betting-market team totals (used only for teams the market reads well).

nflverse's schedule carries the closing spread and over/under for every
game. From them:

  implied total   (total + spread) / 2 for the home team, (total - spread) / 2
                  for the away team (``spread_line`` > 0 = home favored)
  team miss       points scored minus implied total in each played game.
                  Teams that keep falling short of (or beating) their implied
                  totals get that history as a correction, shrunk toward zero
                  by ``market.miss_shrink_games`` because a few games of
                  misses are mostly noise and the market already adjusts.

Only the implied team total is used, and only for teams that consistently
land on it: within ``market.hit_tolerance`` points in at least
``market.min_hit_rate`` of at least ``market.min_games`` games. For those
teams the projector blends the implied total with its own model total
(``market.weight``) and scales touchdown rates, and a little of the yardage,
so the simulated team total lands on the blend. Everyone else is projected
from the model alone. The spread is never used (game script comes from the
model's own projected margin).
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def implied_totals(games: pd.DataFrame) -> pd.DataFrame:
    g = games.dropna(subset=["spread_line", "total_line"])
    home = pd.DataFrame({"week": g["week"], "team": g["home"], "opp": g["away"],
                         "implied": (g["total_line"] + g["spread_line"]) / 2,
                         "spread": g["spread_line"], "points": g["home_score"],
                         "played": g["boxscore_id"].notna()})
    away = pd.DataFrame({"week": g["week"], "team": g["away"], "opp": g["home"],
                         "implied": (g["total_line"] - g["spread_line"]) / 2,
                         "spread": -g["spread_line"], "points": g["away_score"],
                         "played": g["boxscore_id"].notna()})
    out = pd.concat([home, away], ignore_index=True)
    out["miss"] = np.where(out["played"], out["points"] - out["implied"], np.nan)
    return out


def team_misses(totals: pd.DataFrame, before_week: int, k: float, tol: float = 4.0) -> pd.DataFrame:
    """Per team: games, average miss vs implied, how often they fell short,
    and the shrunk correction used in projections."""
    h = totals[totals["played"] & (totals["week"] < before_week)]
    g = h.groupby("team").agg(games=("miss", "size"), avg_miss=("miss", "mean"),
                              abs_miss=("miss", lambda s: s.abs().mean()),
                              under_rate=("miss", lambda s: (s < 0).mean()),
                              implied_avg=("implied", "mean"), scored_avg=("points", "mean"))
    g["correction"] = g["avg_miss"] * g["games"] / (g["games"] + k)
    g["hit_rate"] = h.groupby("team")["miss"].apply(lambda s: (s.abs() <= tol).mean()).reindex(g.index)
    return g.reset_index()


class Market:
    def __init__(self, games: pd.DataFrame, cfg: dict):
        c = cfg.get("market", {})
        self.enabled = c.get("enabled", True) and {"spread_line", "total_line"} <= set(games.columns)
        self.weight = c.get("weight", 0.6)
        self.tol = c.get("hit_tolerance", 4.0)
        self.min_hit_rate = c.get("min_hit_rate", 0.6)
        self.min_games = c.get("min_games", 4)
        self.k = c.get("miss_shrink_games", 6.0)
        self.yards_elasticity = c.get("yards_elasticity", 0.3)
        self.clip = (c.get("min_factor", 0.6), c.get("max_factor", 1.6))
        self.totals = implied_totals(games) if self.enabled else pd.DataFrame()
        self._miss = {}

    def misses(self, week: int) -> pd.DataFrame:
        if week not in self._miss:
            m = team_misses(self.totals, week, self.k, self.tol) if self.enabled else pd.DataFrame()
            if not m.empty:
                m["qualifies"] = (m["games"] >= self.min_games) & (m["hit_rate"] >= self.min_hit_rate)
            self._miss[week] = m
        return self._miss[week]

    def line(self, team: str, week: int) -> dict | None:
        if not self.enabled:
            return None
        r = self.totals[(self.totals["team"] == team) & (self.totals["week"] == week)]
        if r.empty or pd.isna(r["implied"].iloc[0]):
            return None
        m = self.misses(week)
        mrow = m[m["team"] == team]
        if mrow.empty or not bool(mrow["qualifies"].iloc[0]):
            return None  # market hasn't read this team consistently: model only
        return {"implied": float(r["implied"].iloc[0]), "spread": float(r["spread"].iloc[0]),
                "correction": 0.0, "target": float(r["implied"].iloc[0]),
                "hit_rate": float(mrow["hit_rate"].iloc[0]), "abs_miss": float(mrow["abs_miss"].iloc[0]),
                "avg_miss": float(mrow["avg_miss"].iloc[0]) if len(mrow) else np.nan,
                "under_rate": float(mrow["under_rate"].iloc[0]) if len(mrow) else np.nan,
                "games": int(mrow["games"].iloc[0]) if len(mrow) else 0}

    def blend(self, line: dict, model_pts: float) -> dict:
        """Blend market and model points and return the scaling factors."""
        target = self.weight * line["target"] + (1 - self.weight) * model_pts
        td = float(np.clip(target / model_pts, *self.clip)) if model_pts > 0 else 1.0
        return {**line, "model_pts": model_pts, "blended_pts": target, "td_factor": td,
                "ypp_factor": td ** self.yards_elasticity}
