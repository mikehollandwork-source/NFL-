# Backtest

Weeks 2-5 replayed with only the data available before each week (play-by-play, stats, injury report, depth chart as of that week). Left out because they were gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 produce none.

## Picks (top 5 per game)

- **Overall: 70/113 (62%)** (voids: 7, pushes: 2)
- Week 4: 35/60 (58%)
- Week 5: 35/53 (66%)
- overs: 41/72 (57%)
- unders: 29/41 (71%)
- Rank 1 picks only: 21/29 (72%)

By stat:

| stat        | hit rate    |
|:------------|:------------|
| carries     | 17/19 (89%) |
| completions | 3/7 (43%)   |
| pass_yds    | 9/13 (69%)  |
| rec_yds     | 17/23 (74%) |
| receptions  | 10/18 (56%) |
| rush_yds    | 6/13 (46%)  |
| targets     | 8/20 (40%)  |

## Every call, no filters (for comparison)

All over/under calls on players above the usage floor, before the trend gate, signal count and top-5 cut: **161/257 (63%)**. If the picks above beat this, the filters are adding value.

Hit rate by model edge (quartiles): does a bigger edge win more often?

| edge_bin        | hit rate    |
|:----------------|:------------|
| (-0.001, 0.162] | 36/65 (55%) |
| (0.162, 0.211]  | 39/64 (61%) |
| (0.211, 0.292]  | 39/65 (60%) |
| (0.292, 0.542]  | 47/63 (75%) |

## Does each filter add anything? (lift over a no-information call)

`no-info rate` = how often a call on that side of the baseline would hit with no model at all (yardage stats land under their own average more often than not, so unders start ahead). `lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.

Unfiltered calls overall:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| all   |  257.00 |       0.63 |           0.50 |   0.13 |

Usage trend agrees with the call (the qualification rule):

| usage trend agrees   |   calls |   hit rate |   no-info rate |   lift |
|:---------------------|--------:|-----------:|---------------:|-------:|
| False                |  136.00 |       0.65 |           0.52 |   0.13 |
| True                 |  121.00 |       0.60 |           0.48 |   0.13 |

Number of agreeing signals:

|   n_signals |   calls |   hit rate |   no-info rate |   lift |
|------------:|--------:|-----------:|---------------:|-------:|
|           0 |   19.00 |       0.74 |           0.54 |   0.20 |
|           1 |   73.00 |       0.62 |           0.51 |   0.11 |
|           2 |   81.00 |       0.63 |           0.50 |   0.13 |
|           3 |   60.00 |       0.60 |           0.48 |   0.12 |
|           4 |   18.00 |       0.72 |           0.48 |   0.24 |
|           5 |    6.00 |       0.33 |           0.44 |  -0.11 |

Top-5 picks:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| picks |  113.00 |       0.62 |           0.47 |   0.15 |

## Where the team-total miss comes from

Projected vs actual per team-game for each piece of the scoring model (`corr` near 0 = the model can't tell teams apart on that piece; `sd_projected` far above `sd_actual` x corr = projections spread too wide).

| component     |   projected |   actual |   bias |   mae |   corr |   sd_projected |   sd_actual |
|:--------------|------------:|---------:|-------:|------:|-------:|---------------:|------------:|
| plays         |       60.20 |    61.52 |  -1.31 |  7.68 |   0.03 |           5.47 |        8.69 |
| dropbacks     |       36.19 |    37.56 |  -1.37 |  7.38 |   0.07 |           4.29 |        8.71 |
| pass_att      |       31.85 |    33.44 |  -1.59 |  6.99 |   0.19 |           4.28 |        8.59 |
| runs          |       24.01 |    23.95 |   0.06 |  5.38 |   0.10 |           4.43 |        5.84 |
| sacks         |        2.26 |     2.26 |   0.00 |  1.56 |   0.02 |           1.29 |        1.54 |
| interceptions |        0.71 |     0.69 |   0.02 |  0.71 |   0.01 |           0.30 |        0.80 |
| pass_td       |        1.60 |     1.55 |   0.05 |  0.87 |   0.32 |           0.45 |        1.16 |
| rush_td       |        0.98 |     0.93 |   0.05 |  0.91 |  -0.04 |           0.48 |        1.01 |
| td            |        2.57 |     2.48 |   0.10 |  1.10 |   0.24 |           0.64 |        1.41 |
| fga           |        1.92 |     2.10 |  -0.18 |  1.38 |  -0.12 |           1.02 |        1.23 |
| fgm           |        1.62 |     1.79 |  -0.16 |  1.27 |  -0.07 |           0.87 |        1.24 |
| points        |       22.78 |    22.96 |  -0.18 |  7.76 |   0.17 |           4.62 |        9.39 |

| part                                           |   share of points-miss variance |
|:-----------------------------------------------|--------------------------------:|
| touchdowns (x6.95)                             |                            0.86 |
| field goals (x3)                               |                            0.11 |
| other (defensive / return TDs, 2-pt, safeties) |                            0.03 |

Actual drives per team-game: 10.5 (sd 1.6); points per drive 2.23 (sd 0.98). Correlation of the points miss (actual - projected) with drive count: +0.03; with points per drive: +0.81. Red-zone trips per game 3.2, red-zone TD rate 59%.

## Player projections vs a naive season average

Mean absolute error on players who got the ball (lower is better).

| stat        |      n |   model_mae |   naive_mae | model_better   |
|:------------|-------:|------------:|------------:|:---------------|
| carries     | 453.00 |        2.75 |        2.88 | True           |
| completions | 127.00 |        5.27 |        5.51 | True           |
| pass_yds    | 127.00 |       64.29 |       72.25 | True           |
| rec_yds     | 904.00 |       21.23 |       22.05 | True           |
| receptions  | 904.00 |        1.60 |        1.64 | True           |
| rush_yds    | 453.00 |       17.37 |       18.17 | True           |
| targets     | 904.00 |        2.13 |        2.05 | False          |

## Team totals

Mean absolute error in points per team-game (lower is better).

| source                |   MAE |
|:----------------------|------:|
| model (final)         |  7.76 |
| model (before script) |  7.85 |
| market implied total  |  7.02 |
| team's season average |  8.85 |

By week:

|   week |   model |   market |   season_avg |
|-------:|--------:|---------:|-------------:|
|      2 |    9.16 |     8.28 |        12.06 |
|      3 |    8.49 |     7.36 |         8.03 |
|      4 |    5.98 |     5.58 |         7.35 |
|      5 |    7.38 |     6.85 |         7.91 |
