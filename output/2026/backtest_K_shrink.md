# Backtest

Weeks 2-5 replayed with only the data available before each week (play-by-play, stats, injury report, depth chart as of that week). Left out because they were gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 produce none.

## Picks (top 5 per game)

- **Overall: 63/108 (58%)** (voids: 5, pushes: 3)
- Week 4: 34/62 (55%)
- Week 5: 29/46 (63%)
- overs: 33/62 (53%)
- unders: 30/46 (65%)
- Rank 1 picks only: 17/29 (59%)

By stat:

| stat        | hit rate     |
|:------------|:-------------|
| carries     | 10/10 (100%) |
| completions | 3/7 (43%)    |
| pass_yds    | 5/8 (62%)    |
| rec_yds     | 17/22 (77%)  |
| receptions  | 12/21 (57%)  |
| rush_yds    | 6/11 (55%)   |
| targets     | 10/29 (34%)  |

## Every call, no filters (for comparison)

All over/under calls on players above the usage floor, before the trend gate, signal count and top-5 cut: **159/254 (63%)**. If the picks above beat this, the filters are adding value.

Hit rate by model edge (quartiles): does a bigger edge win more often?

| edge_bin        | hit rate    |
|:----------------|:------------|
| (-0.001, 0.154] | 34/65 (52%) |
| (0.154, 0.214]  | 38/63 (60%) |
| (0.214, 0.304]  | 46/63 (73%) |
| (0.304, 0.53]   | 41/63 (65%) |

## Does each filter add anything? (lift over a no-information call)

`no-info rate` = how often a call on that side of the baseline would hit with no model at all (yardage stats land under their own average more often than not, so unders start ahead). `lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.

Unfiltered calls overall:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| all   |  254.00 |       0.63 |           0.50 |   0.13 |

Usage trend agrees with the call (the qualification rule):

| usage trend agrees   |   calls |   hit rate |   no-info rate |   lift |
|:---------------------|--------:|-----------:|---------------:|-------:|
| False                |  132.00 |       0.66 |           0.52 |   0.14 |
| True                 |  122.00 |       0.59 |           0.47 |   0.12 |

Number of agreeing signals:

|   n_signals |   calls |   hit rate |   no-info rate |   lift |
|------------:|--------:|-----------:|---------------:|-------:|
|           0 |   24.00 |       0.54 |           0.53 |   0.02 |
|           1 |   77.00 |       0.70 |           0.51 |   0.19 |
|           2 |   77.00 |       0.61 |           0.48 |   0.13 |
|           3 |   53.00 |       0.62 |           0.48 |   0.14 |
|           4 |   18.00 |       0.56 |           0.50 |   0.05 |
|           5 |    4.00 |       0.50 |           0.50 |   0.00 |
|           6 |    1.00 |       0.00 |           0.60 |  -0.60 |

Top-5 picks:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| picks |  108.00 |       0.58 |           0.48 |   0.11 |

## Where the team-total miss comes from

Projected vs actual per team-game for each piece of the scoring model (`corr` near 0 = the model can't tell teams apart on that piece; `sd_projected` far above `sd_actual` x corr = projections spread too wide).

| component     |   projected |   actual |   bias |   mae |   corr |   sd_projected |   sd_actual |
|:--------------|------------:|---------:|-------:|------:|-------:|---------------:|------------:|
| plays         |       60.18 |    61.52 |  -1.33 |  6.66 |   0.06 |           1.67 |        8.69 |
| dropbacks     |       36.24 |    37.56 |  -1.32 |  7.09 |   0.07 |           2.94 |        8.71 |
| pass_att      |       31.92 |    33.44 |  -1.53 |  6.70 |   0.22 |           3.09 |        8.59 |
| runs          |       23.94 |    23.95 |  -0.01 |  4.65 |   0.17 |           2.99 |        5.84 |
| sacks         |        2.24 |     2.26 |  -0.02 |  1.26 |   0.03 |           0.32 |        1.54 |
| interceptions |        0.71 |     0.69 |   0.02 |  0.69 |   0.03 |           0.17 |        0.80 |
| pass_td       |        1.61 |     1.55 |   0.06 |  0.91 |   0.32 |           0.29 |        1.16 |
| rush_td       |        0.99 |     0.93 |   0.06 |  0.84 |   0.05 |           0.36 |        1.01 |
| td            |        2.59 |     2.48 |   0.12 |  1.11 |   0.21 |           0.41 |        1.41 |
| fga           |        1.91 |     2.10 |  -0.19 |  1.37 |  -0.12 |           1.01 |        1.23 |
| fgm           |        1.61 |     1.79 |  -0.17 |  1.26 |  -0.07 |           0.86 |        1.24 |
| points        |       22.88 |    22.96 |  -0.08 |  7.86 |   0.12 |           3.39 |        9.39 |

| part                                           |   share of points-miss variance |
|:-----------------------------------------------|--------------------------------:|
| touchdowns (x6.95)                             |                            0.86 |
| field goals (x3)                               |                            0.11 |
| other (defensive / return TDs, 2-pt, safeties) |                            0.03 |

Actual drives per team-game: 10.5 (sd 1.6); points per drive 2.23 (sd 0.98). Correlation of the points miss (actual - projected) with drive count: +0.05; with points per drive: +0.86. Red-zone trips per game 3.2, red-zone TD rate 59%.

## Player projections vs a naive season average

Mean absolute error on players who got the ball (lower is better).

| stat        |      n |   model_mae |   naive_mae | model_better   |
|:------------|-------:|------------:|------------:|:---------------|
| carries     | 453.00 |        2.64 |        2.88 | True           |
| completions | 127.00 |        5.08 |        5.51 | True           |
| pass_yds    | 127.00 |       63.18 |       72.25 | True           |
| rec_yds     | 904.00 |       21.18 |       22.05 | True           |
| receptions  | 904.00 |        1.60 |        1.64 | True           |
| rush_yds    | 453.00 |       17.02 |       18.17 | True           |
| targets     | 904.00 |        2.12 |        2.05 | False          |

## Team totals

Mean absolute error in points per team-game (lower is better).

| source                |   MAE |
|:----------------------|------:|
| model (final)         |  7.86 |
| model (before script) |  7.91 |
| market implied total  |  7.02 |
| team's season average |  8.85 |

By week:

|   week |   model |   market |   season_avg |
|-------:|--------:|---------:|-------------:|
|      2 |    9.32 |     8.28 |        12.06 |
|      3 |    7.94 |     7.36 |         8.03 |
|      4 |    6.78 |     5.58 |         7.35 |
|      5 |    7.38 |     6.85 |         7.91 |
