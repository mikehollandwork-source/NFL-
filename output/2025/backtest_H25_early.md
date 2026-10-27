# Backtest

Weeks 2-5 replayed with only the data available before each week (play-by-play, stats, injury report, depth chart as of that week). Left out because they were gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 produce none.

## Picks (top 5 per game)

- **Overall: 60/110 (55%)** (voids: 2, pushes: 3)
- Week 4: 29/56 (52%)
- Week 5: 31/54 (57%)
- overs: 20/45 (44%)
- unders: 40/65 (62%)
- Rank 1 picks only: 13/27 (48%)

By stat:

| stat        | hit rate    |
|:------------|:------------|
| carries     | 3/8 (38%)   |
| completions | 7/12 (58%)  |
| pass_yds    | 6/10 (60%)  |
| rec_yds     | 14/22 (64%) |
| receptions  | 14/32 (44%) |
| rush_yds    | 10/12 (83%) |
| targets     | 6/14 (43%)  |

## Every call, no filters (for comparison)

All over/under calls on players above the usage floor, before the trend gate, signal count and top-5 cut: **149/258 (58%)**. If the picks above beat this, the filters are adding value.

Hit rate by model edge (quartiles): does a bigger edge win more often?

| edge_bin        | hit rate    |
|:----------------|:------------|
| (-0.001, 0.157] | 34/65 (52%) |
| (0.157, 0.2]    | 44/65 (68%) |
| (0.2, 0.277]    | 30/63 (48%) |
| (0.277, 0.496]  | 41/65 (63%) |

## Does each filter add anything? (lift over a no-information call)

`no-info rate` = how often a call on that side of the baseline would hit with no model at all (yardage stats land under their own average more often than not, so unders start ahead). `lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.

Unfiltered calls overall:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| all   |  258.00 |       0.58 |           0.49 |   0.09 |

Usage trend agrees with the call (the qualification rule):

| usage trend agrees   |   calls |   hit rate |   no-info rate |   lift |
|:---------------------|--------:|-----------:|---------------:|-------:|
| False                |  133.00 |       0.61 |           0.49 |   0.12 |
| True                 |  125.00 |       0.54 |           0.49 |   0.06 |

Number of agreeing signals:

|   n_signals |   calls |   hit rate |   no-info rate |   lift |
|------------:|--------:|-----------:|---------------:|-------:|
|           0 |   28.00 |       0.64 |           0.51 |   0.13 |
|           1 |   75.00 |       0.61 |           0.47 |   0.14 |
|           2 |  109.00 |       0.54 |           0.50 |   0.05 |
|           3 |   40.00 |       0.55 |           0.49 |   0.06 |
|           4 |    6.00 |       0.67 |           0.49 |   0.18 |

Top-5 picks:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| picks |  110.00 |       0.55 |           0.50 |   0.05 |

## Where the team-total miss comes from

Projected vs actual per team-game for each piece of the scoring model (`corr` near 0 = the model can't tell teams apart on that piece; `sd_projected` far above `sd_actual` x corr = projections spread too wide).

| component     |   projected |   actual |   bias |   mae |   corr |   sd_projected |   sd_actual |
|:--------------|------------:|---------:|-------:|------:|-------:|---------------:|------------:|
| plays         |       60.00 |    60.38 |  -0.38 |  6.52 |   0.11 |           1.79 |        8.14 |
| dropbacks     |       36.87 |    36.93 |  -0.06 |  7.20 |  -0.02 |           3.20 |        8.08 |
| pass_att      |       32.20 |    32.63 |  -0.43 |  6.91 |   0.02 |           3.19 |        7.72 |
| runs          |       23.13 |    23.45 |  -0.32 |  5.07 |   0.14 |           3.21 |        6.07 |
| sacks         |        2.31 |     2.27 |   0.04 |  1.34 |   0.12 |           0.40 |        1.65 |
| interceptions |        0.64 |     0.72 |  -0.08 |  0.71 |   0.19 |           0.35 |        0.87 |
| pass_td       |        1.37 |     1.69 |  -0.32 |  0.96 |   0.03 |           0.39 |        1.11 |
| rush_td       |        0.88 |     0.90 |  -0.01 |  0.76 |   0.09 |           0.36 |        0.94 |
| td            |        2.25 |     2.58 |  -0.33 |  1.05 |   0.23 |           0.52 |        1.34 |
| fga           |        2.23 |     2.06 |   0.17 |  1.22 |   0.15 |           1.12 |        1.28 |
| fgm           |        1.89 |     1.71 |   0.19 |  1.09 |   0.17 |           0.95 |        1.20 |
| points        |       21.29 |    24.25 |  -2.96 |  8.16 |   0.12 |           4.11 |        9.98 |

| part                                           |   share of points-miss variance |
|:-----------------------------------------------|--------------------------------:|
| touchdowns (x6.95)                             |                            0.75 |
| field goals (x3)                               |                          nan    |
| other (defensive / return TDs, 2-pt, safeties) |                          nan    |

Actual drives per team-game: 10.3 (sd 1.3); points per drive 2.39 (sd 1.04). Correlation of the points miss (actual - projected) with drive count: +0.08; with points per drive: +0.84. Red-zone trips per game 3.3, red-zone TD rate 62%.

## Player projections vs a naive season average

Mean absolute error on players who got the ball (lower is better).

| stat        |      n |   model_mae |   naive_mae | model_better   |
|:------------|-------:|------------:|------------:|:---------------|
| carries     | 452.00 |        2.67 |        2.80 | True           |
| completions | 125.00 |        5.06 |        5.89 | True           |
| pass_yds    | 125.00 |       56.90 |       70.82 | True           |
| rec_yds     | 890.00 |       18.65 |       20.38 | True           |
| receptions  | 890.00 |        1.49 |        1.54 | True           |
| rush_yds    | 452.00 |       17.14 |       18.67 | True           |
| targets     | 890.00 |        1.96 |        1.94 | False          |

## Team totals

Mean absolute error in points per team-game (lower is better).

| source                |   MAE |
|:----------------------|------:|
| model (final)         |  8.16 |
| model (before script) |  8.19 |
| market implied total  |  7.12 |
| team's season average |  9.12 |

By week:

|   week |   model |   market |   season_avg |
|-------:|--------:|---------:|-------------:|
|      2 |    8.52 |     6.77 |        11.12 |
|      3 |    9.56 |     8.39 |         9.66 |
|      4 |    7.33 |     6.00 |         7.76 |
|      5 |    7.10 |     7.34 |         7.75 |
