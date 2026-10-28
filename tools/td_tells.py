"""Touchdown "tells": do scorers look different BEFORE the game than players
who didn't score, beyond what the TD model already knows?

1. Week N (default 7, 2026): every RB/WR/TE with a real role (3+ touches a game
   so far) -> scorers vs non-scorers on their pre-game numbers.
2. Each pre-game number tested on 2025 weeks 4-18 and 2026 weeks 3-N: logistic
   regression of scored ~ model TD odds + the number. A real tell has a
   coefficient reliably away from zero in BOTH seasons.
"""
import sqlite3
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FEATS = {
    "touches": "carries + targets per game",
    "rz": "red-zone touches per game (inside the 20)",
    "i10": "touches inside the 10 per game",
    "ez": "end-zone targets per game",
    "td_rate": "TDs per game so far",
    "last3_touches": "touches per game, last 3 games",
    "trend": "last-3 touches minus season average",
    "last_rz": "red-zone touches last game",
    "drought": "games since last TD",
    "team_td": "team offensive TDs per game",
}


def weekly(season):
    p = pd.read_csv(ROOT / f"data/raw/nflverse/play_by_play_{season}.csv.gz", low_memory=False,
                    usecols=["season_type", "week", "posteam", "yardline_100", "air_yards", "rush_attempt",
                             "pass_attempt", "two_point_attempt", "touchdown", "td_player_id",
                             "receiver_player_id", "rusher_player_id", "qb_scramble"])
    p = p[(p.season_type == "REG") & (p.two_point_attempt != 1)]
    ru = p[(p.rush_attempt == 1) & p.rusher_player_id.notna()].assign(pid=lambda d: d.rusher_player_id, tgt=0, car=1)
    re = p[(p.pass_attempt == 1) & p.receiver_player_id.notna()].assign(pid=lambda d: d.receiver_player_id, tgt=1, car=0)
    t = pd.concat([ru, re])
    t["rz"] = (t.yardline_100 <= 20).astype(int)
    t["i10"] = (t.yardline_100 <= 10).astype(int)
    t["ez"] = ((t.tgt == 1) & (t.air_yards >= t.yardline_100)).astype(int)
    w = t.groupby(["pid", "week", "posteam"]).agg(car=("car", "sum"), tgt=("tgt", "sum"), rz=("rz", "sum"),
                                                   i10=("i10", "sum"), ez=("ez", "sum")).reset_index()
    tds = p[(p.touchdown == 1) & p.td_player_id.notna()].groupby(["td_player_id", "week"]).size().rename("td")
    w = w.merge(tds, left_on=["pid", "week"], right_index=True, how="left").fillna({"td": 0})
    team = p[(p.touchdown == 1) & p.td_player_id.notna()].groupby(["posteam", "week"]).size().rename("team_tds")
    w = w.merge(team, left_on=["posteam", "week"], right_index=True, how="left").fillna({"team_tds": 0})
    w["touches"] = w.car + w.tgt
    return w.rename(columns={"pid": "player_id", "posteam": "team"})


def pregame(w):
    out = []
    for pid, g in w.sort_values("week").groupby("player_id"):
        g = g.reset_index(drop=True)
        for i in range(1, len(g)):
            h = g.iloc[:i]
            last = h.iloc[-1]
            since = (len(h) - 1 - h.index[h.td > 0].max()) if (h.td > 0).any() else len(h)
            out.append({"player_id": pid, "week": g.week[i], "gp": len(h),
                        "touches": h.touches.mean(), "rz": h.rz.mean(), "i10": h.i10.mean(), "ez": h.ez.mean(),
                        "td_rate": h.td.mean(), "last3_touches": h.touches.tail(3).mean(),
                        "trend": h.touches.tail(3).mean() - h.touches.mean(), "last_rz": last.rz,
                        "drought": since, "team_td": h.team_tds.mean()})
    return pd.DataFrame(out)


def logit_fit(y, X):
    X = np.column_stack([np.ones(len(y)), X])
    b = np.zeros(X.shape[1])
    for _ in range(50):
        p = 1 / (1 + np.exp(-X @ b))
        W = p * (1 - p)
        H = X.T @ (X * W[:, None]) + 1e-6 * np.eye(len(b))
        step = np.linalg.solve(H, X.T @ (y - p))
        b += step
        if np.abs(step).max() < 1e-8:
            break
    se = np.sqrt(np.diag(np.linalg.inv(H)))
    return b, se


def sample(season, tag, weeks=None):
    td = pd.read_csv(ROOT / f"output/{season}/backtest_{tag}_td.csv")
    td = td[td.pos.isin(["RB", "WR", "TE"])]
    if weeks:
        td = td[td.week.isin(weeks)]
    pre = pregame(weekly(season))
    d = td.merge(pre, on=["player_id", "week"], how="inner")
    d = d[(d.gp >= 2) & (d.touches >= 3)]
    d["scored"] = (d.actual_td >= 1).astype(int)
    return d


def main(week=7):
    pd.set_option("display.width", 200)
    d26 = sample(2026, "AT26")
    d25 = sample(2025, "AT25")
    wk = d26[d26.week == week]
    L = [f"# Touchdown tells: week {week} scorers vs non-scorers, then tested on 2025 + 2026", "",
         f"Week {week}: {len(wk)} RB/WR/TE with 3+ touches a game so far; {wk.scored.sum()} scored.", "",
         "| pre-game number | scorers | non-scorers | ratio |", "|---|---|---|---|"]
    for f, name in [("anytime_td", "model TD chance")] + list(FEATS.items()):
        a, b = wk[wk.scored == 1][f].mean(), wk[wk.scored == 0][f].mean()
        L.append(f"| {name} | {a:.2f} | {b:.2f} | {a / b if b else float('nan'):.2f} |")
    L += ["", "## Does each number add anything beyond the model's TD chance?", "",
          "Logistic regression: scored ~ model TD log-odds + the number (standardized). Coefficient > 0 = players "
          "higher on it scored more often than the model expected. |t| >= 2 in both seasons with the same sign = a tell.", "",
          "| number | 2025 coef | t | 2026 coef | t | verdict |", "|---|---|---|---|---|---|"]
    for f, name in FEATS.items():
        row = []
        for d in (d25, d26):
            p = d.anytime_td.clip(0.01, 0.99)
            z = (d[f] - d[f].mean()) / d[f].std()
            b, se = logit_fit(d.scored.values, np.column_stack([np.log(p / (1 - p)), z]))
            row += [b[2], b[2] / se[2]]
        same = np.sign(row[0]) == np.sign(row[2])
        verdict = "tell" if same and abs(row[1]) >= 2 and abs(row[3]) >= 2 else (
            "maybe (one season)" if abs(row[1]) >= 2 or abs(row[3]) >= 2 else "no")
        L.append(f"| {name} | {row[0]:+.3f} | {row[1]:+.1f} | {row[2]:+.3f} | {row[3]:+.1f} | {verdict} |")
    # calibration of the model itself
    L += ["", "## Model TD chance vs actual (both seasons)", "", "| model says | n | scored |", "|---|---|---|"]
    allx = pd.concat([d25, d26])
    for lo, hi in ((0, .2), (.2, .3), (.3, .4), (.4, .5), (.5, .6), (.6, 1)):
        x = allx[(allx.anytime_td >= lo) & (allx.anytime_td < hi)]
        L.append(f"| {lo:.0%}-{hi:.0%} | {len(x)} | {x.scored.mean():.0%} |")
    L.append(f"\nSamples: 2025 wk 4-18 {len(d25)} player-games, 2026 wk 3-{week} {len(d26)}.")
    out = ROOT / "output/2026/td_tells.md"
    out.write_text("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
