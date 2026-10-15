# Backtest

Weeks 6-18 replayed with only the data available before each week (play-by-play, stats, injury report, depth chart as of that week). Left out because they were gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 produce none.

## Picks (top 5 per game)

- **Overall: 418/691 (60%)** (voids: 42, pushes: 5)
- Week 6: 36/58 (62%)
- Week 7: 28/50 (56%)
- Week 8: 33/53 (62%)
- Week 9: 35/54 (65%)
- Week 10: 28/45 (62%)
- Week 11: 37/59 (63%)
- Week 12: 28/52 (54%)
- Week 13: 42/67 (63%)
- Week 14: 22/43 (51%)
- Week 15: 34/54 (63%)
- Week 16: 34/57 (60%)
- Week 17: 31/50 (62%)
- Week 18: 30/49 (61%)
- overs: 155/303 (51%)
- unders: 263/388 (68%)
- Rank 1 picks only: 108/176 (61%)

By stat:

| stat        | hit rate      |
|:------------|:--------------|
| carries     | 53/83 (64%)   |
| completions | 42/63 (67%)   |
| pass_yds    | 42/69 (61%)   |
| rec_yds     | 50/87 (57%)   |
| receptions  | 86/151 (57%)  |
| rush_yds    | 43/69 (62%)   |
| targets     | 102/169 (60%) |

## Every call, no filters (for comparison)

All over/under calls on players above the usage floor, before the trend gate, signal count and top-5 cut: **1093/1834 (60%)**. If the picks above beat this, the filters are adding value.

Hit rate by model edge (quartiles): does a bigger edge win more often?

| edge_bin        | hit rate      |
|:----------------|:--------------|
| (-0.001, 0.128] | 244/460 (53%) |
| (0.128, 0.188]  | 263/465 (57%) |
| (0.188, 0.264]  | 278/451 (62%) |
| (0.264, 0.618]  | 308/458 (67%) |

## Does each filter add anything? (lift over a no-information call)

`no-info rate` = how often a call on that side of the baseline would hit with no model at all (yardage stats land under their own average more often than not, so unders start ahead). `lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.

Unfiltered calls overall:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| all   | 1834.00 |       0.60 |           0.50 |   0.09 |

Usage trend agrees with the call (the qualification rule):

| usage trend agrees   |   calls |   hit rate |   no-info rate |   lift |
|:---------------------|--------:|-----------:|---------------:|-------:|
| False                | 1014.00 |       0.61 |           0.51 |   0.10 |
| True                 |  820.00 |       0.58 |           0.50 |   0.08 |

Number of agreeing signals:

|   n_signals |   calls |   hit rate |   no-info rate |   lift |
|------------:|--------:|-----------:|---------------:|-------:|
|           0 |  206.00 |       0.55 |           0.48 |   0.07 |
|           1 |  580.00 |       0.58 |           0.49 |   0.09 |
|           2 |  652.00 |       0.60 |           0.51 |   0.09 |
|           3 |  297.00 |       0.62 |           0.52 |   0.10 |
|           4 |   89.00 |       0.67 |           0.54 |   0.13 |
|           5 |   10.00 |       0.80 |           0.53 |   0.27 |

Top-5 picks:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| picks |  691.00 |       0.60 |           0.51 |   0.10 |

## Where the team-total miss comes from

Projected vs actual per team-game for each piece of the scoring model (`corr` near 0 = the model can't tell teams apart on that piece; `sd_projected` far above `sd_actual` x corr = projections spread too wide).

| component     |   projected |   actual |   bias |   mae |   corr |   sd_projected |   sd_actual |
|:--------------|------------:|---------:|-------:|------:|-------:|---------------:|------------:|
| plays         |       60.32 |    60.36 |  -0.03 |  6.89 |   0.13 |           2.33 |        8.77 |
| dropbacks     |       36.53 |    36.01 |   0.52 |  6.35 |   0.27 |           3.21 |        8.29 |
| pass_att      |       32.15 |    31.66 |   0.49 |  5.87 |   0.30 |           2.92 |        7.87 |
| runs          |       23.79 |    24.35 |  -0.56 |  5.84 |   0.18 |           3.16 |        7.22 |
| sacks         |        2.38 |     2.41 |  -0.04 |  1.39 |   0.25 |           0.58 |        1.84 |
| interceptions |        0.70 |     0.71 |  -0.01 |  0.68 |   0.07 |           0.30 |        0.83 |
| pass_td       |        1.52 |     1.46 |   0.06 |  0.97 |   0.15 |           0.34 |        1.19 |
| rush_td       |        0.93 |     0.95 |  -0.02 |  0.80 |   0.14 |           0.34 |        0.98 |
| td            |        2.45 |     2.42 |   0.03 |  1.14 |   0.26 |           0.49 |        1.44 |
| fga           |        2.00 |     1.97 |   0.03 |  1.16 |   0.08 |           0.59 |        1.36 |
| fgm           |        1.70 |     1.70 |   0.00 |  1.07 |   0.09 |           0.51 |        1.28 |
| points        |       22.16 |    22.81 |  -0.66 |  7.77 |   0.28 |           3.56 |        9.99 |

| part                                           |   share of points-miss variance |
|:-----------------------------------------------|--------------------------------:|
| touchdowns (x6.95)                             |                            0.87 |
| field goals (x3)                               |                            0.07 |
| other (defensive / return TDs, 2-pt, safeties) |                            0.06 |

Actual drives per team-game: 10.1 (sd 1.6); points per drive 2.31 (sd 1.08). Correlation of the points miss (actual - projected) with drive count: +0.03; with points per drive: +0.86. Red-zone trips per game 3.2, red-zone TD rate 55%.

## Player projections vs a naive season average

Mean absolute error on players who got the ball (lower is better).

| stat        |       n |   model_mae |   naive_mae | model_better   |
|:------------|--------:|------------:|------------:|:---------------|
| carries     | 1454.00 |        2.89 |        2.85 | False          |
| completions |  395.00 |        4.88 |        5.22 | True           |
| pass_yds    |  395.00 |       60.39 |       63.18 | True           |
| rec_yds     | 2867.00 |       18.67 |       18.70 | True           |
| receptions  | 2867.00 |        1.41 |        1.38 | False          |
| rush_yds    | 1454.00 |       17.65 |       17.49 | False          |
| targets     | 2867.00 |        1.82 |        1.77 | False          |

## Team totals

Mean absolute error in points per team-game (lower is better).

| source                |   MAE |
|:----------------------|------:|
| model (final)         |  7.77 |
| model (before script) |  7.73 |
| market implied total  |  7.29 |
| team's season average |  7.84 |

By week:

|   week |   model |   market |   season_avg |
|-------:|--------:|---------:|-------------:|
|      6 |    6.72 |     5.98 |         6.92 |
|      7 |    9.30 |     8.02 |         8.08 |
|      8 |   10.58 |     8.90 |         9.41 |
|      9 |    7.27 |     6.75 |         8.61 |
|     10 |    8.52 |     7.88 |         7.86 |
|     11 |    7.33 |     6.90 |         7.67 |
|     12 |    5.40 |     5.80 |         5.81 |
|     13 |    7.02 |     6.00 |         6.28 |
|     14 |    7.60 |     7.98 |         8.55 |
|     15 |    8.71 |     8.11 |         8.48 |
|     16 |    6.66 |     7.16 |         7.18 |
|     17 |    7.74 |     7.55 |         8.76 |
|     18 |    8.37 |     7.86 |         8.46 |
