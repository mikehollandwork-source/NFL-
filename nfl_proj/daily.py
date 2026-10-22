"""Daily grading: the morning after each game day, win / loss on everything the
system put out for that day's games.

- Paper bets (qualifying bets locked before kickoff)
- Money list (carries vs Kalshi, real stakes)
- Every lean on a posted line (right / wrong by stat)
- Board same-game parlays and anytime-TD tickets: the last version shown on
  the board before the ticket's first leg kicked off. A ticket spanning later
  days is graded when its last game is final.

Writes output/<season>/daily/<date>.md; a date already graded is skipped.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from .odds import norm_name
from .picks import STATS


def _price_dec(odds: float) -> float:
    return 1 + (odds / 100 if odds > 0 else 100 / -odds)


def _actual(pw: pd.DataFrame, pid: str, stat: str):
    a = pw[pw["player_id"] == pid]
    if a.empty:
        return None
    if stat == "anytime_td":
        return float(a["rec_td"].sum() + a["rush_td"].sum())
    return float(a[STATS[stat][0]].sum())


def _leg_won(v, stat, side=None, line=None):
    if v is None:
        return None                              # did not play: books void the leg
    if stat == "anytime_td":
        return v >= 1
    if v == line:
        return None                              # push: leg voided
    return v > line if side == "over" else v < line


def _tickets(path, done_teams: set, final_teams: set, date_teams: set) -> list[dict]:
    """Last logged version of each ticket built before its first kickoff,
    graded once all its games are final; only tickets with a game today."""
    if not path.exists():
        return []
    builds = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
    best = {}
    for b in builds:
        built = b["built"]
        for i, t in enumerate(b["tickets"]):
            if built >= t.get("first_kick", "9999"):
                continue
            key = (t["kind"], t["games"][0]) if t["kind"] == "SGP" else (t["kind"], i)
            if key not in best or built > best[key][0]:
                best[key] = (built, t)
    out = []
    for (kind, _), (_, t) in sorted(best.items(), key=lambda kv: (kv[0][0], str(kv[0][1]))):
        teams = {l["team"] for l in t["legs"]}
        if teams & date_teams and teams <= final_teams:
            out.append(t)
    return out


def run(cfg: dict, paths: dict, date: str | None = None, refresh: bool = True, force: bool = False, log=print) -> str:
    from .auto import _refresh
    from .build import load_season
    t = _refresh(cfg, paths, log) if refresh else load_season(paths["db"])
    g = t["games"].copy()
    g["date"] = g["date"].astype(str)
    fin = g[g["home_score"].notna()]
    today = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d")
    if date is None:
        past = fin[fin["date"] < today]
        if past.empty:
            return "nothing to grade"
        date = past["date"].max()
    day = g[g["date"] == date]
    if day.empty:
        return f"no games on {date}"
    if day["home_score"].isna().any():
        return f"{date}: games not final yet"
    out_dir = paths["out"] / "daily"
    out_dir.mkdir(parents=True, exist_ok=True)
    md = out_dir / f"{date}.md"
    if md.exists() and not force:
        return f"{date} already graded ({md.name})"
    week = int(day["week"].iloc[0])
    teams = set(day["home"]) | set(day["away"])
    pg = t["player_games"]
    pw = pg[(pg["week"] == week) & pg["team"].isin(teams)]
    if pw.empty:
        return f"{date}: box scores not in yet (try again later)"
    final_teams = set(fin[fin["week"] == week]["home"]) | set(fin[fin["week"] == week]["away"])
    labels = ", ".join(f"{a} {int(s_a)}-{int(s_h)} {h}" for a, h, s_a, s_h in
                       zip(day["away"], day["home"], day["away_score"], day["home_score"]))
    L = [f"# Daily grade: {date} (week {week})", "", labels, ""]
    tg = [f"📋 Daily grade {date}: {labels}"]

    # 1. Paper bets
    f = paths["out"] / "paper" / f"week_{week:02d}_locked.csv"
    if f.exists():
        b = pd.read_csv(f)
        b = b[b["team"].isin(teams)]
        rows, units, staked = [], 0.0, 0.0
        for x in b.itertuples():
            v = _actual(pw, x.player_id, x.stat)
            w = _leg_won(v, x.stat, x.side, x.line)
            bo, bl = getattr(x, "book_odds", np.nan), getattr(x, "book_line", np.nan)
            price = float(bo) if pd.notna(bo) and pd.notna(bl) and float(bl) == float(x.line) else float(x.odds)
            pr = 0.0 if w is None else (x.stake * (_price_dec(price) - 1) if w else -x.stake)
            units += pr
            staked += x.stake if w is not None else 0
            rows.append(("⛔" if w is None else "✅" if w else "❌", x.player, x.side, x.line, x.stat, v, pr))
        if rows:
            wn, ls = sum(r[0] == "✅" for r in rows), sum(r[0] == "❌" for r in rows)
            head = f"Qualifying bets: {wn}-{ls}, {units:+.2f} units on {staked:.1f} staked"
            L += [f"## {head}", ""] + [f"- {r[0]} {r[1]} {r[2]} {r[3]:g} {r[4]} → {'DNP' if r[5] is None else f'{r[5]:g}'} ({r[6]:+.2f}u)" for r in rows] + [""]
            tg.append(head)

    # 2. Money list
    f = paths["out"] / "money" / f"week_{week:02d}.csv"
    if f.exists():
        m = pd.read_csv(f)
        m = m[m["team"].isin(teams)]
        pk = pw.assign(key=pw["player"].map(norm_name))
        rows, prof, staked = [], 0.0, 0.0
        for x in m.itertuples():
            a = pk[pk["key"] == norm_name(x.player)]
            v = float(a[STATS[x.stat][0]].sum()) if len(a) else None
            w = None if v is None else ((v >= x.k) if x.side == "YES" else (v < x.k))
            pr = 0.0 if w is None else (x.stake * (1 - x.price) / x.price if w else -x.stake)
            prof += pr
            staked += x.stake if w is not None else 0
            rows.append(("⛔" if w is None else "✅" if w else "❌", x.player, x.side, x.k, v, pr, x.price))
        if rows:
            from .clv import season_text, week_clv
            try:
                cv = week_clv(week, paths, log=log)
                cmap = dict(zip(cv["player"], cv["close_mid"])) if len(cv) else {}
                cv = cv[cv["team"].isin(teams)] if len(cv) else cv
            except Exception as e:
                log(f"CLV skipped ({e})")
                cv, cmap = pd.DataFrame(), {}
            wn, ls = sum(r[0] == "✅" for r in rows), sum(r[0] == "❌" for r in rows)
            head = f"💵 Money list: {wn}-{ls}, ${prof:+.2f} on ${staked:.2f}"
            if len(cv):
                head += f"; beat the closing price on {int(cv.beat_close.sum())} of {len(cv)} (avg {cv.clv.mean() * 100:+.1f}¢)"

            def _close(name, side):
                c = cmap.get(name)
                return "" if c is None else f", close {(c if side == 'YES' else 1 - c):.2f}"
            L += [f"## {head}", ""] + [f"- {r[0]} {r[1]} {r[2]} {r[3]}+ rush attempts @ {r[6]:.2f}{_close(r[1], r[2])} → {'DNP' if r[4] is None else f'{r[4]:g}'} (${r[5]:+.2f})" for r in rows]
            L += ["", season_text(paths), ""]
            tg += [head, season_text(paths)]

    # 3. Every lean on a posted line
    files = sorted((paths["out"] / "paper").glob(f"week_{week:02d}_all_lines_evaluated*.csv"))
    if files:
        ev = pd.concat([pd.read_csv(x) for x in files], ignore_index=True)
        ev = ev[ev["team"].isin(teams)]
        lean = ev.sort_values("p_cal", ascending=False).drop_duplicates(["player_id", "stat", "line"])
        res = []
        for x in lean.itertuples():
            w = _leg_won(_actual(pw, x.player_id, x.stat), x.stat, x.side, x.line)
            if w is not None:
                res.append((x.stat, bool(w), x.p_cal))
        if res:
            r = pd.DataFrame(res, columns=["stat", "won", "p"])
            by = r.groupby("stat")["won"].agg(["sum", "size"])
            strong = r[r["p"] >= 0.65]
            head = (f"All leans: {int(r.won.sum())}-{int((~r.won).sum())} ({r.won.mean():.0%})"
                    + (f"; 65%+ leans {int(strong.won.sum())}-{int((~strong.won).sum())}" if len(strong) else ""))
            L += [f"## {head}", "", "| stat | right | wrong |", "|---|---|---|"]
            L += [f"| {s} | {int(a)} | {int(n - a)} |" for s, (a, n) in by.iterrows()] + [""]
            tg.append(head + " — " + ", ".join(f"{s} {int(a)}-{int(n - a)}" for s, (a, n) in by.iterrows()))

    # 4. Board tickets (SGPs, anytime-TD)
    pw_week = pg[pg["week"] == week]
    tk = _tickets(paths["out"] / "board" / f"week_{week:02d}_tickets.jsonl", teams, final_teams, teams)
    for kind, title in (("SGP", "Same-game parlays"), ("Anytime TD", "Anytime-TD tickets")):
        T = [x for x in tk if x["kind"] == kind]
        if not T:
            continue
        lines, hits = [], 0
        for x in T:
            res = []
            for l in x["legs"]:
                v = _actual(pw_week, l.get("player_id"), l["stat"]) if l.get("player_id") else None
                res.append((l, _leg_won(v, l["stat"], l.get("side"), l.get("line")), v))
            live = [w for _, w, _ in res if w is not None]
            hit = bool(live) and all(live)
            hits += hit
            name = x["games"][0] if kind == "SGP" else f"{len(x['legs'])} legs"
            lines.append(f"- {'✅' if hit else '❌'} {name} (fair +{(x['fair'] - 1) * 100:,.0f}): " + "; ".join(
                f"{'✅' if w else '⛔' if w is None else '❌'} {l['player']} {l['what']}" + ("" if v is None else f" ({v:g})")
                for l, w, v in res))
        head = f"{title}: {hits} of {len(T)} hit"
        L += [f"## {head}", ""] + lines + [""]
        tg.append(head)

    if len(L) <= 4:
        L += ["Nothing was locked, listed or posted for these games.", ""]
    md.write_text("\n".join(L))
    return "\n".join(tg) + f"\n(details: {md.relative_to(paths['out'].parent.parent) if paths['out'].parent.parent in md.parents else md})"
