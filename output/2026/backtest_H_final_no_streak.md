# Backtest

Weeks 2-5 replayed with only the data available before each week (play-by-play, stats, injury report, depth chart as of that week). Left out because they were gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 produce none.

## Picks (top 5 per game)

- **Overall: 71/113 (63%)** (voids: 6, pushes: 2)
- Week 4: 38/61 (62%)
- Week 5: 33/52 (63%)
- overs: 40/70 (57%)
- unders: 31/43 (72%)
- Rank 1 picks only: 23/30 (77%)

By stat:

| stat        | hit rate    |
|:------------|:------------|
| carries     | 16/20 (80%) |
| completions | 4/6 (67%)   |
| pass_yds    | 8/13 (62%)  |
| rec_yds     | 19/25 (76%) |
| receptions  | 11/21 (52%) |
| rush_yds    | 6/11 (55%)  |
| targets     | 7/17 (41%)  |

## Every call, no filters (for comparison)

All over/under calls on players above the usage floor, before the trend gate, signal count and top-5 cut: **162/257 (63%)**. If the picks above beat this, the filters are adding value.

Hit rate by model edge (quartiles): does a bigger edge win more often?

| edge_bin        | hit rate    |
|:----------------|:------------|
| (-0.001, 0.164] | 38/68 (56%) |
| (0.164, 0.208]  | 37/62 (60%) |
| (0.208, 0.3]    | 39/64 (61%) |
| (0.3, 0.536]    | 48/63 (76%) |

## Does each filter add anything? (lift over a no-information call)

`no-info rate` = how often a call on that side of the baseline would hit with no model at all (yardage stats land under their own average more often than not, so unders start ahead). `lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.

Unfiltered calls overall:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| all   |  257.00 |       0.63 |           0.50 |   0.13 |

Usage trend agrees with the call (the qualification rule):

| usage trend agrees   |   calls |   hit rate |   no-info rate |   lift |
|:---------------------|--------:|-----------:|---------------:|-------:|
| False                |  137.00 |       0.64 |           0.52 |   0.12 |
| True                 |  120.00 |       0.62 |           0.47 |   0.14 |

Number of agreeing signals:

|   n_signals |   calls |   hit rate |   no-info rate |   lift |
|------------:|--------:|-----------:|---------------:|-------:|
|           0 |   21.00 |       0.71 |           0.55 |   0.17 |
|           1 |   70.00 |       0.60 |           0.50 |   0.10 |
|           2 |   82.00 |       0.63 |           0.51 |   0.12 |
|           3 |   60.00 |       0.63 |           0.48 |   0.15 |
|           4 |   18.00 |       0.72 |           0.47 |   0.25 |
|           5 |    6.00 |       0.33 |           0.43 |  -0.10 |

Top-5 picks:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| picks |  113.00 |       0.63 |           0.48 |   0.15 |

## Where the team-total miss comes from

Projected vs actual per team-game for each piece of the scoring model (`corr` near 0 = the model can't tell teams apart on that piece; `sd_projected` far above `sd_actual` x corr = projections spread too wide).

| component     |   projected |   actual |   bias |   mae |   corr |   sd_projected |   sd_actual |
|:--------------|------------:|---------:|-------:|------:|-------:|---------------:|------------:|
| plays         |       60.21 |    61.52 |  -1.30 |  7.71 |   0.02 |           5.47 |        8.69 |
| dropbacks     |       36.18 |    37.56 |  -1.39 |  7.36 |   0.08 |           4.28 |        8.71 |
| pass_att      |       31.84 |    33.44 |  -1.61 |  6.97 |   0.20 |           4.28 |        8.59 |
| runs          |       24.04 |    23.95 |   0.09 |  5.35 |   0.10 |           4.40 |        5.84 |
| sacks         |        2.27 |     2.26 |   0.00 |  1.55 |   0.02 |           1.29 |        1.54 |
| interceptions |        0.71 |     0.69 |   0.02 |  0.71 |   0.00 |           0.29 |        0.80 |
| pass_td       |        1.60 |     1.55 |   0.05 |  0.88 |   0.31 |           0.45 |        1.16 |
| rush_td       |        0.98 |     0.93 |   0.05 |  0.91 |  -0.04 |           0.48 |        1.01 |
| td            |        2.57 |     2.48 |   0.10 |  1.10 |   0.24 |           0.63 |        1.41 |
| fga           |        1.91 |     2.10 |  -0.19 |  1.38 |  -0.12 |           1.02 |        1.23 |
| fgm           |        1.62 |     1.79 |  -0.17 |  1.27 |  -0.07 |           0.87 |        1.24 |
| points        |       22.75 |    22.96 |  -0.21 |  7.82 |   0.16 |           4.61 |        9.39 |

| part                                           |   share of points-miss variance |
|:-----------------------------------------------|--------------------------------:|
| touchdowns (x6.95)                             |                            0.86 |
| field goals (x3)                               |                            0.11 |
| other (defensive / return TDs, 2-pt, safeties) |                            0.03 |

Actual drives per team-game: 10.5 (sd 1.6); points per drive 2.23 (sd 0.98). Correlation of the points miss (actual - projected) with drive count: +0.04; with points per drive: +0.81. Red-zone trips per game 3.2, red-zone TD rate 59%.

## Player projections vs a naive season average

Mean absolute error on players who got the ball (lower is better).

| stat        |      n |   model_mae |   naive_mae | model_better   |
|:------------|-------:|------------:|------------:|:---------------|
| carries     | 453.00 |        2.75 |        2.88 | True           |
| completions | 127.00 |        5.25 |        5.51 | True           |
| pass_yds    | 127.00 |       63.99 |       72.25 | True           |
| rec_yds     | 904.00 |       21.22 |       22.05 | True           |
| receptions  | 904.00 |        1.60 |        1.64 | True           |
| rush_yds    | 453.00 |       17.31 |       18.17 | True           |
| targets     | 904.00 |        2.12 |        2.05 | False          |

## Team totals

Mean absolute error in points per team-game (lower is better).

| source                |   MAE |
|:----------------------|------:|
| model (final)         |  7.82 |
| model (before script) |  7.82 |
| market implied total  |  7.02 |
| team's season average |  8.85 |

By week:

|   week |   model |   market |   season_avg |
|-------:|--------:|---------:|-------------:|
|      2 |    9.16 |     8.28 |        12.06 |
|      3 |    8.58 |     7.36 |         8.03 |
|      4 |    6.02 |     5.58 |         7.35 |
|      5 |    7.52 |     6.85 |         7.91 |
