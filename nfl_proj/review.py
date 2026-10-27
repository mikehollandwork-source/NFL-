"""Weekly loss review: tag every graded bet with why it won or lost, and keep
running splits so rule/model changes are made from patterns, not one week.

Causes (losses):
  coin_flip   lost by a hair (<= 1 for counts, <= 10% of the line for yards)
  role        snap share fell 20+ points below the player's season norm
  volume      usage (targets / carries / pass attempts) missed the projection by 30%+ in the losing direction
  efficiency  usage within range, per-touch production decided it (mostly variance)
  market      closing line moved against us (book knew something)
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .picks import STATS

USAGE_PROJ = {"targets": "targets", "rush_att": "carries", "pass_att": "pass_att"}
COUNT_STATS = {"receptions", "carries", "completions", "targets"}


def _proj(paper_dir: Path, out_dir: Path, week: int) -> pd.DataFrame:
    f = paper_dir / f"week_{week:02d}_proj.csv"
    if f.exists():
        return pd.read_csv(f)
    f = out_dir / f"week_{week:02d}_projections.csv"   # fallback: last manual weekly run
    return pd.read_csv(f) if f.exists() else pd.DataFrame()


def tag(graded: pd.DataFrame, player_games: pd.DataFrame, proj: pd.DataFrame, week: int) -> pd.DataFrame:
    g = graded.copy()
    pg = player_games.copy()
    if "off_pct" in pg and pg["off_pct"].max() > 1.5:   # stored as 0-100
        pg["off_pct"] = pg["off_pct"] / 100
    pg_w = pg[pg["week"] == week]
    prior = pg[pg["week"] < week]
    norm_snap = prior.groupby("player_id")["off_pct"].mean() if "off_pct" in prior else pd.Series(dtype=float)
    causes, usage_a, usage_p, snap_a, snap_n = [], [], [], [], []
    for r in g.itertuples():
        col, ucol, _ = STATS[r.stat]
        a = pg_w[pg_w["player_id"] == r.player_id]
        ua = float(a[ucol].sum()) if len(a) else np.nan
        pr = proj[proj["player_id"] == r.player_id] if len(proj) else proj
        up = float(pr[USAGE_PROJ[ucol]].iloc[0]) if len(pr) and USAGE_PROJ[ucol] in pr else np.nan
        sa = float(a["off_pct"].iloc[0]) if len(a) and "off_pct" in a else np.nan
        sn = float(norm_snap.get(r.player_id, np.nan))
        usage_a.append(ua); usage_p.append(up); snap_a.append(sa); snap_n.append(sn)
        if r.result != "loss":
            causes.append("" if r.result != "win" else "win")
            continue
        miss = abs(r.actual - r.line)
        clv = getattr(r, "clv_line", np.nan)
        if (r.stat in COUNT_STATS and miss <= 1) or (r.stat not in COUNT_STATS and miss <= 0.1 * r.line):
            c = "coin_flip"
        elif pd.notna(sa) and pd.notna(sn) and sn - sa >= 0.20:
            c = "role"
        elif pd.notna(ua) and pd.notna(up) and up > 0 and (
                (r.side == "over" and ua < 0.7 * up) or (r.side == "under" and ua > 1.3 * up)):
            c = "volume"
        elif pd.notna(clv) and clv < 0:
            c = "market"
        else:
            c = "efficiency"
        causes.append(c)
    g["cause"] = causes
    g["usage_actual"], g["usage_proj"], g["snap_actual"], g["snap_norm"] = usage_a, usage_p, snap_a, snap_n
    return g


FIXABLE = {"role": "availability / depth-chart inputs", "volume": "share model (targets / carries)",
           "market": "information the book had"}


def report(week: int, tagged: pd.DataFrame, paper_dir: Path) -> str:
    d = tagged[tagged["result"].isin(["win", "loss"])]
    w, l = int((d["result"] == "win").sum()), int((d["result"] == "loss").sum())
    lines = [f"# Week {week} review", "", f"Record {w}-{l}, {tagged['profit'].sum():+.2f}u", ""]
    losses = d[d["result"] == "loss"]
    if len(losses):
        lines += ["## Losses by cause", "", "| Cause | n | Fixable? |", "|---|---|---|"]
        for c, n in losses["cause"].value_counts().items():
            lines.append(f"| {c} | {n} | {FIXABLE.get(c, 'no (variance)')} |")
        lines += ["", "| Player | Prop | Line | Actual | Usage proj → actual | Snap norm → actual | Cause |",
                  "|---|---|---|---|---|---|---|"]
        for r in losses.itertuples():
            lines.append(f"| {r.player} | {r.stat} {r.side} | {r.line:g} | {r.actual:g} | "
                         f"{r.usage_proj:.1f} → {r.usage_actual:g} | {r.snap_norm:.0%} → {r.snap_actual:.0%} | {r.cause} |"
                         .replace("nan", "–"))
    if "clv_line" in d and d["clv_line"].notna().any():
        c = d["clv_line"].dropna()
        lines += ["", f"Closing line: beat {int((c > 0).sum())}, same {int((c == 0).sum())}, worse {int((c < 0).sum())}"
                  " (line only; prices need ODDS_API_KEY)"]
    # Running splits across every graded week
    allg = [pd.read_csv(f) for f in sorted(paper_dir.glob("week_*_graded.csv"))]
    if allg:
        a = pd.concat(allg)
        a = a[a["result"].isin(["win", "loss"])]
        a["won"] = (a["result"] == "win").astype(float)
        a["p_bucket"] = pd.cut(a["p_cal"], [0, .58, .62, .66, 1], labels=["<58%", "58-62%", "62-66%", "66%+"])
        lines += ["", "## Season to date (bets)", "", "| Split | n | Hit | Model said |", "|---|---|---|---|"]
        for key in (["stat", "side"], ["p_bucket"]):
            for k, x in a.groupby(key, observed=True):
                k = " ".join(map(str, k)) if isinstance(k, tuple) else str(k)
                lines.append(f"| {k} | {len(x)} | {x['won'].mean():.0%} | {x['p_cal'].mean():.0%} |")
    led = paper_dir / "calls_ledger.csv"
    if led.exists():
        c = pd.read_csv(led)
        c = c[c["result"].isin(["right", "wrong"])]
        c["ok"] = (c["result"] == "right").astype(float)
        lines += ["", "## Season to date (every posted line's lean)", "", "| Stat | Side | n | Right |", "|---|---|---|---|"]
        for (s, sd), x in c.groupby(["stat", "lean"]):
            lines.append(f"| {s} | {sd} | {len(x)} | {x['ok'].mean():.0%} |")
    lines += ["", "Change rule: act only on a pattern that holds 3+ weeks (~100 bets) AND passes the 2021-25 backtest."]
    return "\n".join(lines) + "\n"


def run(week: int, graded: pd.DataFrame, player_games: pd.DataFrame, paper_dir: Path, out_dir: Path) -> str:
    t = tag(graded, player_games, _proj(paper_dir, out_dir, week), week)
    t.to_csv(paper_dir / f"week_{week:02d}_graded.csv", index=False)
    md = report(week, t, paper_dir)
    (paper_dir / f"week_{week:02d}_review.md").write_text(md)
    return md
