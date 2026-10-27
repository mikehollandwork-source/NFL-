"""Why projections miss: every player projection split into parts that add up
exactly to (actual - projected).

For a stat built as volume x rate (receiving yards = targets x yards per
target, and so on):

- team: the team threw / ran more or less than projected   (V_a - V_p) * s_p * r_p
- share: the player's slice of that volume was off          (s_a - s_p) * V_a * r_p
- eff:   yards (or catches) per touch were off               v_a * (r_a - r_p)
- dnp:   projected but did not play                          -projected

Volume stats (targets, carries) have only team + share. Summed over many games,
a component whose average is reliably away from zero in a group of players is
a steady bias worth a backtest; one that averages zero is just noise.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

# stat: (projected volume col, actual volume col, actual stat col)
FAMILY = {
    "rec_yds": ("targets", "targets", "rec_yds"),
    "receptions": ("targets", "targets", "rec"),
    "targets": ("targets", "targets", "targets"),
    "rush_yds": ("carries", "rush_att", "rush_yds"),
    "carries": ("carries", "rush_att", "rush_att"),
    "pass_yds": ("pass_att", "pass_att", "pass_yds"),
    "completions": ("pass_att", "pass_att", "pass_cmp"),
}
COMPONENTS = ["team", "share", "eff", "dnp"]


def attribute(proj: pd.DataFrame, pg: pd.DataFrame, min_proj: dict | None = None) -> pd.DataFrame:
    """proj: one row per player-week projection (team, player_id, pos, week and
    the stat / volume columns). pg: actual player games for the same weeks."""
    min_proj = min_proj or {"rec_yds": 15, "receptions": 1.5, "targets": 2.5, "rush_yds": 15, "carries": 4,
                            "pass_yds": 120, "completions": 12}
    act = pg.copy()
    rows = []
    for stat, (pv, av, ac) in FAMILY.items():
        if stat not in proj or pv not in proj:
            continue
        if stat == pv:
            p = proj[["week", "team", "player_id", "player", "pos", pv]].rename(columns={pv: "v_p"})
            p["y_p"] = p["v_p"]
        else:
            p = proj[["week", "team", "player_id", "player", "pos", pv, stat]].rename(columns={pv: "v_p", stat: "y_p"})
        if pv == "pass_att":      # team passing volume = the projected QB's attempts
            p = p[p["pos"] == "QB"]
        V_p = proj.groupby(["week", "team"])[pv].sum().rename("V_p") if pv != "pass_att" else \
            proj[proj["pos"] == "QB"].groupby(["week", "team"])[pv].sum().rename("V_p")
        V_a = act.groupby(["week", "team"])[av].sum().rename("V_a")
        a = act[["week", "team", "player_id", av, ac]].rename(columns={av: "v_a", ac: "y_a"})
        if av == ac:
            a = act[["week", "team", "player_id", av]].rename(columns={av: "v_a"})
            a["y_a"] = a["v_a"]
        m = p[p["y_p"] >= min_proj.get(stat, 0)].merge(V_p, on=["week", "team"]).merge(V_a, on=["week", "team"])
        m = m.merge(a, on=["week", "team", "player_id"], how="left")
        played = m["v_a"].notna()
        m[["v_a", "y_a"]] = m[["v_a", "y_a"]].fillna(0.0)
        s_p = m["v_p"] / m["V_p"].replace(0, np.nan)
        s_a = m["v_a"] / m["V_a"].replace(0, np.nan)
        r_p = (m["y_p"] / m["v_p"].replace(0, np.nan)).fillna(0)
        r_a = (m["y_a"] / m["v_a"].replace(0, np.nan)).fillna(r_p)
        m["team_c"] = np.where(played, (m["V_a"] - m["V_p"]) * s_p * r_p, 0.0)
        m["share_c"] = np.where(played, (s_a - s_p) * m["V_a"] * r_p, 0.0)
        # yards with no recorded volume (laterals, scoring quirks) count as efficiency
        m["eff_c"] = np.where(played, np.where(m["v_a"] > 0, m["v_a"] * (r_a - r_p), m["y_a"]), 0.0) if av != ac else 0.0
        m["dnp_c"] = np.where(played, 0.0, -m["y_p"])
        m["err"] = m["y_a"] - m["y_p"]
        m["stat"] = stat
        m["s_p"] = s_p
        rows.append(m)
    out = pd.concat(rows, ignore_index=True)
    # Components add up to the error (exact up to rounding); keep the check visible
    out["resid"] = out["err"] - out[[f"{c}_c" for c in COMPONENTS]].sum(axis=1)
    return out


def segments(d: pd.DataFrame, games: pd.DataFrame | None = None, totals: pd.DataFrame | None = None) -> pd.DataFrame:
    """Groups to look for steady biases in: position, role on the team (share
    rank), projected game environment (total, margin) when team projections are
    given, home/away and early/late season."""
    d = d.copy()
    d["role"] = d.groupby(["stat", "week", "team"])["s_p"].rank(ascending=False, method="first") \
        .map(lambda r: "1 lead" if r == 1 else "2 second" if r == 2 else "3 depth")
    d["season_part"] = np.where(d["week"] <= 9, "weeks 1-9", "weeks 10+")
    if games is not None:
        g = games[["week", "home", "away"]]
        home = set(zip(g["week"], g["home"]))
        d["venue"] = ["home" if (w, t) in home else "away" for w, t in zip(d["week"], d["team"])]
    if totals is not None and {"model_points", "team", "opp", "week"} <= set(totals.columns):
        t = totals[["week", "team", "opp", "model_points"]]
        t = t.merge(t.rename(columns={"team": "opp", "opp": "team", "model_points": "opp_points"}),
                    on=["week", "team", "opp"])
        t["proj_total"] = t["model_points"] + t["opp_points"]
        t["proj_margin"] = t["model_points"] - t["opp_points"]
        d = d.merge(t[["week", "team", "proj_total", "proj_margin"]], on=["week", "team"], how="left")
        d["game_total"] = pd.qcut(d["proj_total"], 3, labels=["low total", "mid total", "high total"]).astype(str)
        d["script"] = pd.cut(d["proj_margin"], [-99, -4, 4, 99], labels=["underdog 4+", "close", "favorite 4+"]).astype(str)
    return d


def biases(d: pd.DataFrame, by: list[str], split: str | None = None, min_n: int = 60) -> pd.DataFrame:
    """Mean signed error and each component's mean per group, with t-values.
    With ``split`` (e.g. season), also the error mean in each part, so a bias
    has to show up in both to count."""
    comps = [f"{c}_c" for c in COMPONENTS]
    out = []
    for key, g in d.groupby(["stat"] + by):
        if len(g) < min_n:
            continue
        r = dict(zip(["stat"] + by, key if isinstance(key, tuple) else (key,)))
        r["n"] = len(g)
        r["proj"] = g["y_p"].mean()
        r["bias"] = g["err"].mean()
        r["t"] = g["err"].mean() / (g["err"].std(ddof=1) / np.sqrt(len(g))) if g["err"].std() > 0 else 0
        r["bias_pct"] = r["bias"] / r["proj"] if r["proj"] else np.nan
        for c in comps:
            r[c.replace("_c", "")] = g[c].mean()
        if split:
            for s, gs in g.groupby(split):
                r[f"bias_{s}"] = gs["err"].mean()
                r[f"t_{s}"] = gs["err"].mean() / (gs["err"].std(ddof=1) / np.sqrt(len(gs))) if len(gs) > 2 and gs["err"].std() > 0 else 0
        out.append(r)
    return pd.DataFrame(out)


def error_mix(d: pd.DataFrame) -> pd.DataFrame:
    """How much of each stat's miss comes from each part (share of the summed
    absolute components), and the stat's average miss."""
    comps = [f"{c}_c" for c in COMPONENTS]
    rows = []
    for stat, g in d.groupby("stat"):
        a = g[comps].abs().mean()
        tot = a.sum()
        rows.append({"stat": stat, "n": len(g), "mae": g["err"].abs().mean(), "bias": g["err"].mean(),
                     **{c.replace("_c", ""): a[c] / tot for c in comps}})
    return pd.DataFrame(rows)


# Biases found in the 2025 + 2026 backtests (tools/attribution_study.py, factor_tests section 15);
# tracked live every week to see whether they hold.
WATCH = [("targets", "pos", "RB", "RB targets"), ("targets", "role", "1 lead", "each team's top target"),
         ("carries", "pos", "QB", "QB rush attempts"), ("rec_yds", "pos", "RB", "RB receiving yards"),
         ("pass_yds", "pos", "QB", "QB passing yards")]


def weekly(paths: dict, week: int, pg: pd.DataFrame) -> str | None:
    """Attribute the week's locked projections (paper/week_NN_proj.csv), add
    them to output/<season>/attribution_live.csv and summarize season to date."""
    f = paths["out"] / "paper" / f"week_{week:02d}_proj.csv"
    if not f.exists():
        return None
    proj = pd.read_csv(f)
    d = segments(attribute(proj, pg[pg["week"] == week]))
    live = paths["out"] / "attribution_live.csv"
    old = pd.read_csv(live) if live.exists() else pd.DataFrame()
    if len(old):
        old = old[old["week"] != week]
    allw = pd.concat([old, d], ignore_index=True)
    allw.to_csv(live, index=False)
    mix = error_mix(d)
    lines = [f"🔎 Week {week} misses by cause (team volume / player share / per-touch / didn't play):"]
    for r in mix.itertuples():
        lines.append(f"• {r.stat.replace('_', ' ')}: avg miss {r.mae:.1f}, bias {r.bias:+.1f} → "
                     f"{r.team:.0%} / {r.share:.0%} / {r.eff:.0%} / {r.dnp:.0%}")
    lines.append(f"Known biases, season to date ({allw['week'].nunique()} weeks):")
    for stat, col, val, name in WATCH:
        x = allw[(allw["stat"] == stat) & (allw[col] == val)]
        if len(x) >= 10:
            lines.append(f"• {name}: actual {x['err'].mean():+.2f} vs projected {x['y_p'].mean():.1f} "
                         f"({x['err'].mean() / x['y_p'].mean():+.0%}, n {len(x)})")
    return "\n".join(lines)
