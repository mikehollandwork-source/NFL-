"""Paper trading player props: lock, grade, track.

lock (the day before each game; Saturday for Sunday games)
  For every posted line (player, stat, line, over / under price):
    1. model probability of over / under from the simulation
    2. calibrated: p = sigmoid(a + b * logit(model p)), fitted on the
       backtest (the raw model is overconfident)
    3. expected value at the posted price: EV = p x decimal odds - 1
    4. keep the better side if EV >= min_ev and p >= min_prob, the stat
       isn't excluded, and (optionally) usage is trending the bet's way
    5. stake: quarter Kelly on the calibrated probability, clipped to
       [min_stake, max_stake] units
    6. portfolio: best EV first, one bet per player, at most
       ``max_per_game`` per game and ``max_per_team_side`` per team and
       direction (same-team overs are correlated), at most ``max_bets``
  The locked file is never overwritten (unless --force), so results can't
  be cherry-picked afterwards. It records the line, price, book and time.

grade (after the games)
  Actual stats from the rebuilt database: win / loss / push / void (player
  didn't play), profit in units at the locked price, and closing-line value
  when a "close" odds snapshot exists (did the line move our way?).

The ledger (paper/ledger.csv) accumulates every graded bet; ``summary``
reports units, ROI, hit rate, CLV, results by stat, and a refit of the
calibration from real graded bets.
"""

from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from .odds import american_to_decimal, norm_name
from .picks import STATS, usage_trend


def _sigmoid(x):
    return 1 / (1 + np.exp(-x))


def calibrate(p: float, cfg: dict) -> float:
    c = cfg.get("paper", {})
    p = float(np.clip(p, 1e-4, 1 - 1e-4))
    return float(_sigmoid(c.get("calib_a", 0.0) + c.get("calib_b", 1.0) * np.log(p / (1 - p))))


def _git_rev(root: Path) -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=root, capture_output=True,
                              text=True, timeout=10).stdout.strip()
    except Exception:
        return ""


def evaluate(props: pd.DataFrame, lines: pd.DataFrame, player_games: pd.DataFrame, week: int,
             cfg: dict) -> pd.DataFrame:
    """Every posted line with model / calibrated probability and EV for both sides."""
    c = cfg.get("paper", {})
    if lines.empty:
        return pd.DataFrame()
    pr = props[props["stat"].isin(list(STATS)) & props["_samples"].notna()].copy()
    pr["key"] = pr["player"].map(norm_name)
    idx = {(k, s): i for i, k, s in zip(pr.index, pr["key"], pr["stat"])}
    by_id = {(p, s): i for i, p, s in zip(pr.index, pr["player_id"], pr["stat"])}
    rows = []
    for ln in lines.itertuples():
        pid = getattr(ln, "player_id", None)
        i = by_id.get((pid, ln.stat)) if isinstance(pid, str) and pid else None
        if i is None:
            i = idx.get((norm_name(ln.player), ln.stat))
        if i is None:
            continue
        r = pr.loc[i]
        smp = np.asarray(r["_samples"], dtype=float)
        p_over, p_under = float((smp > ln.line).mean()), float((smp < ln.line).mean())
        for side, p, odds in (("over", p_over, ln.over_odds), ("under", p_under, ln.under_odds)):
            if pd.isna(odds):
                continue
            pc = calibrate(p, cfg)
            dec = american_to_decimal(float(odds))
            ev = pc * dec - 1
            b = dec - 1
            kelly = max(0.0, (pc * b - (1 - pc)) / b)
            rows.append({"week": week, "game": " @ ".join(sorted([r["team"], r["opp"]])), "team": r["team"],
                         "opp": r["opp"], "player": r["player"], "player_id": r["player_id"], "pos": r["pos"],
                         "stat": ln.stat, "side": side, "line": ln.line, "odds": float(odds),
                         "book": getattr(ln, "book", ""), "price_source": getattr(ln, "price_source", "book"),
                         "line_fetched_at": getattr(ln, "fetched_at", ""),
                         "model_mean": float(smp.mean()), "model_median": float(np.median(smp)),
                         "p_model": p, "p_cal": pc, "breakeven": 1 / dec, "ev": ev,
                         "stake_kelly": kelly * c.get("kelly_fraction", 0.25) * 100})
    ev = pd.DataFrame(rows)
    if ev.empty:
        return ev
    # Usage trend (your qualification rule)
    pg = player_games[player_games["week"] < week]
    trend = {}
    for pid, team in set(zip(ev["player_id"], ev["team"])):
        h = pg[(pg["player_id"] == pid) & (pg["team"] == team)].sort_values("week")
        trend[(pid, "targets")] = usage_trend(h.set_index("week")["targets"])["dir"] if len(h) else "flat"
        trend[(pid, "rush_att")] = usage_trend(h.set_index("week")["rush_att"])["dir"] if len(h) else "flat"
    ev["usage_trend"] = [trend.get((pid, STATS[s][1]), "n/a") if STATS[s][2] != "qb" else "QB"
                         for pid, s in zip(ev["player_id"], ev["stat"])]
    return ev


def select(ev: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    c = cfg.get("paper", {})
    if ev.empty:
        return ev
    e = ev[(ev["ev"] >= c.get("min_ev", 0.03)) & (ev["p_cal"] >= c.get("min_prob", 0.54))
           & ~ev["stat"].isin(c.get("exclude_stats", []))].copy()
    if c.get("require_usage_trend", True):
        ok = (e["usage_trend"] == "QB") | ((e["side"] == "over") & (e["usage_trend"] == "up")) | \
             ((e["side"] == "under") & (e["usage_trend"] == "down"))
        e = e[ok]
    e = e.sort_values("ev", ascending=False)
    chosen, per_game, per_side, players = [], {}, {}, set()
    for r in e.itertuples():
        if r.player_id in players:
            continue
        if per_game.get(r.game, 0) >= c.get("max_per_game", 2):
            continue
        if per_side.get((r.team, r.side), 0) >= c.get("max_per_team_side", 1):
            continue
        chosen.append(r.Index)
        players.add(r.player_id)
        per_game[r.game] = per_game.get(r.game, 0) + 1
        per_side[(r.team, r.side)] = per_side.get((r.team, r.side), 0) + 1
        if len(chosen) >= c.get("max_bets", 15):
            break
    out = e.loc[chosen].copy()
    out["stake"] = out["stake_kelly"].clip(lower=c.get("min_stake", 0.5), upper=c.get("max_stake", 1.5)).round(2)
    return out


def lock(props, lines, player_games, week, cfg, paper_dir: Path, root: Path, force=False,
         teams: set | None = None, price_fn=None, skip_teams: set | None = None) -> tuple[pd.DataFrame, Path]:
    """Lock bets. With ``teams`` only games involving those teams are locked
    (e.g. Thursday's game before the Sunday slate); bets already locked for
    other games are kept unchanged and a game can be locked only once."""
    paper_dir.mkdir(parents=True, exist_ok=True)
    path = paper_dir / f"week_{week:02d}_locked.csv"
    prev = pd.read_csv(path) if path.exists() else pd.DataFrame()
    if not prev.empty and teams is None and not force:
        raise FileExistsError(f"{path} is already locked; pass --force only if you mean to replace it")
    ev = evaluate(props, lines, player_games, week, cfg)
    if skip_teams and not ev.empty:
        ev = ev[~ev["team"].isin(skip_teams)]
    if teams is not None and not ev.empty:
        ev = ev[ev["team"].isin(teams) | ev["opp"].isin(teams)]
    if not prev.empty and not force:
        done = set(prev["game"])
        clash = set(ev["game"]) & done if not ev.empty else set()
        if clash:
            raise FileExistsError(f"already locked: {', '.join(sorted(clash))}")
    if not ev.empty:
        tag = "" if teams is None else "_" + "_".join(sorted(teams))
        ev.drop(columns=[c for c in ev.columns if c.startswith("_")], errors="ignore") \
          .to_csv(paper_dir / f"week_{week:02d}_all_lines_evaluated{tag}.csv", index=False)
    c = dict(cfg)
    if teams is not None and not prev.empty:
        # The weekly cap counts bets already locked this week
        c = {**cfg, "paper": {**cfg.get("paper", {}),
                              "max_bets": max(cfg.get("paper", {}).get("max_bets", 15) - len(prev), 0)}}
    bets = select(ev, c)
    bets = bets.assign(locked_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                       model_commit=_git_rev(root))
    if price_fn is not None and not bets.empty:
        bets = price_fn(bets)  # real book prices, recorded for grading only
    out = bets if (prev.empty or force) else pd.concat([prev, bets], ignore_index=True)
    out.to_csv(path, index=False)
    return bets, path


def grade(week: int, player_games: pd.DataFrame, paper_dir: Path, close: pd.DataFrame | None = None) -> pd.DataFrame:
    path = paper_dir / f"week_{week:02d}_locked.csv"
    bets = pd.read_csv(path)
    out = []
    for r in bets.itertuples():
        col = STATS[r.stat][0]
        # Real book price (recorded at lock) when the book's line matched ours; else the assumed price
        bo, bl = getattr(r, "book_odds", np.nan), getattr(r, "book_line", np.nan)
        real = pd.notna(bo) and pd.notna(bl) and float(bl) == float(r.line)
        price, price_src = (float(bo), "book") if real else (float(r.odds), "assumed")
        a = player_games[(player_games["player_id"] == r.player_id) & (player_games["week"] == week)]
        if a.empty:
            res, actual, profit = "void", np.nan, 0.0
        else:
            actual = float(a[col].sum())
            if actual == r.line:
                res, profit = "push", 0.0
            else:
                won = actual > r.line if r.side == "over" else actual < r.line
                res = "win" if won else "loss"
                profit = r.stake * (american_to_decimal(price) - 1) if won else -r.stake
        clv_line = clv_prob = np.nan
        if close is not None and not close.empty:
            m = close[(close["player"].map(norm_name) == norm_name(r.player)) & (close["stat"] == r.stat)]
            if len(m):
                m = m.iloc[0]
                # Line moved our way = positive (over: closing line higher; under: lower)
                clv_line = (m["line"] - r.line) * (1 if r.side == "over" else -1)
                cp = m["over_odds"] if r.side == "over" else m["under_odds"]
                op = m["under_odds"] if r.side == "over" else m["over_odds"]
                # No-vig closing probability of our side at the closing line
                pi, po = 1 / american_to_decimal(cp), 1 / american_to_decimal(op)
                clv_prob = pi / (pi + po) - r.breakeven if m["line"] == r.line else np.nan
        out.append({**r._asdict(), "actual": actual, "result": res, "profit": round(profit, 3),
                    "price_used": price, "price_used_source": price_src,
                    "clv_line": clv_line, "clv_prob": clv_prob})
    g = pd.DataFrame(out).drop(columns=["Index"], errors="ignore")
    g.to_csv(paper_dir / f"week_{week:02d}_graded.csv", index=False)
    ledger = paper_dir / "ledger.csv"
    old = pd.read_csv(ledger) if ledger.exists() else pd.DataFrame()
    if not old.empty:
        old = old[old["week"] != week]
    pd.concat([old, g], ignore_index=True).to_csv(ledger, index=False)
    grade_calls(week, player_games, paper_dir)
    return g


def grade_calls(week: int, player_games: pd.DataFrame, paper_dir: Path) -> pd.DataFrame:
    """Right / wrong on the model's lean for EVERY posted line evaluated at
    lock (not just the bets): the side with the higher calibrated probability."""
    files = sorted(paper_dir.glob(f"week_{week:02d}_all_lines_evaluated*.csv"))
    if not files:
        return pd.DataFrame()
    ev = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    lean = ev.sort_values("p_cal", ascending=False).drop_duplicates(["player_id", "stat", "line"])
    rows = []
    pw = player_games[player_games["week"] == week]
    for r in lean.itertuples():
        a = pw[pw["player_id"] == r.player_id]
        if a.empty:
            res, actual = "void", np.nan
        else:
            actual = float(a[STATS[r.stat][0]].sum())
            res = "push" if actual == r.line else (
                "right" if (actual > r.line) == (r.side == "over") else "wrong")
        rows.append({"week": week, "game": r.game, "player": r.player, "player_id": r.player_id, "stat": r.stat,
                     "line": r.line, "lean": r.side, "p_cal": r.p_cal, "model_median": r.model_median,
                     "actual": actual, "result": res, "bet": False})
    calls = pd.DataFrame(rows)
    locked = paper_dir / f"week_{week:02d}_locked.csv"
    if locked.exists() and not calls.empty:
        b = pd.read_csv(locked)
        keys = set(zip(b["player_id"], b["stat"], b["line"]))
        calls["bet"] = [(p, s, l) in keys for p, s, l in zip(calls["player_id"], calls["stat"], calls["line"])]
    led = paper_dir / "calls_ledger.csv"
    old = pd.read_csv(led) if led.exists() else pd.DataFrame()
    if not old.empty:
        old = old[old["week"] != week]
    pd.concat([old, calls], ignore_index=True).to_csv(led, index=False)
    return calls


def summary(paper_dir: Path) -> str:
    ledger = paper_dir / "ledger.csv"
    if not ledger.exists():
        return "No graded paper trades yet."
    g = pd.read_csv(ledger)
    s = g[g["result"].isin(["win", "loss", "push"])]
    staked = s["stake"].sum()
    units = s["profit"].sum()
    dec = s[s["result"] != "push"]
    lines = [f"# Paper trading ledger", "",
             f"- Bets graded: {len(s)} (voids {int((g['result'] == 'void').sum())}, pushes "
             f"{int((s['result'] == 'push').sum())})",
             f"- Record: {int((dec['result'] == 'win').sum())}-{int((dec['result'] == 'loss').sum())} "
             f"({(dec['result'] == 'win').mean():.1%} hit vs {dec['breakeven'].mean():.1%} needed at the average price)"
             if len(dec) else "- Record: —",
             f"- Units: {units:+.2f} on {staked:.2f} staked → **ROI {units / staked:+.1%}**" if staked else "- ROI: —",
             f"- Prices: {(g.get('price_used_source', pd.Series('assumed', index=g.index)) == 'book').mean():.0%} of bets "
             f"graded at the real book price recorded at lock; the rest at the assumed price (ROI estimate)",
             f"- Average expected value at lock: {s['ev'].mean():+.1%}" if len(s) else "",
             f"- Closing-line value: line moved our way on {(g['clv_line'] > 0).mean():.0%} of bets with a closing "
             f"line (avg {g['clv_line'].mean():+.2f})" if g["clv_line"].notna().any() else
             "- Closing-line value: no closing snapshots yet (pull `odds --label close` before kickoff)", ""]
    led = paper_dir / "calls_ledger.csv"
    if led.exists():
        c = pd.read_csv(led)
        c = c[c["result"].isin(["right", "wrong"])]
        if len(c):
            lines.append(f"- Model lean on every posted line: {(c['result'] == 'right').mean():.1%} right "
                         f"({len(c)} lines); by stat: " + ", ".join(
                f"{k} {v:.0%}" for k, v in c.groupby("stat")["result"].apply(lambda x: (x == "right").mean()).items()))
            lines.append("")
    if len(dec):
        by = dec.groupby("stat").apply(lambda d: pd.Series({
            "bets": len(d), "hit": (d["result"] == "win").mean(), "units": d["profit"].sum(),
            "roi": d["profit"].sum() / d["stake"].sum()}), include_groups=False)
        lines += ["By stat:", "", by.to_markdown(floatfmt=".2f"), ""]
        wk = dec.groupby("week").apply(lambda d: pd.Series({
            "bets": len(d), "hit": (d["result"] == "win").mean(), "units": d["profit"].sum()}), include_groups=False)
        lines += ["By week:", "", wk.to_markdown(floatfmt=".2f"), ""]
        if len(dec) >= 60:
            x = np.log(dec["p_model"].clip(1e-4, 1 - 1e-4) / (1 - dec["p_model"].clip(1e-4, 1 - 1e-4)))
            y = (dec["result"] == "win").astype(float).to_numpy()
            X = np.c_[np.ones(len(x)), x]
            b = np.zeros(2)
            for _ in range(50):
                p = _sigmoid(X @ b)
                W = p * (1 - p)
                b = b + np.linalg.solve(X.T @ (X * W[:, None]) + 1e-6 * np.eye(2), X.T @ (y - p))
            lines.append(f"Calibration refit on graded bets: a = {b[0]:.2f}, b = {b[1]:.2f} "
                         f"(update [paper] calib_a / calib_b once there are 150+ bets).")
    return "\n".join(lines)
