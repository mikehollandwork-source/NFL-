"""Kalshi player-prop prices (public market data, no key).

Kalshi lists weekly NFL player markets as "X+" contracts (receptions,
receiving / rushing / passing yards, rush attempts, completions, anytime TD)
that trade between $0 and $1, so the price is the market's probability with
a small fee. Used ONLY for grading and edge checks, never as a model input.
"""
from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd
import requests

from .odds import norm_name

BASE = "https://api.elections.kalshi.com/trade-api/v2"
SERIES = {"KXNFLREC": "receptions", "KXNFLRECYDS": "rec_yds", "KXNFLPASSYDS": "pass_yds",
          "KXNFLRSHATT": "carries", "KXNFLRSHYDS": "rush_yds", "KXNFLPASSCOMP": "completions",
          "KXNFLPASSATT": "pass_att", "KXNFLANYTD": "anytime_td", "KXNFL2TD": "two_td"}


def fetch(log=print) -> pd.DataFrame:
    """Every open player market: player, stat, k (the X in "X+"), bid, ask, mid, volume."""
    rows = []
    for series, stat in SERIES.items():
        cur = None
        while True:
            params = {"series_ticker": series, "status": "open", "limit": 1000, **({"cursor": cur} if cur else {})}
            try:
                j = requests.get(f"{BASE}/markets", params=params, timeout=30,
                                 headers={"User-Agent": "nfl-proj"}).json()
            except Exception as e:  # never break a run over this
                log(f"kalshi {series}: {e}")
                break
            for m in j.get("markets", []):
                k = m.get("floor_strike")
                name = (m.get("yes_sub_title") or "").split(":")[0].strip()
                if k is None or not name:
                    continue
                bid, ask = float(m.get("yes_bid_dollars") or 0), float(m.get("yes_ask_dollars") or 0)
                rows.append({"player": name, "key": norm_name(name), "stat": stat, "k": float(k) + 0.5,
                             "bid": bid, "ask": ask, "mid": (bid + ask) / 2, "spread": ask - bid,
                             "volume": float(m.get("volume_fp") or 0), "event": m.get("event_ticker"),
                             "ticker": m.get("ticker"), "close_time": m.get("close_time"),
                             "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds")})
            cur = j.get("cursor")
            if not cur:
                break
    return pd.DataFrame(rows)


def price_for(k: pd.DataFrame, player: str, stat: str, line: float, side: str) -> dict | None:
    """Kalshi's price for our bet: over `line` = "ceil(line)+" contract (YES at the ask);
    under = NO at 1 - bid. None when Kalshi has no market at that number."""
    if k is None or k.empty:
        return None
    m = k[(k["key"] == norm_name(player)) & (k["stat"] == stat) & (k["k"] == float(int(line) + 1))]
    if m.empty:
        return None
    m = m.sort_values("volume", ascending=False).iloc[0]
    cost = m["ask"] if side == "over" else 1 - m["bid"]
    return {"kalshi_cost": round(float(cost), 4), "kalshi_mid": round(float(m["mid"] if side == "over" else 1 - m["mid"]), 4),
            "kalshi_spread": round(float(m["spread"]), 4), "kalshi_volume": float(m["volume"]), "kalshi_ticker": m["ticker"]}
