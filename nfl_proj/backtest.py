"""Replay past weeks with only the data available before each one.

For each week W: cut every table to what was known before W (see
pipeline.as_of), project W, then compare with what happened.

Scored:
  picks          the top-5-per-game picks: hit / miss / void (didn't play)
  all calls      every over/under call the picks logic would consider, before
                 the usage gate, signal and top-5 filters (to show whether the
                 filters add anything)
  projections    mean absolute error of the model's player projections vs the
                 naive baseline (the player's own season average so far)
  team totals    model points vs actual, alongside the market implied total
                 and the team's season average so far
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .picks import STATS, grade, pick_week


def _naive_calls(proj, props, pg, week, cfg):
    """Every qualifying-volume call with no gate / signal / top-5 filter."""
    c = dict(cfg)
    c["picks"] = {**cfg.get("picks", {}), "min_signals": 0, "per_game": 999, "min_prob": 0.5, "min_edge": 0.0,
                  "star_target_share": 0.0, "star_carry_share": 0.0, "star_cv": 99}
    return pick_week(proj, props, pg, week, c)


def run(tables: dict, cfg: dict, paths: dict, weeks: list[int], n_sims: int = 2000, log=print) -> dict:
    from .market import implied_totals
    from .pipeline import run_week
    full_pg = tables["player_games"]
    picks, calls, proj_err, totals = [], [], [], []
    imp = implied_totals(tables["games"])
    for w in weeks:
        log(f"backtest: week {w} (data through week {w - 1})")
        r = run_week(tables, cfg, paths, w, asof=True, n_sims=n_sims, log=lambda *_: None)
        if not r["picks"].empty:
            picks.append(grade(r["picks"], full_pg))
        allc = _naive_calls(r["proj"], r["props"], r["tables"]["player_games"], w, cfg)
        if not allc.empty:
            calls.append(grade(allc, full_pg))
        # Projection accuracy vs naive season average
        prior = r["tables"]["player_games"]
        actual = full_pg[full_pg["week"] == w]
        wide = r["wide"]
        for stat, (col, ucol, _) in STATS.items():
            if stat not in wide:
                continue
            m = wide[["player_id", "team", stat]].rename(columns={stat: "proj"}).merge(
                actual[["player_id", "team", col] + ([ucol] if ucol != col else [])], on=["player_id", "team"])
            base = prior.groupby(["player_id", "team"])[col].mean().rename("naive")
            m = m.merge(base, left_on=["player_id", "team"], right_index=True)
            m = m[m[ucol] > 0]
            if len(m):
                proj_err.append({"week": w, "stat": stat, "n": len(m),
                                 "model_mae": float((m["proj"] - m[col]).abs().mean()),
                                 "naive_mae": float((m["naive"] - m[col]).abs().mean())})
        # Team totals
        g = tables["games"][tables["games"]["week"] == w]
        act = pd.concat([pd.DataFrame({"team": g["home"], "actual": g["home_score"]}),
                         pd.DataFrame({"team": g["away"], "actual": g["away_score"]})])
        tt = r["totals"].merge(act, on="team")
        tt = tt.merge(imp[imp["week"] == w][["team", "implied"]], on="team", how="left")
        pg_g = r["tables"]["games"].dropna(subset=["boxscore_id"])
        avg = pd.concat([pd.DataFrame({"team": pg_g["home"], "pts": pg_g["home_score"]}),
                         pd.DataFrame({"team": pg_g["away"], "pts": pg_g["away_score"]})]).groupby("team")["pts"].mean()
        tt["season_avg"] = tt["team"].map(avg)
        totals.append(tt)
    out = {"picks": pd.concat(picks, ignore_index=True) if picks else pd.DataFrame(),
           "calls": pd.concat(calls, ignore_index=True) if calls else pd.DataFrame(),
           "proj_err": pd.DataFrame(proj_err),
           "totals": pd.concat(totals, ignore_index=True) if totals else pd.DataFrame()}
    out["report"] = report(out, weeks)
    return out


def _with_base(df: pd.DataFrame, base_rates: pd.Series) -> pd.DataFrame:
    """Add the no-information hit rate for each call: how often that stat
    landed on that side of its baseline across all calls (skew included)."""
    d = df[df["result"].isin(["hit", "miss"])].copy()
    d["hit"] = d["result"].eq("hit")
    under = d["stat"].map(base_rates)
    d["base"] = np.where(d["direction"] == "under", under, 1 - under)
    return d


def _lift_table(d: pd.DataFrame, by) -> pd.DataFrame:
    return d.groupby(by, observed=True).apply(lambda g: pd.Series({
        "calls": len(g), "hit rate": g["hit"].mean(), "no-info rate": g["base"].mean(),
        "lift": g["hit"].mean() - g["base"].mean()}), include_groups=False)


def _rate(df: pd.DataFrame) -> str:
    d = df[df["result"].isin(["hit", "miss"])]
    if d.empty:
        return "—"
    h = (d["result"] == "hit").sum()
    return f"{h}/{len(d)} ({h / len(d):.0%})"


def report(o: dict, weeks: list[int]) -> str:
    out = ["# Backtest", "",
           f"Weeks {weeks[0]}-{weeks[-1]} replayed with only the data available before each week "
           "(play-by-play, stats, injury report, depth chart as of that week). Left out because they were "
           "gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual "
           "overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 "
           "produce none.", ""]
    p, c = o["picks"], o["calls"]
    out += ["## Picks (top 5 per game)", ""]
    if p.empty:
        out += ["No picks qualified.", ""]
    else:
        out.append(f"- **Overall: {_rate(p)}** (voids: {(p['result'] == 'void').sum()}, pushes: "
                   f"{(p['result'] == 'push').sum()})")
        for w, g in p.groupby("week"):
            out.append(f"- Week {w}: {_rate(g)}")
        for d, g in p.groupby("direction"):
            out.append(f"- {d}s: {_rate(g)}")
        out.append(f"- Rank 1 picks only: {_rate(p[p['rank'] == 1])}")
        out.append("")
        by = p[p["result"].isin(["hit", "miss"])].groupby("stat")["result"].apply(
            lambda s: f"{(s == 'hit').sum()}/{len(s)} ({(s == 'hit').mean():.0%})")
        out += ["By stat:", "", by.to_frame("hit rate").to_markdown(), ""]
    if not c.empty:
        out += ["## Every call, no filters (for comparison)", "",
                f"All over/under calls on players above the usage floor, before the trend gate, signal count "
                f"and top-5 cut: **{_rate(c)}**. If the picks above beat this, the filters are adding value.", ""]
        cc = c[c["result"].isin(["hit", "miss"])].copy()
        if len(cc) >= 40:
            cc["edge_bin"] = pd.qcut(cc["edge"], 4, duplicates="drop")
            t = cc.groupby("edge_bin", observed=True)["result"].apply(
                lambda s: f"{(s == 'hit').sum()}/{len(s)} ({(s == 'hit').mean():.0%})")
            out += ["Hit rate by model edge (quartiles): does a bigger edge win more often?", "",
                    t.to_frame("hit rate").to_markdown(), ""]
    if not c.empty:
        cc = c[c["result"].isin(["hit", "miss"])]
        base_rates = (cc["actual"] < cc["baseline"]).groupby(cc["stat"]).mean()
        dc = _with_base(c, base_rates)
        dc["trend"] = dc["usage"].astype(str).str.split(" ").str[0]
        dc["usage trend agrees"] = np.where(dc["direction"] == "over", dc["trend"].eq("up"), dc["trend"].eq("down"))
        out += ["## Does each filter add anything? (lift over a no-information call)", "",
                "`no-info rate` = how often a call on that side of the baseline would hit with no model at all "
                "(yardage stats land under their own average more often than not, so unders start ahead). "
                "`lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.", "",
                "Unfiltered calls overall:", "", _lift_table(dc.assign(all="all"), "all").to_markdown(floatfmt=".2f"), "",
                "Usage trend agrees with the call (the qualification rule):", "",
                _lift_table(dc, "usage trend agrees").to_markdown(floatfmt=".2f"), "",
                "Number of agreeing signals:", "", _lift_table(dc, "n_signals").to_markdown(floatfmt=".2f"), ""]
        if not p.empty:
            out += ["Top-5 picks:", "", _lift_table(_with_base(p, base_rates).assign(all="picks"), "all")
                    .to_markdown(floatfmt=".2f"), ""]
    e = o["proj_err"]
    if not e.empty:
        s = e.groupby("stat").apply(lambda d: pd.Series({
            "n": d["n"].sum(),
            "model_mae": np.average(d["model_mae"], weights=d["n"]),
            "naive_mae": np.average(d["naive_mae"], weights=d["n"])}), include_groups=False)
        s["model_better"] = s["model_mae"] < s["naive_mae"]
        out += ["## Player projections vs a naive season average", "",
                "Mean absolute error on players who got the ball (lower is better).", "",
                s.to_markdown(floatfmt=".2f"), ""]
    t = o["totals"]
    if not t.empty:
        t = t.dropna(subset=["actual"])
        row = lambda col: float((t[col] - t["actual"]).abs().mean())  # noqa: E731
        lines = [("model (final)", row("final_points")), ("model (before script)", row("model_points"))]
        if t["implied"].notna().any():
            lines.append(("market implied total", float((t["implied"] - t["actual"]).abs().mean())))
        lines.append(("team's season average", float((t["season_avg"] - t["actual"]).abs().mean())))
        out += ["## Team totals", "", "Mean absolute error in points per team-game (lower is better).", "",
                pd.DataFrame(lines, columns=["source", "MAE"]).to_markdown(index=False, floatfmt=".2f"), "",
                "By week:", "",
                t.groupby("week").apply(lambda d: pd.Series({
                    "model": (d["final_points"] - d["actual"]).abs().mean(),
                    "market": (d["implied"] - d["actual"]).abs().mean(),
                    "season_avg": (d["season_avg"] - d["actual"]).abs().mean()}), include_groups=False)
                .to_markdown(floatfmt=".2f"), ""]
    return "\n".join(out)
