"""Real-money list: the one edge that held up against the market.

Backtest (tools/kalshi_backtest.py, 2026 weeks 2-6): single bets on Kalshi
rush-attempt markets where the model's chance beats the price by 10+ points
went +28% ROI over 157 bets (90% range +10% to +52%); every other stat lost
to the Kalshi close. So this list is carries only, priced at what you would
actually pay (YES at the ask, NO at 1 - bid). Each pick is logged the first
time it qualifies, at that price, and graded after the games.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from .odds import norm_name
from .paper import calibrate

DEFAULT = {"min_edge": 0.10, "max_spread": 0.10, "bankroll": 50.0, "kelly_fraction": 0.25, "max_stake_pct": 0.05,
           "stats": ["carries"]}


def _cfg(cfg):
    return {**DEFAULT, **cfg.get("money", {})}


def build(cfg: dict, paths: dict, week: int | None = None, refresh: bool = False, log=print):
    from .auto import _refresh, kickoffs
    from .build import load_season
    from .kalshi import fetch
    from .odds import fetch as fetch_lines, pick_book
    from .pipeline import run_week
    c = _cfg(cfg)
    t = _refresh(cfg, paths, log) if refresh else load_season(paths["db"])
    games = t["games"]
    now = datetime.now(timezone.utc)
    if week is None:
        today = pd.Timestamp.now(tz="America/New_York").strftime("%Y-%m-%d")
        pend = games[games["boxscore_id"].isna() & (games["date"].astype(str) >= today)]
        if pend.empty:
            return None, None
        week = int(pend["week"].min())
    g = kickoffs(games, week)
    ko = {}
    for x in g.itertuples():
        ko[x.home] = ko[x.away] = (x.kickoff, x.label)
    r = run_week(t, cfg, paths, week, log=lambda *a: None)
    P = r["props"][r["props"]["_samples"].notna()].copy()
    P["key"] = P["player"].map(norm_name)
    K = fetch(log=log)
    K = K[K["stat"].isin(c["stats"])] if len(K) else K
    try:
        L = pick_book(fetch_lines(games, week, cfg, None, log=lambda *a: None), cfg)
    except Exception:
        L = pd.DataFrame()
    rows = []
    for x in K.itertuples():
        p = P[(P["key"] == x.key) & (P["stat"] == x.stat)]
        if p.empty:
            continue
        team = p["team"].iloc[0]
        kick, label = ko.get(team, (None, None))
        if kick is None or kick <= now or x.bid <= 0 or x.ask >= 1 or x.ask - x.bid > c["max_spread"]:
            continue
        smp = np.asarray(p["_samples"].iloc[0], float)
        pm = calibrate(float((smp >= x.k).mean()), cfg, x.stat, "over")
        for side, prob, price in (("YES", pm, x.ask), ("NO", 1 - pm, 1 - x.bid)):
            edge = prob - price
            if edge < c["min_edge"]:
                continue
            kelly = max(0.0, (prob - price) / (1 - price)) * c["kelly_fraction"]
            stake = round(min(kelly, c["max_stake_pct"]) * c["bankroll"], 2)
            dk = ""
            if len(L):
                m = L[(L["player"].map(norm_name) == x.key) & (L["stat"] == x.stat)]
                if len(m):
                    ln = float(m["line"].iloc[0])
                    p_dk = calibrate(float((smp > ln).mean()) if side == "YES" else float((smp < ln).mean()), cfg,
                                     x.stat, "over" if side == "YES" else "under")
                    dk = f"DK {'over' if side == 'YES' else 'under'} {ln:g} (model {p_dk:.0%})"
            rows.append({"week": week, "game": label, "kickoff": kick.isoformat(), "player": x.player, "team": team,
                         "stat": x.stat, "k": int(x.k), "side": side, "model": round(prob, 3), "price": round(price, 3),
                         "edge": round(edge, 3), "stake": stake, "volume": x.volume, "ticker": x.ticker, "dk": dk,
                         "found_at": now.isoformat(timespec="seconds")})
    # one bet per player and stat (the backtest priced one market per player): his biggest edge
    picks = (pd.DataFrame(rows).sort_values("edge", ascending=False).drop_duplicates(["player", "stat"])
             if rows else pd.DataFrame())
    if len(picks):
        ov = r.get("overrides")
        outs = set(ov.loc[ov["status"].str.lower() == "out", "player"]) if ov is not None and len(ov) else set()
        picks["hold"] = [_hold(r["tables"]["player_games"], x.team, x.player, pd.Timestamp(x.kickoff), now, outs)
                         for x in picks.itertuples()]
    logf = paths["out"] / "money" / f"week_{week:02d}.csv"
    logf.parent.mkdir(parents=True, exist_ok=True)
    if len(picks):
        old = pd.read_csv(logf) if logf.exists() else pd.DataFrame()
        new = picks[~picks["ticker"].isin(set(old.get("ticker", [])))] if len(old) else picks
        pd.concat([old, new], ignore_index=True).to_csv(logf, index=False)
    picks = freeze(picks, week, paths, now)
    return picks, week


def week_picks(week: int, paths: dict) -> pd.DataFrame:
    """The picks that count: frozen picks for games past their lock run,
    the logged picks for any game never frozen (e.g. weeks before freezing)."""
    d = paths["out"] / "money"
    logf, finalf = d / f"week_{week:02d}.csv", d / f"week_{week:02d}_final.csv"
    lg = pd.read_csv(logf) if logf.exists() else pd.DataFrame()
    fz = frozen_games(week, paths)
    fn = pd.read_csv(finalf) if finalf.exists() else pd.DataFrame()
    if len(lg) and fz:
        lg = lg[~lg["game"].isin(fz)]
    return pd.concat([fn, lg], ignore_index=True)


def frozen_games(week: int, paths: dict) -> set:
    f = paths["out"] / "money" / f"week_{week:02d}_frozen_games.txt"
    return set(f.read_text().splitlines()) if f.exists() else set()


def freeze(picks: pd.DataFrame, week: int, paths: dict, now) -> pd.DataFrame:
    """Once a game's lock run has happened, its money picks are fixed: the
    first money run after the lock records them (price, stake) in
    week_NN_final.csv, and every later run shows exactly those for that game.
    Grading and CLV use the final picks."""
    lockf = paths["out"] / "paper" / f"week_{week:02d}_lock_log.csv"
    locked = set(pd.read_csv(lockf)["label"]) if lockf.exists() else set()
    finalf = paths["out"] / "money" / f"week_{week:02d}_final.csv"
    gf = paths["out"] / "money" / f"week_{week:02d}_frozen_games.txt"
    done = frozen_games(week, paths)
    final = pd.read_csv(finalf) if finalf.exists() else pd.DataFrame()
    picks = picks if picks is not None else pd.DataFrame()
    newly = locked - done
    if newly:
        add = picks[picks["game"].isin(newly)].assign(frozen_at=pd.Timestamp(now).isoformat(timespec="seconds")) \
            if len(picks) else pd.DataFrame()
        if len(add):
            final = pd.concat([final, add], ignore_index=True)
            final.to_csv(finalf, index=False)
        gf.write_text("\n".join(sorted(done | newly)))
        done |= newly
    open_ = picks[~picks["game"].isin(done)].assign(frozen=False) if len(picks) else picks
    if len(final):
        live = final[final["game"].isin(done) & (pd.to_datetime(final["kickoff"], utc=True) > pd.Timestamp(now))]
        open_ = pd.concat([live.assign(frozen=True), open_], ignore_index=True)
    return open_.sort_values("edge", ascending=False) if len(open_) else open_


def _hold(pg: pd.DataFrame, team: str, player: str, kick: pd.Timestamp, now, outs: set = frozenset()) -> str:
    """A team's carries depend on whether a back who missed its last game
    plays. Until game-day inactives post (~90 min before kickoff) that is a
    guess, so such picks are held. 2021-25: a lead back returning after one
    missed game gets 96% of his old share, so the projection itself holds up
    if he plays; the risk is betting before knowing whether he does."""
    if kick - pd.Timestamp(now) <= pd.Timedelta(minutes=90):
        return ""                                 # inactives are out: the projection already knows
    t = pg[pg["team"] == team]
    if t.empty:
        return ""
    last = t["week"].max()
    rb = t[t["pos"] == "RB"]
    tot = rb.groupby("player")["rush_att"].sum()
    gp = rb[rb["rush_att"] > 0].groupby("player")["week"].nunique()
    team_tot = rb.groupby("week")["rush_att"].sum()
    out = []
    for name, c in tot.items():
        weeks = set(rb[(rb["player"] == name) & (rb["rush_att"] > 0)]["week"])
        if last in weeks or gp.get(name, 0) < 2 or name in outs:     # played, too few games, or ruled Out
            continue
        share = c / team_tot[team_tot.index.isin(weeks)].sum()
        if share >= 0.35:
            out.append(name)
    if not out:
        return ""
    return f"HOLD until inactives (~90 min before kickoff): {', '.join(out)} missed {team}'s last game"


def text(picks: pd.DataFrame, week: int, cfg: dict) -> str:
    c = _cfg(cfg)
    if picks is None or picks.empty:
        return f"💵 Week {week} money list: no carries bets beat the Kalshi price by {c['min_edge']:.0%}+ right now."
    lines = [f"💵 Week {week} money list: rush attempts where the model beats the price by {c['min_edge']:.0%}+ "
             f"(bankroll ${c['bankroll']:.0f}, quarter Kelly)"]
    for x in picks.itertuples():
        what = f"{x.k}+ rush attempts" if x.side == "YES" else f"UNDER {x.k} rush attempts (≤{x.k - 1})"
        lines.append(f"• {x.player} ({x.team}) {what}: model {x.model:.0%} vs price {x.price:.0%} "
                     f"→ edge +{x.edge * 100:.0f}, stake ${x.stake:.2f} [{x.game}]" + (f"\n   {x.dk}" if isinstance(x.dk, str) and x.dk else "")
                     + (f"\n   ⏸ {x.hold}" if isinstance(getattr(x, "hold", ""), str) and x.hold else "")
                     + ("\n   🔒 locked: fixed at the lock run, won't change" if getattr(x, "frozen", False) is True else ""))
    lines.append("Kalshi: buy the contract at or below the price shown. Backtest: +28% ROI over 157 bets, weeks 2-6.")
    return "\n".join(lines)


def grade(week: int, player_games: pd.DataFrame, paths: dict) -> str | None:
    from .picks import STATS
    f = paths["out"] / "money" / f"week_{week:02d}.csv"
    m = week_picks(week, paths)
    if m.empty:
        return None
    pw = player_games[player_games["week"] == week].copy()
    pw["key"] = pw["player"].map(norm_name)
    res = []
    for x in m.itertuples():
        a = pw[(pw["key"] == norm_name(x.player)) & (pw["team"] == x.team)]
        if a.empty:
            res.append((np.nan, "void", 0.0)); continue
        v = float(a[STATS[x.stat][0]].sum())
        won = (v >= x.k) if x.side == "YES" else (v < x.k)
        res.append((v, "win" if won else "loss", x.stake * ((1 - x.price) / x.price if won else -1)))
    m["actual"], m["result"], m["profit"] = zip(*res)
    m.to_csv(f.with_name(f"week_{week:02d}_graded.csv"), index=False)
    d = m[m["result"] != "void"]
    staked = d["stake"].sum()
    head = (f"💵 Money list week {week}: {int((d.result == 'win').sum())}-{int((d.result == 'loss').sum())}, "
            f"{d.profit.sum():+.2f} on ${staked:.2f} staked" + (f" (ROI {d.profit.sum() / staked:+.0%})" if staked else ""))
    return head + "\n" + "\n".join(f"{'✅' if x.result == 'win' else '❌' if x.result == 'loss' else '⛔'} {x.player} "
                                   f"{x.side} {x.k}+ carries → {x.actual:g} ({x.profit:+.2f})" for x in m.itertuples()
                                   if x.result != "void" or True)
