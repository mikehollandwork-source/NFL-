# Backtest

Weeks 2-5 replayed with only the data available before each week (play-by-play, stats, injury report, depth chart as of that week). Left out because they were gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 produce none.

## Picks (top 5 per game)

- **Overall: 63/108 (58%)** (voids: 2, pushes: 3)
- Week 4: 29/53 (55%)
- Week 5: 34/55 (62%)
- overs: 21/46 (46%)
- unders: 42/62 (68%)
- Rank 1 picks only: 18/26 (69%)

By stat:

| stat        | hit rate    |
|:------------|:------------|
| carries     | 5/11 (45%)  |
| completions | 8/14 (57%)  |
| pass_yds    | 8/11 (73%)  |
| rec_yds     | 10/18 (56%) |
| receptions  | 17/33 (52%) |
| rush_yds    | 11/12 (92%) |
| targets     | 4/9 (44%)   |

## Every call, no filters (for comparison)

All over/under calls on players above the usage floor, before the trend gate, signal count and top-5 cut: **154/258 (60%)**. If the picks above beat this, the filters are adding value.

Hit rate by model edge (quartiles): does a bigger edge win more often?

| edge_bin        | hit rate    |
|:----------------|:------------|
| (-0.001, 0.151] | 38/65 (58%) |
| (0.151, 0.194]  | 39/66 (59%) |
| (0.194, 0.276]  | 34/62 (55%) |
| (0.276, 0.445]  | 43/65 (66%) |

## Does each filter add anything? (lift over a no-information call)

`no-info rate` = how often a call on that side of the baseline would hit with no model at all (yardage stats land under their own average more often than not, so unders start ahead). `lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.

Unfiltered calls overall:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| all   |  258.00 |       0.60 |           0.49 |   0.11 |

Usage trend agrees with the call (the qualification rule):

| usage trend agrees   |   calls |   hit rate |   no-info rate |   lift |
|:---------------------|--------:|-----------:|---------------:|-------:|
| False                |  136.00 |       0.63 |           0.49 |   0.14 |
| True                 |  122.00 |       0.56 |           0.49 |   0.07 |

Number of agreeing signals:

|   n_signals |   calls |   hit rate |   no-info rate |   lift |
|------------:|--------:|-----------:|---------------:|-------:|
|           0 |   27.00 |       0.70 |           0.49 |   0.21 |
|           1 |   76.00 |       0.54 |           0.47 |   0.06 |
|           2 |  105.00 |       0.62 |           0.50 |   0.12 |
|           3 |   42.00 |       0.57 |           0.50 |   0.07 |
|           4 |    7.00 |       0.57 |           0.46 |   0.11 |
|           5 |    1.00 |       1.00 |           0.48 |   0.52 |

Top-5 picks:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| picks |  108.00 |       0.58 |           0.50 |   0.09 |

## Where the team-total miss comes from

Projected vs actual per team-game for each piece of the scoring model (`corr` near 0 = the model can't tell teams apart on that piece; `sd_projected` far above `sd_actual` x corr = projections spread too wide).

| component     |   projected |   actual |   bias |   mae |   corr |   sd_projected |   sd_actual |
|:--------------|------------:|---------:|-------:|------:|-------:|---------------:|------------:|
| plays         |       60.03 |    60.38 |  -0.34 |  6.50 |   0.13 |           1.79 |        8.14 |
| dropbacks     |       36.90 |    36.93 |  -0.03 |  7.22 |  -0.04 |           3.18 |        8.08 |
| pass_att      |       32.22 |    32.63 |  -0.41 |  6.93 |   0.01 |           3.18 |        7.72 |
| runs          |       23.13 |    23.45 |  -0.32 |  5.10 |   0.13 |           3.17 |        6.07 |
| sacks         |        2.31 |     2.27 |   0.05 |  1.34 |   0.11 |           0.39 |        1.65 |
| interceptions |        0.64 |     0.72 |  -0.08 |  0.72 |   0.17 |           0.35 |        0.87 |
| pass_td       |        1.37 |     1.69 |  -0.32 |  0.96 |   0.01 |           0.37 |        1.11 |
| rush_td       |        0.89 |     0.90 |  -0.01 |  0.76 |   0.06 |           0.34 |        0.94 |
| td            |        2.26 |     2.58 |  -0.33 |  1.06 |   0.22 |           0.49 |        1.34 |
| fga           |        2.23 |     2.06 |   0.17 |  1.22 |   0.15 |           1.11 |        1.28 |
| fgm           |        1.89 |     1.71 |   0.19 |  1.09 |   0.17 |           0.95 |        1.20 |
| points        |       21.30 |    24.25 |  -2.95 |  8.20 |   0.10 |           3.92 |        9.98 |

| part                                           |   share of points-miss variance |
|:-----------------------------------------------|--------------------------------:|
| touchdowns (x6.95)                             |                            0.75 |
| field goals (x3)                               |                          nan    |
| other (defensive / return TDs, 2-pt, safeties) |                          nan    |

Actual drives per team-game: 10.3 (sd 1.3); points per drive 2.39 (sd 1.04). Correlation of the points miss (actual - projected) with drive count: +0.07; with points per drive: +0.85. Red-zone trips per game 3.3, red-zone TD rate 62%.

## Player projections vs a naive season average

Mean absolute error on players who got the ball (lower is better).

| stat        |      n |   model_mae |   naive_mae | model_better   |
|:------------|-------:|------------:|------------:|:---------------|
| carries     | 452.00 |        2.68 |        2.80 | True           |
| completions | 125.00 |        5.08 |        5.89 | True           |
| pass_yds    | 125.00 |       57.32 |       70.82 | True           |
| rec_yds     | 890.00 |       18.70 |       20.38 | True           |
| receptions  | 890.00 |        1.49 |        1.54 | True           |
| rush_yds    | 452.00 |       17.10 |       18.67 | True           |
| targets     | 890.00 |        1.97 |        1.94 | False          |

## Team totals

Mean absolute error in points per team-game (lower is better).

| source                |   MAE |
|:----------------------|------:|
| model (final)         |  8.20 |
| model (before script) |  8.27 |
| market implied total  |  7.12 |
| team's season average |  9.12 |

By week:

|   week |   model |   market |   season_avg |
|-------:|--------:|---------:|-------------:|
|      2 |    8.62 |     6.77 |        11.12 |
|      3 |    9.79 |     8.39 |         9.66 |
|      4 |    7.26 |     6.00 |         7.76 |
|      5 |    6.98 |     7.34 |         7.75 |
