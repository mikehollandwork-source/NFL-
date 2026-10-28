"""Share lab: which pre-game estimate of a player's share of team targets /
carries is closest to what actually happens? (Player-share misses are the
biggest part of prop misses: factor_tests section 15.)

Universe: players who played the game (snaps > 0) for a team they had played
for earlier that season, weeks 4+. Error = |predicted share - actual share| x
actual team volume (= the targets / carries miss caused by share alone).

Estimators (all from games before the week):
  season    share over the games he played
  last1/3   last game / last 3 games played
  ewm_h     exponentially weighted, half-life h games
  snap      share-per-snap (season) x last game's snap %  (playing time first)
  current   the full model's share (backtest_<tag>_proj.csv: player / team projected volume)
  fitted    linear blend of the above, fit on 2024 only, per position group
Tested on 2025 and 2026 against the current model.
"""
import sqlite3
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
STATS = {"targets": ("targets", ["WR", "TE", "RB"]), "carries": ("rush_att", ["RB", "QB", "WR"])}


def season_rows(season, stat):
    col, pos = STATS[stat]
    pg = pd.read_sql("select * from player_games", sqlite3.connect(ROOT / f"data/nfl_{season}.db"))
    pg = pg[pg.off_snaps.fillna(0) > 0].copy()
    tv = pg.groupby(["team", "week"])[col].sum().rename("V")
    snaps = pg.groupby(["team", "week"]).off_snaps.max().rename("team_snaps")   # QB/OL play every snap
    pg = pg.join(tv, on=["team", "week"]).join(snaps, on=["team", "week"])
    pg["s"] = pg[col] / pg.V.replace(0, np.nan)
    pg["snap"] = pg.off_snaps / pg.team_snaps
    pg = pg[pg.pos.isin(pos)].sort_values("week")
    out = []
    for (pid, team), g in pg.groupby(["player_id", "team"]):
        g = g.reset_index(drop=True)
        for i in range(1, len(g)):
            h = g.iloc[:i]
            if h.V.sum() <= 0:
                continue
            r = {"season": season, "player_id": pid, "team": team, "pos": g.pos[i], "week": g.week[i],
                 "gp": i, "V": g.V[i], "actual_s": g.s[i], "actual": g[col][i],
                 "season_s": h[col].sum() / h.V.sum(), "last1": h.s.iloc[-1],
                 "last3": h[col].tail(3).sum() / max(h.V.tail(3).sum(), 1)}
            for hl in (1, 2, 3, 4, 6):
                wts = 0.5 ** (np.arange(len(h))[::-1] / hl)
                r[f"ewm{hl}"] = float((wts * h[col]).sum() / max((wts * h.V).sum(), 1e-9))
            spsnap = h[col].sum() / max((h.snap * h.V).sum(), 1e-9)       # share per unit of snap %
            r["snap_last"] = h.snap.iloc[-1]
            r["snap3"] = h.snap.tail(3).mean()
            r["snap_est"] = spsnap * h.snap.iloc[-1]
            r["snap3_est"] = spsnap * h.snap.tail(3).mean()
            out.append(r)
    d = pd.DataFrame(out)
    return d[d.week >= 4]


def current_model(d, season, tag, stat):
    f = ROOT / f"output/{season}/backtest_{tag}_proj.csv"
    if not f.exists():
        return d.assign(current=np.nan)
    p = pd.read_csv(f, low_memory=False)
    p = p[p[stat].notna()]
    p["current"] = p[stat] / p.groupby(["week", "team"])[stat].transform("sum")
    return d.merge(p[["player_id", "week", "current"]], on=["player_id", "week"], how="left")


EST = ["season_s", "last1", "last3", "ewm1", "ewm2", "ewm3", "ewm4", "ewm6", "snap_est", "snap3_est"]


def fit(train, group):
    """Non-negative-ish linear blend per group: least squares of actual share on estimators."""
    coefs = {}
    for gname, x in train.groupby(group):
        X = np.column_stack([np.ones(len(x))] + [x[c].fillna(x.season_s) for c in EST])
        b = np.linalg.lstsq(X, x.actual_s.values, rcond=None)[0]
        coefs[gname] = b
    return coefs


def apply(d, coefs, group):
    out = np.full(len(d), np.nan)
    for gname, b in coefs.items():
        m = (d[group] == gname).values
        X = np.column_stack([np.ones(m.sum())] + [d.loc[m, c].fillna(d.loc[m, "season_s"]) for c in EST])
        out[m] = np.clip(X @ b, 0, 1)
    return out


def main():
    L = ["# Share lab", ""]
    for stat in STATS:
        tr = season_rows(2024, stat)
        te = {2025: current_model(season_rows(2025, stat), 2025, "AT25", stat),
              2026: current_model(season_rows(2026, stat), 2026, "AT26", stat)}
        tr["grp"] = np.where(tr.pos == "RB", "RB", np.where(tr.pos == "QB", "QB", "WRTE"))
        coefs = fit(tr, "grp")
        L += [f"## {stat}", "", "Average miss in " + stat + " from share alone (|pred share - actual| x actual team volume):", "",
              "| estimator | 2025 | 2026 |", "|---|---|---|"]
        res = {}
        for yr, d in te.items():
            d["grp"] = np.where(d.pos == "RB", "RB", np.where(d.pos == "QB", "QB", "WRTE"))
            d["fitted"] = apply(d, coefs, "grp")
            both = d[d.current.notna()]
            for c in EST + ["fitted", "current"]:
                res.setdefault(c, {})[yr] = ((both[c].fillna(both.season_s) - both.actual_s).abs() * both.V).mean()
            res.setdefault("n", {})[yr] = len(both)
            te[yr] = d
        for c, v in res.items():
            if c == "n":
                continue
            L.append(f"| {c} | {v[2025]:.3f} | {v[2026]:.3f} |")
        L.append(f"| (player-games) | {res['n'][2025]} | {res['n'][2026]} |")
        # blend of current model with fitted
        for w in (0.25, 0.5, 0.75):
            v = {}
            for yr, d in te.items():
                b = d[d.current.notna()]
                v[yr] = ((w * b.fitted + (1 - w) * b.current - b.actual_s).abs() * b.V).mean()
            L.append(f"| {w:.0%} fitted + {1 - w:.0%} current | {v[2025]:.3f} | {v[2026]:.3f} |")
        L.append("")
        L.append("Fitted blend weights (2024): " + "; ".join(
            f"{g}: " + ", ".join(f"{c} {b:+.2f}" for c, b in zip(['const'] + EST, coefs[g]) if abs(b) > 0.02) for g in coefs))
        L.append("")
    out = ROOT / "output/2026/share_lab.md"
    out.write_text("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main()
