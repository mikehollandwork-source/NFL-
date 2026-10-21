"""Rebuild every parlay type for past weeks using only data available before
each week, grade them against the box scores, and pay $1 per parlay.

Prices: yardage / reception / carries legs at the Kalshi closing price for
that exact "X+" market (cached; fetched slowly). TD legs and legs without a
Kalshi market: ESTIMATED book price = model chance + 4 pts (a typical
single-leg margin), reported separately.
"""
import json, sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
from nfl_proj import parlays as PL                      # noqa: E402
from nfl_proj.build import load_season                  # noqa: E402
from nfl_proj.cli import _paths, load_cfg               # noqa: E402
from nfl_proj.odds import norm_name                     # noqa: E402
from nfl_proj.picks import STATS                        # noqa: E402
from nfl_proj.pipeline import run_week                  # noqa: E402
import kalshi_backtest as KB                             # noqa: E402

SER = {"receptions": "KXNFLREC", "rec_yds": "KXNFLRECYDS", "pass_yds": "KXNFLPASSYDS",
       "rush_yds": "KXNFLRSHYDS", "carries": "KXNFLRSHATT"}


def kalshi_index():
    idx = {}
    for stat, s in SER.items():
        for m in KB.settled(s):
            if m.get("floor_strike") is None:
                continue
            name = norm_name((m.get("yes_sub_title") or "").split(":")[0].strip())
            date = m["event_ticker"].split("-")[1][:7]
            idx[(name, stat, int(float(m["floor_strike"]) + 0.5), date)] = (s, m["ticker"])
    return idx


def first_td_scorers(season):
    p = pd.read_csv(ROOT / "data/raw/nflverse" / f"play_by_play_{season}.csv.gz", low_memory=False,
                    usecols=["game_id", "week", "touchdown", "td_player_id", "game_seconds_remaining", "season_type"])
    p = p[(p["touchdown"] == 1) & (p["season_type"] == "REG") & p["td_player_id"].notna()]
    p = p.sort_values(["game_id", "game_seconds_remaining"], ascending=[True, False])
    return set(p.groupby("game_id").head(1)["td_player_id"]), set(p["game_id"])


def main(weeks=range(2, 7)):
    cfg = load_cfg(ROOT / "config/projection.toml")
    paths = _paths(cfg)
    t = load_season(paths["db"])
    g = t["games"]
    pg = t["player_games"]
    firsts, _ = first_td_scorers(int(cfg["season"]))
    kidx = kalshi_index()
    kick = {}
    for x in g.itertuples():
        ts = int(pd.Timestamp(f"{x.date} {x.gametime or '13:00'}", tz="America/New_York").tz_convert("UTC").timestamp())
        kick[(x.week, x.home)] = kick[(x.week, x.away)] = (ts, pd.Timestamp(x.date).strftime("%y%b%d").upper())
    tickets = []
    for w in weeks:
        r = run_week(t, cfg, paths, w, asof=True, log=lambda *a: None)
        form = {}   # no graded weeks before the ones being tested
        c = PL.candidates(r, cfg, w, form)
        td = PL.td_candidates(r, cfg, w)
        used = set()
        brk, _ = PL.breakout(r, cfg, w, used)
        sp, _ = PL.role_surge(r, cfg, w, c, td, used)
        tp, _ = PL.two_td(td, used) if len(td) else ([], None)
        qp, _ = PL.qb_td(r, cfg, w, used)
        fp, _ = PL.first_td(r, td, used) if len(td) else ([], None)
        bp, _ = PL.backups(r, cfg, w, used, asof=True)
        mp = PL.build(c, 5, 10, used=used) if len(c) else []
        ap = PL.build(td, 5, 7, per_stat=7, used=used) if len(td) else []
        jp, _ = PL.jackpot(r, cfg, w, form, used)
        groups = ([("milestone", P, "p") for P in mp] + [("anytime TD", P, "p") for P in ap]
                  + [("breakout", b["legs"], "p") for b in brk] + [("role surge", P, "p") for P in sp]
                  + [("two TD", P, "p2") for P in tp] + [("first TD", P, "p_first") for P in fp]
                  + [("QB TD", P, "p") for P in qp] + [("backup", P, "p") for P in bp] + [("jackpot", P, "p") for P in jp])
        cs = PL.combos([(f"m{i}", P, "p") for i, P in enumerate(mp)] + [(f"t{i}", P, "p") for i, P in enumerate(ap)]
                       + [(f"b{i}", b["legs"], "p") for i, b in enumerate(brk)] + [("s", P.drop_duplicates("player_id"), "p") for P in sp]
                       + [("f", P, "p_first") for P in fp])
        pw = pg[pg["week"] == w]
        for kind, P, col in groups:
            tickets.append(grade(kind, w, P, col, pw, firsts, kidx, kick))
        for C in cs:
            C = C.rename(columns={"what": "what"})
            tickets.append(grade_combo(w, C, pw, r, firsts, kidx, kick))
        done = pd.DataFrame([x for x in tickets if x])
        print(f"week {w}: {len(done[done.week == w])} parlays built", flush=True)
    T = pd.DataFrame([x for x in tickets if x])
    T.to_csv(ROOT / "output/2026/parlay_backtest.csv", index=False)
    report(T)


def leg_result(stat, k, pid, team, pw, firsts):
    a = pw[(pw["player_id"] == pid) & (pw["team"] == team)]
    if a.empty:
        return None                       # did not play: books void the leg; we drop it
    if stat == "anytime TD":
        return float(a["rec_td"].sum() + a["rush_td"].sum() >= 1)
    if stat == "two TD":
        return float(a["rec_td"].sum() + a["rush_td"].sum() >= 2)
    if stat == "first TD":
        return float(pid in firsts)
    col = STATS[stat][0]
    return float(a[col].sum() >= k)


def leg_price(stat, k, player, team, week, p, kidx, kick):
    key = (norm_name(player), stat, int(k))
    ts, date = kick.get((week, team), (None, None))
    hit = kidx.get(key + (date,)) if date else None
    if hit and ts:
        cp = KB.close_price(hit[0], hit[1], ts)
        if cp and cp.get("mid") and 0.02 < cp["mid"] < 0.98:
            return min(cp["mid"] + 0.01, 0.99), "kalshi"
    return min(p + 0.04, 0.97), "estimated"


def grade(kind, w, P, col, pw, firsts, kidx, kick):
    res, prices, src = [], [], []
    for x in P.itertuples():
        stat = {"two TD": "two TD", "first TD": "first TD"}.get(kind, x.stat)
        k = getattr(x, "k", 1)
        rr = leg_result(stat, k, x.player_id, x.team, pw, firsts)
        if rr is None:
            continue
        pr, s = leg_price(stat, k, x.player, x.team, w, float(getattr(x, col)), kidx, kick)
        res.append(rr); prices.append(pr); src.append(s)
    if not res:
        return None
    hit = all(res)
    pay = 1 / np.prod(prices)
    return {"week": w, "type": kind, "legs": len(res), "hit": hit, "legs_won": int(sum(res)), "payout": pay,
            "ret": pay if hit else 0.0, "all_kalshi": all(s == "kalshi" for s in src),
            "model_p": float(np.prod([getattr(x, col) for x in P.itertuples()]))}


def grade_combo(w, C, pw, r, firsts, kidx, kick):
    ids = r["wide"].set_index(["player", "team"])["player_id"].to_dict()
    res, prices, src = [], [], []
    for x in C.itertuples():
        pid = ids.get((x.player, x.team))
        if x.what == "First TD scorer":
            stat, k = "first TD", 1
        elif x.what == "Anytime TD":
            stat, k = "anytime TD", 1
        else:
            k, rest = x.what.split("+ ", 1)
            stat = {v: s for s, v in PL.LABEL.items()}[rest]
            k = int(k)
        rr = leg_result(stat, k, pid, x.team, pw, firsts)
        if rr is None:
            continue
        pr, s = leg_price(stat, k, x.player, x.team, w, float(x.p), kidx, kick)
        res.append(rr); prices.append(pr); src.append(s)
    if not res:
        return None
    hit = all(res)
    pay = 1 / np.prod(prices)
    return {"week": w, "type": "combo", "legs": len(res), "hit": hit, "legs_won": int(sum(res)), "payout": pay,
            "ret": pay if hit else 0.0, "all_kalshi": all(s == "kalshi" for s in src), "model_p": float(np.prod(C["p"]))}


def report(T):
    pd.set_option("display.width", 200)
    print(f"\n{len(T)} parlays, $1 each: {int(T.hit.sum())} hit, returned ${T.ret.sum():,.2f} on ${len(T)} → ROI {T.ret.sum() / len(T) - 1:+.1%}")
    by = T.groupby("type").agg(parlays=("hit", "size"), hits=("hit", "sum"), legs=("legs", "mean"),
                               avg_legs_won=("legs_won", "mean"), model_hit=("model_p", "sum"),
                               returned=("ret", "sum"), avg_payout=("payout", "mean"))
    by["roi"] = by["returned"] / by["parlays"] - 1
    print(by.round(2).to_string())
    print("\nby week:"); print(T.groupby("week").agg(parlays=("hit", "size"), hits=("hit", "sum"), returned=("ret", "sum")).round(2).to_string())
    k = T[T.all_kalshi]
    if len(k):
        print(f"\nparlays priced entirely at Kalshi closes: {len(k)}, {int(k.hit.sum())} hit, ROI {k.ret.sum() / len(k) - 1:+.1%}")
    print("\nwinning tickets:"); print(T[T.hit][["week", "type", "legs", "payout"]].round(1).to_string(index=False))


if __name__ == "__main__":
    main()
