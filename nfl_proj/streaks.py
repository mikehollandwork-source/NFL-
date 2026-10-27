"""How much of a player's recent hot (or cold) streak carries into his next game.

For every player-game in the data, with at least two earlier games as a
baseline:
  x = his average over the last two games  -  his average before them
  y = his next game                         -  his average before the two games
The weighted slope of y on x is the share of a two-game streak that
persists. Measured separately for efficiency (yards per target / carry,
long plays capped) and volume (targets / carries). The projector keeps only
that share of a recent streak.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

CAP = {"rec": 40.0, "rush": 30.0}  # long plays capped when measuring efficiency


def player_game_table(plays: pd.DataFrame) -> pd.DataFrame:
    p = plays[~plays["no_play"].astype(bool)]
    rec = p[(p["play_type"] == "pass") & p["target_id"].notna()].copy()
    rec["yc"] = rec["yards"].fillna(0).clip(upper=CAP["rec"])
    rush = p[(p["play_type"] == "run") & p["rusher_id"].notna()].copy()
    rush["yc"] = rush["yards"].fillna(0).clip(upper=CAP["rush"])
    a = rec.groupby(["target_id", "offense", "season", "week"]).agg(n=("yc", "size"), y=("yc", "sum")).reset_index()
    a = a.rename(columns={"target_id": "player_id"}).assign(kind="rec")
    b = rush.groupby(["rusher_id", "offense", "season", "week"]).agg(n=("yc", "size"), y=("yc", "sum")).reset_index()
    b = b.rename(columns={"rusher_id": "player_id"}).assign(kind="rush")
    return pd.concat([a, b], ignore_index=True)


def measure(plays: pd.DataFrame, min_n: int = 3) -> dict:
    t = player_game_table(plays)
    rows = []
    for (pid, team, season, kind), g in t.groupby(["player_id", "offense", "season", "kind"]):
        g = g.sort_values("week").reset_index(drop=True)
        for i in range(4, len(g)):
            base, win, nxt = g.iloc[: i - 2], g.iloc[i - 2: i], g.iloc[i]
            if base["n"].sum() < 2 * min_n or win["n"].sum() < 2 * min_n or nxt["n"] < min_n:
                continue
            b_eff = base["y"].sum() / base["n"].sum()
            rows.append({"kind": kind,
                         "x_eff": win["y"].sum() / win["n"].sum() - b_eff, "y_eff": nxt["y"] / nxt["n"] - b_eff,
                         "x_vol": win["n"].mean() - base["n"].mean(), "y_vol": nxt["n"] - base["n"].mean(),
                         "w": nxt["n"]})
    d = pd.DataFrame(rows)
    out = {}
    for kind in ("rec", "rush"):
        k = d[d["kind"] == kind]
        for m in ("eff", "vol"):
            if len(k) < 50:
                continue
            x, y, w = k[f"x_{m}"].to_numpy(float), k[f"y_{m}"].to_numpy(float), k["w"].to_numpy(float)
            X = np.column_stack([np.ones(len(x)), x])
            W = np.diag(w)
            coef = np.linalg.solve(X.T @ W @ X, X.T @ W @ y)
            resid = y - X @ coef
            se = np.sqrt(np.diag(np.linalg.inv(X.T @ W @ X)) * (w * resid ** 2).sum() / (len(y) - 2))
            out[f"{kind}_{m}"] = {"persist": float(np.clip(coef[1], 0, 1)), "slope": float(coef[1]),
                                  "se": float(se[1]), "n": len(k)}
    return out
