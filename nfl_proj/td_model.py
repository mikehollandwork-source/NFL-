"""Stats-driven anytime-TD model (what the 2021-25 backtest found drives TDs):
season-to-date targets and carries per game, red-zone / inside-10 / inside-5
touches, end-zone targets, and the scoring environment from our own data
(team TDs per game + opponent TDs allowed per game; no market input).
Blended 50/50 in log-odds with the simulation's calibrated TD probability:
on 2025 out of sample that blend beat either alone (log-loss 0.5256 vs
0.528 simulation, 0.530 stats model).

Fit with `python tools/td_study.py --save` (writes data/models/td_stats.json).
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "data" / "models" / "td_stats.json"
RAW = ROOT / "data" / "raw" / "nflverse"
COLS = ["season", "week", "game_id", "posteam", "defteam", "yardline_100", "play_type", "pass_attempt",
        "rush_attempt", "receiver_player_id", "receiver_player_name", "rusher_player_id", "air_yards",
        "pass_touchdown", "rush_touchdown", "td_player_id", "two_point_attempt", "season_type",
        "complete_pass", "qb_kneel"]


def player_games(season):
    p = pd.read_csv(RAW / f"play_by_play_{season}.csv.gz", usecols=lambda c: c in COLS, low_memory=False)
    p = p[(p["season_type"] == "REG") & (p["two_point_attempt"] != 1)]
    p = p[p["play_type"].isin(["pass", "run"]) & (p.get("qb_kneel", 0) != 1)]
    rec = p[p["pass_attempt"] == 1].dropna(subset=["receiver_player_id"]).copy()
    rec["pid"] = rec["receiver_player_id"]
    rec["tgt"] = 1
    rec["rz_tgt"] = (rec["yardline_100"] <= 20).astype(int)
    rec["i10_tgt"] = (rec["yardline_100"] <= 10).astype(int)
    rec["ez_tgt"] = (rec["air_yards"] >= rec["yardline_100"]).astype(int)
    rec["ez_inc"] = ((rec["ez_tgt"] == 1) & (rec["complete_pass"] != 1)).astype(int)
    rec["deep_tgt"] = (rec["air_yards"] >= 20).astype(int)
    rec["ay"] = rec["air_yards"].fillna(0)
    rec["td"] = ((rec["pass_touchdown"] == 1) & (rec["td_player_id"] == rec["pid"])).astype(int)
    ru = p[p["rush_attempt"] == 1].dropna(subset=["rusher_player_id"]).copy()
    ru["pid"] = ru["rusher_player_id"]
    ru["car"] = 1
    ru["rz_car"] = (ru["yardline_100"] <= 20).astype(int)
    ru["i5_car"] = (ru["yardline_100"] <= 5).astype(int)
    ru["td"] = ((ru["rush_touchdown"] == 1) & (ru["td_player_id"] == ru["pid"])).astype(int)
    keys = ["season", "week", "game_id", "posteam", "defteam", "pid"]
    a = rec.groupby(keys)[["tgt", "rz_tgt", "i10_tgt", "ez_tgt", "ez_inc", "deep_tgt", "ay", "td"]].sum()
    b = ru.groupby(keys)[["car", "rz_car", "i5_car", "td"]].sum().rename(columns={"td": "rtd"})
    g = a.join(b, how="outer").fillna(0).reset_index()
    g["tds"] = g["td"] + g["rtd"]
    team = g.groupby(["season", "week", "posteam"])[["tgt", "rz_tgt", "i10_tgt", "ez_tgt", "car", "rz_car", "i5_car", "tds"]].sum()
    team.columns = ["T_" + c for c in team.columns]
    g = g.merge(team, left_on=["season", "week", "posteam"], right_index=True)
    # defense: TDs allowed per game so far (non-market scoring environment)
    d = g.groupby(["season", "week", "defteam"])["tds"].sum().rename("D_tds").reset_index().sort_values(["defteam", "season", "week"])
    d["m_D_tds"] = d.groupby(["defteam", "season"])["D_tds"].transform(lambda s: s.shift().expanding().mean())
    g = g.merge(d[["season", "week", "defteam", "m_D_tds"]], on=["season", "week", "defteam"], how="left")
    return g


def trailing(g):
    """Season-to-date per-game means before this week (player and team)."""
    g = g.sort_values(["pid", "season", "week"]).copy()
    use = ["tgt", "rz_tgt", "i10_tgt", "ez_tgt", "ez_inc", "deep_tgt", "ay", "car", "rz_car", "i5_car", "tds",
           "T_tgt", "T_rz_tgt", "T_i10_tgt", "T_ez_tgt", "T_car", "T_rz_car", "T_i5_car", "T_tds"]
    grp = g.groupby(["pid", "season"])
    for c in use:
        g["m_" + c] = grp[c].transform(lambda s: s.shift().expanding().mean())
    g["n_prev"] = grp.cumcount()
    # last-week end-zone incompletions ("near misses")
    g["ez_inc_last"] = grp["ez_inc"].shift().fillna(0)
    return g


def games_table():
    gm = pd.read_csv(RAW / "games.csv")
    gm = gm[gm["game_type"] == "REG"]
    rows = []
    for x in gm.itertuples():
        if pd.isna(x.total_line) or pd.isna(x.spread_line):
            continue
        # nflverse spread_line: home favored by spread_line
        rows.append((x.game_id, x.home_team, x.total_line / 2 + x.spread_line / 2))
        rows.append((x.game_id, x.away_team, x.total_line / 2 - x.spread_line / 2))
    return pd.DataFrame(rows, columns=["game_id", "posteam", "implied"])


def fit_logit(X, y, l2=1e-3):
    X = np.c_[np.ones(len(X)), X]
    b = np.zeros(X.shape[1])
    for _ in range(100):
        p = 1 / (1 + np.exp(-X @ b))
        g = X.T @ (y - p) - l2 * np.r_[0, b[1:]]
        H = (X * (p * (1 - p))[:, None]).T @ X + l2 * np.eye(len(b))
        b = b + np.linalg.solve(H, g)
    return b


def pred(b, X):
    return 1 / (1 + np.exp(-np.c_[np.ones(len(X)), X] @ b))


def ll(y, p):
    p = np.clip(p, 1e-6, 1 - 1e-6)
    return -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))


def rows(seasons=range(2021, 2026)):
    g = pd.concat([trailing(player_games(s)) for s in seasons], ignore_index=True)
    g = g.merge(games_table(), on=["game_id", "posteam"], how="left")
    g = g[(g["n_prev"] >= 3) & ((g["m_tgt"] + g["m_car"]) >= 2) & g["implied"].notna() & g["m_D_tds"].notna()].copy()
    g["env"] = g["m_T_tds"] + g["m_D_tds"]   # team TDs/game + opponent TDs allowed/game, from our data only
    g["log_env"] = np.log(g["env"].clip(0.5))
    g["y"] = (g["tds"] > 0).astype(float)
    return g


FEATS = ["m_tgt", "m_car", "m_rz_tgt", "m_rz_car", "m_i10_tgt", "m_i5_car", "m_ez_tgt", "log_env"]




def current_features(season: int, week: int, schedule: pd.DataFrame) -> pd.DataFrame:
    """Season-to-date per-game features for every player, as of before ``week``."""
    from .nflverse import NV_TO_PFR
    g = player_games(season)
    g = g[g["week"] < week].copy()
    if g.empty:
        return pd.DataFrame()
    g["posteam"] = g["posteam"].replace(NV_TO_PFR)   # schedule uses PFR codes (SFO, KAN, ...)
    g["defteam"] = g["defteam"].replace(NV_TO_PFR)
    use = ["tgt", "rz_tgt", "i10_tgt", "ez_tgt", "car", "rz_car", "i5_car"]
    last_team = g.sort_values("week").groupby("pid")["posteam"].last()
    p = g.groupby("pid")[use].mean().add_prefix("m_")
    p["n_prev"] = g.groupby("pid").size()
    p["posteam"] = last_team
    tm = g.groupby(["week", "posteam"])["tds"].sum().groupby("posteam").mean().rename("m_T_tds")
    dd = g.groupby(["week", "defteam"])["tds"].sum().groupby("defteam").mean().rename("m_D_tds")
    sch = schedule[schedule["week"] == week]
    opp = {**dict(zip(sch["home"], sch["away"])), **dict(zip(sch["away"], sch["home"]))}
    p["opp"] = p["posteam"].map(opp)
    p = p.dropna(subset=["opp"])
    p["env"] = p["posteam"].map(tm) + p["opp"].map(dd)
    p["log_env"] = np.log(p["env"].clip(0.5))
    return p.reset_index()


def predict(feat: pd.DataFrame) -> pd.Series:
    if not MODEL.exists() or feat.empty:
        return pd.Series(dtype=float)
    m = json.loads(MODEL.read_text())
    f = m["features"]
    x = ((feat[f] - pd.Series(m["mu"])) / pd.Series(m["sd"])).values
    p = 1 / (1 + np.exp(-(np.c_[np.ones(len(x)), x] @ np.array(m["b"]))))
    return pd.Series(p, index=feat["pid"].values)


def blend(p_sim, p_stats, w_sim: float = 0.5):
    lg = lambda p: np.log(np.clip(p, 1e-4, 1 - 1e-4) / (1 - np.clip(p, 1e-4, 1 - 1e-4)))
    return 1 / (1 + np.exp(-(w_sim * lg(np.asarray(p_sim, float)) + (1 - w_sim) * lg(np.asarray(p_stats, float)))))
