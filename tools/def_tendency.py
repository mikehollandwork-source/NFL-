"""Do offenses call plays differently against certain defenses?

For every play: expected pass chance from the situation alone (down, distance,
field position, score, clock; a league table fit on 2024). Residual = dropback
(pass, sack or scramble) minus that expectation.

  offense lean  = an offense's average residual (how pass-happy it is in any situation)
  defense pull  = average of (residual - that offense's lean) over the plays a
                  defense faced: how much MORE than usual opponents pass against it,
                  after removing score, situation and who the offense is.
  raw faced     = the plain share of plays against the defense that were passes
                  (what the model uses now, shrunk).

Tests:
  1. Does the defense pull repeat? odd vs even weeks, per season.
  2. Does it predict the next game? As of each week (games before it only):
     predict an offense's game residual with its own lean, plus b x the
     opponent's pull (shrunk). b and the shrink fit on 2024, tested on 2025 and 2026.
     Same for the raw-faced version. Reported in pass attempts per game.

Usage: python tools/def_tendency.py   -> output/2026/def_tendency.md
"""
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SEASONS = (2024, 2025, 2026)


def load(season):
    p = pd.read_sql("select boxscore_id, season, week, quarter, down, ytg, yardline_100, score_diff, game_secs_left, "
                    "offense, defense, play_type from plays", sqlite3.connect(ROOT / f"data/nfl_{season}.db"))
    p = p[p["play_type"].isin(["pass", "sack", "scramble", "run"]) & p["down"].between(1, 4)].copy()
    p["db"] = p["play_type"].isin(["pass", "sack", "scramble"]).astype(float)
    # situation bins
    p["d"] = p["down"].astype(int)
    p["y"] = pd.cut(p["ytg"], [-1, 2, 4, 7, 10, 15, 99], labels=False)
    p["f"] = pd.cut(p["yardline_100"], [-1, 5, 20, 50, 80, 101], labels=False)
    p["s"] = pd.cut(p["score_diff"].clip(-30, 30), [-31, -17, -9, -4, 0, 3, 8, 16, 31], labels=False)
    t = p["game_secs_left"]
    p["c"] = np.select([t > 1800 + 120, t > 1800, t > 900, t > 300, t > 120], [0, 1, 2, 3, 4], 5)
    # garbage time out (4th quarter, 17+ point margin)
    return p[~((p["quarter"] >= 4) & (p["score_diff"].abs() >= 17))]


def xpass_table(p):
    """League pass rate by situation, falling back to coarser bins when thin."""
    levels = [["d", "y", "f", "s", "c"], ["d", "y", "s", "c"], ["d", "y", "s"], ["d", "y"], ["d"]]
    return [(lv, p.groupby(lv)["db"].agg(["mean", "size"])) for lv in levels]


def add_xpass(p, tables, min_n=40):
    x = pd.Series(np.nan, index=p.index)
    for lv, tb in tables:
        tb = tb[tb["size"] >= min_n]["mean"]
        m = p[lv].apply(tuple, axis=1).map(tb) if len(lv) > 1 else p[lv[0]].map(tb)
        x = x.fillna(m)
    p["xp"] = x.fillna(p["db"].mean())
    p["r"] = p["db"] - p["xp"]
    return p


def game_table(p):
    """One row per offense-game: plays, dropbacks, residual mean, raw pass share."""
    g = p.groupby(["season", "week", "boxscore_id", "offense", "defense"]).agg(
        n=("r", "size"), r=("r", "mean"), db=("db", "sum"), xp=("xp", "mean")).reset_index()
    return g


def pulls(g, upto_week=None, exclude=None):
    """Offense lean and defense pull from games (weighted by plays)."""
    h = g if upto_week is None else g[g["week"] < upto_week]
    if exclude is not None:
        h = h[exclude(h)]
    lean = (h["r"] * h["n"]).groupby(h["offense"]).sum() / h.groupby("offense")["n"].sum()
    h = h.assign(adj=h["r"] - h["offense"].map(lean))
    pull_sum = (h["adj"] * h["n"]).groupby(h["defense"]).sum()
    pull_n = h.groupby("defense")["n"].sum()
    raw = (h["db"].groupby(h["defense"]).sum() / pull_n)
    lg_raw = h["db"].sum() / h["n"].sum()
    return lean, pull_sum, pull_n, raw - lg_raw, h.groupby("offense")["n"].sum()


def shrunk(s, n, k):
    return s / (n + k)          # s = sum of residuals; shrink toward 0 with k plays of prior


def asof_rows(g, season):
    rows = []
    for w in sorted(g["week"].unique()):
        if w < 4:
            continue
        lean, ps, pn, raw, on = pulls(g[g["season"] == season], upto_week=w)
        cur = g[(g["season"] == season) & (g["week"] == w)]
        for x in cur.itertuples():
            if x.offense not in lean or x.defense not in pn:
                continue
            rows.append({"season": season, "week": w, "offense": x.offense, "defense": x.defense, "n": x.n,
                         "r": x.r, "lean": lean[x.offense], "lean_n": on[x.offense],
                         "pull_sum": ps[x.defense], "pull_n": pn[x.defense], "raw": raw[x.defense]})
    return pd.DataFrame(rows)


def main():
    P = {s: load(s) for s in SEASONS}
    tables = xpass_table(P[2024])
    G = pd.concat([game_table(add_xpass(P[s], tables)) for s in SEASONS], ignore_index=True)
    L = ["# Do offenses pass more or less against certain defenses?", "",
         "Pass = dropback (pass, sack, scramble). Expected pass chance from down, distance, field position, score and "
         "clock (league table, 2024). Garbage time (4th quarter, 17+ points) removed. **Defense pull** = how much more "
         "than usual opponents pass against a defense, after removing situation and each offense's own lean. "
         "**Raw faced** = plain pass share against the defense (what the model uses now).", ""]

    # 1. split-half reliability (odd vs even weeks)
    L += ["## 1. Does it repeat? (odd weeks vs even weeks, same season)", "",
          "| season | defense pull r | raw pass share faced r | offense lean r | spread of defense pull (sd, pts of pass rate) |",
          "|---|---|---|---|---|"]
    for s in SEASONS:
        gs = G[G["season"] == s]
        res = {}
        for half, sel in (("odd", lambda h: h["week"] % 2 == 1), ("even", lambda h: h["week"] % 2 == 0)):
            lean, ps, pn, raw, on = pulls(gs, exclude=sel)
            res[half] = (ps / pn, raw, lean)
        a = pd.concat([res["odd"][0], res["even"][0]], axis=1).dropna()
        b = pd.concat([res["odd"][1], res["even"][1]], axis=1).dropna()
        c = pd.concat([res["odd"][2], res["even"][2]], axis=1).dropna()
        lean, ps, pn, raw, on = pulls(gs)
        L.append(f"| {s} | {a.corr().iloc[0, 1]:+.2f} | {b.corr().iloc[0, 1]:+.2f} | {c.corr().iloc[0, 1]:+.2f} | "
                 f"{(ps / pn).std() * 100:.1f} |")
    L.append("")

    # 2. as-of prediction of each offense-game's pass residual
    A = pd.concat([asof_rows(G, s) for s in SEASONS], ignore_index=True)
    lean_k = 300.0

    def pred(d, b, k, use):
        own = d["lean"] * d["lean_n"] / (d["lean_n"] + lean_k)
        if use == "pull":
            return own + b * shrunk(d["pull_sum"], d["pull_n"], k)
        if use == "raw":
            return own + b * d["raw"] * d["pull_n"] / (d["pull_n"] + k)
        return own

    def err(d, b, k, use):    # mean abs miss in pass attempts per game (residual x plays)
        return float(((d["r"] - pred(d, b, k, use)).abs() * d["n"]).mean())

    tr = A[A["season"] == 2024]
    best = {}
    for use in ("pull", "raw"):
        cand = [(err(tr, b, k, use), b, k) for b in np.arange(0, 1.51, 0.1) for k in (0, 100, 200, 400, 800, 1600)]
        best[use] = min(cand)
    L += ["## 2. Does it predict the next game? (as of each week, weeks 4+)", "",
          "Miss = |actual - predicted| pass-rate residual x plays, i.e. pass attempts per game the situation and the "
          "offense's own lean don't explain. Weight b and shrinkage k (plays) fit on 2024 only.", "",
          f"Fitted on 2024: defense pull b = {best['pull'][1]:.1f}, k = {best['pull'][2]:.0f}; "
          f"raw faced b = {best['raw'][1]:.1f}, k = {best['raw'][2]:.0f}.", "",
          "| season | games | offense lean only | + defense pull | + raw faced (now) | correlation of pull with next-game residual |",
          "|---|---|---|---|---|---|"]
    for s in SEASONS:
        d = A[A["season"] == s]
        own = d["lean"] * d["lean_n"] / (d["lean_n"] + lean_k)
        cr = np.corrcoef(d["r"] - own, d["pull_sum"] / d["pull_n"])[0, 1]
        L.append(f"| {s}{' (fit)' if s == 2024 else ''} | {len(d)} | {err(d, 0, 0, 'none'):.3f} | "
                 f"{err(d, best['pull'][1], best['pull'][2], 'pull'):.3f} | {err(d, best['raw'][1], best['raw'][2], 'raw'):.3f} | {cr:+.3f} |")
    L.append("")

    # 3. the current table: which defenses pull passes / runs (2026 to date, shrunk as fitted)
    b, k = best["pull"][1], best["pull"][2]
    lean, ps, pn, raw, on = pulls(G[G["season"] == 2026])
    t = pd.DataFrame({"pull": ps / pn, "shrunk": shrunk(ps, pn, k) * b, "raw": raw, "plays": pn}).sort_values("pull")
    L += ["## 3. 2026 defenses: how much more opponents pass against them than usual", "",
          "pull and raw in points of pass rate; 'used' = shrunk x b (what a model would apply).", "",
          "| defense | plays faced | pull | used | raw faced |", "|---|---|---|---|---|"]
    for dfn, r in t.iterrows():
        L.append(f"| {dfn} | {r.plays:.0f} | {r.pull * 100:+.1f} | {r.shrunk * 100:+.1f} | {r.raw * 100:+.1f} |")
    L.append("")
    out = ROOT / "output/2026/def_tendency.md"
    out.write_text("\n".join(L))
    A.to_csv(ROOT / "output/2026/def_tendency_rows.csv", index=False)
    print("\n".join(L[:40]))


if __name__ == "__main__":
    main()
