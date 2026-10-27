"""Game-day weather: measured effects and forecasts for upcoming games.

Effects are estimated from the 2025 and 2026 play-by-play (outdoor games
with recorded weather), not assumed:
  * passing yards per dropback vs wind above 10 mph, cold (< 35°F) and rain
  * field-goal make rate on 40+ yard tries vs wind above 10 mph
Each estimate is scaled down when it isn't statistically clear
(x min(1, |t| / 2)), like the adaptation test.

Forecasts come from the National Weather Service hourly forecast (free, US
stadiums, about 6 days out), with Open-Meteo as a fallback for games abroad.
Domes and retractable roofs (assumed closed) get no weather effect.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import requests

UA = {"User-Agent": "nfl-proj research (projection model)"}

# stadium_id -> (lat, lon, indoor)
STADIUMS = {
    "ATL97": (33.7554, -84.4008, True), "BAL00": (39.2780, -76.6227, False), "BOS00": (42.0909, -71.2643, False),
    "BUF00": (42.7738, -78.7870, False), "CAR00": (35.2258, -80.8528, False), "CHI98": (41.8623, -87.6167, False),
    "CIN00": (39.0955, -84.5161, False), "CLE00": (41.5061, -81.6995, False), "DAL00": (32.7473, -97.0945, True),
    "DEN00": (39.7439, -105.0201, False), "DET00": (42.3400, -83.0456, True), "GNB00": (44.5013, -88.0622, False),
    "HOU00": (29.6847, -95.4107, True), "IND00": (39.7601, -86.1639, True), "JAX00": (30.3239, -81.6373, False),
    "KAN00": (39.0489, -94.4839, False), "LAX01": (33.9535, -118.3392, True), "LON00": (51.5560, -0.2795, False),
    "LON02": (51.6043, -0.0664, False), "MIA00": (25.9580, -80.2389, False), "MIN01": (44.9737, -93.2581, True),
    "NAS00": (36.1665, -86.7713, False), "NOR00": (29.9511, -90.0812, True), "NYC01": (40.8135, -74.0745, False),
    "PHI00": (39.9008, -75.1675, False), "PHO00": (33.5276, -112.2626, True), "PIT00": (40.4468, -80.0158, False),
    "SEA00": (47.5952, -122.3316, False), "SFO01": (37.4030, -121.9700, False), "TAM00": (27.9759, -82.5033, False),
    "VEG00": (36.0909, -115.1833, True), "WAS00": (38.9076, -76.8645, False), "MEX00": (19.3029, -99.1505, False),
    "MAD01": (40.4531, -3.6883, False), "MUN01": (48.2188, 11.6247, True), "PAR00": (48.9245, 2.3602, True),
    "RIO00": (-22.9122, -43.2302, False), "MEL00": (-37.8200, 144.9834, True),
}
INDOOR_ROOFS = {"dome", "closed"}


def _rain(text) -> bool:
    t = str(text).lower()
    return any(w in t for w in ("rain", "shower", "snow", "storm", "drizzle", "sleet"))


def estimate_effects(plays: pd.DataFrame, games: pd.DataFrame) -> dict:
    """Pass yards per dropback and long-FG make rate vs wind / cold / rain."""
    g = games.dropna(subset=["boxscore_id"]).copy()
    g = g[~g["roof"].isin(list(INDOOR_ROOFS)) & g["wind"].notna() & g["temp"].notna()]
    if len(g) < 30:
        return {"n_games": len(g)}
    g["wind10"] = (g["wind"] - 10).clip(lower=0)
    g["cold"] = (g["temp"] < 35).astype(float)
    g["rain"] = g.get("weather", pd.Series(index=g.index, dtype=str)).map(_rain).astype(float)
    p = plays.merge(g[["boxscore_id", "wind10", "cold", "rain"]], on="boxscore_id")
    out = {"n_games": len(g)}

    def ols(y, X, names):
        X = np.column_stack([np.ones(len(X))] + [X[c].to_numpy(float) for c in names])
        coef, *_ = np.linalg.lstsq(X, y, rcond=None)
        resid = y - X @ coef
        cov = np.linalg.inv(X.T @ X) * (resid @ resid) / max(len(y) - X.shape[1], 1)
        se = np.sqrt(np.diag(cov))
        return {n: (float(coef[i + 1]), float(coef[i + 1] / se[i + 1]) if se[i + 1] > 0 else 0.0)
                for i, n in enumerate(names)}, float(coef[0])

    db = p[p["play_type"].isin(["pass", "sack", "scramble"]) & ~p["no_play"].astype(bool)]
    if len(db) > 500:
        est, base = ols(db["yards"].fillna(0).to_numpy(float), db, ["wind10", "cold", "rain"])
        out["pass"] = {"base": base, **{k: {"per_unit": v[0], "t": v[1]} for k, v in est.items()}}
    fg = p[(p["kick_type"] == "fg") & (p["kick_distance"] >= 40)]
    if len(fg) > 80:
        est, base = ols(fg["kick_good"].fillna(False).astype(float).to_numpy(), fg, ["wind10"])
        out["fg40"] = {"base": base, "wind10": {"per_unit": est["wind10"][0], "t": est["wind10"][1]}}
    return out


def _shrunk(e: dict) -> float:
    return e["per_unit"] * min(1.0, abs(e["t"]) / 2.0)


def multipliers(effects: dict, wx: dict | None) -> dict:
    """Pass yards and FG multipliers for one game's forecast."""
    out = {"pass": 1.0, "fg": 1.0, "note": None}
    if not wx or wx.get("indoor"):
        return out
    wind10 = max(wx.get("wind", 0) - 10, 0)
    cold = 1.0 if wx.get("temp", 60) < 35 else 0.0
    rain = 1.0 if wx.get("rain") else 0.0
    if "pass" in effects:
        e = effects["pass"]
        delta = _shrunk(e["wind10"]) * wind10 + _shrunk(e["cold"]) * cold + _shrunk(e["rain"]) * rain
        out["pass"] = float(np.clip(1 + delta / e["base"], 0.8, 1.05)) if e["base"] > 0 else 1.0
    if "fg40" in effects:
        e = effects["fg40"]
        out["fg"] = float(np.clip(1 + _shrunk(e["wind10"]) * wind10 / e["base"], 0.7, 1.05)) if e["base"] > 0 else 1.0
    out["note"] = (f"forecast {wx.get('temp', float('nan')):.0f}°F, wind {wx.get('wind', 0):.0f} mph"
                   f"{', rain/snow' if rain else ''} → pass yds x{out['pass']:.2f}, long FG x{out['fg']:.2f}")
    return out


def _nws(lat, lon, when: pd.Timestamp) -> dict | None:
    try:
        pt = requests.get(f"https://api.weather.gov/points/{lat},{lon}", headers=UA, timeout=20).json()
        url = pt["properties"]["forecastHourly"]
        periods = requests.get(url, headers=UA, timeout=20).json()["properties"]["periods"]
    except Exception:
        return None
    best = None
    for per in periods:
        t = pd.Timestamp(per["startTime"]).tz_convert("America/New_York").tz_localize(None)
        if best is None or abs(t - when) < abs(best[0] - when):
            best = (t, per)
    if best is None or abs(best[0] - when) > pd.Timedelta(hours=2):
        return None
    per = best[1]
    wind = float(str(per.get("windSpeed", "0")).split()[0].split("-")[-1] or 0)
    return {"temp": float(per["temperature"]), "wind": wind, "rain": _rain(per.get("shortForecast")),
            "source": "NWS", "summary": per.get("shortForecast")}


def _open_meteo(lat, lon, when: pd.Timestamp) -> dict | None:
    try:
        r = requests.get("https://api.open-meteo.com/v1/forecast", timeout=20, params={
            "latitude": lat, "longitude": lon, "hourly": "temperature_2m,wind_speed_10m,precipitation",
            "temperature_unit": "fahrenheit", "wind_speed_unit": "mph", "timezone": "America/New_York",
            "start_date": when.date().isoformat(), "end_date": when.date().isoformat()}).json()
        h = r["hourly"]
        i = min(range(len(h["time"])), key=lambda k: abs(pd.Timestamp(h["time"][k]) - when))
        return {"temp": h["temperature_2m"][i], "wind": h["wind_speed_10m"][i],
                "rain": (h["precipitation"][i] or 0) > 0.2, "source": "Open-Meteo"}
    except Exception:
        return None


def forecast_week(games: pd.DataFrame, week: int, cache_dir: Path, log=print) -> dict:
    """{home_team: weather dict} for the week's games (cached per week)."""
    cache = Path(cache_dir) / f"weather_week_{week:02d}.json"
    if cache.exists():
        return json.loads(cache.read_text())
    out = {}
    for g in games[games["week"] == week].itertuples():
        sid = getattr(g, "stadium_id", None)
        lat, lon, indoor = STADIUMS.get(sid, (None, None, True))
        roof = str(getattr(g, "sched_roof", "") or "")
        if indoor or roof in INDOOR_ROOFS:
            out[g.home] = {"indoor": True}
            continue
        when = pd.Timestamp(f"{g.date} {getattr(g, 'gametime', '13:00') or '13:00'}") + pd.Timedelta(hours=1, minutes=30)
        wx = _nws(lat, lon, when) or _open_meteo(lat, lon, when)
        out[g.home] = wx or {"unavailable": True}
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(out, indent=1))
    log(f"weather: forecasts for {sum(1 for v in out.values() if 'temp' in v)} outdoor games, "
        f"{sum(1 for v in out.values() if v.get('indoor'))} indoor")
    return out
