# Backtest

Weeks 2-5 replayed with only the data available before each week (play-by-play, stats, injury report, depth chart as of that week). Left out because they were gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 produce none.

## Picks (top 5 per game)

- **Overall: 74/119 (62%)** (voids: 6, pushes: 3)
- Week 4: 39/65 (60%)
- Week 5: 35/54 (65%)
- overs: 43/74 (58%)
- unders: 31/45 (69%)
- Rank 1 picks only: 19/29 (66%)

By stat:

| stat        | hit rate    |
|:------------|:------------|
| carries     | 16/19 (84%) |
| completions | 3/7 (43%)   |
| pass_yds    | 11/15 (73%) |
| rec_yds     | 18/22 (82%) |
| receptions  | 12/23 (52%) |
| rush_yds    | 6/11 (55%)  |
| targets     | 8/22 (36%)  |

## Every call, no filters (for comparison)

All over/under calls on players above the usage floor, before the trend gate, signal count and top-5 cut: **162/253 (64%)**. If the picks above beat this, the filters are adding value.

Hit rate by model edge (quartiles): does a bigger edge win more often?

| edge_bin        | hit rate    |
|:----------------|:------------|
| (-0.001, 0.158] | 36/64 (56%) |
| (0.158, 0.224]  | 38/64 (59%) |
| (0.224, 0.305]  | 43/63 (68%) |
| (0.305, 0.556]  | 45/62 (73%) |

## Does each filter add anything? (lift over a no-information call)

`no-info rate` = how often a call on that side of the baseline would hit with no model at all (yardage stats land under their own average more often than not, so unders start ahead). `lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.

Unfiltered calls overall:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| all   |  253.00 |       0.64 |           0.50 |   0.14 |

Usage trend agrees with the call (the qualification rule):

| usage trend agrees   |   calls |   hit rate |   no-info rate |   lift |
|:---------------------|--------:|-----------:|---------------:|-------:|
| False                |  129.00 |       0.67 |           0.52 |   0.15 |
| True                 |  124.00 |       0.61 |           0.48 |   0.13 |

Number of agreeing signals:

|   n_signals |   calls |   hit rate |   no-info rate |   lift |
|------------:|--------:|-----------:|---------------:|-------:|
|           0 |   16.00 |       0.75 |           0.51 |   0.24 |
|           1 |   70.00 |       0.67 |           0.51 |   0.16 |
|           2 |   84.00 |       0.65 |           0.51 |   0.15 |
|           3 |   56.00 |       0.59 |           0.48 |   0.11 |
|           4 |   22.00 |       0.64 |           0.48 |   0.15 |
|           5 |    4.00 |       0.25 |           0.46 |  -0.21 |
|           6 |    1.00 |       0.00 |           0.53 |  -0.53 |

Top-5 picks:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| picks |  119.00 |       0.62 |           0.48 |   0.14 |

## Where the team-total miss comes from

Projected vs actual per team-game for each piece of the scoring model (`corr` near 0 = the model can't tell teams apart on that piece; `sd_projected` far above `sd_actual` x corr = projections spread too wide).

| component     |   projected |   actual |   bias |   mae |   corr |   sd_projected |   sd_actual |
|:--------------|------------:|---------:|-------:|------:|-------:|---------------:|------------:|
| plays         |       60.15 |    61.52 |  -1.37 |  6.67 |   0.06 |           1.65 |        8.69 |
| dropbacks     |       36.20 |    37.56 |  -1.36 |  7.28 |   0.05 |           3.38 |        8.71 |
| pass_att      |       31.85 |    33.44 |  -1.60 |  6.82 |   0.23 |           3.49 |        8.59 |
| runs          |       23.94 |    23.95 |  -0.01 |  4.82 |   0.17 |           3.45 |        5.84 |
| sacks         |        2.28 |     2.26 |   0.02 |  1.58 |  -0.00 |           1.33 |        1.54 |
| interceptions |        0.71 |     0.69 |   0.02 |  0.71 |   0.03 |           0.30 |        0.80 |
| pass_td       |        1.60 |     1.55 |   0.05 |  0.88 |   0.29 |           0.44 |        1.16 |
| rush_td       |        0.97 |     0.93 |   0.04 |  0.90 |  -0.06 |           0.44 |        1.01 |
| td            |        2.56 |     2.48 |   0.09 |  1.10 |   0.22 |           0.57 |        1.41 |
| fga           |        1.92 |     2.10 |  -0.18 |  1.38 |  -0.12 |           1.03 |        1.23 |
| fgm           |        1.62 |     1.79 |  -0.16 |  1.27 |  -0.07 |           0.88 |        1.24 |
| points        |       22.71 |    22.96 |  -0.25 |  7.74 |   0.17 |           4.11 |        9.39 |

| part                                           |   share of points-miss variance |
|:-----------------------------------------------|--------------------------------:|
| touchdowns (x6.95)                             |                            0.88 |
| field goals (x3)                               |                            0.10 |
| other (defensive / return TDs, 2-pt, safeties) |                            0.03 |

Actual drives per team-game: 10.5 (sd 1.6); points per drive 2.23 (sd 0.98). Correlation of the points miss (actual - projected) with drive count: +0.02; with points per drive: +0.84. Red-zone trips per game 3.2, red-zone TD rate 59%.

## Player projections vs a naive season average

Mean absolute error on players who got the ball (lower is better).

| stat        |      n |   model_mae |   naive_mae | model_better   |
|:------------|-------:|------------:|------------:|:---------------|
| carries     | 453.00 |        2.65 |        2.88 | True           |
| completions | 127.00 |        5.07 |        5.51 | True           |
| pass_yds    | 127.00 |       64.02 |       72.25 | True           |
| rec_yds     | 904.00 |       21.17 |       22.05 | True           |
| receptions  | 904.00 |        1.59 |        1.64 | True           |
| rush_yds    | 453.00 |       17.05 |       18.17 | True           |
| targets     | 904.00 |        2.11 |        2.05 | False          |

## Team totals

Mean absolute error in points per team-game (lower is better).

| source                |   MAE |
|:----------------------|------:|
| model (final)         |  7.74 |
| model (before script) |  7.70 |
| market implied total  |  7.02 |
| team's season average |  8.85 |

By week:

|   week |   model |   market |   season_avg |
|-------:|--------:|---------:|-------------:|
|      2 |    8.99 |     8.28 |        12.06 |
|      3 |    8.55 |     7.36 |         8.03 |
|      4 |    5.98 |     5.58 |         7.35 |
|      5 |    7.41 |     6.85 |         7.91 |
