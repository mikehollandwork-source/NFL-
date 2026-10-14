"""Strength of schedule, market team totals, availability, FTN join."""

import numpy as np
import pandas as pd

from nfl_proj.availability import auto_overrides, merge_overrides
from nfl_proj.market import implied_totals, team_misses
from nfl_proj.nflverse import add_ftn
from nfl_proj.ratings import fit_additive


def test_sos_credits_offense_that_faced_good_defenses():
    # A and B score the same raw points, but A faced the stingy defense S
    # (which holds everyone else to 14) while B faced the soft defense W.
    rows = [("A", "S", 20), ("B", "W", 20), ("C", "S", 14), ("C", "W", 30),
            ("D", "S", 14), ("D", "W", 30)] * 3
    df = pd.DataFrame(rows, columns=["offense", "defense", "points"])
    f = fit_additive(df, "points", lam=0.5)
    off = f["off"]
    assert abs(off.at["A", "raw"] - off.at["B", "raw"]) < 1e-9
    assert off.at["A", "adj"] > off.at["B", "adj"] + 5
    assert f["def"].at["S", "adj"] < f["def"].at["W", "adj"]


def test_implied_totals_and_misses():
    g = pd.DataFrame({"week": [1, 2, 3], "home": ["TEN", "TEN", "IND"], "away": ["IND", "HOU", "TEN"],
                      "spread_line": [-3.0, 2.0, 7.0], "total_line": [41.0, 40.0, 45.0],
                      "home_score": [10, 13, None], "away_score": [24, 20, None],
                      "boxscore_id": ["a", "b", None]})
    t = implied_totals(g)
    ten1 = t[(t["team"] == "TEN") & (t["week"] == 1)].iloc[0]
    assert ten1["implied"] == 19.0 and ten1["miss"] == -9.0
    ind3 = t[(t["team"] == "IND") & (t["week"] == 3)].iloc[0]
    assert ind3["implied"] == 26.0 and np.isnan(ind3["miss"])
    m = team_misses(t, before_week=3, k=6).set_index("team")
    # TEN: 10 vs 19, 13 vs 21 -> avg miss -8.5 over 2 games, shrunk by 2/(2+6)
    assert m.at["TEN", "under_rate"] == 1.0
    assert abs(m.at["TEN", "correction"] - (-8.5 * 2 / 8)) < 1e-9


def _pg(rows):
    return pd.DataFrame(rows, columns=["player_id", "player", "team", "week", "pass_att", "rush_att", "targets"])


def test_availability_carries_out_and_flags_qb():
    pg = _pg([("q1", "Lamar", "BAL", 4, 20, 3, 0), ("q2", "Huntley", "BAL", 5, 32, 2, 0),
              ("q2", "Huntley", "BAL", 4, 9, 0, 0), ("w1", "Flowers", "BAL", 5, 0, 0, 8)])
    inj = pd.DataFrame({"week": [5, 5], "team": ["BAL", "BAL"], "player_id": ["q1", "w1"],
                        "player": ["Lamar", "Flowers"], "report_status": ["Out", "Out"],
                        "injury": ["Ankle", "Hip"]})
    depth = pd.DataFrame({"team": ["BAL", "BAL"], "player_id": ["q1", "q2"],
                          "player": ["Lamar", "Huntley"], "rank": [1, 2]})
    auto, flags = auto_overrides(6, inj, depth, pg, ["BAL"], {})
    outs = set(auto[auto["status"] == "out"]["player"])
    # Lamar missed week 5 -> carried out; Flowers played week 5 despite the tag -> not carried
    assert outs == {"Lamar"}
    assert auto[auto["status"] == "starter"]["player"].tolist() == ["Huntley"]
    assert any("Lamar" in f and "listed out" in f for f in flags)
    # Once the week 6 report posts without Lamar ruled out, the depth chart QB1 starts.
    inj6 = pd.concat([inj, pd.DataFrame({"week": [6], "team": ["BAL"], "player_id": ["q1"], "player": ["Lamar"],
                                         "report_status": ["Questionable"], "injury": ["Ankle"]})])
    auto6, _ = auto_overrides(6, inj6, depth, pg, ["BAL"], {})
    assert auto6[auto6["status"] == "starter"]["player"].tolist() == ["Lamar"]


def test_manual_overrides_win():
    auto = pd.DataFrame({"team": ["CHI", "CHI"], "player": ["Bagent", "Swift"], "player_id": ["b", "s"],
                         "status": ["starter", "out"], "notes": ["", ""]})
    manual = pd.DataFrame({"team": ["CHI"], "player": ["Caleb Williams"], "status": ["starter"], "notes": [""]})
    m = merge_overrides(manual, auto)
    assert m[m["status"] == "starter"]["player"].tolist() == ["Caleb Williams"]
    assert "Swift" in set(m["player"])


def test_ftn_join_marks_blitz():
    plays = pd.DataFrame({"nv_game_id": ["g", "g", "g"], "play_id": [1, 2, 3]})
    ftn = pd.DataFrame({"nflverse_game_id": ["g", "g"], "nflverse_play_id": [1, 2],
                        "n_blitzers": [0, 1], "n_pass_rushers": [5, 4], "n_defense_box": [6, 7],
                        "is_play_action": [False, True], "is_screen_pass": [False, False],
                        "is_rpo": [False, False], "is_motion": [True, False]})
    out = add_ftn(plays, ftn).set_index("play_id")
    assert out.at[1, "is_blitz"] == 1.0 and out.at[2, "is_blitz"] == 1.0
    assert np.isnan(out.at[3, "is_blitz"])


def test_corners_out_and_shadow():
    from nfl_proj.corners import Corners
    cov = pd.DataFrame({
        "week": [1, 1, 1, 2, 2, 2], "team": ["DEN"] * 6,
        "player_id": ["s", "m", "b", "s", "m", "b"], "pfr_id": ["S", "M", "B", "S", "M", "B"],
        "player": ["Pat Surtain II", "Riley Moss", "Jahdae Barron"] * 2, "pos": ["CB"] * 6,
        "targets": [10, 10, 10, 10, 10, 10], "completions": [4, 6, 7] * 2,
        "yards": [40, 80, 100, 40, 80, 100], "td": [0] * 6, "ints": [0] * 6})
    pers = pd.DataFrame({"team": ["DEN"], "coordinator": ["VJ"], "coverage_lean": ["man"],
                         "scheme_notes": [""], "shadow_cb": ["Pat Surtain II"], "shadow_notes": [""],
                         "weak_spot": [""], "sources": [""], "as_of": [""], "confidence": ["medium"]})
    rec = pd.DataFrame({"player_id": ["w1", "w2", "t1"], "player": ["WR One", "WR Two", "TE"],
                        "pos": ["WR", "WR", "TE"], "share": [0.3, 0.2, 0.15]})
    cfg = {"corners": {"shrink_targets": 0.001}}
    healthy = Corners(cov, None, pers, set(), set(), cfg)
    f, notes = healthy.receiver_factors("DEN", rec)
    assert f["w1"] < 1 < f["w2"]          # WR1 draws the shadow; the rest face the weaker corners
    assert any("shadows with Pat Surtain II" in n for n in notes)
    hurt = Corners(cov, None, pers, {"s"}, set(), cfg)
    f2, notes2 = hurt.receiver_factors("DEN", rec)
    assert f2["w1"] > 1 and abs(f2["w1"] - f2["w2"]) < 1e-9 and 1 < f2["t1"] < f2["w1"]
    assert any("is out: no shadow" in n for n in notes2)


def test_market_only_for_consistent_teams():
    from nfl_proj.market import Market
    # TEN lands within 4 of its implied total every game; IND misses by 10 every game.
    rows = []
    for w in range(1, 6):
        rows.append({"week": w, "home": "TEN", "away": "IND", "spread_line": 0.0, "total_line": 40.0,
                     "home_score": 21 if w % 2 else 18, "away_score": 30, "boxscore_id": f"g{w}"})
    rows.append({"week": 6, "home": "TEN", "away": "IND", "spread_line": 3.0, "total_line": 44.0,
                 "home_score": None, "away_score": None, "boxscore_id": None})
    m = Market(pd.DataFrame(rows), {"market": {"enabled": True}})
    ten, ind = m.line("TEN", 6), m.line("IND", 6)
    assert ind is None
    assert ten["target"] == 23.5 and ten["hit_rate"] == 1.0
    b = m.blend(ten, 20.0)
    assert abs(b["blended_pts"] - (0.6 * 23.5 + 0.4 * 20.0)) < 1e-9 and "dropback_shift" not in b
