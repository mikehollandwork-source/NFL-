# NFL player projections

Scrapes box scores and play-by-play from Pro-Football-Reference (no API), profiles every
offense's play-calling and every defense's weaknesses, tests whether coaches really
"cut what failed and call more of what worked," and projects player stat lines for the
upcoming week.

## Run it

```bash
pip install -r requirements.txt
python -m nfl_proj scrape      # schedule + every completed box score (~4s/page, cached)
python -m nfl_proj build       # parse cached pages -> data/nfl_2026.db
python -m nfl_proj styles      # coaching styles, defense labels, adaptation test -> output/2026/styles.md
python -m nfl_proj project     # next week's projections (shows your choices, asks y/N first)
```

Re-run `scrape` after each week; already-cached games are skipped.

## Your choices: `config/projection.toml`

Every modeling decision is a setting. `project` prints the active choices and waits for a
`y` before it projects anything.

| Setting | Default | Meaning |
|---|---|---|
| `definitions.negative_play` | `epa` | What counts as a play a coach would cut: `epa` (EPA < 0), `success` (misses 40/60/100% of yards to go), `loss` (lost yards, sack, turnover) |
| `adaptation.mode` | `measured` | `measured`: apply the effect this season's data shows. `assume`: force it at `assumed_strength`. `off`: ignore last week |
| `matchup.defense_weight` | `0.75` | How far the opponent moves projections (0 = ignore, 1 = full) |
| `matchup.shrink_plays` | `40` | Regression to league average for small samples |
| `matchup.defense_labels` | `both` | `auto` labels from data, `manual` from your tags, or `both` |
| `weighting.half_life_weeks` | `4` | Recency: a game this many weeks old counts half |

## Your inputs: `data/manual/`

- `defense_tags.csv`: `team,base_coverage,third_down_blitz,notes`. Example: `BAL,cover_3,heavy,`.
  Coverage shells aren't in public play-by-play, so this is where your film or charting goes.
  Tags feed the matchup splits and the report notes.
- `player_overrides.csv`: `team,player,status`. Use `out` to remove an injured player (his
  volume is redistributed) and `starter` to set the QB. The `player` name must match PFR exactly.

## How a projection is built

1. **Volume**: the team's plays per game, scaled by how many plays the opponent faces.
2. **Pass/run split**: the team's dropback rate, nudged by the opponent's pass rate faced.
3. **Playbook mix** across 11 buckets: pass {short, deep} × {left, middle, right} and run
   {outside left, inside left, middle, inside right, outside right}. It uses the team's
   recency-weighted mix, then adjusts each bucket by how it did last game (adaptation).
4. **Matchup**: each bucket's yards and completion rate × what this defense allows in that
   bucket relative to league average (shrunk).
5. **Players**: each player's share of targets or carries in each bucket × his own shrunk
   efficiency there. Passing totals go to the starting QB.

## What the data can and can't tell you

- PBP gives down, distance, depth (short/deep), direction, run gap, sacks, EPA, and score.
- It does **not** give coverage shell or per-down blitz rate. The automatic `third_down_pressure`
  label uses PFR's season blitz % when available, otherwise the 3rd-down sack rate as a proxy.
  Use `defense_tags.csv` for real coverage and blitz labels.
- `styles.md` → "League: play family vs defense label" shows, for example, deep-pass EPA on
  3rd down against heavy-pressure defenses vs. light ones. That table is the evidence behind
  calls like "the deep ball is an option."

## Layout

```
nfl_proj/scrape.py      rate-limited downloader + HTML cache
nfl_proj/parse_pfr.py   PFR tables (incl. ones hidden in HTML comments)
nfl_proj/playparse.py   play text -> type, bucket, yards, passer/target/rusher
nfl_proj/build.py       possession, field position, EPA, success -> SQLite
nfl_proj/profiles.py    offense style, defense profile, labels, matchup splits
nfl_proj/adaptation.py  "do more of what worked" test + last-game signal
nfl_proj/project.py     projection engine
nfl_proj/report.py      markdown reports
tests/                  parser tests + end-to-end run on synthetic PFR-format pages
```
