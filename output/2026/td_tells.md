# Touchdown tells: week 7 scorers vs non-scorers, then tested on 2025 + 2026

Week 7: 155 RB/WR/TE with 3+ touches a game so far; 46 scored.

| pre-game number | scorers | non-scorers | ratio |
|---|---|---|---|
| model TD chance | 0.30 | 0.24 | 1.23 |
| carries + targets per game | 10.52 | 7.21 | 1.46 |
| red-zone touches per game (inside the 20) | 1.74 | 1.09 | 1.60 |
| touches inside the 10 per game | 0.88 | 0.50 | 1.78 |
| end-zone targets per game | 0.29 | 0.32 | 0.91 |
| TDs per game so far | 0.45 | 0.30 | 1.47 |
| touches per game, last 3 games | 11.18 | 7.43 | 1.51 |
| last-3 touches minus season average | 0.65 | 0.22 | 3.01 |
| red-zone touches last game | 1.91 | 1.28 | 1.50 |
| games since last TD | 1.43 | 2.39 | 0.60 |
| team offensive TDs per game | 2.59 | 2.50 | 1.04 |

## Does each number add anything beyond the model's TD chance?

Logistic regression: scored ~ model TD log-odds + the number (standardized). Coefficient > 0 = players higher on it scored more often than the model expected. |t| >= 2 in both seasons with the same sign = a tell.

| number | 2025 coef | t | 2026 coef | t | verdict |
|---|---|---|---|---|---|
| carries + targets per game | +0.151 | +2.4 | +0.349 | +2.8 | tell |
| red-zone touches per game (inside the 20) | +0.190 | +3.2 | +0.283 | +2.6 | tell |
| touches inside the 10 per game | +0.180 | +3.2 | +0.305 | +3.0 | tell |
| end-zone targets per game | +0.026 | +0.6 | -0.040 | -0.5 | no |
| TDs per game so far | +0.034 | +0.5 | +0.052 | +0.5 | no |
| touches per game, last 3 games | +0.133 | +2.1 | +0.364 | +3.0 | tell |
| last-3 touches minus season average | -0.016 | -0.4 | +0.075 | +1.0 | no |
| red-zone touches last game | +0.131 | +2.7 | +0.123 | +1.4 | maybe (one season) |
| games since last TD | +0.003 | +0.0 | -0.022 | -0.2 | no |
| team offensive TDs per game | +0.059 | +1.2 | +0.080 | +1.0 | no |

## Model TD chance vs actual (both seasons)

| model says | n | scored |
|---|---|---|
| 0%-20% | 1062 | 16% |
| 20%-30% | 1085 | 28% |
| 30%-40% | 640 | 34% |
| 40%-50% | 319 | 40% |
| 50%-60% | 121 | 52% |
| 60%-100% | 28 | 61% |

Samples: 2025 wk 4-18 2470 player-games, 2026 wk 3-7 785.