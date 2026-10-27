# Backtest

Weeks 6-18 replayed with only the data available before each week (play-by-play, stats, injury report, depth chart as of that week). Left out because they were gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 produce none.

## Picks (top 5 per game)

- **Overall: 412/714 (58%)** (voids: 46, pushes: 6)
- Week 6: 31/59 (53%)
- Week 7: 29/53 (55%)
- Week 8: 30/48 (62%)
- Week 9: 29/52 (56%)
- Week 10: 33/47 (70%)
- Week 11: 39/63 (62%)
- Week 12: 27/52 (52%)
- Week 13: 41/67 (61%)
- Week 14: 24/52 (46%)
- Week 15: 38/62 (61%)
- Week 16: 39/62 (63%)
- Week 17: 26/48 (54%)
- Week 18: 26/49 (53%)
- overs: 162/334 (49%)
- unders: 250/380 (66%)
- Rank 1 picks only: 116/179 (65%)

By stat:

| stat        | hit rate      |
|:------------|:--------------|
| carries     | 49/82 (60%)   |
| completions | 29/42 (69%)   |
| pass_yds    | 46/82 (56%)   |
| rec_yds     | 69/117 (59%)  |
| receptions  | 83/161 (52%)  |
| rush_yds    | 36/58 (62%)   |
| targets     | 100/172 (58%) |

## Every call, no filters (for comparison)

All over/under calls on players above the usage floor, before the trend gate, signal count and top-5 cut: **1077/1829 (59%)**. If the picks above beat this, the filters are adding value.

Hit rate by model edge (quartiles): does a bigger edge win more often?

| edge_bin        | hit rate      |
|:----------------|:--------------|
| (-0.001, 0.128] | 246/458 (54%) |
| (0.128, 0.192]  | 261/465 (56%) |
| (0.192, 0.264]  | 266/451 (59%) |
| (0.264, 0.626]  | 304/455 (67%) |

## Does each filter add anything? (lift over a no-information call)

`no-info rate` = how often a call on that side of the baseline would hit with no model at all (yardage stats land under their own average more often than not, so unders start ahead). `lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.

Unfiltered calls overall:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| all   | 1829.00 |       0.59 |           0.51 |   0.08 |

Usage trend agrees with the call (the qualification rule):

| usage trend agrees   |   calls |   hit rate |   no-info rate |   lift |
|:---------------------|--------:|-----------:|---------------:|-------:|
| False                | 1031.00 |       0.60 |           0.51 |   0.09 |
| True                 |  798.00 |       0.57 |           0.50 |   0.07 |

Number of agreeing signals:

|   n_signals |   calls |   hit rate |   no-info rate |   lift |
|------------:|--------:|-----------:|---------------:|-------:|
|           0 |  155.00 |       0.58 |           0.49 |   0.09 |
|           1 |  496.00 |       0.58 |           0.50 |   0.08 |
|           2 |  622.00 |       0.58 |           0.51 |   0.07 |
|           3 |  392.00 |       0.60 |           0.52 |   0.08 |
|           4 |  145.00 |       0.63 |           0.52 |   0.11 |
|           5 |   18.00 |       0.61 |           0.53 |   0.08 |
|           6 |    1.00 |       1.00 |           0.60 |   0.40 |

Top-5 picks:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| picks |  714.00 |       0.58 |           0.50 |   0.07 |

## Where the team-total miss comes from

Projected vs actual per team-game for each piece of the scoring model (`corr` near 0 = the model can't tell teams apart on that piece; `sd_projected` far above `sd_actual` x corr = projections spread too wide).

| component     |   projected |   actual |   bias |   mae |   corr |   sd_projected |   sd_actual |
|:--------------|------------:|---------:|-------:|------:|-------:|---------------:|------------:|
| plays         |       60.32 |    60.36 |  -0.04 |  6.90 |   0.12 |           2.34 |        8.77 |
| dropbacks     |       36.52 |    36.01 |   0.51 |  6.35 |   0.27 |           3.27 |        8.29 |
| pass_att      |       32.14 |    31.66 |   0.48 |  5.84 |   0.32 |           3.03 |        7.87 |
| runs          |       23.80 |    24.35 |  -0.55 |  5.85 |   0.18 |           3.21 |        7.22 |
| sacks         |        2.38 |     2.41 |  -0.03 |  1.46 |   0.27 |           1.07 |        1.84 |
| interceptions |        0.69 |     0.71 |  -0.01 |  0.68 |   0.06 |           0.30 |        0.83 |
| pass_td       |        1.52 |     1.46 |   0.06 |  0.97 |   0.16 |           0.35 |        1.19 |
| rush_td       |        0.93 |     0.95 |  -0.02 |  0.80 |   0.14 |           0.35 |        0.98 |
| td            |        2.45 |     2.42 |   0.03 |  1.14 |   0.27 |           0.51 |        1.44 |
| fga           |        2.00 |     1.97 |   0.03 |  1.16 |   0.08 |           0.59 |        1.36 |
| fgm           |        1.70 |     1.70 |   0.00 |  1.07 |   0.10 |           0.51 |        1.28 |
| points        |       22.16 |    22.81 |  -0.65 |  7.76 |   0.29 |           3.72 |        9.99 |

| part                                           |   share of points-miss variance |
|:-----------------------------------------------|--------------------------------:|
| touchdowns (x6.95)                             |                            0.87 |
| field goals (x3)                               |                            0.07 |
| other (defensive / return TDs, 2-pt, safeties) |                            0.06 |

Actual drives per team-game: 10.1 (sd 1.6); points per drive 2.31 (sd 1.08). Correlation of the points miss (actual - projected) with drive count: +0.04; with points per drive: +0.85. Red-zone trips per game 3.2, red-zone TD rate 55%.

## Player projections vs a naive season average

Mean absolute error on players who got the ball (lower is better).

| stat        |       n |   model_mae |   naive_mae | model_better   |
|:------------|--------:|------------:|------------:|:---------------|
| carries     | 1454.00 |        2.91 |        2.85 | False          |
| completions |  395.00 |        4.83 |        5.22 | True           |
| pass_yds    |  395.00 |       59.83 |       63.18 | True           |
| rec_yds     | 2867.00 |       18.68 |       18.70 | True           |
| receptions  | 2867.00 |        1.41 |        1.38 | False          |
| rush_yds    | 1454.00 |       17.74 |       17.49 | False          |
| targets     | 2867.00 |        1.82 |        1.77 | False          |

## Team totals

Mean absolute error in points per team-game (lower is better).

| source                |   MAE |
|:----------------------|------:|
| model (final)         |  7.76 |
| model (before script) |  7.75 |
| market implied total  |  7.29 |
| team's season average |  7.84 |

By week:

|   week |   model |   market |   season_avg |
|-------:|--------:|---------:|-------------:|
|      6 |    6.78 |     5.98 |         6.92 |
|      7 |    9.39 |     8.02 |         8.08 |
|      8 |   10.57 |     8.90 |         9.41 |
|      9 |    7.29 |     6.75 |         8.61 |
|     10 |    8.53 |     7.88 |         7.86 |
|     11 |    7.25 |     6.90 |         7.67 |
|     12 |    5.59 |     5.80 |         5.81 |
|     13 |    6.89 |     6.00 |         6.28 |
|     14 |    7.59 |     7.98 |         8.55 |
|     15 |    8.60 |     8.11 |         8.48 |
|     16 |    6.56 |     7.16 |         7.18 |
|     17 |    7.71 |     7.55 |         8.76 |
|     18 |    8.43 |     7.86 |         8.46 |
