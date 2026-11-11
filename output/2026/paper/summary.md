# Paper trading ledger

- Bets graded: 87 (voids 0, pushes 0)
- Record: 44-43 (50.6% hit vs 53.5% needed at the average price)
- Units: -6.79 on 129.55 staked → **ROI -5.2%**
- Prices: 0% of bets graded at the real book price recorded at lock; the rest at the assumed price (ROI estimate)
- Average expected value at lock: +27.0%
- Closing-line value: line moved our way on 18% of bets with a closing line (avg +0.08)
- Kalshi check (38 bets with a Kalshi market): hit 52.6% vs 54.1% Kalshi price → ROI at Kalshi prices -2.6%

- Model lean on every posted line: 52.2% right (1160 lines); by stat: carries 55%, completions 46%, pass_yds 41%, rec_yds 53%, receptions 53%, rush_yds 52%

By stat:

| stat        |   bets |   hit |   units |   roi |
|:------------|-------:|------:|--------:|------:|
| carries     |  20.00 |  0.65 |    6.25 |  0.21 |
| completions |  10.00 |  0.50 |   -0.98 | -0.07 |
| pass_yds    |  13.00 |  0.31 |   -8.28 | -0.42 |
| rec_yds     |  12.00 |  0.58 |    1.66 |  0.09 |
| receptions  |  32.00 |  0.47 |   -5.44 | -0.11 |

By week:

|   week |   bets |   hit |   units |
|-------:|-------:|------:|--------:|
|      6 |  20.00 |  0.65 |    6.45 |
|      7 |   5.00 |  0.20 |   -4.70 |
|      8 |  32.00 |  0.47 |   -6.23 |
|      9 |  30.00 |  0.50 |   -2.32 |

Calibration refit on graded bets: a = 0.01, b = 0.01 (update [paper] calib_a / calib_b once there are 150+ bets).