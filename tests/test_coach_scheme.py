import tomllib
from pathlib import Path

import pandas as pd

from nfl_proj.build import build_season
from nfl_proj.coaches import parse_history, parse_team_season, profiles
from nfl_proj.external import parse_scheme_tables, scheme_labels
from nfl_proj.profiles import prep_plays
from nfl_proj.project import Projector

from .synthetic import write_cache

CFG = tomllib.loads((Path(__file__).parent.parent / "config" / "projection.toml").read_text())


def test_parse_history():
    h = parse_history("GNB:2006-2008;DAL:2024")
    assert h == [("GNB", 2006), ("GNB", 2007), ("GNB", 2008), ("DAL", 2024)]
    assert parse_history("") == []


def test_parse_team_season():
    html = """<table id="team_stats"><tbody>
      <tr><th data-stat="player">Team Stats</th><td data-stat="points">450</td>
          <td data-stat="pass_att">600</td><td data-stat="rush_att">400</td></tr>
      <tr><th data-stat="player">Opp. Stats</th><td data-stat="points">350</td></tr>
    </tbody></table>
    <!--<table id="receiving_and_rushing"><tbody>
      <tr><td data-stat="player">WR A</td><td data-stat="targets">150</td><td data-stat="rush_att">0</td></tr>
      <tr><td data-stat="player">WR B</td><td data-stat="targets">100</td><td data-stat="rush_att">2</td></tr>
      <tr><td data-stat="player">RB C</td><td data-stat="targets">50</td><td data-stat="rush_att">250</td></tr>
    </tbody></table>-->"""
    ts = parse_team_season(html)
    assert ts["pass_att"] == 600 and ts["points_against"] == 350
    assert abs(ts["top_target_share"] - 0.5) < 1e-9
    assert abs(ts["rb1_carry_share"] - 250 / 252) < 1e-9


def _coach_rows():
    return pd.DataFrame([
        {"team": "BUF", "head_coach": "A", "hc_first_nfl_season": "2010", "hc_first_season_with_team": "2015",
         "play_caller": "A", "caller_role": "HC", "caller_first_season_calling": "2010",
         "new_caller_2026": "no", "caller_history": "BUF:2015-2016", "source": "", "confidence": "high"},
        {"team": "DAL", "head_coach": "B", "hc_first_nfl_season": "2026", "hc_first_season_with_team": "2026",
         "play_caller": "C", "caller_role": "OC", "caller_first_season_calling": "2026",
         "new_caller_2026": "yes", "caller_history": "", "source": "", "confidence": "high"},
    ])


def test_coach_profiles_labels():
    hist = pd.DataFrame([
        {"team_now": "BUF", "play_caller": "A", "team": "BUF", "season": y, "pass_rate": 0.66,
         "league_pass_rate": 0.58, "point_diff_pg": 0.0, "top_target_share": 0.33,
         "top2_target_share": 0.5, "rb1_carry_share": 0.6} for y in (2015, 2016)])
    prof = profiles(_coach_rows(), hist, 2026).set_index("team")
    assert prof.loc["BUF", "style"] == "pass-first"
    assert prof.loc["BUF", "star_reliance"] == "leans on stars"
    assert prof.loc["BUF", "hc_tier"] == "veteran HC"
    assert prof.loc["DAL", "hc_tier"] == "first-year HC"
    assert prof.loc["DAL", "caller_tier"] == "first-time play-caller"
    assert prof.loc["DAL", "style"] == "no history"


def test_sharp_table_parser_and_labels():
    from nfl_proj.external import TEAM_NAMES
    vals = {"Vikings": (66.5, 20), "Browns": (25, 46.5), "Lions": (15, 15.7)}
    rows = "".join(f"<tr><td>City {n}</td><td>{vals.get(n, (27, 24))[0]}%</td><td>{vals.get(n, (27, 24))[1]}%</td></tr>"
                   for n in TEAM_NAMES)
    html = f"<table><tr><th>Team</th><th>Blitz Rate</th><th>Man %</th></tr>{rows}</table>"
    df = parse_scheme_tables(html).set_index("team")
    assert df.loc["MIN", "blitz_rate"] == 66.5 and df.loc["CLE", "man_rate"] == 46.5
    lab = scheme_labels(df.reset_index(), pd.DataFrame(), CFG).set_index("team")
    assert lab.loc["MIN", "blitz"] == "heavy" and lab.loc["DET", "blitz"] == "light"
    assert lab.loc["CLE", "coverage"] == "man_heavy" and lab.loc["DET", "coverage"] == "zone_heavy"
    manual = pd.DataFrame([{"team": "MIN", "base_coverage": "cover 3", "third_down_blitz": "light"}])
    lab2 = scheme_labels(df.reset_index(), manual, CFG).set_index("team")
    assert lab2.loc["MIN", "blitz"] == "light" and lab2.loc["MIN", "shell"] == "cover3"


def test_scheme_and_coach_change_projection(tmp_path):
    write_cache(tmp_path / "raw")
    t = build_season(2026, tmp_path / "raw", tmp_path / "nfl.db", log=lambda *_: None)
    plays = prep_plays(t["plays"], CFG)
    scheme = pd.DataFrame([{"team": tm, "blitz": "heavy" if tm in ("DAL", "KAN") else "light",
                            "coverage": "", "shell": "", "scheme_source": "test"}
                           for tm in ("BUF", "DAL", "KAN", "PHI")])
    base = Projector(plays, t["player_games"], t["games"], CFG)
    with_scheme = Projector(plays, t["player_games"], t["games"], CFG, scheme=scheme)
    eff = with_scheme.scheme_effect("BUF", "DAL")
    assert all(0.6 <= v <= 1.6 for v in eff["ypp"].values()) and 0.5 <= eff["deep_share"] <= 2.0
    assert base.scheme_effect("BUF", "DAL")["ypp"] == {"deep": 1.0, "short": 1.0, "run": 1.0}

    # A play-caller who historically feeds his WR1 should push WR1 targets up.
    hist = pd.DataFrame([{"team_now": "BUF", "play_caller": "A", "team": "BUF", "season": 2015,
                          "pass_rate": 0.6, "league_pass_rate": 0.6, "point_diff_pg": 0.0,
                          "top_target_share": 0.45, "top2_target_share": 0.6, "rb1_carry_share": 0.9}])
    coach = profiles(_coach_rows(), hist, 2026)
    star = Projector(plays, t["player_games"], t["games"], CFG, coach=coach)
    df0, _ = base.project_week(7)
    df1, _ = star.project_week(7)
    tg = lambda df: df[(df["team"] == "BUF")].set_index("player")["targets"]
    assert tg(df1).max() > tg(df0).max()
    assert abs(tg(df1).sum() - tg(df0).sum()) < 0.5   # same team volume, redistributed
