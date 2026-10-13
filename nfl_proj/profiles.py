"""Coaching-style (offense) and scheme (defense) profiles from parsed plays."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .playparse import ALL_BUCKETS, PASS_BUCKETS, RUN_BUCKETS

SCRIMMAGE = ("pass", "run", "sack", "scramble")


def shrink(value, n, prior, k):
    """Weighted blend toward ``prior``; at n == k the result is 50/50."""
    value = np.where(pd.isna(value), prior, value)
    return (n * value + k * prior) / (n + k)


def prep_plays(plays: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Scrimmage plays with analysis flags and recency weights."""
    p = plays[plays["play_type"].isin(SCRIMMAGE) & ~plays["no_play"].astype(bool)
              & plays["offense"].notna()].copy()
    f = cfg["filters"]
    margin = p["score_diff"].abs()
    p["garbage"] = (p["quarter"] >= f["garbage_time_quarter"]) & (margin > f["garbage_time_score_margin"])
    p["neutral"] = (p["quarter"] <= 3) & (margin <= f["neutral_score_margin"])
    p["dropback"] = p["play_type"].isin(("pass", "sack", "scramble"))
    p["is_pass"] = p["play_type"] == "pass"
    p["is_run"] = p["play_type"] == "run"
    p["is_sack"] = p["play_type"] == "sack"
    p["deep"] = p["depth"] == "deep"
    p["third"] = p["down"].isin([3, 4])
    p["early"] = p["down"].isin([1, 2])
    p["redzone"] = p["yardline_100"] <= 20

    d = cfg["definitions"]
    p["explosive"] = ((p["is_pass"] & (p["yards"] >= d["explosive_pass_yards"]))
                      | (p["is_run"] & (p["yards"] >= d["explosive_run_yards"])))
    turnover = p["interception"].astype(bool) | (p["fumble"].astype(bool) & (p["epa"] < -1.5))
    mode = d["negative_play"]
    if mode == "epa":
        p["negative"] = p["epa"] < 0
    elif mode == "success":
        p["negative"] = p["success"] == 0
    elif mode == "loss":
        p["negative"] = (p["yards"] < 0) | p["is_sack"] | turnover
    else:
        raise ValueError(f"unknown negative_play definition {mode!r}")

    last_week = p["week"].max()
    hl = cfg["weighting"]["half_life_weeks"]
    p["w"] = 0.5 ** ((last_week - p["week"]) / hl)
    return p


def _wmean(df, col, w="w"):
    m = df[col].notna()
    return np.average(df.loc[m, col].astype(float), weights=df.loc[m, w]) if m.any() else np.nan


# --------------------------------------------------------------------------
# Offense: coaching style
# --------------------------------------------------------------------------

def offense_style(plays: pd.DataFrame, all_plays: pd.DataFrame) -> pd.DataFrame:
    rows = []
    live = plays[~plays["garbage"]]
    for team, g in live.groupby("offense"):
        games = g["boxscore_id"].nunique()
        passes = g[g["is_pass"]]
        runs = g[g["is_run"]]
        r = {
            "team": team, "games": games,
            "plays_per_game": len(plays[plays["offense"] == team]) / max(games, 1),
            "neutral_pass_rate": _wmean(g[g["neutral"]], "dropback"),
            "early_down_pass_rate": _wmean(g[g["early"] & g["neutral"]], "dropback"),
            "third_down_pass_rate": _wmean(g[g["third"]], "dropback"),
            "redzone_pass_rate": _wmean(g[g["redzone"]], "dropback"),
            "deep_pass_share": _wmean(passes[passes["depth"].notna()], "deep"),
            "third_down_deep_share": _wmean(passes[passes["third"] & passes["depth"].notna()], "deep"),
            "sack_rate": _wmean(g[g["dropback"]], "is_sack"),
            "epa_per_play": _wmean(g, "epa"),
            "epa_per_pass": _wmean(g[g["dropback"]], "epa"),
            "epa_per_run": _wmean(runs, "epa"),
            "success_rate": _wmean(g, "success"),
            "negative_rate": _wmean(g, "negative"),
            "explosive_rate": _wmean(g, "explosive"),
            "shotgun_rate": _wmean(g, "shotgun") if g["shotgun"].any() else np.nan,
            "no_huddle_rate": _wmean(g, "no_huddle") if g["no_huddle"].any() else np.nan,
        }
        for b in PASS_BUCKETS:
            r[f"share_{b}"] = (passes["bucket"] == b).sum() / max(passes["bucket"].notna().sum(), 1)
        for b in RUN_BUCKETS:
            r[f"share_{b}"] = (runs["bucket"] == b).sum() / max(runs["bucket"].notna().sum(), 1)
        rows.append(r)
    style = pd.DataFrame(rows)

    # 4th-down aggressiveness needs punts / field goals, so use all plays.
    fourth = all_plays[(all_plays["down"] == 4) & ~all_plays["no_play"].astype(bool)
                       & all_plays["offense"].notna()]
    if not fourth.empty:
        went = fourth["play_type"].isin(SCRIMMAGE)
        decided = fourth[went | fourth["play_type"].eq("special")]
        go = decided.assign(go=went).groupby("offense")["go"].mean().rename("fourth_down_go_rate")
        style = style.merge(go, left_on="team", right_index=True, how="left")
    return style


def describe_style(row: pd.Series, league: pd.Series) -> list[str]:
    """Plain-language notes on where a team's play-calling deviates."""
    notes = []

    def cmp(col, label, fmt="{:.0%}", thresh=0.04):
        v, lg = row.get(col), league.get(col)
        if pd.isna(v) or pd.isna(lg):
            return
        if v - lg > thresh:
            notes.append(f"{label} high: {fmt.format(v)} (league {fmt.format(lg)})")
        elif lg - v > thresh:
            notes.append(f"{label} low: {fmt.format(v)} (league {fmt.format(lg)})")

    cmp("neutral_pass_rate", "Neutral-script pass rate")
    cmp("early_down_pass_rate", "Early-down pass rate")
    cmp("deep_pass_share", "Deep-pass share", thresh=0.03)
    cmp("third_down_deep_share", "3rd-down deep share", thresh=0.04)
    cmp("redzone_pass_rate", "Red-zone pass rate", thresh=0.06)
    cmp("fourth_down_go_rate", "4th-down go rate", thresh=0.06)
    cmp("sack_rate", "Sack rate", thresh=0.015)
    cmp("epa_per_pass", "EPA/dropback", fmt="{:+.2f}", thresh=0.05)
    cmp("epa_per_run", "EPA/run", fmt="{:+.2f}", thresh=0.05)
    run_cols = {b: row.get(f"share_{b}", np.nan) for b in RUN_BUCKETS}
    top_run = max(run_cols, key=lambda b: -1 if pd.isna(run_cols[b]) else run_cols[b])
    if run_cols[top_run] - league.get(f"share_{top_run}", 0) > 0.05:
        notes.append(f"Favors {top_run.replace('_', ' ')} ({run_cols[top_run]:.0%})")
    return notes


# --------------------------------------------------------------------------
# Defense: what it allows
# --------------------------------------------------------------------------

def defense_profile(plays: pd.DataFrame, team_def: pd.DataFrame | None = None) -> pd.DataFrame:
    live = plays[~plays["garbage"]]
    rows = []
    for team, g in live.groupby("defense"):
        drop = g[g["dropback"]]
        passes = g[g["is_pass"]]
        r = {
            "team": team, "games": g["boxscore_id"].nunique(),
            "plays_faced_per_game": len(plays[plays["defense"] == team]) / max(g["boxscore_id"].nunique(), 1),
            "pass_rate_faced": _wmean(g[g["neutral"]], "dropback"),
            "epa_allowed": _wmean(g, "epa"),
            "epa_allowed_pass": _wmean(drop, "epa"),
            "epa_allowed_run": _wmean(g[g["is_run"]], "epa"),
            "epa_allowed_deep": _wmean(passes[passes["deep"]], "epa"),
            "epa_allowed_short": _wmean(passes[passes["depth"] == "short"], "epa"),
            "deep_share_faced": _wmean(passes[passes["depth"].notna()], "deep"),
            "sack_rate": _wmean(drop, "is_sack"),
            "third_down_sack_rate": _wmean(drop[drop["third"]], "is_sack"),
            "third_down_epa_allowed_deep": _wmean(passes[passes["third"] & passes["deep"]], "epa"),
            "third_down_deep_n": int((passes["third"] & passes["deep"]).sum()),
            "explosive_allowed": _wmean(g, "explosive"),
        }
        for b in ALL_BUCKETS:
            sub = g[g["bucket"] == b]
            r[f"n_{b}"] = len(sub)
            r[f"ypp_{b}"] = sub["yards"].mean() if len(sub) else np.nan
            r[f"epa_{b}"] = sub["epa"].mean() if len(sub) else np.nan
        rows.append(r)
    prof = pd.DataFrame(rows)

    if team_def is not None and not team_def.empty:
        cols = [c for c in team_def.columns if c != "team"]
        blitz = [c for c in cols if "blitz" in c.lower() and "pct" in c.lower()]
        press = [c for c in cols if ("pressure" in c.lower() or "prss" in c.lower()) and "pct" in c.lower()]
        keep = {"team": "team"}
        if blitz:
            keep[blitz[0]] = "blitz_pct"
        if press:
            keep[press[0]] = "pressure_pct"
        if len(keep) > 1:
            prof = prof.merge(team_def[list(keep)].rename(columns=keep), on="team", how="left")
    return prof


def auto_labels(prof: pd.DataFrame) -> pd.DataFrame:
    """Data-derived defensive archetypes (terciles of the league)."""
    def tercile(col, hi, lo):
        q1, q2 = prof[col].quantile([1 / 3, 2 / 3])
        return np.where(prof[col] >= q2, hi, np.where(prof[col] <= q1, lo, "avg"))

    out = pd.DataFrame({"team": prof["team"]})
    out["deep_pass_d"] = tercile("epa_allowed_deep", "soft_deep", "tight_deep")
    pressure_col = "blitz_pct" if "blitz_pct" in prof and prof["blitz_pct"].notna().sum() > 10 \
        else "third_down_sack_rate"
    out["third_down_pressure"] = tercile(pressure_col, "heavy", "light")
    out["run_d"] = tercile("epa_allowed_run", "soft_run", "stout_run")
    out["pressure_source"] = pressure_col
    return out


def load_manual_labels(path: Path) -> pd.DataFrame:
    if not Path(path).exists():
        return pd.DataFrame(columns=["team", "base_coverage", "third_down_blitz"])
    df = pd.read_csv(path, dtype=str).fillna("")
    return df[df["team"].str.strip() != ""]


def combined_labels(prof: pd.DataFrame, manual: pd.DataFrame, mode: str) -> pd.DataFrame:
    auto = auto_labels(prof)
    if mode == "auto" or manual.empty:
        auto["base_coverage"] = ""
        return auto
    m = manual.set_index("team")
    labels = auto.set_index("team")
    labels["base_coverage"] = m["base_coverage"].reindex(labels.index).fillna("")
    if "third_down_blitz" in m:
        tagged = m["third_down_blitz"].reindex(labels.index).fillna("").str.lower()
        if mode == "manual":
            labels["third_down_pressure"] = tagged.replace("", "unlabeled")
        else:
            labels["third_down_pressure"] = tagged.where(tagged != "", labels["third_down_pressure"])
    return labels.reset_index()


def matchup_splits(plays: pd.DataFrame, labels: pd.DataFrame) -> pd.DataFrame:
    """League-wide: how each play family performs against each defensive
    label, split by early vs 3rd/4th down. This is the table behind calls
    like "vs blitz-heavy 3rd-down defenses the deep ball pays"."""
    p = plays[~plays["garbage"] & (plays["is_pass"] | plays["is_run"])].merge(
        labels, left_on="defense", right_on="team", how="left", suffixes=("", "_d"))
    p["family"] = np.where(p["is_run"], "run", np.where(p["deep"], "deep_pass", "short_pass"))
    p["down_group"] = np.where(p["third"], "3rd/4th", "1st/2nd")
    out = []
    for label_col in ("deep_pass_d", "third_down_pressure", "run_d", "base_coverage"):
        if label_col not in p or p[label_col].replace("", np.nan).isna().all():
            continue
        grp = p[p[label_col].fillna("") != ""].groupby([label_col, "down_group", "family"])
        t = grp.agg(plays=("epa", "size"), epa=("epa", "mean"), success=("success", "mean"),
                    yards=("yards", "mean")).reset_index().rename(columns={label_col: "label"})
        t.insert(0, "label_type", label_col)
        out.append(t)
    return pd.concat(out, ignore_index=True) if out else pd.DataFrame()


def offense_vs_labels(plays: pd.DataFrame, labels: pd.DataFrame) -> pd.DataFrame:
    """Per offense: EPA by play family against each defensive label."""
    p = plays[~plays["garbage"] & (plays["is_pass"] | plays["is_run"])].merge(
        labels, left_on="defense", right_on="team", how="left", suffixes=("", "_d"))
    p["family"] = np.where(p["is_run"], "run", np.where(p["deep"], "deep_pass", "short_pass"))
    out = []
    for label_col in ("deep_pass_d", "third_down_pressure", "run_d", "base_coverage"):
        if label_col not in p:
            continue
        sub = p[p[label_col].fillna("") != ""]
        t = sub.groupby(["offense", label_col, "family"]).agg(
            plays=("epa", "size"), epa=("epa", "mean")).reset_index()
        t = t.rename(columns={label_col: "label"})
        t.insert(1, "label_type", label_col)
        out.append(t)
    return pd.concat(out, ignore_index=True) if out else pd.DataFrame()
