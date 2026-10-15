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
