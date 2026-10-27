"""Do missing defensive starters hurt a defense, beyond its season-to-date
level? 2021-25. A starter = averaged 60%+ of defensive snaps over his
previous 3 games (2+ games). He is "missing" when he played in one of his
team's previous 2 games but plays < 20% of snaps in this one. Groups: EDGE
(DE), IDL (DT/NT), LB, CB, S. Outcomes: defense EPA per dropback, per rush,
per play, and points allowed. Baseline: defense and opposing offense
season-to-date (earlier weeks). Each season held out in turn."""
import sys
from pathlib import Path
import numpy as np, pandas as pd

RAW = Path(__file__).resolve().parents[1] / "data/raw/nflverse"
GROUP = {"DE": "EDGE", "OLB": "EDGE", "DT": "IDL", "NT": "IDL", "LB": "LB", "ILB": "LB", "MLB": "LB",
         "CB": "CB", "FS": "S", "SS": "S", "S": "S", "DB": "S"}
G = ["EDGE", "IDL", "LB", "CB", "S"]


def missing(season):
    s = pd.read_csv(RAW / f"snap_counts_{season}.csv.gz", low_memory=False)
    s = s[(s.game_type == "REG") & s.position.isin(GROUP)].copy()
    s["grp"] = s.position.map(GROUP)
    games = s[["game_id", "week", "team"]].drop_duplicates().sort_values("week")
    s = s.sort_values("week")
    rows = []
    for team, tg in games.groupby("team"):
        weeks = tg.sort_values("week")
        ts = s[s.team == team]
        for i, g in enumerate(weeks.itertuples()):
            prev = weeks.iloc[max(0, i - 3):i]
            if len(prev) < 2:
                continue
            last2 = set(weeks.iloc[max(0, i - 2):i].game_id)
            pv = ts[ts.game_id.isin(prev.game_id)]
            avg = pv.groupby(["pfr_player_id", "grp"]).agg(n=("defense_pct", "size"), pct=("defense_pct", "mean")).reset_index()
            st = avg[(avg.n >= 2) & (avg.pct >= 0.6)]
            recent = set(ts[ts.game_id.isin(last2) & (ts.defense_pct >= 0.2)].pfr_player_id)
            st = st[st.pfr_player_id.isin(recent)]
            now = ts[(ts.game_id == g.game_id) & (ts.defense_pct >= 0.2)].pfr_player_id
            miss = st[~st.pfr_player_id.isin(set(now))]
            r = {"game_id": g.game_id, "defteam": team, "week": g.week, "season": season, "starters": len(st)}
            for grp in G:
                r["miss_" + grp] = int((miss.grp == grp).sum())
            rows.append(r)
    return pd.DataFrame(rows)


def outcomes(season):
    p = pd.read_csv(RAW / f"play_by_play_{season}.csv.gz", low_memory=False,
                    usecols=["game_id", "season_type", "week", "posteam", "defteam", "epa", "qb_dropback", "rush", "play_type"])
    p = p[(p.season_type == "REG") & p.play_type.isin(["pass", "run"]) & p.epa.notna()]
    p["pass_epa"] = np.where(p.qb_dropback == 1, p.epa, np.nan)
    p["rush_epa"] = np.where((p.rush == 1) & (p.qb_dropback != 1), p.epa, np.nan)
    o = p.groupby(["game_id", "week", "defteam", "posteam"]).agg(epa=("epa", "mean"), pass_epa=("pass_epa", "mean"),
                                                                 rush_epa=("rush_epa", "mean"), plays=("epa", "size")).reset_index()
    o["season"] = season
    return o


def trailing(o, key, cols, k=150):
    o = o.sort_values("week")
    out = o.copy()
    g = o.groupby(key)
    for c in cols:
        s = g[c].transform(lambda x: x.shift().expanding().mean())
        n = g.cumcount()
        out["t_" + c] = s * n / (n + 3)   # shrink early weeks toward 0 (league)
    return out


def main():
    M = pd.concat([missing(s) for s in range(2021, 2026)])
    O = pd.concat([outcomes(s) for s in range(2021, 2026)])
    lg = O.groupby("season")[["epa", "pass_epa", "rush_epa"]].transform("mean")
    for c in ("epa", "pass_epa", "rush_epa"):
        O[c] = O[c] - lg[c]
    O = trailing(O, ["season", "defteam"], ["epa", "pass_epa", "rush_epa"])
    off = trailing(O.rename(columns={"defteam": "d", "posteam": "defteam"}), ["season", "defteam"], ["epa", "pass_epa", "rush_epa"])
    off = off.rename(columns={"defteam": "posteam", "d": "defteam"})[["game_id", "posteam", "t_epa", "t_pass_epa", "t_rush_epa"]]
    off.columns = ["game_id", "posteam", "o_epa", "o_pass_epa", "o_rush_epa"]
    D = O.merge(off, on=["game_id", "posteam"]).merge(M, on=["game_id", "defteam", "season", "week"])
    D = D[D.week >= 4].dropna(subset=["t_epa", "o_epa"])
    print(f"{len(D)} defense-games; starters missing per game: " +
          ", ".join(f"{g} {D['miss_' + g].mean():.2f}" for g in G))
    for target, base in (("pass_epa", ["t_pass_epa", "o_pass_epa"]), ("rush_epa", ["t_rush_epa", "o_rush_epa"]), ("epa", ["t_epa", "o_epa"])):
        d = D.dropna(subset=[target] + base)
        y = d[target].values
        for name, fs in (("baseline", base), ("+ missing starters by group", base + ["miss_" + g for g in G])):
            err = []
            for s in sorted(d.season.unique()):
                tr, te = (d.season != s).values, (d.season == s).values
                X = np.c_[np.ones(tr.sum()), d.loc[tr, fs]]
                b = np.linalg.lstsq(X, y[tr], rcond=None)[0]
                err.append(np.mean((y[te] - np.c_[np.ones(te.sum()), d.loc[te, fs]] @ b) ** 2))
            X = np.c_[np.ones(len(d)), d[fs]]
            b, *_ = np.linalg.lstsq(X, y, rcond=None)
            resid = y - X @ b
            se = np.sqrt(np.diag(np.linalg.inv(X.T @ X)) * resid.var())
            tstats = {f: f"{bb:+.3f} (t {bb / ss:+.1f})" for f, bb, ss in zip(fs, b[1:], se[1:]) if f.startswith("miss")}
            print(f"{target:9s} {name:28s} oos mse {np.mean(err):.5f}  {tstats if tstats else ''}")
    D.to_csv(Path(__file__).resolve().parents[1] / "output/2026/def_injury_test.csv", index=False)


if __name__ == "__main__":
    main()
