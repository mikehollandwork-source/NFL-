# Week 8 review

Record 15-17, -6.23u

## Losses by cause

| Cause | n | Fixable? |
|---|---|---|
| coin_flip | 9 | no (variance) |
| efficiency | 6 | no (variance) |
| volume | 2 | share model (targets / carries) |

| Player | Prop | Line | Actual | Usage proj → actual | Snap norm → actual | Cause |
|---|---|---|---|---|---|---|
| Garrett Wilson | receptions under | 5.5 | 6 | 6.1 → 12 | 90% → 81% | coin_flip |
| Khalil Shakir | receptions under | 4.5 | 5 | 5.6 → 6 | 63% → 67% | coin_flip |
| Bijan Robinson | carries over | 19.5 | 19 | 23.5 → 19 | 71% → 81% | coin_flip |
| Cam Ward | pass_yds under | 191.5 | 304 | 30.9 → 40 | 100% → 100% | efficiency |
| Derrick Henry | receptions under | 1.5 | 2 | 1.9 → 2 | 57% → 45% | coin_flip |
| Ashton Dulin | rec_yds over | 0.5 | 0 | 2.0 → 0 | 19% → 31% | volume |
| Darnell Washington | receptions under | 2.5 | 3 | 3.6 → 5 | 65% → 63% | coin_flip |
| Kirk Cousins | completions over | 20.5 | 19 | 36.6 → 26 | 98% → 100% | efficiency |
| Kee– Allen | receptions under | 4.5 | 7 | 6.7 → 7 | 59% → 52% | efficiency |
| Jared Goff | pass_yds over | 259.5 | 176 | 34.8 → 25 | 99% → 100% | efficiency |
| Caleb Douglas | receptions under | 3.5 | 4 | 3.9 → 6 | 82% → 86% | coin_flip |
| DeMario Douglas | receptions over | 3.5 | 3 | 7.2 → 3 | 55% → 65% | coin_flip |
| Kyle Williams | rec_yds under | 23.5 | 43 | 2.5 → 1 | 30% → 83% | efficiency |
| Jaylen Waddle | receptions over | 3.5 | 3 | 7.8 → 6 | 66% → 45% | coin_flip |
| Patrick Mahomes | pass_yds under | 223.5 | 321 | 35.3 → 41 | 100% → 100% | efficiency |
| Xavier Worthy | receptions over | 3.5 | 3 | 6.9 → 6 | 82% → 94% | coin_flip |
| Saquon Barkley | carries under | 11.5 | 13 | 6.4 → 13 | 36% → 32% | volume |

Closing line: beat 7, same 21, worse 4 (line only; prices need ODDS_API_KEY)

## Season to date (bets)

| Split | n | Hit | Model said |
|---|---|---|---|
| carries over | 10 | 90% | 66% |
| carries under | 4 | 50% | 79% |
| completions over | 4 | 50% | 62% |
| completions under | 3 | 67% | 68% |
| pass_yds over | 2 | 50% | 60% |
| pass_yds under | 7 | 29% | 67% |
| rec_yds over | 3 | 67% | 62% |
| rec_yds under | 4 | 50% | 70% |
| receptions over | 8 | 38% | 63% |
| receptions under | 12 | 33% | 68% |
| <58% | 4 | 75% | 57% |
| 58-62% | 14 | 43% | 60% |
| 62-66% | 17 | 53% | 64% |
| 66%+ | 22 | 50% | 74% |

## Season to date (every posted line's lean)

| Stat | Side | n | Right |
|---|---|---|---|
| carries | over | 39 | 54% |
| carries | under | 38 | 68% |
| completions | over | 19 | 42% |
| completions | under | 24 | 58% |
| pass_yds | over | 15 | 53% |
| pass_yds | under | 26 | 42% |
| rec_yds | over | 87 | 52% |
| rec_yds | under | 173 | 57% |
| receptions | over | 90 | 46% |
| receptions | under | 170 | 55% |
| rush_yds | over | 53 | 49% |
| rush_yds | under | 81 | 57% |

Change rule: act only on a pattern that holds 3+ weeks (~100 bets) AND passes the 2021-25 backtest.
