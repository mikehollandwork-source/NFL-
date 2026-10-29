# Factor tests

Every candidate factor is tested on games it wasn't fit on. Verdicts: **use** = t >= 2.5 with the expected sign; weak = t 1.7-2.5 (not used; revisit with more data); noise = not used.

## 0. How fast team rates become signal (2021-25, odd vs even weeks)

k = plays before a team's rate is trusted at 50% (the model's [matchup] shrink_plays).

| rate               | side    |   split_half_r |   plays_per_half |   k_half_signal |
|:-------------------|:--------|---------------:|-----------------:|----------------:|
| rush yards/carry   | offense |           0.35 |           174.71 |          324.81 |
| rush yards/carry   | defense |           0.31 |           174.71 |          380.09 |
| pass yards/attempt | offense |           0.63 |           255.98 |          152.56 |
| pass yards/attempt | defense |           0.20 |           255.98 |         1013.14 |
| completion rate    | offense |           0.48 |           255.98 |          273.80 |
| completion rate    | defense |           0.35 |           255.98 |          467.40 |
| dropback EPA       | offense |           0.52 |           269.42 |          245.65 |
| dropback EPA       | defense |           0.15 |           269.42 |         1574.84 |
| sack rate          | offense |           0.49 |           269.42 |          284.18 |
| sack rate          | defense |           0.20 |           269.42 |         1074.40 |
| pass TD / attempt  | offense |           0.39 |           255.98 |          408.36 |
| pass TD / attempt  | defense |          -0.03 |           255.98 |          inf    |
| run TD / carry     | offense |           0.35 |           174.71 |          317.82 |
| run TD / carry     | defense |           0.06 |           174.71 |         2923.55 |
| INT / attempt      | offense |           0.05 |           255.98 |         4430.03 |
| INT / attempt      | defense |           0.14 |           255.98 |         1591.75 |

## 1. Run type (team-game yards per carry, weeks 6+, 2021-25; box count 2022-25)

Each row adds one feature to the baseline (offense and defense overall rushing rate, from earlier weeks only). A real effect has a coefficient near 1 and t above 2.5.

| model                                                       |   games |   b_off |   b_def |   t_new | verdict          |   b_f_lane |   b_f_box |   b_f_form |
|:------------------------------------------------------------|--------:|--------:|--------:|--------:|:-----------------|-----------:|----------:|-----------:|
| overall offense + defense                                   |    1930 |    0.63 |    0.63 |  nan    | baseline         |     nan    |    nan    |     nan    |
| + defense weakness by lane x offense lane tendency          |    1930 |    0.64 |    1.01 |   -1.27 | noise (not used) |      -0.50 |    nan    |     nan    |
| + offense vs box count x defense box tendency               |    1546 |    0.41 |    0.66 |    0.61 | noise (not used) |     nan    |      0.19 |     nan    |
| + defense by shotgun / under centre x offense formation mix |    1930 |    0.63 |    0.27 |    1.12 | noise (not used) |     nan    |    nan    |       0.31 |

## 2. Line continuity (season-to-season, 2021->25)

carryover = share of last season's deviation from league that repeats this season. If returning linemen matter, carryover is higher when continuity (share of this season's OL / DL snaps by players who were on the same line last season, 200+ snaps) is high. low / high = 25th / 75th percentile of continuity.

| side   | metric       |   pairs |   carryover_avg |   carryover_low_cont |   carryover_high_cont |   t_interaction | verdict          |
|:-------|:-------------|--------:|----------------:|---------------------:|----------------------:|----------------:|:-----------------|
| off    | rush_ypc     |     124 |            0.32 |                 0.33 |                  0.32 |           -0.06 | noise (not used) |
| off    | rush_epa     |     124 |            0.27 |                 0.24 |                  0.29 |            0.54 | noise (not used) |
| off    | sack_rate    |     124 |            0.46 |                 0.47 |                  0.45 |           -0.15 | noise (not used) |
| off    | dropback_epa |     124 |            0.47 |                 0.44 |                  0.49 |            0.38 | noise (not used) |
| def    | rush_ypc     |     125 |            0.22 |                 0.26 |                  0.17 |           -0.63 | noise (not used) |
| def    | rush_epa     |     125 |            0.19 |                 0.23 |                  0.13 |           -0.77 | noise (not used) |
| def    | sack_rate    |     125 |            0.01 |                -0.06 |                  0.10 |            1.29 | noise (not used) |
| def    | dropback_epa |     125 |            0.04 |                 0.05 |                  0.04 |           -0.11 | noise (not used) |

## 4. Defensive play caller (season-to-season, 2022->25)

carryover_same_dc / new_dc = share of last season's deviation from league that repeats when the coordinator stays / changes (t_change tests the difference). follows_dc = for coordinators who moved teams, how much of their OLD defense's deviation shows up in their new defense, beyond the new team's own last season. Coordinators from (data/external/coordinators.csv, 2022-25 from public staff lists); the defensive play caller is used where it isn't the coordinator (e.g. a head coach who calls the defense).

| metric             |   pairs |   carryover_same_dc |   carryover_new_dc |   t_change | verdict_change   |   movers |   follows_dc |   t_follow | verdict_follow   |
|:-------------------|--------:|--------------------:|-------------------:|-----------:|:-----------------|---------:|-------------:|-----------:|:-----------------|
| rush_ypc           |      96 |                0.23 |              -0.01 |      -1.24 | noise (not used) |       10 |         0.40 |       1.87 | weak (not used)  |
| rush_epa           |      96 |                0.32 |              -0.19 |      -2.47 | weak (not used)  |       10 |        -0.20 |      -0.48 | noise (not used) |
| sack_rate          |      96 |                0.49 |              -0.08 |      -2.66 | **use**          |       10 |         0.63 |       1.38 | noise (not used) |
| dropback_epa       |      96 |                0.16 |              -0.14 |      -1.18 | noise (not used) |       10 |         0.30 |       0.62 | noise (not used) |
| blitz_rate         |      96 |                0.77 |               0.11 |      -3.96 | **use**          |       10 |         0.42 |       0.85 | noise (not used) |
| light_box_rate     |      96 |                0.47 |               0.09 |      -1.81 | weak (not used)  |       10 |         0.10 |       0.41 | noise (not used) |
| wr_rec_yds_allowed |      96 |                0.32 |              -0.11 |      -2.13 | weak (not used)  |       10 |         0.25 |       0.47 | noise (not used) |
| te_rec_yds_allowed |      96 |                0.12 |               0.56 |       2.03 | noise (not used) |       10 |         0.47 |       1.38 | noise (not used) |
| rb_rec_yds_allowed |      96 |                0.23 |               0.04 |      -0.96 | noise (not used) |       10 |        -0.45 |      -1.22 | noise (not used) |
| te_rec_allowed     |      96 |                0.22 |               0.34 |       0.60 | noise (not used) |       10 |         0.26 |       0.76 | noise (not used) |
| rb_rec_allowed     |      96 |                0.37 |               0.10 |      -1.50 | noise (not used) |       10 |        -0.13 |      -0.50 | noise (not used) |

## 3. Receiver vs the same corners (2021-25 player-games)

Residual = result minus the receiver's own 8-game average, minus what that defense allows every receiver that season. carryover = how much of his residual in earlier games against any of today's starting corners (60%+ of snaps, any team) repeats today. Free data has no per-play coverage assignment, so 'faced the corner' means the corner started in that game.

| history                     | stat       |   games |   carryover |      t | verdict          |
|:----------------------------|:-----------|--------:|------------:|-------:|:-----------------|
| same defense, different CBs | rec_yds    |     421 |       0.044 |  0.693 | noise (not used) |
| same defense, different CBs | receptions |     421 |       0.055 |  0.914 | noise (not used) |
| shared starting CB          | rec_yds    |    2034 |       0.031 |  1.070 | noise (not used) |
| shared starting CB          | receptions |    2034 |      -0.006 | -0.192 | noise (not used) |

## 5. What a defense allows by position group (2021-25, odd vs even weeks, ~8 games each)

"Can't cover tight ends" style splits: a real trait repeats between halves of a season.

| measure                                    |   split_half_r | verdict     |
|:-------------------------------------------|---------------:|:------------|
| yards/target vs WR, beyond defense overall |           0.00 | noise       |
| yards/target vs TE, beyond defense overall |           0.00 | noise       |
| yards/target vs RB, beyond defense overall |          -0.06 | noise       |
| share of targets to WR                     |           0.17 | noise       |
| share of targets to TE                     |          -0.01 | noise       |
| share of targets to RB                     |           0.31 | real (weak) |

## 6. Individual corners (PFR coverage charting, seasons 2024, 2025)

k_targets = targets before a defender's own rate is trusted at 50% ([corners] shrink_targets).

| measure                  |   defenders |   targets_per_half |   split_half_r |   k_targets |
|:-------------------------|------------:|-------------------:|---------------:|------------:|
| yards per target allowed |         405 |              29.46 |           0.16 |      159.42 |
| completion % allowed     |         405 |              29.46 |           0.31 |       65.43 |

## 7. What a defense keeps giving up this season (2021-25, odd vs even weeks)

Repeats = the same defense shows it in both halves of a season. Also tested beyond the defense's overall pass rate: deep yards/attempt r = 0.19 and yards after catch r = 0.20 (both real); direction (left / middle / right) r = 0.05 (noise).

| what the defense gives up          |   odd_vs_even_r |   plays_per_half |   k_plays |   trust_after_5_games | verdict   |
|:-----------------------------------|----------------:|-----------------:|----------:|----------------------:|:----------|
| completion % allowed               |            0.35 |           255.98 |    467.40 |                  0.24 | repeats   |
| explosive run rate (10+) allowed   |            0.32 |           174.71 |    369.41 |                  0.22 | repeats   |
| run yards/carry allowed            |            0.31 |           174.71 |    380.09 |                  0.21 | repeats   |
| pass rate faced (1st/2nd down)     |            0.25 |           344.16 |   1027.06 |                  0.16 | repeats   |
| deep attempt share faced (air 15+) |            0.24 |           238.91 |    767.52 |                  0.15 | repeats   |
| deep yards/attempt allowed         |            0.21 |            47.89 |    177.24 |                  0.14 | repeats   |
| pass yards/attempt allowed         |            0.20 |           255.98 |   1020.27 |                  0.13 | repeats   |
| sack rate                          |            0.20 |           269.42 |   1074.40 |                  0.13 | repeats   |
| yards after catch allowed          |            0.17 |           155.45 |    756.13 |                  0.11 | repeats   |
| turnovers forced per play          |            0.15 |           444.12 |   2516.09 |                  0.09 | repeats   |
| 3rd/4th down conversion allowed    |            0.09 |            99.96 |   1069.43 |                  0.05 | noise     |
| red-zone TD rate allowed           |            0.03 |            66.52 |   2377.22 |                  0.02 | noise     |
| explosive pass rate (20+) allowed  |            0.02 |           255.98 |  11077.34 |                  0.01 | noise     |
| scramble rate allowed              |           -0.07 |           269.42 |    inf    |                  0.00 | noise     |

## 8. Third downs, sacks and moving the ball (2021-25, points per drive)

Team-games from week 6 on, predicted from that season's earlier weeks
(offense rate and opponent defense rate vs league); each season held out
in turn. Baseline = what the model already uses (yards per play, TD rate).
Points MAE = |predicted - actual points per drive| x drives.

| added to baseline | points MAE | change | 95% CI | seasons better |
|:--|--:|--:|:--|--:|
| (league average only) | 8.117 | | | |
| baseline: yards/play + TD rate | 7.724 | | | |
| 3rd-down conversion (offense) | 7.699 | -0.025 | [-0.062, +0.012] | 4/5 |
| success rate (offense + defense) | 7.702 | -0.022 | [-0.063, +0.021] | 4/5 |
| **3rd-down (offense) + success rate** | **7.692** | **-0.033** | [-0.082, +0.015] | 4/5 |
| + yards per drive | 7.695 | -0.030 | | 4/5 |
| explosive plays | 7.720 | -0.004 | | |
| sacks | 7.727 | +0.003 | [-0.015, +0.021] | 2/5 |

Used: offense 3rd-down conversion, offense success rate, defense success
rate allowed, as a scoring multiplier ([scoring] drive_eff, capped +/-15%).
Not used: defense 3rd-down rate allowed (noise, section 7), sacks (already in
the model through sack rate on volume; nothing extra for scoring), yards per
drive (nothing beyond success rate).

Full-model backtest with the multiplier on vs off (backtest_DE_*): 2025
weeks 6-18 team MAE 7.768 -> 7.734 (pick lift 0.100 -> 0.099); 2026 weeks
2-5 team MAE 7.856 -> 7.987 (pick lift 0.167 -> 0.147); projections spread
widened (sd 3.6 -> 4.4). Not consistently better, so it is **off**
([scoring] drive_eff = {}); the weights stay in the config comment.

## 9. Pass zones: offense success and defense completions allowed by area (2021-25)

Six zones (short/deep x left/middle/right), team-game level, weeks 5+, season-to-date inputs, each season held out
(`tools/pass_zone_test.py`). Adding offense-in-zone and defense-allowed-in-zone rates to the overall rates:
completion % error -0.42%, EPA/attempt error -0.07% (both within noise). Split-half repeatability of a team's zone
effect beyond its overall rate and the league's zone rate: defense r = 0.08, offense r = 0.01 (no zone above 0.16).
Verdict: noise beyond what the model already uses (overall pass defense + deep share / deep efficiency). Not used.

## 10. Missing defensive starters (2021-25)

Starter = 60%+ of defensive snaps over his previous 3 games; missing = under 20% this game (`tools/def_injury_test.py`).
2,238 defense-games from week 4, defense and opposing offense season-to-date as baseline, each season held out.
Per missing starter: CB +0.040 EPA/dropback (t 3.6) and +0.016 EPA/rush (t 1.9); LB +0.035 EPA/dropback (t 2.7);
S +0.024 EPA/rush (t 2.6); EDGE / interior line not significant (few cases). Out-of-sample error: pass EPA -0.5%,
all plays -0.8%. Implemented as opponent yards-per-play multipliers in `nfl_proj/def_injuries.py`. Projection backtest (on vs off,
same code): prop log-loss 2025 wk 4-18 0.6536 -> 0.6532, 2026 wk 3-6 0.6530 -> 0.6522; team points unchanged;
yardage MAE mixed (pass yds 2026 -0.9, but rec / rush yds slightly worse both seasons). Too small and mixed to
adopt: left OFF.

## 11. Star receiver efficiency prior (ON, receivers only) and backup-RB carries as a win tell (no)

**Star prior.** Receivers' yards per target were shrunk toward the team average (k=25), so proven
efficient receivers with few targets this season were pulled down. Variant: shrink toward the player's
own 2025 rate vs his team (capped, regressed by volume, k=60). Same code, on vs off:

| | 2025 wk 4-18 off | on (rec) | 2026 wk 3-6 off | on (rec) |
|---|---|---|---|---|
| Prop log-loss, all | 0.6536 | 0.6522 | 0.6530 | 0.6512 |
| Receiving props | 0.6559 | 0.6535 | 0.6457 | 0.6425 |
| Rec yds MAE | 18.28 | 18.20 | 19.49 | 19.36 |
| Top-40 WR/TE rec yds bias | -5.8 | -3.4 | -6.5 | -3.5 |

Applying it to rushers too: rushing props 0.6713 -> 0.6779 in 2026. Enabled for receivers only.

**Backup-RB tell.** Both top-2 RBs' projected carries minus their season averages (484 team-games,
2025 wk 4-18 + 2026 wk 3-6): adds +0.7 pt win chance per carry beyond the market spread (t 1.0),
+0.5 pt cover (t 0.6). Both backs projected above their usual: 50% win, 50% cover (n 119). No tell.

## 12. Underdog wins and rushing (2021-26, weeks 4+, `tools/dog_rush_study.py`)

1,130 games; underdogs won 33.4%, covered 50.0%. Spread used only to label underdog / cover.

**After the game** underdog wins look like a rushing story: dog 29.8 runs vs fav 21.1 (losses: 21.3 vs 28.9),
dog's runs +5.7 over its usual, lead back +3.4 carries. That is game script from leading, not a cause.

**Before the game**, 17 rushing signals from prior weeks only (rush EPA / YPC matchups, neutral run rate,
last-3 trends in runs and lead-back carries, run-defense trends). Chosen on 2021-23, checked on 2024-26.
No signal clears noise (one sd: corr 0.04-0.045, 20% bucket cover 4-5 pts):
- Best in 2021-23, lead back's carries rising: 62.3% cover -> 50.5% in 2024-26. Did not repeat.
- Underdog's team runs rising (last 3 vs season), top 20%: 59.2% -> 54.6%; by season 55/61/61/53/60/33 (2026 n=9).
  Pooled 57% on 227, about 2 sd, but it is the best of 17 tries. Watchlist only, not a bet.
- Underdog's rush EPA + favorite's run defense allowed: 50.0% -> 56.7%. Inconsistent.

## 13. Parlay backtest regraded (first-TD grading bug)

First-TD legs had been graded as wins if the player scored first in any game this season. Graded on
that week's game: first-TD tickets 0 of 3 (1 of 12 legs won, 8%), not 1 of 3. All types, weeks 2-6:
65 tickets, 2 hits (both 9-13 leg milestone tickets, +6.3 and +4.7), $11 back on $65 (-83%).
First-TD model: each game's top pick scored first 11.9% vs 16.4% predicted (2025-26, 285 games);
chances above 10% are now shrunk (keep 45% of the excess).

## 14. Lead back returning from a missed game (2021-25, 103 returns) -> money-list hold rule, no model change

Lead back (45%+ of RB carries over his last 2-3 games) misses 1-4 games, then returns:
- His share on return vs before: 0.96x after 1 missed game (55 cases), 0.81x after 2, 0.79x after 3+.
  Same in 2021-23 (0.87x overall) and 2024-25 (0.92x).
- The fill-in keeps part of his bump: 31% of RB carries on return vs 22% before the injury (73% while filling in).
The model only treats backs who played in the team's last 2 games as active, so nearly every case
it sees is a 1-game absence, where the share barely changes: no projection change.
The failure on Oct 22 (Woody Marks, Bam Knight, Tyler Allgeier unders at 35-52 point "edges") was
betting before knowing whether the lead back plays. Rule added to `money`: picks on a team whose
lead back (35%+ share, 2+ games) missed its last game and isn't ruled Out are marked HOLD until
game-day inactives post (~90 min before kickoff); after that the projection knows who is active.

## 15. Why projections miss (2025 wk 4-18 + 2026 wk 3-7 backtests, 12,155 projections; `tools/attribution_study.py`, `output/2026/attribution.md`)

Each miss split into team volume + player share + per-touch efficiency + did-not-play (parts add up exactly).
- Player props miss mostly on **share** (targets 61%, carries 50%, receptions 45%); QB props on **team volume
  and per-attempt efficiency** (pass yds 41% / 41%, share 8%).
- Game script: the final margin vs the projected one explains 26% of team carry misses (+0.30 carries per point)
  and 9% of pass-attempt misses: real but unknowable before kickoff.
- Across ALL projected players the bias is ~0 (targets -0.05, carries -0.02 per player), but projections are
  **too spread out**: top players come in under, depth players over. Steady in both seasons (|t| >= 5):
  - RB targets -21% (2025 -0.79, 2026 -1.06), RB receiving yds -24%; mostly share.
  - Each team's top target -14% (both seasons -1.1); WR1s -12%.
  - QB rush attempts -19% (4.5 projected -> 3.9 actual, both seasons); QB rushing yds -20%.
  - Did-not-play costs 5-10% of every stat's miss: projections assume everyone listed plays.
- Volume going to players the model never projected: 4-7% of team targets / carries.
Candidate fixes (none applied; each needs the out-of-sample backtest): stronger shrinkage of player shares
(or a share calibration slope), RB target share, QB carry share, availability probability for Questionable players.
Tracked live in the weekly grade (`nfl_proj/attribution.weekly`, `output/2026/attribution_live.csv`).

## 16. Share flattening (share^b, renormalized per team): ON for targets (b = 0.9), OFF for carries

Fixes the over-spread found in section 15. Same code, b = 1 (current) vs 0.9 vs 0.8 for targets and carries:

| | 2025 wk 4-18: 1.0 / 0.9 / 0.8 | 2026 wk 3-6: 1.0 / 0.9 / 0.8 |
|---|---|---|
| Targets MAE | 2.300 / 2.244 / 2.207 | 2.602 / 2.552 / 2.520 |
| Receptions MAE | 1.691 / 1.662 / 1.640 | 1.901 / 1.866 / 1.846 |
| Rec yds MAE | 22.55 / 22.14 / 21.77 | 24.58 / 24.04 / 23.69 |
| Carries MAE | 3.935 / 3.840 / 3.837 | 3.863 / 3.782 / 3.757 |
| Top-target bias | -14% / -8% / -1% | -13% / -7% / -1% |
| Receiving-prop log-loss | 0.6543 / 0.6525 / 0.6556 | 0.6471 / 0.6456 / 0.6472 |
| Rush-attempt prop log-loss | 0.6383 / 0.6455 / 0.6626 | 0.6415 / 0.6441 / 0.6705 |

b = 0.9 for targets: chosen on 2025, holds on 2026. Carries: averages improve but the rush-attempt prop
probabilities get worse in both seasons (the only stat with a market edge), so carries stay unflattened.
RB target over-projection (-19% / -25%) is unchanged by flattening: a separate fix to test.

## 17. Touchdown "tells" (week 7 scorers vs non-scorers; tested on 2025 wk 4-18 + 2026 wk 3-7, 3,255 RB/WR/TE games; `tools/td_tells.py`)

Week 7 (155 players with 3+ touches/game, 46 scored): scorers had more touches (10.5 vs 7.2/game), red-zone
touches (1.7 vs 1.1), inside-10 touches (0.9 vs 0.5), last-3 touches (11.2 vs 7.4) and fewer games since a TD.
Tested beyond the model's TD chance (logistic, both seasons):
- vs the simulation alone, volume, red-zone and inside-10 touches add signal in both seasons (t 2.1-3.2).
- vs the LIVE blended chance (simulation + stats TD model): nothing adds reliably (all |t| < 2 in at least one
  season; best inside-10 touches t 0.9 / 1.8). The blend already uses those numbers.
- No signal at all: end-zone targets, TDs so far, games since last TD ("due"), recent usage trend, team TDs/game.
Blended chance is calibrated: 50-60% -> 52% scored, 40-50% -> 40%, 20-30% -> 28%. No change made.

## 18. Team-specific touchdowns (`tools/td_teams.py`, `output/2026/td_teams.md`): small team adjustment ON

Live blended TD chance, RB/WR/TE with 3+ touches/game. Overall it's calibrated (2025: 27.4% scored vs 26.5%;
2026: 28.5% vs 27.6%; RB and WR exact).
- Team miss, odd vs even weeks within a season: r +0.01 (2025), +0.12 (2026): little within-season signal.
- Team miss 2025 -> 2026 (league-adjusted): r +0.41; 20 of 32 teams missed in the same direction both years.
- Out-of-sample test: team log-odds adjustment fit on 2025 (shrunk), applied to 2026: log-loss 0.5702 -> 0.5678
  (k=50) / 0.5683 (k=100); 93% of game-clustered bootstrap draws favor it. Shipped with k=100 (not tuned on 2026):
  `data/models/td_team_adj.json`, -0.15 (MIN, LVR) to +0.16 (LAR, SFO) log-odds = about -3 to +4 points at 30%.
  Refit each season from the previous season's results (tools/td_teams.py rows).
- Tight ends scored above the model in 2025 (27.0% vs 22.3%, t 2.3) but not clearly in 2026 (25.5% vs 24.1%);
  a TE bump fit on 2025 did not help 2026 (0.5703 vs 0.5702): left off.

## 19. Free data sources checked (Oct 28) and Sleeper's free projections vs ours

- nflverse participation (per-play players on field, personnel, box count, coverage, route of the target):
  free for 2025 and earlier; 2026 not published yet (404), so usable for building/fitting, not live inputs.
- nflverse Next Gen Stats rushing (box-count %, rush yards over expected): free, current through 2026 wk 7.
- Sleeper stats endpoint: no routes; adds drops, broken tackles, red-zone targets/attempts (we already have).
- Sleeper projections (api.sleeper.app/v1/projections/nfl/regular/<yr>/<wk>, free, history back to 2025):
  average miss vs ours (players above prop-relevant volume):

| stat | 2025 ours / Sleeper / 50-50 | 2026 wk 3-6 ours / Sleeper / 50-50 |
|---|---|---|
| carries | 3.82 / 3.62 / 3.62 | n/a (too few matched) |
| targets | 2.10 / 1.87 / 1.93 | 2.49 / 2.22 / 2.31 |
| receptions | 1.56 / 1.44 / 1.47 | 1.72 / 1.52 / 1.61 |
| rec yds | 20.48 / 19.85 / 19.86 | 22.55 / 21.23 / 21.45 |
| pass yds | 59.80 / 58.02 / 57.49 | 59.47 / 55.52 / 56.78 |

Caveats: our backtest runs without injury news (as-of), while Sleeper's stored projections are their final
pre-game numbers (injuries known, and likely built partly from betting lines, which our rule 2 excludes).
Not used as a model input. Candidate use pending the owner's decision: a disagreement filter (hold money
picks where our rush-attempt projection differs sharply from Sleeper's), to be backtested vs Kalshi first.

## 20. Sleeper disagreement filter for the money list: REJECTED (`tools/sleeper_filter_test.py`)

Rush-attempt bets with edge 10+ vs the Kalshi close (2026 weeks 2-6, YES at ask / NO at 1 - bid): 147 bets,
38% won, ROI +25%. Filter: hold a bet when Sleeper's free pre-game projection sits on the losing side of the line.
- Sleeper disagreed with 120 of 146 (82%): our edge bets ARE disagreements with consensus, and Sleeper ~ consensus.
- Held bets ROI +24% vs kept +20%; kept beat held in only 45% of bootstrap draws.
- Holding only big disagreements made it worse: Sleeper 3+ carries against us -> held 45 bets at +63% ROI,
  kept 101 at +6%. The more Sleeper disagreed, the better our bets did.
Conclusion: the rush-attempt edge comes from information consensus projections don't use; filtering toward
consensus removes it. Not shipped. Bogus injury-guess edges stay handled by the HOLD rule (section 14).

## 21. Questionable but playing: share haircut ON (`[players] questionable_targets = 0.95`, `questionable_carries = 0.85`)

Bets lock after game-day inactives, so a chance-of-playing discount changes no bet. What does matter: players
listed Questionable who suit up get fewer touches than projected (2025 wk 4-18 + 2026 wk 3-7 backtests):

| | Questionable, played | everyone else |
|---|---|---|
| Carries vs projection | -18% (n 42, t -3.1; 2025 -17%, 2026 -22%) | -3% |
| Targets vs projection | -11% (n 119, t -2.7; 2025 -10%, 2026 -15%) | -5% |
| Questionable players who did not play (backtests use the report, not inactives) | 24-31% | 4-5% |

Factors set from 2025 (relative to everyone else); the cut volume goes to teammates. Same code, off vs on:

| | 2025 wk 4-18: off / on | 2026 wk 3-7 (out of sample): off / on |
|---|---|---|
| Carries MAE | 3.936 / 3.913 | 3.976 / 3.947 |
| Rush-attempt prop log-loss | 0.6385 / 0.6376 | 0.6586 / 0.6569 |
| Receiving-prop log-loss | 0.6530 / 0.6531 | 0.6433 / 0.6427 |
| All props log-loss | 0.6513 / 0.6512 | 0.6518 / 0.6511 |
| Questionable players' props (2026, n 146) | | 0.6633 / 0.6554 |

Carries vs Kalshi closes (2026 wk 2-6, `tools/kalshi_backtest.py`): model log-loss 0.6850 -> 0.6796; edge >= 10
bets: 159 at +37.8% -> 160 at +34.7%. On identical markets only 4 of 268 bets change side (2 wins, 2 losses
either way); the ROI gap comes from different strikes being picked, i.e. noise. Edge intact.
Live: `espn_injuries.live` now marks Questionable players cleared by the active list "active (was Questionable)"
so the haircut still applies at lock time.

## 22. Rejected: recent-share blend, team pace model; RB target bias explained

**Recent-share blend** (`[players] recent_blend_targets / recent_blend_carries`, code kept, off). `tools/share_lab.py`:
share misses are mostly luck. Error from share alone (targets per player-game): model 1.506 / 1.635 (2025 / 2026),
an estimator that knew the player's whole-season share 1.439 / 1.551, pure binomial luck 1.196 / 1.243. Carries:
model 1.203 / 1.205, season-share oracle 1.223 / 1.191. So at most ~4% is left to win on targets, ~0 on carries.
Mixing the model share 50/50 (targets) and 75/25 (carries) with a 3-game weighted recent share helped in the
share-only lab, but the full 2026 backtest got worse: receiving-prop log-loss 0.6433 -> 0.6454, rush-attempt
props 0.6586 -> 0.6627. Rejected.

**Team volume / pace.** Team-level forecasts already beat simple pace models (season average, 3-game weighted,
opponent-adjusted): pass attempts MAE 5.94 vs 6.22 best simple (2025), 6.84 vs 7.39 (2026); team carries (sum of
player projections) 6.11 / 5.53, and blending in the season average makes both seasons worse. The rest of the
team-volume miss is game script (section 15), not knowable before kickoff. No change.

**RB targets (-19% to -25% in section 15).** Over all projected RBs the bias is small: -10% / -5% including
did-not-play, -5% / +2% for RBs who played. The large number appears only among RBs projected 2.5+ targets, i.e.
the high projections regressing. Neither the blend nor the haircut moves it. Left as is.

**Still open:** QB rush attempts are over-projected ~20% in both seasons (-19% / -21%), the largest steady
carries bias left. Candidate for the next test (QB carries are part of the money list).

## 23. Defense play-calling pull ("do teams pass or run more against this defense?"): REJECTED (`tools/def_tendency.py`, `output/2026/def_tendency.md`)

Every play gets an expected pass chance from down, distance, field position, score and clock (league table).
Defense pull = how much more than usual opponents pass against a defense after removing the situation AND each
offense's own lean (the current model instead uses the plain pass share faced, shrunk with k = 1030).

- It exists: spread about 2.4 points of pass rate (~1.5 pass attempts per game). 2026 extremes: LAC -4.5,
  PHI -4.2, MIN -3.7 (opponents run more than usual).
- It repeats in full seasons (odd vs even weeks r 0.49 in 2024, 0.36 in 2025, -0.09 in 2026 after 7 weeks).
- Next-game prediction of the offense's pass residual (b = 0.5 fit on 2024): 2025 miss 3.522 -> 3.482 pass
  attempts (-1.1%, better than the plain faced share, 3.507); 2026 3.259 -> 3.283 (worse).
- Offense style: strong-identity offenses barely bend (slope on the pull: run-first 0.24, pass-first 0.34);
  balanced offenses adapt most (0.58).

In the full model (`[matchup] def_pass_pull`, replacing the plain faced share), no gain in either season:

| | 2025 wk 4-18: now / 0.5 / 0.3 | 2026 wk 3-7: now / 0.5 / 0.3 |
|---|---|---|
| Team pass attempts MAE | 5.938 / 5.951 / 5.976 | 6.831 / 6.830 / 6.832 |
| Team carries MAE | 6.105 / 6.107 / 6.136 | 5.553 / 5.604 / 5.563 |
| Carries MAE | 3.913 / 3.908 / 3.905 | 3.947 / 3.987 / 3.975 |
| Rush-attempt prop log-loss | 0.6376 / 0.6379 / 0.6375 | 0.6569 / 0.6585 / 0.6537 |
| All props log-loss | 0.6512 / 0.6516 / 0.6517 | 0.6511 / 0.6520 / 0.6515 |

The effect is real but ~1 play a game, smaller than the noise, and the existing heavily-shrunk faced share
already captures most of it. Code kept, off (`def_pass_pull = 0` / absent).
