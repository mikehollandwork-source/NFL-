# Team-specific touchdown patterns

3,255 RB/WR/TE games (3+ touches a game so far), live blended TD chance. Miss = scored (1/0) minus the model's chance; summed per team = TDs above or below expected.

## 1. Does a team's miss repeat? (odd weeks vs even weeks)

| season | teams | correlation |
|---|---|---|
| 2025 | 32 | +0.01 |
| 2025 -> 2026 | 32 | +0.41 |

Noise check: with this many games per team, the luck alone in a team's miss is about ±0.070 per player-game.

## 2. Which position scores the team's TDs: does the model's miss by team x position repeat?

| season | team-positions | correlation odd vs even |
|---|---|---|
| 2025 | 31 | -0.16 |

## 3. 2026 so far (weeks 3+): players who scored minus expected, by team and position

Positive = that team's players scored more than the model expected. Single-season numbers like these are mostly luck unless section 1 / 2 show the pattern repeats.

| team | player-games | scored | expected | diff | RB | WR | TE |
|---|---|---|---|---|---|---|---|
| LAC | 22 | 3 | 5.2 | -2.2 | +0.3 | -2.0 | -0.5 |
| HOU | 33 | 6 | 8.0 | -2.0 | -0.8 | -0.0 | -1.2 |
| KAN | 17 | 4 | 6.0 | -2.0 | -0.5 | -1.3 | -0.1 |
| IND | 22 | 5 | 6.9 | -1.9 | -0.6 | -1.4 | +0.0 |
| PHI | 24 | 4 | 5.8 | -1.8 | -0.1 | -1.0 | -0.7 |
| ARI | 26 | 6 | 7.7 | -1.7 | -0.8 | -0.9 | -0.1 |
| BAL | 25 | 6 | 7.6 | -1.6 | -1.0 | -0.3 | -0.2 |
| CAR | 22 | 5 | 6.5 | -1.5 | -0.0 | -2.0 | +0.5 |
| LVR | 26 | 7 | 7.9 | -0.9 | -0.9 | +0.4 | -0.4 |
| TEN | 24 | 5 | 5.8 | -0.8 | -0.7 | +0.4 | -0.5 |
| DET | 23 | 8 | 8.7 | -0.7 | -0.5 | -0.8 | +0.6 |
| CLE | 24 | 5 | 5.7 | -0.7 | -0.1 | -1.5 | +0.8 |
| WAS | 24 | 5 | 5.6 | -0.6 | +0.8 | -1.1 | -0.3 |
| MIN | 15 | 4 | 4.6 | -0.6 | -0.8 | +0.4 | -0.1 |
| SEA | 30 | 8 | 8.3 | -0.3 | +0.7 | -0.3 | -0.8 |
| LAR | 25 | 9 | 9.1 | -0.1 | +1.9 | -0.6 | -1.4 |
| GNB | 28 | 8 | 8.0 | +0.0 | -1.6 | +0.9 | +0.7 |
| TAM | 30 | 7 | 6.9 | +0.1 | +0.7 | +0.3 | -0.9 |
| NOR | 31 | 8 | 7.9 | +0.1 | +0.5 | +0.7 | -1.0 |
| MIA | 17 | 4 | 3.5 | +0.5 | +1.6 | -0.7 | -0.3 |
| NYG | 27 | 8 | 7.5 | +0.5 | +0.4 | +0.0 | +0.1 |
| NYJ | 24 | 7 | 6.1 | +0.9 | -1.3 | +1.5 | +0.7 |
| JAX | 23 | 7 | 5.6 | +1.4 | +1.6 | +0.4 | -0.6 |
| CHI | 28 | 10 | 8.6 | +1.4 | +0.9 | -0.7 | +1.2 |
| DEN | 30 | 8 | 6.5 | +1.5 | +2.0 | +0.2 | -0.7 |
| NWE | 32 | 9 | 7.0 | +2.0 | -0.3 | +1.2 | +1.1 |
| BUF | 21 | 8 | 6.0 | +2.0 | +1.5 | +1.5 | -1.0 |
| DAL | 27 | 11 | 8.9 | +2.1 | +1.8 | +0.5 | -0.1 |
| ATL | 22 | 9 | 6.8 | +2.2 | -0.2 | +0.9 | +1.5 |
| PIT | 27 | 9 | 6.7 | +2.3 | -1.2 | +1.2 | +2.3 |
| CIN | 14 | 8 | 3.3 | +4.7 |  | +2.4 | +2.3 |
| SFO | 22 | 13 | 7.9 | +5.1 | +2.1 | +1.8 | +1.3 |