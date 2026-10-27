# Backtest

Weeks 2-5 replayed with only the data available before each week (play-by-play, stats, injury report, depth chart as of that week). Left out because they were gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 produce none.

## Picks (top 5 per game)

- **Overall: 69/104 (66%)** (voids: 7, pushes: 2)
- Week 4: 39/58 (67%)
- Week 5: 30/46 (65%)
- overs: 37/59 (63%)
- unders: 32/45 (71%)
- Rank 1 picks only: 19/28 (68%)

By stat:

| stat        | hit rate    |
|:------------|:------------|
| carries     | 14/15 (93%) |
| completions | 4/8 (50%)   |
| pass_yds    | 6/7 (86%)   |
| rec_yds     | 13/16 (81%) |
| receptions  | 16/22 (73%) |
| rush_yds    | 5/9 (56%)   |
| targets     | 11/27 (41%) |

## Every call, no filters (for comparison)

All over/under calls on players above the usage floor, before the trend gate, signal count and top-5 cut: **165/257 (64%)**. If the picks above beat this, the filters are adding value.

Hit rate by model edge (quartiles): does a bigger edge win more often?

| edge_bin        | hit rate    |
|:----------------|:------------|
| (-0.001, 0.147] | 32/65 (49%) |
| (0.147, 0.21]   | 44/64 (69%) |
| (0.21, 0.29]    | 46/64 (72%) |
| (0.29, 0.533]   | 43/64 (67%) |

## Does each filter add anything? (lift over a no-information call)

`no-info rate` = how often a call on that side of the baseline would hit with no model at all (yardage stats land under their own average more often than not, so unders start ahead). `lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.

Unfiltered calls overall:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| all   |  257.00 |       0.64 |           0.49 |   0.15 |

Usage trend agrees with the call (the qualification rule):

| usage trend agrees   |   calls |   hit rate |   no-info rate |   lift |
|:---------------------|--------:|-----------:|---------------:|-------:|
| False                |  130.00 |       0.68 |           0.52 |   0.16 |
| True                 |  127.00 |       0.61 |           0.47 |   0.14 |

Number of agreeing signals:

|   n_signals |   calls |   hit rate |   no-info rate |   lift |
|------------:|--------:|-----------:|---------------:|-------:|
|           0 |   31.00 |       0.65 |           0.52 |   0.13 |
|           1 |   79.00 |       0.67 |           0.49 |   0.18 |
|           2 |   90.00 |       0.63 |           0.49 |   0.14 |
|           3 |   42.00 |       0.64 |           0.47 |   0.17 |
|           4 |   12.00 |       0.58 |           0.49 |   0.09 |
|           5 |    3.00 |       0.33 |           0.56 |  -0.22 |

Top-5 picks:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| picks |  104.00 |       0.66 |           0.47 |   0.19 |

## Where the team-total miss comes from

Projected vs actual per team-game for each piece of the scoring model (`corr` near 0 = the model can't tell teams apart on that piece; `sd_projected` far above `sd_actual` x corr = projections spread too wide).

| component     |   projected |   actual |   bias |   mae |   corr |   sd_projected |   sd_actual |
|:--------------|------------:|---------:|-------:|------:|-------:|---------------:|------------:|
| plays         |       60.14 |    61.52 |  -1.38 |  6.69 |   0.05 |           1.66 |        8.69 |
| dropbacks     |       36.21 |    37.56 |  -1.35 |  7.07 |   0.06 |           2.72 |        8.71 |
| pass_att      |       31.89 |    33.44 |  -1.56 |  6.72 |   0.21 |           2.93 |        8.59 |
| runs          |       23.92 |    23.95 |  -0.03 |  4.73 |   0.14 |           2.74 |        5.84 |
| sacks         |        2.24 |     2.26 |  -0.02 |  1.25 |   0.03 |           0.30 |        1.54 |
| interceptions |        0.71 |     0.69 |   0.02 |  0.68 |   0.04 |           0.17 |        0.80 |
| pass_td       |        1.60 |     1.55 |   0.06 |  0.91 |   0.28 |           0.25 |        1.16 |
| rush_td       |        0.99 |     0.93 |   0.06 |  0.85 |   0.02 |           0.32 |        1.01 |
| td            |        2.59 |     2.48 |   0.11 |  1.14 |   0.12 |           0.34 |        1.41 |
| fga           |        1.91 |     2.10 |  -0.19 |  1.38 |  -0.13 |           1.02 |        1.23 |
| fgm           |        1.62 |     1.79 |  -0.17 |  1.27 |  -0.07 |           0.87 |        1.24 |
| points        |       22.86 |    22.96 |  -0.10 |  7.92 |   0.04 |           3.03 |        9.39 |

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
| completions | 127.00 |        5.07 |        5.51 | True           |
| pass_yds    | 127.00 |       62.95 |       72.25 | True           |
| rec_yds     | 904.00 |       21.14 |       22.05 | True           |
| receptions  | 904.00 |        1.60 |        1.64 | True           |
| rush_yds    | 453.00 |       17.12 |       18.17 | True           |
| targets     | 904.00 |        2.12 |        2.05 | False          |

## Team totals

Mean absolute error in points per team-game (lower is better).

| source                |   MAE |
|:----------------------|------:|
| model (final)         |  7.92 |
| model (before script) |  7.99 |
| market implied total  |  7.02 |
| team's season average |  8.85 |

By week:

|   week |   model |   market |   season_avg |
|-------:|--------:|---------:|-------------:|
|      2 |    9.41 |     8.28 |        12.06 |
|      3 |    8.13 |     7.36 |         8.03 |
|      4 |    6.45 |     5.58 |         7.35 |
|      5 |    7.69 |     6.85 |         7.91 |
