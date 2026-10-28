# Share lab

## targets

Average miss in targets from share alone (|pred share - actual| x actual team volume):

| estimator | 2025 | 2026 |
|---|---|---|
| season_s | 1.502 | 1.617 |
| last1 | 1.798 | 1.945 |
| last3 | 1.542 | 1.668 |
| ewm1 | 1.532 | 1.682 |
| ewm2 | 1.489 | 1.637 |
| ewm3 | 1.484 | 1.626 |
| ewm4 | 1.485 | 1.622 |
| ewm6 | 1.488 | 1.620 |
| snap_est | 1.513 | 1.699 |
| snap3_est | 1.481 | 1.634 |
| fitted | 1.486 | 1.612 |
| current | 1.506 | 1.635 |
| (player-games) | 4095 | 1058 |
| 25% fitted + 75% current | 1.484 | 1.613 |
| 50% fitted + 50% current | 1.473 | 1.602 |
| 75% fitted + 25% current | 1.474 | 1.601 |

Fitted blend weights (2024): RB: season_s +4.76, last1 +0.13, last3 -0.38, ewm1 -6.03, ewm2 +59.83, ewm3 -189.40, ewm4 +202.56, ewm6 -71.21, snap_est +0.22, snap3_est +0.29; WRTE: season_s +30.14, last1 +0.04, last3 -0.06, ewm1 -4.85, ewm2 +101.62, ewm3 -507.61, ewm4 +716.07, ewm6 -334.79, snap_est +0.25, snap3_est +0.14

## carries

Average miss in carries from share alone (|pred share - actual| x actual team volume):

| estimator | 2025 | 2026 |
|---|---|---|
| season_s | 1.282 | 1.253 |
| last1 | 1.443 | 1.395 |
| last3 | 1.270 | 1.250 |
| ewm1 | 1.257 | 1.219 |
| ewm2 | 1.238 | 1.219 |
| ewm3 | 1.242 | 1.226 |
| ewm4 | 1.248 | 1.231 |
| ewm6 | 1.257 | 1.236 |
| snap_est | 1.337 | 1.274 |
| snap3_est | 1.266 | 1.262 |
| fitted | 1.257 | 1.201 |
| current | 1.203 | 1.205 |
| (player-games) | 3414 | 861 |
| 25% fitted + 75% current | 1.185 | 1.162 |
| 50% fitted + 50% current | 1.190 | 1.149 |
| 75% fitted + 25% current | 1.215 | 1.165 |

Fitted blend weights (2024): QB: const +0.04, season_s +23.82, last1 +0.45, last3 -0.07, ewm1 -12.62, ewm2 +155.53, ewm3 -618.53, ewm4 +772.00, ewm6 -320.38, snap_est +0.10, snap3_est +0.38; RB: const +0.03, season_s +4.85, last1 +0.16, last3 +0.27, ewm1 -0.41, ewm2 +7.52, ewm3 -48.07, ewm4 +78.39, ewm6 -41.90, snap_est +0.23, snap3_est -0.15; WRTE: season_s -55.22, last1 -0.27, last3 +0.02, ewm1 +15.91, ewm2 -300.99, ewm3 +1424.16, ewm4 -1903.18, ewm6 +820.12, snap_est -0.03, snap3_est +0.15
