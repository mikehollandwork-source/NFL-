"""Command line entry point.

  python -m nfl_proj scrape            download nflverse play-by-play / stats (or PFR pages, see [source])
  python -m nfl_proj build             turn the downloaded data into data/nfl_<season>.db
  python -m nfl_proj styles            coaching-style / defense report + adaptation test
  python -m nfl_proj external          refresh online defensive scheme data (Sharp Football)
  python -m nfl_proj coaches           download play-caller history + coach report
  python -m nfl_proj project --week 7  projections for a week (prints choices first)
  python -m nfl_proj backtest --weeks 2-5   replay past weeks with only the data known then
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
        "nflverse": ROOT / "data" / "raw" / "nflverse",
        "personnel": ROOT / "data" / "external" / "defense_personnel.csv",
    }


def _provider(cfg) -> str:
    return cfg.get("source", {}).get("provider", "nflverse")


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
    if _provider(cfg) == "nflverse":
        from . import nflverse
        hist = nflverse.history_table(coaches, paths["nflverse"])
    else:
        hist = history_table(coaches, Fetcher(paths["cache"].parent / "history"))
    return scheme, profiles(coaches, hist, cfg["season"])


def _scrape_history(cfg, paths, coaches):
    if _provider(cfg) == "nflverse":
        from .coaches import parse_history
        from .nflverse import download_history
        download_history([y for h in coaches["caller_history"] for _, y in parse_history(h)], paths["nflverse"])
        return
    from .coaches import scrape_history
    from .scrape import Fetcher
    scrape_history(coaches, Fetcher(paths["cache"].parent / "history", delay=cfg["scrape"]["delay_seconds"]))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="nfl_proj")
    ap.add_argument("--config", default=str(ROOT / "config" / "projection.toml"))
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("scrape")
    sub.add_parser("build")
    sub.add_parser("styles")
    sub.add_parser("external")
    sub.add_parser("coaches")
    bt = sub.add_parser("backtest")
    bt.add_argument("--weeks", default="2-5", help="e.g. 2-5")
    bt.add_argument("--sims", type=int, default=2000)
    pj = sub.add_parser("project")
    pj.add_argument("--week", type=int, help="defaults to the next week with unplayed games")
    pj.add_argument("--yes", action="store_true", help="skip the confirmation prompt")
    args = ap.parse_args(argv)

    cfg = load_cfg(Path(args.config))
    paths = _paths(cfg)

    if args.cmd == "scrape" and _provider(cfg) == "nflverse":
        from .nflverse import download_season
        download_season(cfg["season"], paths["nflverse"])
        return
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
        from .coaches import load_coaches
        _scrape_history(cfg, paths, load_coaches(paths["coaches"]))
        return
    if args.cmd == "build" and _provider(cfg) == "nflverse":
        from .nflverse import build_season
        build_season(cfg["season"], paths["nflverse"], paths["db"])
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
        from .coaches import load_coaches
        _scrape_history(cfg, paths, load_coaches(paths["coaches"]))
        scheme, coach = _scheme_and_coach(cfg, paths, plays, labels)
        coach.to_csv(paths["out"] / "coaches.csv", index=False)
        print(coach.to_markdown(index=False, floatfmt=".3f"))
        return

    if args.cmd == "styles":
        from .market import Market
        from .ratings import Schedule
        sos = Schedule(plays, t["games"], cfg)
        mk = Market(t["games"], cfg)
        nxt = t["games"][t["games"]["boxscore_id"].isna()]["week"].min()
        md = styles_report(style, dprof, labels, splits, est, scheme, coach, plays,
                           sos=sos, misses=mk.misses(int(nxt)) if mk.enabled and pd.notna(nxt) else None,
                           team_def=t.get("team_defense"))
        (paths["out"] / "styles.md").write_text(md)
        style.to_csv(paths["out"] / "offense_style.csv", index=False)
        dprof.to_csv(paths["out"] / "defense_profile.csv", index=False)
        splits.to_csv(paths["out"] / "matchup_splits.csv", index=False)
        print(md)
        return

    if args.cmd == "backtest":
        from .backtest import run as run_backtest
        a_, _, b_ = args.weeks.partition("-")
        weeks = list(range(int(a_), int(b_ or a_) + 1))
        res = run_backtest(t, cfg, paths, weeks, n_sims=args.sims)
        (paths["out"] / "backtest.md").write_text(res["report"])
        for k in ("picks", "calls", "totals", "proj_err"):
            if not res[k].empty:
                res[k].to_csv(paths["out"] / f"backtest_{k}.csv", index=False)
        print(res["report"])
        return

    games = t["games"]
    week = args.week or int(games[games["boxscore_id"].isna()]["week"].min())
    print(settings_block(cfg, est, strength))
    if not args.yes:
        if input(f"Project week {week} with these choices? [y/N] ").strip().lower() != "y":
            print("Stopped. Edit config/projection.toml and re-run.")
            return
    from .pipeline import run_week
    from .sim import apply_lines, wide_means
    r = run_week(t, cfg, paths, week)
    for f in r["flags"]:
        print("availability:", f)
    r["auto_overrides"].to_csv(paths["out"] / f"week_{week:02d}_availability.csv", index=False)
    lines = pd.read_csv(paths["lines"], dtype=str) if paths["lines"].exists() else None
    props = apply_lines(r["props"], lines)
    if lines is not None and not lines.empty:
        from .picks import pick_week
        r["picks"] = pick_week(r["proj"], props, r["tables"]["player_games"], week, cfg, lines)
    wide = r["wide"]
    props_out = props.drop(columns="_samples").round(3)

    stem = paths["out"] / f"week_{week:02d}"
    wide.to_csv(f"{stem}_projections.csv", index=False)
    props_out.to_csv(f"{stem}_props.csv", index=False)
    r["totals"].round(2).to_csv(f"{stem}_team_totals.csv", index=False)
    if not r["picks"].empty:
        r["picks"].to_csv(f"{stem}_picks.csv", index=False)
    import sqlite3
    with sqlite3.connect(paths["db"]) as con:
        for name, df in ((f"projections_week_{week:02d}", wide), (f"props_week_{week:02d}", props_out)):
            df.to_sql(name, con, if_exists="replace", index=False)
    md = week_report(week, wide, r["ctx"], r["style"], r["dprof"], r["labels"], cfg, r["est"], r["strength"],
                     r["scheme"], r["coach"], r["plays"], overrides=r["overrides"], flags=r["flags"],
                     market=r["proj"].market, corners=r["corners"], picks=r["picks"], projector=r["proj"],
                     totals=r["totals"])
    if "p_over" in props_out:
        edge = props_out[props_out["line"].notna()].assign(
            best=lambda d: d[["p_over", "p_under"]].max(axis=1)).sort_values("best", ascending=False)
        md += "\n## Your prop lines\n\n" + edge[["player", "stat", "line", "median", "p_over", "p_under"]] \
            .to_markdown(index=False, floatfmt=".2f") + "\n"
    Path(f"{stem}_report.md").write_text(md)
    print(f"wrote {stem}_projections.csv, _props.csv, _team_totals.csv, _picks.csv, _report.md "
          f"({wide['player'].nunique()} players, {len(r['ctx']) // 2} games)")


if __name__ == "__main__":
    main()
