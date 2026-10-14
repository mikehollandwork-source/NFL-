"""The five strongest data-led projections per game.

A pick is a direction (over / under) on a player stat against a baseline:
your line from ``data/manual/prop_lines.csv`` when you've entered one,
otherwise the player's own recency-weighted average this season (roughly
where a sportsbook line starts).

To qualify:
  * at least ``picks.min_games`` games played this season
  * usage gate: for an over, carries (rushing stats) or targets (receiving
    stats) must be trending up into the game; for an under, trending down.
    Exempt: superstars with consistent action (top share of the team's
    carries / targets with low game-to-game variation) and starting QBs.
  * the simulation puts the chance of beating the baseline in that
    direction at ``picks.min_prob`` or better
  * at least ``picks.min_signals`` independent signals point the same way

Signals: the opponent's bucket matchup (yards per play allowed in the
plays this team runs), the receiver factor (available corners, shadow,
position-group weakness), comparable offenses vs this defense, the usage
trend, game script, and the projected team total vs the team's average.

Score = edge x sample reliability x signal agreement, where edge is the
probability gained from the projection moving off the baseline with the
stat's skew removed (yardage stats land under their own average more than
half the time, which is not an edge). Fringe players are excluded
(``picks.min_targets`` / ``min_carries`` per game; QB rushing excluded). One pick per player; the top five per game are kept.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

# prop stat -> (player_games column, usage column, family)
STATS = {
    "rush_yds": ("rush_yds", "rush_att", "run"),
    "carries": ("rush_att", "rush_att", "run"),
    "rec_yds": ("rec_yds", "targets", "pass"),
    "receptions": ("rec", "targets", "pass"),
    "targets": ("targets", "targets", "pass"),
    "pass_yds": ("pass_yds", "pass_att", "qb"),
    "completions": ("pass_cmp", "pass_att", "qb"),
}


def usage_trend(series: pd.Series) -> dict:
    """``series``: usage by week, oldest first (games the player played)."""
    s = series.astype(float)
    n = len(s)
    out = {"n": n, "last2": s.iloc[-2:].mean() if n else np.nan, "prior": np.nan, "dir": "flat", "cv": np.nan}
    if n >= 2:
        out["cv"] = float(s.std(ddof=0) / s.mean()) if s.mean() > 0 else np.nan
    if n < 3:
        return out
    prior = s.iloc[:-2].mean()
    out["prior"] = prior
    slope = np.polyfit(np.arange(3), s.iloc[-3:].values, 1)[0]
    tol = 0.05 * max(s.mean(), 1e-9)  # a slope smaller than this is flat
    if out["last2"] >= 1.1 * prior or (slope > tol and s.iloc[-1] >= s.mean()):
        out["dir"] = "up"
    elif out["last2"] <= 0.9 * prior or (slope < -tol and s.iloc[-1] <= s.mean()):
        out["dir"] = "down"
    return out


def _weighted_avg(df: pd.DataFrame, col: str, hl: float) -> float:
    last = df["week"].max()
    w = 0.5 ** ((last - df["week"]) / hl)
    return float(np.average(df[col].astype(float), weights=w))


def pick_week(proj, props: pd.DataFrame, player_games: pd.DataFrame, week: int, cfg: dict,
              lines: pd.DataFrame | None = None) -> pd.DataFrame:
    c = cfg.get("picks", {})
    min_games = c.get("min_games", 3)
    min_prob = c.get("min_prob", 0.55)
    min_edge = c.get("min_edge", 0.06)
    min_tgt, min_car = c.get("min_targets", 4.0), c.get("min_carries", 8.0)
    min_signals = c.get("min_signals", 2)
    per_game = c.get("per_game", 5)
    star_tgt, star_car, star_cv = c.get("star_target_share", 0.25), c.get("star_carry_share", 0.55), c.get("star_cv", 0.35)
    hl = cfg["weighting"]["half_life_weeks"]
    pg = player_games[player_games["week"] < week]
    team_tot = pg.groupby(["team", "week"])[["targets", "rush_att"]].sum()
    user = {}
    if lines is not None and not lines.empty:
        for r in lines.itertuples():
            try:
                user[(r.player, r.stat)] = float(r.line)
            except (TypeError, ValueError):
                pass

    rows = []
    cache = {}
    cand = props[props["stat"].isin(list(STATS))]
    sample_col = cand["_samples"] if "_samples" in cand else None
    for i, r in zip(cand.index, cand.drop(columns=["_samples"], errors="ignore").itertuples()):
        col, ucol, fam = STATS[r.stat]
        hist = pg[(pg["player_id"] == r.player_id) & (pg["team"] == r.team)].sort_values("week")
        hist = hist[hist[ucol] > 0] if fam != "qb" else hist[hist["pass_att"] >= 10]
        if len(hist) < min_games:
            continue
        line = user.get((r.player, r.stat))
        baseline = line if line is not None else _weighted_avg(hist, col, hl)
        if sample_col is None:
            continue
        samples = np.asarray(sample_col.loc[i], dtype=float)
        # Usage floor: real props only
        avg_use = float(hist[ucol].mean())
        if avg_use < {"targets": min_tgt, "rush_att": min_car, "pass_att": 20}[ucol]:
            continue
        if fam == "run" and str(r.pos).upper() == "QB":
            continue  # QB rushing is mostly scrambles: too noisy for a pick
        mean = float(samples.mean())
        direction = "over" if mean > baseline else "under"
        if direction == "over":
            prob = float((samples > baseline).mean())
            edge = prob - float((samples > mean).mean())
        else:
            prob = float((samples < baseline).mean())
            edge = prob - float((samples < mean).mean())
        # ``edge`` is the probability gained from the projection moving off the
        # baseline, with the stat's skew removed (a skewed stat lands under its
        # own average more than half the time, which isn't an edge).
        if prob < min_prob or edge < min_edge:
            continue

        # Usage gate
        tr = usage_trend(hist.set_index("week")[ucol])
        share_col = "targets" if ucol == "targets" else "rush_att"
        if fam == "qb":
            star, gate = True, True
        else:
            tt = team_tot.loc[r.team][share_col].reindex(hist["week"]).replace(0, np.nan)
            share = float((hist.set_index("week")[share_col] / tt).mean())
            star = (share >= (star_tgt if share_col == "targets" else star_car)) and \
                (pd.notna(tr["cv"]) and tr["cv"] <= star_cv)
            gate = star or (tr["dir"] == "up" if direction == "over" else tr["dir"] == "down")
        if not gate:
            continue

        # Signals
        key = (r.team, r.opp)
        if key not in cache:
            cache[key] = _team_signals(proj, r.team, r.opp, week)
        ts = cache[key]
        sign = 1 if direction == "over" else -1
        sig = []
        fam_key = "run" if fam == "run" else "pass"
        if sign * (ts["matchup"][fam_key] - 1) >= 0.02:
            sig.append(f"matchup {fam_key} x{ts['matchup'][fam_key]:.2f}")
        if fam == "pass":
            rf = ts["receiver"].get(r.player_id, 1.0)
            if sign * (rf - 1) >= 0.02:
                sig.append(f"coverage x{rf:.2f}")
        if sign * (ts["comps"][fam_key] - 1) >= 0.02:
            sig.append(f"similar offenses x{ts['comps'][fam_key]:.2f}")
        if fam != "qb" and ((direction == "over" and tr["dir"] == "up") or (direction == "under" and tr["dir"] == "down")):
            sig.append(f"usage trending {tr['dir']} ({tr['prior']:.1f} → {tr['last2']:.1f})")
        script = ts["dropback_shift"] * (1 if fam in ("pass", "qb") else -1)
        if sign * script >= 0.008:
            sig.append(f"game script {ts['dropback_shift']:+.1%} dropbacks")
        if pd.notna(ts["pts_vs_avg"]) and sign * ts["pts_vs_avg"] >= 2:
            sig.append(f"team total {ts['pts_vs_avg']:+.1f} vs its average")
        if len(sig) < min_signals:
            continue
        reliability = min(1.0, len(hist) / 4)
        score = (2 * edge) * reliability * (0.6 + 0.1 * len(sig))
        rows.append({"week": week, "game": " @ ".join(sorted([r.team, r.opp])), "team": r.team, "opp": r.opp,
                     "player": r.player, "player_id": r.player_id, "pos": r.pos, "stat": r.stat,
                     "direction": direction, "baseline": round(baseline, 1),
                     "baseline_source": "your line" if line is not None else "season avg",
                     "projected_median": round(float(np.median(samples)), 1),
                     "projected_mean": round(mean, 1), "prob": round(prob, 3), "edge": round(edge, 3),
                     "score": round(score, 3), "star": star,
                     "usage": f"{tr['dir']} (last 2: {tr['last2']:.1f}, before: {tr['prior']:.1f})"
                     if pd.notna(tr["prior"]) else "n/a",
                     "signals": "; ".join(sig), "n_signals": len(sig)})
    if not rows:
        return pd.DataFrame()
    out = pd.DataFrame(rows).sort_values("score", ascending=False)
    out = out.drop_duplicates(["player_id", "team"])  # one pick per player
    out["rank"] = out.groupby("game")["score"].rank(ascending=False, method="first").astype(int)
    return out[out["rank"] <= per_game].sort_values(["game", "rank"]).reset_index(drop=True)


def _team_signals(proj, team: str, opp: str, week: int) -> dict:
    pmix, _ = proj.mix(team, "pass", opp)
    rmix, _ = proj.mix(team, "run", opp)

    def avg(mix, family):
        tot = sum(mix.values()) or 1.0
        return sum(v * proj.bucket_matchup(team, opp, family, b, week)["m_ypp"] for b, v in mix.items()) / tot
    adj = proj.adjustments(team, opp, week)
    cmp = proj.comps.effect(team, opp)
    rf, _ = proj.corner_factors(team, opp)
    pts = proj.pts_override.get((team, opp))
    g = proj.games.dropna(subset=["boxscore_id"])
    scored = pd.concat([g[g["home"] == team]["home_score"], g[g["away"] == team]["away_score"]])
    avg_pts = float(scored.mean()) if len(scored) else np.nan
    return {"matchup": {"pass": avg(pmix, "pass"), "run": avg(rmix, "run")},
            "comps": {"pass": cmp["pass"], "run": cmp["run"]}, "receiver": rf,
            "dropback_shift": adj.get("dropback_shift", 0.0),
            "pts_vs_avg": (pts - avg_pts) if pts is not None and pd.notna(avg_pts) else np.nan}


def grade(picks: pd.DataFrame, player_games: pd.DataFrame) -> pd.DataFrame:
    """Attach actual results. A pick on a player who didn't play is void."""
    if picks.empty:
        return picks
    out = []
    for r in picks.itertuples():
        col = STATS[r.stat][0]
        a = player_games[(player_games["player_id"] == r.player_id) & (player_games["week"] == r.week)]
        if a.empty:
            out.append({**r._asdict(), "actual": np.nan, "result": "void"})
            continue
        v = float(a[col].sum())
        hit = v > r.baseline if r.direction == "over" else v < r.baseline
        push = v == r.baseline
        out.append({**r._asdict(), "actual": v, "result": "push" if push else ("hit" if hit else "miss")})
    return pd.DataFrame(out).drop(columns=["Index"], errors="ignore")
