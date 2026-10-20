"""Long-shot parlay builder: high-probability alternate milestones ("X+")
from the model's simulations, restricted to the stat types that have graded
best this season, spread across games so legs are close to independent.

Hot streaks: rising *usage* (targets / carries) repeats week to week in our
tests; streaks in *results* (yards, TDs) do not. Usage trend is used for
selection; recent milestone hit rates are shown as context only.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .paper import calibrate
from .picks import usage_trend
from .picks import STATS
from .sim import calibrate_td

MILESTONES = {
    "receptions": [2, 3, 4, 5, 6, 7, 8, 9, 10, 12],
    "carries": [6, 8, 10, 12, 14, 15, 17, 20],
    "rec_yds": [15, 20, 25, 30, 40, 50, 60, 70, 80, 100, 125, 150],
    "rush_yds": [20, 25, 40, 50, 60, 70, 80, 100, 125, 150],
    "pass_yds": [150, 175, 200, 225, 250, 275, 300, 325, 350, 400],
    "completions": [12, 15, 18, 20, 22, 25],
}
LABEL = {"receptions": "receptions", "carries": "rush attempts", "rec_yds": "receiving yds",
         "rush_yds": "rushing yds", "pass_yds": "passing yds", "completions": "completions"}


def american(p: float) -> str:
    if p <= 0 or p >= 1:
        return "n/a"
    return f"{-100 * p / (1 - p):+.0f}" if p >= 0.5 else f"+{100 * (1 - p) / p:.0f}"


def stat_form(paper_dir: Path) -> dict:
    """Season-to-date accuracy of the model's lean on every posted line, by stat."""
    f = paper_dir / "calls_ledger.csv"
    if not f.exists():
        return {}
    c = pd.read_csv(f)
    c = c[c["result"].isin(["right", "wrong"])]
    return {s: ((x["result"] == "right").mean(), len(x)) for s, x in c.groupby("stat")}


def _status(inj: pd.DataFrame | None, week: int) -> dict:
    if inj is None or inj.empty:
        return {}
    i = inj[inj["week"] == week].dropna(subset=["report_status"])
    return dict(zip(i["player_id"], i["report_status"]))


def candidates(r: dict, cfg: dict, week: int, form: dict, target: float = 0.70) -> pd.DataFrame:
    props = r["props"]
    pg = r["tables"]["player_games"]
    pg = pg[pg["week"] < week]
    status = _status(r.get("injuries"), week)
    totals = r["totals"].set_index("team")["proj_points"] if "proj_points" in r["totals"] else pd.Series(dtype=float)
    excluded = set(cfg.get("paper", {}).get("exclude_stats", []))
    rows = []
    sel = props[props["stat"].isin(list(MILESTONES)) & props["_samples"].notna()].rename(columns={"_samples": "samples"})
    for x in sel.itertuples():
        if x.stat in excluded or status.get(x.player_id) in ("Out", "Doubtful", "IR"):
            continue
        acc, n = form.get(x.stat, (0.5, 0))
        if n >= 15 and acc < 0.5:
            continue  # stat type the model has been losing on this season
        smp = np.asarray(x.samples, dtype=float)
        best = None
        for k in MILESTONES[x.stat]:
            pc = calibrate(float((smp >= k).mean()), cfg, x.stat, "over")
            if pc >= target:
                best = (k, pc)
        if best is None:
            continue
        k, pc = best
        col, ucol, fam = STATS[x.stat]
        h = pg[(pg["player_id"] == x.player_id) & (pg["team"] == x.team)].sort_values("week")
        h = h[h[ucol] > 0]
        if len(h) < 3:
            continue
        vals = h[col].tolist()
        last = vals[-5:]
        hit = sum(v >= k for v in last)
        # Realism: he must have cleared it in most recent games, be playing a normal
        # role lately, and the projection can't run far above what he's actually done.
        recent_weeks = sorted(pg[pg["team"] == x.team]["week"].unique())[-4:]
        played = h[h["week"].isin(recent_weeks)]
        if hit < max(3, int(np.ceil(0.6 * len(last)))) or len(played) < 3:
            continue
        if float(np.median(smp)) > 1.3 * float(np.median(last)) + (2 if x.stat in ("receptions", "carries", "completions") else 10):
            continue
        tr = usage_trend(h.set_index("week")[ucol])["dir"] if fam != "qb" else "QB"
        pros, cons = [], []
        if tr == "up":
            pros.append(f"{'targets' if ucol == 'targets' else 'carries'} rising")
        elif tr == "down":
            cons.append(f"{'targets' if ucol == 'targets' else 'carries'} falling")
        if hit >= len(last) - 1:
            pros.append(f"cleared {k}+ in {hit} of last {len(last)}")
        elif hit <= len(last) // 2:
            cons.append(f"cleared {k}+ in only {hit} of last {len(last)}")
        tp = float(totals.get(x.team, np.nan))
        if tp >= 25:
            pros.append(f"team projected {tp:.0f} pts")
        elif tp <= 18:
            cons.append(f"team projected only {tp:.0f} pts")
        if x.stat in ("rec_yds", "rush_yds", "pass_yds"):
            cons.append("yardage: one big play swings it")
        if status.get(x.player_id) == "Questionable":
            cons.append("Questionable on the injury report")
        if n >= 15:
            (pros if acc >= 0.55 else cons).append(f"model {acc:.0%} right on {x.stat.replace('_', ' ')} this season")
        score = pc + 0.02 * (tr == "up") - 0.03 * (tr == "down") + 0.03 * (acc - 0.5) \
            - 0.04 * (status.get(x.player_id) == "Questionable")
        rows.append({"player": x.player, "player_id": x.player_id, "team": x.team, "opp": x.opp, "pos": x.pos,
                     "game": " @ ".join(sorted([x.team, x.opp])), "stat": x.stat, "k": k, "p": pc,
                     "median": float(np.median(smp)), "last": last, "trend": tr, "score": score,
                     "pros": pros, "cons": cons})
    c = pd.DataFrame(rows)
    if c.empty:
        return c
    # one milestone per player (his strongest), so legs aren't two bets on one stat line
    return c.sort_values("score", ascending=False).drop_duplicates("player_id")


def td_candidates(r: dict, cfg: dict, week: int, floor: float = 0.30) -> pd.DataFrame:
    from .td_model import blend, current_features, predict
    w = r["wide"].copy()
    feat = current_features(int(cfg["season"]), week, r["tables"]["games"])
    ps = predict(feat)
    fe = feat.set_index("pid") if len(feat) else pd.DataFrame()
    lg_env = float(feat["env"].median()) if len(feat) else np.nan
    w["p_stats"] = w["player_id"].map(ps)
    w["p_td"] = np.where(w["p_stats"].notna(), blend(w["anytime_td"], w["p_stats"].fillna(0.5)), w["anytime_td"])
    status = _status(r.get("injuries"), week)
    pg = r["tables"]["player_games"]
    pg = pg[pg["week"] < week]
    totals = r["totals"].set_index("team")["proj_points"] if "proj_points" in r["totals"] else pd.Series(dtype=float)
    rows = []
    for x in w[w["pos"].isin(["WR", "TE", "RB"]) & (w["p_td"] >= floor)].itertuples():
        if status.get(x.player_id) in ("Out", "Doubtful", "IR"):
            continue
        h = pg[(pg["player_id"] == x.player_id) & (pg["team"] == x.team)].sort_values("week")
        if len(h) < 3:
            continue
        tds = (h["rec_td"] + h["rush_td"]).tolist()
        ucol = "rush_att" if x.pos == "RB" else "targets"
        tr = usage_trend(h.set_index("week")[ucol])["dir"]
        tp = float(totals.get(x.team, np.nan))
        pros, cons = [], []
        f = fe.loc[x.player_id] if len(fe) and x.player_id in fe.index else None
        if isinstance(f, pd.DataFrame):
            f = f.iloc[0]
        touches = x.targets + x.carries
        (pros if touches >= 12 else cons if touches < 7 else pros).append(
            f"volume {x.targets:.1f} targets + {x.carries:.1f} carries projected")
        if f is not None:
            rz = f["m_rz_tgt"] + f["m_rz_car"]
            gl = f["m_i10_tgt"] + f["m_i5_car"]
            (pros if rz >= 2 else cons if rz < 1 else pros).append(f"{rz:.1f} red-zone touches/game, {gl:.1f} inside the 10")
            if f["m_ez_tgt"] >= 0.6:
                pros.append(f"{f['m_ez_tgt']:.1f} end-zone targets/game")
            if pd.notna(f["env"]) and pd.notna(lg_env):
                (pros if f["env"] >= lg_env * 1.1 else cons if f["env"] <= lg_env * 0.9 else pros).append(
                    f"scoring environment {f['env']:.1f} TDs/game (team scored + opp allowed; median {lg_env:.1f})")
        if tr == "up":
            pros.append("usage rising")
        elif tr == "down":
            cons.append("usage falling")
        if status.get(x.player_id) == "Questionable":
            cons.append("Questionable on the injury report")
        if x.p_td < 0.40:
            cons.append("under 40%: a real long shot on its own")
        if pd.notna(x.p_stats) and abs(x.p_stats - x.anytime_td) >= 0.12:
            cons.append(f"simulation {x.anytime_td:.0%} vs stats model {x.p_stats:.0%} disagree")
        score = x.p_td + 0.02 * (tr == "up") - 0.02 * (tr == "down") - 0.04 * (status.get(x.player_id) == "Questionable")
        rows.append({"player": x.player, "player_id": x.player_id, "team": x.team, "opp": x.opp, "pos": x.pos,
                     "game": " @ ".join(sorted([x.team, x.opp])), "stat": "anytime TD", "k": 1, "p": float(x.p_td),
                     "median": np.nan, "last": tds[-5:], "trend": tr, "score": score, "pros": pros, "cons": cons})
    c = pd.DataFrame(rows)
    return c.sort_values("score", ascending=False) if len(c) else c


def build(c: pd.DataFrame, n_parlays: int, legs: int, max_uses: int = 1, per_stat: int = 3,
          max_shared: int | None = None, min_payout: float = 10.0, max_legs: int = 16,
          used: set | None = None) -> list[pd.DataFrame]:
    """Greedy, diversified: one leg per game per parlay, at most ``per_stat``
    legs of one stat type, each player in at most one parlay (no shared legs,
    across calls via ``used``), best remaining legs first. A parlay stops as
    soon as it reaches +``min_payout`` x fair; if the strong legs run out
    first it is dropped rather than padded with weaker legs."""
    used = set() if used is None else used     # players already in any parlay (shared across calls)
    uses: dict = {p: max_uses for p in used}
    out, prev = [], []
    max_shared = legs // 2 if max_shared is None else max_shared
    for i in range(n_parlays):
        picked, games, stats = [], set(), {}
        pool = c.assign(adj=c["score"] - 0.06 * c["player_id"].map(uses).fillna(0)).sort_values("adj", ascending=False)
        def joint():
            return float(np.prod(c.loc[picked, "p"])) if picked else 1.0
        cap = per_stat
        for x in pool.itertuples():
            # stop at the leg count once the parlay pays at least +1000 fair (all-hit <= 1/11)
            if joint() <= 1 / (1 + min_payout) or len(picked) >= max_legs:
                break
            if len(picked) >= legs:
                cap = per_stat + 2   # beyond the usual length a stat type may repeat a bit more
            if x.game in games or uses.get(x.player_id, 0) >= max_uses or stats.get(x.stat, 0) >= cap:
                continue
            mine = {c.at[i, "player_id"] for i in picked} | {x.player_id}
            if any(len(mine & p) > max_shared for p in prev):
                continue
            stats[x.stat] = stats.get(x.stat, 0) + 1
            picked.append(x.Index)
            games.add(x.game)
            uses[x.player_id] = uses.get(x.player_id, 0) + 1
        if picked and joint() <= 1 / (1 + min_payout):
            out.append(c.loc[picked])
            used |= set(c.loc[picked, "player_id"])
            prev.append(set(c.loc[picked, "player_id"]))
        else:   # not enough strong legs left: give the players back, don't force weaker ones in
            for j in picked:
                uses[c.at[j, "player_id"]] -= 1
    return out


BREAKOUT_STATS = {"QB": ["pass_yds"], "WR": ["rec_yds", "receptions"], "TE": ["rec_yds", "receptions"],
                  "RB": ["rush_yds", "rec_yds"]}


def worst_defenses(r: dict, cfg: dict, n: int = 2) -> pd.DataFrame:
    """Schedule-adjusted defense ratings (points allowed per game, pass and run
    yards per play allowed, each corrected for the offenses faced), combined
    as the average z-score; highest = most vulnerable."""
    from .ratings import Schedule
    t = Schedule(r["plays"], r["tables"]["games"], cfg).table().set_index("team")
    cols = [c for c in ("def_points_adj", "def_pass_adj", "def_run_adj") if c in t]
    z = (t[cols] - t[cols].mean()) / t[cols].std()
    t["vuln"] = z.mean(axis=1)
    for c in cols:
        t[c.replace("_adj", "_rank")] = t[c].rank(ascending=False).astype(int)   # 1 = worst
    return t.sort_values("vuln", ascending=False)


def breakout(r: dict, cfg: dict, week: int, used: set, n_def: int = 2, min_payout: float = 10.0,
             max_legs: int = 5) -> tuple[list[dict], pd.DataFrame]:
    """One same-game long shot per vulnerable defense: the offense facing it,
    players at "big game" milestones (above their 75th-percentile outcome) they
    have actually reached this season. All-hit chance is read from the joint
    simulations (same-game legs rise and fall together), scaled by each leg's
    over-calibration."""
    d = worst_defenses(r, cfg)
    sched = r["tables"]["games"]
    sched = sched[sched["week"] == week]
    opp_of = {**dict(zip(sched["home"], sched["away"])), **dict(zip(sched["away"], sched["home"]))}
    props = r["props"][r["props"]["_samples"].notna()].rename(columns={"_samples": "samples"})
    pg = r["tables"]["player_games"]
    pg = pg[pg["week"] < week]
    status = _status(r.get("injuries"), week)
    out, skipped = [], []
    unreliable = set(r.get("no_qb_history", set()))
    for dfn in [t for t in d.index if t in opp_of]:
        if len(out) >= n_def:
            break
        off = opp_of[dfn]
        dr = d.loc[dfn]
        if off in unreliable:
            skipped.append(f"{dfn} (opponent {off}'s starting QB has no passes this season, so its passing game can't be projected)")
            continue
        weeks = sorted(pg[pg["team"] == off]["week"].unique())[-4:]
        legs = []
        for x in props[(props["team"] == off)].itertuples():
            if x.stat not in BREAKOUT_STATS.get(x.pos, []) or x.player_id in used:
                continue
            if status.get(x.player_id) in ("Out", "Doubtful", "IR", "Questionable"):
                continue
            col, ucol, fam = STATS[x.stat]
            h = pg[(pg["player_id"] == x.player_id) & (pg["team"] == off)].sort_values("week")
            if len(h[h["week"].isin(weeks)]) < 3:
                continue
            smp = np.asarray(x.samples, dtype=float)
            p75 = float(np.percentile(smp, 75))
            ks = [k for k in MILESTONES[x.stat] if k >= p75]
            if not ks:
                continue
            k = ks[0]
            vals = h[col].tolist()
            if max(vals) < k:          # never done it: not a realistic ceiling
                continue
            tr = usage_trend(h.set_index("week")[ucol])["dir"] if fam != "qb" else "QB"
            if tr == "down":
                continue
            p_raw = float((smp >= k).mean())
            p_cal = calibrate(p_raw, cfg, x.stat, "over")
            legs.append({"player": x.player, "player_id": x.player_id, "team": off, "opp": dfn, "pos": x.pos,
                         "stat": x.stat, "k": k, "p": p_cal, "p_raw": p_raw, "median": float(np.median(smp)),
                         "samples": smp >= k, "last": vals[-5:], "trend": tr,
                         "hits": sum(v >= k for v in vals), "n": len(vals)})
        if not legs:
            skipped.append(f"{dfn} (no realistic ceiling legs on {off})")
            continue
        # A breakout is yards: QB passing yards first, then yardage legs, catches only as a fallback
        pri = {"pass_yds": 0, "rec_yds": 1, "rush_yds": 1, "receptions": 2}
        L = pd.DataFrame(legs)
        L["pri"] = L["stat"].map(pri)
        L = L.sort_values(["pri", "p"], ascending=[True, False]).drop_duplicates("player_id")
        L = L.sort_values(["pri", "p"], ascending=[True, False])
        picked, mask, scale = [], None, 1.0
        for x in L.itertuples():
            m = x.samples if mask is None else (mask & x.samples)
            picked.append(x.Index)
            mask, scale = m, scale * (x.p / max(x.p_raw, 1e-6))
            if float(mask.mean()) * scale <= 1 / (1 + min_payout) or len(picked) >= max_legs:
                break
        joint = float(mask.mean()) * scale
        if joint > 1 / (1 + min_payout):
            skipped.append(f"{dfn} (not enough realistic ceiling legs on {off} to reach +1000)")
            continue
        P = L.loc[picked]
        used |= set(P["player_id"])
        out.append({"defense": dfn, "offense": off, "rating": dr, "legs": P, "joint": joint,
                    "indep": float(np.prod(P["p"]))})
    d.attrs["skipped"] = skipped
    return out, d


def _breakout_md(b: list, d: pd.DataFrame) -> list[str]:
    L = ["## Breakout parlays (vs the two most vulnerable defenses)", "",
         "Defense vulnerability = schedule-adjusted points allowed, pass yds/play and run yds/play allowed "
         "(rank 1 = worst of 32). Legs are \"big game\" milestones above each player's 75th-percentile "
         "projection that he has reached at least once this season, usage not falling. All legs come from "
         "the same game, so they hit together when the defense collapses; the chance below is read from the "
         "joint simulations, not multiplied.", ""]
    top = d.head(5)
    L.append("Most vulnerable defenses: " + ", ".join(
        f"{t} (pts #{int(r.get('def_points_rank', 0))}, pass #{int(r.get('def_pass_rank', 0))}, run #{int(r.get('def_run_rank', 0))})"
        for t, r in top.iterrows()))
    L.append("")
    for sk in d.attrs.get("skipped", []):
        L.append(f"- Skipped {sk}")
    if d.attrs.get("skipped"):
        L.append("")
    if not b:
        L += ["No breakout parlay qualified (not enough realistic ceiling legs).", ""]
    for i, x in enumerate(b, 1):
        dr = x["rating"]
        j = x["joint"]
        L += [f"### Breakout #{i}: {x['offense']} vs {x['defense']}: {len(x['legs'])} legs, all hit {j:.1%} "
              f"(fair +{100 * (1 - j) / j:,.0f}; would be {x['indep']:.1%} if the legs were independent)", "",
              f"{x['defense']} defense: points allowed #{int(dr.get('def_points_rank', 0))} worst, pass yds/play "
              f"#{int(dr.get('def_pass_rank', 0))}, run yds/play #{int(dr.get('def_run_rank', 0))} (schedule-adjusted).", ""]
        for y in x["legs"].itertuples():
            last = ", ".join(f"{v:g}" for v in y.last)
            L.append(f"- **{y.player}** ({y.team} {y.pos}) **{y.k}+ {LABEL[y.stat]}**: {y.p:.0%} alone (model median "
                     f"{y.median:.0f}); reached it {y.hits} of {y.n} games this season; last games: {last}\n"
                     f"  - ➕ ceiling game vs a bottom defense; {'usage rising' if y.trend == 'up' else 'steady role'}\n"
                     f"  - ➖ needs a big game: well above his projection")
        L.append("")
    return L


def two_td_prob(p_any):
    """P(2+ TDs) from the anytime-TD chance, treating TDs as a Poisson count
    (2021-25 out of sample this matched a direct 2+ TD model; log-loss
    0.1614 vs 0.1612). Above 25% it ran hot (41% predicted, 33% actual),
    so the top end is pulled in."""
    p = np.clip(np.asarray(p_any, float), 1e-6, 0.999)
    lam = -np.log(1 - p)
    p2 = 1 - np.exp(-lam) * (1 + lam)
    return np.where(p2 > 0.25, 0.25 + 0.6 * (p2 - 0.25), p2)


def two_td(td: pd.DataFrame, used: set, min_payout: float = 10.0, max_legs: int = 4):
    c = td.copy()
    if c.empty:
        return [], c
    c["p2"] = two_td_prob(c["p"])
    c = c.sort_values("p2", ascending=False)
    pool = c[~c["player_id"].isin(used)]
    picked, games = [], set()
    for x in pool.itertuples():
        if picked and np.prod(c.loc[picked, "p2"]) <= 1 / (1 + min_payout):
            break
        if x.game in games or len(picked) >= max_legs:
            continue
        picked.append(x.Index)
        games.add(x.game)
    P = c.loc[picked]
    if not len(P) or float(np.prod(P["p2"])) > 1 / (1 + min_payout):
        return [], c
    used |= set(P["player_id"])
    return [P], c


def role_surge(r: dict, cfg: dict, week: int, cands: pd.DataFrame, td: pd.DataFrame, used: set,
               min_payout: float = 10.0, max_legs: int = 8):
    """Players whose role jumped in their last two games vs before (snap share
    +15 pts with touches +35%, or touches +60%), where the model still
    projects the bigger role this week (so a returning starter rules it out).
    Milestone legs he cleared in BOTH of the last two games, plus anytime-TD
    legs for the two surge players most likely to score."""
    pg = r["tables"]["player_games"]
    pg = pg[pg["week"] < week].copy()
    if "off_pct" in pg and pg["off_pct"].max() > 1.5:
        pg["off_pct"] = pg["off_pct"] / 100
    pg["touch"] = pg["targets"] + pg["rush_att"]
    wide = r["wide"].set_index("player_id")
    status = _status(r.get("injuries"), week)
    surge = {}
    for (pid, team), h in pg[pg["pos"].isin(["WR", "TE", "RB"])].groupby(["player_id", "team"]):
        h = h.sort_values("week")
        if len(h) < 4 or pid in used or status.get(pid) in ("Out", "Doubtful", "IR"):
            continue
        last, before = h.tail(2), h.iloc[:-2]
        t1, t0 = last["touch"].mean(), before["touch"].mean()
        s1, s0 = last["off_pct"].mean(), before["off_pct"].mean()
        big = (s1 - s0 >= 0.15 and t1 >= 1.35 * t0 and t1 - t0 >= 3) or (t1 >= 1.6 * t0 and t1 - t0 >= 4)
        if not big or pid not in wide.index:
            continue
        w = wide.loc[pid]
        if isinstance(w, pd.DataFrame):
            w = w.iloc[0]
        proj = float(w.get("targets", 0) + w.get("carries", 0))
        if proj < 0.8 * t1:            # model doesn't see the bigger role continuing
            continue
        surge[pid] = {"snap0": s0, "snap1": s1, "t0": t0, "t1": t1, "proj": proj, "last2": last}
    if not surge:
        return [], surge
    # Own legs from the simulations: the highest milestone he cleared in BOTH games of
    # the new role that the model (calibrated) still gives 65%+.
    props = r["props"][r["props"]["_samples"].notna()].rename(columns={"_samples": "samples"})
    form_bad = {s_ for s_, (a, n) in stat_form(Path(cfg.get("_paper_dir", ""))).items() if n >= 15 and a < 0.5} \
        if cfg.get("_paper_dir") else set()
    excluded = set(cfg.get("paper", {}).get("exclude_stats", [])) | form_bad
    rows = []
    for x in props[props["player_id"].isin(list(surge)) & props["stat"].isin(list(MILESTONES))].itertuples():
        if x.stat in excluded:
            continue
        col = STATS[x.stat][0]
        last2 = surge[x.player_id]["last2"][col].tolist()
        smp = np.asarray(x.samples, dtype=float)
        best = None
        for k in MILESTONES[x.stat]:
            pc = calibrate(float((smp >= k).mean()), cfg, x.stat, "over")
            if pc >= 0.65 and min(last2) >= k:
                best = (k, pc)
        if best:
            rows.append({"player": x.player, "player_id": x.player_id, "team": x.team, "opp": x.opp, "pos": x.pos,
                         "game": " @ ".join(sorted([x.team, x.opp])), "stat": x.stat, "k": best[0], "p": best[1],
                         "median": float(np.median(smp)), "last": last2, "trend": "up", "score": best[1],
                         "pros": [f"cleared {best[0]}+ in both games of the new role"], "cons": []})
    M = pd.DataFrame(rows)
    M = M.sort_values("p", ascending=False).drop_duplicates("player_id") if len(M) else M
    T = td[td["player_id"].isin(list(surge))].sort_values("p", ascending=False).head(2)
    if len(T) < 2:   # TD legs come from the full projection list, not just the 30%+ TD board
        T = _surge_td(r, list(surge), T)
    P = pd.concat([T, M], ignore_index=True)
    picked = []
    for i in P.index:
        picked.append(i)
        if len(picked) >= max_legs or (len(picked) >= len(T) + 1 and np.prod(P.loc[picked, "p"]) <= 1 / (1 + min_payout)):
            break
    P = P.loc[picked]
    if float(np.prod(P["p"])) > 1 / (1 + min_payout):
        return [], surge
    used |= set(P["player_id"])
    return [P], surge


def _surge_td(r: dict, pids: list, T: pd.DataFrame) -> pd.DataFrame:
    """Top up to two TD legs from the full projections (players under the 30% TD board floor)."""
    have = set(T["player_id"]) if len(T) else set()
    w = r["wide"][r["wide"]["player_id"].isin(pids) & ~r["wide"]["player_id"].isin(have)]
    add = [{"player": x.player, "player_id": x.player_id, "team": x.team, "opp": x.opp, "pos": x.pos,
            "game": " @ ".join(sorted([x.team, x.opp])), "stat": "anytime TD", "k": 1, "p": float(x.anytime_td),
            "median": np.nan, "last": [], "trend": "up", "score": float(x.anytime_td), "pros": [],
            "cons": ["TD chance under 30%"]}
           for x in w.sort_values("anytime_td", ascending=False).head(2 - len(have)).itertuples()]
    return pd.concat([T, pd.DataFrame(add)], ignore_index=True) if add else T


def _surge_md(par: list, surge: dict) -> list[str]:
    L = ["## Role-surge parlay", "",
         "Players whose role jumped in their last two games (snap share +15 pts with touches +35%, or touches +60%) "
         "and whose bigger role the model still projects this week; milestone legs each cleared in both of those games, "
         "plus anytime TDs for the two surge players most likely to score.", ""]
    if surge:
        L.append("Role surges found: " + ", ".join(
            f"{v['last2']['player'].iloc[-1]} ({v['last2']['team'].iloc[-1]}: {v['t0']:.1f} → {v['t1']:.1f} touches/game, "
            f"snaps {v['snap0']:.0%} → {v['snap1']:.0%})" for v in surge.values()))
        L.append("")
    if not par:
        L += ["No role-surge parlay qualified at +1000 without padding.", ""]
        return L
    P = par[0]
    j = float(np.prod(P["p"]))
    L += [f"### {len(P)} legs, all hit {j:.1%} (fair +{100 * (1 - j) / j:,.0f})", ""]
    for x in P.itertuples():
        s = surge.get(x.player_id, {})
        role = f"role: {s.get('t0', 0):.1f} → {s.get('t1', 0):.1f} touches/game, snaps {s.get('snap0', 0):.0%} → {s.get('snap1', 0):.0%}"
        L.append(_leg(x).replace("  - ➕ ", f"  - ➕ {role}; ", 1))
    return L + [""]


def _two_td_md(par: list, c: pd.DataFrame) -> list[str]:
    L = ["## Two-touchdown parlay", "",
         "2+ TD chance comes from each player's anytime-TD chance (simulation blended with the stats-driven TD model). "
         "Tested 2021-25: carries drive multi-TD games more than targets, and dual-threat usage or past TD rate add "
         "nothing beyond that, so goal-line backs on high-scoring teams lead.", "",
         "| # | Player | vs | 2+ TDs | Fair | Anytime | Why |", "|---|---|---|---|---|---|---|"]
    for i, x in enumerate(c.head(10).itertuples(), 1):
        L.append(f"| {i} | {x.player} ({x.team} {x.pos}) | {x.opp} | {x.p2:.0%} | {american(x.p2)} | {x.p:.0%} | {(x.pros or ['—'])[0]} |")
    L.append("")
    if not par:
        return L + ["No two-TD parlay qualified.", ""]
    P = par[0]
    j = float(np.prod(P["p2"]))
    L += [f"### {len(P)} legs, all hit {j:.1%} (fair +{100 * (1 - j) / j:,.0f})", ""]
    for x in P.itertuples():
        L.append(f"- **{x.player}** ({x.team} {x.pos} vs {x.opp}) **2+ TDs**: {x.p2:.0%} (fair {american(x.p2)}; anytime {x.p:.0%})\n"
                 f"  - ➕ {'; '.join(x.pros) or '—'}\n  - ➖ {'; '.join(x.cons) or '—'}")
    return L + [""]


def _leg(x) -> str:
    what = f"Anytime TD" if x.stat == "anytime TD" else f"{x.k}+ {LABEL[x.stat]}"
    med = "" if pd.isna(x.median) else f", model median {x.median:.0f}"
    last = ", ".join(f"{v:g}" for v in x.last)
    return (f"- **{x.player}** ({x.team} {x.pos} vs {x.opp}) **{what}**: {x.p:.0%} (fair {american(x.p)}){med}; last games: {last}\n"
            f"  - ➕ {'; '.join(x.pros) or '—'}\n  - ➖ {'; '.join(x.cons) or '—'}")


def report(week: int, parlays: list, tds: list, form: dict, td_top: pd.DataFrame | None = None,
           brk: tuple | None = None, extra: list | None = None) -> str:
    L = [f"# Week {week} long-shot parlays", "",
         "Every parlay is at least +1000 at fair odds and no player appears in more than one parlay; a parlay stops once it reaches +1000, and if the strong legs run out it is left out rather than padded. Legs are alternate milestones (\"X+\") the model gives about 70%+ after calibration, cleared in at least 3 of the player's last 5 games, with a projection not far above what he has actually done; TD legs blend the simulation with the stats-driven TD model (volume, red-zone and end-zone usage, scoring environment), on stat types the model has graded "
         "well this season, one leg per game so they're close to independent. Probabilities assume independence; "
         "books add extra margin to parlays, so compare the payout with the fair odds before betting.", ""]
    if form:
        L.append("Stat form this season (model lean right %): " + ", ".join(
            f"{s.replace('_', ' ')} {a:.0%} ({n})" for s, (a, n) in sorted(form.items(), key=lambda z: -z[1][0])))
        L.append("")
    if td_top is not None and len(td_top):
        L += ["## Top anytime-TD picks", "", "| # | Player | Team | vs | TD chance | Fair | Main pro | Main con |",
              "|---|---|---|---|---|---|---|---|"]
        for i, x in enumerate(td_top.sort_values("p", ascending=False).head(15).itertuples(), 1):
            L.append(f"| {i} | {x.player} | {x.team} {x.pos} | {x.opp} | {x.p:.0%} | {american(x.p)} | "
                     f"{(x.pros or ['—'])[0]} | {(x.cons or ['—'])[0]} |")
        L.append("")
    for name, group in (("Long-shot parlays (milestones)", parlays), ("Anytime-TD parlays", tds)):
        L += [f"## {name}", ""]
        if not group:
            L += ["Not enough qualifying legs yet (projections or injury news missing).", ""]
        for i, p in enumerate(group, 1):
            joint = float(np.prod(p["p"]))
            L += [f"### #{i}: {len(p)} legs, all hit {joint:.2%} (fair +{100 * (1 - joint) / joint:,.0f})", ""]
            L += [_leg(x) for x in p.itertuples()] + [""]
    if brk is not None:
        L += _breakout_md(*brk)
    for block in extra or []:
        L += block
    return "\n".join(L)


def run(cfg: dict, paths: dict, week: int | None = None, log=print) -> Path | None:
    from .build import load_season
    from .pipeline import run_week
    t = load_season(paths["db"])
    if week is None:
        # next week with a game not yet played (a finished game whose stats aren't posted doesn't count)
        today = pd.Timestamp.now(tz="America/New_York").strftime("%Y-%m-%d")
        pend = t["games"][t["games"]["boxscore_id"].isna() & (t["games"]["date"].astype(str) >= today)]
        if pend.empty:
            return None
        week = int(pend["week"].min())
    r = run_week(t, cfg, paths, week)
    form = stat_form(paths["out"] / "paper")
    c = candidates(r, cfg, week, form)
    td = td_candidates(r, cfg, week)
    used: set = set()
    cfg = {**cfg, "_paper_dir": str(paths["out"] / "paper")}
    # Specialty parlays first (they need specific players), then the regular ones from who's left
    brk = breakout(r, cfg, week, used)
    surge_p, surge = role_surge(r, cfg, week, c, td, used)
    two_p, two_c = two_td(td, used) if len(td) else ([], pd.DataFrame())
    parl = build(c, 5, 10, used=used) if len(c) else []
    tdp = build(td, 5, 7, per_stat=7, used=used) if len(td) else []
    md = report(week, parl, tdp, form, td, brk, [_surge_md(surge_p, surge), _two_td_md(two_p, two_c)])
    out = paths["out"] / "parlays" / f"week_{week:02d}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md)
    log(f"parlays: {len(c)} milestone legs, {len(td)} TD legs -> {out}")
    return out
