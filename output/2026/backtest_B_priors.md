# Backtest

Weeks 2-5 replayed with only the data available before each week (play-by-play, stats, injury report, depth chart as of that week). Left out because they were gathered later: the Sharp scheme scrape, the researched defensive personnel file and manual overrides. Week 1 can't be replayed (no prior 2026 games). Picks need 3 games played, so weeks 2-3 produce none.

## Picks (top 5 per game)

- **Overall: 66/108 (61%)** (voids: 6, pushes: 2)
- Week 4: 35/59 (59%)
- Week 5: 31/49 (63%)
- overs: 37/68 (54%)
- unders: 29/40 (72%)
- Rank 1 picks only: 21/29 (72%)

By stat:

| stat        | hit rate    |
|:------------|:------------|
| carries     | 14/18 (78%) |
| completions | 2/4 (50%)   |
| pass_yds    | 8/12 (67%)  |
| rec_yds     | 16/24 (67%) |
| receptions  | 10/19 (53%) |
| rush_yds    | 7/11 (64%)  |
| targets     | 9/20 (45%)  |

## Every call, no filters (for comparison)

All over/under calls on players above the usage floor, before the trend gate, signal count and top-5 cut: **164/257 (64%)**. If the picks above beat this, the filters are adding value.

Hit rate by model edge (quartiles): does a bigger edge win more often?

| edge_bin        | hit rate    |
|:----------------|:------------|
| (-0.001, 0.158] | 40/65 (62%) |
| (0.158, 0.201]  | 40/64 (62%) |
| (0.201, 0.285]  | 37/64 (58%) |
| (0.285, 0.544]  | 47/64 (73%) |

## Does each filter add anything? (lift over a no-information call)

`no-info rate` = how often a call on that side of the baseline would hit with no model at all (yardage stats land under their own average more often than not, so unders start ahead). `lift` = hit rate minus that. Subgroups of 20-130 calls: differences under ~10 points are noise.

Unfiltered calls overall:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| all   |  257.00 |       0.64 |           0.50 |   0.14 |

Usage trend agrees with the call (the qualification rule):

| usage trend agrees   |   calls |   hit rate |   no-info rate |   lift |
|:---------------------|--------:|-----------:|---------------:|-------:|
| False                |  139.00 |       0.66 |           0.51 |   0.15 |
| True                 |  118.00 |       0.61 |           0.48 |   0.13 |

Number of agreeing signals:

|   n_signals |   calls |   hit rate |   no-info rate |   lift |
|------------:|--------:|-----------:|---------------:|-------:|
|           0 |   21.00 |       0.71 |           0.52 |   0.19 |
|           1 |   74.00 |       0.61 |           0.51 |   0.10 |
|           2 |   79.00 |       0.67 |           0.51 |   0.16 |
|           3 |   54.00 |       0.63 |           0.47 |   0.15 |
|           4 |   23.00 |       0.65 |           0.49 |   0.16 |
|           5 |    5.00 |       0.40 |           0.44 |  -0.04 |
|           6 |    1.00 |       0.00 |           0.60 |  -0.60 |

Top-5 picks:

| all   |   calls |   hit rate |   no-info rate |   lift |
|:------|--------:|-----------:|---------------:|-------:|
| picks |  108.00 |       0.61 |           0.48 |   0.13 |

## Where the team-total miss comes from

Projected vs actual per team-game for each piece of the scoring model (`corr` near 0 = the model can't tell teams apart on that piece; `sd_projected` far above `sd_actual` x corr = projections spread too wide).

| component     |   projected |   actual |   bias |   mae |   corr |   sd_projected |   sd_actual |
|:--------------|------------:|---------:|-------:|------:|-------:|---------------:|------------:|
| plays         |       60.22 |    61.52 |  -1.30 |  7.70 |   0.03 |           5.48 |        8.69 |
| dropbacks     |       36.19 |    37.56 |  -1.38 |  7.38 |   0.07 |           4.29 |        8.71 |
| pass_att      |       31.85 |    33.44 |  -1.59 |  7.00 |   0.19 |           4.28 |        8.59 |
| runs          |       24.03 |    23.95 |   0.08 |  5.37 |   0.10 |           4.45 |        5.84 |
| sacks         |        2.26 |     2.26 |   0.00 |  1.55 |   0.02 |           1.29 |        1.54 |
| interceptions |        0.71 |     0.69 |   0.02 |  0.71 |  -0.00 |           0.29 |        0.80 |
| pass_td       |        1.61 |     1.55 |   0.06 |  0.88 |   0.31 |           0.46 |        1.16 |
| rush_td       |        0.97 |     0.93 |   0.05 |  0.91 |  -0.04 |           0.48 |        1.01 |
| td            |        2.58 |     2.48 |   0.11 |  1.10 |   0.24 |           0.64 |        1.41 |
| fga           |        1.91 |     2.10 |  -0.19 |  1.38 |  -0.13 |           1.02 |        1.23 |
| fgm           |        1.62 |     1.79 |  -0.17 |  1.27 |  -0.08 |           0.87 |        1.24 |
| points        |       22.80 |    22.96 |  -0.16 |  7.78 |   0.16 |           4.63 |        9.39 |

| part                                           |   share of points-miss variance |
|:-----------------------------------------------|--------------------------------:|
| touchdowns (x6.95)                             |                            0.86 |
| field goals (x3)                               |                            0.11 |
| other (defensive / return TDs, 2-pt, safeties) |                            0.03 |

Actual drives per team-game: 10.5 (sd 1.6); points per drive 2.23 (sd 0.98). Correlation of the points miss (actual - projected) with drive count: +0.03; with points per drive: +0.81. Red-zone trips per game 3.2, red-zone TD rate 59%.

## Player projections vs a naive season average

Mean absolute error on players who got the ball (lower is better).

| stat        |      n |   model_mae |   naive_mae | model_better   |
|:------------|-------:|------------:|------------:|:---------------|
| carries     | 453.00 |        2.76 |        2.88 | True           |
| completions | 127.00 |        5.25 |        5.51 | True           |
| pass_yds    | 127.00 |       64.25 |       72.25 | True           |
| rec_yds     | 904.00 |       21.21 |       22.05 | True           |
| receptions  | 904.00 |        1.59 |        1.64 | True           |
| rush_yds    | 453.00 |       17.27 |       18.17 | True           |
| targets     | 904.00 |        2.12 |        2.05 | False          |

## Team totals

Mean absolute error in points per team-game (lower is better).

| source                |   MAE |
|:----------------------|------:|
| model (final)         |  7.78 |
| model (before script) |  7.83 |
| market implied total  |  7.02 |
| team's season average |  8.85 |

By week:

|   week |   model |   market |   season_avg |
|-------:|--------:|---------:|-------------:|
|      2 |    9.19 |     8.28 |        12.06 |
|      3 |    8.56 |     7.36 |         8.03 |
|      4 |    5.88 |     5.58 |         7.35 |
|      5 |    7.45 |     6.85 |         7.91 |
