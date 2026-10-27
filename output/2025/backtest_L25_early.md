# Backtest

Weeks 2-5 replayed with only the data available before each week (play-by-play, stats, injury report, depth chart as of that week). Left out because they were gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 produce none.

## Picks (top 5 per game)

- **Overall: 62/108 (57%)** (voids: 2, pushes: 3)
- Week 4: 31/58 (53%)
- Week 5: 31/50 (62%)
- overs: 25/51 (49%)
- unders: 37/57 (65%)
- Rank 1 picks only: 20/29 (69%)

By stat:

| stat        | hit rate    |
|:------------|:------------|
| carries     | 6/10 (60%)  |
| completions | 5/8 (62%)   |
| pass_yds    | 6/8 (75%)   |
| rec_yds     | 10/19 (53%) |
| receptions  | 21/40 (52%) |
| rush_yds    | 8/10 (80%)  |
| targets     | 6/13 (46%)  |

## Every call, no filters (for comparison)

All over/under calls on players above the usage floor, before the trend gate, signal count and top-5 cut: **151/259 (58%)**. If the picks above beat this, the filters are adding value.

Hit rate by model edge (quartiles): does a bigger edge win more often?

| edge_bin       | hit rate    |
|:---------------|:------------|
| (-0.001, 0.15] | 36/65 (55%) |
| (0.15, 0.195]  | 38/65 (58%) |
| (0.195, 0.266] | 34/64 (53%) |
| (0.266, 0.445] | 43/65 (66%) |

## Does each filter add anything? (lift over a no-information call)

`no-info rate` = how often a call on that side of the baseline would hit with no model at all (yardage stats land under their own average more often than not, so unders start ahead). `lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.

Unfiltered calls overall:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| all   |  259.00 |       0.58 |           0.49 |   0.09 |

Usage trend agrees with the call (the qualification rule):

| usage trend agrees   |   calls |   hit rate |   no-info rate |   lift |
|:---------------------|--------:|-----------:|---------------:|-------:|
| False                |  138.00 |       0.60 |           0.49 |   0.11 |
| True                 |  121.00 |       0.56 |           0.49 |   0.07 |

Number of agreeing signals:

|   n_signals |   calls |   hit rate |   no-info rate |   lift |
|------------:|--------:|-----------:|---------------:|-------:|
|           0 |   20.00 |       0.55 |           0.49 |   0.06 |
|           1 |   74.00 |       0.59 |           0.47 |   0.12 |
|           2 |   90.00 |       0.58 |           0.49 |   0.09 |
|           3 |   61.00 |       0.61 |           0.50 |   0.11 |
|           4 |   12.00 |       0.42 |           0.53 |  -0.12 |
|           5 |    2.00 |       1.00 |           0.62 |   0.38 |

Top-5 picks:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| picks |  108.00 |       0.57 |           0.49 |   0.08 |

## Where the team-total miss comes from

Projected vs actual per team-game for each piece of the scoring model (`corr` near 0 = the model can't tell teams apart on that piece; `sd_projected` far above `sd_actual` x corr = projections spread too wide).

| component     |   projected |   actual |   bias |   mae |   corr |   sd_projected |   sd_actual |
|:--------------|------------:|---------:|-------:|------:|-------:|---------------:|------------:|
| plays         |       60.04 |    60.38 |  -0.34 |  6.50 |   0.13 |           1.77 |        8.14 |
| dropbacks     |       36.90 |    36.93 |  -0.03 |  7.34 |  -0.05 |           3.47 |        8.08 |
| pass_att      |       32.15 |    32.63 |  -0.48 |  7.01 |   0.03 |           3.54 |        7.72 |
| runs          |       23.14 |    23.45 |  -0.31 |  5.16 |   0.14 |           3.45 |        6.07 |
| sacks         |        2.38 |     2.27 |   0.11 |  1.61 |   0.23 |           1.54 |        1.65 |
| interceptions |        0.64 |     0.72 |  -0.08 |  0.72 |   0.17 |           0.36 |        0.87 |
| pass_td       |        1.36 |     1.69 |  -0.32 |  0.96 |   0.02 |           0.38 |        1.11 |
| rush_td       |        0.89 |     0.90 |  -0.01 |  0.76 |   0.09 |           0.37 |        0.94 |
| td            |        2.25 |     2.58 |  -0.33 |  1.05 |   0.25 |           0.52 |        1.34 |
| fga           |        2.23 |     2.06 |   0.17 |  1.22 |   0.15 |           1.11 |        1.28 |
| fgm           |        1.89 |     1.71 |   0.19 |  1.08 |   0.18 |           0.95 |        1.20 |
| points        |       21.27 |    24.25 |  -2.98 |  8.09 |   0.13 |           4.12 |        9.98 |

| part                                           |   share of points-miss variance |
|:-----------------------------------------------|--------------------------------:|
| touchdowns (x6.95)                             |                            0.75 |
| field goals (x3)                               |                          nan    |
| other (defensive / return TDs, 2-pt, safeties) |                          nan    |

Actual drives per team-game: 10.3 (sd 1.3); points per drive 2.39 (sd 1.04). Correlation of the points miss (actual - projected) with drive count: +0.07; with points per drive: +0.84. Red-zone trips per game 3.3, red-zone TD rate 62%.

## Player projections vs a naive season average

Mean absolute error on players who got the ball (lower is better).

| stat        |      n |   model_mae |   naive_mae | model_better   |
|:------------|-------:|------------:|------------:|:---------------|
| carries     | 452.00 |        2.69 |        2.80 | True           |
| completions | 125.00 |        5.15 |        5.89 | True           |
| pass_yds    | 125.00 |       58.75 |       70.82 | True           |
| rec_yds     | 890.00 |       18.77 |       20.38 | True           |
| receptions  | 890.00 |        1.50 |        1.54 | True           |
| rush_yds    | 452.00 |       17.10 |       18.67 | True           |
| targets     | 890.00 |        1.96 |        1.94 | False          |

## Team totals

Mean absolute error in points per team-game (lower is better).

| source                |   MAE |
|:----------------------|------:|
| model (final)         |  8.09 |
| model (before script) |  8.12 |
| market implied total  |  7.12 |
| team's season average |  9.12 |

By week:

|   week |   model |   market |   season_avg |
|-------:|--------:|---------:|-------------:|
|      2 |    8.48 |     6.77 |        11.12 |
|      3 |    9.56 |     8.39 |         9.66 |
|      4 |    7.24 |     6.00 |         7.76 |
|      5 |    6.92 |     7.34 |         7.75 |
