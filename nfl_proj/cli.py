"""Command line entry point.

  python -m nfl_proj scrape            download schedule + every completed box score
  python -m nfl_proj build             parse cached HTML into data/nfl_<season>.db
  python -m nfl_proj styles            coaching-style / defense report + adaptation test
  python -m nfl_proj external          refresh online defensive scheme data (Sharp Football)
  python -m nfl_proj coaches           scrape play-caller history from PFR + coach report
  python -m nfl_proj project --week 7  projections for a week (prints choices first)
"""

from __future__ import annotations

import argparse
import tomllib
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent


def load_cfg(path: Path) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


def _paths(cfg):
    season = cfg["season"]
    return {
        "cache": ROOT / "data" / "raw" / str(season),
        "db": ROOT / "data" / f"nfl_{season}.db",
        "out": ROOT / "output" / str(season),
        "tags": ROOT / "data" / "manual" / "defense_tags.csv",
        "overrides": ROOT / "data" / "manual" / "player_overrides.csv",
        "lines": ROOT / "data" / "manual" / "prop_lines.csv",
        "external": ROOT / "data" / "external" / "defense_scheme.csv",
        "coaches": ROOT / "data" / "manual" / "coaches.csv",
    }


def _analysis(cfg, paths):
    from .build import load_season
    from .profiles import (combined_labels, defense_profile, load_manual_labels, matchup_splits,
                           offense_style, prep_plays)
    t = load_season(paths["db"])
    plays = prep_plays(t["plays"], cfg)
    style = offense_style(plays, t["plays"])
    dprof = defense_profile(plays, t.get("team_defense"))
    labels = combined_labels(dprof, load_manual_labels(paths["tags"]), cfg["matchup"]["defense_labels"])
    return t, plays, style, dprof, labels, matchup_splits(plays, labels)


def _scheme_and_coach(cfg, paths, plays, labels):
    from .coaches import history_table, load_coaches, profiles
    from .external import load_external, scheme_labels
    from .profiles import load_manual_labels
    from .scrape import Fetcher
    scheme = scheme_labels(load_external(paths["external"]), load_manual_labels(paths["tags"]), cfg)
    coaches = load_coaches(paths["coaches"])
    if coaches.empty:
        return scheme, None
    hist = history_table(coaches, Fetcher(paths["cache"].parent / "history"))
    return scheme, profiles(coaches, hist, cfg["season"])


def main(argv=None):
    ap = argparse.ArgumentParser(prog="nfl_proj")
    ap.add_argument("--config", default=str(ROOT / "config" / "projection.toml"))
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("scrape")
    sub.add_parser("build")
    sub.add_parser("styles")
    sub.add_parser("external")
    sub.add_parser("coaches")
    pj = sub.add_parser("project")
    pj.add_argument("--week", type=int, help="defaults to the next week with unplayed games")
    pj.add_argument("--yes", action="store_true", help="skip the confirmation prompt")
    args = ap.parse_args(argv)

    cfg = load_cfg(Path(args.config))
    paths = _paths(cfg)

    if args.cmd == "scrape":
        from .scrape import scrape_season
        scrape_season(cfg["season"], paths["cache"], delay=cfg["scrape"]["delay_seconds"])
        return
    if args.cmd == "external":
        from datetime import date
        from .external import scrape_sharp
        scrape_sharp(paths["external"], date.today().isoformat())
        return
    if args.cmd == "coaches" and not paths["db"].exists():
        from .coaches import load_coaches, scrape_history
        from .scrape import Fetcher
        scrape_history(load_coaches(paths["coaches"]), Fetcher(paths["cache"].parent / "history",
                                                                delay=cfg["scrape"]["delay_seconds"]))
        return
    if args.cmd == "build":
        from .build import build_season
        build_season(cfg["season"], paths["cache"], paths["db"])
        return

    from . import adaptation
    from .report import settings_block, styles_report, week_report
    t, plays, style, dprof, labels, splits = _analysis(cfg, paths)
    scheme, coach = _scheme_and_coach(cfg, paths, plays, labels)
    est = adaptation.estimate(plays, cfg["adaptation"]["min_plays"])
    strength = adaptation.effective_strength(est, cfg)
    paths["out"].mkdir(parents=True, exist_ok=True)

    if args.cmd == "coaches":
        from .coaches import load_coaches, scrape_history
        from .scrape import Fetcher
        scrape_history(load_coaches(paths["coaches"]), Fetcher(paths["cache"].parent / "history",
                                                                delay=cfg["scrape"]["delay_seconds"]))
        scheme, coach = _scheme_and_coach(cfg, paths, plays, labels)
        coach.to_csv(paths["out"] / "coaches.csv", index=False)
        print(coach.to_markdown(index=False, floatfmt=".3f"))
        return

    if args.cmd == "styles":
        md = styles_report(style, dprof, labels, splits, est, scheme, coach, plays)
        (paths["out"] / "styles.md").write_text(md)
        style.to_csv(paths["out"] / "offense_style.csv", index=False)
        dprof.to_csv(paths["out"] / "defense_profile.csv", index=False)
        splits.to_csv(paths["out"] / "matchup_splits.csv", index=False)
        print(md)
        return

    from .project import Projector
    games = t["games"]
    week = args.week or int(games[games["boxscore_id"].isna()]["week"].min())
    print(settings_block(cfg, est, strength))
    if not args.yes:
        if input(f"Project week {week} with these choices? [y/N] ").strip().lower() != "y":
            print("Stopped. Edit config/projection.toml and re-run.")
            return
    overrides = pd.read_csv(paths["overrides"], dtype=str).fillna("") if paths["overrides"].exists() else None
    from .sim import Simulator, apply_lines, wide_means
    proj = Projector(plays, t["player_games"], games, cfg, labels, overrides, scheme, coach)
    _, ctx = proj.project_week(week)
    sim = Simulator(proj, t["player_games"], t.get("defenders"), t.get("kickers"),
                    n_sims=cfg["sim"]["n_sims"], seed=cfg["sim"]["seed"])
    props = sim.run_week(week)
    lines = pd.read_csv(paths["lines"], dtype=str) if paths["lines"].exists() else None
    props = apply_lines(props, lines)
    wide = wide_means(props)
    props_out = props.drop(columns="_samples").round(3)

    stem = paths["out"] / f"week_{week:02d}"
    wide.to_csv(f"{stem}_projections.csv", index=False)
    props_out.to_csv(f"{stem}_props.csv", index=False)
    import sqlite3
    with sqlite3.connect(paths["db"]) as con:
        for name, df in ((f"projections_week_{week:02d}", wide), (f"props_week_{week:02d}", props_out)):
            df.to_sql(name, con, if_exists="replace", index=False)
    md = week_report(week, wide, ctx, style, dprof, labels, cfg, est, strength, scheme, coach, plays)
    if "p_over" in props_out:
        edge = props_out[props_out["line"].notna()].assign(
            best=lambda d: d[["p_over", "p_under"]].max(axis=1)).sort_values("best", ascending=False)
        md += "\n## Your prop lines\n\n" + edge[["player", "stat", "line", "median", "p_over", "p_under"]] \
            .to_markdown(index=False, floatfmt=".2f") + "\n"
    Path(f"{stem}_report.md").write_text(md)
    print(f"wrote {stem}_projections.csv, _props.csv, _report.md "
          f"({wide['player'].nunique()} players, {len(ctx) // 2} games)")


if __name__ == "__main__":
    main()
