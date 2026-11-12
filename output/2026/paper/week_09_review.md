# Week 9 review

Record 15-15, -2.32u

## Losses by cause

| Cause | n | Fixable? |
|---|---|---|
| volume | 8 | share model (targets / carries) |
| coin_flip | 4 | no (variance) |
| market | 2 | information the book had |
| efficiency | 1 | no (variance) |

| Player | Prop | Line | Actual | Usage proj → actual | Snap norm → actual | Cause |
|---|---|---|---|---|---|---|
| Braelon Allen | carries over | 9.5 | 8 | 19.8 → 8 | 69% → 59% | volume |
| Omar Cooper Jr. | receptions under | 4.5 | 8 | 4.1 → 11 | 58% → 86% | volume |
| Austin Ekeler | receptions under | 1.5 | 2 | 1.3 → 3 | 20% → 45% | coin_flip |
| Ollie Gordon II | carries over | 16.5 | 16 | 21.4 → 16 | 57% → 72% | coin_flip |
| Rachaad White | carries over | 10.5 | 7 | 13.7 → 7 | 52% → 56% | volume |
| Bo Nix | pass_yds under | 217.5 | 237 | 32.4 → 37 | 100% → 100% | coin_flip |
| Chris Olave | rec_yds under | 75.5 | 98 | 9.4 → 12 | 81% → 85% | market |
| Tyler Shough | completions over | 22.5 | 21 | 38.0 → 35 | 100% → 100% | efficiency |
| J.J. McCarthy | completions over | 18.5 | 12 | 33.4 → 19 | 46% → 76% | volume |
| Marvin Mims Jr. | rec_yds over | 10.5 | 0 | 3.3 → 2 | 24% → 25% | volume |
| Jameson Williams | receptions over | 3.5 | 1 | 6.2 → 2 | 88% → 83% | volume |
| Jordan Love | pass_yds under | 271.5 | 372 | 36.1 → 29 | 100% → 88% | market |
| Sam Roush | receptions under | 1.5 | 2 | 0.6 → 2 | 25% → 52% | coin_flip |
| Baker Mayfield | pass_yds under | 209.5 | 243 | 24.0 → 32 | 97% → 100% | volume |
| D'Andre Swift | carries over | 16.5 | 12 | 20.0 → 12 | 64% → 72% | volume |

Closing line: beat 6, same 20, worse 4 (line only; prices need ODDS_API_KEY)

## Season to date (bets)

| Split | n | Hit | Model said |
|---|---|---|---|
| carries over | 15 | 67% | 68% |
| carries under | 5 | 60% | 83% |
| completions over | 7 | 43% | 62% |
| completions under | 3 | 67% | 68% |
| pass_yds over | 3 | 67% | 65% |
| pass_yds under | 10 | 20% | 68% |
| rec_yds over | 5 | 60% | 60% |
| rec_yds under | 7 | 57% | 68% |
| receptions over | 11 | 45% | 63% |
| receptions under | 21 | 48% | 71% |
| <58% | 7 | 43% | 56% |
| 58-62% | 18 | 50% | 61% |
| 62-66% | 23 | 61% | 64% |
| 66%+ | 39 | 46% | 76% |

## Season to date (every posted line's lean)

| Stat | Side | n | Right |
|---|---|---|---|
| carries | over | 53 | 45% |
| carries | under | 56 | 64% |
| completions | over | 27 | 37% |
| completions | under | 34 | 53% |
| pass_yds | over | 23 | 48% |
| pass_yds | under | 35 | 37% |
| rec_yds | over | 119 | 52% |
| rec_yds | under | 254 | 54% |
| receptions | over | 129 | 50% |
| receptions | under | 247 | 55% |
| rush_yds | over | 64 | 45% |
| rush_yds | under | 119 | 56% |

Change rule: act only on a pattern that holds 3+ weeks (~100 bets) AND passes the 2021-25 backtest.
