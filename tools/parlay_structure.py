"""Which parlay structure works? Grid search on real Kalshi closing prices and
real results (output/2026/kalshi_backtest.csv, weeks 2-6).

For every structure (legs, selection rule, minimum edge vs the close, one leg
per game or not), each week's qualifying legs are split into as many
non-overlapping parlays as possible. A parlay costs $1 and pays $1 / product
of the leg prices (Kalshi close, plus a per-leg fee) if every leg wins.
Reported: parlays, hit rate, ROI, and a bootstrap 90% range for ROI (weeks and
parlays resampled), plus the analytic EV from leg-level win rates.
"""
import itertools, sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FEE = 0.01          # per leg, approximating Kalshi's fee / spread at the close


def legs(d: pd.DataFrame) -> pd.DataFrame:
    d = d.dropna(subset=["mid"]).copy()
    d = d[(d["mid"] > 0.03) & (d["mid"] < 0.97)]
    # each market can be bet YES (over) or NO (under); take the side the model prefers
    yes = d.assign(side="over", p=d["p_model"], price=d["mid"], win=d["won"])
    no = d.assign(side="under", p=1 - d["p_model"], price=1 - d["mid"], win=1 - d["won"])
    x = pd.concat([yes, no])
    x["edge"] = x["p"] - x["price"]
    x = x.sort_values("edge", ascending=False).drop_duplicates("ticker")
    x["cost"] = (x["price"] + FEE).clip(upper=0.99)
    x["game"] = x["team"]          # one leg per team-game proxy
    return x


RULES = {
    "edge": lambda x: x.sort_values("edge", ascending=False),
    "prob": lambda x: x.sort_values("p", ascending=False),
    "carries": lambda x: x[x["stat"] == "carries"].sort_values("edge", ascending=False),
    "unders": lambda x: x[x["side"] == "under"].sort_values("edge", ascending=False),
    "overs": lambda x: x[x["side"] == "over"].sort_values("edge", ascending=False),
    "receptions": lambda x: x[x["stat"] == "receptions"].sort_values("edge", ascending=False),
    "rec_yds": lambda x: x[x["stat"] == "rec_yds"].sort_values("edge", ascending=False),
    "pass_yds": lambda x: x[x["stat"] == "pass_yds"].sort_values("edge", ascending=False),
    "rush_yds": lambda x: x[x["stat"] == "rush_yds"].sort_values("edge", ascending=False),
}


def build(week_legs: pd.DataFrame, n: int, one_per_game: bool) -> list[pd.DataFrame]:
    pool = week_legs.copy()
    out = []
    while len(pool) >= n:
        pick, games = [], set()
        for i, x in pool.iterrows():
            if one_per_game and x["game"] in games:
                continue
            pick.append(i)
            games.add(x["game"])
            if len(pick) == n:
                break
        if len(pick) < n:
            break
        out.append(pool.loc[pick])
        pool = pool.drop(pick)
    return out


def main():
    d = pd.read_csv(ROOT / "output" / "2026" / "kalshi_backtest.csv")
    L = legs(d)
    print(f"legs with a closing price: {len(L)}; overall leg win rate {L['win'].mean():.3f} vs avg price {L['price'].mean():.3f}")
    res = []
    rng = np.random.default_rng(0)
    for rule, n, min_edge, opg in itertools.product(RULES, range(1, 11), (0.0, 0.03, 0.05, 0.10), (True, False)):
        tickets = []
        for w, x in L.groupby("week"):
            x = RULES[rule](x[x["edge"] >= min_edge])
            for p in build(x, n, opg):
                pay = 1 / np.prod(p["cost"])
                tickets.append({"week": w, "hit": float(p["win"].all()), "ret": pay * float(p["win"].all()),
                                "ev": float(np.prod(p["p"]) * pay)})
        if len(tickets) < 4:
            continue
        T = pd.DataFrame(tickets)
        roi = T["ret"].mean() - 1
        boots = []
        for _ in range(400):
            ws = rng.choice(T["week"].unique(), T["week"].nunique())
            bt = pd.concat([T[T["week"] == w] for w in ws])
            boots.append(bt["ret"].mean() - 1)
        res.append({"rule": rule, "legs": n, "min_edge": min_edge, "one_per_game": opg, "parlays": len(T),
                    "hit_rate": T["hit"].mean(), "roi": roi, "roi_lo": np.percentile(boots, 5),
                    "roi_hi": np.percentile(boots, 95), "model_ev": T["ev"].mean() - 1})
    R = pd.DataFrame(res)
    R.to_csv(ROOT / "output" / "2026" / "parlay_structure.csv", index=False)
    pd.set_option("display.width", 220)
    show = R[R["parlays"] >= 10].sort_values("roi", ascending=False)
    print(show.head(30).round(3).to_string(index=False))
    print("\nBy leg count (best rule per count, >= 10 parlays):")
    print(show.sort_values("roi", ascending=False).drop_duplicates("legs").sort_values("legs").round(3).to_string(index=False))
    # leg-level truth: does the model's edge vs the close predict wins?
    L["eb"] = pd.cut(L["edge"], [-1, 0, 0.03, 0.05, 0.10, 0.2, 1])
    print("\nLeg level: win rate vs price by model edge")
    print(L.groupby("eb", observed=True).agg(n=("win", "size"), win=("win", "mean"), price=("price", "mean")).round(3).to_string())
    return R


def sgp(L: pd.DataFrame | None = None):
    """Same-game parlays with a profit boost. Legs come from one game (both
    teams); outcomes are real, so in-game correlation is whatever actually
    happened. Book price = fair price from Kalshi closes x (1 - margin); a
    profit boost multiplies the profit: payout = 1 + (P - 1) x (1 + boost)."""
    if L is None:
        L = legs(pd.read_csv(ROOT / "output" / "2026" / "kalshi_backtest.csv"))
    games = pd.read_csv(ROOT / "output" / "2026" / "kalshi_backtest.csv")[["ticker"]]
    L = L.copy()
    # game id from the Kalshi event ticker (e.g. KXNFLREC-26OCT18NYJNE -> 26OCT18NYJNE)
    L["gid"] = L["ticker"].str.split("-").str[1]
    out = []
    for rule in ("edge", "prob", "carries", "unders", "overs"):
        for n in range(2, 7):
            for min_edge in (0.0, 0.03, 0.05):
                tickets = []
                for (w, gid), x in L.groupby(["week", "gid"]):
                    x = RULES[rule](x[x["edge"] >= min_edge])
                    x = x.drop_duplicates("player")          # one leg per player
                    while len(x) >= n:
                        p = x.head(n)
                        x = x.iloc[n:]
                        fair = 1 / np.prod(p["price"])
                        tickets.append({"week": w, "hit": float(p["win"].all()), "fair": fair})
                if len(tickets) < 8:
                    continue
                T = pd.DataFrame(tickets)
                for margin in (0.0, 0.15, 0.25, 0.35):
                    for boost in (0.0, 0.25, 0.5, 1.0):
                        P = 1 + (T["fair"] * (1 - margin) - 1).clip(lower=0)
                        pay = 1 + (P - 1) * (1 + boost)
                        roi = (pay * T["hit"]).mean() - 1
                        out.append({"rule": rule, "legs": n, "min_edge": min_edge, "book_margin": margin,
                                    "boost": boost, "parlays": len(T), "hit_rate": T["hit"].mean(), "roi": roi})
    R = pd.DataFrame(out)
    R.to_csv(ROOT / "output" / "2026" / "sgp_structure.csv", index=False)
    pd.set_option("display.width", 220)
    print("\nSame-game parlays: best structures at a 25% book margin, by boost")
    for b in (0.0, 0.25, 0.5, 1.0):
        x = R[(R["book_margin"] == 0.25) & (R["boost"] == b) & (R["parlays"] >= 15)].sort_values("roi", ascending=False)
        print(f"\nboost {b:.0%}:");print(x.head(6).round(3).to_string(index=False))
    return R


if __name__ == "__main__":
    main()
    sgp()
