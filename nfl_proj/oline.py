"""Offensive line injuries.

Starters are linemen (T / G / C / OL) who played 60%+ of the snaps in at
least half of the team's games. For every team-game in 2025 and 2026 the
number of starters who didn't play is compared with how the offense did
against its own norm in its other games (sack rate, yards per dropback,
yards per carry). The per-missing-starter slopes, scaled down when they
aren't statistically clear, are applied for starters listed out this week.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

OL = {"T", "G", "C", "OL", "OT", "OG"}


def starters(player_games: pd.DataFrame, team: str) -> pd.DataFrame:
    pg = player_games[(player_games["team"] == team) & player_games["pos"].isin(OL)]
    n_games = player_games[player_games["team"] == team]["boxscore_id"].nunique()
    if pg.empty or n_games == 0:
        return pd.DataFrame(columns=["player_id", "player", "games"])
    reg = pg[pg["off_pct"] >= 60].groupby(["player_id", "player"]).size().reset_index(name="games")
    return reg[reg["games"] >= max(1, int(np.ceil(0.5 * n_games)))]


def team_game_table(plays: pd.DataFrame, player_games: pd.DataFrame) -> pd.DataFrame:
    p = plays[plays["play_type"].isin(["pass", "run", "sack", "scramble"]) & ~plays["no_play"].astype(bool)
              & plays["offense"].notna()]
    rows = []
    for team in p["offense"].unique():
        st = starters(player_games, team)
        tp = p[p["offense"] == team]
        played = player_games[(player_games["team"] == team) & player_games["pos"].isin(OL)]
        for box, g in tp.groupby("boxscore_id"):
            on = set(played[played["boxscore_id"] == box]["player_id"])
            missing = int((~st["player_id"].isin(on)).sum()) if len(st) else 0
            db = g[g["play_type"].isin(["pass", "sack", "scramble"])]
            ru = g[g["play_type"] == "run"]
            rows.append({"team": team, "boxscore_id": box, "missing": missing,
                         "sack": (db["play_type"] == "sack").mean() if len(db) else np.nan,
                         "pass": db["yards"].fillna(0).mean() if len(db) else np.nan,
                         "run": ru["yards"].fillna(0).mean() if len(ru) else np.nan,
                         "n_db": len(db), "n_run": len(ru)})
    t = pd.DataFrame(rows)
    for c in ("sack", "pass", "run"):
        tot = t.groupby("team")[c].transform("sum")
        cnt = t.groupby("team")[c].transform("count")
        t[f"{c}_res"] = t[c] - (tot - t[c]) / (cnt - 1).replace(0, np.nan)
    return t


def estimate(tables: list[tuple[pd.DataFrame, pd.DataFrame]]) -> dict:
    """Per-missing-starter effect on sack rate, yards/dropback, yards/carry."""
    t = pd.concat([team_game_table(p, pg) for p, pg in tables], ignore_index=True)
    out = {"n_games": len(t), "games_with_missing": int((t["missing"] > 0).sum())}
    for c, wcol in (("sack", "n_db"), ("pass", "n_db"), ("run", "n_run")):
        d = t.dropna(subset=[f"{c}_res"])
        if len(d) < 50:
            continue
        x, y, w = d["missing"].to_numpy(float), d[f"{c}_res"].to_numpy(float), d[wcol].to_numpy(float)
        X = np.column_stack([np.ones(len(x)), x])
        W = np.diag(w)
        coef = np.linalg.solve(X.T @ W @ X, X.T @ W @ y)
        resid = y - X @ coef
        se = np.sqrt(np.diag(np.linalg.inv(X.T @ W @ X)) * (w * resid ** 2).sum() / (len(y) - 2))
        out[c] = {"per_starter": float(coef[1]), "t": float(coef[1] / se[1]) if se[1] > 0 else 0.0,
                  "base": float(np.average(d[c], weights=w))}
    return out


def effect(est: dict, n_missing: int) -> dict:
    """Multipliers on sack rate, yards per dropback and yards per carry."""
    out = {"sack": 1.0, "pass": 1.0, "run": 1.0}
    if n_missing <= 0:
        return out
    for c in out:
        e = est.get(c)
        if not e or not e["base"]:
            continue
        slope = e["per_starter"] * min(1.0, abs(e["t"]) / 2.0)
        lo, hi = (0.8, 1.6) if c == "sack" else (0.85, 1.05)
        out[c] = float(np.clip(1 + slope * min(n_missing, 3) / e["base"], lo, hi))
    return out
