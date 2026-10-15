# Backtest

Weeks 2-5 replayed with only the data available before each week (play-by-play, stats, injury report, depth chart as of that week). Left out because they were gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 produce none.

## Picks (top 5 per game)

- **Overall: 68/112 (61%)** (voids: 6, pushes: 1)
- Week 4: 36/64 (56%)
- Week 5: 32/48 (67%)
- overs: 38/68 (56%)
- unders: 30/44 (68%)
- Rank 1 picks only: 19/30 (63%)

By stat:

| stat        | hit rate    |
|:------------|:------------|
| carries     | 16/18 (89%) |
| completions | 4/9 (44%)   |
| pass_yds    | 8/11 (73%)  |
| rec_yds     | 15/19 (79%) |
| receptions  | 12/20 (60%) |
| rush_yds    | 7/11 (64%)  |
| targets     | 6/24 (25%)  |

## Every call, no filters (for comparison)

All over/under calls on players above the usage floor, before the trend gate, signal count and top-5 cut: **163/259 (63%)**. If the picks above beat this, the filters are adding value.

Hit rate by model edge (quartiles): does a bigger edge win more often?

| edge_bin        | hit rate    |
|:----------------|:------------|
| (-0.001, 0.154] | 34/65 (52%) |
| (0.154, 0.21]   | 40/67 (60%) |
| (0.21, 0.294]   | 45/63 (71%) |
| (0.294, 0.54]   | 44/64 (69%) |

## Does each filter add anything? (lift over a no-information call)

`no-info rate` = how often a call on that side of the baseline would hit with no model at all (yardage stats land under their own average more often than not, so unders start ahead). `lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.

Unfiltered calls overall:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| all   |  259.00 |       0.63 |           0.50 |   0.13 |

Usage trend agrees with the call (the qualification rule):

| usage trend agrees   |   calls |   hit rate |   no-info rate |   lift |
|:---------------------|--------:|-----------:|---------------:|-------:|
| False                |  132.00 |       0.67 |           0.52 |   0.16 |
| True                 |  127.00 |       0.58 |           0.48 |   0.10 |

Number of agreeing signals:

|   n_signals |   calls |   hit rate |   no-info rate |   lift |
|------------:|--------:|-----------:|---------------:|-------:|
|           0 |   26.00 |       0.73 |           0.50 |   0.23 |
|           1 |   85.00 |       0.62 |           0.50 |   0.12 |
|           2 |   94.00 |       0.63 |           0.50 |   0.12 |
|           3 |   42.00 |       0.60 |           0.49 |   0.10 |
|           4 |   11.00 |       0.64 |           0.46 |   0.18 |
|           5 |    1.00 |       0.00 |           0.41 |  -0.41 |

Top-5 picks:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| picks |  112.00 |       0.61 |           0.48 |   0.12 |

## Where the team-total miss comes from

Projected vs actual per team-game for each piece of the scoring model (`corr` near 0 = the model can't tell teams apart on that piece; `sd_projected` far above `sd_actual` x corr = projections spread too wide).

| component     |   projected |   actual |   bias |   mae |   corr |   sd_projected |   sd_actual |
|:--------------|------------:|---------:|-------:|------:|-------:|---------------:|------------:|
| plays         |       60.17 |    61.52 |  -1.35 |  6.66 |   0.06 |           1.65 |        8.69 |
| dropbacks     |       36.24 |    37.56 |  -1.33 |  7.21 |   0.04 |           3.12 |        8.71 |
| pass_att      |       31.91 |    33.44 |  -1.54 |  6.75 |   0.20 |           3.24 |        8.59 |
| runs          |       23.93 |    23.95 |  -0.02 |  4.78 |   0.17 |           3.14 |        5.84 |
| sacks         |        2.25 |     2.26 |  -0.02 |  1.27 |   0.00 |           0.32 |        1.54 |
| interceptions |        0.71 |     0.69 |   0.02 |  0.71 |   0.03 |           0.30 |        0.80 |
| pass_td       |        1.59 |     1.55 |   0.04 |  0.90 |   0.26 |           0.41 |        1.16 |
| rush_td       |        0.96 |     0.93 |   0.03 |  0.90 |  -0.07 |           0.42 |        1.01 |
| td            |        2.55 |     2.48 |   0.07 |  1.12 |   0.17 |           0.53 |        1.41 |
| fga           |        1.91 |     2.10 |  -0.19 |  1.37 |  -0.11 |           1.02 |        1.23 |
| fgm           |        1.62 |     1.79 |  -0.17 |  1.26 |  -0.06 |           0.87 |        1.24 |
| points        |       22.59 |    22.96 |  -0.37 |  7.89 |   0.12 |           3.94 |        9.39 |

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
| carries     | 453.00 |        2.64 |        2.88 | True           |
| completions | 127.00 |        5.02 |        5.51 | True           |
| pass_yds    | 127.00 |       63.64 |       72.25 | True           |
| rec_yds     | 904.00 |       21.15 |       22.05 | True           |
| receptions  | 904.00 |        1.60 |        1.64 | True           |
| rush_yds    | 453.00 |       17.02 |       18.17 | True           |
| targets     | 904.00 |        2.12 |        2.05 | False          |

## Team totals

Mean absolute error in points per team-game (lower is better).

| source                |   MAE |
|:----------------------|------:|
| model (final)         |  7.89 |
| model (before script) |  7.91 |
| market implied total  |  7.02 |
| team's season average |  8.85 |

By week:

|   week |   model |   market |   season_avg |
|-------:|--------:|---------:|-------------:|
|      2 |    9.30 |     8.28 |        12.06 |
|      3 |    8.74 |     7.36 |         8.03 |
|      4 |    5.88 |     5.58 |         7.35 |
|      5 |    7.63 |     6.85 |         7.91 |
