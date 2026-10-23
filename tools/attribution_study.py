"""Where projections miss, from the as-of backtests (2025 weeks 4-18, 2026 weeks 3+).

Every player projection's miss is split into team volume / player share /
efficiency / did-not-play (nfl_proj.attribution). Then: which part drives each
stat's misses, how much of the team-volume miss is the game going off script
(unforecastable), and which groups of players carry a bias that shows up in
BOTH seasons (candidates for a backtested fix; nothing here changes the model).

Usage: python tools/attribution_study.py [TAG25] [TAG26]   (default AT25 AT26)
"""
import sqlite3
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from nfl_proj.attribution import attribute, biases, error_mix, segments  # noqa: E402


def load(season, tag):
    proj = pd.read_csv(ROOT / f"output/{season}/backtest_{tag}_proj.csv", low_memory=False)
    tot = pd.read_csv(ROOT / f"output/{season}/backtest_{tag}_totals.csv")
    con = sqlite3.connect(ROOT / f"data/nfl_{season}.db")
    pg = pd.read_sql("select * from player_games", con)
    games = pd.read_sql("select * from games", con)
    pg = pg[pg["week"].isin(set(proj["week"]))]
    d = segments(attribute(proj, pg), games, tot)
    d["season"] = season
    # team-level: volume miss vs how far the final margin was from the projected one
    g = games[games["home_score"].notna()]
    res = pd.concat([pd.DataFrame({"week": g["week"], "team": g["home"], "pts": g["home_score"], "opp_pts": g["away_score"]}),
                     pd.DataFrame({"week": g["week"], "team": g["away"], "pts": g["away_score"], "opp_pts": g["home_score"]})])
    act = pg.groupby(["week", "team"])[["pass_att", "rush_att"]].sum().reset_index()
    t = tot.merge(res, on=["week", "team"]).merge(act, on=["week", "team"])
    t = t.merge(tot[["week", "team", "model_points"]].rename(columns={"team": "opp", "model_points": "opp_model"}), on=["week", "opp"])
    t["script_miss"] = (t["pts"] - t["opp_pts"]) - (t["model_points"] - t["opp_model"])
    t["season"] = season
    return d, t


def main(tag25="AT25", tag26="AT26"):
    d25, t25 = load(2025, tag25)
    d26, t26 = load(2026, tag26)
    d = pd.concat([d25, d26], ignore_index=True)
    T = pd.concat([t25, t26], ignore_index=True)
    pd.set_option("display.width", 220)
    L = ["# Why projections miss (as-of backtests: 2025 weeks 4-18, 2026 weeks 3+)", "",
         f"{len(d):,} player-stat projections. Each miss = team volume + player share + efficiency + did-not-play "
         f"(parts add up exactly; largest leftover {d['resid'].abs().max():.2g}).", ""]

    mix = error_mix(d)
    L += ["## 1. What drives each stat's misses", "",
          "Share of the miss from each part (average size of each part / their sum), average miss and bias (actual - projected).", "",
          "| stat | n | avg miss | bias | team volume | player share | efficiency | didn't play |", "|---|---|---|---|---|---|---|---|"]
    for r in mix.itertuples():
        L.append(f"| {r.stat} | {r.n} | {r.mae:.1f} | {r.bias:+.2f} | {r.team:.0%} | {r.share:.0%} | {r.eff:.0%} | {r.dnp:.0%} |")
    L.append("")

    # Game script: how much of the team-volume miss is the final margin differing from the projection
    L += ["## 2. Team volume misses vs the game going off script", "",
          "Team pass attempts / carries minus projected, against (final margin - projected margin). "
          "The slope is volume per point of surprise; R² is the share of the volume miss that the score explains "
          "(not knowable before kickoff).", "", "| | slope per point | R² | bias (actual - proj) | n |", "|---|---|---|---|---|"]
    for col, pc in (("pass_att", "proj_pass_att"), ("rush_att", "proj_runs")):
        if pc not in T:
            continue
        e = T[col] - T[pc]
        x = T["script_miss"]
        b = np.polyfit(x, e, 1)
        r2 = np.corrcoef(x, e)[0, 1] ** 2
        L.append(f"| {col.replace('_att', ' attempts').replace('rush', 'carries (team)')} | {b[0]:+.2f} | {r2:.0%} | {e.mean():+.2f} | {len(T)} |")
    L.append("")

    # Steady biases: pooled |t| >= 3, same sign in both seasons, at least 5% of the projection
    groups = [["pos"], ["role"], ["game_total"], ["script"], ["venue"], ["season_part"],
              ["pos", "role"], ["pos", "game_total"], ["pos", "script"], ["pos", "venue"]]
    cand = []
    for by in groups:
        b = biases(d, by, split="season")
        if b.empty:
            continue
        b["group"] = " / ".join(by)
        cand.append(b)
    B = pd.concat(cand, ignore_index=True)
    both = B[["bias_2025", "bias_2026"]].notna().all(axis=1)
    steady = B[both & (B["t"].abs() >= 3) & (np.sign(B["bias_2025"]) == np.sign(B["bias_2026"]))
               & (B["bias_pct"].abs() >= 0.05)].copy()
    steady["main_part"] = steady[["team", "share", "eff", "dnp"]].abs().idxmax(axis=1)
    steady = steady.sort_values("t", key=abs, ascending=False)
    L += ["## 3. Steady biases (same direction in 2025 and 2026, |t| >= 3, at least 5% of the projection)", "",
          "Each is a candidate for a fix that must still pass the out-of-sample backtest. Main part = the component "
          "carrying most of the bias.", "",
          "| stat | group | n | projected | bias | bias % | 2025 | 2026 | t | main part | team | share | eff | dnp |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in steady.head(30).itertuples():
        grp = " / ".join(str(getattr(r, c)) for c in ["pos", "role", "game_total", "script", "venue", "season_part"]
                         if c in steady.columns and isinstance(getattr(r, c), str))
        L.append(f"| {r.stat} | {grp} | {r.n} | {r.proj:.1f} | {r.bias:+.2f} | {r.bias_pct:+.0%} | {r.bias_2025:+.2f} | "
                 f"{r.bias_2026:+.2f} | {r.t:+.1f} | {r.main_part} | {r.team:+.2f} | {r.share:+.2f} | {r.eff:+.2f} | {r.dnp:+.2f} |")
    if steady.empty:
        L.append("| none | | | | | | | | | | | | | |")
    L.append("")
    out = ROOT / "output/2026/attribution.md"
    out.write_text("\n".join(L))
    d.to_csv(ROOT / "output/2026/attribution_rows.csv.gz", index=False)
    print("\n".join(L))


if __name__ == "__main__":
    main(*sys.argv[1:3])
