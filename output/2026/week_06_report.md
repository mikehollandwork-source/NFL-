# Week 6 projections

## Choices used for this projection
- Negative play = `custom`
- Recency half-life = 4.0 weeks
- Adaptation mode = `measured` → applied strength +0.07
- Adaptation test: beta +0.12, t +1.2, n 923 bucket-games — **not clearly supported: last game's results barely change next game's calls**
- Defense weight = 0.75, shrink = 40 plays, labels = `both`

## Availability flags

- The week 6 injury report isn't out yet (posts Wed-Fri); players Out last week who also missed last week's game are carried as out. Re-run after it posts.
- BAL: depth chart lists Lamar Jackson as QB1 but he is listed out; projecting Tyler Huntley. Check the week 6 report.
- CHI: depth chart lists Caleb Williams as QB1 but he hasn't played in the team's last two games; projecting Tyson Bagent. Check the week 6 report.
- TAM: depth chart lists Baker Mayfield as QB1 but he is listed out; projecting Jalon Daniels. Check the week 6 report.

## Teams falling short of their implied team totals

Points scored minus the betting market's implied team total, per game. The shrunk `correction` is added to this week's implied total before blending.

| team   |   games |   implied_avg |   scored_avg |   avg_miss |   under_rate |   correction |
|:-------|--------:|--------------:|-------------:|-----------:|-------------:|-------------:|
| LAC    |       5 |         22.40 |        16.80 |      -5.60 |         0.80 |        -2.55 |
| TEN    |       5 |         17.05 |        11.60 |      -5.45 |         0.60 |        -2.48 |
| MIA    |       5 |         17.10 |        14.00 |      -3.10 |         0.80 |        -1.41 |
| PHI    |       5 |         21.50 |        18.40 |      -3.10 |         0.40 |        -1.41 |
| DEN    |       5 |         22.45 |        19.40 |      -3.05 |         0.60 |        -1.39 |
| GNB    |       5 |         22.75 |        20.80 |      -1.95 |         0.80 |        -0.89 |

## DEN vs SEA
Projected 56 plays, 61% dropbacks, 31.7 pass att, 21.8 runs, 1.2 sacks. QB: Bo Nix
**Coaching style:** Deep-pass share low: 12% (league 19%); 3rd-down deep share low: 14% (league 21%); 4th-down go rate low: 8% (league 19%); Sack rate low: 3% (league 6%); Pass rate on 2nd & short low: 0% (league 31%); EPA/dropback low: -0.08 (league +0.06); Favors run middle (35%).
**Market:** implied team total 19.0 (spread -2.5); has scored -3.0 pts/game vs its implied totals over 5 games (fell short in 60%), correction -1.4. Model 19.1 → blended 18.2: TD rates x0.95, yards x0.99, dropback rate +1.0%.
**Strength of schedule:** own pass yds x1.03, own run yds x1.04, own scoring x1.05 (raw stats re-rated against the opponents actually faced).
**Out:** Pat Surtain II (carried from week 5 report: Out (Ankle)), Riley Moss (carried from week 5 report: Out (Ribs)).
**Coach angle:** HC Sean Payton (veteran HC, 20 prior seasons); plays called by OC Davis Webb (first-time play-caller, 0 seasons calling); no prior play-calling seasons: this season's data only; this season top target share 22%.
**SEA defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: two_high [online (high)].
- Best matchups: run_outside_right (x1.06), run_inside_right (x1.05); worst: pass_short_middle (x0.85).
- SEA blitzes 21% of dropbacks (league 31%, FTN charting); DEN gains x0.76 as much per dropback vs the blitz as other offenses (57 blitzed dropbacks) -> pass yards x1.03
- DEN deep plays vs zone heavy coverage defenses: x0.95 vs how other offenses fare (7 plays)
- DEN deep plays vs two high shell defenses: x1.08 vs how other offenses fare (13 plays)

| player           | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-----------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Bo Nix           | QB    |     161.58 |      1.42 |            0.96 |      2.78 |      14.37 |      0.00 |         0.00 |      0.00 |         0.07 |
| J.K. Dobbins     | RB    |       0.00 |      0.00 |            0.00 |     14.51 |      56.79 |      1.43 |         1.00 |      7.80 |         0.33 |
| Jaylen Waddle    | WR    |       0.00 |      0.00 |            0.00 |      0.41 |       1.87 |      6.31 |         4.01 |     35.89 |         0.27 |
| RJ Harvey        | RB    |       0.00 |      0.00 |            0.00 |      3.16 |      12.85 |      4.62 |         3.32 |     25.25 |         0.23 |
| Courtland Sutton | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.51 |         2.67 |     25.78 |         0.21 |
| Evan Engram      | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.24 |         2.07 |     18.63 |         0.17 |
| Pat Bryant       | WR    |       0.00 |      0.00 |            0.00 |      0.14 |       0.57 |      2.08 |         1.37 |     12.92 |         0.12 |
| Tyler Badie      | RB    |       0.00 |      0.00 |            0.00 |      1.00 |       4.00 |      1.52 |         1.08 |      9.31 |         0.09 |

**DEN kicker**

| player   |   fg_made |   xp_made |   kicking_points |
|:---------|----------:|----------:|-----------------:|
| Wil Lutz |      1.71 |      1.87 |             7.00 |

**DEN defenders (vs SEA offense)**

| player          |   tackles |   sacks |   def_int |
|:----------------|----------:|--------:|----------:|
| Alex Singleton  |     10.09 |    0.00 |      0.00 |
| Brandon Jones   |      6.95 |    0.00 |      0.46 |
| Justin Strnad   |      5.66 |    0.00 |      0.00 |
| Talanoa Hufanga |      4.24 |    0.20 |      0.42 |
| Que Robinson    |      3.85 |    0.17 |      0.00 |
| Pat Surtain II  |      3.83 |    0.00 |      0.00 |
| Zach Allen      |      3.21 |    0.75 |      0.00 |
| Malcolm Roach   |      3.18 |    0.17 |      0.00 |

## SEA vs DEN
Projected 61 plays, 53% dropbacks, 29.1 pass att, 28.6 runs, 2.8 sacks. QB: Sam Darnold
**Coaching style:** Neutral-script pass rate low: 55% (league 59%); Early-down pass rate low: 47% (league 53%); Sack rate high: 8% (league 6%); Shotgun rate low: 47% (league 61%); No-huddle rate low: 1% (league 6%); 3rd-down conversion low: 29% (league 42%); EPA/run low: -0.29 (league -0.09).
**Market:** implied team total 21.5 (spread +2.5); has scored +2.9 pts/game vs its implied totals over 5 games (fell short in 20%), correction +1.3. Model 24.5 → blended 23.5: TD rates x0.96, yards x0.99, dropback rate -1.0%.
**Strength of schedule:** opp pass D x0.96, opp run D x0.98 (raw stats re-rated against the opponents actually faced).
**Out:** Chazz Surratt (carried from week 5 report: Out (Calf)), Zach Charbonnet (carried from week 5 report: Out (Knee)), Julian Neal (carried from week 5 report: Out (Hamstring)).
**Coach angle:** HC Mike Macdonald (young HC, 2 prior seasons); plays called by OC Brian Fleury (first-time play-caller, 0 seasons calling); no prior play-calling seasons: this season's data only; this season top target share 34%.
**DEN defensive scheme (online/tagged):** blitz: heavy, coverage: avg, shell: two_high [online (high)].
- DEN brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed -1.10 on 7 attempts. SEA 3rd-down deep share 19%.
- Best matchups: pass_short_left (x1.21), run_middle (x1.07); worst: pass_deep_left (x0.82).
- SEA short plays vs two high shell defenses: x1.11 vs how other offenses fare (86 plays)

| player             | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Sam Darnold        | QB    |     217.96 |      1.64 |            1.08 |      0.85 |       6.53 |      0.00 |         0.00 |      0.00 |         0.00 |
| Jaxon Smith-Njigba | WR    |       0.00 |      0.00 |            0.00 |      0.33 |       1.41 |      9.89 |         6.27 |     84.40 |         0.56 |
| Emanuel Wilson     | RB    |       0.00 |      0.00 |            0.00 |     20.70 |      80.96 |      1.71 |         1.10 |     12.23 |         0.49 |
| George Holani      | RB    |       0.00 |      0.00 |            0.00 |      6.67 |      26.52 |      2.70 |         1.85 |     20.09 |         0.27 |
| AJ Barner          | TE    |       0.00 |      0.00 |            0.00 |      0.20 |       0.73 |      4.50 |         2.78 |     31.76 |         0.19 |
| Rashid Shaheed     | WR    |       0.00 |      0.00 |            0.00 |      0.61 |       2.88 |      3.75 |         2.26 |     28.80 |         0.14 |
| Cooper Kupp        | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.10 |         1.96 |     23.21 |         0.15 |

**SEA kicker**

| player      |   fg_made |   xp_made |   kicking_points |
|:------------|----------:|----------:|-----------------:|
| Jason Myers |      2.04 |      2.32 |             8.45 |

**SEA defenders (vs DEN offense)**

| player            |   tackles |   sacks |   def_int |
|:------------------|----------:|--------:|----------:|
| Ernest Jones      |      8.72 |    0.22 |      0.17 |
| Drake Thomas      |      5.91 |    0.06 |      0.17 |
| Devon Witherspoon |      5.57 |    0.00 |      0.00 |
| Julian Love       |      3.60 |    0.00 |      0.23 |
| Josh Jobe         |      3.50 |    0.00 |      0.10 |
| Byron Murphy II   |      3.36 |    0.33 |      0.00 |
| Nick Emmanwori    |      3.25 |    0.10 |      0.00 |
| Uchenna Nwosu     |      2.72 |    0.10 |      0.00 |

## JAX vs HOU
Projected 58 plays, 59% dropbacks, 30.5 pass att, 23.8 runs, 2.5 sacks. QB: Trevor Lawrence
**Coaching style:** Deep-pass share low: 15% (league 19%); Red-zone pass rate high: 61% (league 53%); Pass rate on 2nd & short high: 47% (league 31%); EPA/dropback high: +0.26 (league +0.06); EPA/run high: -0.02 (league -0.09).
**Market:** implied team total 22.8 (spread +3.0); has scored +0.7 pts/game vs its implied totals over 5 games (fell short in 60%), correction +0.3. Model 20.0 → blended 21.8: TD rates x1.09, yards x1.03, dropback rate -1.2%.
**Strength of schedule:** own pass yds x1.03, own scoring x1.03 (raw stats re-rated against the opponents actually faced).
**Out:** Eric Murray (carried from week 5 report: Doubtful (Concussion)), Jaylon Jones (carried from week 5 report: Out (Hamstring)).
**Coach angle:** HC Liam Coen (young HC, 1 prior seasons); calls own plays (developing play-caller, 2 seasons calling); career balanced (+1.1 pts pass rate vs league, 2 seasons); spreads it around; this season top target share 24%.
**HOU defensive scheme (online/tagged):** blitz: light, coverage: zone_heavy [online (high)].
- HOU is soft deep (+0.95 EPA/deep att vs league +0.43); JAX throws deep 15%.
- Best matchups: pass_deep_middle (x1.12), pass_deep_right (x1.11); worst: run_outside_left (x0.84).
- Last game — worked: run_middle; failed: run_outside_left, run_outside_right.
- HOU blitzes 21% of dropbacks (league 31%, FTN charting); JAX gains x0.86 as much per dropback vs the blitz as other offenses (47 blitzed dropbacks) -> pass yards x1.02
- JAX short plays vs zone heavy coverage defenses: x1.08 vs how other offenses fare (40 plays)
- JAX run plays vs zone heavy coverage defenses: x0.92 vs how other offenses fare (24 plays)
- JAX deep-throw rate vs zone heavy coverage: x0.83

| player              | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:--------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Trevor Lawrence     | QB    |     241.18 |      1.42 |            0.52 |      2.26 |      13.55 |      0.00 |         0.00 |      0.00 |         0.04 |
| Bhayshul Tuten      | RB    |       0.00 |      0.00 |            0.00 |     15.55 |      59.78 |      2.41 |         1.68 |     18.89 |         0.43 |
| Parker Washington   | WR    |       0.00 |      0.00 |            0.00 |      0.20 |       0.74 |      6.55 |         4.20 |     56.60 |         0.33 |
| Brenton Strange     | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.26 |         4.35 |     52.43 |         0.21 |
| Jakobi Meyers       | WR    |       0.00 |      0.00 |            0.00 |      0.12 |       0.45 |      3.68 |         2.44 |     30.18 |         0.19 |
| Brian Thomas Jr.    | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.39 |         2.12 |     26.39 |         0.14 |
| Josh Cameron        | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.04 |         1.98 |     24.64 |         0.15 |
| Chris Rodriguez Jr. | RB    |       0.00 |      0.00 |            0.00 |      5.84 |      22.05 |      0.34 |         0.24 |      2.61 |         0.28 |

**JAX kicker**

| player     |   fg_made |   xp_made |   kicking_points |
|:-----------|----------:|----------:|-----------------:|
| Cam Little |      2.44 |      2.16 |             9.46 |

**JAX defenders (vs HOU offense)**

| player           |   tackles |   sacks |   def_int |
|:-----------------|----------:|--------:|----------:|
| Foyesade Oluokun |      8.09 |    0.00 |      0.18 |
| Ventrell Miller  |      6.82 |    0.17 |      0.00 |
| Antonio Johnson  |      5.34 |    0.16 |      0.00 |
| Travis Hunter    |      4.67 |    0.00 |      0.09 |
| Josh Hines-Allen |      4.17 |    0.24 |      0.00 |
| Jarrian Jones    |      4.01 |    0.00 |      0.10 |
| Rayuan Lane III  |      3.83 |    0.00 |      0.00 |
| Jourdan Lewis    |      3.70 |    0.00 |      0.19 |

## HOU vs JAX
Projected 61 plays, 68% dropbacks, 37.5 pass att, 19.6 runs, 2.1 sacks. QB: C.J. Stroud
**Coaching style:** Early-down pass rate high: 58% (league 53%); Deep-pass share high: 23% (league 19%); Pass rate on 2nd & short high: 60% (league 31%); EPA/dropback high: +0.17 (league +0.06); EPA/run low: -0.20 (league -0.09); Favors run inside right (35%).
**Market:** implied team total 19.8 (spread -3.0); has scored -1.0 pts/game vs its implied totals over 5 games (fell short in 40%), correction -0.5. Model 15.8 → blended 17.9: TD rates x1.13, yards x1.04, dropback rate +1.2%.
**Strength of schedule:** own pass yds x0.95, own scoring x0.95, opp pass D x1.03, opp run D x1.02, opp scoring D x1.02 (raw stats re-rated against the opponents actually faced).
**Out:** Tank Dell (carried from week 5 report: Out (Knee)).
**Coach angle:** HC DeMeco Ryans (young HC, 3 prior seasons); plays called by OC Nick Caley (developing play-caller, 1 seasons calling); career balanced (+1.8 pts pass rate vs league, 1 seasons); typical; this season top target share 18%.
**JAX defensive scheme (online/tagged):** blitz: avg, coverage: avg, shell: two_high [online (high)].
- Best matchups: pass_short_left (x1.22), pass_short_right (x1.19); worst: pass_deep_left (x0.92).
- JAX blitzes 31% of dropbacks (league 31%, FTN charting); HOU gains x1.34 as much per dropback vs the blitz as other offenses (42 blitzed dropbacks) -> pass yards x1.00
- HOU deep plays vs two high shell defenses: x0.87 vs how other offenses fare (14 plays)
- HOU short plays vs two high shell defenses: x1.14 vs how other offenses fare (63 plays)
- HOU run plays vs two high shell defenses: x1.08 vs how other offenses fare (53 plays)

| player            | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| C.J. Stroud       | QB    |     296.46 |      1.07 |            0.55 |      2.62 |      15.20 |      0.00 |         0.00 |      0.00 |         0.07 |
| Xavier Hutchinson | WR    |       0.00 |      0.00 |            0.00 |      0.27 |       1.03 |      6.83 |         4.30 |     59.49 |         0.14 |
| Dalton Schultz    | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.93 |         4.18 |     52.48 |         0.12 |
| Woody Marks       | RB    |       0.00 |      0.00 |            0.00 |      7.92 |      30.12 |      2.97 |         2.09 |     22.15 |         0.37 |
| Nico Collins      | WR    |       0.00 |      0.00 |            0.00 |      0.10 |       0.39 |      5.25 |         3.50 |     45.90 |         0.23 |
| David Montgomery  | RB    |       0.00 |      0.00 |            0.00 |      9.34 |      32.98 |      1.20 |         0.85 |      9.67 |         0.37 |
| Jaylin Noel       | WR    |       0.00 |      0.00 |            0.00 |      0.68 |       2.83 |      3.77 |         2.54 |     32.43 |         0.15 |
| Kayshon Boutte    | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.90 |         2.48 |     31.99 |         0.10 |
| Foster Moreau     | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.59 |         1.76 |     19.82 |         0.09 |
| Jared Wayne       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.10 |         1.25 |     17.33 |         0.07 |

**HOU kicker**

| player           |   fg_made |   xp_made |   kicking_points |
|:-----------------|----------:|----------:|-----------------:|
| Ka'imi Fairbairn |      1.92 |      1.89 |             7.66 |

**HOU defenders (vs JAX offense)**

| player            |   tackles |   sacks |   def_int |
|:------------------|----------:|--------:|----------:|
| Azeez Al-Shaair   |      8.62 |    0.00 |      0.00 |
| Reed Blankenship  |      8.61 |    0.00 |      0.21 |
| Jake Hansen       |      7.28 |    0.16 |      0.31 |
| Kamari Lassiter   |      6.24 |    0.00 |      0.00 |
| Tommy Togiai      |      6.09 |    0.00 |      0.00 |
| Will Anderson Jr. |      5.64 |    1.15 |      0.00 |
| Jalen Pitre       |      4.96 |    0.00 |      0.00 |
| Calen Bullock     |      4.26 |    0.00 |      0.00 |

## ATL vs CHI
Projected 53 plays, 55% dropbacks, 25.7 pass att, 23.6 runs, 2.5 sacks. QB: Michael Penix Jr.
**Coaching style:** Neutral-script pass rate low: 48% (league 59%); Early-down pass rate low: 39% (league 53%); 3rd-down deep share high: 27% (league 21%); Red-zone pass rate low: 36% (league 53%); 4th-down go rate low: 9% (league 19%); Shotgun rate low: 48% (league 61%); Pass rate on 2nd & short low: 13% (league 31%); Red-zone run share high: 68% (league 46%); EPA/dropback low: -0.02 (league +0.06); EPA/run high: +0.06 (league -0.09); Favors run inside left (38%).
**Market:** implied team total 23.2 (spread -3.0); has scored +3.0 pts/game vs its implied totals over 5 games (fell short in 60%), correction +1.4. Model 21.1 → blended 23.2: TD rates x1.10, yards x1.03, dropback rate +1.2%.
**Strength of schedule:** own scoring x0.97 (raw stats re-rated against the opponents actually faced).
**Out:** Yasir Abdullah (carried from week 5 report: Out (Hamstring)).
**Coach angle:** HC Kevin Stefanski (new to team, 6 prior seasons); plays called by OC Tommy Rees (developing play-caller, 1 seasons calling); career balanced (+1.5 pts pass rate vs league, 1 seasons); spreads it around; this season top target share 32%.
**CHI defensive scheme (online/tagged):** blitz: heavy, coverage: man_heavy [online (high)].
- CHI is soft deep (+1.54 EPA/deep att vs league +0.43); ATL throws deep 20%.
- CHI brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed +0.59 on 5 attempts. ATL 3rd-down deep share 27%.
- CHI run defense is soft (+0.05 EPA/run).
- Best matchups: pass_deep_right (x1.23), pass_deep_middle (x1.20); worst: pass_short_left (x0.99).
- Last game — worked: pass_deep_right, run_inside_right; failed: none.
- CHI blitzes 39% of dropbacks (league 31%, FTN charting); ATL gains x1.38 as much per dropback vs the blitz as other offenses (49 blitzed dropbacks) -> pass yards x1.03

| player            | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Michael Penix Jr. | QB    |     207.16 |      1.23 |            0.85 |      0.93 |       7.22 |      0.00 |         0.00 |      0.00 |         0.00 |
| Bijan Robinson    | RB    |       0.00 |      0.00 |            0.00 |     16.04 |      81.39 |      5.18 |         3.32 |     37.67 |         0.68 |
| Drake London      | WR    |       0.00 |      0.00 |            0.00 |      0.22 |       1.26 |      7.09 |         4.50 |     68.55 |         0.21 |
| Brian Robinson    | RB    |       0.00 |      0.00 |            0.00 |      7.26 |      33.49 |      0.70 |         0.43 |      4.83 |         0.38 |
| Kyle Pitts        | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.58 |         2.31 |     29.29 |         0.18 |
| Jahan Dotson      | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.20 |         1.85 |     30.81 |         0.20 |
| Zachariah Branch  | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.66 |         1.08 |     12.51 |         0.07 |

**ATL kicker**

| player    |   fg_made |   xp_made |   kicking_points |
|:----------|----------:|----------:|-----------------:|
| Nick Folk |      1.73 |      2.40 |             7.60 |

**ATL defenders (vs CHI offense)**

| player             |   tackles |   sacks |   def_int |
|:-------------------|----------:|--------:|----------:|
| Xavier Watts       |     10.74 |    0.10 |      0.37 |
| Divine Deablo      |      8.31 |    0.00 |      0.00 |
| C.J. Henderson     |      7.64 |    0.00 |      0.00 |
| Mike Hughes        |      7.60 |    0.00 |      0.00 |
| Kendal Daniels     |      6.94 |    0.23 |      0.00 |
| Jessie Bates       |      6.53 |    0.00 |      0.00 |
| Harold Perkins Jr. |      6.23 |    0.10 |      0.00 |
| Sydney Brown       |      5.11 |    0.00 |      0.00 |

## CHI vs ATL
Projected 75 plays, 55% dropbacks, 36.5 pass att, 33.4 runs, 2.0 sacks. QB: Tyson Bagent
**Coaching style:** 3rd-down deep share low: 14% (league 21%); Red-zone pass rate low: 42% (league 53%); 4th-down go rate high: 42% (league 19%); Shotgun rate low: 53% (league 61%); Pass rate on 2nd & short high: 44% (league 31%); Red-zone run share high: 56% (league 46%); 3rd-down conversion high: 48% (league 42%); EPA/run high: -0.03 (league -0.09); Favors run inside right (45%).
**Market:** implied team total 26.2 (spread +3.0); has scored +0.2 pts/game vs its implied totals over 5 games (fell short in 60%), correction +0.1. Model 23.2 → blended 25.1: TD rates x1.08, yards x1.02, dropback rate -1.2%.
**Strength of schedule:** own pass yds x1.05, own scoring x1.03, opp pass D x0.98, opp scoring D x0.98 (raw stats re-rated against the opponents actually faced).
**Out:** Kyle Monangai (carried from week 5 report: Out (Thumb)), Keyshaun Elliott (carried from week 5 report: Out (Quadricep)).
**Coach angle:** HC Ben Johnson (young HC, 1 prior seasons); calls own plays (developing play-caller, 4 seasons calling); career balanced (-0.8 pts pass rate vs league, 4 seasons); typical; this season top target share 23%.
**ATL defensive scheme (online/tagged):** blitz: avg, coverage: avg, shell: single_high [online (high)].
- Best matchups: run_middle (x1.19), pass_deep_middle (x1.05); worst: pass_short_right (x0.92).
- ATL blitzes 30% of dropbacks (league 31%, FTN charting); CHI gains x1.16 as much per dropback vs the blitz as other offenses (79 blitzed dropbacks) -> pass yards x1.00

| player            | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Tyson Bagent      | QB    |     245.59 |      1.50 |            0.37 |      3.39 |      24.88 |      0.00 |         0.00 |      0.00 |         0.01 |
| D'Andre Swift     | RB    |       0.00 |      0.00 |            0.00 |     24.99 |     110.65 |      3.97 |         2.85 |     26.52 |         0.72 |
| Luther Burden III | WR    |       0.00 |      0.00 |            0.00 |      2.16 |       9.56 |      8.32 |         5.31 |     60.85 |         0.36 |
| Kalif Raymond     | WR    |       0.00 |      0.00 |            0.00 |      0.42 |       1.78 |      6.09 |         4.36 |     42.60 |         0.27 |
| Rome Odunze       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.92 |         3.75 |     46.14 |         0.20 |
| Colston Loveland  | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.95 |         3.85 |     41.02 |         0.20 |
| Cole Kmet         | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.17 |         1.43 |     15.08 |         0.13 |
| Roschon Johnson   | RB    |       0.00 |      0.00 |            0.00 |      4.76 |      19.12 |      0.30 |         0.20 |      1.85 |         0.16 |

**CHI kicker**

| player       |   fg_made |   xp_made |   kicking_points |
|:-------------|----------:|----------:|-----------------:|
| Cairo Santos |      1.64 |      2.76 |             7.67 |

**CHI defenders (vs ATL offense)**

| player            |   tackles |   sacks |   def_int |
|:------------------|----------:|--------:|----------:|
| Dillon Thieneman  |      8.83 |    0.00 |      0.31 |
| Devin Bush        |      6.82 |    0.24 |      0.00 |
| Cam Lewis         |      4.38 |    0.00 |      0.00 |
| Tyrique Stevenson |      4.31 |    0.00 |      0.00 |
| Malik Muhammad    |      4.24 |    0.17 |      0.22 |
| T.J. Edwards      |      4.19 |    0.00 |      0.31 |
| Jaylon Johnson    |      3.84 |    0.00 |      0.00 |
| Austin Booker     |      3.77 |    0.98 |      0.00 |

## CLE vs BAL
Projected 58 plays, 64% dropbacks, 30.5 pass att, 21.1 runs, 3.4 sacks. QB: Deshaun Watson
**Coaching style:** Red-zone pass rate high: 60% (league 53%); Sack rate high: 10% (league 6%); Shotgun rate high: 81% (league 61%); 3rd-down conversion low: 31% (league 42%); EPA/dropback low: +0.01 (league +0.06); EPA/run low: -0.34 (league -0.09).
**Market:** implied team total 18.5 (spread -4.5); has scored +1.0 pts/game vs its implied totals over 5 games (fell short in 40%), correction +0.5. Model 16.1 → blended 17.8: TD rates x1.11, yards x1.03, dropback rate +1.8%.
**Strength of schedule:** own scoring x1.05 (raw stats re-rated against the opponents actually faced).
**Out:** Tylan Wallace (carried from week 5 report: Out (Knee)), Teven Jenkins (carried from week 5 report: Out (Back)), Kalia Davis (carried from week 5 report: Out (Quadricep)), Mike Hall Jr. (carried from week 5 report: Out (Ankle)), Mason Graham (carried from week 5 report: Out (Knee)), Dillon Gabriel (carried from week 5 report: Out (Back)), Carsen Ryan (carried from week 5 report: Out (Calf)).
**Coach angle:** HC Todd Monken (first-year HC, 0 prior seasons); calls own plays (developing play-caller, 4 seasons calling); career run-first (-4.8 pts pass rate vs league, 4 seasons); leans on stars; this season top target share 19%.
**BAL defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: two_high [online (high)].
- BAL is soft deep (+0.98 EPA/deep att vs league +0.43); CLE throws deep 17%.
- Best matchups: run_inside_left (x1.26), pass_deep_right (x1.14); worst: pass_short_left (x0.82).
- Last game — worked: run_middle, run_inside_right; failed: run_inside_left, run_outside_right.
- BAL blitzes 32% of dropbacks (league 31%, FTN charting); CLE gains x1.25 as much per dropback vs the blitz as other offenses (66 blitzed dropbacks) -> pass yards x1.00
- CLE short plays vs zone heavy coverage defenses: x1.07 vs how other offenses fare (65 plays)
- CLE run plays vs zone heavy coverage defenses: x1.14 vs how other offenses fare (46 plays)
- CLE short plays vs two high shell defenses: x0.77 vs how other offenses fare (55 plays)
- CLE deep-throw rate vs two high shell: x1.27

| player            | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Deshaun Watson    | QB    |     193.86 |      1.19 |            0.51 |      5.79 |      34.79 |      0.00 |         0.00 |      0.00 |         0.11 |
| Quinshon Judkins  | RB    |       0.00 |      0.00 |            0.00 |     15.69 |      64.80 |      4.04 |         2.73 |     22.52 |         0.50 |
| Denzel Boston     | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.33 |         3.67 |     47.27 |         0.26 |
| Harold Fannin Jr. | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.46 |         3.40 |     37.01 |         0.27 |
| KC Concepcion     | WR    |       0.00 |      0.00 |            0.00 |      0.26 |       1.21 |      5.45 |         3.29 |     32.32 |         0.15 |
| Jerry Jeudy       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.35 |         1.95 |     20.43 |         0.10 |
| Raheim Sanders    | RB    |       0.00 |      0.00 |            0.00 |      2.02 |       8.92 |      2.15 |         1.46 |     11.97 |         0.15 |
| Isaiah Bond       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.22 |         1.29 |     16.49 |         0.08 |

**CLE kicker**

| player      |   fg_made |   xp_made |   kicking_points |
|:------------|----------:|----------:|-----------------:|
| Andre Szmyt |      2.27 |      1.85 |             8.66 |

**CLE defenders (vs BAL offense)**

| player                 |   tackles |   sacks |   def_int |
|:-----------------------|----------:|--------:|----------:|
| Carson Schwesinger     |      9.31 |    0.24 |      0.00 |
| Quincy Williams        |      7.91 |    0.00 |      0.00 |
| Denzel Ward            |      5.35 |    0.00 |      0.11 |
| Ronnie Hickman Jr.     |      5.31 |    0.14 |      0.10 |
| Grant Delpit           |      5.25 |    0.15 |      0.12 |
| Tyson Campbell         |      5.23 |    0.00 |      0.00 |
| Myles Harden           |      4.14 |    0.00 |      0.08 |
| Emmanuel McNeil-Warren |      3.97 |    0.00 |      0.00 |

## BAL vs CLE
Projected 62 plays, 52% dropbacks, 26.7 pass att, 29.9 runs, 3.0 sacks. QB: Tyler Huntley
**Coaching style:** Neutral-script pass rate low: 54% (league 59%); Red-zone pass rate low: 40% (league 53%); 4th-down go rate low: 13% (league 19%); Pass rate on 2nd & short low: 10% (league 31%); Pass rate on 3rd & short low: 28% (league 41%); Red-zone run share high: 61% (league 46%); EPA/dropback high: +0.20 (league +0.06); EPA/run high: +0.05 (league -0.09).
**Market:** implied team total 23.0 (spread +4.5); has scored +3.5 pts/game vs its implied totals over 5 games (fell short in 40%), correction +1.6. Model 22.6 → blended 23.8: TD rates x1.05, yards x1.02, dropback rate -1.8%.
**Strength of schedule:** own run yds x0.97, own scoring x0.96 (raw stats re-rated against the opponents actually faced).
**Out:** Trey Hendrickson (carried from week 5 report: Out (Finger)), Lamar Jackson (carried from week 5 report: Out (Ankle)), Cam Jurgens (carried from week 5 report: Out (Concussion)).
**Coach angle:** HC Jesse Minter (first-year HC, 0 prior seasons); plays called by OC Declan Doyle (first-time play-caller, 0 seasons calling); no prior play-calling seasons: this season's data only; this season top target share 25%.
**CLE defensive scheme (online/tagged):** blitz: avg, coverage: man_heavy, shell: single_high [online (high)].
- CLE run defense is soft (+0.01 EPA/run).
- Best matchups: run_outside_left (x1.20), run_inside_left (x1.11); worst: pass_short_left (x0.79).
- Last game — worked: none; failed: pass_short_middle.
- CLE blitzes 25% of dropbacks (league 31%, FTN charting); BAL gains x0.93 as much per dropback vs the blitz as other offenses (56 blitzed dropbacks) -> pass yards x1.00
- BAL short plays vs single high shell defenses: x0.83 vs how other offenses fare (65 plays)
- BAL deep-throw rate vs single high shell: x0.90

| player         | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:---------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Tyler Huntley  | QB    |     174.74 |      1.46 |            0.42 |      3.42 |      23.57 |      0.00 |         0.00 |      0.00 |         0.03 |
| Derrick Henry  | RB    |       0.00 |      0.00 |            0.00 |     24.98 |     114.98 |      1.80 |         1.29 |     11.09 |         0.61 |
| Zay Flowers    | WR    |       0.00 |      0.00 |            0.00 |      0.44 |       2.19 |      6.77 |         4.75 |     48.04 |         0.33 |
| Mark Andrews   | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.00 |         4.16 |     36.92 |         0.30 |
| Rashod Bateman | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.08 |         2.77 |     30.21 |         0.18 |
| Justice Hill   | RB    |       0.00 |      0.00 |            0.00 |      3.56 |      18.07 |      2.20 |         1.50 |     13.61 |         0.15 |

**BAL kicker**

| player     |   fg_made |   xp_made |   kicking_points |
|:-----------|----------:|----------:|-----------------:|
| Tyler Loop |      2.23 |      2.29 |             8.98 |

**BAL defenders (vs CLE offense)**

| player          |   tackles |   sacks |   def_int |
|:----------------|----------:|--------:|----------:|
| Roquan Smith    |      7.65 |    0.33 |      0.11 |
| Kyle Hamilton   |      7.10 |    0.00 |      0.22 |
| Trenton Simpson |      6.48 |    0.46 |      0.18 |
| Malaki Starks   |      6.39 |    0.23 |      0.00 |
| Jaylinn Hawkins |      4.11 |    0.00 |      0.00 |
| Marlon Humphrey |      3.65 |    0.00 |      0.00 |
| Tavius Robinson |      3.02 |    0.99 |      0.00 |
| Nate Wiggins    |      2.68 |    0.00 |      0.00 |

## IND vs TEN
Projected 65 plays, 54% dropbacks, 32.7 pass att, 29.8 runs, 1.5 sacks. QB: Daniel Jones
**Coaching style:** Red-zone pass rate low: 44% (league 53%); 4th-down go rate high: 28% (league 19%); Sack rate low: 4% (league 6%); Pass rate on 3rd & short low: 29% (league 41%); Red-zone run share high: 55% (league 46%); EPA/dropback low: -0.15 (league +0.06); EPA/run high: +0.10 (league -0.09).
**Market:** implied team total 25.8 (spread +7.0); has scored +3.2 pts/game vs its implied totals over 5 games (fell short in 20%), correction +1.5. Model 19.0 → blended 23.9: TD rates x1.26, yards x1.07, dropback rate -2.8%.
**Strength of schedule:** own pass yds x0.97, own run yds x1.04, opp run D x1.03, opp scoring D x1.03 (raw stats re-rated against the opponents actually faced).
**Out:** Arden Key (carried from week 5 report: Out (Hamstring)), Ashton Dulin (carried from week 5 report: Out (Hamstring)), Will Mallory (carried from week 5 report: Out (Thumb)), Jaylon Carlies (carried from week 5 report: Out (Ribs)).
**Coach angle:** HC Shane Steichen (young HC, 3 prior seasons); calls own plays (veteran play-caller, 5 seasons calling); career run-first (-3.3 pts pass rate vs league, 5 seasons); typical; this season top target share 22%.
**TEN defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: two_high [online (high)].
- TEN is soft deep (+0.94 EPA/deep att vs league +0.43); IND throws deep 17%.
- Best matchups: run_inside_right (x1.32), run_inside_left (x1.24); worst: pass_deep_middle (x0.99).
- Last game — worked: none; failed: pass_deep_left, run_inside_right.
- IND deep plays vs zone heavy coverage defenses: x0.90 vs how other offenses fare (23 plays)
- IND run plays vs two high shell defenses: x1.15 vs how other offenses fare (77 plays)
- IND deep-throw rate vs two high shell: x0.72

| player           | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-----------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Daniel Jones     | QB    |     205.61 |      1.34 |            0.48 |      2.74 |      14.72 |      0.00 |         0.00 |      0.00 |         0.11 |
| Jonathan Taylor  | RB    |       0.00 |      0.00 |            0.00 |     21.88 |     110.19 |      3.87 |         2.68 |     24.26 |         0.78 |
| Tyler Warren     | TE    |       0.00 |      0.00 |            0.00 |      0.69 |       3.09 |      7.69 |         5.66 |     50.98 |         0.31 |
| Josh Downs       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.25 |         4.15 |     44.49 |         0.19 |
| Keenan Allen     | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.52 |         3.64 |     34.06 |         0.24 |
| Laquon Treadwell | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.21 |         2.80 |     30.04 |         0.16 |
| Seth McGowan     | RB    |       0.00 |      0.00 |            0.00 |      4.73 |      24.10 |      0.92 |         0.66 |      5.55 |         0.21 |

**IND kicker**

| player          |   fg_made |   xp_made |   kicking_points |
|:----------------|----------:|----------:|-----------------:|
| Spencer Shrader |      4.73 |      2.82 |            17.02 |

**IND defenders (vs TEN offense)**

| player              |   tackles |   sacks |   def_int |
|:--------------------|----------:|--------:|----------:|
| Akeem Davis-Gaither |      7.44 |    0.00 |      0.00 |
| Justin Walley       |      4.99 |    0.13 |      0.00 |
| DeForest Buckner    |      4.45 |    0.46 |      0.00 |
| A.J. Haulcy         |      3.72 |    0.00 |      0.00 |
| Bryce Boettcher     |      3.43 |    0.00 |      0.00 |
| Camryn Bynum        |      3.40 |    0.00 |      0.00 |
| Grover Stewart      |      3.27 |    0.04 |      0.00 |
| Charvarius Ward     |      3.07 |    0.00 |      0.00 |

## TEN vs IND
Projected 54 plays, 64% dropbacks, 31.3 pass att, 19.3 runs, 1.1 sacks. QB: Cam Ward
**Coaching style:** Early-down pass rate low: 49% (league 53%); Deep-pass share low: 16% (league 19%); 3rd-down deep share low: 9% (league 21%); Red-zone pass rate low: 41% (league 53%); Sack rate low: 3% (league 6%); Shotgun rate high: 69% (league 61%); No-huddle rate high: 10% (league 6%); Pass rate on 3rd & short low: 17% (league 41%); Red-zone run share high: 59% (league 46%); 3rd-down conversion low: 34% (league 42%); EPA/dropback low: -0.25 (league +0.06); Favors run inside left (33%).
**Market:** implied team total 18.8 (spread -7.0); has scored -5.5 pts/game vs its implied totals over 5 games (fell short in 60%), correction -2.5. Model 16.4 → blended 16.3: TD rates x0.99, yards x1.00, dropback rate +2.8%.
**Strength of schedule:** own scoring x1.02 (raw stats re-rated against the opponents actually faced).
**Out:** Amani Hooker (carried from week 5 report: Out (Concussion)).
**Coach angle:** HC Robert Saleh (new to team, 5 prior seasons); plays called by OC Brian Daboll (veteran play-caller, 6 seasons calling); career balanced (-0.7 pts pass rate vs league, 6 seasons); typical; this season top target share 29%.
**IND defensive scheme (online/tagged):** blitz: avg, coverage: avg [online (high)].
- IND run defense is soft (+0.08 EPA/run).
- Best matchups: run_inside_left (x1.19), run_outside_left (x1.07); worst: run_inside_right (x0.88).
- IND blitzes 20% of dropbacks (league 31%, FTN charting); TEN gains x1.13 as much per dropback vs the blitz as other offenses (33 blitzed dropbacks) -> pass yards x0.99

| player             | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Cam Ward           | QB    |     188.66 |      1.33 |            0.42 |      2.99 |      21.04 |      0.00 |         0.00 |      0.00 |         0.03 |
| Tony Pollard       | RB    |       0.00 |      0.00 |            0.00 |     13.73 |      54.55 |      2.90 |         1.85 |     17.64 |         0.43 |
| Carnell Tate       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      7.95 |         4.89 |     57.28 |         0.24 |
| Wan'Dale Robinson  | WR    |       0.00 |      0.00 |            0.00 |      0.17 |       0.69 |      6.08 |         3.92 |     38.73 |         0.32 |
| Tyjae Spears       | RB    |       0.00 |      0.00 |            0.00 |      3.24 |      12.26 |      2.73 |         1.86 |     16.88 |         0.21 |
| Gunnar Helm        | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.12 |         1.40 |     13.08 |         0.10 |
| Elic Ayomanor      | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.96 |         1.18 |     13.85 |         0.09 |
| Calvin Ridley      | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.77 |         1.07 |     12.17 |         0.08 |
| Nicholas Singleton | RB    |       0.00 |      0.00 |            0.00 |      1.61 |       6.15 |      0.00 |         0.00 |      0.00 |         0.06 |

**TEN kicker**

| player    |   fg_made |   xp_made |   kicking_points |
|:----------|----------:|----------:|-----------------:|
| Joey Slye |      1.10 |      1.89 |             5.18 |

**TEN defenders (vs IND offense)**

| player            |   tackles |   sacks |   def_int |
|:------------------|----------:|--------:|----------:|
| Anthony Hill Jr.  |      8.61 |    0.00 |      0.00 |
| Cody Barton       |      5.54 |    0.00 |      0.00 |
| Jeffery Simmons   |      5.54 |    0.26 |      0.00 |
| Kevin Winston Jr. |      5.09 |    0.00 |      0.00 |
| Alontae Taylor    |      4.94 |    0.13 |      0.00 |
| Cedric Gray       |      4.86 |    0.10 |      0.00 |
| Amani Hooker      |      4.86 |    0.00 |      0.24 |
| Marcus Harris     |      4.29 |    0.08 |      0.24 |

## NWE vs NYJ
Projected 63 plays, 57% dropbacks, 29.4 pass att, 27.4 runs, 3.0 sacks. QB: Drake Maye
**Coaching style:** Deep-pass share high: 24% (league 19%); 3rd-down deep share low: 17% (league 21%); Red-zone pass rate high: 65% (league 53%); No-huddle rate low: 0% (league 6%); Red-zone run share low: 33% (league 46%); EPA/dropback high: +0.23 (league +0.06); Favors run middle (39%).
**Market:** implied team total 25.5 (spread +7.5); has scored -0.2 pts/game vs its implied totals over 5 games (fell short in 60%), correction -0.1. Model 19.9 → blended 23.2: TD rates x1.17, yards x1.05, dropback rate -3.0%.
**Out:** Mack Hollins (carried from week 5 report: Out (Calf)), Carlton Davis III (carried from week 5 report: Out (Neck)), Reggie Gilliam (carried from week 5 report: Out (Ankle)), Christian Gonzalez (carried from week 5 report: Out (Shoulder)), Karon Prunty (carried from week 5 report: Out (Hamstring)), Channing Canada (carried from week 5 report: Out (Hamstring)).
**Coach angle:** HC Mike Vrabel (veteran HC, 8 prior seasons); plays called by OC Josh McDaniels (veteran play-caller, 13 seasons calling); career balanced (+0.7 pts pass rate vs league, 13 seasons); typical; this season top target share 15%.
**NYJ defensive scheme (online/tagged):** blitz: heavy, coverage: avg, shell: two_high [online (high)].
- NYJ brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed +0.02 on 9 attempts. NWE 3rd-down deep share 17%.
- Best matchups: pass_short_middle (x1.13), pass_short_right (x1.11); worst: run_inside_left (x0.91).
- Last game — worked: pass_short_right, pass_deep_right; failed: pass_deep_left.
- NYJ blitzes 39% of dropbacks (league 31%, FTN charting); NWE gains x1.15 as much per dropback vs the blitz as other offenses (54 blitzed dropbacks) -> pass yards x1.01
- NWE deep plays vs two high shell defenses: x0.93 vs how other offenses fare (27 plays)
- NWE short plays vs two high shell defenses: x1.09 vs how other offenses fare (114 plays)

| player              | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:--------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Drake Maye          | QB    |     226.89 |      1.33 |            0.54 |      4.67 |      32.15 |      0.00 |         0.00 |      0.00 |         0.05 |
| Rhamondre Stevenson | RB    |       0.00 |      0.00 |            0.00 |     13.81 |      57.49 |      4.76 |         3.15 |     34.46 |         0.51 |
| Romeo Doubs         | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.72 |         3.48 |     48.81 |         0.28 |
| TreVeyon Henderson  | RB    |       0.00 |      0.00 |            0.00 |     10.38 |      41.20 |      1.11 |         0.70 |      7.82 |         0.35 |
| Hunter Henry        | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.54 |         2.95 |     37.46 |         0.19 |
| DeMario Douglas     | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.28 |         2.65 |     36.63 |         0.18 |
| Efton Chism III     | WR    |       0.00 |      0.00 |            0.00 |      0.26 |       1.18 |      3.21 |         1.94 |     27.24 |         0.16 |
| Eli Raridon         | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.24 |         1.41 |     17.19 |         0.11 |
| Kyle Williams       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.04 |         1.18 |     17.28 |         0.10 |
| Corey Kiner         | RB    |       0.00 |      0.00 |            0.00 |      1.97 |       7.62 |      0.00 |         0.00 |      0.00 |         0.07 |

**NWE kicker**

| player          |   fg_made |   xp_made |   kicking_points |
|:----------------|----------:|----------:|-----------------:|
| Andy Borregales |      1.18 |      2.31 |             5.84 |

**NWE defenders (vs NYJ offense)**

| player            |   tackles |   sacks |   def_int |
|:------------------|----------:|--------:|----------:|
| Robert Spillane   |      7.30 |    0.00 |      0.00 |
| Christian Elliss  |      7.01 |    0.25 |      0.00 |
| Charles Woods     |      4.69 |    0.00 |      0.00 |
| Elijah Ponder     |      4.47 |    1.63 |      0.00 |
| Marcus Jones      |      4.21 |    0.00 |      0.12 |
| Kevin Byard       |      3.90 |    0.00 |      0.00 |
| Craig Woodson     |      3.65 |    0.00 |      0.14 |
| Carlton Davis III |      3.41 |    0.00 |      0.00 |

## NYJ vs NWE
Projected 55 plays, 64% dropbacks, 29.6 pass att, 19.9 runs, 3.5 sacks. QB: Geno Smith
**Coaching style:** Deep-pass share low: 16% (league 19%); 4th-down go rate low: 11% (league 19%); Sack rate high: 10% (league 6%); Pass rate on 2nd & short low: 10% (league 31%); EPA/dropback low: -0.02 (league +0.06); Favors run inside left (31%).
**Market:** implied team total 18.0 (spread -7.5); has scored -1.6 pts/game vs its implied totals over 5 games (fell short in 60%), correction -0.8. Model 16.9 → blended 17.1: TD rates x1.01, yards x1.00, dropback rate +3.0%.
**Strength of schedule:** opp pass D x0.95, opp scoring D x0.95 (raw stats re-rated against the opponents actually faced).
**Out:** Dylan Parham (carried from week 5 report: Out (Knee)), Breece Hall (carried from week 5 report: Out (Quadricep)), Adonai Mitchell (carried from week 5 report: Out (Finger)), Francisco Mauigoa (carried from week 5 report: Out (Quadricep)).
**Coach angle:** HC Aaron Glenn (young HC, 1 prior seasons); plays called by OC Frank Reich (veteran play-caller, 5 seasons calling); career balanced (-0.9 pts pass rate vs league, 5 seasons); spreads it around; this season top target share 31%.
**NWE defensive scheme (online/tagged):** blitz: heavy, coverage: avg, shell: two_high [online (high)].
- NWE is soft deep (+0.67 EPA/deep att vs league +0.43); NYJ throws deep 16%.
- NWE brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed +0.48 on 11 attempts. NYJ 3rd-down deep share 19%.
- Best matchups: pass_short_middle (x1.17), pass_other (x1.00); worst: run_inside_right (x0.88).
- NWE blitzes 35% of dropbacks (league 31%, FTN charting); NYJ gains x1.16 as much per dropback vs the blitz as other offenses (44 blitzed dropbacks) -> pass yards x1.01
- NYJ short plays vs two high shell defenses: x1.08 vs how other offenses fare (98 plays)
- NYJ run plays vs two high shell defenses: x0.95 vs how other offenses fare (74 plays)
- NYJ deep-throw rate vs two high shell: x1.18

| player          | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:----------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Geno Smith      | QB    |     192.46 |      1.30 |            0.36 |      2.41 |      15.56 |      0.00 |         0.00 |      0.00 |         0.03 |
| Garrett Wilson  | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      9.33 |         6.00 |     69.67 |         0.39 |
| Braelon Allen   | RB    |       0.00 |      0.00 |            0.00 |     17.81 |      66.28 |      3.22 |         2.04 |     17.65 |         0.52 |
| Kenyon Sadiq    | TE    |       0.00 |      0.00 |            0.00 |      0.14 |       0.59 |      5.66 |         3.53 |     36.33 |         0.22 |
| Isaiah Williams | WR    |       0.00 |      0.00 |            0.00 |      0.49 |       1.95 |      3.60 |         2.29 |     26.12 |         0.17 |
| Jeremy Ruckert  | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.77 |         1.22 |     11.76 |         0.09 |

**NYJ kicker**

| player        |   fg_made |   xp_made |   kicking_points |
|:--------------|----------:|----------:|-----------------:|
| Jason Sanders |      1.25 |      1.86 |             5.60 |

**NYJ defenders (vs NWE offense)**

| player             |   tackles |   sacks |   def_int |
|:-------------------|----------:|--------:|----------:|
| Dane Belton        |      8.08 |    0.22 |      0.00 |
| Jamien Sherwood    |      7.25 |    0.00 |      0.00 |
| Demario Davis      |      7.13 |    0.34 |      0.00 |
| David Bailey       |      5.59 |    0.92 |      0.00 |
| Minkah Fitzpatrick |      5.06 |    0.00 |      0.54 |
| Azareye'h Thomas   |      3.83 |    0.00 |      0.00 |
| Jowon Briggs       |      3.38 |    0.35 |      0.00 |
| Andre Cisco        |      3.30 |    0.15 |      0.00 |

## NYG vs NOR
Projected 64 plays, 60% dropbacks, 34.3 pass att, 25.9 runs, 2.6 sacks. QB: Jameis Winston
**Coaching style:** Neutral-script pass rate low: 55% (league 59%); Early-down pass rate low: 45% (league 53%); Deep-pass share high: 22% (league 19%); 3rd-down deep share high: 25% (league 21%); 4th-down go rate low: 11% (league 19%); Pass rate on 3rd & short low: 0% (league 41%); 3rd-down conversion high: 47% (league 42%); EPA/dropback high: +0.13 (league +0.06); EPA/run low: -0.23 (league -0.09); Favors run inside left (33%).
**Market:** implied team total 22.0 (spread -1.5); has scored +1.2 pts/game vs its implied totals over 5 games (fell short in 40%), correction +0.6. Model 25.7 → blended 23.8: TD rates x0.93, yards x0.98, dropback rate +0.6%.
**Strength of schedule:** own pass yds x0.93, own scoring x0.93, opp scoring D x0.97 (raw stats re-rated against the opponents actually faced).
**Out:** Jason Pinnock (carried from week 5 report: Out (Concussion)), Chauncey Golston (carried from week 5 report: Out (Neck)).
**Coach angle:** HC John Harbaugh (new to team, 18 prior seasons); plays called by OC Matt Nagy (developing play-caller, 3 seasons calling); career balanced (+1.2 pts pass rate vs league, 3 seasons); leans on stars; this season top target share 31%.
**NOR defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: single_high [online (high)].
- NOR is soft deep (+0.79 EPA/deep att vs league +0.43); NYG throws deep 22%.
- NOR brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed +0.35 on 9 attempts. NYG 3rd-down deep share 25%.
- Best matchups: run_outside_left (x1.16), run_inside_right (x1.16); worst: pass_short_middle (x0.88).
- Last game — worked: none; failed: pass_deep_right.
- NOR blitzes 35% of dropbacks (league 31%, FTN charting); NYG gains x0.79 as much per dropback vs the blitz as other offenses (61 blitzed dropbacks) -> pass yards x0.99
- NYG deep plays vs zone heavy coverage defenses: x1.05 vs how other offenses fare (23 plays)

| player         | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:---------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Jameis Winston | QB    |     219.78 |      1.71 |            0.39 |      1.92 |      13.54 |      0.00 |         0.00 |      0.00 |         0.01 |
| Isaiah Likely  | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |     10.50 |         7.13 |     67.69 |         0.49 |
| Malik Nabers   | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      9.83 |         6.31 |     65.48 |         0.36 |
| Cam Skattebo   | RB    |       0.00 |      0.00 |            0.00 |     17.26 |      66.21 |      2.61 |         1.83 |     16.06 |         0.48 |
| Darnell Mooney | WR    |       0.00 |      0.00 |            0.00 |      0.16 |       0.68 |      3.85 |         2.33 |     25.55 |         0.14 |
| Malachi Fields | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.80 |         1.86 |     20.27 |         0.13 |
| Najee Harris   | RB    |       0.00 |      0.00 |            0.00 |      6.23 |      23.91 |      0.29 |         0.20 |      1.81 |         0.22 |
| Theo Johnson   | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.93 |         1.25 |     12.38 |         0.10 |

**NYG kicker**

| player        |   fg_made |   xp_made |   kicking_points |
|:--------------|----------:|----------:|-----------------:|
| Dominic Zvada |      2.27 |      2.48 |             9.29 |

**NYG defenders (vs NOR offense)**

| player           |   tackles |   sacks |   def_int |
|:-----------------|----------:|--------:|----------:|
| Arvell Reese     |      9.66 |    0.29 |      0.27 |
| Tremaine Edmunds |      9.05 |    0.54 |      0.00 |
| Greg Newsome II  |      4.90 |    0.00 |      0.27 |
| Jevon Holland    |      4.48 |    0.00 |      0.56 |
| Andru Phillips   |      4.25 |    0.60 |      0.00 |
| Tyler Nubin      |      4.04 |    0.00 |      0.00 |
| Deonte Banks     |      3.38 |    0.00 |      0.27 |
| Abdul Carter     |      3.25 |    0.45 |      0.00 |

## NOR vs NYG
Projected 63 plays, 64% dropbacks, 37.7 pass att, 22.7 runs, 2.1 sacks. QB: Tyler Shough
**Coaching style:** 3rd-down deep share high: 27% (league 21%); 4th-down go rate high: 34% (league 19%); No-huddle rate high: 15% (league 6%); Pass rate on 3rd & short low: 28% (league 41%); 3rd-down conversion high: 48% (league 42%); EPA/dropback low: -0.07 (league +0.06); EPA/run low: -0.17 (league -0.09); Favors run middle (40%).
**Market:** implied team total 23.5 (spread +1.5); has scored +2.1 pts/game vs its implied totals over 5 games (fell short in 40%), correction +1.0. Model 24.6 → blended 24.5: TD rates x1.00, yards x1.00, dropback rate -0.6%.
**Strength of schedule:** opp pass D x1.02, opp scoring D x1.03 (raw stats re-rated against the opponents actually faced).
**Out:** Kaden Elliss (carried from week 5 report: Out (Calf)), Anfernee Jennings (carried from week 5 report: Out (Knee)), Jeremiah Wright (carried from week 5 report: Out (Concussion)).
**Coach angle:** HC Kellen Moore (young HC, 1 prior seasons); calls own plays (veteran play-caller, 7 seasons calling); career balanced (-0.1 pts pass rate vs league, 7 seasons); typical; this season top target share 28%.
**NYG defensive scheme (online/tagged):** blitz: heavy, coverage: avg, shell: two_high [online (high)].
- NYG brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed +0.03 on 7 attempts. NOR 3rd-down deep share 27%.
- Best matchups: run_middle (x1.29), run_outside_right (x1.14); worst: pass_deep_left (x0.98).
- NYG blitzes 40% of dropbacks (league 31%, FTN charting); NOR gains x0.86 as much per dropback vs the blitz as other offenses (72 blitzed dropbacks) -> pass yards x0.99
- NOR deep plays vs two high shell defenses: x1.06 vs how other offenses fare (22 plays)
- NOR run plays vs two high shell defenses: x1.08 vs how other offenses fare (91 plays)
- NOR deep-throw rate vs two high shell: x0.89

| player        | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:--------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Tyler Shough  | QB    |     246.05 |      1.92 |            1.37 |      2.59 |      13.80 |      0.00 |         0.00 |      0.00 |         0.08 |
| Chris Olave   | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      9.72 |         6.60 |     74.51 |         0.32 |
| Juwan Johnson | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.77 |         4.94 |     46.41 |         0.39 |
| Devaughn Vele | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.94 |         4.52 |     47.52 |         0.29 |
| Alvin Kamara  | RB    |       0.00 |      0.00 |            0.00 |      7.91 |      32.93 |      3.67 |         2.61 |     21.56 |         0.35 |
| Kendre Miller | RB    |       0.00 |      0.00 |            0.00 |     10.11 |      41.43 |      1.55 |         1.07 |      9.22 |         0.40 |
| Bryce Lance   | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.65 |         2.14 |     22.67 |         0.14 |
| Noah Fant     | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.61 |         1.89 |     16.47 |         0.21 |
| CJ Donaldson  | RB    |       0.00 |      0.00 |            0.00 |      2.52 |      10.39 |      0.57 |         0.39 |      3.78 |         0.11 |

**NOR kicker**

| player         |   fg_made |   xp_made |   kicking_points |
|:---------------|----------:|----------:|-----------------:|
| Daniel Carlson |      0.63 |      2.55 |             4.45 |

**NOR defenders (vs NYG offense)**

| player             |   tackles |   sacks |   def_int |
|:-------------------|----------:|--------:|----------:|
| Pete Werner        |      7.03 |    0.22 |      0.00 |
| Jonas Sanker       |      6.56 |    0.00 |      0.00 |
| Danny Stutsman     |      6.45 |    0.00 |      0.00 |
| Justin Reid        |      6.07 |    0.00 |      0.00 |
| Julian Blackmon    |      5.39 |    0.00 |      0.39 |
| Kool-Aid McKinstry |      3.94 |    0.00 |      0.00 |
| Carl Granderson    |      3.22 |    0.72 |      0.00 |
| Quincy Riley       |      3.04 |    0.00 |      0.00 |

## PHI vs CAR
Projected 61 plays, 63% dropbacks, 34.7 pass att, 22.6 runs, 2.1 sacks. QB: Jalen Hurts
**Coaching style:** Deep-pass share low: 16% (league 19%); Red-zone pass rate low: 38% (league 53%); No-huddle rate high: 11% (league 6%); Pass rate on 3rd & short high: 55% (league 41%); Red-zone run share high: 61% (league 46%); 3rd-down conversion low: 33% (league 42%); EPA/dropback low: -0.09 (league +0.06); EPA/run low: -0.24 (league -0.09).
**Market:** implied team total 21.0 (spread +1.5); has scored -3.1 pts/game vs its implied totals over 5 games (fell short in 40%), correction -1.4. Model 22.9 → blended 20.9: TD rates x0.91, yards x0.97, dropback rate -0.6%.
**Strength of schedule:** own pass yds x0.96, own run yds x1.04, own scoring x1.02 (raw stats re-rated against the opponents actually faced).
**Out:** Saquon Barkley (carried from week 5 report: Out (Hamstring)), Marcus Epps (carried from week 5 report: Out (Groin)), Marquise Brown (carried from week 5 report: Out (Ankle)), DeVonta Smith (carried from week 5 report: Out (Hamstring)), Drew Kendall (carried from week 5 report: Out (Knee)).
**Coach angle:** HC Nick Sirianni (veteran HC, 5 prior seasons); plays called by OC Sean Mannion (first-time play-caller, 0 seasons calling); no prior play-calling seasons: this season's data only; this season top target share 20%.
**CAR defensive scheme (online/tagged):** blitz: heavy, coverage: zone_heavy [online (high)].
- CAR is soft deep (+0.54 EPA/deep att vs league +0.43); PHI throws deep 16%.
- CAR brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed -0.29 on 3 attempts. PHI 3rd-down deep share 19%.
- Best matchups: pass_short_middle (x1.19), pass_deep_left (x1.13); worst: pass_deep_middle (x0.91).
- CAR blitzes 32% of dropbacks (league 31%, FTN charting); PHI gains x0.80 as much per dropback vs the blitz as other offenses (68 blitzed dropbacks) -> pass yards x1.00
- PHI short plays vs zone heavy coverage defenses: x1.13 vs how other offenses fare (62 plays)
- PHI deep-throw rate vs zone heavy coverage: x1.21

| player           | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-----------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Jalen Hurts      | QB    |     211.05 |      1.39 |            0.72 |      4.15 |      23.40 |      0.00 |         0.00 |      0.00 |         0.10 |
| Dontayvion Wicks | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      7.86 |         4.54 |     57.81 |         0.25 |
| Makai Lemon      | WR    |       0.00 |      0.00 |            0.00 |      0.18 |       0.73 |      6.13 |         3.71 |     36.83 |         0.17 |
| Dallas Goedert   | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.84 |         2.92 |     31.62 |         0.23 |
| Will Shipley     | RB    |       0.00 |      0.00 |            0.00 |      6.81 |      27.61 |      2.33 |         1.35 |     12.82 |         0.31 |
| Darius Cooper    | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.92 |         2.23 |     31.43 |         0.28 |
| Tank Bigsby      | RB    |       0.00 |      0.00 |            0.00 |      8.89 |      36.42 |      1.15 |         0.70 |      5.92 |         0.33 |
| Dameon Pierce    | RB    |       0.00 |      0.00 |            0.00 |      4.53 |      18.41 |      1.95 |         1.11 |     10.06 |         0.22 |
| Zach Ertz        | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.43 |         1.38 |     17.08 |         0.08 |

**PHI kicker**

| player       |   fg_made |   xp_made |   kicking_points |
|:-------------|----------:|----------:|-----------------:|
| Jake Elliott |      0.97 |      2.21 |             5.12 |

**PHI defenders (vs CAR offense)**

| player               |   tackles |   sacks |   def_int |
|:---------------------|----------:|--------:|----------:|
| Jihaad Campbell      |      8.05 |    0.22 |      0.00 |
| Zack Baun            |      7.06 |    0.00 |      0.00 |
| Cooper DeJean        |      6.72 |    0.00 |      0.23 |
| Riq Woolen           |      4.88 |    0.00 |      0.00 |
| Quinyon Mitchell     |      4.82 |    0.00 |      0.27 |
| Andrew Mukuba        |      4.55 |    0.00 |      0.21 |
| Jeremiah Trotter Jr. |      4.03 |    0.00 |      0.00 |
| Jordan Davis         |      3.58 |    0.00 |      0.00 |

## CAR vs PHI
Projected 70 plays, 65% dropbacks, 42.9 pass att, 24.1 runs, 1.9 sacks. QB: Bryce Young
**Coaching style:** Neutral-script pass rate high: 65% (league 59%); Early-down pass rate high: 61% (league 53%); 3rd-down deep share low: 16% (league 21%); Red-zone pass rate high: 69% (league 53%); 4th-down go rate high: 27% (league 19%); Red-zone run share low: 30% (league 46%); EPA/dropback high: +0.20 (league +0.06); Favors run inside left (32%).
**Market:** implied team total 19.5 (spread -1.5); has scored +7.4 pts/game vs its implied totals over 4 games (fell short in 25%), correction +3.0. Model 26.3 → blended 24.0: TD rates x0.91, yards x0.97, dropback rate +0.6%.
**Strength of schedule:** opp pass D x0.97 (raw stats re-rated against the opponents actually faced).
**Coach angle:** HC Dave Canales (young HC, 2 prior seasons); calls own plays (developing play-caller, 3 seasons calling); career balanced (-0.9 pts pass rate vs league, 3 seasons); leans on stars; this season top target share 27%.
**PHI defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: two_high [online (high)].
- Best matchups: pass_short_left (x1.28), pass_short_right (x1.21); worst: pass_deep_middle (x0.86).
- Last game — worked: pass_deep_right; failed: none.
- CAR short plays vs zone heavy coverage defenses: x1.12 vs how other offenses fare (39 plays)
- CAR run plays vs zone heavy coverage defenses: x1.06 vs how other offenses fare (25 plays)
- CAR short plays vs two high shell defenses: x1.11 vs how other offenses fare (39 plays)
- CAR run plays vs two high shell defenses: x1.06 vs how other offenses fare (25 plays)

| player            | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Bryce Young       | QB    |     319.56 |      1.52 |            0.72 |      0.82 |       6.41 |      0.00 |         0.00 |      0.00 |         0.00 |
| Chuba Hubbard     | RB    |       0.00 |      0.00 |            0.00 |     20.21 |      98.05 |      3.05 |         2.01 |     22.91 |         0.67 |
| Tetairoa McMillan | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |     10.47 |         6.50 |     91.49 |         0.32 |
| Darren Waller     | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.24 |         3.88 |     49.09 |         0.26 |
| Jalen Coker       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.15 |         3.29 |     43.04 |         0.17 |
| Tommy Tremble     | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.65 |         2.99 |     35.34 |         0.13 |
| John Metchie III  | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.50 |         2.19 |     27.14 |         0.13 |
| Brycen Tremayne   | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.82 |         1.67 |     23.52 |         0.08 |
| AJ Dillon         | RB    |       0.00 |      0.00 |            0.00 |      3.88 |      17.59 |      0.74 |         0.48 |      5.40 |         0.16 |
| Mitchell Evans    | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.88 |         1.23 |     14.47 |         0.06 |

**CAR kicker**

| player          |   fg_made |   xp_made |   kicking_points |
|:----------------|----------:|----------:|-----------------:|
| Ryan Fitzgerald |      2.03 |      2.31 |             8.40 |

**CAR defenders (vs PHI offense)**

| player              |   tackles |   sacks |   def_int |
|:--------------------|----------:|--------:|----------:|
| Devin Lloyd         |      8.20 |    0.28 |      0.48 |
| Bobby Okereke       |      7.19 |    0.00 |      0.23 |
| Akayleb Evans       |      5.83 |    0.00 |      0.00 |
| Will Lee III        |      5.12 |    0.00 |      0.00 |
| Lathan Ransom       |      5.10 |    0.00 |      0.00 |
| Tre'von Moehrig     |      4.85 |    0.00 |      0.00 |
| Zakee Wheatley      |      4.21 |    0.00 |      0.00 |
| Princely Umanmielen |      3.08 |    0.96 |      0.00 |

## TAM vs PIT
Projected 58 plays, 61% dropbacks, 28.6 pass att, 22.7 runs, 2.8 sacks. QB: Jalon Daniels
**Coaching style:** Sack rate high: 9% (league 6%); Pass rate on 3rd & short high: 61% (league 41%); EPA/dropback low: -0.10 (league +0.06); EPA/run high: +0.01 (league -0.09); Favors run inside right (32%).
**Market:** implied team total 18.5 (spread -2.5); has scored -1.4 pts/game vs its implied totals over 5 games (fell short in 60%), correction -0.6. Model 15.4 → blended 16.9: TD rates x1.10, yards x1.03, dropback rate +1.0%.
**Strength of schedule:** own run yds x0.96, own scoring x1.02, opp pass D x1.03 (raw stats re-rated against the opponents actually faced).
**Out:** Baker Mayfield (carried from week 5 report: Out (Thumb)), Antoine Winfield Jr. (carried from week 5 report: Out (Rib)), SirVocea Dennis (carried from week 5 report: Out (Ankle)), Benjamin Morrison (carried from week 5 report: Out (Quadricep)).
**Coach angle:** HC Todd Bowles (veteran HC, 11 prior seasons); plays called by OC Zac Robinson (developing play-caller, 2 seasons calling); career run-first (-2.5 pts pass rate vs league, 2 seasons); leans on stars; this season top target share 24%.
**PIT defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy [online (high)].
- Best matchups: pass_deep_right (x1.06), pass_short_middle (x1.04); worst: run_inside_right (x0.79).
- PIT blitzes 27% of dropbacks (league 31%, FTN charting); TAM gains x0.87 as much per dropback vs the blitz as other offenses (71 blitzed dropbacks) -> pass yards x1.01
- TAM deep plays vs zone heavy coverage defenses: x0.94 vs how other offenses fare (9 plays)
- TAM run plays vs zone heavy coverage defenses: x0.85 vs how other offenses fare (43 plays)
- TAM deep-throw rate vs zone heavy coverage: x0.90

| player           | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-----------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Jalon Daniels    | QB    |     189.77 |      1.06 |            0.74 |      4.35 |      32.82 |      0.00 |         0.00 |      0.00 |         0.01 |
| Bucky Irving     | RB    |       0.00 |      0.00 |            0.00 |     15.93 |      63.32 |      3.24 |         2.34 |     19.22 |         0.50 |
| Emeka Egbuka     | WR    |       0.00 |      0.00 |            0.00 |      0.32 |       1.26 |      6.81 |         4.53 |     45.43 |         0.24 |
| Cade Otton       | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.12 |         3.43 |     38.90 |         0.14 |
| Kenny Gainwell   | RB    |       0.00 |      0.00 |            0.00 |      3.42 |      12.19 |      3.40 |         2.34 |     20.12 |         0.24 |
| Chris Godwin Jr. | WR    |       0.00 |      0.00 |            0.00 |      0.50 |       1.83 |      4.24 |         3.10 |     29.29 |         0.15 |
| Ted Hurst III    | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.35 |         1.49 |     17.92 |         0.10 |
| Tez Johnson      | WR    |       0.00 |      0.00 |            0.00 |      0.25 |       1.00 |      1.66 |         1.06 |     12.95 |         0.08 |
| Sean Tucker      | RB    |       0.00 |      0.00 |            0.00 |      1.94 |       6.76 |      0.00 |         0.00 |      0.00 |         0.09 |

**TAM kicker**

| player           |   fg_made |   xp_made |   kicking_points |
|:-----------------|----------:|----------:|-----------------:|
| Chase McLaughlin |      2.42 |      1.82 |             9.07 |

**TAM defenders (vs PIT offense)**

| player               |   tackles |   sacks |   def_int |
|:---------------------|----------:|--------:|----------:|
| Josiah Trotter       |      7.38 |    0.23 |      0.13 |
| Alex Anzalone        |      4.91 |    0.33 |      0.26 |
| Keionte Scott        |      4.80 |    0.00 |      0.00 |
| Jacob Parrish        |      4.71 |    0.00 |      0.21 |
| Tykee Smith          |      4.64 |    0.00 |      0.00 |
| Antoine Winfield Jr. |      4.11 |    0.00 |      0.00 |
| A'Shawn Robinson     |      2.76 |    0.28 |      0.18 |
| Zyon McCollum        |      2.51 |    0.00 |      0.00 |

## PIT vs TAM
Projected 56 plays, 66% dropbacks, 34.4 pass att, 18.9 runs, 1.7 sacks. QB: Aaron Rodgers
**Coaching style:** Neutral-script pass rate high: 68% (league 59%); Early-down pass rate high: 64% (league 53%); 3rd-down deep share high: 29% (league 21%); Red-zone pass rate high: 76% (league 53%); Red-zone run share low: 24% (league 46%); EPA/dropback low: -0.05 (league +0.06); EPA/run high: +0.11 (league -0.09).
**Market:** implied team total 21.0 (spread +2.5); has scored +1.4 pts/game vs its implied totals over 5 games (fell short in 40%), correction +0.6. Model 20.8 → blended 21.3: TD rates x1.02, yards x1.01, dropback rate -1.0%.
**Strength of schedule:** own pass yds x1.03, own run yds x0.97, opp run D x1.03 (raw stats re-rated against the opponents actually faced).
**Out:** DeShon Elliott (carried from week 5 report: Out (Knee)), Jamel Dean (carried from week 5 report: Out (Ankle)), Michael Pittman (carried from week 5 report: Out (Foot)).
**Coach angle:** HC Mike McCarthy (new to team, 20 prior seasons); calls own plays (veteran play-caller, 15 seasons calling); career pass-first (+3.4 pts pass rate vs league, 15 seasons); typical; this season top target share 20%.
**TAM defensive scheme (online/tagged):** blitz: heavy, coverage: avg, shell: single_high [online (high)].
- TAM brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed -0.59 on 12 attempts. PIT 3rd-down deep share 29%.
- Best matchups: pass_deep_middle (x1.13), pass_deep_right (x1.07); worst: pass_short_middle (x0.83).
- TAM blitzes 42% of dropbacks (league 31%, FTN charting); PIT gains x0.77 as much per dropback vs the blitz as other offenses (52 blitzed dropbacks) -> pass yards x0.97
- PIT deep plays vs single high shell defenses: x1.14 vs how other offenses fare (23 plays)
- PIT short plays vs single high shell defenses: x0.86 vs how other offenses fare (65 plays)
- PIT run plays vs single high shell defenses: x0.89 vs how other offenses fare (37 plays)
- PIT deep-throw rate vs single high shell: x1.12

| player             | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Aaron Rodgers      | QB    |     235.67 |      1.68 |            1.03 |      0.73 |       5.64 |      0.00 |         0.00 |      0.00 |         0.00 |
| Jaylen Warren      | RB    |       0.00 |      0.00 |            0.00 |     15.97 |      69.72 |      5.65 |         3.83 |     41.11 |         0.45 |
| DK Metcalf         | WR    |       0.00 |      0.00 |            0.00 |      0.27 |       1.23 |      7.59 |         4.46 |     55.02 |         0.26 |
| Pat Freiermuth     | TE    |       0.00 |      0.00 |            0.00 |      0.71 |       2.67 |      5.57 |         3.58 |     39.52 |         0.38 |
| Roman Wilson       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.58 |         2.69 |     34.96 |         0.24 |
| Germie Bernard     | WR    |       0.00 |      0.00 |            0.00 |      0.27 |       1.15 |      4.67 |         2.91 |     33.18 |         0.16 |
| Darnell Washington | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.52 |         2.29 |     24.66 |         0.16 |

**PIT kicker**

| player        |   fg_made |   xp_made |   kicking_points |
|:--------------|----------:|----------:|-----------------:|
| Chris Boswell |      2.19 |      2.01 |             8.58 |

**PIT defenders (vs TAM offense)**

| player                 |   tackles |   sacks |   def_int |
|:-----------------------|----------:|--------:|----------:|
| Payton Wilson          |      8.84 |    0.32 |      0.00 |
| Jaquan Brisker         |      7.04 |    0.00 |      0.15 |
| Patrick Queen          |      6.99 |    0.00 |      0.18 |
| Jalen Ramsey           |      5.75 |    0.00 |      0.00 |
| Cameron Heyward        |      3.56 |    0.41 |      0.00 |
| Robert Spears-Jennings |      3.16 |    0.00 |      0.26 |
| Asante Samuel Jr.      |      3.13 |    0.00 |      0.00 |
| Yahya Black            |      3.06 |    0.00 |      0.00 |

## LAR vs ARI
Projected 67 plays, 59% dropbacks, 37.7 pass att, 27.2 runs, 1.4 sacks. QB: Matthew Stafford
**Coaching style:** Neutral-script pass rate high: 65% (league 59%); Early-down pass rate high: 61% (league 53%); Red-zone pass rate high: 60% (league 53%); 4th-down go rate high: 26% (league 19%); Sack rate low: 3% (league 6%); No-huddle rate high: 11% (league 6%); Pass rate on 2nd & short high: 57% (league 31%); 3rd-down conversion high: 50% (league 42%); EPA/dropback high: +0.16 (league +0.06); EPA/run high: -0.00 (league -0.09); Favors run middle (40%).
**Market:** implied team total 32.0 (spread +12.5); has scored -1.4 pts/game vs its implied totals over 5 games (fell short in 20%), correction -0.6. Model 39.9 → blended 34.8: TD rates x0.87, yards x0.96, dropback rate -5.0%.
**Coach angle:** HC Sean McVay (veteran HC, 9 prior seasons); calls own plays (veteran play-caller, 9 seasons calling); career balanced (+1.2 pts pass rate vs league, 9 seasons); typical; this season top target share 24%.
**ARI defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: cover4 [online (low)].
- ARI is soft deep (+1.13 EPA/deep att vs league +0.43); LAR throws deep 22%.
- Best matchups: pass_short_left (x1.09), pass_short_right (x1.06); worst: pass_deep_middle (x0.86).
- Last game — worked: none; failed: pass_deep_middle, pass_deep_right.
- ARI blitzes 25% of dropbacks (league 31%, FTN charting); LAR gains x0.92 as much per dropback vs the blitz as other offenses (43 blitzed dropbacks) -> pass yards x1.00
- LAR deep plays vs zone heavy coverage defenses: x0.93 vs how other offenses fare (25 plays)
- LAR run plays vs zone heavy coverage defenses: x0.94 vs how other offenses fare (66 plays)

| player           | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-----------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Matthew Stafford | QB    |     281.65 |      2.73 |            0.93 |      1.02 |       6.64 |      0.00 |         0.00 |      0.00 |         0.01 |
| Kyren Williams   | RB    |       0.00 |      0.00 |            0.00 |     17.73 |      71.50 |      6.64 |         4.62 |     45.93 |         0.73 |
| Puka Nacua       | WR    |       0.00 |      0.00 |            0.00 |      0.76 |       3.07 |      9.20 |         6.17 |     71.17 |         0.44 |
| Davante Adams    | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      7.30 |         4.67 |     61.66 |         0.52 |
| Tyler Higbee     | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.06 |         3.50 |     39.35 |         0.30 |
| Blake Corum      | RB    |       0.00 |      0.00 |            0.00 |      8.41 |      32.51 |      2.33 |         1.57 |     17.36 |         0.34 |
| Konata Mumpfield | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.13 |         1.29 |     17.92 |         0.16 |
| Davis Allen      | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.54 |         0.97 |     11.04 |         0.09 |

**LAR kicker**

| player         |   fg_made |   xp_made |   kicking_points |
|:---------------|----------:|----------:|-----------------:|
| Harrison Mevis |      0.98 |      3.68 |             6.63 |

**LAR defenders (vs ARI offense)**

| player          |   tackles |   sacks |   def_int |
|:----------------|----------:|--------:|----------:|
| Nate Landman    |      9.59 |    0.00 |      0.00 |
| Quentin Lake    |      7.42 |    0.00 |      0.23 |
| Kam Curl        |      5.22 |    0.00 |      0.00 |
| Omar Speights   |      5.04 |    0.63 |      0.00 |
| Kamren Kinchens |      4.65 |    0.17 |      0.00 |
| Byron Young     |      4.36 |    1.10 |      0.00 |
| Kobie Turner    |      4.01 |    0.00 |      0.00 |
| Trent McDuffie  |      3.46 |    0.00 |      0.27 |

## ARI vs LAR
Projected 64 plays, 69% dropbacks, 40.5 pass att, 20.0 runs, 2.5 sacks. QB: Jacoby Brissett
**Coaching style:** Red-zone pass rate high: 64% (league 53%); No-huddle rate high: 11% (league 6%); Pass rate on 2nd & short high: 52% (league 31%); Red-zone run share low: 38% (league 46%); EPA/dropback low: -0.02 (league +0.06); Favors run middle (37%).
**Market:** implied team total 19.5 (spread -12.5); has scored +0.2 pts/game vs its implied totals over 5 games (fell short in 40%), correction +0.1. Model 25.7 → blended 22.0: TD rates x0.86, yards x0.96, dropback rate +5.0%.
**Strength of schedule:** own pass yds x1.04 (raw stats re-rated against the opponents actually faced).
**Out:** Andrew Wingard (carried from week 5 report: Out (Knee)), Isaiah Adams (carried from week 5 report: Out (Ankle)).
**Coach angle:** HC Mike LaFleur (first-year HC, 0 prior seasons); calls own plays (developing play-caller, 2 seasons calling); career pass-first (+3.9 pts pass rate vs league, 2 seasons); spreads it around; this season top target share 29%.
**LAR defensive scheme (online/tagged):** blitz: avg, coverage: avg, shell: two_high [online (high)].
- Best matchups: run_inside_right (x1.03), run_inside_left (x1.01); worst: pass_deep_right (x0.87).
- Last game — worked: pass_short_left, run_middle; failed: pass_deep_right, run_outside_right.
- LAR blitzes 27% of dropbacks (league 31%, FTN charting); ARI gains x0.90 as much per dropback vs the blitz as other offenses (58 blitzed dropbacks) -> pass yards x1.00

| player              | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:--------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Jacoby Brissett     | QB    |     244.69 |      1.70 |            1.27 |      2.63 |      12.38 |      0.34 |         0.22 |      1.97 |         0.08 |
| Trey McBride        | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |     11.93 |         7.74 |     70.49 |         0.38 |
| Michael Wilson      | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |     10.52 |         6.18 |     64.71 |         0.35 |
| Jeremiyah Love      | RB    |       0.00 |      0.00 |            0.00 |     11.63 |      42.06 |      2.95 |         1.96 |     15.99 |         0.36 |
| Tyler Allgeier      | RB    |       0.00 |      0.00 |            0.00 |      6.48 |      23.30 |      2.50 |         1.72 |     14.03 |         0.25 |
| Kendrick Bourne     | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.00 |         2.56 |     27.30 |         0.13 |
| Marvin Harrison Jr. | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.66 |         1.51 |     17.38 |         0.12 |
| Elijah Higgins      | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.16 |         1.40 |     14.15 |         0.10 |

**ARI kicker**

| player      |   fg_made |   xp_made |   kicking_points |
|:------------|----------:|----------:|-----------------:|
| Chad Ryland |      1.46 |      2.16 |             6.55 |

**ARI defenders (vs LAR offense)**

| player         |   tackles |   sacks |   def_int |
|:---------------|----------:|--------:|----------:|
| Budda Baker    |      8.87 |    0.31 |      0.37 |
| Mack Wilson    |      8.36 |    0.00 |      0.00 |
| Jack Gibbens   |      7.91 |    0.04 |      0.00 |
| Roy Lopez      |      5.04 |    0.18 |      0.00 |
| Andrew Wingard |      4.76 |    0.00 |      0.22 |
| Denzel Burke   |      3.78 |    0.00 |      0.35 |
| Max Melton     |      3.73 |    0.00 |      0.00 |
| Zaven Collins  |      3.61 |    0.14 |      0.00 |

## KAN vs LAC
Projected 61 plays, 55% dropbacks, 30.8 pass att, 27.3 runs, 1.4 sacks. QB: Patrick Mahomes
**Coaching style:** Early-down pass rate high: 58% (league 53%); 3rd-down deep share high: 37% (league 21%); Red-zone pass rate high: 60% (league 53%); 4th-down go rate high: 26% (league 19%); Sack rate low: 4% (league 6%); No-huddle rate low: 0% (league 6%); EPA/dropback high: +0.22 (league +0.06); EPA/run high: +0.11 (league -0.09); Favors run middle (38%).
**Market:** implied team total 25.5 (spread +8.5); has scored +3.9 pts/game vs its implied totals over 4 games (fell short in 25%), correction +1.6. Model 27.5 → blended 27.2: TD rates x0.99, yards x1.00, dropback rate -3.4%.
**Strength of schedule:** own pass yds x0.97, own run yds x0.97, own scoring x0.98, opp scoring D x0.97 (raw stats re-rated against the opponents actually faced).
**Coach angle:** HC Andy Reid (veteran HC, 27 prior seasons); calls own plays (veteran play-caller, 13 seasons calling); career pass-first (+3.1 pts pass rate vs league, 13 seasons); typical; this season top target share 19%.
**LAC defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: two_high [online (high)].
- Best matchups: run_outside_left (x1.16), run_inside_left (x1.08); worst: pass_short_middle (x0.87).
- LAC blitzes 27% of dropbacks (league 31%, FTN charting); KAN gains x1.17 as much per dropback vs the blitz as other offenses (38 blitzed dropbacks) -> pass yards x0.99
- KAN run plays vs two high shell defenses: x1.06 vs how other offenses fare (70 plays)
- KAN deep-throw rate vs two high shell: x1.19

| player             | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Patrick Mahomes    | QB    |     205.72 |      1.52 |            0.70 |      1.79 |      13.75 |      0.00 |         0.00 |      0.00 |         0.00 |
| Kenneth Walker III | RB    |       0.00 |      0.00 |            0.00 |     22.95 |     120.43 |      4.02 |         2.56 |     24.95 |         0.75 |
| Xavier Worthy      | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.07 |         3.80 |     43.12 |         0.25 |
| Travis Kelce       | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.06 |         3.24 |     38.89 |         0.26 |
| Tyquan Thornton    | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.94 |         2.41 |     32.07 |         0.21 |
| Rashee Rice        | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.12 |         2.63 |     31.94 |         0.17 |
| Emmett Johnson     | RB    |       0.00 |      0.00 |            0.00 |      3.44 |      16.17 |      0.93 |         0.61 |      5.91 |         0.16 |
| Noah Gray          | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.97 |         1.21 |     13.02 |         0.07 |

**KAN kicker**

| player          |   fg_made |   xp_made |   kicking_points |
|:----------------|----------:|----------:|-----------------:|
| Harrison Butker |      1.94 |      2.69 |             8.50 |

**KAN defenders (vs LAC offense)**

| player           |   tackles |   sacks |   def_int |
|:-----------------|----------:|--------:|----------:|
| Nick Bolton      |     11.13 |    0.00 |      0.00 |
| Drue Tranquill   |      8.48 |    0.00 |      0.00 |
| L'Jarius Sneed   |      7.24 |    0.00 |      0.00 |
| Mansoor Delane   |      6.89 |    0.00 |      0.23 |
| Jaden Hicks      |      6.54 |    0.00 |      0.00 |
| Alohi Gilman     |      5.01 |    0.00 |      0.00 |
| George Karlaftis |      4.46 |    0.00 |      0.34 |
| Nohl Williams    |      4.41 |    0.78 |      0.00 |

## LAC vs KAN
Projected 63 plays, 62% dropbacks, 33.1 pass att, 23.6 runs, 2.4 sacks. QB: Justin Herbert
**Coaching style:** Neutral-script pass rate low: 46% (league 59%); Early-down pass rate low: 37% (league 53%); 3rd-down deep share high: 25% (league 21%); Sack rate high: 10% (league 6%); Pass rate on 3rd & short high: 55% (league 41%); 3rd-down conversion low: 36% (league 42%); EPA/dropback low: -0.24 (league +0.06); EPA/run low: -0.18 (league -0.09).
**Market:** implied team total 17.0 (spread -8.5); has scored -5.6 pts/game vs its implied totals over 5 games (fell short in 80%), correction -2.5. Model 16.0 → blended 15.1: TD rates x0.94, yards x0.98, dropback rate +3.4%.
**Strength of schedule:** own pass yds x1.03, own scoring x0.94, opp pass D x1.03 (raw stats re-rated against the opponents actually faced).
**Out:** Donte Jackson (carried from week 5 report: Out (Hamstring)), Derwin James (carried from week 5 report: Out (Hamstring)), Kayode Awosika (carried from week 5 report: Out (Fibula)), Trey Lance (carried from week 5 report: Doubtful (Groin)), Trevor Penning (carried from week 5 report: Out (Concussion)), Quentin Johnston (carried from week 5 report: Out (Chest)), Joe Alt (carried from week 5 report: Out (Neck)), Brenen Thompson (carried from week 5 report: Out (Quadricep)).
**Coach angle:** HC Jim Harbaugh (veteran HC, 15 prior seasons); plays called by OC Mike McDaniel (developing play-caller, 4 seasons calling); career balanced (+1.1 pts pass rate vs league, 4 seasons); typical; this season top target share 18%.
**KAN defensive scheme (online/tagged):** blitz: avg, coverage: avg, shell: two_high [online (high)].
- Best matchups: run_middle (x1.06), run_outside_right (x1.04); worst: run_inside_right (x0.92).
- KAN blitzes 29% of dropbacks (league 31%, FTN charting); LAC gains x0.92 as much per dropback vs the blitz as other offenses (44 blitzed dropbacks) -> pass yards x1.00
- LAC short plays vs two high shell defenses: x0.94 vs how other offenses fare (116 plays)
- LAC run plays vs two high shell defenses: x1.05 vs how other offenses fare (115 plays)

| player                   | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-------------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Justin Herbert           | QB    |     215.41 |      1.02 |            1.26 |      4.78 |      32.54 |      0.30 |         0.19 |      2.00 |         0.04 |
| Tre Harris               | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      7.59 |         4.41 |     53.87 |         0.16 |
| Omarion Hampton          | RB    |       0.00 |      0.00 |            0.00 |     13.05 |      51.36 |      1.73 |         1.11 |     10.95 |         0.36 |
| Keaton Mitchell          | RB    |       0.00 |      0.00 |            0.00 |      6.02 |      24.84 |      4.54 |         2.97 |     26.75 |         0.26 |
| Oronde Gadsden II        | TE    |       0.00 |      0.00 |            0.00 |      0.18 |       0.69 |      4.74 |         2.88 |     32.38 |         0.16 |
| Ladd McConkey            | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.00 |         2.37 |     29.88 |         0.13 |
| Kimani Vidal             | RB    |       0.00 |      0.00 |            0.00 |      3.16 |      13.75 |      2.53 |         1.57 |     16.47 |         0.19 |
| Charlie Kolar            | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.27 |         1.48 |     14.56 |         0.07 |
| Marquez Valdes-Scantling | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.62 |         1.01 |     11.15 |         0.05 |

**LAC kicker**

| player         |   fg_made |   xp_made |   kicking_points |
|:---------------|----------:|----------:|-----------------:|
| Cameron Dicker |      1.55 |      1.64 |             6.29 |

**LAC defenders (vs KAN offense)**

| player             |   tackles |   sacks |   def_int |
|:-------------------|----------:|--------:|----------:|
| Daiyan Henley      |      5.99 |    0.04 |      0.00 |
| Del'Shawn Phillips |      5.59 |    0.00 |      0.00 |
| Akheem Mesidor     |      4.83 |    0.34 |      0.00 |
| Tuli Tuipulotu     |      4.41 |    0.27 |      0.20 |
| Cam Hart           |      3.97 |    0.00 |      0.15 |
| Tony Jefferson     |      3.75 |    0.00 |      0.00 |
| Elijah Molden      |      3.75 |    0.00 |      0.00 |
| Justin Eboigbe     |      3.37 |    0.07 |      0.00 |

## LVR vs BUF
Projected 69 plays, 63% dropbacks, 41.7 pass att, 25.5 runs, 1.5 sacks. QB: Kirk Cousins
**Coaching style:** Sack rate low: 4% (league 6%); Pass rate on 2nd & short low: 8% (league 31%); Pass rate on 3rd & short high: 53% (league 41%); EPA/dropback high: +0.14 (league +0.06); EPA/run low: -0.23 (league -0.09); Favors run middle (36%).
**Market:** implied team total 24.0 (spread -5.5); has scored +5.8 pts/game vs its implied totals over 5 games (fell short in 20%), correction +2.7. Model 32.3 → blended 28.9: TD rates x0.90, yards x0.97, dropback rate +2.2%.
**Strength of schedule:** opp pass D x0.97 (raw stats re-rated against the opponents actually faced).
**Out:** Jalen Nailor (carried from week 5 report: Out (Concussion)), Dont'e Thornton Jr. (carried from week 5 report: Out (Hamstring)), Trey Zuhn III (carried from week 5 report: Out (Knee)).
**Coach angle:** HC Klint Kubiak (first-year HC, 0 prior seasons); calls own plays (developing play-caller, 3 seasons calling); career balanced (-1.0 pts pass rate vs league, 3 seasons); leans on stars; this season top target share 24%.
**BUF defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: two_high [online (high)].
- Best matchups: pass_deep_left (x1.05), run_outside_left (x1.02); worst: run_inside_left (x0.85).
- BUF blitzes 25% of dropbacks (league 31%, FTN charting); LVR gains x1.17 as much per dropback vs the blitz as other offenses (48 blitzed dropbacks) -> pass yards x0.99
- LVR deep plays vs zone heavy coverage defenses: x1.07 vs how other offenses fare (7 plays)
- LVR deep-throw rate vs zone heavy coverage: x0.82
- LVR deep-throw rate vs two high shell: x1.12

| player              | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:--------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Kirk Cousins        | QB    |     300.17 |      2.46 |            0.58 |      0.75 |       5.30 |      0.00 |         0.00 |      0.00 |         0.01 |
| Ashton Jeanty       | RB    |       0.00 |      0.00 |            0.00 |     17.82 |      61.10 |      7.61 |         5.19 |     51.79 |         0.54 |
| Brock Bowers        | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |     11.19 |         7.62 |     87.98 |         0.55 |
| Tre Tucker          | WR    |       0.00 |      0.00 |            0.00 |      0.54 |       1.97 |      6.51 |         4.34 |     52.95 |         0.29 |
| Michael Mayer       | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.62 |         4.90 |     46.88 |         0.28 |
| Cody White          | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.71 |         2.37 |     26.82 |         0.28 |
| Mike Washington Jr. | RB    |       0.00 |      0.00 |            0.00 |      5.57 |      20.41 |      1.25 |         0.85 |      8.40 |         0.24 |

**LVR kicker**

| player   |   fg_made |   xp_made |   kicking_points |
|:---------|----------:|----------:|-----------------:|
| Matt Gay |      1.80 |      2.93 |             8.34 |

**LVR defenders (vs BUF offense)**

| player          |   tackles |   sacks |   def_int |
|:----------------|----------:|--------:|----------:|
| Nakobe Dean     |      9.41 |    0.18 |      0.00 |
| Quay Walker     |      6.65 |    0.20 |      0.00 |
| Jeremy Chinn    |      6.23 |    0.17 |      0.00 |
| Taron Johnson   |      4.68 |    0.00 |      0.00 |
| Hezekiah Masses |      3.95 |    0.00 |      0.55 |
| Treydan Stukes  |      3.38 |    0.00 |      0.14 |
| Eric Stokes     |      3.36 |    0.14 |      0.00 |
| Adam Butler     |      2.73 |    0.09 |      0.00 |

## BUF vs LVR
Projected 58 plays, 55% dropbacks, 26.2 pass att, 26.1 runs, 1.9 sacks. QB: Josh Allen
**Coaching style:** Deep-pass share high: 24% (league 19%); 3rd-down deep share high: 25% (league 21%); Shotgun rate low: 46% (league 61%); Pass rate on 3rd & short low: 11% (league 41%); 3rd-down conversion high: 54% (league 42%); EPA/dropback high: +0.35 (league +0.06); EPA/run high: +0.03 (league -0.09); Favors run middle (34%).
**Market:** implied team total 29.5 (spread +5.5); has scored +5.6 pts/game vs its implied totals over 5 games (fell short in 40%), correction +2.5. Model 30.3 → blended 31.4: TD rates x1.03, yards x1.01, dropback rate -2.2%.
**Strength of schedule:** own pass yds x1.03, opp scoring D x1.03 (raw stats re-rated against the opponents actually faced).
**Out:** Ed Oliver (carried from week 5 report: Out (Knee)), Josh Palmer (carried from week 5 report: Out (Shoulder)).
**Coach angle:** HC Joe Brady (first-year HC, 0 prior seasons); calls own plays (developing play-caller, 4 seasons calling); career balanced (-1.9 pts pass rate vs league, 4 seasons); typical; this season top target share 20%.
**LVR defensive scheme (online/tagged):** blitz: avg, coverage: avg, shell: two_high [online (high)].
- LVR is soft deep (+0.58 EPA/deep att vs league +0.43); BUF throws deep 24%.
- Best matchups: run_inside_right (x1.33), pass_short_right (x1.17); worst: pass_deep_middle (x0.94).
- Last game — worked: run_inside_left, run_inside_right; failed: none.
- LVR blitzes 26% of dropbacks (league 31%, FTN charting); BUF gains x0.93 as much per dropback vs the blitz as other offenses (42 blitzed dropbacks) -> pass yards x1.00
- BUF deep plays vs two high shell defenses: x0.95 vs how other offenses fare (23 plays)
- BUF run plays vs two high shell defenses: x1.07 vs how other offenses fare (107 plays)

| player         | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:---------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Josh Allen     | QB    |     216.74 |      1.61 |            0.70 |      7.91 |      48.36 |      0.17 |         0.12 |      1.41 |         0.40 |
| James Cook     | RB    |       0.00 |      0.00 |            0.00 |     20.06 |     111.80 |      2.10 |         1.41 |     15.34 |         0.73 |
| Khalil Shakir  | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.44 |         3.73 |     47.58 |         0.23 |
| Keon Coleman   | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.83 |         2.54 |     36.05 |         0.29 |
| DJ Moore       | WR    |       0.00 |      0.00 |            0.00 |      0.30 |       1.60 |      3.73 |         2.37 |     32.71 |         0.24 |
| Dalton Kincaid | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.62 |         2.36 |     34.85 |         0.21 |
| Ty Johnson     | RB    |       0.00 |      0.00 |            0.00 |      0.28 |       1.34 |      2.44 |         1.78 |     21.46 |         0.15 |
| Dawson Knox    | TE    |       0.00 |      0.00 |            0.00 |      0.21 |       0.98 |      2.09 |         1.43 |     16.97 |         0.16 |

**BUF kicker**

| player     |   fg_made |   xp_made |   kicking_points |
|:-----------|----------:|----------:|-----------------:|
| Tyler Bass |      1.22 |      3.09 |             6.76 |

**BUF defenders (vs LVR offense)**

| player               |   tackles |   sacks |   def_int |
|:---------------------|----------:|--------:|----------:|
| Dorian Williams      |      8.04 |    0.00 |      0.00 |
| Cole Bishop          |      7.33 |    0.00 |      0.00 |
| Terrel Bernard       |      6.81 |    0.00 |      0.00 |
| Christian Benford    |      5.17 |    0.00 |      0.00 |
| Davison Igbinosun    |      5.16 |    0.00 |      0.00 |
| C.J. Gardner-Johnson |      4.94 |    0.00 |      0.26 |
| Greg Rousseau        |      3.70 |    0.76 |      0.00 |
| Bradley Chubb        |      3.23 |    0.19 |      0.00 |

## GNB vs DAL
Projected 57 plays, 61% dropbacks, 33.5 pass att, 22.3 runs, 1.4 sacks. QB: Jordan Love
**Coaching style:** 3rd-down conversion low: 33% (league 42%); EPA/dropback high: +0.13 (league +0.06); EPA/run low: -0.25 (league -0.09); Favors run inside left (32%).
**Market:** implied team total 27.0 (spread +1.5); has scored -1.9 pts/game vs its implied totals over 5 games (fell short in 80%), correction -0.9. Model 31.2 → blended 28.1: TD rates x0.90, yards x0.97, dropback rate -0.6%.
**Strength of schedule:** own scoring x1.06 (raw stats re-rated against the opponents actually faced).
**Out:** Aaron Banks (carried from week 5 report: Doubtful (Knee)), Chris Brooks (carried from week 5 report: Out (Ankle)), Jacob Monk (carried from week 5 report: Doubtful (Quadricep)), Savion Williams (carried from week 5 report: Out (Ankle)).
**Coach angle:** HC Matt LaFleur (veteran HC, 7 prior seasons); calls own plays (veteran play-caller, 8 seasons calling); career balanced (-1.7 pts pass rate vs league, 8 seasons); typical; this season top target share 23%.
**DAL defensive scheme (online/tagged):** blitz: avg, coverage: avg [online (high)].
- DAL is soft deep (+0.83 EPA/deep att vs league +0.43); GNB throws deep 22%.
- Best matchups: run_inside_right (x1.13), run_outside_left (x1.08); worst: run_middle (x0.94).
- DAL blitzes 27% of dropbacks (league 31%, FTN charting); GNB gains x1.14 as much per dropback vs the blitz as other offenses (74 blitzed dropbacks) -> pass yards x0.99

| player           | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-----------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Jordan Love      | QB    |     249.30 |      2.24 |            0.24 |      0.80 |       4.32 |      0.00 |         0.00 |      0.00 |         0.02 |
| Christian Watson | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      7.61 |         4.88 |     61.28 |         0.58 |
| MarShawn Lloyd   | RB    |       0.00 |      0.00 |            0.00 |     12.88 |      49.51 |      3.29 |         2.35 |     21.87 |         0.55 |
| Matthew Golden   | WR    |       0.00 |      0.00 |            0.00 |      0.26 |       1.23 |      7.98 |         5.11 |     64.06 |         0.34 |
| Tucker Kraft     | TE    |       0.00 |      0.00 |            0.00 |      0.72 |       2.59 |      6.33 |         4.39 |     46.52 |         0.31 |
| Kaleb Johnson    | RB    |       0.00 |      0.00 |            0.00 |      6.55 |      26.93 |      0.70 |         0.47 |      4.45 |         0.23 |
| Skyy Moore       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.51 |         1.68 |     16.65 |         0.12 |
| Bo Melton        | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.52 |         1.05 |     11.05 |         0.08 |

**GNB kicker**

| player     |   fg_made |   xp_made |   kicking_points |
|:-----------|----------:|----------:|-----------------:|
| Trey Smack |      1.48 |      2.89 |             7.33 |

**GNB defenders (vs DAL offense)**

| player          |   tackles |   sacks |   def_int |
|:----------------|----------:|--------:|----------:|
| Evan Williams   |      9.80 |    0.10 |      0.18 |
| Zaire Franklin  |      8.24 |    0.00 |      0.00 |
| Javon Bullard   |      6.59 |    0.00 |      0.00 |
| Keisean Nixon   |      6.45 |    0.03 |      0.11 |
| Edgerrin Cooper |      5.72 |    0.24 |      0.18 |
| Lukas Van Ness  |      4.62 |    0.17 |      0.00 |
| Brandon Cisse   |      4.42 |    0.16 |      0.00 |
| Isaiah McDuffie |      3.95 |    0.00 |      0.00 |

## DAL vs GNB
Projected 63 plays, 64% dropbacks, 37.5 pass att, 22.7 runs, 1.3 sacks. QB: Dak Prescott
**Coaching style:** Neutral-script pass rate high: 68% (league 59%); Early-down pass rate high: 61% (league 53%); 3rd-down deep share low: 13% (league 21%); Sack rate low: 3% (league 6%); No-huddle rate high: 11% (league 6%); Pass rate on 3rd & short high: 60% (league 41%); EPA/dropback high: +0.16 (league +0.06); EPA/run high: -0.01 (league -0.09); Favors run middle (38%).
**Market:** implied team total 25.5 (spread -1.5); has scored +1.6 pts/game vs its implied totals over 5 games (fell short in 40%), correction +0.7. Model 27.9 → blended 26.9: TD rates x0.96, yards x0.99, dropback rate +0.6%.
**Strength of schedule:** own run yds x1.02, opp run D x0.97, opp scoring D x1.02 (raw stats re-rated against the opponents actually faced).
**Out:** Cobie Durant (carried from week 5 report: Out (Hamstring)), DeMarvion Overshown (carried from week 5 report: Out (Hamstring)), Drew Shelton (carried from week 5 report: Out (Hamstring)).
**Coach angle:** HC Brian Schottenheimer (young HC, 1 prior seasons); calls own plays (developing play-caller, 4 seasons calling); career run-first (-2.5 pts pass rate vs league, 4 seasons); typical; this season top target share 27%.
**GNB defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: two_high [online (high)].
- GNB brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed +0.82 on 11 attempts. DAL 3rd-down deep share 13%.
- GNB run defense is soft (+0.01 EPA/run).
- Best matchups: run_outside_left (x1.21), pass_deep_left (x1.17); worst: pass_short_middle (x0.90).
- Last game — worked: none; failed: pass_short_middle, pass_deep_left.
- GNB blitzes 38% of dropbacks (league 31%, FTN charting); DAL gains x0.92 as much per dropback vs the blitz as other offenses (68 blitzed dropbacks) -> pass yards x0.99
- DAL deep plays vs zone heavy coverage defenses: x1.16 vs how other offenses fare (14 plays)
- DAL short plays vs zone heavy coverage defenses: x0.94 vs how other offenses fare (117 plays)
- DAL deep-throw rate vs zone heavy coverage: x0.84
- DAL run plays vs two high shell defenses: x1.06 vs how other offenses fare (60 plays)

| player           | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-----------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Dak Prescott     | QB    |     254.68 |      1.55 |            1.29 |      2.08 |      15.08 |      0.00 |         0.00 |      0.00 |         0.01 |
| Javonte Williams | RB    |       0.00 |      0.00 |            0.00 |     18.53 |      72.35 |      3.81 |         2.78 |     23.24 |         0.79 |
| CeeDee Lamb      | WR    |       0.00 |      0.00 |            0.00 |      0.36 |       1.42 |      9.37 |         6.68 |     70.38 |         0.40 |
| George Pickens   | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      8.23 |         5.58 |     62.24 |         0.24 |
| Ryan Flournoy    | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.29 |         3.48 |     35.68 |         0.14 |
| Jake Ferguson    | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.33 |         2.97 |     26.17 |         0.23 |
| KaVontae Turpin  | WR    |       0.00 |      0.00 |            0.00 |      0.36 |       1.54 |      1.62 |         1.14 |     10.35 |         0.08 |
| Jonathan Mingo   | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.57 |         1.03 |     10.70 |         0.05 |
| Tyler Goodson    | RB    |       0.00 |      0.00 |            0.00 |      2.48 |      10.03 |      0.42 |         0.28 |      2.61 |         0.12 |

**DAL kicker**

| player         |   fg_made |   xp_made |   kicking_points |
|:---------------|----------:|----------:|-----------------:|
| Brandon Aubrey |      1.21 |      2.94 |             6.57 |

**DAL defenders (vs GNB offense)**

| player            |   tackles |   sacks |   def_int |
|:------------------|----------:|--------:|----------:|
| Dee Winters       |      6.32 |    0.00 |      0.00 |
| Caleb Downs       |      5.12 |    0.19 |      0.00 |
| Jaishawn Barham   |      4.76 |    0.00 |      0.00 |
| Donovan Ezeiruaku |      4.39 |    0.09 |      0.00 |
| DaRon Bland       |      3.65 |    0.00 |      0.00 |
| Markquese Bell    |      3.25 |    0.00 |      0.00 |
| Otito Ogbonnia    |      3.12 |    0.00 |      0.00 |
| Malik Hooker      |      2.71 |    0.00 |      0.00 |

## SFO vs WAS
Projected 57 plays, 57% dropbacks, 29.2 pass att, 24.2 runs, 0.7 sacks. QB: Brock Purdy
**Coaching style:** 4th-down go rate low: 8% (league 19%); Sack rate low: 3% (league 6%); Shotgun rate low: 48% (league 61%); No-huddle rate low: 0% (league 6%); 3rd-down conversion high: 50% (league 42%); EPA/dropback high: +0.38 (league +0.06); Favors run middle (37%).
**Market:** implied team total 29.0 (spread +7.5); has scored +5.6 pts/game vs its implied totals over 5 games (fell short in 20%), correction +2.5. Model 32.8 → blended 32.1: TD rates x0.98, yards x0.99, dropback rate -3.0%.
**Strength of schedule:** own pass yds x1.03, opp pass D x1.04, opp run D x1.02 (raw stats re-rated against the opponents actually faced).
**Out:** Kyle Juszczyk (carried from week 5 report: Out (Knee)), Nick Bosa (carried from week 5 report: Out (Knee)), Marques Sigle (carried from week 5 report: Out (Ankle)), James Thompson Jr. (carried from week 5 report: Out (Ankle)).
**Coach angle:** HC Kyle Shanahan (veteran HC, 9 prior seasons); calls own plays (veteran play-caller, 11 seasons calling); career balanced (-1.3 pts pass rate vs league, 11 seasons); typical; this season top target share 27%.
**WAS defensive scheme (online/tagged):** blitz: heavy, coverage: zone_heavy, shell: two_high [online (high)].
- WAS is soft deep (+0.68 EPA/deep att vs league +0.43); SFO throws deep 19%.
- WAS brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed +0.50 on 7 attempts. SFO 3rd-down deep share 23%.
- Best matchups: pass_short_middle (x1.09), run_inside_left (x1.09); worst: pass_short_left (x0.93).
- Last game — worked: none; failed: pass_deep_right.
- WAS blitzes 46% of dropbacks (league 31%, FTN charting); SFO gains x1.31 as much per dropback vs the blitz as other offenses (46 blitzed dropbacks) -> pass yards x1.04
- SFO deep plays vs zone heavy coverage defenses: x0.95 vs how other offenses fare (12 plays)
- SFO run plays vs zone heavy coverage defenses: x1.05 vs how other offenses fare (41 plays)
- SFO deep-throw rate vs zone heavy coverage: x1.13
- SFO short plays vs two high shell defenses: x0.92 vs how other offenses fare (103 plays)

| player              | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:--------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Brock Purdy         | QB    |     237.20 |      2.21 |            0.46 |      4.21 |      26.43 |      0.00 |         0.00 |      0.00 |         0.05 |
| Christian McCaffrey | RB    |       0.00 |      0.00 |            0.00 |     13.36 |      60.86 |      5.19 |         3.46 |     37.66 |         0.60 |
| Mike Evans          | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      7.81 |         4.93 |     74.55 |         0.50 |
| George Kittle       | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.94 |         4.56 |     60.16 |         0.49 |
| Deebo Samuel Sr.    | WR    |       0.00 |      0.00 |            0.00 |      1.99 |       9.55 |      4.34 |         2.94 |     33.31 |         0.33 |
| Kaelon Black        | RB    |       0.00 |      0.00 |            0.00 |      6.96 |      29.93 |      0.40 |         0.25 |      2.90 |         0.17 |

**SFO kicker**

| player       |   fg_made |   xp_made |   kicking_points |
|:-------------|----------:|----------:|-----------------:|
| Eddy Pineiro |      1.50 |      2.97 |             7.46 |

**SFO defenders (vs WAS offense)**

| player            |   tackles |   sacks |   def_int |
|:------------------|----------:|--------:|----------:|
| Fred Warner       |     10.48 |    0.08 |      0.00 |
| Dre Greenlaw      |      7.58 |    0.00 |      0.00 |
| Ji'Ayir Brown     |      7.00 |    0.00 |      0.00 |
| Marques Sigle     |      4.71 |    0.18 |      0.00 |
| Renardo Green     |      4.43 |    0.00 |      0.49 |
| Deommodore Lenoir |      4.07 |    0.00 |      0.00 |
| Jaden Dugger      |      3.84 |    0.29 |      0.00 |
| Malik Mustapha    |      3.66 |    0.00 |      0.00 |

## WAS vs SFO
Projected 65 plays, 64% dropbacks, 34.5 pass att, 23.2 runs, 2.6 sacks. QB: Jayden Daniels
**Coaching style:** Deep-pass share high: 23% (league 19%); Shotgun rate high: 71% (league 61%); Pass rate on 3rd & short high: 54% (league 41%); 3rd-down conversion low: 32% (league 42%); EPA/run low: -0.15 (league -0.09); Favors run inside right (30%).
**Market:** implied team total 21.5 (spread -7.5); has scored +2.5 pts/game vs its implied totals over 5 games (fell short in 40%), correction +1.2. Model 17.6 → blended 20.6: TD rates x1.17, yards x1.05, dropback rate +3.0%.
**Strength of schedule:** own run yds x0.97, opp pass D x1.03, opp scoring D x1.02 (raw stats re-rated against the opponents actually faced).
**Out:** Stefon Diggs (carried from week 5 report: Out (Hamstring)), Marcus Mariota (carried from week 5 report: Out (Knee)), Charles Omenihu (carried from week 5 report: Out (Groin)), Nick Cross (carried from week 5 report: Out (Illness)), Percy Butler (carried from week 5 report: Out (Hamstring)), Tyler Owens (carried from week 5 report: Out (Hamstring)).
**Coach angle:** HC Dan Quinn (veteran HC, 11 prior seasons); plays called by OC David Blough (first-time play-caller, 0 seasons calling); no prior play-calling seasons: this season's data only; this season top target share 19%.
**SFO defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy [online (high)].
- Best matchups: pass_short_left (x1.04), pass_deep_middle (x1.00); worst: pass_short_right (x0.89).
- SFO blitzes 33% of dropbacks (league 31%, FTN charting); WAS gains x0.88 as much per dropback vs the blitz as other offenses (55 blitzed dropbacks) -> pass yards x1.00
- WAS deep plays vs zone heavy coverage defenses: x0.93 vs how other offenses fare (15 plays)
- WAS short plays vs zone heavy coverage defenses: x0.93 vs how other offenses fare (58 plays)
- WAS run plays vs zone heavy coverage defenses: x0.92 vs how other offenses fare (57 plays)

| player                 | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-----------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Jayden Daniels         | QB    |     213.59 |      1.31 |            0.49 |      5.24 |      38.42 |      0.00 |         0.00 |      0.00 |         0.02 |
| Jacory Croskey-Merritt | RB    |       0.00 |      0.00 |            0.00 |     13.02 |      46.82 |      1.92 |         1.25 |     12.04 |         0.46 |
| Terry McLaurin         | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.38 |         3.88 |     46.27 |         0.21 |
| Antonio Williams       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.18 |         3.85 |     39.07 |         0.21 |
| Rachaad White          | RB    |       0.00 |      0.00 |            0.00 |      5.44 |      19.81 |      2.34 |         1.64 |     14.29 |         0.26 |
| Chig Okonkwo           | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.94 |         2.39 |     25.81 |         0.13 |
| Treylon Burks          | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.47 |         2.05 |     23.76 |         0.18 |
| Dyami Brown            | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.71 |         2.14 |     24.94 |         0.12 |
| Austin Ekeler          | RB    |       0.00 |      0.00 |            0.00 |      1.60 |       6.04 |      0.99 |         0.64 |      6.18 |         0.10 |
| Kaytron Allen          | RB    |       0.00 |      0.00 |            0.00 |      1.94 |       7.16 |      0.00 |         0.00 |      0.00 |         0.08 |

**WAS kicker**

| player       |   fg_made |   xp_made |   kicking_points |
|:-------------|----------:|----------:|-----------------:|
| Drew Stevens |      2.46 |      1.98 |             9.37 |

**WAS defenders (vs SFO offense)**

| player          |   tackles |   sacks |   def_int |
|:----------------|----------:|--------:|----------:|
| Sonny Styles    |      6.59 |    0.05 |      0.15 |
| Jeremy Reaves   |      6.20 |    0.00 |      0.00 |
| Amik Robertson  |      6.07 |    0.00 |      0.00 |
| Rasul Douglas   |      4.82 |    0.00 |      0.17 |
| Quan Martin     |      4.50 |    0.00 |      0.00 |
| Frankie Luvu    |      3.71 |    0.05 |      0.00 |
| Mike Sainristil |      2.78 |    0.00 |      0.00 |
| Daron Payne     |      2.15 |    0.10 |      0.00 |
