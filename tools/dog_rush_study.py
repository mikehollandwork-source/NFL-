"""Underdog wins and rushing: is anything knowable before kickoff repeatable?

Underdog / cover labels come from the closing spread (grading only). Every
candidate signal is built from rushing data of PRIOR weeks of the same season
(nflverse play-by-play 2021-26, weeks 4+). Signals are chosen on 2021-23 and
checked on 2024-26.
"""
import sys
import numpy as np
import pandas as pd

RAW = "data/raw/nflverse"
COLS = ["game_id", "season_type", "week", "posteam", "defteam", "qtr", "down", "score_differential",
        "epa", "success", "rush_attempt", "qb_scramble", "qb_dropback", "two_point_attempt",
        "rusher_player_id", "yards_gained"]


def team_games(season):
    p = pd.read_csv(f"{RAW}/play_by_play_{season}.csv.gz", usecols=COLS, low_memory=False)
    p = p[(p.season_type == "REG") & p.posteam.notna() & (p.two_point_attempt != 1)]
    run = (p.rush_attempt == 1) & (p.qb_scramble != 1)
    p["run"] = run.astype(int)
    p["play"] = (run | (p.qb_dropback == 1)).astype(int)
    neu = (p.qtr <= 3) & (p.score_differential.abs() <= 7) & p.down.isin([1, 2]) & (p.play == 1)
    p["neu_play"] = neu.astype(int)
    p["neu_run"] = (neu & run).astype(int)
    r = p[run]
    off = p.groupby(["game_id", "week", "posteam"]).agg(runs=("run", "sum"), plays=("play", "sum"),
                                                         neu_play=("neu_play", "sum"), neu_run=("neu_run", "sum"))
    ro = r.groupby(["game_id", "week", "posteam"]).agg(r_epa=("epa", "sum"), r_succ=("success", "sum"),
                                                        r_yds=("yards_gained", "sum"))
    top = (r.groupby(["game_id", "week", "posteam", "rusher_player_id"]).size()
            .groupby(level=[0, 1, 2]).max().rename("rb1"))
    o = off.join(ro).join(top).fillna(0).reset_index().rename(columns={"posteam": "team"})
    d = r.groupby(["game_id", "defteam"]).agg(d_runs=("run", "sum"), d_epa=("epa", "sum"),
                                              d_succ=("success", "sum"), d_yds=("yards_gained", "sum"))
    d = d.reset_index().rename(columns={"defteam": "team"})
    o = o.merge(d, on=["game_id", "team"], how="left")
    o["season"] = season
    return o


def pregame(tg):
    """Season-to-date and last-3 rates for each team before each week."""
    out = []
    sums = ["runs", "plays", "neu_play", "neu_run", "r_epa", "r_succ", "r_yds", "rb1", "d_runs", "d_epa", "d_succ", "d_yds"]
    for (s, t), g in tg.sort_values("week").groupby(["season", "team"]):
        c = g[sums].cumsum().shift(1)
        l3 = g[sums].rolling(3, min_periods=3).sum().shift(1)
        n = np.arange(len(g))
        f = pd.DataFrame({"season": s, "team": t, "week": g.week.values, "gp": n})
        f["ypc"] = (c.r_yds / c.runs).values
        f["r_epa"] = (c.r_epa / c.runs).values
        f["r_succ"] = (c.r_succ / c.runs).values
        f["neu_rr"] = (c.neu_run / c.neu_play).values
        f["neu_rr_l3"] = (l3.neu_run / l3.neu_play).values
        f["runs_pg"] = (c.runs / n).values
        f["runs_l3"] = (l3.runs / 3).values
        f["rb1_share"] = (c.rb1 / c.runs).values
        f["rb1_l3"] = (l3.rb1 / 3).values
        f["rb1_pg"] = (c.rb1 / n).values
        f["d_epa"] = (c.d_epa / c.d_runs).values
        f["d_ypc"] = (c.d_yds / c.d_runs).values
        f["d_epa_l3"] = (l3.d_epa / l3.d_runs).values
        f["r_epa_l3"] = (l3.r_epa / l3.runs).values
        out.append(f)
    f = pd.concat(out)
    f["rr_trend"] = f.neu_rr_l3 - f.neu_rr          # running more lately (neutral situations)
    f["runs_trend"] = f.runs_l3 - f.runs_pg
    f["rb1_trend"] = f.rb1_l3 - f.rb1_pg           # lead back's carries rising
    f["r_epa_trend"] = f.r_epa_l3 - f.r_epa
    f["d_epa_trend"] = f.d_epa_l3 - f.d_epa         # run defense getting worse (+)
    return f


def main():
    seasons = range(2021, 2027)
    tg = pd.concat(team_games(s) for s in seasons)
    pre = pregame(tg)
    g = pd.read_csv(f"{RAW}/games.csv")
    g = g[g.season.isin(seasons) & (g.game_type == "REG") & g.result.notna() & g.spread_line.notna()
          & (g.spread_line != 0) & (g.week >= 4)]
    home_fav = g.spread_line > 0
    gm = pd.DataFrame({"game_id": g.game_id, "season": g.season, "week": g.week,
                       "dog": np.where(home_fav, g.away_team, g.home_team),
                       "fav": np.where(home_fav, g.home_team, g.away_team),
                       "spread": g.spread_line.abs(),
                       "dog_margin": np.where(home_fav, -g.result, g.result)})
    gm = gm[gm.dog_margin != 0]
    gm["dog_win"] = (gm.dog_margin > 0).astype(int)
    ats = gm.dog_margin + gm.spread
    gm = gm[ats != 0]
    gm["dog_cover"] = (ats[ats != 0] > 0).astype(int)
    k = ["season", "week", "team"]
    feats = [c for c in pre.columns if c not in k + ["gp"]]
    gm = gm.merge(pre.rename(columns={c: "dog_" + c for c in feats + ["team"]}).rename(columns={"dog_team": "dog"}),
                  on=["season", "week", "dog"])
    gm = gm.merge(pre.rename(columns={c: "fav_" + c for c in feats}).rename(columns={"team": "fav", "gp": "fgp"}),
                  on=["season", "week", "fav"])
    # Matchups: dog's rushing vs fav's run defense, and the reverse
    gm["dog_rush_edge"] = gm.dog_r_epa + gm.fav_d_epa
    gm["fav_rush_edge"] = gm.fav_r_epa + gm.dog_d_epa
    gm["rush_matchup"] = gm.dog_rush_edge - gm.fav_rush_edge
    gm["ypc_matchup"] = (gm.dog_ypc + gm.fav_d_ypc) - (gm.fav_ypc + gm.dog_d_ypc)
    gm["rr_diff"] = gm.dog_neu_rr - gm.fav_neu_rr
    gm = gm.dropna()
    gm["half"] = np.where(gm.season <= 2023, "2021-23", "2024-26")

    # What dog wins looked like (after the game; descriptive only)
    act = tg[["game_id", "team", "runs", "r_yds", "rb1"]]
    a = gm.merge(act.rename(columns={"team": "dog", "runs": "dog_runs_act", "r_yds": "dog_ryds_act", "rb1": "dog_rb1_act"}),
                 on=["game_id", "dog"]).merge(act.rename(columns={"team": "fav", "runs": "fav_runs_act", "r_yds": "fav_ryds_act", "rb1": "fav_rb1_act"}),
                                              on=["game_id", "fav"])
    a["dog_rb1_vs_usual"] = a.dog_rb1_act - a.dog_rb1_pg
    a["dog_runs_vs_usual"] = a.dog_runs_act - a.dog_runs_pg
    print(f"{len(gm)} games (weeks 4+), underdogs won {gm.dog_win.mean():.1%}, covered {gm.dog_cover.mean():.1%}\n")
    print("AFTER the game (not usable pregame): underdog wins vs losses")
    print(a.groupby("dog_win")[["dog_runs_act", "fav_runs_act", "dog_runs_vs_usual", "dog_rb1_vs_usual", "dog_ryds_act", "fav_ryds_act"]].mean().round(1).to_string(), "\n")

    sig = ["rush_matchup", "ypc_matchup", "dog_rush_edge", "fav_rush_edge", "rr_diff", "dog_neu_rr", "dog_rr_trend",
           "dog_runs_trend", "dog_rb1_trend", "dog_rb1_share", "dog_r_epa_trend", "fav_d_epa_trend", "fav_rr_trend",
           "fav_rb1_trend", "dog_r_succ", "fav_d_epa", "dog_d_epa"]
    rows = []
    for s in sig:
        r = {"signal": s}
        for h, x in gm.groupby("half"):
            q_hi = x[s] >= x[s].quantile(0.8)
            q_lo = x[s] <= x[s].quantile(0.2)
            r[f"{h} top20 cover"] = x[q_hi].dog_cover.mean()
            r[f"{h} bot20 cover"] = x[q_lo].dog_cover.mean()
            r[f"{h} top20 win"] = x[q_hi].dog_win.mean()
            r[f"{h} corr"] = np.corrcoef(x[s], x.dog_margin + x.spread)[0, 1]
        rows.append(r)
    res = pd.DataFrame(rows).set_index("signal")
    pd.set_option("display.width", 250)
    print("Pregame signals, underdog's margin vs the spread (corr) and cover rates in top / bottom 20%:")
    print(res.round(3).to_string())
    n = gm.groupby("half").size().to_dict()
    print("\ngames per half:", n, "| one-sd noise on corr ~", {h: round(1 / np.sqrt(v), 3) for h, v in n.items()},
          "| on a 20% bucket cover rate ~", {h: round(np.sqrt(.25 / (v * .2)), 3) for h, v in n.items()})
    gm.to_csv("output/2026/dog_rush_study.csv", index=False)


if __name__ == "__main__":
    main()
