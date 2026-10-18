"""Hands-off weekly cycle: lock each game shortly before its own kickoff,
send picks to Telegram, grade the week once its stats are in.

``python -m nfl_proj auto --mode lock`` (run at fixed times on game days):
  1. refresh nflverse data and rebuild the season database
  2. every game this week kicking off within ``[auto] lock_window_hours``
     that isn't locked yet is due; by then the final injury report and
     game-day inactives are out, and live ESPN statuses are merged in
  3. pull DraftKings lines (ESPN), project, lock the due games (assumed
     price for selection), record real book prices for the bets if
     ODDS_API_KEY is set (grading only)
  4. log every game (locked / no bets / no lines / missed) in
     paper/week_NN_lock_log.csv so the whole week is accounted for, and
     send a Telegram message
``--mode grade`` (Tuesday): grade any locked week whose games are final,
update the ledgers and send the results.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

ET = ZoneInfo("America/New_York")


def kickoffs(games: pd.DataFrame, week: int) -> pd.DataFrame:
    g = games[games["week"] == week].copy()
    g["kickoff"] = [datetime.strptime(f"{d} {t or '13:00'}", "%Y-%m-%d %H:%M").replace(tzinfo=ET).astimezone(timezone.utc)
                    for d, t in zip(g["date"], g["gametime"])]
    g["game"] = [" @ ".join(sorted([a, h])) for a, h in zip(g["away"], g["home"])]
    g["label"] = g["away"] + " @ " + g["home"]
    return g


def _refresh(cfg: dict, paths: dict, log) -> dict:
    """Same steps as ``scrape`` + ``build``: current season refreshed, last
    season (priors) and coach history built if a fresh checkout lacks them."""
    from .build import load_season
    from .cli import main as cli_main
    cli_main(["scrape"])
    cli_main(["build"])
    return load_season(paths["db"])


def _fmt_bet(b) -> str:
    real = f", book {int(b.book_odds):+d}" if "book_odds" in b and pd.notna(b.book_odds) else ""
    return (f"• {b.player} ({b.team}) {b.stat.replace('_', ' ')} {b.side.upper()} {b.line:g} "
            f"— model {b.model_median:.0f}, {b.p_cal:.0%}, EV {b.ev:+.0%}, {b.stake:g}u{real}")


def run_lock(cfg: dict, paths: dict, root: Path, now: datetime | None = None, window_h: float | None = None,
             refresh: bool = True, log=print) -> str:
    from .notify import send
    from .odds import fetch, fetch_prices, pick_book, save
    from .paper import lock
    from .pipeline import run_week
    now = now or datetime.now(timezone.utc)
    window_h = window_h if window_h is not None else cfg.get("auto", {}).get("lock_window_hours", 2.25)
    paper_dir = paths["out"] / "paper"
    paper_dir.mkdir(parents=True, exist_ok=True)
    t = _refresh(cfg, paths, log) if refresh else __import__("nfl_proj.build", fromlist=["x"]).load_season(paths["db"])
    games = t["games"]
    pending = games[games["boxscore_id"].isna()]
    if pending.empty:
        return "season over"
    week = int(pending["week"].min())
    g = kickoffs(games, week)
    logf = paper_dir / f"week_{week:02d}_lock_log.csv"
    lg = pd.read_csv(logf) if logf.exists() else pd.DataFrame(columns=["game", "label", "kickoff", "status",
                                                                      "n_bets", "n_lines", "at"])
    locked = paper_dir / f"week_{week:02d}_locked.csv"
    done = set(lg["game"]) | (set(pd.read_csv(locked)["game"]) if locked.exists() else set())
    stamp = now.isoformat(timespec="seconds")
    new_log, msgs = [], []
    for r in g[(g["kickoff"] <= now) & ~g["game"].isin(done)].itertuples():
        new_log.append({"game": r.game, "label": r.label, "kickoff": r.kickoff.isoformat(), "status": "missed",
                        "n_bets": 0, "n_lines": 0, "at": stamp})
        msgs.append(f"⚠️ MISSED: {r.label} kicked off {r.kickoff.astimezone(ET):%a %I:%M %p ET} without a lock")
    due = g[(g["kickoff"] > now) & (g["kickoff"] <= now + timedelta(hours=window_h)) & ~g["game"].isin(done)]
    if due.empty:
        if new_log:
            pd.concat([lg, pd.DataFrame(new_log)]).to_csv(logf, index=False)
            send("\n".join(msgs), log=log)
        nxt = g[(g["kickoff"] > now) & ~g["game"].isin(done)].sort_values("kickoff").head(1)
        return "nothing due" + (f"; next {nxt.iloc[0]['label']} at {nxt.iloc[0]['kickoff'].astimezone(ET):%a %I:%M %p ET}"
                                if len(nxt) else "")
    # Lines: keep earlier snapshots for other games, refresh this slate
    rp = paths["nflverse"] / f"roster_weekly_{int(cfg['season'])}.csv.gz"
    roster = pd.read_csv(rp, low_memory=False) if rp.exists() else None
    lines_now = fetch(games, week, cfg, roster, log=log)
    odds_dir = root / "data" / "odds"
    snap = odds_dir / f"week_{week:02d}_lock.csv"
    old = pd.read_csv(snap) if snap.exists() else pd.DataFrame()
    due_pairs = set(zip(due["home"], due["away"]))
    if not old.empty and not lines_now.empty:
        old = old[~old.apply(lambda x: (x["home"], x["away"]) in due_pairs, axis=1)]
    save(pd.concat([old, lines_now], ignore_index=True), odds_dir, week, "lock")
    lines = pick_book(lines_now, cfg)
    r = run_week(t, cfg, paths, week)
    teams = set(due["home"]) | set(due["away"])
    bets, path = lock(r["props"], lines, r["tables"]["player_games"], week, cfg, paper_dir, root,
                      teams=teams, price_fn=lambda b: fetch_prices(b, cfg, log=log),
                      skip_teams=r.get("no_qb_history", set()))
    flags = [f for f in r["flags"] if any(tm in f for tm in teams) or "injury report" in f]
    for d in due.sort_values("kickoff").itertuples():
        n_lines = int(((lines_now["home"] == d.home) & (lines_now["away"] == d.away)).sum()) if not lines_now.empty else 0
        b = bets[bets["game"] == d.game] if not bets.empty else bets
        status = "locked" if len(b) else ("no lines posted" if n_lines == 0 else "no qualifying bets")
        new_log.append({"game": d.game, "label": d.label, "kickoff": d.kickoff.isoformat(), "status": status,
                        "n_bets": len(b), "n_lines": n_lines, "at": stamp})
        head = f"🏈 {d.label} — {d.kickoff.astimezone(ET):%a %I:%M %p ET} ({n_lines} lines)"
        msgs.append(head + ("\n" + "\n".join(_fmt_bet(x) for x in b.itertuples()) if len(b) else f"\n  {status}"))
    pd.concat([lg, pd.DataFrame(new_log)]).to_csv(logf, index=False)
    out = f"Week {week} lock\n\n" + "\n\n".join(msgs)
    if flags:
        out += "\n\nAvailability notes:\n" + "\n".join(f"- {f}" for f in flags)
    left = g[~g["game"].isin(set(lg["game"]) | {x["game"] for x in new_log})]
    out += f"\n\nWeek {week}: {len(g) - len(left)}/{len(g)} games handled"
    send(out, log=log)
    return out


def run_grade(cfg: dict, paths: dict, root: Path, refresh: bool = True, log=print) -> str:
    from .notify import send
    from .odds import load_lines, pick_book
    from .paper import grade, summary
    paper_dir = paths["out"] / "paper"
    t = _refresh(cfg, paths, log) if refresh else __import__("nfl_proj.build", fromlist=["x"]).load_season(paths["db"])
    games, pg = t["games"], t["player_games"]
    msgs = []
    for f in sorted(paper_dir.glob("week_*_locked.csv")):
        week = int(f.name.split("_")[1])
        if (paper_dir / f"week_{week:02d}_graded.csv").exists():
            continue
        wk = games[games["week"] == week]
        if wk["boxscore_id"].isna().any() or not (pg["week"] == week).any():
            continue  # games or stats not final yet
        gr = grade(week, pg, paper_dir, pick_book(load_lines(root / "data" / "odds", week, "close"), cfg))
        d = gr[gr["result"].isin(["win", "loss"])]
        lines = [f"📊 Week {week} graded: {int((d['result'] == 'win').sum())}-{int((d['result'] == 'loss').sum())}"
                 f", {gr['profit'].sum():+.2f}u"]
        for r in gr.itertuples():
            icon = {"win": "✅", "loss": "❌", "push": "➖", "void": "⛔"}[r.result]
            lines.append(f"{icon} {r.player} {r.stat.replace('_', ' ')} {r.side} {r.line:g} → {r.actual:g}"
                         f" ({r.profit:+.2f}u @ {int(r.price_used):+d} {r.price_used_source})"
                         if pd.notna(r.actual) else f"{icon} {r.player} {r.stat} — did not play")
        msgs.append("\n".join(lines))
    if not msgs:
        return "nothing to grade"
    summ = summary(paper_dir)
    (paper_dir / "summary.md").write_text(summ)
    out = "\n\n".join(msgs) + "\n\n" + summ.replace("**", "")
    send(out, log=log)
    return out
