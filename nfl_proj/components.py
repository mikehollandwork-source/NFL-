"""Actual team-game components, to compare with what the model projected.

From the play-by-play: scrimmage plays, dropbacks, pass attempts, runs,
sacks, interceptions, fumbles lost, offensive TDs (pass / rush), field goal
attempts and makes, drives, red-zone trips (drives that reached the 20),
red-zone TD rate, and points per drive.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def actual_components(plays: pd.DataFrame, games: pd.DataFrame) -> pd.DataFrame:
    p = plays[plays["offense"].notna()]
    live = p[~p["no_play"].astype(bool)]
    scrim = live[live["play_type"].isin(["pass", "run", "sack", "scramble"])]
    rows = []
    pts = pd.concat([games[["boxscore_id", "home", "home_score"]].rename(columns={"home": "team", "home_score": "points"}),
                     games[["boxscore_id", "away", "away_score"]].rename(columns={"away": "team", "away_score": "points"})])
    pts = pts.set_index(["boxscore_id", "team"])["points"]
    for (box, team), g in scrim.groupby(["boxscore_id", "offense"]):
        allg = live[(live["boxscore_id"] == box) & (live["offense"] == team)]
        drives = g["drive"].dropna().unique() if "drive" in g else []
        rz = g[g["yardline_100"] <= 20]["drive"].dropna().unique() if "drive" in g else []
        dres = g.drop_duplicates("drive").set_index("drive")["drive_result"] if "drive_result" in g else pd.Series()
        rz_td = sum(1 for d in rz if dres.get(d) == "Touchdown")
        fg = allg[allg["kick_type"] == "fg"]
        td = g["touchdown"].astype(bool) & ~g["interception"].astype(bool)
        pass_td = (td & (g["play_type"] == "pass")).sum()
        rush_td = (td & g["play_type"].isin(["run", "scramble"])).sum()
        points = pts.get((box, team), np.nan)
        rows.append({
            "boxscore_id": box, "team": team, "week": int(g["week"].iloc[0]),
            "plays": len(g), "dropbacks": int(g["play_type"].isin(["pass", "sack", "scramble"]).sum()),
            "pass_att": int((g["play_type"] == "pass").sum()), "runs": int((g["play_type"] == "run").sum()),
            "sacks": int((g["play_type"] == "sack").sum()),
            "interceptions": int(g["interception"].astype(bool).sum()),
            "fumbles_lost": int((g["fumble"].astype(bool) & (g["epa"] < -1.5)).sum()),
            "pass_td": int(pass_td), "rush_td": int(rush_td), "td": int(pass_td + rush_td),
            "fga": len(fg), "fgm": int(fg["kick_good"].fillna(False).astype(bool).sum()),
            "drives": len(drives), "rz_trips": len(rz), "rz_td_rate": rz_td / len(rz) if len(rz) else np.nan,
            "points": points, "points_per_drive": points / len(drives) if len(drives) else np.nan,
        })
    return pd.DataFrame(rows)


COMPARE = ["plays", "dropbacks", "pass_att", "runs", "sacks", "interceptions", "pass_td", "rush_td", "td",
           "fga", "fgm", "points"]


def error_table(totals: pd.DataFrame, actual: pd.DataFrame) -> pd.DataFrame:
    """Per component: mean projected, mean actual, bias, mean abs error,
    correlation, and how much of the points miss it explains."""
    m = totals.merge(actual, on=["week", "team"], suffixes=("", "_act"))
    out = []
    for c in COMPARE:
        pc = f"proj_{c}"
        if pc not in m or c not in m:
            continue
        d = m[list(dict.fromkeys([pc, c, "final_points", "points"]))].dropna()
        if d.empty:
            continue
        err = d[pc] - d[c]
        out.append({"component": c, "projected": d[pc].mean(), "actual": d[c].mean(), "bias": err.mean(),
                    "mae": err.abs().mean(), "corr": np.corrcoef(d[pc], d[c])[0, 1] if d[pc].std() > 0 else np.nan,
                    "sd_projected": d[pc].std(), "sd_actual": d[c].std()})
    return pd.DataFrame(out), m
