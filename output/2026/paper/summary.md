# Paper trading ledger

- Bets graded: 110 (voids 0, pushes 0)
- Record: 56-54 (50.9% hit vs 53.5% needed at the average price)
- Units: -7.64 on 164.05 staked → **ROI -4.7%**
- Prices: 0% of bets graded at the real book price recorded at lock; the rest at the assumed price (ROI estimate)
- Average expected value at lock: +27.8%
- Closing-line value: line moved our way on 16% of bets with a closing line (avg +0.08)
- Kalshi check (57 bets with a Kalshi market): hit 52.6% vs 54.3% Kalshi price → ROI at Kalshi prices -3.1%

- Model lean on every posted line: 52.3% right (1395 lines); by stat: carries 54%, completions 47%, pass_yds 43%, rec_yds 54%, receptions 53%, rush_yds 53%

By stat:

| stat        |   bets |   hit |   units |   roi |
|:------------|-------:|------:|--------:|------:|
| carries     |  25.00 |  0.64 |    7.16 |  0.19 |
| completions |  11.00 |  0.45 |   -2.48 | -0.15 |
| pass_yds    |  15.00 |  0.33 |   -8.48 | -0.38 |
| rec_yds     |  15.00 |  0.53 |   -0.04 | -0.00 |
| receptions  |  44.00 |  0.50 |   -3.81 | -0.06 |

By week:

|   week |   bets |   hit |   units |
|-------:|-------:|------:|--------:|
|      6 |  20.00 |  0.65 |    6.45 |
|      7 |   5.00 |  0.20 |   -4.70 |
|      8 |  32.00 |  0.47 |   -6.23 |
|      9 |  30.00 |  0.50 |   -2.32 |
|     10 |  23.00 |  0.52 |   -0.85 |

Calibration refit on graded bets: a = -0.19, b = 0.20 (update [paper] calib_a / calib_b once there are 150+ bets).