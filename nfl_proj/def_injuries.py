"""Missing defensive starters -> opponent yards per play.

Measured on 2021-25 (tools/def_injury_test.py, factor_tests.md section 10):
per missing starter, a defense allowed (beyond its season-to-date level and
the offense's) +0.040 EPA/dropback for a CB, +0.035 for a LB, and +0.024
EPA/rush for a S, +0.016 for a CB. Converted to yards per play (pass 0.137
EPA/yard at 6.3 yds/dropback, run 0.116 at 4.2 yds/rush). Edge / interior
line effects were not significant and are left out.

Starter = averaged 60%+ of defensive snaps over his previous 3 games (2+),
and played in one of the team's last two games. Missing = listed Out /
Doubtful / IR this week (live), or < 20% of snaps in the game (replays,
equivalent to knowing the inactives at lock).
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from .odds import norm_name

GROUP = {"DE": "EDGE", "OLB": "LB", "DT": "IDL", "NT": "IDL", "LB": "LB", "ILB": "LB", "MLB": "LB",
         "CB": "CB", "FS": "S", "SS": "S", "S": "S", "DB": "S"}
DEFAULT = {"pass": {"CB": 0.047, "LB": 0.041}, "run": {"S": 0.049, "CB": 0.033}, "cap": 1.25}


def load_snaps(raw_dir: Path, season: int) -> pd.DataFrame:
    f = Path(raw_dir) / f"snap_counts_{season}.csv.gz"
    if not f.exists():
        return pd.DataFrame()
    s = pd.read_csv(f, low_memory=False)
    s = s[(s["game_type"] == "REG") & s["position"].isin(GROUP)].copy()
    # Snap files can label every defensive back "DB": take CB / FS / SS / OLB etc. from the weekly roster
    r = Path(raw_dir) / f"roster_weekly_{season}.csv.gz"
    if r.exists():
        ro = pd.read_csv(r, low_memory=False, usecols=lambda c: c in ("pfr_id", "depth_chart_position", "position"))
        ro = ro.dropna(subset=["pfr_id"]).drop_duplicates("pfr_id", keep="last")
        dcp = dict(zip(ro["pfr_id"], ro["depth_chart_position"].fillna(ro["position"])))
        s["position"] = [dcp.get(i, p) if dcp.get(i, p) in GROUP else p for i, p in zip(s["pfr_player_id"], s["position"])]
    s["grp"] = s["position"].map(GROUP)
    s["key"] = s["player"].map(norm_name)
    return s


def nv_team(t: str) -> str:
    from .nflverse import NV_TO_PFR
    return NV_TO_PFR.get(t, t)


def starters(snaps: pd.DataFrame, team: str, week: int) -> pd.DataFrame:
    s = snaps[(snaps["team_pfr"] == team) & (snaps["week"] < week)]
    wks = sorted(s["week"].unique())
    if len(wks) < 2:
        return s.iloc[0:0]
    prev = s[s["week"].isin(wks[-3:])]
    avg = prev.groupby(["pfr_player_id", "player", "key", "grp"]).agg(n=("defense_pct", "size"),
                                                                     pct=("defense_pct", "mean")).reset_index()
    recent = set(s[s["week"].isin(wks[-2:]) & (s["defense_pct"] >= 0.2)]["pfr_player_id"])
    return avg[(avg["n"] >= 2) & (avg["pct"] >= 0.6) & avg["pfr_player_id"].isin(recent)]


def missing(snaps: pd.DataFrame, injuries: pd.DataFrame | None, team: str, week: int, asof: bool) -> pd.DataFrame:
    st = starters(snaps, team, week)
    if st.empty:
        return st
    if asof:
        now = snaps[(snaps["team_pfr"] == team) & (snaps["week"] == week) & (snaps["defense_pct"] >= 0.2)]
        if now.empty:      # game not in the snap file yet
            return st.iloc[0:0]
        return st[~st["pfr_player_id"].isin(set(now["pfr_player_id"]))]
    if injuries is None or injuries.empty:
        return st.iloc[0:0]
    i = injuries[(injuries["week"] == week) & (injuries["team"] == team)
                 & injuries["report_status"].isin(["Out", "Doubtful", "IR"])]
    out = set(i["player"].map(norm_name))
    return st[st["key"].isin(out)]


def effect(miss: pd.DataFrame, cfg: dict) -> dict:
    c = {**DEFAULT, **cfg.get("def_injuries", {})}
    n = miss["grp"].value_counts().to_dict() if len(miss) else {}
    pas = 1 + sum(c["pass"].get(g, 0) * k for g, k in n.items())
    run = 1 + sum(c["run"].get(g, 0) * k for g, k in n.items())
    return {"pass": min(pas, c["cap"]), "run": min(run, c["cap"]), "missing": list(miss["player"]) if len(miss) else []}
