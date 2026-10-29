# Do offenses pass more or less against certain defenses?

Pass = dropback (pass, sack, scramble). Expected pass chance from down, distance, field position, score and clock (league table, 2024). Garbage time (4th quarter, 17+ points) removed. **Defense pull** = how much more than usual opponents pass against a defense, after removing situation and each offense's own lean. **Raw faced** = plain pass share against the defense (what the model uses now).

## 1. Does it repeat? (odd weeks vs even weeks, same season)

| season | defense pull r | raw pass share faced r | offense lean r | spread of defense pull (sd, pts of pass rate) |
|---|---|---|---|---|
| 2024 | +0.49 | +0.51 | +0.76 | 2.3 |
| 2025 | +0.36 | +0.20 | +0.48 | 2.5 |
| 2026 | -0.09 | -0.13 | +0.49 | 2.4 |

## 2. Does it predict the next game? (as of each week, weeks 4+)

Miss = |actual - predicted| pass-rate residual x plays, i.e. pass attempts per game the situation and the offense's own lean don't explain. Weight b and shrinkage k (plays) fit on 2024 only.

Fitted on 2024: defense pull b = 0.5, k = 0; raw faced b = 0.2, k = 0.

| season | games | offense lean only | + defense pull | + raw faced (now) | correlation of pull with next-game residual |
|---|---|---|---|---|---|
| 2024 (fit) | 448 | 3.362 | 3.298 | 3.326 | +0.142 |
| 2025 | 448 | 3.522 | 3.482 | 3.507 | +0.170 |
| 2026 | 118 | 3.259 | 3.283 | 3.268 | +0.048 |

## 3. 2026 defenses: how much more opponents pass against them than usual

pull and raw in points of pass rate; 'used' = shrunk x b (what a model would apply).

| defense | plays faced | pull | used | raw faced |
|---|---|---|---|---|
| LAC | 356 | -4.5 | -2.2 | -7.7 |
| PHI | 460 | -4.2 | -2.1 | -3.2 |
| MIN | 328 | -3.7 | -1.9 | -1.4 |
| DAL | 410 | -3.0 | -1.5 | -5.2 |
| NYG | 395 | -2.5 | -1.3 | -0.3 |
| LAR | 402 | -2.0 | -1.0 | -3.4 |
| TEN | 440 | -1.7 | -0.8 | -4.2 |
| NYJ | 424 | -1.6 | -0.8 | -5.4 |
| DEN | 457 | -1.4 | -0.7 | +1.5 |
| CAR | 355 | -1.1 | -0.5 | -0.8 |
| SEA | 383 | -0.8 | -0.4 | +1.3 |
| IND | 389 | -0.7 | -0.3 | -1.7 |
| KAN | 368 | -0.6 | -0.3 | +0.1 |
| SFO | 404 | -0.6 | -0.3 | +1.1 |
| GNB | 428 | -0.5 | -0.3 | -2.2 |
| CLE | 431 | -0.0 | -0.0 | +0.7 |
| HOU | 417 | -0.0 | -0.0 | -0.1 |
| MIA | 331 | +0.1 | +0.0 | -4.6 |
| NWE | 362 | +0.4 | +0.2 | +0.2 |
| LVR | 418 | +0.5 | +0.3 | -2.4 |
| ARI | 371 | +0.6 | +0.3 | -2.1 |
| BAL | 407 | +0.7 | +0.3 | +1.3 |
| BUF | 393 | +1.0 | +0.5 | +2.5 |
| CHI | 299 | +1.2 | +0.6 | +2.1 |
| JAX | 319 | +1.7 | +0.9 | +6.0 |
| NOR | 419 | +1.9 | +1.0 | -1.6 |
| CIN | 342 | +2.3 | +1.2 | +4.7 |
| ATL | 402 | +2.4 | +1.2 | +5.1 |
| TAM | 392 | +2.6 | +1.3 | +6.3 |
| PIT | 412 | +3.9 | +1.9 | +3.5 |
| DET | 398 | +4.1 | +2.0 | +7.3 |
| WAS | 375 | +6.5 | +3.2 | +4.8 |
