"""Do pass-zone matchups repeat? 2021-25 play-by-play. Unit = team-game x zone
(short/deep x left/middle/right). Predict that game's completion rate and EPA
per attempt in the zone from season-to-date (earlier weeks only): offense
overall + defense overall (baseline) vs adding offense-in-zone and
defense-allowed-in-zone. Each season held out in turn."""
import sys
from pathlib import Path
import numpy as np, pandas as pd

RAW = Path(__file__).resolve().parents[1] / "data/raw/nflverse"
COLS = ["season", "week", "game_id", "posteam", "defteam", "pass_attempt", "sack", "pass_length", "pass_location",
        "complete_pass", "epa", "season_type", "two_point_attempt", "air_yards", "yards_gained"]


def zone_games(season):
    p = pd.read_csv(RAW / f"play_by_play_{season}.csv.gz", usecols=lambda c: c in COLS, low_memory=False)
    p = p[(p.season_type == "REG") & (p.pass_attempt == 1) & (p.sack != 1) & (p.two_point_attempt != 1)
          & p.pass_length.notna() & p.pass_location.notna()].copy()
    p["zone"] = p.pass_length + "_" + p.pass_location
    agg = dict(att=("complete_pass", "size"), comp=("complete_pass", "sum"), epa=("epa", "sum"), yds=("yards_gained", "sum"))
    z = p.groupby(["season", "week", "game_id", "posteam", "defteam", "zone"]).agg(**agg).reset_index()
    tot = p.groupby(["season", "week", "game_id", "posteam", "defteam"]).agg(**agg).reset_index()
    return z, tot


def trailing(df, key, cols):
    df = df.sort_values(["season", "week"])
    g = df.groupby(key)
    out = df.copy()
    for c in cols:
        out["c_" + c] = g[c].transform(lambda s: s.shift().cumsum())
    return out


def main():
    Z, T = zip(*[zone_games(s) for s in range(2021, 2026)])
    Z, T = pd.concat(Z), pd.concat(T)
    cols = ["att", "comp", "epa", "yds"]
    oz = trailing(Z, ["season", "posteam", "zone"], cols)
    dz = trailing(Z, ["season", "defteam", "zone"], cols)
    ot = trailing(T, ["season", "posteam"], cols)
    dt = trailing(T, ["season", "defteam"], cols)
    lg = Z.groupby(["season", "zone"])[cols].sum()
    k = {"cmp": 40, "epa": 80}       # shrink: attempts to 50% trust
    d = Z.merge(oz[["game_id", "posteam", "zone"] + ["c_" + c for c in cols]], on=["game_id", "posteam", "zone"]) \
         .merge(dz[["game_id", "defteam", "zone"] + ["c_" + c for c in cols]], on=["game_id", "defteam", "zone"], suffixes=("_oz", "_dz")) \
         .merge(ot[["game_id", "posteam"] + ["c_" + c for c in cols]].rename(columns={f"c_{c}": f"c_{c}_ot" for c in cols}), on=["game_id", "posteam"]) \
         .merge(dt[["game_id", "defteam"] + ["c_" + c for c in cols]].rename(columns={f"c_{c}": f"c_{c}_dt" for c in cols}), on=["game_id", "defteam"])
    d = d[(d.week >= 5) & (d.att >= 3)].dropna()
    d = d.join(lg, on=["season", "zone"], rsuffix="_lg")
    lcmp, lepa = d.comp_lg / d.att_lg, d.epa_lg / d.att_lg
    def rate(num, den, lgv, kk):           # shrunk toward the league zone rate
        return (num + kk * lgv) / (den + kk)
    feats = {
        "off_overall_cmp": rate(d.c_comp_ot, d.c_att_ot, lcmp, 40) - lcmp,
        "def_overall_cmp": rate(d.c_comp_dt, d.c_att_dt, lcmp, 40) - lcmp,
        "off_zone_cmp": rate(d.c_comp_oz, d.c_att_oz, lcmp, 40) - lcmp,
        "def_zone_cmp": rate(d.c_comp_dz, d.c_att_dz, lcmp, 40) - lcmp,
        "off_overall_epa": rate(d.c_epa_ot, d.c_att_ot, lepa, 80) - lepa,
        "def_overall_epa": rate(d.c_epa_dt, d.c_att_dt, lepa, 80) - lepa,
        "off_zone_epa": rate(d.c_epa_oz, d.c_att_oz, lepa, 80) - lepa,
        "def_zone_epa": rate(d.c_epa_dz, d.c_att_dz, lepa, 80) - lepa,
    }
    F = pd.DataFrame(feats)
    out = []
    for target, base, add in (("cmp", ["off_overall_cmp", "def_overall_cmp"], ["off_zone_cmp", "def_zone_cmp"]),
                              ("epa", ["off_overall_epa", "def_overall_epa"], ["off_zone_epa", "def_zone_epa"])):
        y = (d.comp / d.att - lcmp) if target == "cmp" else (d.epa / d.att - lepa)
        wts = d.att.values
        for name, fs in (("baseline (overall)", base), ("+ offense zone", base + add[:1]), ("+ defense zone", base + add[1:]),
                         ("+ both zones", base + add)):
            err, errb = [], []
            for s in sorted(d.season.unique()):
                tr, te = d.season != s, d.season == s
                X = np.c_[np.ones(tr.sum()), F.loc[tr, fs]]
                W = wts[tr.values]
                b = np.linalg.lstsq(X * np.sqrt(W)[:, None], y[tr] * np.sqrt(W), rcond=None)[0]
                pred = np.c_[np.ones(te.sum()), F.loc[te, fs]] @ b
                err.append(np.average((y[te] - pred) ** 2, weights=wts[te.values]))
            X = np.c_[np.ones(len(d)), F[fs]]
            b, res, *_ = np.linalg.lstsq(X * np.sqrt(wts)[:, None], y * np.sqrt(wts), rcond=None)
            out.append({"target": target, "model": name, "oos_mse": np.mean(err), "coefs": dict(zip(fs, np.round(b[1:], 3)))})
    R = pd.DataFrame(out)
    for t, g in R.groupby("target"):
        base = g.oos_mse.iloc[0]
        g = g.assign(change_pct=(g.oos_mse / base - 1) * 100)
        print(f"\n{t}: out-of-sample error (lower is better; change vs overall-only)")
        for x in g.itertuples():
            print(f"  {x.model:22s} {x.oos_mse:.5f}  {x.change_pct:+.2f}%   {x.coefs}")
    print(f"\n{len(d)} team-game-zone rows, weeks 5+, 2021-25")
    # split-half repeatability of defense zone weakness (relative to its overall)
    Zs = Z.copy(); Zs["half"] = Zs.week % 2
    h = Zs.groupby(["season", "defteam", "zone", "half"])[["comp", "att"]].sum()
    h["r"] = h.comp / h.att
    ov = Zs.groupby(["season", "defteam", "half"])[["comp", "att"]].sum(); ov["o"] = ov.comp / ov.att
    h = h.join(ov["o"], on=["season", "defteam", "half"]); h["rel"] = h.r - h.o
    piv = h["rel"].unstack("half").dropna()
    print("defense zone weakness (completion % vs its own overall), odd vs even weeks: r =",
          round(np.corrcoef(piv[0], piv[1])[0, 1], 3), f"(n={len(piv)})")
    h2 = Zs.groupby(["season", "posteam", "zone", "half"])[["comp", "att"]].sum(); h2["r"] = h2.comp / h2.att
    ov2 = Zs.groupby(["season", "posteam", "half"])[["comp", "att"]].sum(); ov2["o"] = ov2.comp / ov2.att
    h2 = h2.join(ov2["o"], on=["season", "posteam", "half"]); h2["rel"] = h2.r - h2.o
    p2 = h2["rel"].unstack("half").dropna()
    print("offense zone strength (completion % vs its own overall), odd vs even weeks: r =",
          round(np.corrcoef(p2[0], p2[1])[0, 1], 3), f"(n={len(p2)})")


if __name__ == "__main__":
    main()
