"""What predicts a skill player scoring a TD? Out-of-sample study on nflverse
play-by-play: trailing same-season usage features -> logistic regression,
trained on earlier seasons, scored on later ones (log-loss vs base)."""
import sys
from pathlib import Path
import numpy as np, pandas as pd

RAW = Path(__file__).resolve().parents[1] / "data" / "raw" / "nflverse"
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


def main(seasons=range(2021, 2026)):
    g = pd.concat([trailing(player_games(s)) for s in seasons], ignore_index=True)
    g = g.merge(games_table(), on=["game_id", "posteam"], how="left")
    g = g[(g["n_prev"] >= 3) & ((g["m_tgt"] + g["m_car"]) >= 2) & g["implied"].notna()].copy()
    g["y"] = (g["tds"] > 0).astype(float)
    eps = 1e-9
    g["sh_tgt"] = g["m_tgt"] / (g["m_T_tgt"] + eps)
    g["sh_car"] = g["m_car"] / (g["m_T_car"] + eps)
    g["sh_rz"] = (g["m_rz_tgt"] + g["m_rz_car"]) / (g["m_T_rz_tgt"] + g["m_T_rz_car"] + eps)
    g["sh_i10"] = (g["m_i10_tgt"] + g["m_i5_car"]) / (g["m_T_i10_tgt"] + g["m_T_i5_car"] + eps)
    g["sh_ez"] = g["m_ez_tgt"] / (g["m_T_ez_tgt"] + eps)
    g["sh_deep"] = g["m_deep_tgt"] / (g["m_tgt"] + eps)
    g["log_impl"] = np.log(g["implied"].clip(3))
    sets = {
        "volume (targets, carries per game)": ["m_tgt", "m_car"],
        "+ red-zone touches/game": ["m_tgt", "m_car", "m_rz_tgt", "m_rz_car"],
        "+ inside-10 / inside-5": ["m_tgt", "m_car", "m_rz_tgt", "m_rz_car", "m_i10_tgt", "m_i5_car"],
        "+ end-zone targets": ["m_tgt", "m_car", "m_rz_tgt", "m_rz_car", "m_i10_tgt", "m_i5_car", "m_ez_tgt"],
        "+ team implied points": ["m_tgt", "m_car", "m_rz_tgt", "m_rz_car", "m_i10_tgt", "m_i5_car", "m_ez_tgt", "log_impl"],
        "+ TD rate so far": ["m_tgt", "m_car", "m_rz_tgt", "m_rz_car", "m_i10_tgt", "m_i5_car", "m_ez_tgt", "log_impl", "m_tds"],
        "+ last-week end-zone incompletions": ["m_tgt", "m_car", "m_rz_tgt", "m_rz_car", "m_i10_tgt", "m_i5_car", "m_ez_tgt", "log_impl", "ez_inc_last"],
        "+ deep share, air yards": ["m_tgt", "m_car", "m_rz_tgt", "m_rz_car", "m_i10_tgt", "m_i5_car", "m_ez_tgt", "log_impl", "sh_deep", "m_ay"],
        "shares instead of counts": ["sh_tgt", "sh_car", "sh_rz", "sh_i10", "sh_ez", "log_impl", "m_T_tds"],
    }
    out = []
    for test in sorted(g["season"].unique())[2:]:
        tr, te = g[g["season"] < test], g[g["season"] == test]
        base = ll(te["y"].values, np.full(len(te), tr["y"].mean()))
        for name, f in sets.items():
            mu, sd = tr[f].mean(), tr[f].std() + 1e-9
            b = fit_logit(((tr[f] - mu) / sd).values, tr["y"].values)
            p = pred(b, ((te[f] - mu) / sd).values)
            out.append({"test": test, "set": name, "logloss": ll(te["y"].values, p), "base": base, "n": len(te)})
    r = pd.DataFrame(out)
    piv = r.pivot(index="set", columns="test", values="logloss")
    piv["mean"] = piv.mean(axis=1)
    piv = piv.loc[list(sets)]
    print(f"rows {len(g)}, scored-rate {g['y'].mean():.3f}")
    print(piv.round(4).to_string())
    # final model on all but last season: coefficient view
    f = sets["+ team implied points"]
    mu, sd = g[f].mean(), g[f].std()
    b = fit_logit(((g[f] - mu) / sd).values, g["y"].values)
    print("standardized coefficients:", dict(zip(f, np.round(b[1:], 3))))
    pass
    return g, r


if __name__ == "__main__":
    main()
