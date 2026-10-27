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


def test_simulation_props(tmp_path):
    from nfl_proj.sim import Simulator, apply_lines, wide_means
    cache = tmp_path / "raw"
    write_cache(cache)
    t = build_season(2026, cache, tmp_path / "nfl.db", log=lambda *_: None)
    assert not t["defenders"].empty and not t["kickers"].empty
    plays = prep_plays(t["plays"], CFG)
    proj = Projector(plays, t["player_games"], t["games"], CFG)
    sim = Simulator(proj, t["player_games"], t["defenders"], t["kickers"], n_sims=800)
    props = sim.run_week(7)
    lines = pd.DataFrame([{"player": "BUF WR1", "stat": "rec_yds", "line": "60.5"}])
    props = apply_lines(props, lines)
    row = props[(props["player"] == "BUF WR1") & (props["stat"] == "rec_yds")].iloc[0]
    assert abs(row["p_over"] + row["p_under"] - 1) < 1e-9
    w = wide_means(props).set_index("player")
    # QB passing yards equal the sum of his receivers' yards.
    buf = w[w["team"] == "BUF"]
    assert abs(buf.loc["BUF QB", "pass_yds"] - buf["rec_yds"].sum()) < 1.0
    assert buf.loc["BUF QB", "longest_completion"] >= buf["longest_rec"].max() - 1e-6
    assert w.loc["BUF K", "kicking_points"] > 0
    assert w.loc["DAL LB1", "tackles"] > w.loc["DAL LB3", "tackles"]
    assert 0 < w.loc["BUF RB", "anytime_td"] <= 1
