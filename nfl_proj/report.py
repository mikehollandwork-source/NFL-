"""Markdown reports: coaching styles, defensive profiles, matchup notes."""

from __future__ import annotations

import pandas as pd

from .profiles import describe_style


def _pct(v):
    return "—" if pd.isna(v) else f"{v:.0%}"


def _epa(v):
    return "—" if pd.isna(v) else f"{v:+.2f}"


def settings_block(cfg: dict, est: dict, strength: float) -> str:
    a, m, d = cfg["adaptation"], cfg["matchup"], cfg["definitions"]
    return "\n".join([
        "## Choices used for this projection",
        f"- Negative play = `{d['negative_play']}`",
        f"- Recency half-life = {cfg['weighting']['half_life_weeks']} weeks",
        f"- Adaptation mode = `{a['mode']}` → applied strength {strength:+.2f}",
        f"- Adaptation test: beta {est['beta']:+.2f}, t {est['t']:+.1f}, "
        f"n {est['n']} bucket-games — **{est['verdict']}**",
        f"- Defense weight = {m['defense_weight']}, shrink = {m['shrink_plays']} plays, "
        f"labels = `{m['defense_labels']}`",
        "",
    ])


def matchup_notes(ctx: dict, style: pd.DataFrame, dprof: pd.DataFrame, labels: pd.DataFrame,
                  lg_def: pd.Series) -> list[str]:
    team, opp = ctx["team"], ctx["opp"]
    notes = []
    s = style.set_index("team").loc[team] if team in set(style["team"]) else None
    d = dprof.set_index("team").loc[opp] if opp in set(dprof["team"]) else None
    lab = labels.set_index("team").loc[opp] if opp in set(labels["team"]) else None
    if d is not None and s is not None:
        if d["epa_allowed_deep"] - lg_def["epa_allowed_deep"] > 0.10:
            notes.append(f"{opp} is soft deep ({_epa(d['epa_allowed_deep'])} EPA/deep att vs league "
                         f"{_epa(lg_def['epa_allowed_deep'])}); {team} throws deep {_pct(s['deep_pass_share'])}.")
        if lab is not None and lab["third_down_pressure"] == "heavy":
            notes.append(f"{opp} brings heavy 3rd-down pressure (source: {lab.get('pressure_source', 'manual')}); "
                         f"3rd-down deep EPA allowed {_epa(d['third_down_epa_allowed_deep'])} "
                         f"on {int(d['third_down_deep_n'])} attempts. {team} 3rd-down deep share "
                         f"{_pct(s['third_down_deep_share'])}.")
        if d["epa_allowed_run"] - lg_def["epa_allowed_run"] > 0.07:
            notes.append(f"{opp} run defense is soft ({_epa(d['epa_allowed_run'])} EPA/run).")
        if lab is not None and lab.get("base_coverage"):
            notes.append(f"{opp} base coverage (your tag): {lab['base_coverage']}.")
    eff = ctx["pass_eff"] | ctx["run_eff"]
    best = sorted(eff.items(), key=lambda kv: -kv[1]["m_ypp"])[:2]
    worst = sorted(eff.items(), key=lambda kv: kv[1]["m_ypp"])[:1]
    notes.append("Best matchups: " + ", ".join(f"{b} (x{e['m_ypp']:.2f})" for b, e in best)
                 + f"; worst: {worst[0][0]} (x{worst[0][1]['m_ypp']:.2f}).")
    sig = {**ctx["pass_signal"], **ctx["run_signal"]}
    up = [b for b, x in sig.items() if x > 0.25]
    down = [b for b, x in sig.items() if x < -0.25]
    if up or down:
        notes.append(f"Last game — worked: {', '.join(up) or 'none'}; failed: {', '.join(down) or 'none'}.")
    return notes


def _coach_line(team, coach, plays):
    if coach is None or team not in set(coach["team"]):
        return None
    from .coaches import current_concentration, describe
    cur = current_concentration(plays).set_index("team") if plays is not None else None
    row = coach.set_index("team").loc[team]
    return describe(row, cur.loc[team] if cur is not None and team in cur.index else None)


def _scheme_line(team, scheme):
    if scheme is None or team not in set(scheme["team"]):
        return None
    r = scheme.set_index("team").loc[team]
    parts = [f"{k}: {r[k]}" for k in ("blitz", "coverage", "shell") if r[k]]
    return (", ".join(parts) + f" [{r['scheme_source']}]") if parts else None


def _adjust_lines(ctx: dict) -> list[str]:
    a = ctx.get("adjust")
    if not a:
        return []
    out = []
    m = a.get("market")
    if m:
        out.append(f"**Market team total:** implied {m['implied']:.1f} (this team landed within the "
                   f"tolerance in {m['hit_rate']:.0%} of its games, avg miss {m['abs_miss']:.1f}). "
                   f"Model {m['model_pts']:.1f} → blended {m['blended_pts']:.1f}: TD rates x{m['td_factor']:.2f}, "
                   f"yards x{m['ypp_factor']:.2f}.")
    sc = a.get("script")
    if sc:
        out.append(f"**Model game script:** projected {sc['model_pts']:.1f} – {sc['opp_model_pts']:.1f} "
                   f"(margin {sc['margin']:+.1f}) → dropback rate {a['dropback_shift']:+.1%}.")
    s = a["sos"]
    moved = {k: v for k, v in s.items() if abs(v - 1) >= 0.02}
    if moved:
        names = {"off_pass": "own pass yds", "off_run": "own run yds", "off_pts": "own scoring",
                 "def_pass": "opp pass D", "def_run": "opp run D", "def_pts": "opp scoring D"}
        out.append("**Strength of schedule:** " + ", ".join(f"{names[k]} x{v:.2f}" for k, v in moved.items())
                   + " (raw stats re-rated against the opponents actually faced).")
    return out


def week_report(week: int, proj: pd.DataFrame, contexts: list[dict], style: pd.DataFrame,
                dprof: pd.DataFrame, labels: pd.DataFrame, cfg: dict, est: dict, strength: float,
                scheme: pd.DataFrame | None = None, coach: pd.DataFrame | None = None,
                plays: pd.DataFrame | None = None, overrides: pd.DataFrame | None = None,
                flags: list[str] | None = None, market=None, corners=None,
                picks: pd.DataFrame | None = None, projector=None, totals: pd.DataFrame | None = None) -> str:
    lg_style = style.mean(numeric_only=True)
    lg_def = dprof.mean(numeric_only=True)
    out = [f"# Week {week} projections", "", settings_block(cfg, est, strength)]
    if flags:
        out += ["## Availability flags", ""] + [f"- {f}" for f in flags] + [""]
    if picks is not None and not picks.empty:
        out += ["## Top 5 data-led projections per game", "",
                "Direction vs the baseline (your line if entered, otherwise the player's own season "
                "average). Overs need rising carries/targets, unders falling ones, unless the player is a "
                "consistent-volume star or a starting QB. Ranked by score = edge x sample x signal agreement.", ""]
        for game, g in picks.groupby("game", sort=False):
            out.append(f"**{game}**")
            out.append("")
            out.append(g[["rank", "player", "team", "stat", "direction", "baseline", "projected_median", "prob",
                          "signals"]].to_markdown(index=False, floatfmt=".2f"))
            out.append("")
    if totals is not None and not totals.empty:
        out += ["## Projected team totals (model)", "",
                "`model_points` = simulated 6 x TD + extra points + 3 x field goals before game script; "
                "`final_points` = after game script (and the market blend for qualifying teams).", "",
                totals[["team", "opp", "model_points", "final_points"]].to_markdown(index=False, floatfmt=".1f"), ""]
    if market is not None and market.enabled:
        mm = market.misses(week)
        if not mm.empty:
            q = mm.sort_values(["qualifies", "hit_rate", "abs_miss"], ascending=[False, False, True])
            out += ["## Market team totals: which teams qualify", "",
                    f"Only teams that landed within {market.tol:.0f} points of their implied team total in at "
                    f"least {market.min_hit_rate:.0%} of their games (min {market.min_games}) get the market "
                    f"blended in ({market.weight:.0%} market). Everyone else is model only. No spreads are used.", "",
                    q[["team", "games", "hit_rate", "abs_miss", "implied_avg", "scored_avg", "qualifies"]]
                    .to_markdown(index=False, floatfmt=".2f"), ""]
    for ctx in contexts:
        team, opp = ctx["team"], ctx["opp"]
        v = ctx["volume"]
        out.append(f"## {team} vs {opp}")
        out.append(f"Projected {v['plays']:.0f} plays, {v['dropback_rate']:.0%} dropbacks, "
                   f"{v['pass_att']:.1f} pass att, {v['runs']:.1f} runs, {v['sacks']:.1f} sacks. "
                   f"QB: {ctx['qb'] or 'unknown'}")
        if team in set(style["team"]):
            notes = describe_style(style.set_index("team").loc[team], lg_style)
            if notes:
                out.append("**Coaching style:** " + "; ".join(notes) + ".")
        for line in _adjust_lines(ctx):
            out.append(line)
        if overrides is not None and not overrides.empty:
            o = overrides[(overrides["team"] == team) & (overrides["status"].str.lower() == "out")]
            if not o.empty:
                out.append("**Out:** " + ", ".join(f"{r.player}" + (f" ({r.notes})" if getattr(r, "notes", "") else "")
                                                   for r in o.itertuples()) + ".")
        cl = _coach_line(team, coach, plays)
        if cl:
            out.append(f"**Coach angle:** {cl}.")
        if corners is not None:
            cl2 = corners.describe(opp)
            if cl2:
                out.append(f"**{opp} secondary:** {cl2}.")
        if projector is not None:
            weak = projector.defan.weaknesses(opp)
            if weak:
                out.append(f"**{opp} defensive weak spots:** " + "; ".join(weak) + ".")
            for line in projector.defan.describe_struggles(opp):
                out.append(f"- {opp} struggle: {line}")
            cm = projector.comps.effect(team, opp)
            if cm["comps"]:
                sims = ", ".join(f"{o} (similarity {s:.2f}: {p:+.1f} pass / {r_:+.1f} run yds/play vs their norm)"
                                 for o, s, p, r_ in cm["comps"])
                out.append(f"**Offenses like {team} that faced {opp}:** {sims} → {team} pass x{cm['pass']:.2f}, "
                           f"run x{cm['run']:.2f}.")
        sl = _scheme_line(opp, scheme)
        if sl:
            out.append(f"**{opp} defensive scheme (online/tagged):** {sl}.")
        for n in matchup_notes(ctx, style, dprof, labels, lg_def) + ctx.get("scheme_notes", []):
            out.append(f"- {n}")
        t = proj[proj["team"] == team]
        cols = ["player", "pos", "pass_yds", "pass_td", "interceptions", "carries", "rush_yds",
                "targets", "receptions", "rec_yds", "anytime_td"]
        off = t[(t["pass_att"] > 1) | (t["carries"] > 1.5) | (t["targets"] > 1.5)]
        out += ["", off[[c for c in cols if c in off]].to_markdown(index=False, floatfmt=".2f"), ""]
        if "kicking_points" in t:
            k = t[t["kicking_points"] > 0][["player", "fg_made", "xp_made", "kicking_points"]]
            if not k.empty:
                out += [f"**{team} kicker**", "", k.to_markdown(index=False, floatfmt=".2f"), ""]
        if "tackles" in t:
            d = t[t["tackles"] > 1.5].sort_values("tackles", ascending=False)[["player", "tackles", "sacks", "def_int"]]
            if not d.empty:
                out += [f"**{team} defenders (vs {opp} offense)**", "",
                        d.head(8).to_markdown(index=False, floatfmt=".2f"), ""]
    return "\n".join(out)


def styles_report(style: pd.DataFrame, dprof: pd.DataFrame, labels: pd.DataFrame,
                  splits: pd.DataFrame, est: dict, scheme: pd.DataFrame | None = None,
                  coach: pd.DataFrame | None = None, plays: pd.DataFrame | None = None,
                  sos=None, misses: pd.DataFrame | None = None,
                  team_def: pd.DataFrame | None = None) -> str:
    lg = style.mean(numeric_only=True)
    out = ["# Coaching styles and defensive profiles", "",
           "## Do coaches call more of what worked last game?",
           f"beta {est['beta']:+.2f} (t {est['t']:+.1f}, n {est['n']}): **{est['verdict']}**", "",
           "## Offense tendencies"]
    for _, r in style.sort_values("team").iterrows():
        notes = describe_style(r, lg)
        out.append(f"- **{r['team']}**: " + ("; ".join(notes) if notes else "close to league average"))
    out += ["", "## Defense labels", "",
            labels.to_markdown(index=False), "",
            "## League: play family vs defense label", "",
            splits.to_markdown(index=False, floatfmt=".2f") if not splits.empty else "(no data)", ""]
    if sos is not None:
        tb = sos.table()
        cols = [c for c in ("team", "off_pass_raw", "off_pass_adj", "off_pass_sched", "def_pass_raw",
                            "def_pass_adj", "def_pass_sched", "off_points_raw", "off_points_adj",
                            "def_points_raw", "def_points_adj", "def_points_sched") if c in tb]
        out += ["## Strength of schedule", "",
                "Ratings vs league average (yards per dropback, per run; points per game). `raw` is the "
                "team's own numbers, `adj` re-rates them against the opponents actually faced, `sched` is "
                "the average strength of those opponents (for an offense: the defenses it faced, positive "
                "= faced generous defenses; for a defense: the offenses it faced, positive = faced good "
                "offenses). For defenses, lower is better.", "",
                tb[cols].to_markdown(index=False, floatfmt="+.2f"), ""]
    if misses is not None and not misses.empty:
        out += ["## Market: points vs implied team totals", "",
                "Implied total from the closing spread and over/under. `correction` (shrunk average miss) "
                "is applied to next week's implied total.", "",
                misses.sort_values("avg_miss").to_markdown(index=False, floatfmt=".2f"), ""]
    if team_def is not None and not team_def.empty and "blitz_pct" in team_def:
        cols = [c for c in ("team", "blitz_pct", "third_down_blitz_rate", "avg_rushers", "pressure_per_db_pct")
                if c in team_def]
        out += ["## Blitz and pressure (FTN charting + PFR advanced defense)", "",
                "Blitz = any blitzer or 5+ rushers on a charted dropback. Pressures per dropback sum "
                "individual defenders' pressures, so it's an index, not a play rate.", "",
                team_def[cols].sort_values("blitz_pct", ascending=False).to_markdown(index=False, floatfmt=".1f"), ""]
    if coach is not None:
        out += ["## Coaches", ""]
        for t in sorted(coach["team"]):
            out.append(f"- **{t}**: {_coach_line(t, coach, plays)}")
        out.append("")
    if scheme is not None:
        from .external import compare_with_pbp
        chk = compare_with_pbp(scheme, labels)
        out += ["## Online scheme data vs what the play-by-play shows", "",
                "Blitz labels come from online charting; `third_down_pressure` comes from 3rd-down sack "
                "rate in the scraped play-by-play. A mismatch means the blitzes aren't getting home (or "
                "pressure comes without blitzing), which is worth knowing before betting on it.", "",
                chk.to_markdown(index=False) if not chk.empty else "(no online blitz data)", ""]
    return "\n".join(out)
