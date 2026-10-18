"""Automatic player availability from the injury report and depth charts.

Produces rows in the same shape as ``data/manual/player_overrides.csv``
(team, player, status, notes) plus ``player_id``. Your manual file always
wins over these.

Rules:
  * Out (and Doubtful, unless ``availability.doubtful_plays``) on the
    projected week's injury report -> ``out``.
  * The report is published Wednesday-Friday. Before that, a player listed
    Out last week who also didn't play last week is carried forward as out,
    flagged so you can re-check once the new report posts.
  * Starting QB: the depth chart's QB1, if he played in one of the team's
    last two games or is on this week's report as active. Otherwise the QB
    who took the most snaps last game, flagged for review.
"""

from __future__ import annotations

import pandas as pd


def auto_overrides(week: int, injuries: pd.DataFrame | None, depth: pd.DataFrame | None,
                   player_games: pd.DataFrame, teams: list[str], cfg: dict) -> tuple[pd.DataFrame, list[str]]:
    c = cfg.get("availability", {})
    out_statuses = {"Out"} | (set() if c.get("doubtful_plays", False) else {"Doubtful"})
    rows, flags = [], []
    pg = player_games

    def played_in(pid, team, weeks):
        return bool(((pg["player_id"] == pid) & (pg["team"] == team) & pg["week"].isin(weeks)
                     & ((pg["pass_att"] + pg["rush_att"] + pg["targets"]) > 0)).any())

    inj = injuries if injuries is not None else pd.DataFrame(columns=["week", "report_status"])
    this_week = inj[(inj["week"] == week) & inj["report_status"].notna()]
    report_posted = len(this_week) > 0
    prev = inj[(inj["week"] == week - 1) & inj["report_status"].notna()]
    if not report_posted and len(inj):
        flags.append(f"The week {week} injury report isn't out yet (posts Wed-Fri); players Out last week "
                     f"who also missed last week's game are carried as out. Re-run after it posts.")

    for team in teams:
        tw = sorted(pg[pg["team"] == team]["week"].unique())
        last_week = tw[-1] if tw else None
        recent = tw[-2:]
        src = this_week if report_posted else prev
        for r in src[src["team"] == team].itertuples():
            if r.report_status not in out_statuses:
                continue
            if not report_posted and last_week is not None and played_in(r.player_id, team, [last_week]):
                continue
            note = (f"week {week} report: {r.report_status} ({r.injury})" if report_posted
                    else f"carried from week {week - 1} report: {r.report_status} ({r.injury})")
            rows.append({"team": team, "player": r.player, "player_id": r.player_id, "status": "out",
                         "notes": note})

        # Starting quarterback
        if depth is None or depth.empty:
            continue
        out_ids = {x["player_id"] for x in rows if x["team"] == team}
        qbs = depth[depth["team"] == team].sort_values("rank")
        qb1 = qbs.iloc[0] if len(qbs) else None
        last_qb = pg[(pg["team"] == team) & (pg["week"] == last_week) & (pg["pass_att"] > 0)] \
            .sort_values("pass_att", ascending=False)
        last_qb = last_qb.iloc[0] if len(last_qb) else None
        # Once this week's report is out, a QB1 not ruled out is expected to play.
        active_now = report_posted and qb1 is not None
        if qb1 is not None and qb1["player_id"] not in out_ids and (
                played_in(qb1["player_id"], team, recent) or active_now):
            pick, note = qb1, "depth chart QB1"
        elif last_qb is not None and last_qb["player_id"] in out_ids and qbs[~qbs["player_id"].isin(out_ids)].shape[0]:
            # Last game's starter is out too: next healthy QB on the depth chart
            pick = qbs[~qbs["player_id"].isin(out_ids)].iloc[0]
            note = "next healthy QB on the depth chart"
            flags.append(f"{team}: {last_qb['player']} is listed out; projecting {pick['player']} (depth chart). "
                         f"Check the week {week} report.")
        elif last_qb is not None:
            pick, note = last_qb, "started last game"
            if qb1 is not None and qb1["player_id"] != last_qb["player_id"]:
                why = ("is listed out" if qb1["player_id"] in out_ids
                       else "hasn't played in the team's last two games")
                flags.append(f"{team}: depth chart lists {qb1['player']} as QB1 but he {why}; projecting "
                             f"{last_qb['player']}. Check the week {week} report.")
        else:
            continue
        rows.append({"team": team, "player": pick["player"], "player_id": pick["player_id"],
                     "status": "starter", "notes": note})
    return pd.DataFrame(rows, columns=["team", "player", "player_id", "status", "notes"]), flags


def merge_overrides(manual: pd.DataFrame | None, auto: pd.DataFrame) -> pd.DataFrame:
    """Manual rows win: any team+status your file sets for a starter, or any
    player it names, replaces the automatic row."""
    if manual is None or manual.empty:
        return auto
    m = manual.copy()
    if "player_id" not in m:
        m["player_id"] = ""
    m_starters = set(m.loc[m["status"].str.lower() == "starter", "team"])
    keep = auto[~auto["player"].isin(set(m["player"]))
                & ~((auto["status"] == "starter") & auto["team"].isin(m_starters))]
    return pd.concat([m, keep], ignore_index=True).fillna("")
