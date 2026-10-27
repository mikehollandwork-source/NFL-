# Backtest

Weeks 4-5 replayed with only the data available before each week (play-by-play, stats, injury report, depth chart as of that week). Left out because they were gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 produce none.

## Picks (top 5 per game)

- **Overall: 70/118 (59%)** (voids: 6, pushes: 3)
- Week 4: 35/65 (54%)
- Week 5: 35/53 (66%)
- overs: 43/74 (58%)
- unders: 27/44 (61%)
- Rank 1 picks only: 19/29 (66%)

By stat:

| stat        | hit rate    |
|:------------|:------------|
| carries     | 15/18 (83%) |
| completions | 3/7 (43%)   |
| pass_yds    | 10/15 (67%) |
| rec_yds     | 17/23 (74%) |
| receptions  | 10/21 (48%) |
| rush_yds    | 6/11 (55%)  |
| targets     | 9/23 (39%)  |

## Every call, no filters (for comparison)

All over/under calls on players above the usage floor, before the trend gate, signal count and top-5 cut: **159/254 (63%)**. If the picks above beat this, the filters are adding value.

Hit rate by model edge (quartiles): does a bigger edge win more often?

| edge_bin       | hit rate    |
|:---------------|:------------|
| (-0.001, 0.16] | 33/64 (52%) |
| (0.16, 0.216]  | 38/63 (60%) |
| (0.216, 0.304] | 42/63 (67%) |
| (0.304, 0.55]  | 46/64 (72%) |

## Does each filter add anything? (lift over a no-information call)

`no-info rate` = how often a call on that side of the baseline would hit with no model at all (yardage stats land under their own average more often than not, so unders start ahead). `lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.

Unfiltered calls overall:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| all   |  254.00 |       0.63 |           0.50 |   0.13 |

Usage trend agrees with the call (the qualification rule):

| usage trend agrees   |   calls |   hit rate |   no-info rate |   lift |
|:---------------------|--------:|-----------:|---------------:|-------:|
| False                |  131.00 |       0.66 |           0.52 |   0.15 |
| True                 |  123.00 |       0.59 |           0.48 |   0.10 |

Number of agreeing signals:

|   n_signals |   calls |   hit rate |   no-info rate |   lift |
|------------:|--------:|-----------:|---------------:|-------:|
|           0 |   16.00 |       0.69 |           0.51 |   0.18 |
|           1 |   70.00 |       0.66 |           0.51 |   0.15 |
|           2 |   83.00 |       0.63 |           0.50 |   0.12 |
|           3 |   56.00 |       0.61 |           0.49 |   0.12 |
|           4 |   24.00 |       0.62 |           0.49 |   0.13 |
|           5 |    4.00 |       0.25 |           0.45 |  -0.20 |
|           6 |    1.00 |       0.00 |           0.55 |  -0.55 |

Top-5 picks:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| picks |  118.00 |       0.59 |           0.49 |   0.11 |

## Where the team-total miss comes from

Projected vs actual per team-game for each piece of the scoring model (`corr` near 0 = the model can't tell teams apart on that piece; `sd_projected` far above `sd_actual` x corr = projections spread too wide).

| component     |   projected |   actual |   bias |   mae |   corr |   sd_projected |   sd_actual |
|:--------------|------------:|---------:|-------:|------:|-------:|---------------:|------------:|
| plays         |       60.62 |    62.00 |  -1.38 |  6.67 |   0.13 |           1.62 |        9.29 |
| dropbacks     |       36.59 |    38.15 |  -1.56 |  7.22 |   0.05 |           3.28 |        8.93 |
| pass_att      |       32.50 |    33.92 |  -1.42 |  7.23 |   0.23 |           3.42 |        9.20 |
| runs          |       24.03 |    23.85 |   0.17 |  4.39 |   0.34 |           3.26 |        6.05 |
| sacks         |        2.18 |     2.34 |  -0.16 |  1.54 |   0.02 |           0.97 |        1.62 |
| interceptions |        0.71 |     0.69 |   0.02 |  0.76 |  -0.01 |           0.29 |        0.86 |
| pass_td       |        1.61 |     1.45 |   0.16 |  0.74 |   0.40 |           0.45 |        1.04 |
| rush_td       |        0.88 |     1.21 |  -0.33 |  0.91 |  -0.01 |           0.40 |        1.04 |
| td            |        2.49 |     2.66 |  -0.17 |  0.91 |   0.38 |           0.53 |        1.32 |
| fga           |        2.01 |     2.13 |  -0.12 |  1.22 |  -0.02 |           0.76 |        1.27 |
| fgm           |        1.71 |     1.81 |  -0.10 |  1.14 |  -0.01 |           0.65 |        1.27 |
| points        |       22.45 |    24.03 |  -1.58 |  6.68 |   0.30 |           3.88 |        8.72 |

| part                                           |   share of points-miss variance |
|:-----------------------------------------------|--------------------------------:|
| touchdowns (x6.95)                             |                            0.86 |
| field goals (x3)                               |                            0.13 |
| other (defensive / return TDs, 2-pt, safeties) |                            0.01 |

Actual drives per team-game: 10.8 (sd 1.5); points per drive 2.25 (sd 0.84). Correlation of the points miss (actual - projected) with drive count: +0.16; with points per drive: +0.83. Red-zone trips per game 3.1, red-zone TD rate 63%.

## Player projections vs a naive season average

Mean absolute error on players who got the ball (lower is better).

| stat        |      n |   model_mae |   naive_mae | model_better   |
|:------------|-------:|------------:|------------:|:---------------|
| carries     | 230.00 |        2.58 |        2.63 | True           |
| completions |  62.00 |        5.50 |        5.61 | True           |
| pass_yds    |  62.00 |       69.78 |       69.98 | True           |
| rec_yds     | 466.00 |       20.71 |       21.24 | True           |
| receptions  | 466.00 |        1.52 |        1.52 | True           |
| rush_yds    | 230.00 |       16.37 |       16.67 | True           |
| targets     | 466.00 |        2.03 |        1.95 | False          |

## Team totals

Mean absolute error in points per team-game (lower is better).

| source                |   MAE |
|:----------------------|------:|
| model (final)         |  6.68 |
| model (before script) |  6.68 |
| market implied total  |  6.19 |
| team's season average |  7.62 |

By week:

|   week |   model |   market |   season_avg |
|-------:|--------:|---------:|-------------:|
|      4 |    5.98 |     5.58 |         7.35 |
|      5 |    7.43 |     6.85 |         7.91 |
