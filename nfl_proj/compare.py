"""Side-by-side scores for backtest variants (output/<season>/backtest_<tag>_*.csv)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def _lift(df: pd.DataFrame, base_rates: pd.Series) -> tuple[float, float, int]:
    d = df[df["result"].isin(["hit", "miss"])]
    if d.empty:
        return np.nan, np.nan, 0
    hit = d["result"].eq("hit")
    under = d["stat"].map(base_rates)
    base = np.where(d["direction"] == "under", under, 1 - under)
    return float(hit.mean()), float(hit.mean() - np.mean(base)), len(d)


def compare(out_dir: Path, tags: list[str]) -> str:
    rows, err_rows = [], []
    calls_all = pd.concat([pd.read_csv(out_dir / f"backtest_{t}_calls.csv") for t in tags
                           if (out_dir / f"backtest_{t}_calls.csv").exists()])
    cc = calls_all[calls_all["result"].isin(["hit", "miss"])]
    base_rates = (cc["actual"] < cc["baseline"]).groupby(cc["stat"]).mean()
    for t in tags:
        f = lambda k: out_dir / f"backtest_{t}_{k}.csv"  # noqa: E731
        if not f("totals").exists():
            continue
        tt = pd.read_csv(f("totals")).dropna(subset=["actual"])
        p = pd.read_csv(f("picks")) if f("picks").exists() else pd.DataFrame()
        c = pd.read_csv(f("calls")) if f("calls").exists() else pd.DataFrame()
        e = pd.read_csv(f("proj_err")) if f("proj_err").exists() else pd.DataFrame()
        ph, pl, pn = _lift(p, base_rates) if not p.empty else (np.nan, np.nan, 0)
        ch, cl, cn = _lift(c, base_rates) if not c.empty else (np.nan, np.nan, 0)
        wk45 = tt[tt["week"] >= 4]
        rows.append({"variant": t,
                     "team total MAE": (tt["final_points"] - tt["actual"]).abs().mean(),
                     "corr w/ actual": np.corrcoef(tt["final_points"], tt["actual"])[0, 1],
                     "MAE wk 4-5": (wk45["final_points"] - wk45["actual"]).abs().mean(),
                     "spread (sd)": tt["final_points"].std(),
                     "picks hit": ph, "picks lift": pl, "picks n": pn,
                     "all calls hit": ch, "all calls lift": cl, "calls n": cn})
        if not e.empty:
            s = e.groupby("stat").apply(lambda d: np.average(d["model_mae"], weights=d["n"]), include_groups=False)
            err_rows.append(s.rename(t))
    tab = pd.DataFrame(rows)
    mk = pd.read_csv(out_dir / f"backtest_{tags[0]}_totals.csv").dropna(subset=["actual", "implied"])
    out = ["# Backtest comparison (weeks 2-5)", "",
           f"Market implied totals for reference: MAE {(mk['implied'] - mk['actual']).abs().mean():.2f}, "
           f"corr {np.corrcoef(mk['implied'], mk['actual'])[0, 1]:.2f}, sd {mk['implied'].std():.2f}. "
           f"Actual team points sd {mk['actual'].std():.2f}.", "",
           "`lift` = hit rate minus the no-information rate for the same calls (yardage stats land under their "
           "own average more often than not). Picks: weeks 4-5 only (3 games needed).", "",
           tab.to_markdown(index=False, floatfmt=".3f"), ""]
    if err_rows:
        naive = pd.read_csv(out_dir / f"backtest_{tags[0]}_proj_err.csv").groupby("stat").apply(
            lambda d: np.average(d["naive_mae"], weights=d["n"]), include_groups=False).rename("naive season avg")
        et = pd.concat(err_rows + [naive], axis=1)
        out += ["## Player projection error by stat (mean absolute error, lower is better)", "",
                et.to_markdown(floatfmt=".2f"), ""]
    return "\n".join(out)
