"""Test the "coaches cut what failed and call more of what worked" idea.

For every team, game and play bucket (e.g. pass_deep_right, run_inside_left):

  x = team's negative-play rate in that game  -  bucket's negative-play rate
      (positive = the bucket worked better than the team's other calls)
  y = relative change in how often the bucket is called next game vs the
      team's season-to-date share

If coaches really lean into what worked, the weighted slope of y on x is
positive. The slope (beta) is what the projection applies, scaled down when
it is not statistically clear.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .playparse import PASS_BUCKETS, RUN_BUCKETS


def _family(bucket: str) -> str:
    return "pass" if bucket.startswith("pass") else "run"


def game_bucket_table(plays: pd.DataFrame) -> pd.DataFrame:
    p = plays[~plays["garbage"] & plays["bucket"].notna()].copy()
    p["family"] = p["bucket"].map(_family)
    g = p.groupby(["offense", "week", "family", "bucket"]).agg(
        n=("negative", "size"), neg=("negative", "mean"), epa=("epa", "mean")).reset_index()
    fam = p.groupby(["offense", "week", "family"]).agg(
        fam_n=("negative", "size"), team_neg=("negative", "mean")).reset_index()
    g = g.merge(fam, on=["offense", "week", "family"])
    # Fill missing buckets with zero counts so a bucket that disappears counts.
    full = []
    for (team, week, family), sub in g.groupby(["offense", "week", "family"]):
        buckets = PASS_BUCKETS if family == "pass" else RUN_BUCKETS
        sub = sub.set_index("bucket").reindex(buckets)
        sub[["offense", "week", "family"]] = team, week, family
        sub["n"] = sub["n"].fillna(0)
        sub["fam_n"] = sub["fam_n"].ffill().bfill()
        sub["team_neg"] = sub["team_neg"].ffill().bfill()
        full.append(sub.reset_index())
    g = pd.concat(full, ignore_index=True)
    g["share"] = g["n"] / g["fam_n"]
    return g


def adaptation_samples(plays: pd.DataFrame, min_plays: int = 3) -> pd.DataFrame:
    g = game_bucket_table(plays)
    rows = []
    for (team, bucket), sub in g.groupby(["offense", "bucket"]):
        sub = sub.sort_values("week").reset_index(drop=True)
        for i in range(len(sub) - 1):
            cur, nxt = sub.iloc[i], sub.iloc[i + 1]
            prior = sub.iloc[: i + 1]
            prior_share = prior["n"].sum() / prior["fam_n"].sum()
            if cur["n"] < min_plays or prior_share < 0.02:
                continue
            rows.append({
                "team": team, "bucket": bucket, "week": cur["week"], "next_week": nxt["week"],
                "n": cur["n"], "x": cur["team_neg"] - cur["neg"],
                "y": (nxt["share"] - prior_share) / prior_share,
            })
    return pd.DataFrame(rows)


def estimate(plays: pd.DataFrame, min_plays: int = 3) -> dict:
    s = adaptation_samples(plays, min_plays)
    if len(s) < 30:
        return {"beta": 0.0, "se": np.nan, "t": 0.0, "n": len(s),
                "verdict": "not enough data yet (need 30+ bucket-games)"}
    w = s["n"].to_numpy(float)
    X = np.column_stack([np.ones(len(s)), s["x"].to_numpy(float)])
    y = s["y"].to_numpy(float)
    W = np.diag(w)
    xtwx = X.T @ W @ X
    coef = np.linalg.solve(xtwx, X.T @ W @ y)
    resid = y - X @ coef
    sigma2 = (w * resid ** 2).sum() / (len(s) - 2)
    se = np.sqrt(np.diag(np.linalg.inv(xtwx)) * sigma2)
    beta, t = coef[1], coef[1] / se[1]
    if t > 2:
        verdict = "supported: teams call more of what worked last game"
    elif t < -2:
        verdict = "contradicted: teams call LESS of what worked (regression / opponent effects)"
    else:
        verdict = "not clearly supported: last game's results barely change next game's calls"
    return {"beta": float(beta), "se": float(se[1]), "t": float(t), "n": len(s), "verdict": verdict}


def effective_strength(est: dict, cfg: dict) -> float:
    a = cfg["adaptation"]
    if a["mode"] == "off":
        return 0.0
    if a["mode"] == "assume":
        return float(a["assumed_strength"])
    clarity = min(1.0, abs(est.get("t", 0.0)) / 2.0)
    return float(est.get("beta", 0.0)) * clarity


def last_game_signal(plays: pd.DataFrame, team: str, min_plays: int) -> dict[str, float]:
    """x for each bucket in the team's most recent game."""
    g = game_bucket_table(plays[plays["offense"] == team])
    if g.empty:
        return {}
    last = g[g["week"] == g["week"].max()]
    return {r.bucket: r.team_neg - r.neg for r in last.itertuples()
            if r.n >= min_plays and not pd.isna(r.neg)}
