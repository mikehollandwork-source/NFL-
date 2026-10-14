"""Load play-by-play, box score stats and snap counts from nflverse.

Pro-Football-Reference sits behind a Cloudflare bot check that cloud
machines can't pass, so the default source is nflverse
(https://github.com/nflverse/nflverse-data): free, public CSV releases with
structured play-by-play (play type, pass depth/direction, run gap, EPA,
tacklers) built from the NFL's own game feed. Files are downloaded once and
cached under ``data/raw/nflverse``.

``build_season`` writes the same tables, columns and team codes as the PFR
path in ``build.py`` (PFR abbreviations such as GNB / KAN / LVR, and PFR
boxscore ids for games), so everything downstream and every file in
``data/manual`` keeps working unchanged. Player ids are NFL GSIS ids
(``00-0034796``) instead of PFR ids.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
import requests

from .playparse import is_success

RELEASES = "https://github.com/nflverse/nflverse-data/releases/download"
GAMES_URL = "https://raw.githubusercontent.com/nflverse/nfldata/master/data/games.csv"

# nflverse code -> PFR abbreviation used everywhere else in this project.
NV_TO_PFR = {"GB": "GNB", "KC": "KAN", "LV": "LVR", "LA": "LAR", "NE": "NWE", "NO": "NOR",
             "SF": "SFO", "TB": "TAM",
             # Relocated franchises in older seasons
             "OAK": "LVR", "SD": "LAC", "STL": "LAR"}


def team(code):
    if not isinstance(code, str) or not code:
        return None
    return NV_TO_PFR.get(code, code)


def season_files(season: int) -> dict[str, str]:
    return {
        "pbp": f"{RELEASES}/pbp/play_by_play_{season}.csv.gz",
        "player_week": f"{RELEASES}/stats_player/stats_player_week_{season}.csv.gz",
        "snaps": f"{RELEASES}/snap_counts/snap_counts_{season}.csv.gz",
        "rosters": f"{RELEASES}/weekly_rosters/roster_weekly_{season}.csv.gz",
        # FTN charting: blitzers, pass rushers, play action, screens, box count per play
        "ftn": f"{RELEASES}/ftn_charting/ftn_charting_{season}.csv",
        "injuries": f"{RELEASES}/injuries/injuries_{season}.csv.gz",
        "depth": f"{RELEASES}/depth_charts/depth_charts_{season}.csv.gz",
        # PFR advanced defense per defender per game (pressures, hurries, QB hits)
        "adv_def": f"{RELEASES}/pfr_advstats/advstats_week_def_{season}.csv.gz",
    }

# Files the build can run without (charting and injury feeds can lag).
OPTIONAL = {"ftn", "injuries", "depth", "adv_def"}


class Downloader:
    """Cache-first file downloader. ``refresh`` re-downloads (used for the
    current season, which nflverse updates nightly during the season)."""

    def __init__(self, cache_dir: Path, log=print):
        self.dir = Path(cache_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.log = log

    def path(self, url: str) -> Path:
        return self.dir / url.rsplit("/", 1)[-1]

    def get(self, url: str, refresh: bool = False) -> Path:
        p = self.path(url)
        if p.exists() and not refresh:
            return p
        resp = requests.get(url, timeout=120)
        resp.raise_for_status()
        p.write_bytes(resp.content)
        self.log(f"downloaded {p.name} ({len(resp.content) / 1e6:.1f} MB)")
        return p


def download_season(season: int, cache_dir: Path, log=print, refresh: bool = True) -> None:
    d = Downloader(cache_dir, log)
    d.get(GAMES_URL, refresh=refresh)
    for key, url in season_files(season).items():
        try:
            d.get(url, refresh=refresh)
        except requests.HTTPError as exc:
            if key not in OPTIONAL:
                raise
            log(f"warning: optional {key} file unavailable ({exc}); continuing without it")


# --------------------------------------------------------------------------
# Games
# --------------------------------------------------------------------------

def parse_games(games: pd.DataFrame, season: int, played_ids: set[str]) -> pd.DataFrame:
    """Regular-season schedule. ``boxscore_id`` (PFR id) is set only for games
    that have play-by-play, which is how the rest of the code tells played
    games from upcoming ones."""
    g = games[(games["season"] == season) & (games["game_type"] == "REG")]
    out = pd.DataFrame({
        "season": season, "week": g["week"].astype(int), "date": g["gameday"],
        "away": g["away_team"].map(team), "home": g["home_team"].map(team),
        "boxscore_id": np.where(g["game_id"].isin(played_ids), g["pfr"], None),
        "neutral": g["location"].eq("Neutral"), "nv_game_id": g["game_id"],
        # Market: spread_line > 0 means the home team is favored by that many points.
        "spread_line": g["spread_line"], "total_line": g["total_line"],
        "gametime": g.get("gametime"), "stadium_id": g.get("stadium_id"), "sched_roof": g.get("roof"),
        "home_score": g["home_score"], "away_score": g["away_score"],
    })
    return out.reset_index(drop=True)


# --------------------------------------------------------------------------
# Plays
# --------------------------------------------------------------------------

def _ids(row, cols) -> str:
    return ",".join(str(row[c]) for c in cols if isinstance(row.get(c), str) and row[c])


TACKLE_COLS = ["solo_tackle_1_player_id", "solo_tackle_2_player_id",
               "tackle_with_assist_1_player_id", "tackle_with_assist_2_player_id",
               "assist_tackle_1_player_id", "assist_tackle_2_player_id",
               "assist_tackle_3_player_id", "assist_tackle_4_player_id"]
SACK_COLS = ["sack_player_id", "half_sack_1_player_id", "half_sack_2_player_id"]


def _flag(v) -> bool:
    return bool(v) and not (isinstance(v, float) and np.isnan(v))


def classify(r: dict) -> dict:
    """Map one nflverse play row onto the fields ``playparse.parse_detail``
    produces from PFR text, so both sources feed identical columns."""
    pt = r.get("play_type")
    out = {
        "play_type": "other", "bucket": None, "depth": None, "direction": None,
        "yards": r.get("yards_gained") if pd.notna(r.get("yards_gained")) else None,
        "complete": None, "interception": _flag(r.get("interception")),
        "fumble": _flag(r.get("fumble")), "touchdown": _flag(r.get("touchdown")),
        "penalty": _flag(r.get("penalty")), "no_play": pt == "no_play",
        "shotgun": _flag(r.get("shotgun")), "no_huddle": _flag(r.get("no_huddle")),
        "passer_id": None, "target_id": None, "rusher_id": None,
        "kicker_id": None, "kick_type": None, "kick_distance": None, "kick_good": None,
        "tacklers": _ids(r, TACKLE_COLS), "sackers": _ids(r, SACK_COLS),
        "interceptor_id": r.get("interception_player_id") if isinstance(r.get("interception_player_id"), str) else None,
    }
    s = lambda k: r.get(k) if isinstance(r.get(k), str) else None  # noqa: E731

    if pt == "no_play":
        # nflverse also files timeouts and other dead-ball rows as no_play.
        out["play_type"] = ("timeout" if _flag(r.get("timeout")) and not out["penalty"]
                            else "penalty" if out["penalty"] else "other")
        return out
    if pt is None or (isinstance(pt, float) and np.isnan(pt)):
        out["play_type"] = "timeout" if _flag(r.get("timeout")) else "other"
        return out
    if pt in ("kickoff", "punt", "field_goal", "extra_point") or _flag(r.get("two_point_attempt")):
        out["play_type"] = "special"
        if pt == "field_goal":
            out.update(kick_type="fg", kick_distance=r.get("kick_distance"),
                       kick_good=r.get("field_goal_result") == "made", kicker_id=s("kicker_player_id"))
        elif pt == "extra_point":
            out.update(kick_type="xp", kick_good=r.get("extra_point_result") == "good",
                       kicker_id=s("kicker_player_id"))
        return out
    if pt == "qb_kneel":
        out["play_type"] = "kneel"
        return out
    if pt == "qb_spike":
        out["play_type"] = "spike"
        return out
    if _flag(r.get("sack")):
        out["play_type"] = "sack"
        out["passer_id"] = s("passer_player_id")
        if out["yards"] is None:
            out["yards"] = 0.0
        return out
    if _flag(r.get("qb_scramble")):
        out["play_type"] = "scramble"
        out["rusher_id"] = s("rusher_player_id") or s("passer_player_id")
        return out
    if pt == "pass":
        out["play_type"] = "pass"
        out["passer_id"] = s("passer_player_id")
        out["target_id"] = s("receiver_player_id")
        out["complete"] = _flag(r.get("complete_pass"))
        if not out["complete"]:
            out["yards"] = 0.0
        depth, direction = s("pass_length"), s("pass_location")
        out["depth"], out["direction"] = depth, direction
        if depth and direction:
            out["bucket"] = f"pass_{depth}_{direction}"
        return out
    if pt == "run":
        out["play_type"] = "run"
        out["rusher_id"] = s("rusher_player_id")
        loc, gap = s("run_location"), s("run_gap")
        out["direction"] = loc
        if loc == "middle":
            out["bucket"] = "run_middle"
        elif loc and gap:
            out["bucket"] = (f"run_outside_{loc}" if gap == "end" else f"run_inside_{loc}")
        return out
    return out


PBP_COLS = ["game_id", "play_id", "week", "qtr", "time", "down", "ydstogo", "yardline_100",
            "posteam", "defteam", "score_differential", "desc", "epa", "play_type",
            "yards_gained", "interception", "fumble", "touchdown", "penalty", "shotgun",
            "no_huddle", "sack", "qb_scramble", "complete_pass", "two_point_attempt", "timeout",
            "pass_length", "pass_location", "run_location", "run_gap", "kick_distance",
            "field_goal_result", "extra_point_result", "passer_player_id", "receiver_player_id",
            "rusher_player_id", "kicker_player_id", "interception_player_id",
            "fixed_drive", "fixed_drive_result", "game_seconds_remaining", "drive_time_of_possession",
            "drive_play_count", *TACKLE_COLS, *SACK_COLS]


def _mmss(v):
    """'6:11' -> 371 seconds."""
    if not isinstance(v, str) or ":" not in v:
        return None
    m, _, sec = v.partition(":")
    try:
        return int(m) * 60 + int(sec)
    except ValueError:
        return None


def build_plays(pbp: pd.DataFrame, games: pd.DataFrame, season: int) -> pd.DataFrame:
    box = dict(zip(games["nv_game_id"], games["boxscore_id"]))
    pbp = pbp[[c for c in PBP_COLS if c in pbp.columns]]
    rows = []
    for seq_game, (gid, gp) in enumerate(pbp.groupby("game_id", sort=False)):
        for seq, r in enumerate(gp.to_dict("records")):
            parsed = classify(r)
            down = int(r["down"]) if pd.notna(r["down"]) else None
            ytg = float(r["ydstogo"]) if pd.notna(r["ydstogo"]) else None
            rows.append({
                "boxscore_id": box.get(gid), "nv_game_id": gid, "play_id": r["play_id"],
                "season": season, "week": int(r["week"]),
                "seq": seq, "quarter": int(r["qtr"]) if pd.notna(r["qtr"]) else None,
                "clock": r["time"] if isinstance(r["time"], str) else "",
                "down": down, "ytg": ytg,
                "yardline_100": r["yardline_100"] if pd.notna(r["yardline_100"]) else None,
                "offense": team(r["posteam"]), "defense": team(r["defteam"]),
                "score_diff": r["score_differential"] if pd.notna(r["score_differential"]) else None,
                "detail": r["desc"] if isinstance(r["desc"], str) else "",
                "epa": r["epa"] if pd.notna(r["epa"]) else None,
                "drive": r.get("fixed_drive"), "drive_result": r.get("fixed_drive_result"),
                "game_secs_left": r.get("game_seconds_remaining"),
                "drive_top": _mmss(r.get("drive_time_of_possession")), "drive_plays": r.get("drive_play_count"),
                "success": is_success(down, ytg, parsed["yards"])
                if parsed["play_type"] in ("pass", "run", "sack", "scramble") else None,
                **parsed,
            })
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# Players
# --------------------------------------------------------------------------

def _longest(plays: pd.DataFrame, id_col: str, mask) -> pd.Series:
    p = plays[mask & plays[id_col].notna() & ~plays["no_play"]]
    return p.groupby(["boxscore_id", id_col])["yards"].max()


def build_player_games(stats: pd.DataFrame, snaps: pd.DataFrame, rosters: pd.DataFrame,
                       plays: pd.DataFrame, games: pd.DataFrame) -> pd.DataFrame:
    box = dict(zip(games["nv_game_id"], games["boxscore_id"]))
    st = stats[stats["season_type"] == "REG"].copy()
    st = st[st["game_id"].map(box).notna()]
    out = pd.DataFrame({
        "player_id": st["player_id"], "player": st["player_display_name"],
        "team": st["team"].map(team), "boxscore_id": st["game_id"].map(box),
        "week": st["week"].astype(int),
        "pass_cmp": st["completions"], "pass_att": st["attempts"], "pass_yds": st["passing_yards"],
        "pass_td": st["passing_tds"], "pass_int": st["passing_interceptions"],
        "pass_sacked": st["sacks_suffered"], "pass_sacked_yds": st["sack_yards_lost"],
        "rush_att": st["carries"], "rush_yds": st["rushing_yards"], "rush_td": st["rushing_tds"],
        "targets": st["targets"], "rec": st["receptions"], "rec_yds": st["receiving_yards"],
        "rec_td": st["receiving_tds"],
        "fumbles": st[["sack_fumbles", "rushing_fumbles", "receiving_fumbles"]].sum(axis=1),
        "fumbles_lost": st[["sack_fumbles_lost", "rushing_fumbles_lost", "receiving_fumbles_lost"]].sum(axis=1),
        "_pos": st["position"],
    })
    is_rush = plays["play_type"].isin(["run", "scramble"])
    longs = {
        "pass_long": _longest(plays, "passer_id", plays["play_type"].eq("pass") & plays["complete"].eq(True)),
        "rush_long": _longest(plays, "rusher_id", is_rush),
        "rec_long": _longest(plays, "target_id", plays["play_type"].eq("pass") & plays["complete"].eq(True)),
    }
    key = pd.MultiIndex.from_arrays([out["boxscore_id"], out["player_id"]])
    for col, s in longs.items():
        out[col] = s.reindex(key).to_numpy()

    # Snap counts are keyed by PFR id; map to GSIS through the weekly rosters.
    pfr_to_gsis = (rosters.dropna(subset=["pfr_id", "gsis_id"])
                   .drop_duplicates("pfr_id").set_index("pfr_id")["gsis_id"])
    sn = snaps[snaps["game_type"] == "REG"].copy()
    sn["player_id"] = sn["pfr_player_id"].map(pfr_to_gsis)
    sn["team"] = sn["team"].map(team)
    sn["boxscore_id"] = sn["game_id"].map(box)
    # Fall back to name + team for players the roster file doesn't link.
    name_map = out.drop_duplicates(["player", "team"]).set_index(["player", "team"])["player_id"]
    miss = sn["player_id"].isna()
    sn.loc[miss, "player_id"] = pd.MultiIndex.from_arrays(
        [sn.loc[miss, "player"], sn.loc[miss, "team"]]).map(lambda k: name_map.get(k))
    sn = sn.dropna(subset=["player_id", "boxscore_id"])
    sn = sn.assign(off_pct=sn["offense_pct"] * 100).rename(
        columns={"offense_snaps": "off_snaps", "position": "pos"})
    sn = sn.drop_duplicates(["boxscore_id", "player_id"])

    m = out.merge(sn[["boxscore_id", "player_id", "pos", "off_snaps", "off_pct"]],
                  on=["boxscore_id", "player_id"], how="left")
    m["pos"] = m["pos"].fillna(m["_pos"])
    m = m.drop(columns="_pos")
    # Offensive players with snaps but no stats still matter for usage.
    seen = set(zip(m["boxscore_id"], m["player_id"]))
    new = np.array([k not in seen for k in zip(sn["boxscore_id"], sn["player_id"])], dtype=bool)
    extra = sn[(sn["off_snaps"] > 0).to_numpy() & new]
    extra = extra[["player_id", "player", "team", "boxscore_id", "week", "pos", "off_snaps", "off_pct"]]
    m = pd.concat([m, extra], ignore_index=True)
    # Keep offensive players only (the stats file also lists defenders and
    # special-teamers), like PFR's player_offense table.
    stat_cols = ["pass_att", "rush_att", "targets", "off_snaps"]
    m = m[m["player_id"].notna() & (m[stat_cols].fillna(0).sum(axis=1) > 0)]
    return m.fillna({c: 0 for c in m.columns if c not in ("player", "team", "pos", "player_id", "boxscore_id")}) \
            .fillna({"pos": ""})


def build_defenders(stats: pd.DataFrame, games: pd.DataFrame) -> pd.DataFrame:
    box = dict(zip(games["nv_game_id"], games["boxscore_id"]))
    st = stats[(stats["season_type"] == "REG") & stats["game_id"].map(box).notna()]
    # Defensive players only: offensive players credited with a tackle after
    # a turnover would otherwise get a second, defensive projection row.
    st = st[st["position_group"].isin(["DL", "LB", "DB"])]
    tackles = st[["def_tackles_solo", "def_tackles_with_assist", "def_tackle_assists"]].fillna(0).sum(axis=1)
    d = pd.DataFrame({"boxscore_id": st["game_id"].map(box), "week": st["week"].astype(int),
                      "player_id": st["player_id"], "player": st["player_display_name"],
                      "team": st["team"].map(team), "tackles": tackles,
                      "sacks": st["def_sacks"].fillna(0), "def_int": st["def_interceptions"].fillna(0)})
    return d[(d[["tackles", "sacks", "def_int"]].sum(axis=1) > 0)].reset_index(drop=True)


def build_kickers(stats: pd.DataFrame, games: pd.DataFrame) -> pd.DataFrame:
    box = dict(zip(games["nv_game_id"], games["boxscore_id"]))
    st = stats[(stats["season_type"] == "REG") & stats["game_id"].map(box).notna()]
    st = st[(st["fg_att"].fillna(0) + st["pat_att"].fillna(0)) > 0]
    return pd.DataFrame({
        "boxscore_id": st["game_id"].map(box), "week": st["week"].astype(int),
        "player_id": st["player_id"], "team": st["team"].map(team),
        "fg_att": st["fg_att"], "fg_made": st["fg_made"],
        "fg_50_made": st["fg_made_50_59"].fillna(0) + st["fg_made_60_"].fillna(0),
        "xp_att": st["pat_att"], "xp_made": st["pat_made"],
        "player": st["player_display_name"],
    }).reset_index(drop=True)


def build_season(season: int, cache_dir: Path, db_path: Path, log=print) -> dict[str, pd.DataFrame]:
    d = Downloader(cache_dir, log)
    files = season_files(season)
    paths = {k: d.path(u) for k, u in files.items()}
    paths["games"] = d.path(GAMES_URL)
    missing = [p.name for k, p in paths.items() if not p.exists() and k not in OPTIONAL]
    if missing:
        raise FileNotFoundError(f"missing {missing} in {cache_dir}; run `scrape` first.")
    pbp = pd.read_csv(paths["pbp"], low_memory=False)
    pbp = pbp[pbp["season_type"] == "REG"]
    games = parse_games(pd.read_csv(paths["games"], low_memory=False), season, set(pbp["game_id"]))
    # Game-day weather from the play-by-play (temperature °F, wind mph, roof)
    wx = pbp.drop_duplicates("game_id").set_index("game_id")
    for col in ("temp", "wind", "roof", "weather"):
        if col in wx:
            games[col] = games["nv_game_id"].map(wx[col])
    stats = pd.read_csv(paths["player_week"], low_memory=False)
    plays = build_plays(pbp, games, season)
    opt = {k: paths[k] for k in OPTIONAL if paths[k].exists()}
    if "ftn" in opt:
        plays = add_ftn(plays, pd.read_csv(opt["ftn"], low_memory=False))
    else:
        log("warning: no FTN charting file; blitz / play-action columns left empty")
    tables = {
        "games": games.drop(columns="nv_game_id"),
        "plays": plays,
        "def_snaps": def_snaps(pd.read_csv(paths["snaps"]), games),
        "player_games": build_player_games(stats, pd.read_csv(paths["snaps"]),
                                           pd.read_csv(paths["rosters"], low_memory=False), plays, games),
        "defenders": build_defenders(stats, games),
        "kickers": build_kickers(stats, games),
    }
    adv = pd.read_csv(opt["adv_def"]) if "adv_def" in opt else None
    tables["team_defense"] = team_defense(plays, adv)
    rosters = pd.read_csv(paths["rosters"], low_memory=False)
    if adv is not None:
        tables["coverage"] = coverage_table(adv, rosters)
    if "injuries" in opt:
        tables["injuries"] = injuries_table(pd.read_csv(opt["injuries"], low_memory=False))
    if "depth" in opt:
        depth = pd.read_csv(opt["depth"], low_memory=False)
        tables["depth_qb"] = by_week(depth, games, depth_qbs)
        tables["depth_db"] = by_week(depth, games, depth_dbs)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as con:
        for name in ("team_defense", "injuries", "depth_qb", "depth_db", "coverage", "def_snaps"):
            con.execute(f"drop table if exists {name}")
        for name, df in tables.items():
            df.to_sql(name, con, if_exists="replace", index=False)
    log(f"built {db_path}: {games['boxscore_id'].notna().sum()} games, {len(plays)} plays, "
        f"{len(tables['player_games'])} player-game rows")
    return tables


# --------------------------------------------------------------------------
# Charting, pressure, injuries, depth charts
# --------------------------------------------------------------------------

FTN_COLS = {"n_blitzers": "n_blitzers", "n_pass_rushers": "n_rushers", "n_defense_box": "box",
            "is_play_action": "play_action", "is_screen_pass": "screen", "is_rpo": "rpo",
            "is_motion": "motion"}


def add_ftn(plays: pd.DataFrame, ftn: pd.DataFrame) -> pd.DataFrame:
    """Join FTN charting onto plays by (nflverse game id, play id).
    ``is_blitz`` = 5+ rushers or any blitzer (NaN where FTN didn't chart the play)."""
    f = ftn.rename(columns={"nflverse_game_id": "nv_game_id", "nflverse_play_id": "play_id", **FTN_COLS})
    f = f[["nv_game_id", "play_id", *FTN_COLS.values()]].drop_duplicates(["nv_game_id", "play_id"])
    out = plays.drop(columns=[c for c in FTN_COLS.values() if c in plays], errors="ignore") \
               .merge(f, on=["nv_game_id", "play_id"], how="left")
    out["is_blitz"] = np.where(out["n_rushers"].isna(), np.nan,
                            ((out["n_blitzers"].fillna(0) > 0) | (out["n_rushers"] >= 5)).astype(float))
    return out


def team_defense(plays: pd.DataFrame, adv: pd.DataFrame | None) -> pd.DataFrame:
    """Season blitz rate (FTN, per charted dropback, overall and on 3rd/4th
    down) and pressures per dropback (PFR, summed over defenders, so a play
    with two pressuring defenders counts twice: an index, not a rate)."""
    drop = plays[plays["play_type"].isin(["pass", "sack", "scramble"]) & ~plays["no_play"]]
    rows = []
    for tm, g in drop.groupby("defense"):
        ch = g[g["is_blitz"].notna()] if "is_blitz" in g else g.iloc[0:0]
        third = ch[ch["down"].isin([3, 4])]
        rows.append({"team": tm, "dropbacks_faced": len(g),
                     "blitz_pct": 100 * ch["is_blitz"].mean() if len(ch) else np.nan,
                     "third_down_blitz_rate": 100 * third["is_blitz"].mean() if len(third) else np.nan,
                     "avg_rushers": ch["n_rushers"].mean() if len(ch) else np.nan})
    out = pd.DataFrame(rows)
    if adv is not None and not adv.empty:
        a = adv[adv["game_type"] == "REG"].assign(team=lambda d: d["team"].map(team))
        pr = a.groupby("team")[["def_pressures", "def_times_hurried", "def_times_hitqb"]].sum()
        out = out.merge(pr, left_on="team", right_index=True, how="left")
        out["pressure_per_db_pct"] = 100 * out["def_pressures"] / out["dropbacks_faced"]
    return out


def injuries_table(inj: pd.DataFrame) -> pd.DataFrame:
    i = inj[inj["game_type"] == "REG"]
    return pd.DataFrame({"week": i["week"], "team": i["team"].map(team), "player_id": i["gsis_id"],
                         "player": i["full_name"], "pos": i["position"],
                         "report_status": i["report_status"], "injury": i["report_primary_injury"],
                         "practice_status": i["practice_status"]})


def by_week(depth: pd.DataFrame, games: pd.DataFrame, fn) -> pd.DataFrame:
    """Depth chart as it stood before each week: for week W, the last
    snapshot taken before W's first game (``for_week`` column). Lets past
    weeks be replayed without using later information."""
    first = pd.to_datetime(games.groupby("week")["date"].min())
    snaps = pd.Series(sorted(depth["dt"].unique()))
    snap_t = pd.to_datetime(snaps).dt.tz_localize(None)
    out = []
    for wk, day in first.items():
        before = snaps[snap_t < day]
        if before.empty:
            continue
        frame = fn(depth[depth["dt"] == before.iloc[-1]])
        out.append(frame.assign(for_week=int(wk)))
    return pd.concat(out, ignore_index=True) if out else pd.DataFrame()


def def_snaps(snaps: pd.DataFrame, games: pd.DataFrame) -> pd.DataFrame:
    """Defensive snaps per player per game (who actually played)."""
    box = dict(zip(games["nv_game_id"], games["boxscore_id"]))
    s = snaps[(snaps["game_type"] == "REG") & (snaps["defense_snaps"] > 0)]
    return pd.DataFrame({"boxscore_id": s["game_id"].map(box), "week": s["week"], "team": s["team"].map(team),
                         "pfr_id": s["pfr_player_id"], "player": s["player"], "pos": s["position"],
                         "snaps": s["defense_snaps"], "pct": s["defense_pct"]})


def depth_qbs(depth: pd.DataFrame) -> pd.DataFrame:
    """One depth-chart snapshot, quarterbacks only, ranked."""
    last = depth[depth["dt"] == depth["dt"].max()]
    q = last[last["pos_abb"] == "QB"].sort_values(["team", "pos_rank"]).drop_duplicates(["team", "gsis_id"])
    return pd.DataFrame({"as_of": q["dt"], "team": q["team"].map(team), "player_id": q["gsis_id"],
                         "player": q["player_name"], "rank": q["pos_rank"]})


DB_SLOTS = {"LCB": "outside", "RCB": "outside", "CB": "outside", "NB": "slot",
            "SS": "safety", "FS": "safety"}


def depth_dbs(depth: pd.DataFrame) -> pd.DataFrame:
    """One depth-chart snapshot, defensive backs with their alignment
    (LCB / RCB outside, NB nickel = slot, SS / FS safeties)."""
    last = depth[(depth["dt"] == depth["dt"].max()) & depth["pos_abb"].isin(list(DB_SLOTS))]
    last = last.sort_values(["team", "pos_abb", "pos_rank"])
    return pd.DataFrame({"as_of": last["dt"], "team": last["team"].map(team), "player_id": last["gsis_id"],
                         "player": last["player_name"], "slot": last["pos_abb"],
                         "role": last["pos_abb"].map(DB_SLOTS), "rank": last["pos_rank"]})


def coverage_table(adv: pd.DataFrame, rosters: pd.DataFrame) -> pd.DataFrame:
    """PFR charting per defender per game: targets, completions, yards and
    TDs allowed in coverage. Keyed to GSIS ids through the weekly rosters."""
    a = adv[adv["game_type"] == "REG"]
    pfr_to_gsis = (rosters.dropna(subset=["pfr_id", "gsis_id"]).drop_duplicates("pfr_id")
                   .set_index("pfr_id")["gsis_id"])
    pos = rosters.dropna(subset=["pfr_id"]).drop_duplicates("pfr_id").set_index("pfr_id")["position"]
    return pd.DataFrame({"week": a["week"], "team": a["team"].map(team),
                         "player_id": a["pfr_player_id"].map(pfr_to_gsis), "pfr_id": a["pfr_player_id"],
                         "player": a["pfr_player_name"], "pos": a["pfr_player_id"].map(pos),
                         "targets": a["def_targets"].fillna(0), "completions": a["def_completions_allowed"].fillna(0),
                         "yards": a["def_yards_allowed"].fillna(0), "td": a["def_receiving_td_allowed"].fillna(0),
                         "ints": a["def_ints"].fillna(0)})


# --------------------------------------------------------------------------
# Coach history (replaces the PFR team-season pages)
# --------------------------------------------------------------------------

def history_files(years) -> list[str]:
    return [f"{RELEASES}/stats_player/stats_player_week_{y}.csv.gz" for y in years]


def download_history(years, cache_dir: Path, log=print) -> None:
    d = Downloader(cache_dir, log)
    d.get(GAMES_URL)
    for url in history_files(sorted(set(years))):
        d.get(url)


def team_seasons(year: int, cache_dir: Path) -> pd.DataFrame:
    """Per team for one regular season: pass/rush attempts, point
    differential per game, top / top-2 target share, RB1 carry share."""
    d = Downloader(cache_dir)
    p = d.path(f"{RELEASES}/stats_player/stats_player_week_{year}.csv.gz")
    if not p.exists():
        return pd.DataFrame()
    st = pd.read_csv(p, low_memory=False)
    st = st[st["season_type"] == "REG"].assign(team=lambda x: x["team"].map(team))
    agg = st.groupby("team")[["attempts", "sacks_suffered", "carries"]].sum()
    per = st.groupby(["team", "player_id"])[["targets", "carries"]].sum()

    def share(col, k):
        s = per[col].groupby(level=0).apply(lambda x: x.sort_values(ascending=False).iloc[:k].sum() / max(x.sum(), 1))
        return s

    g = pd.read_csv(d.path(GAMES_URL), low_memory=False)
    g = g[(g["season"] == year) & (g["game_type"] == "REG") & g["result"].notna()]
    pdiff = pd.concat([
        pd.DataFrame({"team": g["home_team"].map(team), "d": g["home_score"] - g["away_score"]}),
        pd.DataFrame({"team": g["away_team"].map(team), "d": g["away_score"] - g["home_score"]}),
    ]).groupby("team")["d"].mean()
    out = pd.DataFrame({
        # Dropbacks (attempts + sacks) vs carries, matching how PFR counts team pass plays
        "pass_att": agg["attempts"] + agg["sacks_suffered"], "rush_att": agg["carries"],
        "point_diff_pg": pdiff, "top_target_share": share("targets", 1),
        "top2_target_share": share("targets", 2), "rb1_carry_share": share("carries", 1),
    })
    out["pass_rate"] = out["pass_att"] / (out["pass_att"] + out["rush_att"])
    return out


def history_table(coaches: pd.DataFrame, cache_dir: Path) -> pd.DataFrame:
    """Same columns as ``coaches.history_table`` (PFR version)."""
    from .coaches import parse_history
    cache = {}
    rows = []
    for c in coaches.itertuples():
        for tm, year in parse_history(c.caller_history):
            if year not in cache:
                cache[year] = team_seasons(year, cache_dir)
            ts = cache[year]
            if ts.empty or tm not in ts.index:
                continue
            r = ts.loc[tm]
            rows.append({"team_now": c.team, "play_caller": c.play_caller, "team": tm, "season": year,
                         "pass_rate": r["pass_rate"], "league_pass_rate": ts["pass_rate"].mean(),
                         "point_diff_pg": r["point_diff_pg"],
                         "top_target_share": r["top_target_share"],
                         "top2_target_share": r["top2_target_share"],
                         "rb1_carry_share": r["rb1_carry_share"]})
    return pd.DataFrame(rows)
