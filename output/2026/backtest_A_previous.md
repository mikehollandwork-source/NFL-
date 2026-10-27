# Backtest

Weeks 2-5 replayed with only the data available before each week (play-by-play, stats, injury report, depth chart as of that week). Left out because they were gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 produce none.

## Picks (top 5 per game)

- **Overall: 65/107 (61%)** (voids: 6, pushes: 4)
- Week 4: 34/58 (59%)
- Week 5: 31/49 (63%)
- overs: 36/66 (55%)
- unders: 29/41 (71%)
- Rank 1 picks only: 18/27 (67%)

By stat:

| stat        | hit rate    |
|:------------|:------------|
| carries     | 15/17 (88%) |
| completions | 3/3 (100%)  |
| pass_yds    | 8/13 (62%)  |
| rec_yds     | 17/27 (63%) |
| receptions  | 9/18 (50%)  |
| rush_yds    | 6/11 (55%)  |
| targets     | 7/18 (39%)  |

## Every call, no filters (for comparison)

All over/under calls on players above the usage floor, before the trend gate, signal count and top-5 cut: **165/255 (65%)**. If the picks above beat this, the filters are adding value.

Hit rate by model edge (quartiles): does a bigger edge win more often?

| edge_bin        | hit rate    |
|:----------------|:------------|
| (-0.001, 0.146] | 39/64 (61%) |
| (0.146, 0.202]  | 46/67 (69%) |
| (0.202, 0.272]  | 36/60 (60%) |
| (0.272, 0.522]  | 44/64 (69%) |

## Does each filter add anything? (lift over a no-information call)

`no-info rate` = how often a call on that side of the baseline would hit with no model at all (yardage stats land under their own average more often than not, so unders start ahead). `lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.

Unfiltered calls overall:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| all   |  255.00 |       0.65 |           0.50 |   0.14 |

Usage trend agrees with the call (the qualification rule):

| usage trend agrees   |   calls |   hit rate |   no-info rate |   lift |
|:---------------------|--------:|-----------:|---------------:|-------:|
| False                |  144.00 |       0.65 |           0.52 |   0.13 |
| True                 |  111.00 |       0.65 |           0.48 |   0.16 |

Number of agreeing signals:

|   n_signals |   calls |   hit rate |   no-info rate |   lift |
|------------:|--------:|-----------:|---------------:|-------:|
|           0 |   23.00 |       0.74 |           0.54 |   0.20 |
|           1 |   79.00 |       0.68 |           0.51 |   0.17 |
|           2 |   87.00 |       0.66 |           0.50 |   0.16 |
|           3 |   50.00 |       0.56 |           0.49 |   0.07 |
|           4 |   13.00 |       0.69 |           0.49 |   0.20 |
|           5 |    3.00 |       0.00 |           0.54 |  -0.54 |

Top-5 picks:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| picks |  107.00 |       0.61 |           0.48 |   0.13 |

## Where the team-total miss comes from

Projected vs actual per team-game for each piece of the scoring model (`corr` near 0 = the model can't tell teams apart on that piece; `sd_projected` far above `sd_actual` x corr = projections spread too wide).

| component     |   projected |   actual |   bias |   mae |   corr |   sd_projected |   sd_actual |
|:--------------|------------:|---------:|-------:|------:|-------:|---------------:|------------:|
| plays         |       60.22 |    61.52 |  -1.30 |  8.98 |   0.03 |           8.01 |        8.69 |
| dropbacks     |       36.16 |    37.56 |  -1.40 |  7.56 |   0.12 |           5.21 |        8.71 |
| pass_att      |       31.85 |    33.44 |  -1.59 |  7.21 |   0.22 |           5.17 |        8.59 |
| runs          |       24.06 |    23.95 |   0.11 |  5.90 |   0.01 |           5.11 |        5.84 |
| sacks         |        2.25 |     2.26 |  -0.02 |  1.54 |   0.03 |           1.25 |        1.54 |
| interceptions |        0.70 |     0.69 |   0.01 |  0.72 |  -0.01 |           0.29 |        0.80 |
| pass_td       |        1.59 |     1.55 |   0.04 |  0.91 |   0.24 |           0.45 |        1.16 |
| rush_td       |        0.98 |     0.93 |   0.05 |  0.94 |  -0.11 |           0.48 |        1.01 |
| td            |        2.57 |     2.48 |   0.10 |  1.17 |   0.13 |           0.65 |        1.41 |
| fga           |        1.91 |     2.10 |  -0.19 |  1.37 |  -0.12 |           1.01 |        1.23 |
| fgm           |        1.62 |     1.79 |  -0.17 |  1.27 |  -0.07 |           0.86 |        1.24 |
| points        |       22.74 |    22.96 |  -0.22 |  8.19 |   0.07 |           4.76 |        9.39 |

| part                                           |   share of points-miss variance |
|:-----------------------------------------------|--------------------------------:|
| touchdowns (x6.95)                             |                            0.88 |
| field goals (x3)                               |                            0.10 |
| other (defensive / return TDs, 2-pt, safeties) |                            0.02 |

Actual drives per team-game: 10.5 (sd 1.6); points per drive 2.23 (sd 0.98). Correlation of the points miss (actual - projected) with drive count: +0.03; with points per drive: +0.82. Red-zone trips per game 3.2, red-zone TD rate 59%.

## Player projections vs a naive season average

Mean absolute error on players who got the ball (lower is better).

| stat        |      n |   model_mae |   naive_mae | model_better   |
|:------------|-------:|------------:|------------:|:---------------|
| carries     | 453.00 |        2.88 |        2.88 | False          |
| completions | 127.00 |        5.29 |        5.51 | True           |
| pass_yds    | 127.00 |       63.67 |       72.25 | True           |
| rec_yds     | 904.00 |       21.27 |       22.05 | True           |
| receptions  | 904.00 |        1.60 |        1.64 | True           |
| rush_yds    | 453.00 |       17.78 |       18.17 | True           |
| targets     | 904.00 |        2.13 |        2.05 | False          |

## Team totals

Mean absolute error in points per team-game (lower is better).

| source                |   MAE |
|:----------------------|------:|
| model (final)         |  8.19 |
| model (before script) |  8.27 |
| market implied total  |  7.02 |
| team's season average |  8.85 |

By week:

|   week |   model |   market |   season_avg |
|-------:|--------:|---------:|-------------:|
|      2 |   10.23 |     8.28 |        12.06 |
|      3 |    8.94 |     7.36 |         8.03 |
|      4 |    5.69 |     5.58 |         7.35 |
|      5 |    7.89 |     6.85 |         7.91 |
