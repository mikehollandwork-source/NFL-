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


def td_candidates(r: dict, cfg: dict, week: int, floor: float = 0.30,
                  positions: tuple = ("WR", "TE", "RB")) -> pd.DataFrame:
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
    for x in w[w["pos"].isin(list(positions)) & (w["p_td"] >= floor)].itertuples():
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


def first_td(r: dict, td: pd.DataFrame, used: set, legs: int = 4):
    """First-TD-scorer legs. Each player's expected TDs = -ln(1 - calibrated
    anytime chance) (blended TD model where available, calibrated simulation
    otherwise); first-TD chance = his share of the game's expected TDs
    (offense plus ~6% defense / special teams) x chance the game has a TD.
    One leg per game. Not backtested."""
    w = r["wide"][r["wide"]["anytime_td"] > 0][["player_id", "team", "opp", "anytime_td"]].copy()
    blended = dict(zip(td["player_id"], td["p"]))
    w["p"] = w["player_id"].map(blended).fillna(w["anytime_td"])
    w["lam"] = -np.log(1 - w["p"].clip(upper=0.995))
    w["game"] = [" @ ".join(sorted([a, b])) for a, b in zip(w["team"], w["opp"])]
    lam_game = w.groupby("game")["lam"].sum() / 0.94
    c = td[~td["player_id"].isin(used)].copy()
    if c.empty:
        return [], c
    lam_i = -np.log(1 - c["p"].clip(upper=0.995))
    L = c["game"].map(lam_game)
    c["p_first"] = lam_i / L * (1 - np.exp(-L))
    P = c.sort_values("p_first", ascending=False).drop_duplicates("game").head(legs)
    if len(P) < legs:
        return [], c
    used |= set(P["player_id"])
    return [P], c


def qb_td(r: dict, cfg: dict, week: int, used: set, legs: int = 4):
    """QB rushing-TD legs (how books grade "QB anytime TD"): blended TD model,
    which counts a QB's carries, red-zone and goal-line runs."""
    q = td_candidates(r, cfg, week, floor=0.05, positions=("QB",))
    if q.empty:
        return [], q
    q = q[~q["player_id"].isin(used)].sort_values("p", ascending=False).drop_duplicates("game").head(legs)
    if len(q) < legs:
        return [], q
    used |= set(q["player_id"])
    return [q], q


def _simple_md(title: str, note: str, par: list, col: str, what: str) -> list[str]:
    L = [f"## {title}", "", note, ""]
    if not par:
        return L + ["Not enough qualifying legs.", ""]
    P = par[0]
    j = float(np.prod(P[col]))
    L += [f"### {len(P)} legs, all hit {j:.2%} (fair +{100 * (1 - j) / j:,.0f})", ""]
    for x in P.itertuples():
        L.append(f"- **{x.player}** ({x.team} {x.pos} vs {x.opp}) **{what}**: {getattr(x, col):.0%} "
                 f"(fair {american(getattr(x, col))}; anytime TD {x.p:.0%})\n"
                 f"  - ➕ {'; '.join(x.pros) or '—'}\n  - ➖ {'; '.join(x.cons) or '—'}")
    return L + [""]


def jackpot(r: dict, cfg: dict, week: int, form: dict, used: set, target_payout: float = 25000.0,
            max_legs: int = 60, per_game: int = 4):
    """$1 -> ~$25k at fair odds: up to 25 realistic legs (calibrated ~62%+,
    same realism filters as the regular milestone legs), from players in no
    other parlay, at most two legs per game."""
    # The one exception to the no-overlap rule: the jackpot may reuse players from other parlays.
    c = candidates(r, cfg, week, form, target=0.62)
    if c.empty:
        return [], c
    c = c.sort_values("score", ascending=False)
    # Lean on the stat types the model has been right on: carries uncapped, unproven ones capped
    cap = {"completions": 6, "pass_yds": 5, "rec_yds": 6, "receptions": 4}
    picked, per, nstat = [], {}, {}
    for x in c.itertuples():
        if len(picked) >= max_legs or (picked and np.prod(c.loc[picked, "p"]) <= 1 / (1 + target_payout)):
            break
        if per.get(x.game, 0) >= per_game or nstat.get(x.stat, 0) >= cap.get(x.stat, 99):
            continue
        picked.append(x.Index)
        per[x.game] = per.get(x.game, 0) + 1
        nstat[x.stat] = nstat.get(x.stat, 0) + 1
    P = c.loc[picked]
    return ([P] if len(P) else []), P


def _career(season: int, before_week: int | None = None) -> pd.DataFrame:
    from .nflverse import Downloader, season_files
    from .td_model import RAW
    d = Downloader(RAW, log=lambda *a: None)
    for y in range(season - 8, season + 1):      # a fresh checkout (e.g. GitHub Actions) lacks older seasons
        try:
            d.get(season_files(y)["player_week"])
        except Exception:
            pass
    fs = sorted(RAW.glob("stats_player_week_*.csv.gz"))
    cols = ["player_id", "season", "week", "season_type", "team", "position", "carries", "rushing_yards",
            "targets", "receptions", "receiving_yards", "attempts"]
    out = []
    for f in fs:
        if int(f.name.split("_")[-1][:4]) < season - 8:
            continue
        d = pd.read_csv(f, usecols=lambda c: c in cols, low_memory=False)
        out.append(d[d["season_type"] == "REG"])
    car = pd.concat(out, ignore_index=True)
    if before_week is not None:   # backtests: nothing from the week being predicted or later
        car = car[(car["season"] < season) | (car["week"] < before_week)]
    return car


BIG_ROLE = {"RB": ("carries", 15), "WR": ("targets", 8), "TE": ("targets", 7)}
ROLE_STATS = {"RB": [("rush_yds", "rushing_yards"), ("carries", "carries")],
              "WR": [("rec_yds", "receiving_yards"), ("receptions", "receptions")],
              "TE": [("rec_yds", "receiving_yards"), ("receptions", "receptions")]}


def backups(r: dict, cfg: dict, week: int, used: set, n_parlays: int = 2, legs: int = 4, asof: bool = False):
    """Backups who'd fill a big role if the starter ahead of them misses time.
    Starter / backup = 1st / 2nd in projected workload at the position (RB
    carries; WR, TE targets). Starter risk = share of his team's games he
    missed in 2025-26 (floor 5% for an in-game injury), raised to 25%+ if he is
    Questionable. The backup must have had a big-role game before (RB 15+
    carries, WR 8+ targets, TE 7+ targets); the leg is the number he reached in
    60% of those games. Chance = sim chance in his normal role + P(starter out)
    x his hit rate in big-role games."""
    w = r["wide"]
    status = _status(r.get("injuries"), week)
    car = _career(int(cfg["season"]), before_week=week if asof else None)
    recent = car[car["season"] >= int(cfg["season"]) - 1]
    gp = recent.groupby("player_id").size()
    season_g = recent.groupby("season")["week"].nunique()          # games played so far each season
    seasons_in = recent.groupby("player_id")["season"].unique()    # only seasons he was in the league
    props = r["props"][r["props"]["_samples"].notna()].rename(columns={"_samples": "samples"})
    rows = []
    for (team, pos), g in w[w["pos"].isin(list(BIG_ROLE))].groupby(["team", "pos"]):
        key = "carries" if pos == "RB" else "targets"
        g = g.sort_values(key, ascending=False)
        if len(g) < 2:
            continue
        st, bk = g.iloc[0], g.iloc[1 if pos != "WR" else min(3, len(g) - 1)]
        if pos == "WR":   # the 4th WR is the one who steps into a top-3 role
            bk = g.iloc[min(3, len(g) - 1)]
        if bk["player_id"] in used or status.get(bk["player_id"]) in ("Out", "Doubtful", "IR"):
            continue
        if st["player_id"] in gp.index:
            possible = sum(int(season_g.get(y, 0)) for y in seasons_in[st["player_id"]])
            miss = 1 - min(1.0, gp[st["player_id"]] / max(possible, 1))
        else:
            miss = 0.05
        # Past absences cluster in long injuries, so cap the weekly risk unless he's on this week's report
        p_out = min(max(miss, 0.05), 0.30)
        if status.get(st["player_id"]) == "Questionable":
            p_out = max(p_out, 0.25)
        stat_col, thr = BIG_ROLE[pos]
        hist = car[car["player_id"] == bk["player_id"]]
        big = hist[hist[stat_col] >= thr]
        if len(big) < 2:      # must have done it more than once
            continue
        for stat, col in ROLE_STATS[pos]:
            k_raw = float(np.percentile(big[col], 40))   # reached in ~60% of his big-role games
            ks = [k for k in MILESTONES[stat] if k <= k_raw]
            if not ks:
                continue
            k = ks[-1]
            if k < {"carries": 12, "rush_yds": 50, "receptions": 4, "rec_yds": 40}[stat]:
                continue          # not a "massive role" number
            p_role = float((big[col] >= k).mean())
            pr = props[(props["player_id"] == bk["player_id"]) & (props["stat"] == stat)]
            p_sim = calibrate(float((np.asarray(pr["samples"].iloc[0]) >= k).mean()), cfg, stat, "over") if len(pr) else 0.0
            p = p_sim + (1 - p_sim) * p_out * p_role
            rows.append({"player": bk["player"], "player_id": bk["player_id"], "team": team, "opp": bk["opp"],
                         "pos": pos, "game": " @ ".join(sorted([team, bk["opp"]])), "stat": stat, "k": k, "p": p,
                         "p_sim": p_sim, "p_out": p_out, "p_role": p_role, "starter": st["player"],
                         "n_big": len(big), "best": float(big[col].max()), "median": np.nan, "last": [],
                         "score": p_out * p_role,
                         "pros": [f"{len(big)} career big-role games ({stat_col} {thr}+), reached {k}+ in {p_role:.0%} of them, best {big[col].max():.0f}",
                                  f"{st['player']} ahead of him: {p_out:.0%} chance he misses or leaves"
                                  + (" (Questionable)" if status.get(st['player_id']) == 'Questionable' else "")],
                         "cons": [f"only {p_sim:.0%} in his normal backup role: needs the injury"]})
    c = pd.DataFrame(rows)
    if c.empty:
        return [], c
    c = c.sort_values("score", ascending=False).drop_duplicates("player_id")
    out = []
    for _ in range(n_parlays):
        pick, games = [], set()
        for x in c[~c["player_id"].isin(used)].itertuples():
            if x.game in games:
                continue
            pick.append(x.Index)
            games.add(x.game)
            if len(pick) >= legs:
                break
        if len(pick) < 2:
            break
        P = c.loc[pick]
        used |= set(P["player_id"])
        out.append(P)
    return out, c


def _backup_md(par: list) -> list[str]:
    L = ["## Backup / injury parlays", "",
         "Backups who would step into a big role if the starter ahead of them misses or leaves the game. Each has done "
         "it before (career big-role games). Leg = the number he reached in ~60% of those games; chance = his normal "
         "backup-role chance + P(starter out) x his big-role hit rate. These mostly need an injury to cash.", ""]
    if not par:
        return L + ["No backup parlay qualified.", ""]
    for i, P in enumerate(par, 1):
        j = float(np.prod(P["p"]))
        L += [f"### Backup #{i}: {len(P)} legs, all hit {j:.2%} (fair +{100 * (1 - j) / j:,.0f})", ""]
        for x in P.itertuples():
            L.append(f"- **{x.player}** ({x.team} {x.pos} vs {x.opp}, behind {x.starter}) **{x.k}+ {LABEL[x.stat]}**: "
                     f"{x.p:.0%}\n  - ➕ {'; '.join(x.pros)}\n  - ➖ {'; '.join(x.cons)}")
        L.append("")
    return L


def _jackpot_md(par: list) -> list[str]:
    L = ["## Jackpot parlay ($1 → ~$25k at fair odds)", "",
         "Career-floor legs can't get there: they hit ~95-98% each, so 25,000-to-1 would take ~200 legs. This uses "
         "realistic ~62%+ legs (same filters as the milestone parlays: cleared in 3+ of the last 5, normal role, "
         "projection not above what he has done), as many as it takes, up to four per game. The only parlay allowed "
         "to reuse players from the others. Books cap leg counts and their margin compounds per leg, so the real "
         "payout will be well below fair.", ""]
    if not par:
        return L + ["Not enough unused legs.", ""]
    P = par[0]
    j = float(np.prod(P["p"]))
    L += [f"### {len(P)} legs, all hit {j:.4%} (fair ${(1 - j) / j:,.0f} on $1)", ""]
    L += [f"- **{x.player}** ({x.team} {x.pos} vs {x.opp}) **{x.k}+ {LABEL[x.stat]}**: {x.p:.0%}" for x in P.itertuples()]
    return L + [""]


def combos(sources: list[tuple[str, pd.DataFrame, str]]) -> list[pd.DataFrame]:
    """One leg from each source parlay per combo. Each leg is used once, so the
    number of combos = the smallest source's leg count. Legs are dealt snake
    style (best legs spread evenly) so the combos have similar chances."""
    srcs = [(name, df.sort_values(col, ascending=False).reset_index(drop=True), col)
            for name, df, col in sources if df is not None and len(df)]
    if not srcs:
        return []
    n = min(len(df) for _, df, _ in srcs)
    out = [[] for _ in range(n)]
    for j, (name, df, col) in enumerate(srcs):
        order = range(n) if j % 2 == 0 else range(n - 1, -1, -1)
        for combo, i in zip(order, range(n)):
            x = df.iloc[i]
            what = ("First TD scorer" if col == "p_first" else "Anytime TD" if x["stat"] == "anytime TD"
                    else f"{x['k']}+ {LABEL[x['stat']]}")
            out[combo].append({"source": name, "player": x["player"], "team": x["team"], "opp": x["opp"],
                               "pos": x["pos"], "what": what, "p": float(x[col])})
    return [pd.DataFrame(c) for c in out]


def _combos_md(cs: list) -> list[str]:
    L = ["## Combo parlays (one leg from each parlay)", "",
         "One leg from each milestone, anytime-TD, breakout, role-surge and first-TD parlay (backup/injury, two-TD, QB-TD "
         "and the jackpot left out). Each leg is used in only one combo, so the count is capped by the smallest source "
         "parlay. Chances multiply the legs as if independent; legs from the same game (e.g. a breakout leg and a TD on "
         "that team) tend to move together, so the true chance is a bit higher.", ""]
    if not cs:
        return L + ["No combos built.", ""]
    for i, c in enumerate(cs, 1):
        j = float(np.prod(c["p"]))
        L += [f"### Combo #{i}: {len(c)} legs, all hit {j:.5%} (fair ${(1 - j) / j:,.0f} on $1)", ""]
        L += [f"- **{x.player}** ({x.team} {x.pos} vs {x.opp}) **{x.what}**: {x.p:.0%}  _(from {x.source})_"
              for x in c.itertuples()]
        L.append("")
    return L


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


def run(cfg: dict, paths: dict, week: int | None = None, log=print, once: bool = False) -> Path | None:
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
    out = paths["out"] / "parlays" / f"week_{week:02d}.md"
    if once and out.exists():
        log(f"parlays for week {week} already built ({out}); skipping")
        return None
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
    qb_p, _ = qb_td(r, cfg, week, used)
    first_p, _ = first_td(r, td, used) if len(td) else ([], pd.DataFrame())
    bk_p, _ = backups(r, cfg, week, used)
    parl = build(c, 5, 10, used=used) if len(c) else []
    tdp = build(td, 5, 7, per_stat=7, used=used) if len(td) else []
    jp_p, _ = jackpot(r, cfg, week, form, used)
    md = report(week, parl, tdp, form, td, brk, [
        _surge_md(surge_p, surge), _two_td_md(two_p, two_c),
        _simple_md("First TD scorer parlay", "One leg per game: the player most likely to score his game's first "
                   "touchdown (simulation share of the game's TDs x chance the game has one, rescaled by the blended TD "
                   "model). Extreme long shot; this market is not backtested.", first_p, "p_first", "First TD scorer"),
        _simple_md("QB touchdown parlay", "Quarterback rushing TDs (how books grade \"QB anytime TD\"), one per game, "
                   "from the blended TD model (QB carries, red-zone and goal-line runs, scoring environment).",
                   qb_p, "p", "Anytime TD (rushing)"),
        _backup_md(bk_p), _jackpot_md(jp_p),
        _combos_md(combos(
            [(f"milestone #{i}", P, "p") for i, P in enumerate(parl, 1)]
            + [(f"anytime-TD #{i}", P, "p") for i, P in enumerate(tdp, 1)]
            + [(f"breakout {b['offense']} vs {b['defense']}", b["legs"], "p") for b in brk[0]]
            + [("role surge", P.drop_duplicates("player_id"), "p") for P in surge_p]
            + [("first TD", P, "p_first") for P in first_p]))])
    out = paths["out"] / "parlays" / f"week_{week:02d}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md)
    log(f"parlays: {len(c)} milestone legs, {len(td)} TD legs -> {out}")
    return out


# First-TD probabilities from the share-of-expected-TDs method run high at the top:
# 2025 wk 4-18 + 2026 wk 3-6 (6,005 player-games), predicted 17% -> 12.7% actual,
# 22.5% -> 16%; below 10% it is about right. Each game's top pick scored first 11.9%
# (predicted 16.4%). Above the knee, keep 45% of the excess.
FIRST_TD_KNEE, FIRST_TD_SLOPE = 0.10, 0.45


def _first_td_adj(p):
    p = np.asarray(p, float)
    return np.where(p > FIRST_TD_KNEE, FIRST_TD_KNEE + FIRST_TD_SLOPE * (p - FIRST_TD_KNEE), p)


def board_parlays(r: dict, cfg: dict, week: int, games: set | None = None,
                  n_first: int = 10, first_legs: int = 4, n_any: int = 5, any_legs: int = 7) -> list[dict]:
    """$1 touchdown tickets for the prop board: ``n_first`` first-TD parlays
    (one leg per game, no player in two tickets, best legs first) and ``n_any``
    anytime-TD parlays (the regular builder). ``games`` limits legs to games
    not yet kicked off."""
    out = []
    td = td_candidates(r, cfg, week, floor=0.15)
    if games is not None and len(td):
        td = td[td["game"].isin({" @ ".join(sorted(g.split(" @ "))) for g in games})]
    if td.empty:
        return out
    w = r["wide"][r["wide"]["anytime_td"] > 0][["player_id", "team", "opp", "anytime_td"]].copy()
    blended = dict(zip(td["player_id"], td["p"]))
    w["p"] = w["player_id"].map(blended).fillna(w["anytime_td"])
    w["lam"] = -np.log(1 - w["p"].clip(upper=0.995))
    w["game"] = [" @ ".join(sorted([a, b])) for a, b in zip(w["team"], w["opp"])]
    lam_game = w.groupby("game")["lam"].sum() / 0.94
    c = td.copy()
    L = c["game"].map(lam_game)
    c["p_raw"] = -np.log(1 - c["p"].clip(upper=0.995)) / L * (1 - np.exp(-L))
    c["p_first"] = _first_td_adj(c["p_raw"])
    c = c.sort_values("p_first", ascending=False)
    used: set = set()
    for i in range(n_first):
        pool = c[~c["player_id"].isin(used)].drop_duplicates("game")
        # spread the slate: each game appears in about the same number of tickets
        if len(pool) < first_legs:
            break
        P = pool.head(first_legs) if i == 0 else pool.assign(
            k=pool["game"].map(lambda g: sum(g in t for t in [x["games"] for x in out]))
        ).sort_values(["k", "p_first"], ascending=[True, False]).head(first_legs).sort_values("p_first", ascending=False)
        used |= set(P["player_id"])
        out.append({"kind": "First TD", "games": set(P["game"]), "p": float(np.prod(P["p_first"])),
                    "legs": [{"player": x.player, "team": x.team, "pos": x.pos, "game": x.game, "what": "first TD",
                              "p": round(float(x.p_first), 3), "note": (x.pros[0] if x.pros else "")} for x in P.itertuples()]})
    for P in build(td, n_any, any_legs, per_stat=any_legs):
        out.append({"kind": "Anytime TD", "games": set(P["game"]), "p": float(np.prod(P["p"])),
                    "legs": [{"player": x.player, "player_id": x.player_id, "team": x.team, "pos": x.pos, "game": x.game,
                              "stat": "anytime_td", "what": "anytime TD",
                              "p": round(float(x.p), 3), "note": (x.pros[0] if x.pros else "")} for x in P.itertuples()]})
    for t in out:
        t["games"] = sorted(t["games"])
        t["fair"] = round(1 / t["p"]) if t["p"] > 0 else None
    return out


# Against real market lines (Kalshi closes, 2026 weeks 2-6) only the carries lean carries signal:
# carries hit 0.508 + 0.64 x (p - 0.5) (272 lines); every other stat ~0.54 whatever the model's
# confidence (2,021 lines; leans the model put at 70%+ hit 46%). Same-game legs use those rates.
SGP_REAL = {"carries": (0.508, 0.64)}
SGP_OTHER = 0.54
SGP_STATS = {"carries": 0, "completions": 1, "pass_yds": 1, "rec_yds": 1, "receptions": 1}


def sgp_tickets(r: dict, lean: pd.DataFrame, cfg: dict, legs: int = 3, min_p: float = 0.55) -> list[dict]:
    """One same-game parlay per game on posted lines: rush-attempt leans first
    (the only prop the model reads better than the market), then the strongest
    other leans, one leg per player. Each leg's chance is its measured hit
    rate against real lines; same-team legs are combined through the
    simulations (a team's players share each simulated game; the two
    offenses are independent)."""
    props = r["props"][r["props"]["_samples"].notna()]
    smp = {(pid, st): np.asarray(v, float) for pid, st, v in zip(props["player_id"], props["stat"], props["_samples"])}
    skip = r.get("no_qb_history", set())
    L = lean[lean["stat"].isin(list(SGP_STATS)) & (lean["p_cal"] >= min_p) & ~lean["team"].isin(skip)].copy()
    L["pri"] = L["stat"].map(SGP_STATS)
    a, b = SGP_REAL["carries"]
    L["p_real"] = np.where(L["stat"] == "carries", a + b * (L["p_cal"] - 0.5), SGP_OTHER)
    out = []
    for g, x in L.groupby("game"):
        x = x.sort_values(["pri", "p_real", "p_cal"], ascending=[True, False, False]).drop_duplicates("player_id").head(legs)
        if len(x) < legs:
            continue
        masks, scale, rows = {}, 1.0, []
        for y in x.itertuples():
            s = smp.get((y.player_id, y.stat))
            if s is None:
                break
            hit = s > y.line if y.side == "over" else s < y.line
            masks[y.team] = hit if y.team not in masks else (masks[y.team] & hit)
            scale *= y.p_real / max(float(hit.mean()), 1e-6)
            rows.append({"player": y.player, "player_id": y.player_id, "team": y.team, "pos": y.pos, "game": g,
                         "stat": y.stat, "side": y.side, "line": float(y.line),
                         "what": f"{y.side} {y.line:g} {y.stat.replace('_', ' ').replace('carries', 'rush attempts')}",
                         "p": round(float(y.p_real), 3),
                         "note": f"model {y.p_cal:.0%}, median {y.model_median:.1f}"})
        if len(rows) < legs:
            continue
        joint = float(np.prod([m.mean() for m in masks.values()])) * scale
        out.append({"kind": "SGP", "games": [g], "p": joint, "fair": round(1 / joint, 2), "legs": rows,
                    "carries": int((x["stat"] == "carries").sum())})
    return sorted(out, key=lambda t: (-t["carries"], -t["p"]))
