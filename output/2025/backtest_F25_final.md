# Backtest

Weeks 6-18 replayed with only the data available before each week (play-by-play, stats, injury report, depth chart as of that week). Left out because they were gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 produce none.

## Picks (top 5 per game)

- **Overall: 422/689 (61%)** (voids: 36, pushes: 6)
- Week 6: 30/57 (53%)
- Week 7: 27/47 (57%)
- Week 8: 32/50 (64%)
- Week 9: 34/52 (65%)
- Week 10: 28/44 (64%)
- Week 11: 36/60 (60%)
- Week 12: 27/50 (54%)
- Week 13: 43/66 (65%)
- Week 14: 23/45 (51%)
- Week 15: 41/60 (68%)
- Week 16: 36/56 (64%)
- Week 17: 33/50 (66%)
- Week 18: 32/52 (62%)
- overs: 155/299 (52%)
- unders: 267/390 (68%)
- Rank 1 picks only: 119/177 (67%)

By stat:

| stat        | hit rate     |
|:------------|:-------------|
| carries     | 50/78 (64%)  |
| completions | 37/59 (63%)  |
| pass_yds    | 42/69 (61%)  |
| rec_yds     | 64/101 (63%) |
| receptions  | 82/143 (57%) |
| rush_yds    | 48/73 (66%)  |
| targets     | 99/166 (60%) |

## Every call, no filters (for comparison)

All over/under calls on players above the usage floor, before the trend gate, signal count and top-5 cut: **1094/1833 (60%)**. If the picks above beat this, the filters are adding value.

Hit rate by model edge (quartiles): does a bigger edge win more often?

| edge_bin        | hit rate      |
|:----------------|:--------------|
| (-0.001, 0.125] | 246/461 (53%) |
| (0.125, 0.188]  | 260/460 (57%) |
| (0.188, 0.267]  | 288/457 (63%) |
| (0.267, 0.616]  | 300/455 (66%) |

## Does each filter add anything? (lift over a no-information call)

`no-info rate` = how often a call on that side of the baseline would hit with no model at all (yardage stats land under their own average more often than not, so unders start ahead). `lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.

Unfiltered calls overall:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| all   | 1833.00 |       0.60 |           0.50 |   0.09 |

Usage trend agrees with the call (the qualification rule):

| usage trend agrees   |   calls |   hit rate |   no-info rate |   lift |
|:---------------------|--------:|-----------:|---------------:|-------:|
| False                | 1012.00 |       0.61 |           0.51 |   0.10 |
| True                 |  821.00 |       0.59 |           0.50 |   0.09 |

Number of agreeing signals:

|   n_signals |   calls |   hit rate |   no-info rate |   lift |
|------------:|--------:|-----------:|---------------:|-------:|
|           0 |  206.00 |       0.56 |           0.49 |   0.07 |
|           1 |  583.00 |       0.57 |           0.49 |   0.08 |
|           2 |  631.00 |       0.60 |           0.51 |   0.10 |
|           3 |  319.00 |       0.62 |           0.52 |   0.10 |
|           4 |   86.00 |       0.70 |           0.54 |   0.16 |
|           5 |    8.00 |       0.75 |           0.52 |   0.23 |

Top-5 picks:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| picks |  689.00 |       0.61 |           0.51 |   0.11 |

## Where the team-total miss comes from

Projected vs actual per team-game for each piece of the scoring model (`corr` near 0 = the model can't tell teams apart on that piece; `sd_projected` far above `sd_actual` x corr = projections spread too wide).

| component     |   projected |   actual |   bias |   mae |   corr |   sd_projected |   sd_actual |
|:--------------|------------:|---------:|-------:|------:|-------:|---------------:|------------:|
| plays         |       60.32 |    60.36 |  -0.04 |  6.88 |   0.14 |           2.33 |        8.77 |
| dropbacks     |       36.52 |    36.01 |   0.51 |  6.35 |   0.26 |           3.22 |        8.29 |
| pass_att      |       32.13 |    31.66 |   0.47 |  5.86 |   0.31 |           2.92 |        7.87 |
| runs          |       23.80 |    24.35 |  -0.55 |  5.84 |   0.18 |           3.17 |        7.22 |
| sacks         |        2.38 |     2.41 |  -0.04 |  1.40 |   0.25 |           0.59 |        1.84 |
| interceptions |        0.69 |     0.71 |  -0.01 |  0.68 |   0.07 |           0.30 |        0.83 |
| pass_td       |        1.52 |     1.46 |   0.05 |  0.98 |   0.15 |           0.34 |        1.19 |
| rush_td       |        0.93 |     0.95 |  -0.02 |  0.80 |   0.13 |           0.33 |        0.98 |
| td            |        2.45 |     2.42 |   0.03 |  1.14 |   0.27 |           0.48 |        1.44 |
| fga           |        1.99 |     1.97 |   0.03 |  1.16 |   0.08 |           0.59 |        1.36 |
| fgm           |        1.69 |     1.70 |  -0.00 |  1.07 |   0.09 |           0.51 |        1.28 |
| points        |       22.13 |    22.81 |  -0.69 |  7.76 |   0.29 |           3.53 |        9.99 |

| part                                           |   share of points-miss variance |
|:-----------------------------------------------|--------------------------------:|
| touchdowns (x6.95)                             |                            0.87 |
| field goals (x3)                               |                            0.07 |
| other (defensive / return TDs, 2-pt, safeties) |                            0.06 |

Actual drives per team-game: 10.1 (sd 1.6); points per drive 2.31 (sd 1.08). Correlation of the points miss (actual - projected) with drive count: +0.03; with points per drive: +0.86. Red-zone trips per game 3.2, red-zone TD rate 55%.

## Player projections vs a naive season average

Mean absolute error on players who got the ball (lower is better).

| stat        |       n |   model_mae |   naive_mae | model_better   |
|:------------|--------:|------------:|------------:|:---------------|
| carries     | 1454.00 |        2.90 |        2.85 | False          |
| completions |  395.00 |        4.88 |        5.22 | True           |
| pass_yds    |  395.00 |       60.39 |       63.18 | True           |
| rec_yds     | 2867.00 |       18.64 |       18.70 | True           |
| receptions  | 2867.00 |        1.41 |        1.38 | False          |
| rush_yds    | 1454.00 |       17.68 |       17.49 | False          |
| targets     | 2867.00 |        1.82 |        1.77 | False          |

## Team totals

Mean absolute error in points per team-game (lower is better).

| source                |   MAE |
|:----------------------|------:|
| model (final)         |  7.76 |
| model (before script) |  7.73 |
| market implied total  |  7.29 |
| team's season average |  7.84 |

By week:

|   week |   model |   market |   season_avg |
|-------:|--------:|---------:|-------------:|
|      6 |    6.67 |     5.98 |         6.92 |
|      7 |    9.11 |     8.02 |         8.08 |
|      8 |   10.66 |     8.90 |         9.41 |
|      9 |    7.31 |     6.75 |         8.61 |
|     10 |    8.50 |     7.88 |         7.86 |
|     11 |    7.29 |     6.90 |         7.67 |
|     12 |    5.54 |     5.80 |         5.81 |
|     13 |    6.99 |     6.00 |         6.28 |
|     14 |    7.59 |     7.98 |         8.55 |
|     15 |    8.62 |     8.11 |         8.48 |
|     16 |    6.74 |     7.16 |         7.18 |
|     17 |    7.79 |     7.55 |         8.76 |
|     18 |    8.38 |     7.86 |         8.46 |
