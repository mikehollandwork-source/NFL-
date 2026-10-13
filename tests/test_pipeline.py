import tomllib
from pathlib import Path

import pandas as pd

from nfl_proj import adaptation
from nfl_proj.build import build_season, load_season
from nfl_proj.parse_pfr import parse_schedule
from nfl_proj.profiles import (combined_labels, defense_profile, matchup_splits, offense_style,
                               prep_plays)
from nfl_proj.project import Projector
from nfl_proj.report import styles_report, week_report

from .synthetic import render_schedule, write_cache

CFG = tomllib.loads((Path(__file__).parent.parent / "config" / "projection.toml").read_text())


def test_schedule_home_away():
    games = parse_schedule(render_schedule(), 2026)
    g1 = games[0]
    assert (g1["away"], g1["home"], g1["week"]) == ("KAN", "BUF", 1)
    assert g1["boxscore_id"] == "202609010buf"
    assert games[-1]["boxscore_id"] is None and len(games) == 14


def test_end_to_end(tmp_path):
    cache = tmp_path / "raw"
    write_cache(cache)
    t = build_season(2026, cache, tmp_path / "nfl.db", log=lambda *_: None)
    assert len(t["plays"]) > 1000
    t = load_season(tmp_path / "nfl.db")

    plays = prep_plays(t["plays"], CFG)
    # Possession inference: every scrimmage play has an offense from the 4 teams.
    assert plays["offense"].isin(["KAN", "BUF", "PHI", "DAL"]).all()
    assert set(plays["bucket"].dropna()) >= {"pass_deep_left", "run_middle", "run_outside_left"}

    style = offense_style(plays, t["plays"])
    dprof = defense_profile(plays)
    assert len(style) == 4 and len(dprof) == 4
    # DAL was generated soft vs deep passes.
    assert dprof.set_index("team")["epa_allowed_deep"].idxmax() == "DAL"
    labels = combined_labels(dprof, pd.DataFrame(), "auto")
    assert labels.set_index("team").loc["DAL", "deep_pass_d"] == "soft_deep"

    est = adaptation.estimate(plays, CFG["adaptation"]["min_plays"])
    assert est["n"] > 30
    strength = adaptation.effective_strength(est, CFG)

    proj = Projector(plays, t["player_games"], t["games"], CFG, labels)
    df, ctx = proj.project_week(7)
    assert len(ctx) == 4
    qb = df[(df["team"] == "BUF") & (df["pass_att"] > 0)]
    assert len(qb) == 1 and 15 < qb["pass_att"].iloc[0] < 60
    # Receivers' projected targets add up to the team's pass attempts.
    buf = df[df["team"] == "BUF"]
    assert abs(buf["targets"].sum() - qb["pass_att"].iloc[0]) < 0.5
    assert (df[["rec_yds", "rush_yds", "pass_yds"]] >= -5).all().all()

    md = week_report(7, df, ctx, style, dprof, labels, CFG, est, strength)
    assert "BUF vs DAL" in md
    assert "Do coaches" in styles_report(style, dprof, labels, matchup_splits(plays, labels), est)


def test_out_override_removes_player(tmp_path):
    cache = tmp_path / "raw"
    write_cache(cache)
    t = build_season(2026, cache, tmp_path / "nfl.db", log=lambda *_: None)
    plays = prep_plays(t["plays"], CFG)
    ov = pd.DataFrame([{"team": "BUF", "player": "BUF WR1", "status": "out"}])
    df, _ = Projector(plays, t["player_games"], t["games"], CFG, None, ov).project_week(7)
    assert "BUF WR1" not in set(df["player"])
    buf = df[df["team"] == "BUF"]
    assert abs(buf["targets"].sum() - buf["pass_att"].max()) < 0.5
