"""Model vs Kalshi closing prices, 2026 weeks 2-6.

For each week: the model as of that week (data through the week before), every
settled Kalshi player market (receptions, receiving / rushing / passing yards,
rush attempts), and per player+stat the strike nearest a main line (model
50/50). Closing price = Kalshi bid/ask midpoint in the last hour before
kickoff (candlesticks; fetched slowly, cached, backs off on 429). Reports
log-loss (model vs close) and the ROI of betting where the model disagrees
with the close, paying the close price.
"""
import json, sys, time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from nfl_proj.build import load_season          # noqa: E402
from nfl_proj.cli import _paths, load_cfg        # noqa: E402
from nfl_proj.odds import norm_name              # noqa: E402
from nfl_proj.paper import calibrate             # noqa: E402
from nfl_proj.pipeline import run_week           # noqa: E402

B = "https://api.elections.kalshi.com/trade-api/v2"
H = {"User-Agent": "nfl-proj research (slow, cached)"}
SERIES = {"KXNFLREC": "receptions", "KXNFLRECYDS": "rec_yds", "KXNFLPASSYDS": "pass_yds",
          "KXNFLRSHYDS": "rush_yds", "KXNFLRSHATT": "carries"}
KCODE = {"NE": "NWE", "KC": "KAN", "LV": "LVR", "LA": "LAR", "LAR": "LAR", "NO": "NOR", "SF": "SFO", "TB": "TAM",
         "GB": "GNB", "JAC": "JAX", "WAS": "WAS"}
CACHE = ROOT / "data" / "odds" / "kalshi"
CACHE.mkdir(parents=True, exist_ok=True)
_last = [0.0]


def get(url, params, tries=6):
    wait = 1.2
    for _ in range(tries):
        dt = time.time() - _last[0]
        if dt < 1.1:
            time.sleep(1.1 - dt)
        _last[0] = time.time()
        r = requests.get(url, params=params, headers=H, timeout=30)
        if r.status_code == 429:
            time.sleep(wait * 10)
            wait *= 2
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError("Kalshi kept rate-limiting; stopping (respecting the limit)")


def settled(series):
    f = CACHE / f"settled_{series}.json"
    if f.exists():
        return json.loads(f.read_text())
    out, cur = [], None
    while True:
        j = get(f"{B}/markets", {"series_ticker": series, "status": "settled", "limit": 1000, **({"cursor": cur} if cur else {})})
        out += j.get("markets", [])
        cur = j.get("cursor")
        if not cur:
            break
    f.write_text(json.dumps(out))
    return out


def close_price(series, ticker, kickoff_ts):
    f = CACHE / f"close_{ticker}.json"
    if f.exists():
        return json.loads(f.read_text())
    j = get(f"{B}/series/{series}/markets/{ticker}/candlesticks",
            {"start_ts": kickoff_ts - 6 * 3600, "end_ts": kickoff_ts, "period_interval": 60})
    c = [x for x in j.get("candlesticks", []) if x["end_period_ts"] <= kickoff_ts + 60]
    res = None
    if c:
        x = c[-1]
        bid, ask = float(x["yes_bid"]["close_dollars"] or 0), float(x["yes_ask"]["close_dollars"] or 0)
        trade = x.get("price", {}).get("close_dollars")
        mid = (bid + ask) / 2 if bid > 0 and ask < 1 and ask - bid <= 0.10 else (float(trade) if trade else None)
        res = {"mid": mid, "bid": bid, "ask": ask, "vol": float(x.get("volume_fp") or 0)}
    f.write_text(json.dumps(res))
    return res


def main(weeks=range(2, 7), config=None, tag=""):
    cfg = load_cfg(Path(config) if config else ROOT / "config" / "projection.toml")
    paths = _paths(cfg)
    t = load_season(paths["db"])
    g = t["games"]
    g["kick"] = [datetime.strptime(f"{d} {tm or '13:00'}", "%Y-%m-%d %H:%M").replace(
        tzinfo=__import__("zoneinfo").ZoneInfo("America/New_York")).astimezone(timezone.utc) for d, tm in zip(g["date"], g["gametime"])]
    mk = []
    for s, stat in SERIES.items():
        for m in settled(s):
            name = (m.get("yes_sub_title") or "").split(":")[0].strip()
            if m.get("floor_strike") is None or m.get("result") not in ("yes", "no"):
                continue
            date = datetime.strptime(m["event_ticker"].split("-")[1][:7], "%y%b%d").date()
            mk.append({"series": s, "stat": stat, "ticker": m["ticker"], "player": name, "key": norm_name(name),
                       "k": float(m["floor_strike"]) + 0.5, "won": 1.0 if m["result"] == "yes" else 0.0, "date": str(date)})
    mk = pd.DataFrame(mk)
    print("settled markets", len(mk))
    rows = []
    for w in weeks:
        gw = g[g["week"] == w]
        dates = set(gw["date"].astype(str))
        m = mk[mk["date"].isin(dates)]
        if m.empty:
            continue
        r = run_week(t, cfg, paths, w, asof=True, log=lambda *a: None)
        P = r["props"][r["props"]["_samples"].notna()].copy()
        P["key"] = P["player"].map(norm_name)
        kick = {}
        for x in gw.itertuples():
            kick[x.home] = kick[x.away] = int(x.kick.timestamp())
        for x in m.itertuples():
            p = P[(P["key"] == x.key) & (P["stat"] == x.stat)]
            if p.empty:
                continue
            smp = np.asarray(p["_samples"].iloc[0], float)
            raw = float((smp >= x.k).mean())
            rows.append({"week": w, "series": x.series, "ticker": x.ticker, "player": x.player, "team": p["team"].iloc[0],
                         "stat": x.stat, "k": x.k, "won": x.won, "raw": raw,
                         "p_model": calibrate(raw, cfg, x.stat, "over"), "kick": kick.get(p["team"].iloc[0])})
        print(f"week {w}: {len(rows)} matched so far")
    d = pd.DataFrame(rows)
    # one strike per player+stat: the one nearest the model's 50/50 (a main-line equivalent)
    d["dist"] = (d["raw"] - 0.5).abs()
    main_ = d.sort_values("dist").drop_duplicates(["week", "player", "stat"])
    print("main-line markets to price:", len(main_))
    closes = []
    for i, x in enumerate(main_.itertuples()):
        c = close_price(x.series, x.ticker, x.kick) if x.kick else None
        closes.append(c or {})
        if i % 50 == 0:
            print(f"  priced {i}/{len(main_)}", flush=True)
    main_ = pd.concat([main_.reset_index(drop=True), pd.DataFrame(closes)], axis=1)
    main_.to_csv(ROOT / "output" / "2026" / f"kalshi_backtest{('_' + tag) if tag else ''}.csv", index=False)
    return main_


if __name__ == "__main__":
    # python tools/kalshi_backtest.py [first-last weeks] [config file] [output tag]
    a = sys.argv[1:]
    wk = range(int(a[0].split("-")[0]), int(a[0].split("-")[1]) + 1) if a else range(2, 7)
    main(wk, a[1] if len(a) > 1 else None, a[2] if len(a) > 2 else "")
