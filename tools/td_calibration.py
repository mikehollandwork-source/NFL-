"""Anytime-TD calibration of the model's backtest predictions (backtest_*_td.csv)."""
import sys
import numpy as np, pandas as pd


def ll(y, p):
    p = np.clip(p, 1e-6, 1 - 1e-6)
    return -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))


def main(files):
    d = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    d = d[d["pos"].isin(["WR", "TE", "RB"]) & (d["anytime_td"] > 0.02)].copy()
    d["y"] = (d["actual_td"] > 0).astype(float)
    print(f"{len(d)} player-games, weeks {sorted(d['week'].unique())}")
    print(f"mean predicted {d['anytime_td'].mean():.3f}  actual {d['y'].mean():.3f}")
    d["b"] = pd.cut(d["anytime_td"], [0, .1, .2, .3, .4, .5, .6, 1])
    t = d.groupby("b", observed=True).agg(n=("y", "size"), predicted=("anytime_td", "mean"), actual=("y", "mean"))
    print(t.round(3).to_string())
    print(d.groupby("pos").agg(n=("y", "size"), predicted=("anytime_td", "mean"), actual=("y", "mean")).round(3).to_string())
    print("log-loss model", round(ll(d["y"].values, d["anytime_td"].values), 4),
          " base rate", round(ll(d["y"].values, np.full(len(d), d["y"].mean())), 4))
    return d


if __name__ == "__main__":
    main(sys.argv[1:])
