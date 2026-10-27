# Backtest

Weeks 2-5 replayed with only the data available before each week (play-by-play, stats, injury report, depth chart as of that week). Left out because they were gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 produce none.

## Picks (top 5 per game)

- **Overall: 70/116 (60%)** (voids: 7, pushes: 2)
- Week 4: 36/64 (56%)
- Week 5: 34/52 (65%)
- overs: 41/73 (56%)
- unders: 29/43 (67%)
- Rank 1 picks only: 19/29 (66%)

By stat:

| stat        | hit rate    |
|:------------|:------------|
| carries     | 16/18 (89%) |
| completions | 5/9 (56%)   |
| pass_yds    | 7/11 (64%)  |
| rec_yds     | 16/20 (80%) |
| receptions  | 11/20 (55%) |
| rush_yds    | 7/12 (58%)  |
| targets     | 8/26 (31%)  |

## Every call, no filters (for comparison)

All over/under calls on players above the usage floor, before the trend gate, signal count and top-5 cut: **160/257 (62%)**. If the picks above beat this, the filters are adding value.

Hit rate by model edge (quartiles): does a bigger edge win more often?

| edge_bin        | hit rate    |
|:----------------|:------------|
| (-0.001, 0.153] | 36/65 (55%) |
| (0.153, 0.21]   | 41/65 (63%) |
| (0.21, 0.299]   | 41/63 (65%) |
| (0.299, 0.528]  | 42/64 (66%) |

## Does each filter add anything? (lift over a no-information call)

`no-info rate` = how often a call on that side of the baseline would hit with no model at all (yardage stats land under their own average more often than not, so unders start ahead). `lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.

Unfiltered calls overall:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| all   |  257.00 |       0.62 |           0.50 |   0.13 |

Usage trend agrees with the call (the qualification rule):

| usage trend agrees   |   calls |   hit rate |   no-info rate |   lift |
|:---------------------|--------:|-----------:|---------------:|-------:|
| False                |  130.00 |       0.66 |           0.52 |   0.14 |
| True                 |  127.00 |       0.58 |           0.47 |   0.11 |

Number of agreeing signals:

|   n_signals |   calls |   hit rate |   no-info rate |   lift |
|------------:|--------:|-----------:|---------------:|-------:|
|           0 |   18.00 |       0.67 |           0.53 |   0.14 |
|           1 |   88.00 |       0.64 |           0.50 |   0.13 |
|           2 |   84.00 |       0.60 |           0.49 |   0.10 |
|           3 |   47.00 |       0.66 |           0.48 |   0.18 |
|           4 |   18.00 |       0.61 |           0.50 |   0.11 |
|           5 |    2.00 |       0.00 |           0.50 |  -0.50 |

Top-5 picks:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| picks |  116.00 |       0.60 |           0.48 |   0.12 |

## Where the team-total miss comes from

Projected vs actual per team-game for each piece of the scoring model (`corr` near 0 = the model can't tell teams apart on that piece; `sd_projected` far above `sd_actual` x corr = projections spread too wide).

| component     |   projected |   actual |   bias |   mae |   corr |   sd_projected |   sd_actual |
|:--------------|------------:|---------:|-------:|------:|-------:|---------------:|------------:|
| plays         |       60.17 |    61.52 |  -1.35 |  6.65 |   0.07 |           1.65 |        8.69 |
| dropbacks     |       36.25 |    37.56 |  -1.31 |  7.22 |   0.05 |           3.24 |        8.71 |
| pass_att      |       31.91 |    33.44 |  -1.53 |  6.76 |   0.19 |           3.31 |        8.59 |
| runs          |       23.92 |    23.95 |  -0.03 |  4.76 |   0.19 |           3.25 |        5.84 |
| sacks         |        2.26 |     2.26 |  -0.01 |  1.26 |   0.03 |           0.33 |        1.54 |
| interceptions |        0.71 |     0.69 |   0.02 |  0.71 |   0.04 |           0.30 |        0.80 |
| pass_td       |        1.59 |     1.55 |   0.05 |  0.89 |   0.28 |           0.42 |        1.16 |
| rush_td       |        0.97 |     0.93 |   0.04 |  0.90 |  -0.05 |           0.43 |        1.01 |
| td            |        2.56 |     2.48 |   0.09 |  1.10 |   0.21 |           0.55 |        1.41 |
| fga           |        1.91 |     2.10 |  -0.19 |  1.38 |  -0.12 |           1.02 |        1.23 |
| fgm           |        1.62 |     1.79 |  -0.17 |  1.27 |  -0.07 |           0.87 |        1.24 |
| points        |       22.66 |    22.96 |  -0.30 |  7.77 |   0.15 |           4.05 |        9.39 |

| part                                           |   share of points-miss variance |
|:-----------------------------------------------|--------------------------------:|
| touchdowns (x6.95)                             |                            0.87 |
| field goals (x3)                               |                            0.10 |
| other (defensive / return TDs, 2-pt, safeties) |                            0.03 |

Actual drives per team-game: 10.5 (sd 1.6); points per drive 2.23 (sd 0.98). Correlation of the points miss (actual - projected) with drive count: +0.03; with points per drive: +0.84. Red-zone trips per game 3.2, red-zone TD rate 59%.

## Player projections vs a naive season average

Mean absolute error on players who got the ball (lower is better).

| stat        |      n |   model_mae |   naive_mae | model_better   |
|:------------|-------:|------------:|------------:|:---------------|
| carries     | 453.00 |        2.63 |        2.88 | True           |
| completions | 127.00 |        5.08 |        5.51 | True           |
| pass_yds    | 127.00 |       64.23 |       72.25 | True           |
| rec_yds     | 904.00 |       21.19 |       22.05 | True           |
| receptions  | 904.00 |        1.60 |        1.64 | True           |
| rush_yds    | 453.00 |       16.97 |       18.17 | True           |
| targets     | 904.00 |        2.12 |        2.05 | False          |

## Team totals

Mean absolute error in points per team-game (lower is better).

| source                |   MAE |
|:----------------------|------:|
| model (final)         |  7.77 |
| model (before script) |  7.79 |
| market implied total  |  7.02 |
| team's season average |  8.85 |

By week:

|   week |   model |   market |   season_avg |
|-------:|--------:|---------:|-------------:|
|      2 |    9.02 |     8.28 |        12.06 |
|      3 |    8.55 |     7.36 |         8.03 |
|      4 |    5.96 |     5.58 |         7.35 |
|      5 |    7.54 |     6.85 |         7.91 |
