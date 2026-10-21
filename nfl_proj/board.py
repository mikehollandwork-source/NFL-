"""Prop board: every posted line for games not yet kicked off, the model's lean,
win chance, season hit log, and which bets qualify / are already locked.
Rebuilt after each lock run so injuries and lines are current."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

TEMPLATE = Path(__file__).with_name("board_template.html")


def build(cfg: dict, paths: dict, root: Path, refresh: bool = False, log=print) -> Path | None:
    from .auto import _refresh, kickoffs
    from .build import load_season
    from .odds import fetch, pick_book
    from .paper import evaluate, select
    from .picks import STATS
    from .pipeline import run_week

    t = _refresh(cfg, paths, log) if refresh else load_season(paths["db"])
    games = t["games"]
    pending = games[games["boxscore_id"].isna()]
    if pending.empty:
        return None
    week = int(pending["week"].min())
    now = datetime.now(timezone.utc)
    g = kickoffs(games, week)
    future = {x.game for x in g.itertuples() if x.kickoff > now}
    rp = paths["nflverse"] / f"roster_weekly_{int(cfg['season'])}.csv.gz"
    roster = pd.read_csv(rp, low_memory=False) if rp.exists() else None
    lines = pick_book(fetch(games, week, cfg, roster, log=lambda *a: None), cfg)
    r = run_week(t, cfg, paths, week)
    ev = evaluate(r["props"], lines, r["tables"]["player_games"], week, cfg)
    ev = ev[ev["game"].isin(future)]
    skip = r.get("no_qb_history", set())
    lean = ev.sort_values("p_cal", ascending=False).drop_duplicates(["player_id", "stat", "line"])
    bets = select(ev[~ev["team"].isin(skip)], cfg)
    bk = set(zip(bets["player_id"], bets["stat"], bets["side"]))
    lf = paths["out"] / "paper" / f"week_{week:02d}_locked.csv"
    lk = set()
    if lf.exists():
        L = pd.read_csv(lf)
        lk = set(zip(L["player_id"], L["stat"], L["side"]))
    pg = r["tables"]["player_games"]
    logs = {pid: h.sort_values("week") for pid, h in pg[pg["week"] < week].groupby("player_id")}
    ko = {x.game: (x.label, x.kickoff) for x in g.itertuples()}
    et = ZoneInfo("America/New_York")
    rows = []
    for x in lean.itertuples():
        h = logs.get(x.player_id)
        vals = [float(v) for v in h[STATS[x.stat][0]]] if h is not None else []
        hit = sum((v > x.line) if x.side == "over" else (v < x.line) for v in vals)
        lab, k = ko[x.game]
        key = (x.player_id, x.stat, x.side)
        rows.append({"game": lab, "kick": k.astimezone(et).strftime("%a %-I:%M %p"), "ko": k.isoformat(),
                     "player": x.player, "team": x.team, "pos": x.pos, "stat": x.stat, "line": float(x.line),
                     "side": x.side, "model": round(float(x.model_median), 1), "mean": round(float(x.model_mean), 1),
                     "p": round(float(x.p_cal), 3), "ev": round(float(x.ev), 3), "trend": x.usage_trend,
                     "log": vals, "hit": int(hit), "n": len(vals), "bet": key in bk, "locked": key in lk,
                     "skip": x.team in skip})
    try:
        from .parlays import board_parlays, sgp_tickets
        tickets = [t for t in board_parlays(r, cfg, week, future, n_first=0) if t["kind"] == "Anytime TD"]
        tickets += sgp_tickets(r, lean, cfg)
    except Exception as e:      # the prop list matters more than the tickets
        log(f"board: TD parlays skipped ({e})")
        tickets = []
    data = {"generated": now.isoformat(timespec="minutes"), "flags": r["flags"], "rows": rows,
            "price": cfg["odds"].get("assumed_price", -115), "parlays": tickets}
    out = paths["out"] / "board" / "prop-board.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    html = TEMPLATE.read_text().replace("__WEEK__", str(week)).replace(
        "__DATA__", json.dumps(data).replace("</", "<\\/"))
    out.write_text(html)
    log(f"board: {len(rows)} lines, {sum(r['bet'] for r in rows)} qualifying, "
        f"{sum(r['locked'] for r in rows)} locked, {len(future)} games -> {out}")
    return out


def summary_text(path: Path) -> str:
    """Plain-text list of the board's qualifying and locked bets (for Telegram)."""
    import re
    html = Path(path).read_text()
    m = re.search(r'<script id="data" type="application/json">(.*?)</script>', html, re.S)
    d = json.loads(m.group(1).replace("<\\/", "</"))
    rows = [r for r in d["rows"] if r["bet"] or r["locked"]]
    head = f"🏈 Prop board ({d['generated'][:16].replace('T', ' ')} UTC): {len(rows)} qualifying / locked"
    lines = [head]
    for g in sorted({r["game"] for r in rows}, key=lambda g: min(x["ko"] for x in rows if x["game"] == g)):
        rs = [r for r in rows if r["game"] == g]
        lines.append(f"\n{g} ({rs[0]['kick']} ET)")
        for r in sorted(rs, key=lambda r: -r["p"]):
            tag = "LOCKED" if r["locked"] else "qualifies"
            lines.append(f"• {r['player']} {r['stat'].replace('_', ' ')} {r['side'].upper()} {r['line']:g} "
                         f"(model {r['model']:g}, {r['p']:.0%}) [{tag}]")
    flags = [f for f in d.get("flags", []) if "injury report isn't out" not in f]
    if flags:
        lines += ["\nAvailability:"] + [f"- {f}" for f in flags]
    return "\n".join(lines)
