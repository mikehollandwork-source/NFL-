"""Closing-line value (CLV) for the real-money list, from Kalshi's public
price history (no key).

For each money pick: the price we listed (YES at the ask, NO at 1 - bid) vs
the market's closing midpoint in the last hour before kickoff. Beating the
close consistently is the fastest evidence that an edge is real: win/loss
needs hundreds of bets to separate skill from luck, CLV about 50.

clv      = closing value of our side - price paid (dollars per $1 contract)
clv_roi  = closing value / price paid - 1 (expected return if the close is fair)
"""
from __future__ import annotations

import json
import time

import pandas as pd
import requests

from .kalshi import BASE

H = {"User-Agent": "nfl-proj research (slow, cached)"}
_last = [0.0]


def _get(url, params, tries=6):
    """1.1 s between calls; backs off on 429 and stops if it keeps happening."""
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
    raise RuntimeError("Kalshi kept rate-limiting; stopped (respecting the limit)")


def close_price(ticker: str, kickoff: pd.Timestamp, cache_dir) -> dict | None:
    """Last hourly candle at or before kickoff: bid/ask midpoint when the
    spread is 10 cents or less, else the last trade. Cached once final."""
    f = cache_dir / f"close_{ticker}.json"
    if f.exists():
        return json.loads(f.read_text())
    ts = int(kickoff.timestamp())
    series = ticker.split("-")[0]
    j = _get(f"{BASE}/series/{series}/markets/{ticker}/candlesticks",
             {"start_ts": ts - 6 * 3600, "end_ts": ts, "period_interval": 60})
    c = [x for x in j.get("candlesticks", []) if x["end_period_ts"] <= ts + 60]
    res = None
    if c:
        x = c[-1]
        bid = float(x["yes_bid"]["close_dollars"] or 0)
        ask = float(x["yes_ask"]["close_dollars"] or 0)
        trade = (x.get("price") or {}).get("close_dollars")
        mid = (bid + ask) / 2 if bid > 0 and ask < 1 and ask - bid <= 0.10 else (float(trade) if trade else None)
        res = {"mid": mid, "bid": bid, "ask": ask}
    f.write_text(json.dumps(res))
    return res


def week_clv(week: int, paths: dict, log=print) -> pd.DataFrame:
    """CLV for every money pick of the week whose game has kicked off."""
    f = paths["out"] / "money" / f"week_{week:02d}.csv"
    if not f.exists():
        return pd.DataFrame()
    m = pd.read_csv(f)
    cache = paths["out"].parents[1] / "data" / "odds" / "kalshi"     # repo/data/odds/kalshi
    cache.mkdir(parents=True, exist_ok=True)
    now = pd.Timestamp.now(tz="UTC")
    rows = []
    for x in m.itertuples():
        ko = pd.Timestamp(x.kickoff)
        if ko > now or not isinstance(x.ticker, str):
            continue
        try:
            c = close_price(x.ticker, ko, cache)
        except Exception as e:
            log(f"CLV: {x.ticker} unavailable ({e})")
            continue
        if not c or c.get("mid") is None:
            continue
        close_val = c["mid"] if x.side == "YES" else 1 - c["mid"]
        rows.append({**x._asdict(), "close_mid": c["mid"], "close_value": close_val,
                     "clv": close_val - x.price, "clv_roi": close_val / x.price - 1, "beat_close": close_val > x.price})
    out = pd.DataFrame(rows).drop(columns=["Index"], errors="ignore")
    if len(out):
        out.to_csv(f.with_name(f"week_{week:02d}_clv.csv"), index=False)
    return out


def season_text(paths: dict) -> str:
    files = sorted((paths["out"] / "money").glob("week_*_clv.csv"))
    if not files:
        return "CLV: no money picks with a closing price yet"
    d = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    return (f"📈 Money-list CLV, season: {len(d)} picks, beat the close {d.beat_close.mean():.0%}, "
            f"avg {d.clv.mean() * 100:+.1f}¢ per contract, expected ROI at the close {d.clv_roi.mean():+.0%}"
            + ("  (about 50 picks needed before this means much)" if len(d) < 50 else ""))
