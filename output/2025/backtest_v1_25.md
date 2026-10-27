# Backtest

Weeks 6-18 replayed with only the data available before each week (play-by-play, stats, injury report, depth chart as of that week). Left out because they were gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 produce none.

## Picks (top 5 per game)

- **Overall: 418/680 (61%)** (voids: 43, pushes: 7)
- Week 6: 35/58 (60%)
- Week 7: 25/46 (54%)
- Week 8: 32/50 (64%)
- Week 9: 35/52 (67%)
- Week 10: 28/44 (64%)
- Week 11: 33/56 (59%)
- Week 12: 26/52 (50%)
- Week 13: 46/65 (71%)
- Week 14: 25/45 (56%)
- Week 15: 36/57 (63%)
- Week 16: 33/56 (59%)
- Week 17: 31/49 (63%)
- Week 18: 33/50 (66%)
- overs: 153/296 (52%)
- unders: 265/384 (69%)
- Rank 1 picks only: 116/176 (66%)

By stat:

| stat        | hit rate      |
|:------------|:--------------|
| carries     | 45/79 (57%)   |
| completions | 45/66 (68%)   |
| pass_yds    | 41/67 (61%)   |
| rec_yds     | 54/85 (64%)   |
| receptions  | 86/148 (58%)  |
| rush_yds    | 45/69 (65%)   |
| targets     | 102/166 (61%) |

## Every call, no filters (for comparison)

All over/under calls on players above the usage floor, before the trend gate, signal count and top-5 cut: **1084/1830 (59%)**. If the picks above beat this, the filters are adding value.

Hit rate by model edge (quartiles): does a bigger edge win more often?

| edge_bin        | hit rate      |
|:----------------|:--------------|
| (-0.001, 0.128] | 236/460 (51%) |
| (0.128, 0.188]  | 272/469 (58%) |
| (0.188, 0.269]  | 273/445 (61%) |
| (0.269, 0.618]  | 303/456 (66%) |

## Does each filter add anything? (lift over a no-information call)

`no-info rate` = how often a call on that side of the baseline would hit with no model at all (yardage stats land under their own average more often than not, so unders start ahead). `lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.

Unfiltered calls overall:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| all   | 1830.00 |       0.59 |           0.50 |   0.09 |

Usage trend agrees with the call (the qualification rule):

| usage trend agrees   |   calls |   hit rate |   no-info rate |   lift |
|:---------------------|--------:|-----------:|---------------:|-------:|
| False                | 1006.00 |       0.60 |           0.51 |   0.09 |
| True                 |  824.00 |       0.58 |           0.50 |   0.08 |

Number of agreeing signals:

|   n_signals |   calls |   hit rate |   no-info rate |   lift |
|------------:|--------:|-----------:|---------------:|-------:|
|           0 |  204.00 |       0.55 |           0.48 |   0.07 |
|           1 |  585.00 |       0.57 |           0.49 |   0.08 |
|           2 |  642.00 |       0.59 |           0.51 |   0.08 |
|           3 |  298.00 |       0.63 |           0.53 |   0.10 |
|           4 |   91.00 |       0.69 |           0.54 |   0.15 |
|           5 |   10.00 |       0.80 |           0.54 |   0.26 |

Top-5 picks:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| picks |  680.00 |       0.61 |           0.51 |   0.11 |

## Where the team-total miss comes from

Projected vs actual per team-game for each piece of the scoring model (`corr` near 0 = the model can't tell teams apart on that piece; `sd_projected` far above `sd_actual` x corr = projections spread too wide).

| component     |   projected |   actual |   bias |   mae |   corr |   sd_projected |   sd_actual |
|:--------------|------------:|---------:|-------:|------:|-------:|---------------:|------------:|
| plays         |       60.31 |    60.36 |  -0.05 |  6.90 |   0.12 |           2.33 |        8.77 |
| dropbacks     |       36.52 |    36.01 |   0.51 |  6.35 |   0.27 |           3.21 |        8.29 |
| pass_att      |       32.15 |    31.66 |   0.48 |  5.87 |   0.31 |           2.92 |        7.87 |
| runs          |       23.79 |    24.35 |  -0.56 |  5.85 |   0.18 |           3.18 |        7.22 |
| sacks         |        2.38 |     2.41 |  -0.04 |  1.40 |   0.25 |           0.59 |        1.84 |
| interceptions |        0.69 |     0.71 |  -0.01 |  0.68 |   0.07 |           0.30 |        0.83 |
| pass_td       |        1.52 |     1.46 |   0.06 |  0.97 |   0.15 |           0.34 |        1.19 |
| rush_td       |        0.93 |     0.95 |  -0.02 |  0.80 |   0.14 |           0.34 |        0.98 |
| td            |        2.46 |     2.42 |   0.04 |  1.14 |   0.28 |           0.49 |        1.44 |
| fga           |        1.99 |     1.97 |   0.03 |  1.16 |   0.08 |           0.59 |        1.36 |
| fgm           |        1.70 |     1.70 |  -0.00 |  1.07 |   0.10 |           0.51 |        1.28 |
| points        |       22.18 |    22.81 |  -0.63 |  7.73 |   0.30 |           3.62 |        9.99 |

| part                                           |   share of points-miss variance |
|:-----------------------------------------------|--------------------------------:|
| touchdowns (x6.95)                             |                            0.87 |
| field goals (x3)                               |                            0.07 |
| other (defensive / return TDs, 2-pt, safeties) |                            0.06 |

Actual drives per team-game: 10.1 (sd 1.6); points per drive 2.31 (sd 1.08). Correlation of the points miss (actual - projected) with drive count: +0.03; with points per drive: +0.85. Red-zone trips per game 3.2, red-zone TD rate 55%.

## Player projections vs a naive season average

Mean absolute error on players who got the ball (lower is better).

| stat        |       n |   model_mae |   naive_mae | model_better   |
|:------------|--------:|------------:|------------:|:---------------|
| carries     | 1454.00 |        2.90 |        2.85 | False          |
| completions |  395.00 |        4.87 |        5.22 | True           |
| pass_yds    |  395.00 |       60.31 |       63.18 | True           |
| rec_yds     | 2867.00 |       18.69 |       18.70 | True           |
| receptions  | 2867.00 |        1.41 |        1.38 | False          |
| rush_yds    | 1454.00 |       17.71 |       17.49 | False          |
| targets     | 2867.00 |        1.82 |        1.77 | False          |

## Team totals

Mean absolute error in points per team-game (lower is better).

| source                |   MAE |
|:----------------------|------:|
| model (final)         |  7.73 |
| model (before script) |  7.74 |
| market implied total  |  7.29 |
| team's season average |  7.84 |

By week:

|   week |   model |   market |   season_avg |
|-------:|--------:|---------:|-------------:|
|      6 |    6.61 |     5.98 |         6.92 |
|      7 |    9.20 |     8.02 |         8.08 |
|      8 |   10.64 |     8.90 |         9.41 |
|      9 |    7.25 |     6.75 |         8.61 |
|     10 |    8.51 |     7.88 |         7.86 |
|     11 |    7.35 |     6.90 |         7.67 |
|     12 |    5.39 |     5.80 |         5.81 |
|     13 |    7.00 |     6.00 |         6.28 |
|     14 |    7.64 |     7.98 |         8.55 |
|     15 |    8.59 |     8.11 |         8.48 |
|     16 |    6.56 |     7.16 |         7.18 |
|     17 |    7.64 |     7.55 |         8.76 |
|     18 |    8.39 |     7.86 |         8.46 |
