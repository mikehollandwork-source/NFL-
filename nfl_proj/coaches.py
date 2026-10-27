"""Coach angle: experience, historical run/pass lean and star reliance.

Inputs:
  data/manual/coaches.csv  head coach, play-caller, experience, and the
                           seasons the play-caller called plays (``caller_history``)
  PFR team-season pages    /teams/<franchise>/<year>.htm for each of those seasons
  PFR league pages         /years/<year>/ for league averages that season

Per play-caller this produces:
  pass_lean      career pass rate minus league pass rate that season, adjusted
                 for game script (point differential), in percentage points
  star_target    career top-receiver target share minus league average
  star_carry     career RB1 carry share minus league average
plus experience tiers. ``priors`` turns the lean and star numbers into
early-season priors that this season's data gradually overrides.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

from .parse_pfr import all_tables, table_rows, _num, _text
from .teams import ABBR_TO_FRANCHISE, abbr_from_href


def load_coaches(path: Path) -> pd.DataFrame:
    if not Path(path).exists():
        return pd.DataFrame()
    return pd.read_csv(path, dtype=str).fillna("")


def parse_history(s: str) -> list[tuple[str, int]]:
    """``"GNB:2006-2018;DAL:2023-2024"`` -> [(GNB, 2006), ..., (DAL, 2024)]."""
    out = []
    for part in filter(None, (p.strip() for p in s.split(";"))):
        team, years = part.split(":")
        a, _, b = years.partition("-")
        out += [(team.strip(), y) for y in range(int(a), int(b or a) + 1)]
    return out


# --------------------------------------------------------------------------
# Parsing PFR team-season and league pages
# --------------------------------------------------------------------------

def parse_team_season(html: str) -> dict:
    """Pass/rush attempts, point differential and usage concentration."""
    tables = all_tables(html)
    out = {}
    ts = tables.get("team_stats")
    if ts is not None:
        for r in table_rows(ts):
            label = _text(r.get("player")).lower()
            if "team stats" in label or label == "team":
                out["pass_att"] = _num(r.get("pass_att"))
                out["rush_att"] = _num(r.get("rush_att"))
                out["points_for"] = _num(r.get("points"))
            elif "opp" in label:
                out["points_against"] = _num(r.get("points"))
    # Receiving / rushing table id has varied ("receiving_and_rushing",
    # "rushing_and_receiving"); pick any table with a per-player targets column.
    rr = next((t for k, t in tables.items() if "receiving" in k and t.find(attrs={"data-stat": "targets"})), None)
    if rr is not None:
        rows = [r for r in table_rows(rr) if r.get("player") is not None
                and "team" not in _text(r.get("player")).lower()]
        tg = sorted((_num(r.get("targets")) or 0 for r in rows), reverse=True)
        ra = sorted((_num(r.get("rush_att")) or 0 for r in rows), reverse=True)
        if sum(tg):
            out["top_target_share"] = tg[0] / sum(tg)
            out["top2_target_share"] = sum(tg[:2]) / sum(tg)
        if sum(ra):
            out["rb1_carry_share"] = ra[0] / sum(ra)  # QB scrambles included: noted limitation
    games = None
    for k in ("games", "team_games"):
        if k in tables:
            games = sum(1 for r in table_rows(tables[k]) if _num(r.get("pts_off")) is not None)
    out["games"] = games or 17
    return out


def parse_league_season(html: str) -> pd.DataFrame:
    """Per-team pass/rush attempts and points for one season (team offense table)."""
    tables = all_tables(html)
    t = tables.get("team_stats")
    rows = []
    if t is None:
        return pd.DataFrame()
    for r in table_rows(t):
        cell = r.get("team")
        a = cell.find("a", href=True) if cell else None
        abbr = abbr_from_href(a["href"]) if a else None
        if abbr:
            rows.append({"team": abbr, "pass_att": _num(r.get("pass_att")),
                         "rush_att": _num(r.get("rush_att")), "points": _num(r.get("points"))})
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# Scraping
# --------------------------------------------------------------------------

def scrape_history(coaches: pd.DataFrame, fetcher, log=print) -> None:
    """Download every team-season and league-season page the histories need."""
    seasons = set()
    for h in coaches["caller_history"]:
        for team, year in parse_history(h):
            fr = ABBR_TO_FRANCHISE.get(team)
            if fr:
                fetcher.get(f"/teams/{fr}/{year}.htm")
                seasons.add(year)
    for y in sorted(seasons):
        fetcher.get(f"/years/{y}/")
    log(f"cached history for {len(coaches)} play-callers across {len(seasons)} seasons")


def history_table(coaches: pd.DataFrame, fetcher) -> pd.DataFrame:
    """One row per play-caller season, with league comparison."""
    league_cache = {}
    rows = []
    for c in coaches.itertuples():
        for team, year in parse_history(c.caller_history):
            fr = ABBR_TO_FRANCHISE.get(team)
            tp = fetcher.cache_path(f"/teams/{fr}/{year}.htm")
            lp = fetcher.cache_path(f"/years/{year}/")
            if not tp.exists():
                continue
            ts = parse_team_season(tp.read_text(encoding="utf-8"))
            if year not in league_cache and lp.exists():
                league_cache[year] = parse_league_season(lp.read_text(encoding="utf-8"))
            lg = league_cache.get(year, pd.DataFrame())
            pr = (ts.get("pass_att") or 0) / max((ts.get("pass_att") or 0) + (ts.get("rush_att") or 0), 1)
            lg_pr = (lg["pass_att"] / (lg["pass_att"] + lg["rush_att"])).mean() if not lg.empty else np.nan
            pd_pg = ((ts.get("points_for") or 0) - (ts.get("points_against") or 0)) / ts.get("games", 17)
            rows.append({"team_now": c.team, "play_caller": c.play_caller, "team": team, "season": year,
                         "pass_rate": pr, "league_pass_rate": lg_pr, "point_diff_pg": pd_pg,
                         "top_target_share": ts.get("top_target_share"),
                         "top2_target_share": ts.get("top2_target_share"),
                         "rb1_carry_share": ts.get("rb1_carry_share")})
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# Profiles
# --------------------------------------------------------------------------

LEAGUE_TOP_TARGET = 0.25   # typical NFL top-receiver target share (used when history is thin)
LEAGUE_RB1_CARRY = 0.55


def profiles(coaches: pd.DataFrame, hist: pd.DataFrame, season: int) -> pd.DataFrame:
    """One row per team: experience tiers, pass lean, star reliance, labels."""
    out = []
    script_slope = 0.0
    if not hist.empty and hist["point_diff_pg"].std() > 0 and len(hist) >= 15:
        # Winning teams run more late in games; remove that effect so "run-first"
        # means the coach's choice, not a lead. Slope estimated from the data.
        x, y = hist["point_diff_pg"], hist["pass_rate"] - hist["league_pass_rate"]
        script_slope = float(np.polyfit(x, y, 1)[0])
    lg_top = hist["top_target_share"].mean() if not hist.empty and hist["top_target_share"].notna().sum() > 10 else LEAGUE_TOP_TARGET
    lg_rb1 = hist["rb1_carry_share"].mean() if not hist.empty and hist["rb1_carry_share"].notna().sum() > 10 else LEAGUE_RB1_CARRY
    for c in coaches.itertuples():
        h = hist[hist["team_now"] == c.team] if not hist.empty else pd.DataFrame()
        hc_years = season - int(c.hc_first_nfl_season or season)
        team_years = season - int(c.hc_first_season_with_team or season)
        called = parse_history(c.caller_history)
        # Seasons actually spent calling plays (history), not the calendar span.
        call_years = len(called) if called else season - int(c.caller_first_season_calling or season)
        r = {
            "team": c.team, "head_coach": c.head_coach, "play_caller": c.play_caller,
            "caller_role": c.caller_role,
            "hc_tier": ("first-year HC" if hc_years == 0 else "new to team" if team_years == 0
                        else "veteran HC" if hc_years >= 5 else "young HC"),
            "hc_seasons": hc_years,
            "caller_tier": ("first-time play-caller" if call_years == 0 else
                            "veteran play-caller" if call_years >= 5 else "developing play-caller"),
            "caller_seasons": call_years, "new_caller_2026": c.new_caller_2026 == "yes",
            "history_seasons": len(h), "history_listed": len(called), "confidence": c.confidence,
        }
        if len(h):
            lean = (h["pass_rate"] - h["league_pass_rate"]) - script_slope * h["point_diff_pg"]
            r["pass_lean"] = float(lean.mean())
            r["star_target"] = float(h["top_target_share"].mean() - lg_top) if h["top_target_share"].notna().any() else np.nan
            r["star_carry"] = float(h["rb1_carry_share"].mean() - lg_rb1) if h["rb1_carry_share"].notna().any() else np.nan
        else:
            r["pass_lean"] = r["star_target"] = r["star_carry"] = np.nan
        r["style"] = ("pass-first" if r["pass_lean"] > 0.025 else "run-first" if r["pass_lean"] < -0.025
                      else "balanced" if not pd.isna(r["pass_lean"]) else "no history")
        r["star_reliance"] = ("leans on stars" if (r["star_target"] or 0) > 0.03 or (r["star_carry"] or 0) > 0.08
                              else "spreads it around" if (r["star_target"] or 0) < -0.03
                              else "typical" if not pd.isna(r["star_target"]) else "no history")
        out.append(r)
    return pd.DataFrame(out)


def current_concentration(plays: pd.DataFrame) -> pd.DataFrame:
    """This season's top target share and RB1 carry share per team."""
    p = plays[~plays["garbage"]]
    tg = p[p["is_pass"] & p["target_id"].notna()].groupby(["offense", "target_id"])["w"].sum()
    ru = p[p["is_run"] & p["rusher_id"].notna()].groupby(["offense", "rusher_id"])["w"].sum()
    top_t = (tg.groupby(level=0).max() / tg.groupby(level=0).sum()).rename("top_target_share")
    top_r = (ru.groupby(level=0).max() / ru.groupby(level=0).sum()).rename("rb1_carry_share")
    return pd.concat([top_t, top_r], axis=1).reset_index().rename(columns={"offense": "team"})


def describe(prof_row: pd.Series, current: pd.Series | None) -> str:
    bits = [f"HC {prof_row['head_coach']} ({prof_row['hc_tier']}, {prof_row['hc_seasons']} prior seasons)"]
    caller = prof_row["play_caller"]
    if caller != prof_row["head_coach"]:
        bits.append(f"plays called by {prof_row['caller_role']} {caller} ({prof_row['caller_tier']}, "
                    f"{prof_row['caller_seasons']} seasons calling)")
    else:
        bits.append(f"calls own plays ({prof_row['caller_tier']}, {prof_row['caller_seasons']} seasons calling)")
    if not pd.isna(prof_row.get("pass_lean")):
        bits.append(f"career {prof_row['style']} ({prof_row['pass_lean'] * 100:+.1f} pts pass rate vs league, "
                    f"{int(prof_row['history_seasons'])} seasons)")
    elif prof_row.get("history_listed", 0):
        bits.append("career tendencies not scraped yet (run `coaches`)")
    else:
        bits.append("no prior play-calling seasons: this season's data only")
    if prof_row["star_reliance"] not in ("no history",):
        bits.append(prof_row["star_reliance"])
    if current is not None and not pd.isna(current.get("top_target_share", np.nan)):
        bits.append(f"this season top target share {current['top_target_share']:.0%}")
    return "; ".join(bits)
