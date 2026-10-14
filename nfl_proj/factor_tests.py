"""Out-of-sample tests for candidate factors, 2021-2025 (nflverse, free).

A factor enters the model only if it predicts games it wasn't fit on. Each
test reports a coefficient, its t-statistic and a verdict:

1. Run type: do running lane, defenders in the box or shotgun / under
   centre add anything beyond the offense's and defense's overall rushing
   rate? (team-game yards per carry, weeks 6+, features from earlier weeks)
2. Line continuity: does last season predict this season better when the
   same offensive / defensive linemen return? (team-season pairs)
3. Corner history: does a receiver's result in earlier games against the
   same starting corners predict today, beyond his own average and the
   defense's average? (player-games)
4. Defensive coordinator: does a defense's profile (yards allowed to WR /
   TE / RB, run defense, sacks, blitz and box rates) carry over more when
   the coordinator stays, and does it follow a coordinator to a new team?

Run: python -m nfl_proj factor-tests  ->  output/<season>/factor_tests.md
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .nflverse import team as nv_team

PBP_COLS = ["season", "season_type", "week", "game_id", "play_id", "posteam", "defteam", "play_type",
            "rush_attempt", "qb_dropback", "qb_scramble", "sack", "yards_gained", "run_location", "run_gap",
            "shotgun", "wp", "two_point_attempt", "epa", "receiver_player_id", "pass_attempt",
            "complete_pass", "touchdown", "td_team", "interception"]
OL, DL = {"T", "G", "C"}, {"DE", "DT", "NT"}


# ----------------------------------------------------------------- loading
def load(raw: Path, seasons: list[int]) -> dict:
    pbp, snaps, ftn, pw = [], [], [], []
    for y in seasons:
        p = pd.read_csv(raw / f"play_by_play_{y}.csv.gz", usecols=PBP_COLS, low_memory=False)
        pbp.append(p[(p["season_type"] == "REG") & p["play_type"].isin(["run", "pass"])
                     & (p["two_point_attempt"].fillna(0) == 0)])
        snaps.append(pd.read_csv(raw / f"snap_counts_{y}.csv.gz").query("game_type == 'REG'"))
        f = raw / f"ftn_charting_{y}.csv"
        if f.exists():
            ftn.append(pd.read_csv(f, usecols=["nflverse_game_id", "nflverse_play_id", "n_defense_box",
                                               "n_blitzers"]))
        w = pd.read_csv(raw / f"stats_player_week_{y}.csv.gz", low_memory=False)
        pw.append(w[w["season_type"] == "REG"])
    p = pd.concat(pbp, ignore_index=True)
    for c in ("posteam", "defteam", "td_team"):
        p[c] = p[c].map(nv_team)
    if ftn:
        f = pd.concat(ftn).rename(columns={"nflverse_game_id": "game_id", "nflverse_play_id": "play_id"})
        p = p.merge(f.drop_duplicates(["game_id", "play_id"]), on=["game_id", "play_id"], how="left")
    p["run"] = (p["rush_attempt"] == 1) & (p["qb_scramble"].fillna(0) == 0) & (p["play_type"] == "run")
    p["ry"] = p["yards_gained"].clip(upper=30)  # long-run cap: one 70-yarder isn't a trait
    s = pd.concat(snaps, ignore_index=True)
    for c in ("team", "opponent"):
        s[c] = s[c].map(nv_team)
    w = pd.concat(pw, ignore_index=True)
    w["team"] = w["team"].map(nv_team)
    w["opponent_team"] = w["opponent_team"].map(nv_team)
    return {"pbp": p, "snaps": s, "pw": w}


def _ols(X: np.ndarray, y: np.ndarray, w: np.ndarray | None = None) -> tuple[np.ndarray, np.ndarray]:
    """Weighted least squares; returns coefficients and t-statistics."""
    w = np.ones(len(y)) if w is None else w
    Xw = X * np.sqrt(w)[:, None]
    yw = y * np.sqrt(w)
    b, *_ = np.linalg.lstsq(Xw, yw, rcond=None)
    resid = yw - Xw @ b
    dof = max(len(y) - X.shape[1], 1)
    cov = np.linalg.pinv(Xw.T @ Xw) * (resid @ resid / dof)
    return b, b / np.sqrt(np.clip(np.diag(cov), 1e-12, None))


def _verdict(t: float, sign_ok: bool = True) -> str:
    if abs(t) >= 2.5 and sign_ok:
        return "**use**"
    if abs(t) >= 1.7 and sign_ok:
        return "weak (not used)"
    return "noise (not used)"


def _shrunk(sum_dev: pd.Series, n: pd.Series, k: float) -> pd.Series:
    return sum_dev / (n + k)


# ------------------------------------------------------------- 1. run type
def run_type(d: dict, first_week: int = 6) -> tuple[pd.DataFrame, str]:
    p = d["pbp"]
    r = p[p["run"] & p["wp"].between(0.05, 0.95)].copy()
    r["lane"] = np.where(r["run_location"] == "middle", "middle",
                         r["run_location"].fillna("x") + "_" + np.where(r["run_gap"] == "end", "out", "in"))
    r = r[r["lane"] != "x_in"]
    r["box"] = pd.cut(r["n_defense_box"], [-1, 6, 7, 20], labels=["light", "seven", "heavy"]).astype(str)
    r["form"] = np.where(r["shotgun"] == 1, "gun", "uc")
    games = r.groupby(["season", "week", "game_id", "posteam", "defteam"]).agg(
        ypc=("ry", "mean"), n=("ry", "size")).reset_index()
    rows = []
    for (season, week), g in games[games["week"] >= first_week].groupby(["season", "week"]):
        h = r[(r["season"] == season) & (r["week"] < week)]
        lg = h["ry"].mean()
        h = h.assign(dev=h["ry"] - lg)

        def dev(keys, k):
            a = h.groupby(keys)["dev"].agg(["sum", "size"])
            return _shrunk(a["sum"], a["size"], k)
        off, dfn = dev("posteam", 120), dev("defteam", 120)
        lane_lg = h.groupby("lane")["ry"].mean() - lg
        h2 = h.assign(ldev=h["ry"] - lg - h["lane"].map(lane_lg))
        dl = h2.groupby(["defteam", "lane"])["ldev"].agg(["sum", "size"])
        def_lane = _shrunk(dl["sum"], dl["size"], 40)
        off_share = h.groupby(["posteam", "lane"]).size() / h.groupby("posteam").size()
        has_box = h["n_defense_box"].notna().mean() > 0.5
        if has_box:
            box_lg = h.groupby("box")["ry"].mean() - lg
            hb = h.assign(bdev=h["ry"] - lg - h["box"].map(box_lg))
            ob = hb.groupby(["posteam", "box"])["bdev"].agg(["sum", "size"])
            off_box = _shrunk(ob["sum"], ob["size"], 40)
            def_box_share = h.groupby(["defteam", "box"]).size() / h.groupby("defteam").size()
        form_lg = h.groupby("form")["ry"].mean() - lg
        hf = h.assign(fdev=h["ry"] - lg - h["form"].map(form_lg))
        dfm = hf.groupby(["defteam", "form"])["fdev"].agg(["sum", "size"])
        def_form = _shrunk(dfm["sum"], dfm["size"], 40)
        off_form_share = h.groupby(["posteam", "form"]).size() / h.groupby("posteam").size()
        for x in g.itertuples():
            o, de = off.get(x.posteam, 0.0), dfn.get(x.defteam, 0.0)
            f_lane = sum(off_share.get((x.posteam, L), 0) * def_lane.get((x.defteam, L), 0.0)
                         for L in lane_lg.index)
            f_box = (sum(def_box_share.get((x.defteam, b), 0) * off_box.get((x.posteam, b), 0.0)
                         for b in ("light", "seven", "heavy")) if has_box else np.nan)
            f_form = sum(off_form_share.get((x.posteam, f), 0) * def_form.get((x.defteam, f), 0.0)
                         for f in ("gun", "uc"))
            rows.append({"season": season, "week": week, "y": x.ypc - lg, "n": x.n, "off": o, "def": de,
                         "f_lane": f_lane, "f_box": f_box, "f_form": f_form})
    df = pd.DataFrame(rows)
    out = []
    base = df.dropna(subset=["f_box"])
    for name, cols, data in (("overall offense + defense", ["off", "def"], df),
                             ("+ defense weakness by lane x offense lane tendency", ["off", "def", "f_lane"], df),
                             ("+ offense vs box count x defense box tendency", ["off", "def", "f_box"], base),
                             ("+ defense by shotgun / under centre x offense formation mix",
                              ["off", "def", "f_form"], df)):
        X = np.c_[np.ones(len(data)), data[cols].to_numpy()]
        b, t = _ols(X, data["y"].to_numpy(), data["n"].to_numpy())
        out.append({"model": name, "games": len(data), **{f"b_{c}": b[i + 1] for i, c in enumerate(cols)},
                    "t_new": t[-1] if len(cols) > 2 else np.nan,
                    "verdict": _verdict(t[-1], b[-1] > 0) if len(cols) > 2 else "baseline"})
    tab = pd.DataFrame(out)
    md = ["## 1. Run type (team-game yards per carry, weeks 6+, 2021-25; box count 2022-25)", "",
          "Each row adds one feature to the baseline (offense and defense overall rushing rate, from "
          "earlier weeks only). A real effect has a coefficient near 1 and t above 2.5.", "",
          tab.to_markdown(index=False, floatfmt=".2f"), ""]
    return tab, "\n".join(md)


# ------------------------------------------------------------- reliability
def reliability(d: dict) -> tuple[pd.DataFrame, str]:
    """How many plays before a team's rate is half signal, half noise.

    Split each team-season into odd / even weeks; the correlation r between
    halves with n plays per half gives k = n (1 - r) / r (Spearman-Brown):
    a rate from n plays deserves weight n / (n + k) against the league."""
    p = d["pbp"]
    p = p[p["wp"].between(0.05, 0.95)].assign(half=lambda x: x["week"] % 2)
    p = p.assign(**{c: p[c].astype(float) for c in ("sack", "complete_pass", "interception")})
    rows = []
    p = p.assign(pyd=p["yards_gained"].clip(-15, 40), td=(p["touchdown"] == 1) & (p["td_team"] == p["posteam"]))
    for name, mask, col in (("rush yards/carry", p["run"], "ry"),
                            ("pass yards/attempt", p["pass_attempt"] == 1, "pyd"),
                            ("completion rate", p["pass_attempt"] == 1, "complete_pass"),
                            ("dropback EPA", p["qb_dropback"] == 1, "epa"),
                            ("sack rate", p["qb_dropback"] == 1, "sack"),
                            ("pass TD / attempt", p["pass_attempt"] == 1, "td"),
                            ("run TD / carry", p["run"], "td"),
                            ("INT / attempt", p["pass_attempt"] == 1, "interception")):
        q = p[mask]
        for side, key in (("offense", "posteam"), ("defense", "defteam")):
            g = q.groupby(["season", key, "half"])[col].agg(["mean", "size"]).unstack("half")
            m = g["mean"].sub(g["mean"].groupby(level=0).transform("mean"))
            r = float(m[0].corr(m[1]))
            n = float(g["size"].mean().mean())
            k = n * (1 - r) / r if r > 0 else np.inf
            rows.append({"rate": name, "side": side, "split_half_r": r, "plays_per_half": n, "k_half_signal": k})
    tab = pd.DataFrame(rows)
    md = ["## 0. How fast team rates become signal (2021-25, odd vs even weeks)", "",
          "k = plays before a team's rate is trusted at 50% (the model's [matchup] shrink_plays).", "",
          tab.to_markdown(index=False, floatfmt=".2f"), ""]
    return tab, "\n".join(md)


# --------------------------------------------------- position groups / CBs
def position_groups(d: dict) -> tuple[pd.DataFrame, str]:
    """Does what a defense allows to WRs / TEs / RBs repeat (odd vs even weeks)?"""
    p, w = d["pbp"], d["pw"]
    pos = w.drop_duplicates("player_id").set_index("player_id")["position_group"]
    a = p[(p["pass_attempt"] == 1) & p["receiver_player_id"].notna() & p["wp"].between(0.05, 0.95)].copy()
    a["grp"] = a["receiver_player_id"].map(pos)
    a = a[a["grp"].isin(["WR", "TE", "RB"])]
    a["y"] = a["yards_gained"].clip(-10, 40)
    a["half"] = a["week"] % 2
    a["dev"] = a["y"] - a.groupby(["season", "grp"])["y"].transform("mean")
    a["rel"] = a["dev"] - a.groupby(["season", "defteam", "half"])["dev"].transform("mean")
    rows = []
    for grp in ("WR", "TE", "RB"):
        g = a[a["grp"] == grp].groupby(["season", "defteam", "half"])["rel"].mean().unstack("half").dropna()
        rows.append({"measure": f"yards/target vs {grp}, beyond defense overall", "split_half_r": g[0].corr(g[1])})
    gw = w[w["position_group"].isin(["WR", "TE", "RB"])].groupby(
        ["season", "opponent_team", "week", "position_group"])["targets"].sum().unstack().fillna(0)
    share = gw.div(gw.sum(axis=1), axis=0).reset_index()
    share["half"] = share["week"] % 2
    for grp in ("WR", "TE", "RB"):
        m = share.groupby(["season", "opponent_team", "half"])[grp].mean().unstack("half")
        m = m.sub(m.groupby(level=0).transform("mean"))
        rows.append({"measure": f"share of targets to {grp}", "split_half_r": m[0].corr(m[1])})
    tab = pd.DataFrame(rows)
    tab["verdict"] = np.where(tab["split_half_r"] >= 0.2, "real (weak)", "noise")
    md = ["## 5. What a defense allows by position group (2021-25, odd vs even weeks, ~8 games each)", "",
          "\"Can't cover tight ends\" style splits: a real trait repeats between halves of a season.", "",
          tab.to_markdown(index=False, floatfmt=".2f"), ""]
    return tab, "\n".join(md)


def corner_quality(raw: Path) -> tuple[pd.DataFrame, str]:
    """Individual coverage (PFR charting, nflverse 2024+): does a defender's
    yards / completions per target allowed repeat?"""
    fr = [pd.read_csv(f) for f in sorted(raw.glob("advstats_week_def_*.csv.gz"))]
    a = pd.concat(fr, ignore_index=True)
    a = a[(a.get("game_type", "REG") == "REG") & (a["def_targets"].fillna(0) > 0)]
    a = a[a["season"] < a["season"].max()]  # complete seasons only
    a["half"] = a["week"] % 2
    g = a.groupby(["season", "pfr_player_id", "half"])[["def_targets", "def_yards_allowed",
                                                         "def_completions_allowed"]].sum().unstack("half").dropna()
    g = g[(g["def_targets"][0] >= 15) & (g["def_targets"][1] >= 15)]
    n = float(g["def_targets"].mean().mean())
    rows = []
    for name, num in (("yards per target allowed", "def_yards_allowed"),
                      ("completion % allowed", "def_completions_allowed")):
        x = g[num] / g["def_targets"]
        r = float(x[0].corr(x[1]))
        rows.append({"measure": name, "defenders": len(g), "targets_per_half": n, "split_half_r": r,
                     "k_targets": n * (1 - r) / r if r > 0 else np.inf})
    tab = pd.DataFrame(rows)
    md = ["## 6. Individual corners (PFR coverage charting, seasons " +
          ", ".join(map(str, sorted(a["season"].unique()))) + ")", "",
          "k_targets = targets before a defender's own rate is trusted at 50% ([corners] shrink_targets).", "",
          tab.to_markdown(index=False, floatfmt=".2f"), ""]
    return tab, "\n".join(md)


# ----------------------------------------------------- team-season metrics
def team_seasons(d: dict) -> pd.DataFrame:
    p = d["pbp"]
    p = p[p["wp"].between(0.05, 0.95)]
    out = []
    for side, key in (("off", "posteam"), ("def", "defteam")):
        g = p.groupby(["season", key])
        r = p[p["run"]].groupby(["season", key])
        db = p[p["qb_dropback"] == 1].groupby(["season", key])
        m = pd.DataFrame({"rush_ypc": r["ry"].mean(), "rush_epa": r["epa"].mean(),
                          "sack_rate": db["sack"].mean(), "dropback_epa": db["epa"].mean()})
        if side == "def":
            m["blitz_rate"] = db["n_blitzers"].apply(lambda s: (s > 0).mean() if s.notna().any() else np.nan)
            m["light_box_rate"] = r["n_defense_box"].apply(lambda s: (s <= 6).mean() if s.notna().any() else np.nan)
        m = m.reset_index().rename(columns={key: "team"}).assign(side=side)
        out.append(m)
    ts = pd.concat(out, ignore_index=True)
    # Receiving allowed by position group per game (the "props" a defense gives up)
    w = d["pw"]
    rec = w[w["position_group"].isin(["WR", "TE", "RB"])].groupby(
        ["season", "opponent_team", "position_group", "week"])[["receiving_yards", "receptions"]].sum()
    rec = rec.groupby(level=[0, 1, 2]).mean().reset_index()
    for col in ("receiving_yards", "receptions"):
        pv = rec.pivot_table(index=["season", "opponent_team"], columns="position_group", values=col)
        pv.columns = [f"{c.lower()}_{'rec_yds' if col == 'receiving_yards' else 'rec'}_allowed" for c in pv.columns]
        pv = pv.reset_index().rename(columns={"opponent_team": "team"}).assign(side="def")
        ts = ts.merge(pv, on=["season", "team", "side"], how="left")
    return ts


def _dev(ts: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    ts = ts.copy()
    for c in cols:
        ts[c] = ts[c] - ts.groupby(["season", "side"])[c].transform("mean")
    return ts


# --------------------------------------------------------- 2. continuity
def continuity(d: dict) -> pd.DataFrame:
    s = d["snaps"]
    rows = []
    for grp, pos, col in (("ol", OL, "offense_snaps"), ("dl", DL, "defense_snaps")):
        x = s[s["position"].isin(pos)].groupby(["season", "team", "pfr_player_id"])[col].sum().reset_index()
        for (season, team), g in x.groupby(["season", "team"]):
            prev = x[(x["season"] == season - 1) & (x["team"] == team) & (x[col] >= 200)]
            if prev.empty:
                continue
            ret = g[g["pfr_player_id"].isin(set(prev["pfr_player_id"]))][col].sum()
            rows.append({"season": season, "team": team, f"{grp}_continuity": ret / g[col].sum()})
    c = pd.DataFrame(rows)
    return c.groupby(["season", "team"]).first().reset_index()


def continuity_test(ts: pd.DataFrame, cont: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    metrics = {"off": (["rush_ypc", "rush_epa", "sack_rate", "dropback_epa"], "ol_continuity"),
               "def": (["rush_ypc", "rush_epa", "sack_rate", "dropback_epa"], "dl_continuity")}
    allc = sum((v[0] for v in metrics.values()), [])
    dv = _dev(ts, sorted(set(allc)))
    out = []
    for side, (ms, ccol) in metrics.items():
        a = dv[dv["side"] == side]
        pair = a.merge(a.assign(season=a["season"] + 1), on=["season", "team"], suffixes=("", "_prev")) \
                .merge(cont, on=["season", "team"], how="inner")
        pair = pair[pair["season"] <= 2025]
        cm = pair[ccol].mean()
        for m in ms:
            q = pair.dropna(subset=[m, f"{m}_prev", ccol])
            x = q[f"{m}_prev"].to_numpy()
            cc = (q[ccol] - cm).to_numpy()
            X = np.c_[np.ones(len(q)), x, x * cc]
            b, t = _ols(X, q[m].to_numpy())
            lo, hi = q[ccol].quantile(0.25), q[ccol].quantile(0.75)
            out.append({"side": side, "metric": m, "pairs": len(q), "carryover_avg": b[1],
                        "carryover_low_cont": b[1] + b[2] * (lo - cm), "carryover_high_cont": b[1] + b[2] * (hi - cm),
                        "t_interaction": t[2], "verdict": _verdict(t[2], b[2] > 0)})
    tab = pd.DataFrame(out)
    md = ["## 2. Line continuity (season-to-season, 2021->25)", "",
          "carryover = share of last season's deviation from league that repeats this season. If returning "
          "linemen matter, carryover is higher when continuity (share of this season's OL / DL snaps by "
          "players who were on the same line last season, 200+ snaps) is high. low / high = 25th / 75th "
          "percentile of continuity.", "",
          tab.to_markdown(index=False, floatfmt=".2f"), ""]
    return tab, "\n".join(md)


# ------------------------------------------------------ 3. corner history
def corner_history(d: dict, max_seasons_back: int = 3) -> tuple[pd.DataFrame, str]:
    s, w = d["snaps"], d["pw"]
    cb = s[(s["position"] == "CB") & (s["defense_pct"] >= 0.6)]
    starters = cb.groupby(["season", "week", "team"])["pfr_player_id"].apply(frozenset).rename("cbs")
    wr = w[(w["position"] == "WR")][["player_id", "player_display_name", "season", "week", "team",
                                     "opponent_team", "targets", "receiving_yards", "receptions"]].copy()
    wr = wr.sort_values(["player_id", "season", "week"])
    wr["t"] = wr["season"] * 100 + wr["week"]
    for col in ("receiving_yards", "targets", "receptions"):
        wr[f"{col}_avg"] = wr.groupby("player_id")[col].transform(lambda x: x.shift().rolling(8, min_periods=4).mean())
    wr = wr[wr["targets_avg"] >= 4].copy()
    for col in ("receiving_yards", "receptions"):
        wr[f"r_{col}"] = wr[col] - wr[f"{col}_avg"]
        # Remove the defense's general effect (leave-one-out within season)
        g = wr.groupby(["season", "opponent_team"])[f"r_{col}"]
        wr[f"r2_{col}"] = wr[f"r_{col}"] - (g.transform("sum") - wr[f"r_{col}"]) / (g.transform("count") - 1).clip(lower=1)
    wr = wr.join(starters, on=["season", "week", "opponent_team"])
    wr = wr[wr["cbs"].notna()]
    rows = []
    for pid, g in wr.groupby("player_id"):
        g = g.reset_index(drop=True)
        for i in range(1, len(g)):
            cur = g.loc[i]
            prev = g.loc[:i - 1]
            prev = prev[prev["season"] >= cur["season"] - max_seasons_back]
            shared = prev[prev["cbs"].apply(lambda c: len(c & cur["cbs"]) > 0)]
            same_team_other = prev[(prev["opponent_team"] == cur["opponent_team"])
                                   & ~prev.index.isin(shared.index)]
            rec = {"y_yds": cur["r2_receiving_yards"], "y_rec": cur["r2_receptions"]}
            if len(shared):
                rec |= {"h_yds": shared["r2_receiving_yards"].mean(), "h_rec": shared["r2_receptions"].mean(),
                        "n_hist": len(shared), "kind": "shared starting CB"}
                rows.append(rec)
            elif len(same_team_other):
                rec |= {"h_yds": same_team_other["r2_receiving_yards"].mean(),
                        "h_rec": same_team_other["r2_receptions"].mean(),
                        "n_hist": len(same_team_other), "kind": "same defense, different CBs"}
                rows.append(rec)
    h = pd.DataFrame(rows)
    out = []
    for kind, g in h.groupby("kind"):
        for stat in ("yds", "rec"):
            X = np.c_[np.ones(len(g)), g[f"h_{stat}"].to_numpy()]
            b, t = _ols(X, g[f"y_{stat}"].to_numpy(), g["n_hist"].clip(upper=4).to_numpy())
            out.append({"history": kind, "stat": "rec_yds" if stat == "yds" else "receptions", "games": len(g),
                        "carryover": b[1], "t": t[1], "verdict": _verdict(t[1], b[1] > 0)})
    tab = pd.DataFrame(out)
    md = ["## 3. Receiver vs the same corners (2021-25 player-games)", "",
          "Residual = result minus the receiver's own 8-game average, minus what that defense allows every "
          "receiver that season. carryover = how much of his residual in earlier games against any of today's "
          "starting corners (60%+ of snaps, any team) repeats today. Free data has no per-play coverage "
          "assignment, so 'faced the corner' means the corner started in that game.", "",
          tab.to_markdown(index=False, floatfmt=".3f"), ""]
    return tab, "\n".join(md)


# -------------------------------------------------- 4. defensive coordinator
def coordinator_test(ts: pd.DataFrame, coord: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    col = "def_play_caller" if "def_play_caller" in coord else "def_coordinator"
    c = coord[["season", "team", col]].copy()
    c["dc"] = c[col].fillna("").str.split(" / ").str[0].str.strip()
    metrics = ["rush_ypc", "rush_epa", "sack_rate", "dropback_epa", "blitz_rate", "light_box_rate",
               "wr_rec_yds_allowed", "te_rec_yds_allowed", "rb_rec_yds_allowed", "te_rec_allowed",
               "rb_rec_allowed"]
    a = _dev(ts[ts["side"] == "def"], metrics).merge(c[["season", "team", "dc"]], on=["season", "team"], how="left")
    prev = a.assign(season=a["season"] + 1)
    pair = a.merge(prev, on=["season", "team"], suffixes=("", "_prev"))
    pair = pair[(pair["season"] <= 2025) & pair["dc"].fillna("").ne("") & pair["dc_prev"].fillna("").ne("")]
    pair["new_dc"] = (pair["dc"] != pair["dc_prev"]).astype(float)
    # Defenses whose new coordinator ran another defense last season
    by_dc = prev.dropna(subset=["dc"]).set_index(["season", "dc"])
    out = []
    for m in metrics:
        q = pair.dropna(subset=[m, f"{m}_prev"])
        if len(q) < 30:
            continue
        x = q[f"{m}_prev"].to_numpy()
        X = np.c_[np.ones(len(q)), x, x * q["new_dc"].to_numpy()]
        b, t = _ols(X, q[m].to_numpy())
        mv = q[(q["new_dc"] == 1)].copy()
        mv["dc_old"] = [by_dc[m].get((s, dc), np.nan) if (s, dc) in by_dc.index else np.nan
                        for s, dc in zip(mv["season"], mv["dc"])]
        mv = mv.dropna(subset=["dc_old"])
        mv = mv[mv["dc_old"] != mv[f"{m}_prev"]]
        if len(mv) >= 8:
            X2 = np.c_[np.ones(len(mv)), mv[f"{m}_prev"].to_numpy(), mv["dc_old"].to_numpy()]
            b2, t2 = _ols(X2, mv[m].to_numpy())
            follow, t_follow, n_mv = b2[2], t2[2], len(mv)
        else:
            follow = t_follow = np.nan
            n_mv = len(mv)
        out.append({"metric": m, "pairs": len(q), "carryover_same_dc": b[1], "carryover_new_dc": b[1] + b[2],
                    "t_change": t[2], "verdict_change": _verdict(t[2], b[2] < 0),
                    "movers": n_mv, "follows_dc": follow, "t_follow": t_follow,
                    "verdict_follow": _verdict(t_follow, follow > 0) if np.isfinite(t_follow) else "too few"})
    tab = pd.DataFrame(out)
    md = ["## 4. Defensive play caller (season-to-season, 2022->25)", "",
          "carryover_same_dc / new_dc = share of last season's deviation from league that repeats when the "
          "coordinator stays / changes (t_change tests the difference). follows_dc = for coordinators who "
          "moved teams, how much of their OLD defense's deviation shows up in their new defense, beyond the "
          "new team's own last season. Coordinators from "
          "(data/external/coordinators.csv, 2022-25 from public staff lists); the defensive play caller is used "
          "where it isn't the coordinator (e.g. a head coach who calls the defense).", "",
          tab.to_markdown(index=False, floatfmt=".2f"), ""]
    return tab, "\n".join(md)


def ensure_files(raw: Path, seasons, log=print) -> None:
    """Download any missing history files (nflverse releases, cached)."""
    from .nflverse import RELEASES, Downloader
    dl = Downloader(raw, log=log)
    for y in seasons:
        for rel in (f"pbp/play_by_play_{y}.csv.gz", f"snap_counts/snap_counts_{y}.csv.gz",
                    f"stats_player/stats_player_week_{y}.csv.gz"):
            dl.get(f"{RELEASES}/{rel}")
        if y >= 2024:  # PFR coverage charting in nflverse starts 2024
            dl.get(f"{RELEASES}/pfr_advstats/advstats_week_def_{y}.csv.gz")
        if y >= 2022:
            try:
                dl.get(f"{RELEASES}/ftn_charting/ftn_charting_{y}.csv")
            except Exception as e:  # charting is optional
                log(f"ftn {y}: {e}")


def run_all(raw: Path, coord_path: Path, out: Path, seasons=(2021, 2022, 2023, 2024, 2025), log=print) -> dict:
    ensure_files(raw, seasons, log)
    d = load(raw, list(seasons))
    log("loaded", len(d["pbp"]), "plays")
    res, md = {}, ["# Factor tests", "",
                   "Every candidate factor is tested on games it wasn't fit on. Verdicts: **use** = t >= 2.5 "
                   "with the expected sign; weak = t 1.7-2.5 (not used; revisit with more data); noise = not "
                   "used.", ""]
    res["reliability"], m = reliability(d)
    md.append(m)
    res["run"], m = run_type(d)
    md.append(m)
    log("run type done")
    ts = team_seasons(d)
    cont = continuity(d)
    res["continuity"], m = continuity_test(ts, cont)
    md.append(m)
    log("continuity done")
    if coord_path.exists():
        res["coordinator"], m = coordinator_test(ts, pd.read_csv(coord_path))
        md.append(m)
        log("coordinator done")
    res["corners"], m = corner_history(d)
    md.append(m)
    res["positions"], m = position_groups(d)
    md.append(m)
    res["corner_quality"], m = corner_quality(raw)
    md.append(m)
    log("corners done")
    out.write_text("\n".join(md))
    return res
