# Backtest

Weeks 2-5 replayed with only the data available before each week (play-by-play, stats, injury report, depth chart as of that week). Left out because they were gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 produce none.

## Picks (top 5 per game)

- **Overall: 65/107 (61%)** (voids: 6, pushes: 1)
- Week 4: 36/61 (59%)
- Week 5: 29/46 (63%)
- overs: 36/64 (56%)
- unders: 29/43 (67%)
- Rank 1 picks only: 17/29 (59%)

By stat:

| stat        | hit rate    |
|:------------|:------------|
| carries     | 13/14 (93%) |
| completions | 5/10 (50%)  |
| pass_yds    | 4/5 (80%)   |
| rec_yds     | 17/23 (74%) |
| receptions  | 13/20 (65%) |
| rush_yds    | 5/9 (56%)   |
| targets     | 8/26 (31%)  |

## Every call, no filters (for comparison)

All over/under calls on players above the usage floor, before the trend gate, signal count and top-5 cut: **161/257 (63%)**. If the picks above beat this, the filters are adding value.

Hit rate by model edge (quartiles): does a bigger edge win more often?

| edge_bin        | hit rate    |
|:----------------|:------------|
| (-0.001, 0.147] | 36/65 (55%) |
| (0.147, 0.211]  | 37/64 (58%) |
| (0.211, 0.308]  | 45/64 (70%) |
| (0.308, 0.55]   | 43/64 (67%) |

## Does each filter add anything? (lift over a no-information call)

`no-info rate` = how often a call on that side of the baseline would hit with no model at all (yardage stats land under their own average more often than not, so unders start ahead). `lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.

Unfiltered calls overall:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| all   |  257.00 |       0.63 |           0.50 |   0.13 |

Usage trend agrees with the call (the qualification rule):

| usage trend agrees   |   calls |   hit rate |   no-info rate |   lift |
|:---------------------|--------:|-----------:|---------------:|-------:|
| False                |  131.00 |       0.66 |           0.53 |   0.14 |
| True                 |  126.00 |       0.59 |           0.47 |   0.12 |

Number of agreeing signals:

|   n_signals |   calls |   hit rate |   no-info rate |   lift |
|------------:|--------:|-----------:|---------------:|-------:|
|           0 |   25.00 |       0.56 |           0.54 |   0.02 |
|           1 |   73.00 |       0.66 |           0.51 |   0.15 |
|           2 |   88.00 |       0.64 |           0.50 |   0.14 |
|           3 |   48.00 |       0.62 |           0.47 |   0.16 |
|           4 |   17.00 |       0.53 |           0.50 |   0.03 |
|           5 |    5.00 |       0.60 |           0.47 |   0.13 |
|           6 |    1.00 |       1.00 |           0.57 |   0.43 |

Top-5 picks:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| picks |  107.00 |       0.61 |           0.48 |   0.13 |

## Where the team-total miss comes from

Projected vs actual per team-game for each piece of the scoring model (`corr` near 0 = the model can't tell teams apart on that piece; `sd_projected` far above `sd_actual` x corr = projections spread too wide).

| component     |   projected |   actual |   bias |   mae |   corr |   sd_projected |   sd_actual |
|:--------------|------------:|---------:|-------:|------:|-------:|---------------:|------------:|
| plays         |       60.17 |    61.52 |  -1.35 |  6.66 |   0.06 |           1.66 |        8.69 |
| dropbacks     |       36.21 |    37.56 |  -1.35 |  7.11 |   0.05 |           2.85 |        8.71 |
| pass_att      |       31.89 |    33.44 |  -1.56 |  6.73 |   0.21 |           3.07 |        8.59 |
| runs          |       23.95 |    23.95 |   0.00 |  4.72 |   0.15 |           2.91 |        5.84 |
| sacks         |        2.25 |     2.26 |  -0.01 |  1.26 |   0.02 |           0.31 |        1.54 |
| interceptions |        0.71 |     0.69 |   0.02 |  0.68 |   0.07 |           0.17 |        0.80 |
| pass_td       |        1.60 |     1.55 |   0.05 |  0.91 |   0.27 |           0.26 |        1.16 |
| rush_td       |        0.98 |     0.93 |   0.05 |  0.84 |   0.03 |           0.33 |        1.01 |
| td            |        2.58 |     2.48 |   0.11 |  1.14 |   0.13 |           0.34 |        1.41 |
| fga           |        1.92 |     2.10 |  -0.19 |  1.38 |  -0.13 |           1.02 |        1.23 |
| fgm           |        1.62 |     1.79 |  -0.16 |  1.27 |  -0.07 |           0.87 |        1.24 |
| points        |       22.83 |    22.96 |  -0.13 |  7.94 |   0.04 |           3.03 |        9.39 |

| part                                           |   share of points-miss variance |
|:-----------------------------------------------|--------------------------------:|
| touchdowns (x6.95)                             |                            0.87 |
| field goals (x3)                               |                            0.11 |
| other (defensive / return TDs, 2-pt, safeties) |                            0.02 |

Actual drives per team-game: 10.5 (sd 1.6); points per drive 2.23 (sd 0.98). Correlation of the points miss (actual - projected) with drive count: +0.03; with points per drive: +0.88. Red-zone trips per game 3.2, red-zone TD rate 59%.

## Player projections vs a naive season average

Mean absolute error on players who got the ball (lower is better).

| stat        |      n |   model_mae |   naive_mae | model_better   |
|:------------|-------:|------------:|------------:|:---------------|
| carries     | 453.00 |        2.64 |        2.88 | True           |
| completions | 127.00 |        5.06 |        5.51 | True           |
| pass_yds    | 127.00 |       62.79 |       72.25 | True           |
| rec_yds     | 904.00 |       21.15 |       22.05 | True           |
| receptions  | 904.00 |        1.60 |        1.64 | True           |
| rush_yds    | 453.00 |       17.15 |       18.17 | True           |
| targets     | 904.00 |        2.12 |        2.05 | False          |

## Team totals

Mean absolute error in points per team-game (lower is better).

| source                |   MAE |
|:----------------------|------:|
| model (final)         |  7.94 |
| model (before script) |  7.97 |
| market implied total  |  7.02 |
| team's season average |  8.85 |

By week:

|   week |   model |   market |   season_avg |
|-------:|--------:|---------:|-------------:|
|      2 |    9.38 |     8.28 |        12.06 |
|      3 |    8.15 |     7.36 |         8.03 |
|      4 |    6.50 |     5.58 |         7.35 |
|      5 |    7.73 |     6.85 |         7.91 |
