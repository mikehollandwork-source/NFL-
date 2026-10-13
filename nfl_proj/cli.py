"""Command line entry point.

  python -m nfl_proj scrape            download schedule + every completed box score
  python -m nfl_proj build             parse cached HTML into data/nfl_<season>.db
  python -m nfl_proj styles            coaching-style / defense report + adaptation test
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


def main(argv=None):
    ap = argparse.ArgumentParser(prog="nfl_proj")
    ap.add_argument("--config", default=str(ROOT / "config" / "projection.toml"))
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("scrape")
    sub.add_parser("build")
    sub.add_parser("styles")
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
    if args.cmd == "build":
        from .build import build_season
        build_season(cfg["season"], paths["cache"], paths["db"])
        return

    from . import adaptation
    from .report import settings_block, styles_report, week_report
    t, plays, style, dprof, labels, splits = _analysis(cfg, paths)
    est = adaptation.estimate(plays, cfg["adaptation"]["min_plays"])
    strength = adaptation.effective_strength(est, cfg)
    paths["out"].mkdir(parents=True, exist_ok=True)

    if args.cmd == "styles":
        md = styles_report(style, dprof, labels, splits, est)
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
    proj = Projector(plays, t["player_games"], games, cfg, labels, overrides)
    df, ctx = proj.project_week(week)
    df.to_csv(paths["out"] / f"week_{week:02d}_projections.csv", index=False)
    md = week_report(week, df, ctx, style, dprof, labels, cfg, est, strength)
    (paths["out"] / f"week_{week:02d}_report.md").write_text(md)
    print(f"wrote {paths['out']}/week_{week:02d}_projections.csv and _report.md "
          f"({len(df)} players, {len(ctx) // 2} games)")


if __name__ == "__main__":
    main()
