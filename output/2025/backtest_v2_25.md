# Backtest

Weeks 6-18 replayed with only the data available before each week (play-by-play, stats, injury report, depth chart as of that week). Left out because they were gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 produce none.

## Picks (top 5 per game)

- **Overall: 441/741 (60%)** (voids: 48, pushes: 3)
- Week 6: 35/59 (59%)
- Week 7: 29/57 (51%)
- Week 8: 31/51 (61%)
- Week 9: 33/54 (61%)
- Week 10: 29/44 (66%)
- Week 11: 37/65 (57%)
- Week 12: 31/56 (55%)
- Week 13: 45/68 (66%)
- Week 14: 30/56 (54%)
- Week 15: 39/62 (63%)
- Week 16: 40/63 (63%)
- Week 17: 30/54 (56%)
- Week 18: 32/52 (62%)
- overs: 165/323 (51%)
- unders: 276/418 (66%)
- Rank 1 picks only: 116/176 (66%)

By stat:

| stat        | hit rate      |
|:------------|:--------------|
| carries     | 52/84 (62%)   |
| completions | 43/65 (66%)   |
| pass_yds    | 52/87 (60%)   |
| rec_yds     | 61/97 (63%)   |
| receptions  | 83/151 (55%)  |
| rush_yds    | 47/84 (56%)   |
| targets     | 103/173 (60%) |

## Every call, no filters (for comparison)

All over/under calls on players above the usage floor, before the trend gate, signal count and top-5 cut: **1083/1833 (59%)**. If the picks above beat this, the filters are adding value.

Hit rate by model edge (quartiles): does a bigger edge win more often?

| edge_bin        | hit rate      |
|:----------------|:--------------|
| (-0.001, 0.144] | 251/463 (54%) |
| (0.144, 0.201]  | 242/454 (53%) |
| (0.201, 0.29]   | 287/461 (62%) |
| (0.29, 0.611]   | 303/455 (67%) |

## Does each filter add anything? (lift over a no-information call)

`no-info rate` = how often a call on that side of the baseline would hit with no model at all (yardage stats land under their own average more often than not, so unders start ahead). `lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.

Unfiltered calls overall:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| all   | 1833.00 |       0.59 |           0.51 |   0.08 |

Usage trend agrees with the call (the qualification rule):

| usage trend agrees   |   calls |   hit rate |   no-info rate |   lift |
|:---------------------|--------:|-----------:|---------------:|-------:|
| False                | 1007.00 |       0.61 |           0.51 |   0.10 |
| True                 |  826.00 |       0.57 |           0.50 |   0.07 |

Number of agreeing signals:

|   n_signals |   calls |   hit rate |   no-info rate |   lift |
|------------:|--------:|-----------:|---------------:|-------:|
|           0 |  142.00 |       0.54 |           0.48 |   0.05 |
|           1 |  517.00 |       0.57 |           0.50 |   0.08 |
|           2 |  705.00 |       0.60 |           0.51 |   0.10 |
|           3 |  355.00 |       0.59 |           0.52 |   0.07 |
|           4 |  104.00 |       0.66 |           0.54 |   0.12 |
|           5 |   10.00 |       0.70 |           0.53 |   0.17 |

Top-5 picks:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| picks |  741.00 |       0.60 |           0.51 |   0.09 |

## Where the team-total miss comes from

Projected vs actual per team-game for each piece of the scoring model (`corr` near 0 = the model can't tell teams apart on that piece; `sd_projected` far above `sd_actual` x corr = projections spread too wide).

| component     |   projected |   actual |   bias |   mae |   corr |   sd_projected |   sd_actual |
|:--------------|------------:|---------:|-------:|------:|-------:|---------------:|------------:|
| plays         |       60.33 |    60.36 |  -0.03 |  6.88 |   0.13 |           2.32 |        8.77 |
| dropbacks     |       36.53 |    36.01 |   0.52 |  6.43 |   0.27 |           3.77 |        8.29 |
| pass_att      |       32.14 |    31.66 |   0.48 |  5.91 |   0.31 |           3.39 |        7.87 |
| runs          |       23.80 |    24.35 |  -0.55 |  5.91 |   0.20 |           3.77 |        7.22 |
| sacks         |        2.38 |     2.41 |  -0.03 |  1.43 |   0.25 |           0.86 |        1.84 |
| interceptions |        0.70 |     0.71 |  -0.01 |  0.68 |   0.08 |           0.30 |        0.83 |
| pass_td       |        1.52 |     1.46 |   0.05 |  0.97 |   0.15 |           0.34 |        1.19 |
| rush_td       |        0.93 |     0.95 |  -0.02 |  0.81 |   0.13 |           0.35 |        0.98 |
| td            |        2.45 |     2.42 |   0.03 |  1.14 |   0.27 |           0.49 |        1.44 |
| fga           |        2.00 |     1.97 |   0.03 |  1.16 |   0.08 |           0.59 |        1.36 |
| fgm           |        1.70 |     1.70 |  -0.00 |  1.07 |   0.10 |           0.51 |        1.28 |
| points        |       22.15 |    22.81 |  -0.67 |  7.74 |   0.29 |           3.58 |        9.99 |

| part                                           |   share of points-miss variance |
|:-----------------------------------------------|--------------------------------:|
| touchdowns (x6.95)                             |                            0.87 |
| field goals (x3)                               |                            0.07 |
| other (defensive / return TDs, 2-pt, safeties) |                            0.06 |

Actual drives per team-game: 10.1 (sd 1.6); points per drive 2.31 (sd 1.08). Correlation of the points miss (actual - projected) with drive count: +0.04; with points per drive: +0.85. Red-zone trips per game 3.2, red-zone TD rate 55%.

## Player projections vs a naive season average

Mean absolute error on players who got the ball (lower is better).

| stat        |       n |   model_mae |   naive_mae | model_better   |
|:------------|--------:|------------:|------------:|:---------------|
| carries     | 1454.00 |        2.92 |        2.85 | False          |
| completions |  395.00 |        4.82 |        5.22 | True           |
| pass_yds    |  395.00 |       60.21 |       63.18 | True           |
| rec_yds     | 2867.00 |       18.62 |       18.70 | True           |
| receptions  | 2867.00 |        1.41 |        1.38 | False          |
| rush_yds    | 1454.00 |       17.88 |       17.49 | False          |
| targets     | 2867.00 |        1.82 |        1.77 | False          |

## Team totals

Mean absolute error in points per team-game (lower is better).

| source                |   MAE |
|:----------------------|------:|
| model (final)         |  7.74 |
| model (before script) |  7.76 |
| market implied total  |  7.29 |
| team's season average |  7.84 |

By week:

|   week |   model |   market |   season_avg |
|-------:|--------:|---------:|-------------:|
|      6 |    6.59 |     5.98 |         6.92 |
|      7 |    9.34 |     8.02 |         8.08 |
|      8 |   10.66 |     8.90 |         9.41 |
|      9 |    7.20 |     6.75 |         8.61 |
|     10 |    8.56 |     7.88 |         7.86 |
|     11 |    7.28 |     6.90 |         7.67 |
|     12 |    5.55 |     5.80 |         5.81 |
|     13 |    6.89 |     6.00 |         6.28 |
|     14 |    7.47 |     7.98 |         8.55 |
|     15 |    8.71 |     8.11 |         8.48 |
|     16 |    6.49 |     7.16 |         7.18 |
|     17 |    7.74 |     7.55 |         8.76 |
|     18 |    8.42 |     7.86 |         8.46 |
