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
    "receptions": [2, 3, 4, 5, 6, 7, 8],
    "carries": [6, 8, 10, 12, 14, 15, 17, 20],
    "rec_yds": [15, 20, 25, 30, 40, 50, 60, 70, 80, 100],
    "rush_yds": [20, 25, 40, 50, 60, 70, 80, 100],
    "pass_yds": [150, 175, 200, 225, 250, 275, 300],
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
    w = r["wide"]
    status = _status(r.get("injuries"), week)
    pg = r["tables"]["player_games"]
    pg = pg[pg["week"] < week]
    totals = r["totals"].set_index("team")["proj_points"] if "proj_points" in r["totals"] else pd.Series(dtype=float)
    rows = []
    for x in w[w["pos"].isin(["WR", "TE", "RB"]) & (w["anytime_td"] >= floor)].itertuples():
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
        vol = f"{x.targets:.1f} targets" + (f", {x.carries:.1f} carries" if x.carries >= 3 else "")
        pros.append(f"projected {vol}")
        if tp >= 25:
            pros.append(f"team projected {tp:.0f} pts")
        elif tp <= 19:
            cons.append(f"team projected only {tp:.0f} pts")
        if tr == "up":
            pros.append("usage rising")
        elif tr == "down":
            cons.append("usage falling")
        scored = sum(v > 0 for v in tds)
        (pros if scored >= len(tds) / 2 else cons).append(f"scored in {scored} of {len(tds)} games")
        if status.get(x.player_id) == "Questionable":
            cons.append("Questionable on the injury report")
        if x.anytime_td < 0.40:
            cons.append("under 40%: a real long shot on its own")
        score = x.anytime_td + 0.02 * (tr == "up") - 0.02 * (tr == "down") - 0.04 * (status.get(x.player_id) == "Questionable")
        rows.append({"player": x.player, "player_id": x.player_id, "team": x.team, "opp": x.opp, "pos": x.pos,
                     "game": " @ ".join(sorted([x.team, x.opp])), "stat": "anytime TD", "k": 1, "p": float(x.anytime_td),
                     "median": np.nan, "last": tds[-5:], "trend": tr, "score": score, "pros": pros, "cons": cons})
    c = pd.DataFrame(rows)
    return c.sort_values("score", ascending=False) if len(c) else c


def build(c: pd.DataFrame, n_parlays: int, legs: int, max_uses: int = 2, per_stat: int = 3,
          max_shared: int | None = None) -> list[pd.DataFrame]:
    """Greedy, diversified: one leg per game per parlay, at most ``per_stat``
    legs of one stat type, each player in at most ``max_uses`` parlays, best
    remaining legs first."""
    uses: dict = {}
    out, prev = [], []
    max_shared = legs // 2 if max_shared is None else max_shared
    for i in range(n_parlays):
        picked, games, stats = [], set(), {}
        pool = c.assign(adj=c["score"] - 0.06 * c["player_id"].map(uses).fillna(0)).sort_values("adj", ascending=False)
        for x in pool.itertuples():
            if len(picked) == legs:
                break
            if x.game in games or uses.get(x.player_id, 0) >= max_uses or stats.get(x.stat, 0) >= per_stat:
                continue
            mine = {c.at[i, "player_id"] for i in picked} | {x.player_id}
            if any(len(mine & p) > max_shared for p in prev):
                continue
            stats[x.stat] = stats.get(x.stat, 0) + 1
            picked.append(x.Index)
            games.add(x.game)
            uses[x.player_id] = uses.get(x.player_id, 0) + 1
        if len(picked) == legs:
            out.append(c.loc[picked])
            prev.append(set(c.loc[picked, "player_id"]))
    return out


def _leg(x) -> str:
    what = f"Anytime TD" if x.stat == "anytime TD" else f"{x.k}+ {LABEL[x.stat]}"
    med = "" if pd.isna(x.median) else f", model median {x.median:.0f}"
    last = ", ".join(f"{v:g}" for v in x.last)
    return (f"- **{x.player}** ({x.team} {x.pos} vs {x.opp}) **{what}**: {x.p:.0%} (fair {american(x.p)}){med}; last games: {last}\n"
            f"  - ➕ {'; '.join(x.pros) or '—'}\n  - ➖ {'; '.join(x.cons) or '—'}")


def report(week: int, parlays: list, tds: list, form: dict) -> str:
    L = [f"# Week {week} long-shot parlays", "",
         "Legs are alternate milestones (\"X+\") the model gives about 70%+ after calibration, on stat types the model has graded "
         "well this season, one leg per game so they're close to independent. Probabilities assume independence; "
         "books add extra margin to parlays, so compare the payout with the fair odds before betting.", ""]
    if form:
        L.append("Stat form this season (model lean right %): " + ", ".join(
            f"{s.replace('_', ' ')} {a:.0%} ({n})" for s, (a, n) in sorted(form.items(), key=lambda z: -z[1][0])))
        L.append("")
    for name, group in (("10-leg parlays", parlays), ("7-leg anytime-TD parlays", tds)):
        L += [f"## {name}", ""]
        if not group:
            L += ["Not enough qualifying legs yet (projections or injury news missing).", ""]
        for i, p in enumerate(group, 1):
            joint = float(np.prod(p["p"]))
            L += [f"### #{i}: all hit {joint:.2%} (fair +{100 * (1 - joint) / joint:,.0f})", ""]
            L += [_leg(x) for x in p.itertuples()] + [""]
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
    md = report(week, build(c, 5, 10) if len(c) else [], build(td, 5, 7, per_stat=7) if len(td) else [], form)
    out = paths["out"] / "parlays" / f"week_{week:02d}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md)
    log(f"parlays: {len(c)} milestone legs, {len(td)} TD legs -> {out}")
    return out
