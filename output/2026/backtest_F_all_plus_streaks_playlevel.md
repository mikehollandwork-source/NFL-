# Backtest

Weeks 2-5 replayed with only the data available before each week (play-by-play, stats, injury report, depth chart as of that week). Left out because they were gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 produce none.

## Picks (top 5 per game)

- **Overall: 70/114 (61%)** (voids: 5, pushes: 3)
- Week 4: 35/60 (58%)
- Week 5: 35/54 (65%)
- overs: 43/74 (58%)
- unders: 27/40 (68%)
- Rank 1 picks only: 19/29 (66%)

By stat:

| stat        | hit rate    |
|:------------|:------------|
| carries     | 13/16 (81%) |
| completions | 7/8 (88%)   |
| pass_yds    | 8/14 (57%)  |
| rec_yds     | 17/26 (65%) |
| receptions  | 11/19 (58%) |
| rush_yds    | 9/18 (50%)  |
| targets     | 5/13 (38%)  |

## Every call, no filters (for comparison)

All over/under calls on players above the usage floor, before the trend gate, signal count and top-5 cut: **153/258 (59%)**. If the picks above beat this, the filters are adding value.

Hit rate by model edge (quartiles): does a bigger edge win more often?

| edge_bin        | hit rate    |
|:----------------|:------------|
| (-0.001, 0.172] | 35/65 (54%) |
| (0.172, 0.226]  | 39/64 (61%) |
| (0.226, 0.321]  | 35/64 (55%) |
| (0.321, 0.537]  | 44/65 (68%) |

## Does each filter add anything? (lift over a no-information call)

`no-info rate` = how often a call on that side of the baseline would hit with no model at all (yardage stats land under their own average more often than not, so unders start ahead). `lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.

Unfiltered calls overall:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| all   |  258.00 |       0.59 |           0.49 |   0.10 |

Usage trend agrees with the call (the qualification rule):

| usage trend agrees   |   calls |   hit rate |   no-info rate |   lift |
|:---------------------|--------:|-----------:|---------------:|-------:|
| False                |  146.00 |       0.60 |           0.51 |   0.09 |
| True                 |  112.00 |       0.58 |           0.47 |   0.11 |

Number of agreeing signals:

|   n_signals |   calls |   hit rate |   no-info rate |   lift |
|------------:|--------:|-----------:|---------------:|-------:|
|           0 |   20.00 |       0.60 |           0.51 |   0.09 |
|           1 |   72.00 |       0.58 |           0.50 |   0.09 |
|           2 |   83.00 |       0.59 |           0.50 |   0.09 |
|           3 |   59.00 |       0.61 |           0.49 |   0.12 |
|           4 |   18.00 |       0.67 |           0.50 |   0.16 |
|           5 |    6.00 |       0.33 |           0.43 |  -0.10 |

Top-5 picks:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| picks |  114.00 |       0.61 |           0.48 |   0.13 |

## Where the team-total miss comes from

Projected vs actual per team-game for each piece of the scoring model (`corr` near 0 = the model can't tell teams apart on that piece; `sd_projected` far above `sd_actual` x corr = projections spread too wide).

| component     |   projected |   actual |   bias |   mae |   corr |   sd_projected |   sd_actual |
|:--------------|------------:|---------:|-------:|------:|-------:|---------------:|------------:|
| plays         |       60.23 |    61.52 |  -1.29 |  7.69 |   0.03 |           5.47 |        8.69 |
| dropbacks     |       36.21 |    37.56 |  -1.36 |  7.36 |   0.08 |           4.34 |        8.71 |
| pass_att      |       31.87 |    33.44 |  -1.58 |  6.98 |   0.20 |           4.34 |        8.59 |
| runs          |       24.02 |    23.95 |   0.06 |  5.33 |   0.11 |           4.42 |        5.84 |
| sacks         |        2.27 |     2.26 |   0.00 |  1.55 |   0.02 |           1.28 |        1.54 |
| interceptions |        0.71 |     0.69 |   0.02 |  0.71 |   0.01 |           0.29 |        0.80 |
| pass_td       |        1.60 |     1.55 |   0.05 |  0.87 |   0.32 |           0.45 |        1.16 |
| rush_td       |        0.97 |     0.93 |   0.05 |  0.90 |  -0.04 |           0.47 |        1.01 |
| td            |        2.58 |     2.48 |   0.10 |  1.10 |   0.25 |           0.63 |        1.41 |
| fga           |        1.91 |     2.10 |  -0.19 |  1.38 |  -0.13 |           1.02 |        1.23 |
| fgm           |        1.62 |     1.79 |  -0.17 |  1.27 |  -0.08 |           0.87 |        1.24 |
| points        |       22.76 |    22.96 |  -0.20 |  7.72 |   0.18 |           4.59 |        9.39 |

| part                                           |   share of points-miss variance |
|:-----------------------------------------------|--------------------------------:|
| touchdowns (x6.95)                             |                            0.87 |
| field goals (x3)                               |                            0.11 |
| other (defensive / return TDs, 2-pt, safeties) |                            0.03 |

Actual drives per team-game: 10.5 (sd 1.6); points per drive 2.23 (sd 0.98). Correlation of the points miss (actual - projected) with drive count: +0.04; with points per drive: +0.82. Red-zone trips per game 3.2, red-zone TD rate 59%.

## Player projections vs a naive season average

Mean absolute error on players who got the ball (lower is better).

| stat        |      n |   model_mae |   naive_mae | model_better   |
|:------------|-------:|------------:|------------:|:---------------|
| carries     | 453.00 |        2.79 |        2.88 | True           |
| completions | 127.00 |        5.33 |        5.51 | True           |
| pass_yds    | 127.00 |       65.62 |       72.25 | True           |
| rec_yds     | 904.00 |       21.67 |       22.05 | True           |
| receptions  | 904.00 |        1.61 |        1.64 | True           |
| rush_yds    | 453.00 |       17.88 |       18.17 | True           |
| targets     | 904.00 |        2.12 |        2.05 | False          |

## Team totals

Mean absolute error in points per team-game (lower is better).

| source                |   MAE |
|:----------------------|------:|
| model (final)         |  7.72 |
| model (before script) |  7.79 |
| market implied total  |  7.02 |
| team's season average |  8.85 |

By week:

|   week |   model |   market |   season_avg |
|-------:|--------:|---------:|-------------:|
|      2 |    9.06 |     8.28 |        12.06 |
|      3 |    8.48 |     7.36 |         8.03 |
|      4 |    5.96 |     5.58 |         7.35 |
|      5 |    7.38 |     6.85 |         7.91 |
