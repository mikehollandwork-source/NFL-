# Backtest

Weeks 6-18 replayed with only the data available before each week (play-by-play, stats, injury report, depth chart as of that week). Left out because they were gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 produce none.

## Picks (top 5 per game)

- **Overall: 388/638 (61%)** (voids: 39, pushes: 6)
- Week 6: 30/53 (57%)
- Week 7: 28/49 (57%)
- Week 8: 28/45 (62%)
- Week 9: 30/49 (61%)
- Week 10: 25/40 (62%)
- Week 11: 36/55 (65%)
- Week 12: 26/46 (57%)
- Week 13: 37/59 (63%)
- Week 14: 24/42 (57%)
- Week 15: 33/50 (66%)
- Week 16: 27/50 (54%)
- Week 17: 32/49 (65%)
- Week 18: 32/51 (63%)
- overs: 135/262 (52%)
- unders: 253/376 (67%)
- Rank 1 picks only: 112/173 (65%)

By stat:

| stat        | hit rate     |
|:------------|:-------------|
| carries     | 51/80 (64%)  |
| completions | 37/53 (70%)  |
| pass_yds    | 36/61 (59%)  |
| rec_yds     | 55/86 (64%)  |
| receptions  | 84/149 (56%) |
| rush_yds    | 40/60 (67%)  |
| targets     | 85/149 (57%) |

## Every call, no filters (for comparison)

All over/under calls on players above the usage floor, before the trend gate, signal count and top-5 cut: **1080/1824 (59%)**. If the picks above beat this, the filters are adding value.

Hit rate by model edge (quartiles): does a bigger edge win more often?

| edge_bin        | hit rate      |
|:----------------|:--------------|
| (-0.001, 0.124] | 232/456 (51%) |
| (0.124, 0.188]  | 259/462 (56%) |
| (0.188, 0.265]  | 281/450 (62%) |
| (0.265, 0.604]  | 308/456 (68%) |

## Does each filter add anything? (lift over a no-information call)

`no-info rate` = how often a call on that side of the baseline would hit with no model at all (yardage stats land under their own average more often than not, so unders start ahead). `lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.

Unfiltered calls overall:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| all   | 1824.00 |       0.59 |           0.50 |   0.09 |

Usage trend agrees with the call (the qualification rule):

| usage trend agrees   |   calls |   hit rate |   no-info rate |   lift |
|:---------------------|--------:|-----------:|---------------:|-------:|
| False                |  999.00 |       0.60 |           0.50 |   0.10 |
| True                 |  825.00 |       0.58 |           0.50 |   0.08 |

Number of agreeing signals:

|   n_signals |   calls |   hit rate |   no-info rate |   lift |
|------------:|--------:|-----------:|---------------:|-------:|
|           0 |  253.00 |       0.55 |           0.48 |   0.07 |
|           1 |  622.00 |       0.57 |           0.49 |   0.08 |
|           2 |  600.00 |       0.62 |           0.52 |   0.11 |
|           3 |  275.00 |       0.59 |           0.53 |   0.07 |
|           4 |   69.00 |       0.68 |           0.52 |   0.16 |
|           5 |    5.00 |       0.80 |           0.60 |   0.20 |

Top-5 picks:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| picks |  638.00 |       0.61 |           0.51 |   0.10 |

## Where the team-total miss comes from

Projected vs actual per team-game for each piece of the scoring model (`corr` near 0 = the model can't tell teams apart on that piece; `sd_projected` far above `sd_actual` x corr = projections spread too wide).

| component     |   projected |   actual |   bias |   mae |   corr |   sd_projected |   sd_actual |
|:--------------|------------:|---------:|-------:|------:|-------:|---------------:|------------:|
| plays         |       60.30 |    60.36 |  -0.06 |  6.88 |   0.13 |           2.34 |        8.77 |
| dropbacks     |       36.51 |    36.01 |   0.50 |  6.26 |   0.28 |           2.91 |        8.29 |
| pass_att      |       32.14 |    31.66 |   0.48 |  5.80 |   0.33 |           2.71 |        7.87 |
| runs          |       23.78 |    24.35 |  -0.56 |  5.78 |   0.18 |           2.87 |        7.22 |
| sacks         |        2.37 |     2.41 |  -0.04 |  1.39 |   0.26 |           0.57 |        1.84 |
| interceptions |        0.69 |     0.71 |  -0.01 |  0.68 |   0.05 |           0.21 |        0.83 |
| pass_td       |        1.52 |     1.46 |   0.06 |  0.98 |   0.15 |           0.22 |        1.19 |
| rush_td       |        0.94 |     0.95 |  -0.01 |  0.78 |   0.17 |           0.26 |        0.98 |
| td            |        2.46 |     2.42 |   0.05 |  1.14 |   0.24 |           0.35 |        1.44 |
| fga           |        1.99 |     1.97 |   0.03 |  1.16 |   0.08 |           0.59 |        1.36 |
| fgm           |        1.70 |     1.70 |  -0.00 |  1.08 |   0.09 |           0.51 |        1.28 |
| points        |       22.23 |    22.81 |  -0.58 |  7.97 |   0.18 |           2.73 |        9.99 |

| part                                           |   share of points-miss variance |
|:-----------------------------------------------|--------------------------------:|
| touchdowns (x6.95)                             |                            0.85 |
| field goals (x3)                               |                            0.08 |
| other (defensive / return TDs, 2-pt, safeties) |                            0.07 |

Actual drives per team-game: 10.1 (sd 1.6); points per drive 2.31 (sd 1.08). Correlation of the points miss (actual - projected) with drive count: -0.01; with points per drive: +0.90. Red-zone trips per game 3.2, red-zone TD rate 55%.

## Player projections vs a naive season average

Mean absolute error on players who got the ball (lower is better).

| stat        |       n |   model_mae |   naive_mae | model_better   |
|:------------|--------:|------------:|------------:|:---------------|
| carries     | 1454.00 |        2.91 |        2.85 | False          |
| completions |  395.00 |        4.79 |        5.22 | True           |
| pass_yds    |  395.00 |       59.36 |       63.18 | True           |
| rec_yds     | 2867.00 |       18.61 |       18.70 | True           |
| receptions  | 2867.00 |        1.40 |        1.38 | False          |
| rush_yds    | 1454.00 |       17.69 |       17.49 | False          |
| targets     | 2867.00 |        1.82 |        1.77 | False          |

## Team totals

Mean absolute error in points per team-game (lower is better).

| source                |   MAE |
|:----------------------|------:|
| model (final)         |  7.97 |
| model (before script) |  7.99 |
| market implied total  |  7.29 |
| team's season average |  7.84 |

By week:

|   week |   model |   market |   season_avg |
|-------:|--------:|---------:|-------------:|
|      6 |    6.41 |     5.98 |         6.92 |
|      7 |    9.02 |     8.02 |         8.08 |
|      8 |   10.83 |     8.90 |         9.41 |
|      9 |    7.85 |     6.75 |         8.61 |
|     10 |    8.42 |     7.88 |         7.86 |
|     11 |    7.54 |     6.90 |         7.67 |
|     12 |    6.28 |     5.80 |         5.81 |
|     13 |    6.53 |     6.00 |         6.28 |
|     14 |    8.17 |     7.98 |         8.55 |
|     15 |    9.14 |     8.11 |         8.48 |
|     16 |    6.69 |     7.16 |         7.18 |
|     17 |    8.04 |     7.55 |         8.76 |
|     18 |    9.00 |     7.86 |         8.46 |
