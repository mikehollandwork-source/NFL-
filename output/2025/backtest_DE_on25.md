# Backtest

Weeks 6-18 replayed with only the data available before each week (play-by-play, stats, injury report, depth chart as of that week). Left out because they were gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 produce none.

## Picks (top 5 per game)

- **Overall: 418/695 (60%)** (voids: 45, pushes: 6)
- Week 6: 38/61 (62%)
- Week 7: 26/48 (54%)
- Week 8: 33/51 (65%)
- Week 9: 34/53 (64%)
- Week 10: 26/42 (62%)
- Week 11: 39/61 (64%)
- Week 12: 27/48 (56%)
- Week 13: 41/65 (63%)
- Week 14: 24/47 (51%)
- Week 15: 34/56 (61%)
- Week 16: 38/62 (61%)
- Week 17: 30/49 (61%)
- Week 18: 28/52 (54%)
- overs: 161/315 (51%)
- unders: 257/380 (68%)
- Rank 1 picks only: 122/179 (68%)

By stat:

| stat        | hit rate     |
|:------------|:-------------|
| carries     | 65/98 (66%)  |
| completions | 44/64 (69%)  |
| pass_yds    | 37/63 (59%)  |
| rec_yds     | 55/88 (62%)  |
| receptions  | 86/161 (53%) |
| rush_yds    | 37/64 (58%)  |
| targets     | 94/157 (60%) |

## Every call, no filters (for comparison)

All over/under calls on players above the usage floor, before the trend gate, signal count and top-5 cut: **1067/1829 (58%)**. If the picks above beat this, the filters are adding value.

Hit rate by model edge (quartiles): does a bigger edge win more often?

| edge_bin        | hit rate      |
|:----------------|:--------------|
| (-0.001, 0.128] | 240/458 (52%) |
| (0.128, 0.189]  | 248/459 (54%) |
| (0.189, 0.269]  | 285/459 (62%) |
| (0.269, 0.591]  | 294/453 (65%) |

## Does each filter add anything? (lift over a no-information call)

`no-info rate` = how often a call on that side of the baseline would hit with no model at all (yardage stats land under their own average more often than not, so unders start ahead). `lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.

Unfiltered calls overall:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| all   | 1829.00 |       0.58 |           0.50 |   0.08 |

Usage trend agrees with the call (the qualification rule):

| usage trend agrees   |   calls |   hit rate |   no-info rate |   lift |
|:---------------------|--------:|-----------:|---------------:|-------:|
| False                | 1003.00 |       0.59 |           0.50 |   0.09 |
| True                 |  826.00 |       0.57 |           0.50 |   0.07 |

Number of agreeing signals:

|   n_signals |   calls |   hit rate |   no-info rate |   lift |
|------------:|--------:|-----------:|---------------:|-------:|
|           0 |  190.00 |       0.53 |           0.48 |   0.05 |
|           1 |  586.00 |       0.55 |           0.49 |   0.06 |
|           2 |  635.00 |       0.59 |           0.50 |   0.09 |
|           3 |  318.00 |       0.63 |           0.52 |   0.11 |
|           4 |   94.00 |       0.65 |           0.53 |   0.11 |
|           5 |    6.00 |       0.50 |           0.48 |   0.02 |

Top-5 picks:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| picks |  695.00 |       0.60 |           0.50 |   0.10 |

## Where the team-total miss comes from

Projected vs actual per team-game for each piece of the scoring model (`corr` near 0 = the model can't tell teams apart on that piece; `sd_projected` far above `sd_actual` x corr = projections spread too wide).

| component     |   projected |   actual |   bias |   mae |   corr |   sd_projected |   sd_actual |
|:--------------|------------:|---------:|-------:|------:|-------:|---------------:|------------:|
| plays         |       60.31 |    60.36 |  -0.05 |  6.89 |   0.13 |           2.35 |        8.77 |
| dropbacks     |       36.50 |    36.01 |   0.49 |  6.39 |   0.26 |           3.35 |        8.29 |
| pass_att      |       32.13 |    31.66 |   0.46 |  5.88 |   0.30 |           3.05 |        7.87 |
| runs          |       23.81 |    24.35 |  -0.54 |  5.91 |   0.17 |           3.41 |        7.22 |
| sacks         |        2.38 |     2.41 |  -0.04 |  1.40 |   0.25 |           0.59 |        1.84 |
| interceptions |        0.70 |     0.71 |  -0.01 |  0.68 |   0.07 |           0.30 |        0.83 |
| pass_td       |        1.53 |     1.46 |   0.06 |  0.97 |   0.18 |           0.39 |        1.19 |
| rush_td       |        0.95 |     0.95 |  -0.00 |  0.80 |   0.17 |           0.39 |        0.98 |
| td            |        2.47 |     2.42 |   0.06 |  1.14 |   0.30 |           0.61 |        1.44 |
| fga           |        1.99 |     1.97 |   0.03 |  1.16 |   0.08 |           0.59 |        1.36 |
| fgm           |        1.70 |     1.70 |  -0.00 |  1.07 |   0.10 |           0.51 |        1.28 |
| points        |       22.31 |    22.81 |  -0.50 |  7.73 |   0.31 |           4.42 |        9.99 |

| part                                           |   share of points-miss variance |
|:-----------------------------------------------|--------------------------------:|
| touchdowns (x6.95)                             |                            0.87 |
| field goals (x3)                               |                            0.07 |
| other (defensive / return TDs, 2-pt, safeties) |                            0.06 |

Actual drives per team-game: 10.1 (sd 1.6); points per drive 2.31 (sd 1.08). Correlation of the points miss (actual - projected) with drive count: +0.06; with points per drive: +0.82. Red-zone trips per game 3.2, red-zone TD rate 55%.

## Player projections vs a naive season average

Mean absolute error on players who got the ball (lower is better).

| stat        |       n |   model_mae |   naive_mae | model_better   |
|:------------|--------:|------------:|------------:|:---------------|
| carries     | 1454.00 |        2.90 |        2.85 | False          |
| completions |  395.00 |        4.90 |        5.22 | True           |
| pass_yds    |  395.00 |       60.65 |       63.18 | True           |
| rec_yds     | 2867.00 |       18.66 |       18.70 | True           |
| receptions  | 2867.00 |        1.41 |        1.38 | False          |
| rush_yds    | 1454.00 |       17.67 |       17.49 | False          |
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
|      6 |    6.82 |     5.98 |         6.92 |
|      7 |    9.17 |     8.02 |         8.08 |
|      8 |   10.21 |     8.90 |         9.41 |
|      9 |    7.76 |     6.75 |         8.61 |
|     10 |    8.33 |     7.88 |         7.86 |
|     11 |    7.16 |     6.90 |         7.67 |
|     12 |    5.89 |     5.80 |         5.81 |
|     13 |    6.61 |     6.00 |         6.28 |
|     14 |    7.50 |     7.98 |         8.55 |
|     15 |    8.61 |     8.11 |         8.48 |
|     16 |    6.76 |     7.16 |         7.18 |
|     17 |    7.83 |     7.55 |         8.76 |
|     18 |    8.17 |     7.86 |         8.46 |
