# Backtest

Weeks 2-5 replayed with only the data available before each week (play-by-play, stats, injury report, depth chart as of that week). Left out because they were gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 produce none.

## Picks (top 5 per game)

- **Overall: 70/112 (62%)** (voids: 6, pushes: 1)
- Week 4: 37/61 (61%)
- Week 5: 33/51 (65%)
- overs: 38/69 (55%)
- unders: 32/43 (74%)
- Rank 1 picks only: 19/28 (68%)

By stat:

| stat        | hit rate    |
|:------------|:------------|
| carries     | 16/18 (89%) |
| completions | 2/3 (67%)   |
| pass_yds    | 11/15 (73%) |
| rec_yds     | 17/27 (63%) |
| receptions  | 10/19 (53%) |
| rush_yds    | 6/11 (55%)  |
| targets     | 8/19 (42%)  |

## Every call, no filters (for comparison)

All over/under calls on players above the usage floor, before the trend gate, signal count and top-5 cut: **162/255 (64%)**. If the picks above beat this, the filters are adding value.

Hit rate by model edge (quartiles): does a bigger edge win more often?

| edge_bin        | hit rate    |
|:----------------|:------------|
| (-0.001, 0.142] | 37/64 (58%) |
| (0.142, 0.198]  | 42/64 (66%) |
| (0.198, 0.27]   | 40/63 (63%) |
| (0.27, 0.521]   | 43/64 (67%) |

## Does each filter add anything? (lift over a no-information call)

`no-info rate` = how often a call on that side of the baseline would hit with no model at all (yardage stats land under their own average more often than not, so unders start ahead). `lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.

Unfiltered calls overall:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| all   |  255.00 |       0.64 |           0.50 |   0.14 |

Usage trend agrees with the call (the qualification rule):

| usage trend agrees   |   calls |   hit rate |   no-info rate |   lift |
|:---------------------|--------:|-----------:|---------------:|-------:|
| False                |  146.00 |       0.63 |           0.51 |   0.12 |
| True                 |  109.00 |       0.64 |           0.48 |   0.17 |

Number of agreeing signals:

|   n_signals |   calls |   hit rate |   no-info rate |   lift |
|------------:|--------:|-----------:|---------------:|-------:|
|           0 |   19.00 |       0.68 |           0.51 |   0.18 |
|           1 |   79.00 |       0.63 |           0.50 |   0.13 |
|           2 |   90.00 |       0.68 |           0.50 |   0.18 |
|           3 |   49.00 |       0.59 |           0.49 |   0.10 |
|           4 |   14.00 |       0.57 |           0.49 |   0.08 |
|           5 |    4.00 |       0.25 |           0.51 |  -0.26 |

Top-5 picks:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| picks |  112.00 |       0.62 |           0.47 |   0.15 |

## Where the team-total miss comes from

Projected vs actual per team-game for each piece of the scoring model (`corr` near 0 = the model can't tell teams apart on that piece; `sd_projected` far above `sd_actual` x corr = projections spread too wide).

| component     |   projected |   actual |   bias |   mae |   corr |   sd_projected |   sd_actual |
|:--------------|------------:|---------:|-------:|------:|-------:|---------------:|------------:|
| plays         |       60.25 |    61.52 |  -1.26 |  8.99 |   0.02 |           7.99 |        8.69 |
| dropbacks     |       36.16 |    37.56 |  -1.40 |  7.56 |   0.12 |           5.20 |        8.71 |
| pass_att      |       31.86 |    33.44 |  -1.59 |  7.21 |   0.21 |           5.16 |        8.59 |
| runs          |       24.09 |    23.95 |   0.14 |  5.90 |   0.01 |           5.09 |        5.84 |
| sacks         |        2.24 |     2.26 |  -0.02 |  1.54 |   0.03 |           1.25 |        1.54 |
| interceptions |        0.70 |     0.69 |   0.01 |  0.72 |  -0.00 |           0.30 |        0.80 |
| pass_td       |        1.59 |     1.55 |   0.04 |  0.91 |   0.25 |           0.44 |        1.16 |
| rush_td       |        0.98 |     0.93 |   0.06 |  0.94 |  -0.10 |           0.49 |        1.01 |
| td            |        2.57 |     2.48 |   0.09 |  1.17 |   0.13 |           0.65 |        1.41 |
| fga           |        1.91 |     2.10 |  -0.19 |  1.37 |  -0.12 |           1.02 |        1.23 |
| fgm           |        1.62 |     1.79 |  -0.17 |  1.26 |  -0.07 |           0.87 |        1.24 |
| points        |       22.72 |    22.96 |  -0.24 |  8.22 |   0.07 |           4.77 |        9.39 |

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
| carries     | 453.00 |        2.89 |        2.88 | False          |
| completions | 127.00 |        5.30 |        5.51 | True           |
| pass_yds    | 127.00 |       63.78 |       72.25 | True           |
| rec_yds     | 904.00 |       21.32 |       22.05 | True           |
| receptions  | 904.00 |        1.60 |        1.64 | True           |
| rush_yds    | 453.00 |       17.79 |       18.17 | True           |
| targets     | 904.00 |        2.13 |        2.05 | False          |

## Team totals

Mean absolute error in points per team-game (lower is better).

| source                |   MAE |
|:----------------------|------:|
| model (final)         |  8.22 |
| model (before script) |  8.21 |
| market implied total  |  7.02 |
| team's season average |  8.85 |

By week:

|   week |   model |   market |   season_avg |
|-------:|--------:|---------:|-------------:|
|      2 |   10.23 |     8.28 |        12.06 |
|      3 |    8.89 |     7.36 |         8.03 |
|      4 |    5.76 |     5.58 |         7.35 |
|      5 |    7.97 |     6.85 |         7.91 |
