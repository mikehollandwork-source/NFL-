# NFL player projections

Pulls play-by-play, box score stats and snap counts from the free public
[nflverse](https://github.com/nflverse/nflverse-data) data releases, profiles every
offense's play-calling and every defense's weaknesses, tests whether coaches really
"cut what failed and call more of what worked," and projects player stat lines for the
upcoming week.

## Run it

```bash
pip install -r requirements.txt
python -m nfl_proj scrape      # download this season's nflverse files -> data/raw/nflverse/
python -m nfl_proj build       # turn them into data/nfl_2026.db
python -m nfl_proj styles      # coaching styles, defense labels, adaptation test -> output/2026/styles.md
python -m nfl_proj external    # refresh online scheme data (blitz / man / zone / Cover N) from Sharp Football
python -m nfl_proj coaches     # each play-caller's past seasons (nflverse stats) -> coach profiles
python -m nfl_proj project     # next week's projections + props (shows your choices, asks y/N first)
```

Outputs in `output/2026/` (also written to SQLite tables `projections_week_NN` / `props_week_NN`):

- `week_NN_projections.csv`: one row per player with the mean for every stat, plus anytime-TD and first-TD odds.
- `week_NN_props.csv`: one row per player per stat with mean, median, 10/25/75/90th percentiles,
  P(1+), P(2+), and P(over)/P(under) for any line you enter.
- `week_NN_report.md`: per game, the coaching-style notes, matchup notes and prop tables.

## Props covered

5,000 simulated games per matchup. Every prop is read from the same simulations, so they
stay consistent (QB passing yards = the sum of his receivers' yards in each run).

- **QB:** pass attempts, completions, passing yards, pass TDs, interceptions, longest completion,
  rushing yards and carries (designed runs + scrambles), pass+rush yards
- **RB/WR/TE:** carries, rushing yards, rush TDs, longest rush, targets, receptions, receiving
  yards, rec TDs, longest reception, rush+rec yards, anytime TD, 2+ TDs, first TD (approximate)
- **K:** FG attempts, FGs made, XPs made, kicking points
- **Defenders:** tackles + assists, sacks, interceptions
- **All:** PPR fantasy points

To get over/under probabilities, add lines to `data/manual/prop_lines.csv`
(`player,stat,line`, e.g. `Josh Allen,pass_yds,251.5`). Stat names match the `stat` column of
`week_NN_props.csv`.

Re-run `scrape` after each week. nflverse updates the current season's files nightly during the
season, so `scrape` always re-downloads them (about 7 MB).

## Data source

`[source] provider` in `config/projection.toml`:

- `nflverse` (default): structured play-by-play from the NFL's game feed (play type, pass depth and
  direction, run gap, shotgun / no-huddle, EPA, tacklers), weekly player stats, and snap counts.
  Team codes are converted to PFR's (GNB, KAN, LVR, ...) and games keep PFR boxscore ids, so
  `data/manual/` files work unchanged. Player ids are NFL GSIS ids.
- `pfr`: the original Pro-Football-Reference HTML scraper (4s/page). PFR serves a Cloudflare bot
  check to cloud machines (HTTP 403), so this only works from a home connection. It doesn't
  provide the advanced-defense blitz table the nflverse path lacks either way; blitz data comes
  from Sharp (below).

## Your choices: `config/projection.toml`

Every modeling decision is a setting. `project` prints the active choices and waits for a
`y` before it projects anything.

| Setting | Default | Meaning |
|---|---|---|
| `definitions.negative_play` | `custom` | What counts as a play a coach would cut. `custom` (yours): nets 0 or less (incl. incompletions and sacks), a turnover, or a 3rd/4th-down play that doesn't convert. Others: `epa` (EPA < 0), `success`, `loss` |
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
  volume is redistributed) and `starter` to set the QB. The `player` name must match the
  `player` column of `week_NN_projections.csv` exactly.

## Coaching-style traits measured

Pass rate by down and distance (1st & long; 2nd & short/medium/long; 3rd & short/medium/long/very
long), neutral-script and early-down pass rate, shotgun and no-huddle rate, deep-pass share overall and on 3rd down, pass direction
mix, run direction and gap mix, 4th-down go rate, red-zone play mix (short pass / deep pass / run),
red-zone EPA, 3rd-down conversion rate, sack rate, and explosive and negative play rates.

## Coach angle (`data/manual/coaches.csv`)

All 32 teams: head coach, years as an NFL head coach and with this team, who calls plays (HC or OC),
whether the play-caller is new for 2026, and the seasons he called plays before (`caller_history`).
Each row lists its source and confidence. The 2026 hires and play-callers come from 2026 web
reporting; MIN's play-caller was not confirmed in 2026 sources. `coaches` downloads nflverse weekly
player stats for each listed season (pass rate = dropbacks incl. sacks / (dropbacks + carries)) and
computes:

- **Experience tiers**: first-year HC / new to team / young / veteran HC, and first-time / developing
  / veteran play-caller (counted in seasons actually calling plays).
- **Run-first / pass-first**: career pass rate vs league that season, adjusted for game script
  (winning teams run more; the slope is estimated from the scraped seasons).
- **Leans on stars**: career top-receiver target share and RB1 carry share vs league.

In the projection: the play-caller's career pass lean is the early-season prior for pass rate, and his
star reliance pulls the top receiver's and RB1's shares. Both count as `coach.prior_games` games of
evidence, so they fade as this season's games accumulate. First-time or newly arrived play-callers get
a wider volume spread (`coach.new_caller_sd_mult`).

## Defensive scheme (`data/external/defense_scheme.csv` + your tags)

Coverage and blitz data don't exist in play-by-play, so they come from online charting. Every value
has its source, date and confidence. It's seeded with what could be verified from 2026 reporting
(blitz rates for 13 teams, coverage splits for DET/PHI, ARI shells). `external` fills all 32 teams
from Sharp Football Analysis when that site is reachable. Your `defense_tags.csv` always overrides.

Labels: blitz heavy / light (≥33% / ≤20%), man-heavy / zone-heavy (≥30% / ≤18% man), and the
most-used Cover N shell.

In the projection, only the **offense-specific** part of a scheme matchup is used: how this offense
does against, for example, heavy-blitz defenses on 3rd down, compared with how every other offense
does against them. The league-wide part is already in the defense's own allowed stats, so using it
again would double-count. Blitz effects use 3rd/4th-down plays and are weighted by the offense's
3rd/4th-down share. If this offense throws deep more often against blitz-heavy teams, its deep-pass
share goes up in that matchup. Everything is shrunk by `scheme.shrink_plays`, so early-season effects
are small on purpose.

`styles.md` also cross-checks the online blitz labels against the 3rd-down sack rate in the
play-by-play. A heavy-blitz team that isn't getting sacks shows up as a mismatch.

## How a projection is built

1. **Volume**: the team's plays per game, scaled by how many plays the opponent faces.
2. **Pass/run split**: the team's dropback rate, nudged by the opponent's pass rate faced.
0. **Coach prior**: pass rate and star usage start from the play-caller's career tendencies.
3. **Playbook mix** across 11 buckets: pass {short, deep} × {left, middle, right} and run
   {outside left, inside left, middle, inside right, outside right}. It uses the team's
   recency-weighted mix, then adjusts each bucket by how it did last game (adaptation).
4. **Matchup**: each bucket's yards and completion rate × what this defense allows in that
   bucket relative to league average (shrunk), × this offense's scheme interaction effect.
5. **Players**: each player's share of targets or carries in each bucket × his own shrunk
   efficiency there. Passing totals go to the starting QB.
6. **Strength of schedule**: pass yards/dropback, run yards/carry and points/game are re-rated
   against the opponents each team actually faced (additive offense + defense ratings, ridge-shrunk,
   `[sos]`). Each raw input is scaled by adjusted ÷ raw, capped at ±15%. An offense that padded its
   numbers against soft defenses is scaled down; a defense that faced strong offenses gets credit.
7. **Game script** (`[script]`): the model projects both teams' points on its own, and the team
   it projects to lead passes less (0.4% dropback rate per point of projected margin), the
   trailing team more. The betting spread is never used.
   **Market team totals** (`[market]`): the only market input is the implied team total, and only
   for teams that consistently land on it (within 4 points in at least 60% of at least 4 games).
   For those teams 60% of projected points come from the implied total and TD rates (and a little
   yardage) scale to match; every other team is projected from the model alone. The report lists
   which teams qualify and why.
8. **Availability** (`[availability]`): the injury report marks Out (and Doubtful) players out.
   Before the week's report posts (Wed-Fri), players Out last week who also missed last week's
   game are carried as out. The starting QB is the depth chart's QB1 unless he's out or hasn't
   played recently, in which case last game's starter is used and the report flags it. Your
   `player_overrides.csv` always wins. Rows written to `week_NN_availability.csv`.

9. **Cornerbacks** (`[corners]`): each defensive back's yards allowed per target (PFR coverage
   charting, shrunk toward league average) and the live depth chart (LCB / RCB / nickel). When
   defensive backs are out, their share of targets goes to a replacement-level corner and the
   opposing wide receivers' yards per target rise by this week's coverage ÷ the season's.
   When `defense_personnel.csv` names a shadow corner and he plays, the offense's top WR spends
   70% of his routes against him; the other WRs face the group without him. Capped at ±20%.

10. **Team totals** are simulated: 6 x touchdowns + extra points (the kicker's own rate) + 3 x field
    goals (the kicker's own volume and accuracy), QB scramble TDs included. A first simulation pass
    without game script gives each team's model total; the projected margin then sets game script.
11. **Defensive weak spots** (`[defense]`): how each defense does against WRs, TEs and RBs relative to
    its own average (feeds receiver projections), plus persistent weak spots (deep, short, inside /
    outside runs, 3rd down, red zone, play action, explosives) in the report.
12. **Struggle weeks**: games where a defense allowed clearly more EPA/play than its norm, each with a
    diagnosis (which plays and positions broke down, 3rd down / red zone, the blitz, explosives, the
    opponent's quality, and which regular starters didn't play, from snap counts). A struggle played
    without starters who are available now counts half toward that defense's allowed rates.
13. **Comparable offenses** (`[comps]`): offenses described by structure (neutral and early-down pass
    rate, deep share, shotgun, no-huddle, play action, screens, motion, scrambles, outside runs, box
    faced). How structurally similar offenses did against this defense, relative to their own norms
    and beyond how every offense did against it, moves pass and run efficiency (capped at ±12%).

14. **Player-level adaptation** (`[player_adaptation]`): each player's individual plays from last game
    are listed (`week_NN_player_plays.md`). Plays that netted zero or less, turned it over or failed
    on 3rd/4th down are cancelled; the rest are kept. Next week his volume shifts out of the kinds of
    plays that failed and into the kinds he was kept on (his total volume is unchanged), the team's
    play mix is rebuilt from those plans, and each kept play is judged against this week's defense by
    its exact kind (direction, depth, play action, screen). How hard to shift: `mode = "measured"`
    (default) uses the size measured from the data: after a player's plays of one kind all failed,
    his share of that kind drops about 16% next game (2025: 13,741 cases, t = -9.4; 2026: t = -4.4).
    `mode = "assume"` with `cut = 1.0` cancels failed kinds outright; in the backtest that made
    receiving projections slightly worse.
15. **2025 priors** (`[priors]`): small samples are pulled toward the team's own 2025 rates
    (regressed toward league; more for offenses with a new play-caller) instead of league average.
15b. **Streak regression** (`[streaks]`): a player's efficiency weighs every game equally (a hot
    stretch gets no recency boost) and long plays are capped (40 yds receiving, 30 rushing) when
    measuring him. Measured on 2025-26: only 32% of a two-game yards-per-target streak carries into
    the next game (29% for yards per carry; 42% / 48% for targets / carries).
15c. **Clock / possession** (`[volume]`): play volume comes from the shared game clock. Time of
    possession is NOT a stable team trait (2025 first half vs second half r = 0.06; it follows the
    scoreboard), but pace is (seconds per clock-running play, r = 0.70). Drives in the game come from
    both teams' pace and plays per drive (shrunk hard: it barely repeats); each team's plays = drives
    x its plays per drive vs this defense. A slow, drive-sustaining opponent therefore cuts your plays
    too, and projected possession falls out of the model (shown per game in the report). Walk-forward
    test on projected team plays: MAE 6.80 vs 6.91 for the old method (2025), 6.66 vs 6.86 (2026).
16. **Weather** (`[weather]`): wind, cold and rain effects measured from 2025-26 outdoor games and
    applied from the National Weather Service hourly forecast at kickoff (Open-Meteo abroad).
17. **Offensive line** (`[oline]`): per-missing-starter effects measured from 2025-26 team-games,
    applied for starting linemen listed out.

## Top 5 picks per game (`week_NN_picks.csv`, `[picks]`)

Over / under calls against your line (`prop_lines.csv`) or, without one, the player's own season
average. To qualify: 3+ games, real volume (4+ targets or 8+ carries a game; QB rushing excluded),
usage trending the pick's way (rising carries / targets for overs, falling for unders) unless the
player is a consistent-volume star or the starting QB, a 55%+ simulated chance with at least a 6-point
edge from the projection itself (the stat's skew removed), and 2+ agreeing signals (bucket matchup,
coverage / position factor, comparable offenses, usage trend, game script, team total). Ranked by
edge x sample x signal agreement; one pick per player.

## Backtest (`python -m nfl_proj backtest --weeks 2-5` → `backtest.md`)

`--tag NAME` writes `backtest_NAME.*` so variants (e.g. a config with a feature switched off,
`python -m nfl_proj --config other.toml backtest --tag other`) can be compared side by side. The
report includes where the team-total miss comes from: projected vs actual plays, dropbacks, TDs,
field goals, turnovers and sacks, plus drives, points per drive and red-zone trips.

Replays each week with only what was known before it (play-by-play, stats, injury report, depth chart
as of that week) and scores the picks, every unfiltered call, player projections vs a naive season
average, and team totals vs actual (with the market's implied totals for reference).

## Researched defensive personnel (`data/external/defense_personnel.csv`)

Web research on each defense: coordinator, man / zone lean, scheme notes, shadow corner, and the
weak spot opponents attack, each row with source links, date and confidence. Only the shadow
corner feeds the math; the rest is printed in the report under each game ("secondary"). Corner
alignment always comes from the live depth chart, not the research, because rosters change weekly.
Every name was checked against the current rosters. Re-research before trusting it in later weeks.

## What the data can and can't tell you

- PBP gives down, distance, depth (short/deep), direction, run gap, sacks, EPA, and score.
- FTN charting (free, via nflverse) adds per-play blitzers, pass rushers, box count, play action,
  screens, RPOs and motion. The projection uses the per-play blitz split: how much better or
  worse THIS offense does when blitzed than the league does, weighted by how often the opponent
  blitzes. `styles.md` lists every defense's blitz rate (overall and 3rd down) and PFR pressures.
- Still **no** coverage shell (Cover 0-6): the free per-play coverage labels stop after 2024. The automatic `third_down_pressure`
  label uses PFR's season blitz % when available (PFR source only), otherwise the 3rd-down sack
  rate as a proxy.
  Use `defense_tags.csv` for real coverage and blitz labels.
- `styles.md` → "League: play family vs defense label" shows, for example, deep-pass EPA on
  3rd down against heavy-pressure defenses vs. light ones. That table is the evidence behind
  calls like "the deep ball is an option."

## Layout

```
nfl_proj/nflverse.py    nflverse download + mapping to the tables below (default source)
nfl_proj/scrape.py      rate-limited PFR downloader + HTML cache (PFR source)
nfl_proj/parse_pfr.py   PFR tables (incl. ones hidden in HTML comments)
nfl_proj/playparse.py   play text -> type, bucket, yards, passer/target/rusher
nfl_proj/build.py       possession, field position, EPA, success -> SQLite
nfl_proj/profiles.py    offense style, defense profile, labels, matchup splits
nfl_proj/adaptation.py  "do more of what worked" test + last-game signal
nfl_proj/project.py     projection inputs (volume, mix, matchup, player shares)
nfl_proj/sim.py         Monte Carlo game simulation -> every prop
nfl_proj/coaches.py     coach experience, career pass lean, star reliance
nfl_proj/ratings.py     strength of schedule (opponent-adjusted ratings)
nfl_proj/market.py      implied team totals, teams missing them, market blend
nfl_proj/availability.py injury report + depth chart -> outs and starting QB
nfl_proj/corners.py     cornerback coverage quality, injuries, shadow assignments
nfl_proj/defense.py     position-group weakness, struggle-week diagnosis, comparable offenses
nfl_proj/picks.py       usage-trend gate and the top 5 picks per game
nfl_proj/pipeline.py    one week's run, live or replayed as of a past week
nfl_proj/backtest.py    replay and score past weeks
nfl_proj/components.py  actual team-game components (drives, red zone, TDs, FGs) vs projected
nfl_proj/priors.py      2025 team rates as early-season starting points
nfl_proj/weather.py     measured weather effects + NWS / Open-Meteo forecasts
nfl_proj/oline.py       offensive line starters and the measured effect of missing ones
nfl_proj/external.py    online scheme data (Sharp scraper), scheme labels, PBP cross-check
nfl_proj/report.py      markdown reports
tests/                  parser + nflverse mapping tests, end-to-end run on synthetic pages
```
