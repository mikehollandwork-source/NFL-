"""Team-specific touchdown patterns: does the model miss some teams' scorers
in a way that repeats? Uses the live blended TD chance (simulation + stats
model) for RB/WR/TE with 3+ touches a game, 2025 weeks 4-18 and 2026 weeks 3+.

Repeatability test: a team's miss (actual TDs - expected) in one half of the
games vs the other half (odd vs even weeks). Real team effects correlate
across halves; noise doesn't."""
import sqlite3
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
import td_tells as T                                                        # noqa: E402
from nfl_proj.td_model import blend, current_features, predict              # noqa: E402


def load():
    out = []
    for yr, tag in ((2025, "AT25"), (2026, "AT26")):
        d = T.sample(yr, tag)
        g = pd.read_sql("select * from games", sqlite3.connect(ROOT / f"data/nfl_{yr}.db"))
        ps = {}
        for w in sorted(d.week.unique()):
            for pid, v in predict(current_features(yr, int(w), g)).items():
                ps[(w, pid)] = v
        d["p_stats"] = [ps.get((w, p), np.nan) for w, p in zip(d.week, d.player_id)]
        d["p"] = np.where(d.p_stats.notna(), blend(d.anytime_td, d.p_stats.fillna(.5)), d.anytime_td)
        d["season"] = yr
        out.append(d)
    d = pd.concat(out, ignore_index=True)
    d["resid"] = d.scored - d.p
    d["half"] = np.where(d.week % 2 == 0, "even", "odd")
    return d


def persistence(d, key):
    """Correlation of a group's average miss in odd vs even weeks, each season."""
    rows = []
    for yr, x in d.groupby("season"):
        m = x.groupby([key, "half"]).resid.mean().unstack()
        n = x.groupby([key, "half"]).size().unstack()
        m = m[(n.min(axis=1) >= 15)]
        if len(m) > 5:
            rows.append((yr, len(m), np.corrcoef(m["odd"], m["even"])[0, 1]))
    return rows


def main():
    d = load()
    L = ["# Team-specific touchdown patterns", "",
         f"{len(d):,} RB/WR/TE games (3+ touches a game so far), live blended TD chance. "
         "Miss = scored (1/0) minus the model's chance; summed per team = TDs above or below expected.", ""]
    # 1. Team miss: does it repeat between odd and even weeks?
    L += ["## 1. Does a team's miss repeat? (odd weeks vs even weeks)", "",
          "| season | teams | correlation |", "|---|---|---|"]
    for yr, n, r in persistence(d, "team"):
        L.append(f"| {yr} | {n} | {r:+.2f} |")
    t25 = d[d.season == 2025].groupby("team").resid.mean()
    t26 = d[d.season == 2026].groupby("team").resid.mean()
    j = pd.concat([t25, t26], axis=1, keys=["y25", "y26"]).dropna()
    L += [f"| 2025 -> 2026 | {len(j)} | {np.corrcoef(j.y25, j.y26)[0, 1]:+.2f} |", "",
          "Noise check: with this many games per team, the luck alone in a team's miss is about "
          f"±{d.groupby(['season', 'team']).resid.apply(lambda v: v.std() / np.sqrt(len(v))).mean():.3f} per player-game.", ""]
    # 2. Position share per team: actual vs expected, persistence
    d["pos_grp"] = d.pos
    L += ["## 2. Which position scores the team's TDs: does the model's miss by team x position repeat?", "",
          "| season | team-positions | correlation odd vs even |", "|---|---|---|"]
    d["team_pos"] = d.team + " " + d.pos
    for yr, n, r in persistence(d, "team_pos"):
        L.append(f"| {yr} | {n} | {r:+.2f} |")
    L.append("")
    # 3. Current-season table (2026): TDs vs expected by team and position
    x = d[d.season == 2026]
    tab = x.groupby(["team", "pos"]).agg(games=("scored", "size"), tds=("scored", "sum"), exp=("p", "sum"))
    tab["diff"] = tab.tds - tab.exp
    piv = tab["diff"].unstack().round(1)
    tot = x.groupby("team").agg(tds=("scored", "sum"), exp=("p", "sum"), games=("scored", "size"))
    tot["diff"] = (tot.tds - tot.exp).round(1)
    tot = tot.join(piv).sort_values("diff")
    L += ["## 3. 2026 so far (weeks 3+): players who scored minus expected, by team and position", "",
          "Positive = that team's players scored more than the model expected. Single-season numbers like these are "
          "mostly luck unless section 1 / 2 show the pattern repeats.", "",
          "| team | player-games | scored | expected | diff | RB | WR | TE |", "|---|---|---|---|---|---|---|---|"]
    for t, r in tot.iterrows():
        L.append(f"| {t} | {int(r.games)} | {int(r.tds)} | {r.exp:.1f} | {r['diff']:+.1f} | "
                 + " | ".join(f"{r.get(p, np.nan):+.1f}" if pd.notna(r.get(p, np.nan)) else "" for p in ("RB", "WR", "TE")) + " |")
    # 4. Team goal-line concentration: does the lead goal-line back's share of inside-10 carries predict better?
    out = ROOT / "output/2026/td_teams.md"
    out.write_text("\n".join(L))
    print("\n".join(L))
    d.to_csv(ROOT / "output/2026/td_teams_rows.csv.gz", index=False)


if __name__ == "__main__":
    main()
