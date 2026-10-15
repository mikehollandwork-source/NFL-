# Backtest

Weeks 2-5 replayed with only the data available before each week (play-by-play, stats, injury report, depth chart as of that week). Left out because they were gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 produce none.

## Picks (top 5 per game)

- **Overall: 75/115 (65%)** (voids: 6, pushes: 2)
- Week 4: 40/66 (61%)
- Week 5: 35/49 (71%)
- overs: 43/70 (61%)
- unders: 32/45 (71%)
- Rank 1 picks only: 22/29 (76%)

By stat:

| stat        | hit rate    |
|:------------|:------------|
| carries     | 18/20 (90%) |
| completions | 7/12 (58%)  |
| pass_yds    | 7/9 (78%)   |
| rec_yds     | 16/19 (84%) |
| receptions  | 13/23 (57%) |
| rush_yds    | 5/9 (56%)   |
| targets     | 9/23 (39%)  |

## Every call, no filters (for comparison)

All over/under calls on players above the usage floor, before the trend gate, signal count and top-5 cut: **165/255 (65%)**. If the picks above beat this, the filters are adding value.

Hit rate by model edge (quartiles): does a bigger edge win more often?

| edge_bin        | hit rate    |
|:----------------|:------------|
| (-0.001, 0.157] | 38/65 (58%) |
| (0.157, 0.215]  | 38/64 (59%) |
| (0.215, 0.295]  | 45/63 (71%) |
| (0.295, 0.528]  | 44/63 (70%) |

## Does each filter add anything? (lift over a no-information call)

`no-info rate` = how often a call on that side of the baseline would hit with no model at all (yardage stats land under their own average more often than not, so unders start ahead). `lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.

Unfiltered calls overall:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| all   |  255.00 |       0.65 |           0.50 |   0.15 |

Usage trend agrees with the call (the qualification rule):

| usage trend agrees   |   calls |   hit rate |   no-info rate |   lift |
|:---------------------|--------:|-----------:|---------------:|-------:|
| False                |  131.00 |       0.69 |           0.52 |   0.17 |
| True                 |  124.00 |       0.60 |           0.47 |   0.13 |

Number of agreeing signals:

|   n_signals |   calls |   hit rate |   no-info rate |   lift |
|------------:|--------:|-----------:|---------------:|-------:|
|           0 |   23.00 |       0.70 |           0.53 |   0.16 |
|           1 |   86.00 |       0.63 |           0.49 |   0.13 |
|           2 |   85.00 |       0.67 |           0.50 |   0.17 |
|           3 |   44.00 |       0.68 |           0.49 |   0.19 |
|           4 |   15.00 |       0.53 |           0.47 |   0.07 |
|           5 |    2.00 |       0.00 |           0.50 |  -0.50 |

Top-5 picks:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| picks |  115.00 |       0.65 |           0.48 |   0.17 |

## Where the team-total miss comes from

Projected vs actual per team-game for each piece of the scoring model (`corr` near 0 = the model can't tell teams apart on that piece; `sd_projected` far above `sd_actual` x corr = projections spread too wide).

| component     |   projected |   actual |   bias |   mae |   corr |   sd_projected |   sd_actual |
|:--------------|------------:|---------:|-------:|------:|-------:|---------------:|------------:|
| plays         |       60.17 |    61.52 |  -1.35 |  6.64 |   0.07 |           1.67 |        8.69 |
| dropbacks     |       36.24 |    37.56 |  -1.33 |  7.20 |   0.05 |           3.16 |        8.71 |
| pass_att      |       31.91 |    33.44 |  -1.53 |  6.75 |   0.20 |           3.27 |        8.59 |
| runs          |       23.93 |    23.95 |  -0.02 |  4.76 |   0.18 |           3.19 |        5.84 |
| sacks         |        2.25 |     2.26 |  -0.02 |  1.26 |   0.02 |           0.32 |        1.54 |
| interceptions |        0.72 |     0.69 |   0.03 |  0.70 |   0.04 |           0.30 |        0.80 |
| pass_td       |        1.59 |     1.55 |   0.04 |  0.90 |   0.26 |           0.41 |        1.16 |
| rush_td       |        0.97 |     0.93 |   0.04 |  0.90 |  -0.08 |           0.42 |        1.01 |
| td            |        2.56 |     2.48 |   0.08 |  1.12 |   0.18 |           0.52 |        1.41 |
| fga           |        1.91 |     2.10 |  -0.19 |  1.38 |  -0.13 |           1.02 |        1.23 |
| fgm           |        1.62 |     1.79 |  -0.17 |  1.27 |  -0.07 |           0.87 |        1.24 |
| points        |       22.64 |    22.96 |  -0.32 |  7.86 |   0.12 |           3.83 |        9.39 |

| part                                           |   share of points-miss variance |
|:-----------------------------------------------|--------------------------------:|
| touchdowns (x6.95)                             |                            0.88 |
| field goals (x3)                               |                            0.10 |
| other (defensive / return TDs, 2-pt, safeties) |                            0.03 |

Actual drives per team-game: 10.5 (sd 1.6); points per drive 2.23 (sd 0.98). Correlation of the points miss (actual - projected) with drive count: +0.02; with points per drive: +0.85. Red-zone trips per game 3.2, red-zone TD rate 59%.

## Player projections vs a naive season average

Mean absolute error on players who got the ball (lower is better).

| stat        |      n |   model_mae |   naive_mae | model_better   |
|:------------|-------:|------------:|------------:|:---------------|
| carries     | 453.00 |        2.63 |        2.88 | True           |
| completions | 127.00 |        5.03 |        5.51 | True           |
| pass_yds    | 127.00 |       63.86 |       72.25 | True           |
| rec_yds     | 904.00 |       21.15 |       22.05 | True           |
| receptions  | 904.00 |        1.60 |        1.64 | True           |
| rush_yds    | 453.00 |       17.05 |       18.17 | True           |
| targets     | 904.00 |        2.12 |        2.05 | False          |

## Team totals

Mean absolute error in points per team-game (lower is better).

| source                |   MAE |
|:----------------------|------:|
| model (final)         |  7.86 |
| model (before script) |  7.86 |
| market implied total  |  7.02 |
| team's season average |  8.85 |

By week:

|   week |   model |   market |   season_avg |
|-------:|--------:|---------:|-------------:|
|      2 |    9.21 |     8.28 |        12.06 |
|      3 |    8.72 |     7.36 |         8.03 |
|      4 |    5.82 |     5.58 |         7.35 |
|      5 |    7.68 |     6.85 |         7.91 |
