"""Monte Carlo game simulation for prop markets.

Each simulated game draws play volume, the pass/run split, bucket mix,
who gets each target / carry, completions, yards (resampled from real plays
in that bucket, adjusted to the player and the matchup), touchdowns,
interceptions, sacks, kicks and defensive credits. Every prop is then read
off the same simulated games, so the numbers are consistent with each other
(QB passing yards = sum of his receivers' yards in every simulation).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .profiles import shrink
from .project import OTHER_PASS, Projector, _wmean

OFFENSE_STATS = ["pass_att", "completions", "pass_yds", "pass_td", "interceptions",
                 "longest_completion", "carries", "rush_yds", "rush_td", "longest_rush",
                 "targets", "receptions", "rec_yds", "rec_td", "longest_rec"]
DERIVED = ["rush_rec_yds", "pass_rush_yds", "rush_rec_td", "fantasy_ppr"]
KICKER_STATS = ["fg_made", "fg_att", "xp_made", "kicking_points"]
DEFENSE_STATS = ["tackles", "sacks", "def_int"]


def _draw_sum_max(rng, counts, pool, scale=1.0, shift=0.0):
    """For each sim i, sum and max of counts[i] draws from ``pool``."""
    n = len(counts)
    k = int(counts.max()) if n else 0
    if k == 0 or len(pool) == 0:
        return np.zeros(n), np.zeros(n)
    draws = rng.choice(pool, size=(n, k)) * scale + shift
    mask = np.arange(k)[None, :] < counts[:, None]
    total = np.where(mask, draws, 0).sum(1)
    longest = np.where(mask, draws, -np.inf).max(1)
    return total, np.where(counts > 0, longest, 0.0)


class Simulator:
    def __init__(self, proj: Projector, player_games: pd.DataFrame, defenders: pd.DataFrame | None,
                 kickers: pd.DataFrame | None, n_sims: int = 5000, seed: int = 0):
        self.P = proj
        self.n = n_sims
        self.rng = np.random.default_rng(seed)
        self.defenders = defenders if defenders is not None else pd.DataFrame()
        self.kickers = kickers if kickers is not None else pd.DataFrame()
        p = proj.p
        comp = proj.passes[proj.passes["complete"].fillna(False).astype(bool)]
        self.comp_pool = {b: g["yards"].dropna().to_numpy(float) for b, g in comp.groupby("pb")}
        self.comp_all = comp["yards"].dropna().to_numpy(float)
        self.run_pool = {b: g["yards"].dropna().to_numpy(float) for b, g in proj.runs.groupby("bucket")}
        sc = p[p["play_type"] == "scramble"]["yards"].dropna().to_numpy(float)
        self.team_points = {}
        self.team_point_samples = {}
        self.team_components = {}
        self.scramble_pool = sc if len(sc) >= 30 else np.clip(np.random.default_rng(1).normal(6, 5, 400), -3, 40)

    # ------------------------------------------------------------ offense
    def offense(self, team: str, opp: str, week: int) -> tuple[dict, dict]:
        P, rng, n = self.P, self.rng, self.n
        vol = P.team_volume(team, opp, week)
        pmix, _ = P.mix(team, "pass", opp)
        rmix, _ = P.mix(team, "run", opp)
        peff = {b: P.bucket_matchup(team, opp, "pass", b, week) for b in pmix}
        reff = {b: P.bucket_matchup(team, opp, "run", b, week) for b in rmix}
        tm = P.td_mults(team, opp, week)
        active_df = P.active_players(team)
        active = set(active_df["player_id"])

        plays = np.clip(np.round(rng.normal(vol["plays"], P.coach_volume_sd(team), n)), 40, 95).astype(int)
        db = rng.binomial(plays, np.clip(vol["dropback_rate"], 0.2, 0.85))
        dropbacks = vol["pass_att"] + vol["sacks"] + vol["scrambles"]
        sacks = rng.binomial(db, vol["sacks"] / dropbacks)
        scr = rng.binomial(db - sacks, vol["scrambles"] / max(dropbacks - vol["sacks"], 1e-9))
        att = db - sacks - scr
        runs = plays - db

        out: dict[str, dict[str, np.ndarray]] = {}

        def acc(pid, stat, arr, how="sum"):
            d = out.setdefault(pid, {})
            if stat not in d:
                d[stat] = np.array(arr, dtype=float)
            elif how == "max":
                d[stat] = np.maximum(d[stat], arr)
            else:
                d[stat] = d[stat] + arr

        # --- passing / receiving
        tp = P.passes[P.passes["offense"] == team]
        k_t = P.cfg["players"]["shrink_targets"]
        shares = P._shares(tp, "target_id", "pb", active, k_t, team, "target")
        pmix, shares, _ = P.usage_plan(team, opp, "pass", shares, pmix)
        eff, td = P._player_eff(tp, "target_id", "pb", peff, k_t)
        cbf, _ = P.corner_factors(team, opp)
        tgt_rate = tp.assign(has=tp["target_id"].notna()).groupby("pb").apply(
            lambda d: np.average(d["has"], weights=d["w"]), include_groups=False)
        m_pass_td = tm["pass_td"]
        buckets = list(pmix)
        bcounts = rng.multinomial(att, [pmix[b] for b in buckets])
        team_comp = np.zeros(n)
        team_long = np.zeros(n)
        for j, b in enumerate(buckets):
            sb = shares[shares["pb"] == b]
            if sb.empty or sb["share"].sum() <= 0:
                continue
            targeted = rng.binomial(bcounts[:, j], float(tgt_rate.get(b, 0.9)))
            pids = sb["target_id"].tolist()
            per = rng.multinomial(targeted, sb["share"].to_numpy() / sb["share"].sum())
            e_b = peff[b]
            pool = self.comp_pool.get(b, self.comp_all)
            pool_mean = pool.mean() if len(pool) else 1.0
            for i, pid in enumerate(pids):
                k = per[:, i]
                e = eff.loc[(pid, b)] if (pid, b) in eff.index else None
                ypt = (e["ypp_s"] if e is not None else e_b["ypp"]) * e_b["m_ypp"] * cbf.get(pid, 1.0) * \
                    P.sig_mult(team, opp, pid, "pass").get(b, 1.0)
                cr = min((e["cmp_s"] if e is not None else e_b["cmp"]) * e_b["m_cmp"], 0.95)
                comp = rng.binomial(k, max(cr, 0.01))
                scale = ypt / max(cr, 0.01) / pool_mean if pool_mean > 0 else 1.0
                yds, longest = _draw_sum_max(rng, comp, pool, scale=scale)
                if pid in td.index:
                    rate = shrink(td.loc[pid, "td"] / td.loc[pid, "n"], td.loc[pid, "n"],
                                  P.lg_pass_td * P.priors.factor("off", team, "pass_td"), 60)
                else:
                    rate = P.lg_pass_td
                tds = rng.binomial(comp, min(rate * m_pass_td / max(cr, 0.05), 0.8))
                acc(pid, "targets", k)
                acc(pid, "receptions", comp)
                acc(pid, "rec_yds", yds)
                acc(pid, "rec_td", tds)
                acc(pid, "longest_rec", longest, "max")
                team_comp += comp
                team_long = np.maximum(team_long, longest)

        qb = P.starting_qb(team)
        if qb:
            rec_yds = sum(d.get("rec_yds", 0) for d in out.values())
            rec_td = sum(d.get("rec_td", 0) for d in out.values())
            m_int = tm["int"]
            int_rate = shrink(_wmean(tp, "interception"), len(tp), P.lg_int, 200) * m_int
            acc(qb, "pass_att", att)
            acc(qb, "completions", team_comp)
            acc(qb, "pass_yds", rec_yds)
            acc(qb, "pass_td", rec_td)
            acc(qb, "interceptions", rng.binomial(att, min(int_rate, 0.2)))
            acc(qb, "longest_completion", team_long, "max")
            acc(qb, "sacks_taken", sacks)
            syds, slong = _draw_sum_max(rng, scr, self.scramble_pool)
            acc(qb, "carries", scr)
            acc(qb, "rush_yds", syds)
            acc(qb, "rush_td", rng.binomial(scr, min(P.scramble_td_rate(team) * tm["run_td"], 0.5)))
            acc(qb, "longest_rush", slong, "max")

        # --- rushing
        tr = P.runs[P.runs["offense"] == team]
        k_c = P.cfg["players"]["shrink_carries"]
        rshares = P._shares(tr, "rusher_id", "bucket", active, k_c, team, "carry")
        rmix, rshares, _ = P.usage_plan(team, opp, "run", rshares, rmix)
        reff_p, rtd = P._player_eff(tr, "rusher_id", "bucket", reff, k_c)
        m_run_td = tm["run_td"]
        rb = list(rmix)
        rcounts = rng.multinomial(runs, [rmix[b] for b in rb])
        for j, b in enumerate(rb):
            sb = rshares[rshares["bucket"] == b]
            if sb.empty or sb["share"].sum() <= 0:
                continue
            per = rng.multinomial(rcounts[:, j], sb["share"].to_numpy() / sb["share"].sum())
            pool = self.run_pool.get(b, np.array([4.0]))
            for i, pid in enumerate(sb["rusher_id"]):
                k = per[:, i]
                e = reff_p.loc[(pid, b)] if (pid, b) in reff_p.index else None
                ypc = (e["ypp_s"] if e is not None else reff[b]["ypp"]) * reff[b]["m_ypp"] * P.sig_mult(team, opp, pid, "run").get(b, 1.0)
                yds, longest = _draw_sum_max(rng, k, pool, shift=ypc - pool.mean())
                if pid in rtd.index:
                    rate = shrink(rtd.loc[pid, "td"] / rtd.loc[pid, "n"], rtd.loc[pid, "n"],
                                  P.lg_run_td * P.priors.factor("off", team, "run_td"), 80)
                else:
                    rate = P.lg_run_td
                acc(pid, "carries", k)
                acc(pid, "rush_yds", yds)
                acc(pid, "rush_td", rng.binomial(k, min(rate * m_run_td, 0.5)))
                acc(pid, "longest_rush", longest, "max")

        for d in out.values():
            for s in OFFENSE_STATS:
                d.setdefault(s, np.zeros(n))
            d["rush_rec_yds"] = d["rush_yds"] + d["rec_yds"]
            d["pass_rush_yds"] = d["pass_yds"] + d["rush_yds"]
            d["rush_rec_td"] = d["rush_td"] + d["rec_td"]
            d["fantasy_ppr"] = (0.04 * d["pass_yds"] + 4 * d["pass_td"] - d["interceptions"]
                                + 0.1 * (d["rush_yds"] + d["rec_yds"]) + 6 * d["rush_rec_td"]
                                + d["receptions"])
        team_sim = {"plays": plays, "sacks": sacks, "interceptions": out.get(qb, {}).get("interceptions", np.zeros(n)),
                    "tackle_opps": runs + scr + team_comp + sacks,
                    "dropbacks": db, "pass_att": att, "runs": runs, "scrambles": scr,
                    "pass_td": sum(d.get("rec_td", 0) for d in out.values()),
                    "td": sum(d["rush_rec_td"] for d in out.values())}
        meta = {pid: (row.player, row.pos) for row in active_df.itertuples() for pid in [row.player_id]}
        return {"players": out, "meta": meta, "team": team_sim}, {"qb": qb}

    # ------------------------------------------------------------ kicker
    def kicker(self, team: str, opp: str, team_td: np.ndarray, week: int | None = None) -> dict | None:
        k = self.kickers
        if k.empty or team not in set(k["team"]):
            return None
        rng, n, P = self.rng, self.n, self.P
        last = k["week"].max()
        hl = P.cfg["weighting"]["half_life_weeks"]
        k = k.assign(w=0.5 ** ((last - k["week"]) / hl))
        tk = k[k["team"] == team]
        recent = tk[tk["week"] == tk["week"].max()].sort_values("fg_att", ascending=False)
        if recent.empty:
            return None
        pid, name = recent["player_id"].iloc[0], recent["player"].iloc[0]
        team_fga = np.average(tk.groupby("boxscore_id")["fg_att"].sum(),
                              weights=tk.groupby("boxscore_id")["w"].first())
        games = P.games.dropna(subset=["boxscore_id"])
        opp_games = games[(games["home"] == opp) | (games["away"] == opp)]["boxscore_id"]
        vs = k[k["boxscore_id"].isin(opp_games) & (k["team"] != opp)].groupby("boxscore_id")["fg_att"].sum()
        lg_fga = k.groupby(["boxscore_id", "team"])["fg_att"].sum().mean()
        lam = team_fga * (1 + P.dw * ((vs.mean() if len(vs) else lg_fga) / lg_fga - 1))
        lg_pct = k["fg_made"].sum() / max(k["fg_att"].sum(), 1)
        mine = k[k["player_id"] == pid]
        pct = shrink(mine["fg_made"].sum() / max(mine["fg_att"].sum(), 1), mine["fg_att"].sum(), lg_pct, 20)
        xp_pct = shrink(mine["xp_made"].sum() / max(mine["xp_att"].sum(), 1), mine["xp_att"].sum(),
                        k["xp_made"].sum() / max(k["xp_att"].sum(), 1), 30)
        if week is not None:
            # Field goals move with the drives: schedule and market yardage factors.
            a = P.adjustments(team, opp, week)
            lam *= a["sos"]["off_pts"] * a["sos"]["def_pts"] * a["ypp_factor"]
            pct = pct * (1 + 0.5 * (a["weather"]["fg"] - 1))  # the fg factor is for 40+ yard tries
        fga = rng.poisson(max(lam, 0.0), n)
        fgm = rng.binomial(fga, pct)
        xpa = np.round(team_td).astype(int)
        xpm = rng.binomial(xpa, xp_pct)
        return {"player_id": pid, "player": name, "pos": "K",
                "stats": {"fg_att": fga, "fg_made": fgm, "xp_made": xpm, "kicking_points": 3 * fgm + xpm}}

    # ------------------------------------------------------------ defense
    def defense(self, team: str, opp_team_sim: dict) -> list[dict]:
        d = self.defenders
        if d.empty or team not in set(d["team"]):
            return []
        P, rng = self.P, self.rng
        d = d[d["team"] == team]
        weeks = sorted(d["week"].unique())[-P.cfg["players"]["active_within_games"]:]
        active = set(d[d["week"].isin(weeks)]["player_id"])
        last = d["week"].max()
        d = d.assign(w=0.5 ** ((last - d["week"]) / P.cfg["weighting"]["half_life_weeks"]))
        tot = {s: (d[s] * d["w"]).sum() for s in DEFENSE_STATS}
        opps = P.p[P.p["defense"] == team]
        opps_w = (opps["w"] * (opps["is_run"] | opps["complete"].fillna(False).astype(bool)
                               | opps["is_sack"] | opps["play_type"].eq("scramble"))).sum()
        credits_per_opp = tot["tackles"] / max(opps_w, 1e-9)
        out = []
        for pid, g in d[d["player_id"].isin(active)].groupby("player_id"):
            share = {s: (g[s] * g["w"]).sum() / tot[s] if tot[s] else 0 for s in DEFENSE_STATS}
            stats = {
                "tackles": rng.poisson(share["tackles"] * credits_per_opp * opp_team_sim["tackle_opps"]),
                "sacks": rng.binomial(opp_team_sim["sacks"], min(share["sacks"], 1.0)),
                "def_int": rng.binomial(opp_team_sim["interceptions"].astype(int), min(share["def_int"], 1.0)),
            }
            out.append({"player_id": pid, "player": g["player"].iloc[-1], "pos": "DEF", "stats": stats})
        return out

    # ------------------------------------------------------------ week
    def run_week(self, week: int) -> pd.DataFrame:
        sched = self.P.games[self.P.games["week"] == week]
        rows = []
        for g in sched.itertuples():
            sims = {}
            for team, opp in ((g.home, g.away), (g.away, g.home)):
                sims[team], _ = self.offense(team, opp, week)
            for team, opp in ((g.home, g.away), (g.away, g.home)):
                s = sims[team]
                for pid, stats in s["players"].items():
                    name, pos = s["meta"].get(pid, (pid, ""))
                    rows += _summ(week, team, opp, pid, name, pos, stats)
                kk = self.kicker(team, opp, s["team"]["td"], week)
                if kk:
                    rows += _summ(week, team, opp, kk["player_id"], kk["player"], "K", kk["stats"])
                    pts = 6 * s["team"]["td"] + kk["stats"]["xp_made"] + 3 * kk["stats"]["fg_made"]
                else:
                    pts = 6.95 * s["team"]["td"]
                self.team_points[(team, opp)] = float(np.mean(pts))
                ts = s["team"]
                comp = {k: float(np.mean(ts[k])) for k in ("plays", "dropbacks", "pass_att", "runs", "sacks",
                                                            "interceptions", "td", "pass_td")}
                comp["rush_td"] = comp["td"] - comp["pass_td"]
                comp["fga"] = float(np.mean(kk["stats"]["fg_att"])) if kk else np.nan
                comp["fgm"] = float(np.mean(kk["stats"]["fg_made"])) if kk else np.nan
                comp["points"] = float(np.mean(pts))
                self.team_components[(team, opp)] = comp
                self.team_point_samples[(team, opp)] = pts
                for dp in self.defense(team, sims[opp]["team"]):
                    rows += _summ(week, team, opp, dp["player_id"], dp["player"], dp["pos"], dp["stats"])
        return pd.DataFrame(rows)


def _summ(week, team, opp, pid, name, pos, stats: dict) -> list[dict]:
    rows = []
    for stat, arr in stats.items():
        arr = np.asarray(arr, dtype=float)
        if stat in ("sacks_taken",) or not arr.any():
            continue
        q = np.percentile(arr, [10, 25, 50, 75, 90])
        rows.append({"week": week, "team": team, "opp": opp, "player_id": pid, "player": name,
                     "pos": pos, "stat": stat, "mean": arr.mean(), "p10": q[0], "p25": q[1],
                     "median": q[2], "p75": q[3], "p90": q[4],
                     "p_ge_1": (arr >= 1).mean(), "p_ge_2": (arr >= 2).mean(),
                     "_samples": arr})
    return rows


def first_td_probs(props: pd.DataFrame) -> pd.DataFrame:
    """P(first TD of the game) ≈ player's share of the game's expected TDs ×
    P(the game has a TD)."""
    t = props[props["stat"] == "rush_rec_td"].copy()
    if t.empty:
        return t
    t["game"] = t.apply(lambda r: "-".join(sorted([r["team"], r["opp"]])), axis=1)
    lam = t.groupby("game")["mean"].transform("sum")
    t["p_first_td"] = t["mean"] / lam * (1 - np.exp(-lam))
    return t[["player_id", "team", "p_first_td"]]


def apply_lines(props: pd.DataFrame, lines: pd.DataFrame) -> pd.DataFrame:
    """Add P(over)/P(under) for any (player, stat, line) you enter."""
    if lines is None or lines.empty:
        return props
    lines = lines.copy()
    lines["line"] = pd.to_numeric(lines["line"], errors="coerce")
    props = props.merge(lines[["player", "stat", "line"]], on=["player", "stat"], how="left")
    has = props["line"].notna()
    props.loc[has, "p_over"] = [float((s > l).mean()) for s, l in zip(props.loc[has, "_samples"], props.loc[has, "line"])]
    props.loc[has, "p_under"] = [float((s < l).mean()) for s, l in zip(props.loc[has, "_samples"], props.loc[has, "line"])]
    return props


def wide_means(props: pd.DataFrame) -> pd.DataFrame:
    cols = OFFENSE_STATS + DERIVED + KICKER_STATS + DEFENSE_STATS
    w = props.pivot_table(index=["week", "team", "opp", "player", "pos", "player_id"],
                          columns="stat", values="mean", fill_value=0.0).reset_index()
    for c in cols:
        if c not in w:
            w[c] = 0.0
    td = props[props["stat"] == "rush_rec_td"][["player_id", "team", "p_ge_1"]].rename(
        columns={"p_ge_1": "anytime_td"})
    w = w.merge(td, on=["player_id", "team"], how="left").fillna({"anytime_td": 0.0})
    ft = first_td_probs(props)
    if not ft.empty:
        w = w.merge(ft, on=["player_id", "team"], how="left").fillna({"p_first_td": 0.0})
    keep = ["week", "team", "opp", "player", "pos", "player_id"] + cols + ["anytime_td", "p_first_td"]
    w = w[[c for c in keep if c in w]]
    return w.round(3).sort_values(["team", "pass_yds", "fantasy_ppr"], ascending=[True, False, False])
