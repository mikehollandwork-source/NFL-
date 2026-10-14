# Backtest comparison (weeks 2-5)

Market implied totals for reference: MAE 7.02, corr 0.40, sd 3.49. Actual team points sd 9.39.

`lift` = hit rate minus the no-information rate for the same calls (yardage stats land under their own average more often than not). Picks: weeks 4-5 only (3 games needed).

| variant                      |   team total MAE |   corr w/ actual |   MAE wk 4-5 |   spread (sd) |   picks hit |   picks lift |   picks n |   all calls hit |   all calls lift |   calls n |
|:-----------------------------|-----------------:|-----------------:|-------------:|--------------:|------------:|-------------:|----------:|----------------:|-----------------:|----------:|
| A_previous                   |            8.193 |            0.069 |        6.756 |         4.760 |       0.607 |        0.134 |       107 |           0.647 |            0.149 |       255 |
| B_priors                     |            7.776 |            0.162 |        6.641 |         4.629 |       0.611 |        0.137 |       108 |           0.638 |            0.142 |       257 |
| C_player_assume              |            8.159 |            0.073 |        6.792 |         4.750 |       0.605 |        0.130 |       114 |           0.625 |            0.127 |       256 |
| D_player_measured            |            8.215 |            0.072 |        6.830 |         4.767 |       0.625 |        0.150 |       112 |           0.635 |            0.139 |       255 |
| E_all                        |            7.754 |            0.169 |        6.707 |         4.583 |       0.619 |        0.143 |       118 |           0.639 |            0.146 |       255 |
| F_all_plus_streaks_playlevel |            7.724 |            0.177 |        6.645 |         4.592 |       0.614 |        0.131 |       114 |           0.593 |            0.097 |       258 |
| G_final                      |            7.757 |            0.172 |        6.659 |         4.623 |       0.619 |        0.145 |       113 |           0.626 |            0.129 |       257 |
| H_final_no_streak            |            7.825 |            0.158 |        6.747 |         4.609 |       0.628 |        0.148 |       113 |           0.630 |            0.131 |       257 |

## Player projection error by stat (mean absolute error, lower is better)

| stat        |   A_previous |   B_priors |   C_player_assume |   D_player_measured |   E_all |   F_all_plus_streaks_playlevel |   G_final |   H_final_no_streak |   naive season avg |
|:------------|-------------:|-----------:|------------------:|--------------------:|--------:|-------------------------------:|----------:|--------------------:|-------------------:|
| carries     |         2.88 |       2.76 |              2.88 |                2.89 |    2.75 |                           2.79 |      2.75 |                2.75 |               2.88 |
| completions |         5.29 |       5.25 |              5.34 |                5.30 |    5.33 |                           5.33 |      5.27 |                5.25 |               5.51 |
| pass_yds    |        63.67 |      64.25 |             64.13 |               63.78 |   64.66 |                          65.62 |     64.29 |               63.99 |              72.25 |
| rec_yds     |        21.27 |      21.21 |             21.58 |               21.32 |   21.50 |                          21.67 |     21.23 |               21.22 |              22.05 |
| receptions  |         1.60 |       1.59 |              1.62 |                1.60 |    1.62 |                           1.61 |      1.60 |                1.60 |               1.64 |
| rush_yds    |        17.78 |      17.27 |             17.88 |               17.79 |   17.35 |                          17.88 |     17.37 |               17.31 |              18.17 |
| targets     |         2.13 |       2.12 |              2.14 |                2.13 |    2.13 |                           2.12 |      2.13 |                2.12 |               2.05 |
