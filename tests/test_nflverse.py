"""nflverse mapping, using rows copied from the real 2026 play-by-play
(2026_01_ARI_LAC) with the columns ``classify`` reads."""

import pandas as pd

from nfl_proj import nflverse
from nfl_proj.nflverse import classify, team

BASE = {"interception": 0.0, "fumble": 0.0, "touchdown": 0.0, "penalty": 0.0, "shotgun": 0,
        "no_huddle": 0, "sack": 0.0, "qb_scramble": 0, "complete_pass": 0.0,
        "two_point_attempt": 0.0, "timeout": 0.0}


def row(**kw):
    return {**BASE, **kw}


def test_complete_deep_pass():
    # 7-J.Brissett pass deep right to 85-T.McBride to LAC 43 for 27 yards (2-E.Molden).
    out = classify(row(play_type="pass", yards_gained=27.0, complete_pass=1.0, pass_length="deep",
                       pass_location="right", passer_player_id="00-0033119",
                       receiver_player_id="00-0037744", solo_tackle_1_player_id="00-0036992"))
    assert out["play_type"] == "pass" and out["bucket"] == "pass_deep_right"
    assert out["complete"] and out["yards"] == 27.0
    assert out["passer_id"] == "00-0033119" and out["target_id"] == "00-0037744"
    assert out["tacklers"] == "00-0036992"


def test_sack_is_not_a_pass():
    # (Shotgun) 10-J.Herbert sacked at ARI 13 for -10 yards (55-D.Stills).
    out = classify(row(play_type="pass", yards_gained=-10.0, sack=1.0, shotgun=1,
                       passer_player_id="00-0036355", sack_player_id="00-0038623"))
    assert out["play_type"] == "sack" and out["yards"] == -10.0
    assert out["sackers"] == "00-0038623" and out["shotgun"]


def test_scramble_and_run_gaps():
    # 7-J.Brissett scrambles left end ran ob at LAC 30 for 11 yards
    scr = classify(row(play_type="run", yards_gained=11.0, qb_scramble=1, run_location="left",
                       run_gap="end", rusher_player_id="00-0033119"))
    assert scr["play_type"] == "scramble" and scr["rusher_id"] == "00-0033119"
    mid = classify(row(play_type="run", yards_gained=2.0, run_location="middle",
                       rusher_player_id="00-0033119"))
    assert mid["bucket"] == "run_middle"
    end = classify(row(play_type="run", yards_gained=4.0, run_location="right", run_gap="end"))
    tackle = classify(row(play_type="run", yards_gained=4.0, run_location="left", run_gap="tackle"))
    assert end["bucket"] == "run_outside_right" and tackle["bucket"] == "run_inside_left"


def test_kicks():
    # 38-C.Ryland 54 yard field goal is No Good, Hit Right Upright
    fg = classify(row(play_type="field_goal", kick_distance=54.0, field_goal_result="missed",
                      kicker_player_id="00-0038567"))
    assert fg["play_type"] == "special" and fg["kick_type"] == "fg"
    assert fg["kick_good"] is False and fg["kick_distance"] == 54.0
    xp = classify(row(play_type="extra_point", extra_point_result="good", kicker_player_id="00-0038567"))
    assert xp["kick_type"] == "xp" and xp["kick_good"] is True


def test_timeout_is_not_a_penalty():
    # "Timeout #1 by ARI at 09:34." is play_type no_play in nflverse
    assert classify(row(play_type="no_play", timeout=1.0))["play_type"] == "timeout"
    assert classify(row(play_type="no_play", penalty=1.0))["play_type"] == "penalty"


def test_interception():
    # 10-J.Herbert pass deep right intended for 12-D.Davis INTERCEPTED by 28-A.Wingard
    out = classify(row(play_type="pass", interception=1.0, pass_length="deep", pass_location="right",
                       passer_player_id="00-0036355", receiver_player_id="00-0038573",
                       interception_player_id="00-0035378"))
    assert out["interception"] and out["interceptor_id"] == "00-0035378" and not out["complete"]


def test_team_codes_match_pfr():
    assert team("GB") == "GNB" and team("KC") == "KAN" and team("LA") == "LAR"
    assert team("OAK") == "LVR" and team("ARI") == "ARI" and team(float("nan")) is None


def test_games_mark_played_by_pbp():
    g = pd.DataFrame({"season": [2026, 2026], "game_type": ["REG", "REG"], "week": [1, 6],
                      "gameday": ["2026-09-13", "2026-10-18"], "away_team": ["ARI", "GB"],
                      "home_team": ["LAC", "DAL"], "location": ["Home", "Home"],
                      "game_id": ["2026_01_ARI_LAC", "2026_06_GB_DAL"],
                      "pfr": ["202609130sdg", "202610180dal"]})
    out = nflverse.parse_games(g, 2026, {"2026_01_ARI_LAC"})
    assert out.loc[0, "boxscore_id"] == "202609130sdg" and out.loc[0, "home"] == "LAC"
    assert pd.isna(out.loc[1, "boxscore_id"]) and out.loc[1, "away"] == "GNB"
