"""Sleeper disagreement filter for the money list (rush attempts vs Kalshi).

Bets: every Kalshi rush-attempt market in the backtest (2026 weeks 2-6, one
strike per player near the model's 50/50) where the model beats the closing
price by 10+ points: YES at the ask, NO at 1 - bid (as the money list buys).
Filter (no tuning): hold a bet when Sleeper's free pre-game projection of the
player's rush attempts sits on the losing side of the line. Sleeper is only a
warning light; it never changes our numbers. Usage:
  python tools/sleeper_filter_test.py <dir with Sleeper players.json and p_<yr>_<wk>.json>
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from nfl_proj.odds import norm_name  # noqa: E402


def sleeper(dirpath, season, weeks):
    pl = json.load(open(Path(dirpath) / "players.json"))
    rows = []
    for w in weeks:
        f = Path(dirpath) / f"p_{season}_{w}.json"
        if not f.exists():
            continue
        for sid, v in json.load(open(f)).items():
            p = pl.get(sid, {})
            if p.get("position") not in ("RB", "QB", "WR", "TE"):
                continue
            name = p.get("full_name") or f"{p.get('first_name', '')} {p.get('last_name', '')}"
            rows.append({"week": w, "key": norm_name(name), "sl_car": v.get("rush_att", np.nan)})
    return pd.DataFrame(rows).dropna().drop_duplicates(["week", "key"])


def main(dirpath):
    k = pd.read_csv(ROOT / "output/2026/kalshi_backtest.csv")
    k = k[(k.stat == "carries") & k.mid.notna() & (k.mid > .03) & (k.mid < .97)].copy()
    k["key"] = k.player.map(norm_name)
    s = sleeper(dirpath, 2026, sorted(k.week.unique()))
    k = k.merge(s, on=["week", "key"], how="left")
    rows = []
    for x in k.itertuples():
        for side, prob, price in (("YES", x.p_model, x.ask), ("NO", 1 - x.p_model, 1 - x.bid)):
            if not (0 < price < 1) or prob - price < 0.10:
                continue
            won = x.won if side == "YES" else 1 - x.won
            line = x.k - 0.5
            against = (side == "YES" and x.sl_car < line) or (side == "NO" and x.sl_car > line)
            rows.append({"week": x.week, "player": x.player, "side": side, "k": x.k, "price": price, "p": prob,
                         "won": won, "sl_car": x.sl_car, "hold": bool(against) if not np.isnan(x.sl_car) else None,
                         "pl": (1 - price) / price if won else -1.0})
    b = pd.DataFrame(rows)
    roi = lambda d: f"{len(d):3d} bets, {d.won.mean():.0%} won, ROI {d.pl.mean():+.0%}" if len(d) else "0 bets"
    print("All edge bets:          ", roi(b))
    print("No Sleeper projection:  ", roi(b[b.hold.isna()]))
    m = b[b.hold.notna()]
    print("Sleeper agrees (kept):  ", roi(m[m.hold == False]))     # noqa: E712
    print("Sleeper disagrees (held)", roi(m[m.hold == True]))      # noqa: E712
    for w, x in m.groupby("week"):
        print(f"  week {w}: kept {roi(x[x.hold == False])} | held {roi(x[x.hold == True])}")  # noqa: E712
    # bootstrap: kept minus held ROI
    rng = np.random.default_rng(1)
    kept, held = m[m.hold == False].pl.values, m[m.hold == True].pl.values  # noqa: E712
    if len(kept) and len(held):
        d = [rng.choice(kept, len(kept)).mean() - rng.choice(held, len(held)).mean() for _ in range(5000)]
        print(f"Kept beats held in {np.mean(np.array(d) > 0):.0%} of bootstrap draws "
              f"(gap {kept.mean() - held.mean():+.0%})")
    b.to_csv(ROOT / "output/2026/sleeper_filter_test.csv", index=False)


if __name__ == "__main__":
    main(sys.argv[1])
