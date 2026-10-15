# Backtest

Weeks 2-5 replayed with only the data available before each week (play-by-play, stats, injury report, depth chart as of that week). Left out because they were gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 produce none.

## Picks (top 5 per game)

- **Overall: 70/112 (62%)** (voids: 7, pushes: 3)
- Week 4: 38/63 (60%)
- Week 5: 32/49 (65%)
- overs: 41/69 (59%)
- unders: 29/43 (67%)
- Rank 1 picks only: 21/28 (75%)

By stat:

| stat        | hit rate    |
|:------------|:------------|
| carries     | 17/20 (85%) |
| completions | 4/8 (50%)   |
| pass_yds    | 8/11 (73%)  |
| rec_yds     | 14/18 (78%) |
| receptions  | 12/21 (57%) |
| rush_yds    | 5/9 (56%)   |
| targets     | 10/25 (40%) |

## Every call, no filters (for comparison)

All over/under calls on players above the usage floor, before the trend gate, signal count and top-5 cut: **162/255 (64%)**. If the picks above beat this, the filters are adding value.

Hit rate by model edge (quartiles): does a bigger edge win more often?

| edge_bin        | hit rate    |
|:----------------|:------------|
| (-0.001, 0.156] | 40/64 (62%) |
| (0.156, 0.216]  | 38/64 (59%) |
| (0.216, 0.292]  | 42/63 (67%) |
| (0.292, 0.541]  | 42/64 (66%) |

## Does each filter add anything? (lift over a no-information call)

`no-info rate` = how often a call on that side of the baseline would hit with no model at all (yardage stats land under their own average more often than not, so unders start ahead). `lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.

Unfiltered calls overall:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| all   |  255.00 |       0.64 |           0.50 |   0.14 |

Usage trend agrees with the call (the qualification rule):

| usage trend agrees   |   calls |   hit rate |   no-info rate |   lift |
|:---------------------|--------:|-----------:|---------------:|-------:|
| False                |  130.00 |       0.68 |           0.52 |   0.16 |
| True                 |  125.00 |       0.59 |           0.47 |   0.12 |

Number of agreeing signals:

|   n_signals |   calls |   hit rate |   no-info rate |   lift |
|------------:|--------:|-----------:|---------------:|-------:|
|           0 |   17.00 |       0.76 |           0.54 |   0.22 |
|           1 |   92.00 |       0.62 |           0.49 |   0.13 |
|           2 |   86.00 |       0.64 |           0.51 |   0.13 |
|           3 |   40.00 |       0.68 |           0.47 |   0.20 |
|           4 |   18.00 |       0.56 |           0.48 |   0.07 |
|           5 |    2.00 |       0.00 |           0.50 |  -0.50 |

Top-5 picks:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| picks |  112.00 |       0.62 |           0.48 |   0.14 |

## Where the team-total miss comes from

Projected vs actual per team-game for each piece of the scoring model (`corr` near 0 = the model can't tell teams apart on that piece; `sd_projected` far above `sd_actual` x corr = projections spread too wide).

| component     |   projected |   actual |   bias |   mae |   corr |   sd_projected |   sd_actual |
|:--------------|------------:|---------:|-------:|------:|-------:|---------------:|------------:|
| plays         |       60.17 |    61.52 |  -1.35 |  6.63 |   0.08 |           1.67 |        8.69 |
| dropbacks     |       36.24 |    37.56 |  -1.33 |  7.21 |   0.06 |           3.41 |        8.71 |
| pass_att      |       31.90 |    33.44 |  -1.54 |  6.78 |   0.19 |           3.43 |        8.59 |
| runs          |       23.93 |    23.95 |  -0.02 |  4.98 |   0.15 |           3.50 |        5.84 |
| sacks         |        2.25 |     2.26 |  -0.01 |  1.27 |   0.01 |           0.35 |        1.54 |
| interceptions |        0.71 |     0.69 |   0.02 |  0.71 |   0.03 |           0.30 |        0.80 |
| pass_td       |        1.59 |     1.55 |   0.04 |  0.91 |   0.24 |           0.47 |        1.16 |
| rush_td       |        0.97 |     0.93 |   0.04 |  0.92 |  -0.05 |           0.48 |        1.01 |
| td            |        2.56 |     2.48 |   0.08 |  1.13 |   0.17 |           0.68 |        1.41 |
| fga           |        1.91 |     2.10 |  -0.20 |  1.38 |  -0.12 |           1.02 |        1.23 |
| fgm           |        1.61 |     1.79 |  -0.17 |  1.26 |  -0.07 |           0.87 |        1.24 |
| points        |       22.64 |    22.96 |  -0.32 |  7.99 |   0.14 |           4.76 |        9.39 |

| part                                           |   share of points-miss variance |
|:-----------------------------------------------|--------------------------------:|
| touchdowns (x6.95)                             |                            0.89 |
| field goals (x3)                               |                            0.08 |
| other (defensive / return TDs, 2-pt, safeties) |                            0.03 |

Actual drives per team-game: 10.5 (sd 1.6); points per drive 2.23 (sd 0.98). Correlation of the points miss (actual - projected) with drive count: +0.03; with points per drive: +0.81. Red-zone trips per game 3.2, red-zone TD rate 59%.

## Player projections vs a naive season average

Mean absolute error on players who got the ball (lower is better).

| stat        |      n |   model_mae |   naive_mae | model_better   |
|:------------|-------:|------------:|------------:|:---------------|
| carries     | 453.00 |        2.65 |        2.88 | True           |
| completions | 127.00 |        5.00 |        5.51 | True           |
| pass_yds    | 127.00 |       64.55 |       72.25 | True           |
| rec_yds     | 904.00 |       21.22 |       22.05 | True           |
| receptions  | 904.00 |        1.60 |        1.64 | True           |
| rush_yds    | 453.00 |       17.03 |       18.17 | True           |
| targets     | 904.00 |        2.12 |        2.05 | False          |

## Team totals

Mean absolute error in points per team-game (lower is better).

| source                |   MAE |
|:----------------------|------:|
| model (final)         |  7.99 |
| model (before script) |  7.97 |
| market implied total  |  7.02 |
| team's season average |  8.85 |

By week:

|   week |   model |   market |   season_avg |
|-------:|--------:|---------:|-------------:|
|      2 |    9.65 |     8.28 |        12.06 |
|      3 |    8.39 |     7.36 |         8.03 |
|      4 |    6.10 |     5.58 |         7.35 |
|      5 |    7.79 |     6.85 |         7.91 |
