# Why projections miss (as-of backtests: 2025 weeks 4-18, 2026 weeks 3+)

12,155 player-stat projections. Each miss = team volume + player share + efficiency + did-not-play (parts add up exactly; largest leftover 5.7e-14).

## 1. What drives each stat's misses

Share of the miss from each part (average size of each part / their sum), average miss and bias (actual - projected).

| stat | n | avg miss | bias | team volume | player share | efficiency | didn't play |
|---|---|---|---|---|---|---|---|
| carries | 1218 | 3.9 | -0.81 | 41% | 50% | 0% | 9% |
| completions | 569 | 5.3 | -1.04 | 50% | 10% | 29% | 10% |
| pass_yds | 569 | 64.4 | -8.98 | 41% | 8% | 41% | 9% |
| rec_yds | 2913 | 23.0 | -1.96 | 18% | 37% | 40% | 5% |
| receptions | 2855 | 1.7 | -0.27 | 22% | 45% | 28% | 6% |
| rush_yds | 1341 | 23.3 | -2.89 | 26% | 32% | 37% | 6% |
| targets | 2690 | 2.4 | -0.53 | 31% | 61% | 0% | 8% |

## 2. Team volume misses vs the game going off script

Team pass attempts / carries minus projected, against (final margin - projected margin). The slope is volume per point of surprise; R² is the share of the volume miss that the score explains (not knowable before kickoff).

| | slope per point | R² | bias (actual - proj) | n |
|---|---|---|---|---|
| pass attempts | -0.18 | 9% | +0.33 | 570 |
| carries (team) attempts | +0.30 | 26% | +3.05 | 570 |

## 3. Steady biases (same direction in 2025 and 2026, |t| >= 3, at least 5% of the projection)

Each is a candidate for a fix that must still pass the out-of-sample backtest. Main part = the component carrying most of the bias.

| stat | group | n | projected | bias | bias % | 2025 | 2026 | t | main part | team | share | eff | dnp |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| targets | RB | 506 | 4.1 | -0.85 | -21% | -0.79 | -1.06 | -8.3 | share | +0.01 | -0.66 | +0.00 | -0.20 |
| targets | 1 lead | 570 | 8.2 | -1.13 | -14% | -1.15 | -1.06 | -7.6 | share | +0.04 | -0.86 | +0.00 | -0.31 |
| rec_yds | RB | 526 | 25.3 | -6.18 | -24% | -5.67 | -7.94 | -7.3 | share | +0.16 | -3.85 | -1.19 | -1.30 |
| targets | away | 1321 | 5.3 | -0.55 | -10% | -0.57 | -0.46 | -7.0 | share | +0.04 | -0.36 | +0.00 | -0.23 |
| receptions | 1 lead | 570 | 5.3 | -0.74 | -14% | -0.75 | -0.70 | -6.7 | share | +0.03 | -0.57 | -0.00 | -0.20 |
| targets | RB / 3 depth | 428 | 3.6 | -0.68 | -19% | -0.66 | -0.78 | -6.7 | share | +0.01 | -0.48 | +0.00 | -0.21 |
| receptions | WR | 1563 | 3.6 | -0.37 | -10% | -0.44 | -0.11 | -6.4 | dnp | +0.01 | -0.11 | -0.08 | -0.19 |
| targets | underdog 4+ | 665 | 5.2 | -0.68 | -13% | -0.70 | -0.59 | -6.3 | share | -0.15 | -0.26 | +0.00 | -0.26 |
| targets | RB / close | 259 | 4.2 | -0.91 | -22% | -0.77 | -1.45 | -6.3 | share | +0.10 | -0.81 | +0.00 | -0.20 |
| rec_yds | RB / 3 depth | 448 | 22.3 | -5.43 | -24% | -5.20 | -6.21 | -6.2 | share | +0.16 | -2.68 | -1.50 | -1.41 |
| targets | RB / low total | 179 | 4.1 | -1.04 | -26% | -1.05 | -1.02 | -6.2 | share | -0.01 | -0.80 | +0.00 | -0.23 |
| targets | home | 1369 | 5.2 | -0.51 | -10% | -0.59 | -0.24 | -6.2 | dnp | +0.00 | -0.24 | +0.00 | -0.27 |
| targets | RB / away | 242 | 4.1 | -0.88 | -21% | -0.87 | -0.90 | -6.1 | share | +0.04 | -0.75 | +0.00 | -0.17 |
| targets | close | 1392 | 5.3 | -0.48 | -9% | -0.51 | -0.40 | -6.0 | share | +0.08 | -0.31 | +0.00 | -0.26 |
| targets | low total | 910 | 5.2 | -0.59 | -11% | -0.57 | -0.65 | -6.0 | share | -0.06 | -0.28 | +0.00 | -0.25 |
| targets | weeks 1-9 | 1404 | 5.4 | -0.48 | -9% | -0.58 | -0.35 | -5.9 | share | +0.14 | -0.40 | +0.00 | -0.22 |
| targets | WR / 1 lead | 470 | 8.1 | -0.96 | -12% | -1.05 | -0.64 | -5.8 | share | +0.02 | -0.67 | +0.00 | -0.32 |
| carries | QB | 234 | 5.9 | -1.12 | -19% | -1.12 | -1.10 | -5.8 | share | +0.05 | -0.91 | +0.00 | -0.26 |
| rec_yds | RB / close | 270 | 25.9 | -6.83 | -26% | -5.84 | -10.52 | -5.7 | share | +0.71 | -4.81 | -1.47 | -1.26 |
| targets | mid total | 887 | 5.2 | -0.55 | -11% | -0.63 | -0.25 | -5.7 | share | +0.02 | -0.31 | +0.00 | -0.26 |
| targets | WR | 1522 | 5.7 | -0.46 | -8% | -0.57 | -0.09 | -5.7 | dnp | +0.02 | -0.18 | +0.00 | -0.29 |
| receptions | WR / 1 lead | 470 | 5.3 | -0.68 | -13% | -0.74 | -0.46 | -5.6 | share | +0.02 | -0.43 | -0.08 | -0.20 |
| targets | RB / home | 264 | 4.1 | -0.82 | -20% | -0.71 | -1.19 | -5.6 | share | -0.02 | -0.58 | +0.00 | -0.23 |
| carries | weeks 1-9 | 625 | 10.7 | -1.05 | -10% | -0.94 | -1.21 | -5.6 | dnp | -0.01 | -0.52 | +0.00 | -0.52 |
| rec_yds | RB / away | 257 | 25.4 | -6.25 | -25% | -6.26 | -6.19 | -5.3 | share | +0.22 | -4.16 | -1.16 | -1.15 |
| receptions | away | 1417 | 3.4 | -0.29 | -9% | -0.32 | -0.18 | -5.2 | share | +0.02 | -0.23 | +0.06 | -0.15 |
| rec_yds | RB / low total | 182 | 24.5 | -7.22 | -29% | -7.36 | -6.79 | -5.1 | share | +0.12 | -4.44 | -1.47 | -1.43 |
| rush_yds | QB | 331 | 27.1 | -5.47 | -20% | -5.94 | -3.31 | -5.1 | share | +0.01 | -3.06 | -1.17 | -1.25 |
| carries | QB / away | 118 | 6.0 | -1.36 | -23% | -1.30 | -1.64 | -5.1 | share | -0.09 | -0.97 | +0.00 | -0.30 |
| rec_yds | RB / home | 269 | 25.2 | -6.12 | -24% | -5.09 | -9.41 | -5.0 | share | +0.10 | -3.56 | -1.22 | -1.44 |
