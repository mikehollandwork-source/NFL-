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

## Top 5 data-led projections per game

Direction vs the baseline (your line if entered, otherwise the player's own season average). Overs need rising carries/targets, unders falling ones, unless the player is a consistent-volume star or a starting QB. Ranked by score = edge x sample x signal agreement.

**ARI @ LAR**

|   rank | player          | team   | stat        | direction   |   baseline |   projected_median |   prob | signals                                                                                       |
|-------:|:----------------|:-------|:------------|:------------|-----------:|-------------------:|-------:|:----------------------------------------------------------------------------------------------|
|      1 | Tyler Higbee    | LAR    | targets     | under       |       6.50 |               4.00 |   0.81 | usage trending down (6.5 → 6.0); game script -5.8% dropbacks                                  |
|      2 | Jeremiyah Love  | ARI    | carries     | under       |      13.60 |              10.00 |   0.83 | usage trending down (13.7 → 13.0); game script +5.8% dropbacks                                |
|      3 | Davante Adams   | LAR    | targets     | under       |       9.00 |               6.00 |   0.79 | usage trending down (9.7 → 8.0); game script -5.8% dropbacks                                  |
|      4 | Kyren Williams  | LAR    | carries     | over        |      14.50 |              16.00 |   0.66 | usage trending up (12.7 → 16.0); game script -5.8% dropbacks; team total +11.5 vs its average |
|      5 | Jacoby Brissett | ARI    | completions | under       |      26.70 |              24.00 |   0.68 | matchup pass x0.92; similar offenses x0.96                                                    |

**ATL @ CHI**

|   rank | player         | team   | stat       | direction   |   baseline |   projected_median |   prob | signals                                                                     |
|-------:|:---------------|:-------|:-----------|:------------|-----------:|-------------------:|-------:|:----------------------------------------------------------------------------|
|      1 | Bijan Robinson | ATL    | rec_yds    | over        |      26.80 |              37.40 |   0.65 | matchup pass x1.09; usage trending up (5.3 → 4.5)                           |
|      2 | Kalif Raymond  | CHI    | receptions | under       |       4.40 |               4.00 |   0.67 | matchup pass x0.91; similar offenses x0.96; usage trending down (7.0 → 3.0) |

**BAL @ CLE**

|   rank | player           | team   | stat     | direction   |   baseline |   projected_median |   prob | signals                                                                         |
|-------:|:-----------------|:-------|:---------|:------------|-----------:|-------------------:|-------:|:--------------------------------------------------------------------------------|
|      1 | Quinshon Judkins | CLE    | rush_yds | over        |      45.90 |              68.90 |   0.82 | matchup run x1.12; usage trending up (14.0 → 15.5)                              |
|      2 | Zay Flowers      | BAL    | rec_yds  | under       |      94.00 |              43.80 |   0.89 | matchup pass x0.88; game script -1.3% dropbacks; team total -5.9 vs its average |
|      3 | Derrick Henry    | BAL    | rush_yds | over        |      93.00 |             108.40 |   0.67 | matchup run x1.07; game script -1.3% dropbacks                                  |
|      4 | Mark Andrews     | BAL    | targets  | over        |       6.00 |               6.00 |   0.56 | similar offenses x1.05; usage trending up (6.0 → 6.0)                           |

**BUF @ LVR**

|   rank | player        | team   | stat        | direction   |   baseline |   projected_median |   prob | signals                                                                                      |
|-------:|:--------------|:-------|:------------|:------------|-----------:|-------------------:|-------:|:---------------------------------------------------------------------------------------------|
|      1 | DJ Moore      | BUF    | targets     | under       |       6.20 |               4.00 |   0.91 | usage trending down (8.0 → 6.0); game script -1.4% dropbacks; team total -2.8 vs its average |
|      2 | Michael Mayer | LVR    | targets     | over        |       4.80 |               6.00 |   0.70 | usage trending up (4.7 → 5.5); game script +1.4% dropbacks                                   |
|      3 | Josh Allen    | BUF    | completions | under       |      17.70 |              17.00 |   0.58 | game script -1.4% dropbacks; team total -2.8 vs its average                                  |

**CAR @ PHI**

|   rank | player           | team   | stat        | direction   |   baseline |   projected_median |   prob | signals                                                                                                        |
|-------:|:-----------------|:-------|:------------|:------------|-----------:|-------------------:|-------:|:---------------------------------------------------------------------------------------------------------------|
|      1 | Jalen Coker      | CAR    | receptions  | under       |       5.60 |               3.00 |   0.93 | usage trending down (9.0 → 6.5); game script -1.0% dropbacks; team total -6.7 vs its average                   |
|      2 | Makai Lemon      | PHI    | targets     | over        |       4.80 |               6.00 |   0.74 | matchup pass x1.08; usage trending up (3.0 → 6.5); game script +1.0% dropbacks; team total +2.6 vs its average |
|      3 | Dontayvion Wicks | PHI    | targets     | over        |       5.80 |               8.00 |   0.78 | matchup pass x1.08; usage trending up (5.0 → 6.5); game script +1.0% dropbacks; team total +2.6 vs its average |
|      4 | Bryce Young      | CAR    | completions | under       |      25.70 |              22.00 |   0.80 | game script -1.0% dropbacks; team total -6.7 vs its average                                                    |
|      5 | Chuba Hubbard    | CAR    | carries     | over        |      16.00 |              19.00 |   0.76 | matchup run x1.10; usage trending up (11.0 → 19.5); game script -1.0% dropbacks                                |

**DAL @ GNB**

|   rank | player           | team   | stat     | direction   |   baseline |   projected_median |   prob | signals                                                                                                        |
|-------:|:-----------------|:-------|:---------|:------------|-----------:|-------------------:|-------:|:---------------------------------------------------------------------------------------------------------------|
|      1 | MarShawn Lloyd   | GNB    | rush_yds | over        |      22.00 |              52.30 |   0.94 | matchup run x1.10; usage trending up (7.7 → 8.5); game script -1.6% dropbacks; team total +10.0 vs its average |
|      2 | Christian Watson | GNB    | rec_yds  | under       |      95.60 |              60.50 |   0.78 | usage trending down (9.7 → 5.5); game script -1.6% dropbacks                                                   |
|      3 | Jake Ferguson    | DAL    | rec_yds  | over        |      20.10 |              22.80 |   0.56 | usage trending up (3.7 → 5.0); game script +1.6% dropbacks                                                     |
|      4 | Ryan Flournoy    | DAL    | rec_yds  | under       |      44.30 |              31.20 |   0.69 | matchup pass x0.96; usage trending down (6.0 → 4.5)                                                            |
|      5 | Matthew Golden   | GNB    | rec_yds  | under       |      80.50 |              67.40 |   0.62 | usage trending down (10.0 → 7.0); game script -1.6% dropbacks                                                  |

**DEN @ SEA**

|   rank | player             | team   | stat       | direction   |   baseline |   projected_median |   prob | signals                                                                                       |
|-------:|:-------------------|:-------|:-----------|:------------|-----------:|-------------------:|-------:|:----------------------------------------------------------------------------------------------|
|      1 | Emanuel Wilson     | SEA    | carries    | over        |      15.80 |              20.00 |   0.87 | usage trending up (10.7 → 20.5); game script -1.6% dropbacks                                  |
|      2 | Jaxon Smith-Njigba | SEA    | rec_yds    | under       |     112.40 |              74.10 |   0.80 | usage trending down (12.0 → 7.0); game script -1.6% dropbacks; team total -2.4 vs its average |
|      3 | RJ Harvey          | DEN    | receptions | under       |       4.80 |               3.00 |   0.72 | matchup pass x0.91; usage trending down (5.5 → 5.5)                                           |
|      4 | Sam Darnold        | SEA    | pass_yds   | under       |     237.20 |             206.30 |   0.68 | game script -1.6% dropbacks; team total -2.4 vs its average                                   |

**HOU @ JAX**

|   rank | player           | team   | stat       | direction   |   baseline |   projected_median |   prob | signals                                                                                       |
|-------:|:-----------------|:-------|:-----------|:------------|-----------:|-------------------:|-------:|:----------------------------------------------------------------------------------------------|
|      1 | Nico Collins     | HOU    | receptions | under       |       6.10 |               3.00 |   0.95 | usage trending down (10.0 → 7.5); team total -5.0 vs its average                              |
|      2 | Dalton Schultz   | HOU    | receptions | under       |       4.40 |               4.00 |   0.65 | usage trending down (8.3 → 3.0); team total -5.0 vs its average                               |
|      3 | Brenton Strange  | JAX    | targets    | over        |       5.80 |               6.00 |   0.60 | matchup pass x1.07; usage trending up (3.3 → 8.0)                                             |
|      4 | David Montgomery | HOU    | carries    | under       |       9.50 |               9.00 |   0.58 | usage trending down (12.3 → 7.5); game script +2.6% dropbacks; team total -5.0 vs its average |

**IND @ TEN**

|   rank | player          | team   | stat       | direction   |   baseline |   projected_median |   prob | signals                                                                                    |
|-------:|:----------------|:-------|:-----------|:------------|-----------:|-------------------:|-------:|:-------------------------------------------------------------------------------------------|
|      1 | Jonathan Taylor | IND    | rush_yds   | over        |      76.00 |             105.90 |   0.84 | matchup run x1.16; game script -4.5% dropbacks; team total +5.0 vs its average             |
|      2 | Carnell Tate    | TEN    | receptions | over        |       4.60 |               5.00 |   0.64 | usage trending up (6.7 → 8.5); game script +4.5% dropbacks; team total +7.0 vs its average |
|      3 | Josh Downs      | IND    | targets    | under       |       6.70 |               6.00 |   0.62 | usage trending down (8.0 → 5.0); game script -4.5% dropbacks                               |

**KAN @ LAC**

|   rank | player             | team   | stat     | direction   |   baseline |   projected_median |   prob | signals                                                                                                          |
|-------:|:-------------------|:-------|:---------|:------------|-----------:|-------------------:|-------:|:-----------------------------------------------------------------------------------------------------------------|
|      1 | Patrick Mahomes    | KAN    | pass_yds | under       |     258.20 |             193.70 |   0.83 | matchup pass x0.92; game script -3.2% dropbacks; team total -4.4 vs its average                                  |
|      2 | Kenneth Walker III | KAN    | rush_yds | under       |     134.10 |              99.10 |   0.82 | usage trending down (23.5 → 20.0); team total -4.4 vs its average                                                |
|      3 | Travis Kelce       | KAN    | rec_yds  | under       |      56.70 |              31.10 |   0.79 | matchup pass x0.92; usage trending down (8.0 → 3.0); game script -3.2% dropbacks; team total -4.4 vs its average |
|      4 | Ladd McConkey      | LAC    | rec_yds  | under       |      41.10 |              24.60 |   0.73 | matchup pass x0.97; usage trending down (5.0 → 3.5)                                                              |
|      5 | Omarion Hampton    | LAC    | carries  | under       |      14.20 |              13.00 |   0.66 | usage trending down (16.7 → 11.5); game script +3.2% dropbacks                                                   |

**NOR @ NYG**

|   rank | player         | team   | stat       | direction   |   baseline |   projected_median |   prob | signals                                                                                                      |
|-------:|:---------------|:-------|:-----------|:------------|-----------:|-------------------:|-------:|:-------------------------------------------------------------------------------------------------------------|
|      1 | Chris Olave    | NOR    | rec_yds    | under       |      99.20 |              66.70 |   0.81 | matchup pass x0.96; similar offenses x0.96; usage trending down (12.0 → 9.0); team total -3.3 vs its average |
|      2 | Alvin Kamara   | NOR    | rec_yds    | over        |       9.90 |              17.60 |   0.71 | usage trending up (3.5 → 4.5); game script +2.5% dropbacks                                                   |
|      3 | Noah Fant      | NOR    | receptions | under       |       2.60 |               2.00 |   0.71 | matchup pass x0.96; similar offenses x0.96; usage trending down (8.0 → 2.5); team total -3.3 vs its average  |
|      4 | Cam Skattebo   | NYG    | rush_yds   | over        |      58.20 |              69.60 |   0.67 | game script -2.5% dropbacks; team total +4.6 vs its average                                                  |
|      5 | Jameis Winston | NYG    | pass_yds   | under       |     218.20 |             192.00 |   0.67 | matchup pass x0.93; similar offenses x0.97; game script -2.5% dropbacks                                      |

**NWE @ NYJ**

|   rank | player              | team   | stat    | direction   |   baseline |   projected_median |   prob | signals                                                                   |
|-------:|:--------------------|:-------|:--------|:------------|-----------:|-------------------:|-------:|:--------------------------------------------------------------------------|
|      1 | Romeo Doubs         | NWE    | targets | over        |       4.70 |               6.00 |   0.73 | matchup pass x1.10; similar offenses x1.03; usage trending up (3.7 → 6.0) |
|      2 | Rhamondre Stevenson | NWE    | carries | over        |      11.40 |              13.00 |   0.67 | usage trending up (10.3 → 13.0); game script -1.1% dropbacks              |

**PIT @ TAM**

|   rank | player        | team   | stat       | direction   |   baseline |   projected_median |   prob | signals                                                 |
|-------:|:--------------|:-------|:-----------|:------------|-----------:|-------------------:|-------:|:--------------------------------------------------------|
|      1 | Ted Hurst III | TAM    | targets    | under       |       3.90 |               2.00 |   0.75 | matchup pass x0.94; usage trending down (5.0 → 3.0)     |
|      2 | Bucky Irving  | TAM    | receptions | under       |       3.30 |               2.00 |   0.79 | matchup pass x0.94; usage trending down (5.5 → 3.5)     |
|      3 | Jaylen Warren | PIT    | carries    | over        |      14.50 |              17.00 |   0.72 | similar offenses x1.02; usage trending up (12.7 → 16.0) |

**SFO @ WAS**

|   rank | player                 | team   | stat       | direction   |   baseline |   projected_median |   prob | signals                                                                           |
|-------:|:-----------------------|:-------|:-----------|:------------|-----------:|-------------------:|-------:|:----------------------------------------------------------------------------------|
|      1 | Christian McCaffrey    | SFO    | carries    | over        |      12.40 |              14.00 |   0.70 | matchup run x1.08; usage trending up (11.7 → 13.0); game script -3.3% dropbacks   |
|      2 | Antonio Williams       | WAS    | receptions | over        |       2.90 |               4.00 |   0.72 | usage trending up (3.7 → 5.5); game script +3.3% dropbacks                        |
|      3 | Terry McLaurin         | WAS    | rec_yds    | under       |      54.70 |              37.10 |   0.71 | matchup pass x0.93; usage trending down (6.5 → 6.5)                               |
|      4 | Jacory Croskey-Merritt | WAS    | rush_yds   | under       |      48.60 |              40.70 |   0.64 | matchup run x0.91; usage trending down (15.7 → 10.0); game script +3.3% dropbacks |

## Projected team totals (model)

`model_points` = simulated 6 x TD + extra points + 3 x field goals before game script; `final_points` = after game script (and the market blend for qualifying teams).

| team   | opp   |   model_points |   final_points |
|:-------|:------|---------------:|---------------:|
| DEN    | SEA   |           20.5 |           20.2 |
| SEA    | DEN   |           24.4 |           24.2 |
| JAX    | HOU   |           23.5 |           23.5 |
| HOU    | JAX   |           17.0 |           17.2 |
| ATL    | CHI   |           22.9 |           22.7 |
| CHI    | ATL   |           22.3 |           22.1 |
| CLE    | BAL   |           20.1 |           19.8 |
| BAL    | CLE   |           23.3 |           23.4 |
| IND    | TEN   |           29.8 |           30.8 |
| TEN    | IND   |           18.6 |           18.2 |
| NWE    | NYJ   |           20.3 |           20.6 |
| NYJ    | NWE   |           17.5 |           18.0 |
| NYG    | NOR   |           26.4 |           26.5 |
| NOR    | NYG   |           20.3 |           20.2 |
| PHI    | CAR   |           21.0 |           21.1 |
| CAR    | PHI   |           23.5 |           23.4 |
| TAM    | PIT   |           20.6 |           20.6 |
| PIT    | TAM   |           22.2 |           21.8 |
| LAR    | ARI   |           35.3 |           34.0 |
| ARI    | LAR   |           20.7 |           21.4 |
| KAN    | LAC   |           25.1 |           25.1 |
| LAC    | KAN   |           17.2 |           17.6 |
| LVR    | BUF   |           26.4 |           26.7 |
| BUF    | LVR   |           30.0 |           29.7 |
| GNB    | DAL   |           30.8 |           30.8 |
| DAL    | GNB   |           26.8 |           26.6 |
| SFO    | WAS   |           30.2 |           29.5 |
| WAS    | SFO   |           22.1 |           21.5 |

## DEN vs SEA
**Clock:** 11.1 drives each; DEN 5.45 plays/drive at 37.6 s per clock-running play vs SEA 5.44 at 38.1 s → projected possession 50%, 61 plays to 61.
Projected 61 plays, 61% dropbacks, 34.4 pass att, 23.5 runs, 1.9 sacks. QB: Bo Nix
**Coaching style:** Deep-pass share low: 12% (league 19%); 3rd-down deep share low: 14% (league 21%); 4th-down go rate low: 8% (league 19%); Sack rate low: 3% (league 6%); Pass rate on 2nd & short low: 0% (league 31%); EPA/dropback low: -0.08 (league +0.06); Favors run middle (35%).
**Model game script:** projected 20.5 – 24.4 (margin -3.9) → dropback rate +1.6%.
**Strength of schedule:** own pass yds x1.03, own run yds x1.04, own scoring x1.05 (raw stats re-rated against the opponents actually faced).
**Out:** Pat Surtain II (carried from week 5 report: Out (Ankle)), Riley Moss (carried from week 5 report: Out (Ribs)).
**Coach angle:** HC Sean Payton (veteran HC, 20 prior seasons); plays called by OC Davis Webb (first-time play-caller, 0 seasons calling); no prior play-calling seasons: this season's data only; this season top target share 22%.
**SEA secondary:** DC Mike Macdonald, mixed-leaning: Witherspoon stays at nickel (run fits / screens / blitzes); Emmanwori can also play inside; outside Devon Witherspoon / Josh Jobe; nickel Nick Emmanwori; note: depth chart lists Devon Witherspoon outside but reporting has him at nickel; weak spot: Outside corners tested (Mike Evans 113 yards in the SF loss); [research confidence medium, 2026-10-14].

**What worked last game → this week vs SEA** (failed play types cut, volume moved to what worked; `SEA allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player           | type      | cut (failed last game)                                                         | more of                                                                                    | SEA allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:-----------------|:----------|:-------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Evan Engram      | receiving | short_right (100% failed), short_left (50% failed)                             | short_left x1.1, deep_left x1.2                                                            | x0.91, x0.98                      |         0.0 |         1.1 |         0.0 |          0.0 |       22.1 |
| Marvin Mims Jr.  | receiving | short_left (100% failed)                                                       | short_right x1.1                                                                           | x0.91                             |         0.0 |         0.4 |         0.0 |          0.0 |        9.4 |
| Tyler Badie      | rushing   | run middle (100% failed)                                                       | run outside_left x1.1, run inside_right x1.1, run outside_right x1.1, run inside_left x1.1 | x0.97, x0.97, x0.97, x0.97        |        -0.0 |         0.3 |         0.0 |          0.0 |       14.6 |
| Tyler Badie      | receiving | short_right (100% failed)                                                      | deep_middle x1.1, short_left x1.1, deep_left x1.1, short_middle x1.1, deep_right x1.1      | x0.98, x0.91, x0.98, x0.91, x0.98 |        -0.0 |         0.3 |         0.0 |          0.0 |       14.6 |
| Courtland Sutton | receiving | short_left (100% failed)                                                       | short_right x1.2                                                                           | x0.91                             |         0.0 |         0.3 |         0.0 |          0.0 |       29.8 |
| Jaylen Waddle    | receiving | short_right (100% failed), short_left (33% failed), short_middle (100% failed) | short_left x1.2                                                                            | x0.91                             |         0.0 |         0.2 |         0.0 |          0.0 |       44.0 |
| J.K. Dobbins     | rushing   | run outside_right (50% failed), run middle (25% failed)                        | —                                                                                          | —                                 |         0.0 |         0.0 |         0.0 |          0.0 |       72.2 |
| RJ Harvey        | receiving | short_left (100% failed)                                                       | deep_middle x1.1, short_right x1.1, deep_left x1.1, short_middle x1.1, deep_right x1.1     | x0.98, x0.91, x0.98, x0.91, x0.98 |         0.0 |        -0.0 |         0.0 |          0.0 |       43.5 |

**SEA defensive weak spots:** red-zone TDs per play: 32% allowed vs league 21% (28 plays); vs RBs: 5.1 yds/target (league 5.3), x1.08 for RBs.
**Offenses like DEN that faced SEA:** ARI (similarity 0.23: -2.6 pass / -0.7 run yds/play vs their norm), SFO (similarity 0.06: -4.5 pass / +0.1 run yds/play vs their norm), WAS (similarity 0.04: -1.1 pass / -1.3 run yds/play vs their norm) → DEN pass x1.00, run x1.00.
**SEA defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: two_high [online (high)].
- Best matchups: pass_other (x1.00), pass_deep_left (x0.98); worst: pass_short_left (x0.91).
- SEA blitzes 21% of dropbacks (league 32%, FTN charting); DEN gains x0.75 as much per dropback vs the blitz as other offenses (57 blitzed dropbacks) -> pass yards x1.03
- DEN deep plays vs zone heavy coverage defenses: x0.95 vs how other offenses fare (7 plays)
- DEN deep plays vs two high shell defenses: x1.08 vs how other offenses fare (13 plays)

| player           | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-----------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Bo Nix           | QB    |     172.56 |      1.55 |            1.06 |      3.00 |      15.50 |      0.00 |         0.00 |      0.00 |         0.10 |
| J.K. Dobbins     | RB    |       0.00 |      0.00 |            0.00 |     15.63 |      63.21 |      1.51 |         1.03 |      8.21 |         0.34 |
| Jaylen Waddle    | WR    |       0.00 |      0.00 |            0.00 |      0.43 |       1.90 |      6.99 |         4.39 |     38.67 |         0.29 |
| RJ Harvey        | RB    |       0.00 |      0.00 |            0.00 |      3.43 |      14.06 |      4.94 |         3.52 |     26.50 |         0.23 |
| Courtland Sutton | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.86 |         2.88 |     27.19 |         0.23 |
| Evan Engram      | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.54 |         2.19 |     20.49 |         0.18 |
| Pat Bryant       | WR    |       0.00 |      0.00 |            0.00 |      0.14 |       0.64 |      2.29 |         1.45 |     13.48 |         0.12 |
| Tyler Badie      | RB    |       0.00 |      0.00 |            0.00 |      1.08 |       4.16 |      1.65 |         1.12 |      9.76 |         0.10 |

**DEN kicker**

| player   |   fg_made |   xp_made |   kicking_points |
|:---------|----------:|----------:|-----------------:|
| Wil Lutz |      1.75 |      2.05 |             7.29 |

**DEN defenders (vs SEA offense)**

| player          |   tackles |   sacks |   def_int |
|:----------------|----------:|--------:|----------:|
| Alex Singleton  |     10.08 |    0.00 |      0.00 |
| Brandon Jones   |      6.91 |    0.00 |      0.44 |
| Justin Strnad   |      5.61 |    0.00 |      0.00 |
| Talanoa Hufanga |      4.18 |    0.15 |      0.43 |
| Que Robinson    |      3.79 |    0.13 |      0.00 |
| Pat Surtain II  |      3.78 |    0.00 |      0.00 |
| Zach Allen      |      3.14 |    0.60 |      0.00 |
| Malcolm Roach   |      3.14 |    0.13 |      0.00 |

## SEA vs DEN
**Clock:** 11.1 drives each; SEA 5.44 plays/drive at 38.1 s per clock-running play vs DEN 5.45 at 37.6 s → projected possession 50%, 61 plays to 61.
Projected 61 plays, 53% dropbacks, 29.3 pass att, 28.3 runs, 2.2 sacks. QB: Sam Darnold
**Coaching style:** Neutral-script pass rate low: 55% (league 59%); Early-down pass rate low: 47% (league 53%); Sack rate high: 8% (league 6%); Shotgun rate low: 47% (league 61%); No-huddle rate low: 1% (league 6%); 3rd-down conversion low: 29% (league 42%); EPA/run low: -0.29 (league -0.09).
**Model game script:** projected 24.4 – 20.5 (margin +3.9) → dropback rate -1.6%.
**Strength of schedule:** opp pass D x0.96, opp run D x0.98 (raw stats re-rated against the opponents actually faced).
**Out:** Chazz Surratt (carried from week 5 report: Out (Calf)), Zach Charbonnet (carried from week 5 report: Out (Knee)), Julian Neal (carried from week 5 report: Out (Hamstring)).
**Coach angle:** HC Mike Macdonald (young HC, 2 prior seasons); plays called by OC Brian Fleury (first-time play-caller, 0 seasons calling); no prior play-calling seasons: this season's data only; this season top target share 34%.
**DEN secondary:** DC Vance Joseph, man-leaning: Man-heavy with Cover 1 among the league's most used; pressure plan built around Surtain's assignment; outside Pat Surtain II (OUT) / Riley Moss (OUT); nickel Ja'Quan McMillian; weak spot: Without Surtain the replacements (Barron / Abrams-Draine) take the boundary; Riley Moss also out; [research confidence medium, 2026-10-14].

**What worked last game → this week vs DEN** (failed play types cut, volume moved to what worked; `DEN allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player             | type      | cut (failed last game)                                                                                                 | more of                | DEN allows there   |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:-------------------|:----------|:-----------------------------------------------------------------------------------------------------------------------|:-----------------------|:-------------------|------------:|------------:|------------:|-------------:|-----------:|
| Jaxon Smith-Njigba | receiving | short_right (50% failed), deep_left (50% failed)                                                                       | —                      | —                  |         0.0 |        -2.6 |         0.0 |          0.0 |       84.1 |
| Rashid Shaheed     | receiving | short_left (100% failed), deep_right (100% failed)                                                                     | short_right x1.2       | x1.01              |         0.0 |        -1.7 |        -0.0 |          0.0 |       31.5 |
| Emanuel Wilson     | rushing   | run inside_right (20% failed), run middle (14% failed), run outside_right (25% failed), run outside_left (100% failed) | —                      | —                  |         0.0 |        -0.7 |         0.0 |         -0.3 |       94.8 |
| AJ Barner          | receiving | short_right (67% failed)                                                                                               | short_left x1.1        | x1.01              |         0.0 |        -0.7 |         0.0 |          0.0 |       33.6 |
| Cooper Kupp        | receiving | short_middle (100% failed), short_left (100% failed)                                                                   | short_right x1.2       | x1.01              |         0.0 |        -0.3 |         0.0 |          0.0 |       24.8 |
| George Holani      | receiving | short_right (100% failed), short_left (50% failed)                                                                     | short_left x1.2        | x1.01              |         0.0 |         0.1 |         0.0 |          0.0 |       46.6 |
| George Holani      | rushing   | run inside_left (100% failed), run outside_right (33% failed)                                                          | run outside_right x1.1 | x1.00              |         0.0 |         0.1 |         0.0 |          0.0 |       46.6 |
| Elijah Arroyo      | receiving | deep_left (100% failed)                                                                                                | —                      | —                  |         0.0 |        -0.0 |         0.0 |          0.0 |        3.1 |

**DEN defensive weak spots:** 3rd-down conversions: 49% allowed vs league 42% (76 plays); outside runs: 5.7 allowed vs league 4.9 (47 plays); vs TEs: 8.1 yds/target (league 7.2), x1.06 for TEs.
- DEN struggle: Wk1 vs KAN: +0.19 EPA/play allowed (norm -0.08). Why: outside runs 13.6 yds/play vs 4.1 in other games; TEs 13.2 yds/target vs 7.1 in other games; red-zone TD rate per play 33% vs 15%; KAN is a strong offense (+0.18 EPA/play in its other games)
- DEN struggle: Wk4 vs SFO: +0.12 EPA/play allowed (norm -0.06). Why: when blitzing 8.7 yds/dropback vs 5.2 in other games; TEs 11.7 yds/target vs 7.4 in other games; SFO is a strong offense (+0.28 EPA/play in its other games); short passes 7.3 yds/play vs 6.1 in other games
**Offenses like SEA that faced DEN:** JAX (similarity 0.32: -2.1 pass / -0.4 run yds/play vs their norm), KAN (similarity 0.12: -1.9 pass / +1.7 run yds/play vs their norm), LAC (similarity 0.05: -2.1 pass / +0.0 run yds/play vs their norm) → SEA pass x0.99, run x1.00.
**DEN defensive scheme (online/tagged):** blitz: heavy, coverage: avg, shell: two_high [online (high)].
- DEN brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed -1.10 on 7 attempts. SEA 3rd-down deep share 19%.
- Best matchups: pass_short_left (x1.01), pass_short_middle (x1.01); worst: pass_deep_left (x0.88).
- SEA short plays vs two high shell defenses: x1.11 vs how other offenses fare (86 plays)
- DEN DBs out: Riley Moss (22 tgts, 7.7 yds/tgt allowed), Patrick Surtain II (18 tgts, 7.6 yds/tgt allowed) -> coverage 7.8 → 8.1 yds/tgt; WR yards x1.04
- DEN shadow corner Pat Surtain II is out: no shadow this week

| player             | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Sam Darnold        | QB    |     211.52 |      1.72 |            1.05 |      0.83 |       6.24 |      0.00 |         0.00 |      0.00 |         0.02 |
| Jaxon Smith-Njigba | WR    |       0.00 |      0.00 |            0.00 |      0.31 |       1.39 |      9.90 |         6.33 |     79.32 |         0.58 |
| Emanuel Wilson     | RB    |       0.00 |      0.00 |            0.00 |     20.62 |      82.74 |      1.75 |         1.17 |     11.83 |         0.49 |
| George Holani      | RB    |       0.00 |      0.00 |            0.00 |      6.55 |      26.86 |      2.73 |         1.87 |     19.37 |         0.27 |
| AJ Barner          | TE    |       0.00 |      0.00 |            0.00 |      0.20 |       0.80 |      4.51 |         2.86 |     31.54 |         0.20 |
| Rashid Shaheed     | WR    |       0.00 |      0.00 |            0.00 |      0.61 |       2.79 |      3.85 |         2.33 |     27.60 |         0.16 |
| Cooper Kupp        | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.19 |         2.04 |     24.52 |         0.15 |

**SEA kicker**

| player      |   fg_made |   xp_made |   kicking_points |
|:------------|----------:|----------:|-----------------:|
| Jason Myers |      2.06 |      2.43 |             8.63 |

**SEA defenders (vs DEN offense)**

| player            |   tackles |   sacks |   def_int |
|:------------------|----------:|--------:|----------:|
| Ernest Jones      |      9.52 |    0.34 |      0.18 |
| Drake Thomas      |      6.42 |    0.09 |      0.17 |
| Devon Witherspoon |      6.03 |    0.00 |      0.00 |
| Julian Love       |      3.92 |    0.00 |      0.25 |
| Josh Jobe         |      3.86 |    0.00 |      0.10 |
| Byron Murphy II   |      3.74 |    0.53 |      0.00 |
| Nick Emmanwori    |      3.61 |    0.15 |      0.00 |
| Uchenna Nwosu     |      2.88 |    0.17 |      0.00 |

## JAX vs HOU
**Clock:** 9.9 drives each; JAX 6.04 plays/drive at 39.1 s per clock-running play vs HOU 5.96 at 37.9 s → projected possession 51%, 60 plays to 59.
Projected 60 plays, 57% dropbacks, 31.0 pass att, 25.6 runs, 2.2 sacks. QB: Trevor Lawrence
**Coaching style:** Deep-pass share low: 15% (league 19%); Red-zone pass rate high: 61% (league 53%); Pass rate on 2nd & short high: 47% (league 31%); EPA/dropback high: +0.26 (league +0.06); EPA/run high: -0.02 (league -0.09).
**Model game script:** projected 23.5 – 17.0 (margin +6.5) → dropback rate -2.6%.
**Strength of schedule:** own pass yds x1.03, own scoring x1.03 (raw stats re-rated against the opponents actually faced).
**Out:** Eric Murray (carried from week 5 report: Doubtful (Concussion)), Jaylon Jones (carried from week 5 report: Out (Hamstring)).
**Coach angle:** HC Liam Coen (young HC, 1 prior seasons); calls own plays (developing play-caller, 2 seasons calling); career balanced (+1.1 pts pass rate vs league, 2 seasons); spreads it around; this season top target share 24%.
**HOU secondary:** DC DeMeco Ryans, mixed-leaning: Mixes zone and man; declined to shadow George Pickens with Stingley; outside Derek Stingley Jr. / Kamari Lassiter; nickel Jalen Pitre; weak spot: Receivers who move around avoid Stingley; [research confidence medium, 2026-10-14].

**What worked last game → this week vs HOU** (failed play types cut, volume moved to what worked; `HOU allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player            | type      | cut (failed last game)                                                                                                     | more of                                                            | HOU allows there           |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:------------------|:----------|:---------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------|:---------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Brian Thomas Jr.  | receiving | deep_right (100% failed), short_right (100% failed), short_left (100% failed)                                              | short_middle x1.6, deep_left x1.6, deep_middle x1.6                | x1.08, x1.02, x1.02        |        -0.0 |         1.2 |         0.0 |          0.0 |       29.5 |
| Bhayshul Tuten    | rushing   | run inside_right (25% failed), run outside_left (75% failed), run inside_left (25% failed), run outside_right (67% failed) | run middle x1.1                                                    | x0.85                      |         0.0 |        -0.9 |         0.0 |         -0.3 |       77.0 |
| Bhayshul Tuten    | receiving | short_right (100% failed)                                                                                                  | short_middle x1.1, short_left x1.1                                 | x1.08, x1.08               |         0.0 |        -0.9 |         0.0 |         -0.3 |       77.0 |
| Parker Washington | receiving | short_right (67% failed), short_left (50% failed), deep_left (100% failed)                                                 | deep_right x1.1                                                    | x1.02                      |        -0.0 |        -0.8 |         0.0 |          0.0 |       58.7 |
| Jakobi Meyers     | receiving | short_left (100% failed)                                                                                                   | short_middle x1.1, short_right x1.1                                | x1.08, x1.08               |        -0.0 |        -0.5 |         0.0 |          0.0 |       32.3 |
| Josh Cameron      | receiving | short_right (50% failed), short_left (67% failed)                                                                          | short_middle x1.1                                                  | x1.08                      |         0.0 |        -0.4 |         0.0 |          0.0 |       24.8 |
| LeQuint Allen Jr. | receiving | short_middle (100% failed), short_right (100% failed)                                                                      | deep_right x1.4, short_left x1.4, deep_left x1.4, deep_middle x1.4 | x1.02, x1.08, x1.02, x1.02 |         0.0 |         0.3 |         0.0 |          0.0 |        9.6 |
| Brenton Strange   | receiving | short_middle (50% failed), short_left (33% failed)                                                                         | —                                                                  | —                          |         0.0 |        -0.1 |         0.0 |          0.0 |       54.9 |

**HOU defensive weak spots:** deep passes: 15.6 allowed vs league 11.9 (30 plays).
- HOU struggle: Wk1 vs BUF: +0.25 EPA/play allowed (norm -0.15). Why: TEs 19.6 yds/target vs 4.1 in other games; vs play action 11.0 yds/dropback vs 5.6 in other games; when blitzing 8.8 yds/dropback vs 6.3 in other games; deep passes 19.0 yds/play vs 13.6 in other games; WRs 10.9 yds/target vs 8.1 in other games
- HOU struggle: Wk4 vs DAL: +0.14 EPA/play allowed (norm -0.12). Why: vs play action 10.7 yds/dropback vs 5.0 in other games; deep passes 24.2 yds/play vs 13.8 in other games; missing starters: Azeez Al-Shaair (LB); red-zone TD rate per play 31% vs 13%; DAL is a strong offense (+0.12 EPA/play in its other games) → counted at 50% weight (those starters are available now)
**Offenses like JAX that faced HOU:** IND (similarity 0.52: +0.2 pass / -1.1 run yds/play vs their norm), BUF (similarity 0.05: +2.8 pass / -1.5 run yds/play vs their norm), DAL (similarity 0.05: -0.2 pass / -0.7 run yds/play vs their norm) → JAX pass x1.01, run x0.98.
**HOU defensive scheme (online/tagged):** blitz: light, coverage: zone_heavy [online (high)].
- HOU is soft deep (+0.95 EPA/deep att vs league +0.43); JAX throws deep 15%.
- Best matchups: pass_short_left (x1.08), pass_short_middle (x1.08); worst: run_outside_left (x0.85).
- Last game — worked: run_middle; failed: run_outside_left, run_outside_right.
- HOU blitzes 21% of dropbacks (league 32%, FTN charting); JAX gains x0.85 as much per dropback vs the blitz as other offenses (47 blitzed dropbacks) -> pass yards x1.02
- JAX short plays vs zone heavy coverage defenses: x1.08 vs how other offenses fare (40 plays)
- JAX run plays vs zone heavy coverage defenses: x0.92 vs how other offenses fare (24 plays)
- JAX deep-throw rate vs zone heavy coverage: x0.83

| player              | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:--------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Trevor Lawrence     | QB    |     242.62 |      1.38 |            0.53 |      2.34 |      13.53 |      0.00 |         0.00 |      0.00 |         0.08 |
| Bhayshul Tuten      | RB    |       0.00 |      0.00 |            0.00 |     16.73 |      58.60 |      2.41 |         1.67 |     17.82 |         0.43 |
| Parker Washington   | WR    |       0.00 |      0.00 |            0.00 |      0.21 |       0.80 |      6.77 |         4.26 |     56.57 |         0.33 |
| Brenton Strange     | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.28 |         4.27 |     52.33 |         0.20 |
| Jakobi Meyers       | WR    |       0.00 |      0.00 |            0.00 |      0.13 |       0.51 |      3.78 |         2.48 |     30.51 |         0.18 |
| Brian Thomas Jr.    | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.48 |         2.09 |     28.67 |         0.14 |
| Josh Cameron        | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.05 |         2.01 |     24.45 |         0.16 |
| Chris Rodriguez Jr. | RB    |       0.00 |      0.00 |            0.00 |      6.28 |      21.29 |      0.32 |         0.21 |      2.33 |         0.29 |

**JAX kicker**

| player     |   fg_made |   xp_made |   kicking_points |
|:-----------|----------:|----------:|-----------------:|
| Cam Little |      2.40 |      2.20 |             9.41 |

**JAX defenders (vs HOU offense)**

| player           |   tackles |   sacks |   def_int |
|:-----------------|----------:|--------:|----------:|
| Foyesade Oluokun |      7.82 |    0.00 |      0.18 |
| Ventrell Miller  |      6.61 |    0.18 |      0.00 |
| Antonio Johnson  |      5.13 |    0.18 |      0.00 |
| Travis Hunter    |      4.45 |    0.00 |      0.09 |
| Josh Hines-Allen |      3.98 |    0.25 |      0.00 |
| Jarrian Jones    |      3.81 |    0.00 |      0.09 |
| Rayuan Lane III  |      3.72 |    0.00 |      0.00 |
| Jourdan Lewis    |      3.59 |    0.00 |      0.19 |

## HOU vs JAX
**Clock:** 9.9 drives each; HOU 5.96 plays/drive at 37.9 s per clock-running play vs JAX 6.04 at 39.1 s → projected possession 49%, 59 plays to 60.
Projected 59 plays, 68% dropbacks, 36.7 pass att, 18.9 runs, 2.4 sacks. QB: C.J. Stroud
**Coaching style:** Early-down pass rate high: 58% (league 53%); Deep-pass share high: 23% (league 19%); Pass rate on 2nd & short high: 60% (league 31%); EPA/dropback high: +0.17 (league +0.06); EPA/run low: -0.20 (league -0.09); Favors run inside right (35%).
**Model game script:** projected 17.0 – 23.5 (margin -6.5) → dropback rate +2.6%.
**Strength of schedule:** own pass yds x0.95, own scoring x0.95, opp pass D x1.03, opp run D x1.02, opp scoring D x1.02 (raw stats re-rated against the opponents actually faced).
**Out:** Tank Dell (carried from week 5 report: Out (Knee)).
**Coach angle:** HC DeMeco Ryans (young HC, 3 prior seasons); plays called by OC Nick Caley (developing play-caller, 1 seasons calling); career balanced (+1.8 pts pass rate vs league, 1 seasons); typical; this season top target share 18%.
**JAX secondary:** DC Anthony Campanile, coverage lean unknown: New coverage scheme with pass game coordinator Mathieu Araujo; outside Travis Hunter / Montaric Brown; nickel Jourdan Lewis; weak spot: Hunter is the least experienced starter (returning from LCL tear); [research confidence low, 2026-10-14].

**What worked last game → this week vs JAX** (failed play types cut, volume moved to what worked; `JAX allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player            | type      | cut (failed last game)                                                                 | more of                                      | JAX allows there   |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:------------------|:----------|:---------------------------------------------------------------------------------------|:---------------------------------------------|:-------------------|------------:|------------:|------------:|-------------:|-----------:|
| Xavier Hutchinson | receiving | short_middle (50% failed)                                                              | —                                            | —                  |         0.0 |        -1.5 |         0.0 |          0.0 |       57.3 |
| Jaylin Noel       | receiving | short_left (33% failed), short_middle (100% failed)                                    | short_right x1.1                             | x1.14              |         0.0 |        -0.8 |         0.0 |          0.0 |       32.9 |
| Dalton Schultz    | receiving | deep_middle (100% failed)                                                              | —                                            | —                  |        -0.0 |         0.5 |         0.0 |          0.0 |       48.8 |
| Woody Marks       | receiving | short_right (33% failed)                                                               | —                                            | —                  |         0.0 |        -0.4 |         0.0 |         -0.1 |       48.1 |
| Woody Marks       | rushing   | run inside_left (50% failed), run outside_right (100% failed), run middle (25% failed) | run inside_right x1.1, run outside_left x1.1 | x0.98, x0.98       |         0.0 |        -0.4 |         0.0 |         -0.1 |       48.1 |
| Kayshon Boutte    | receiving | deep_right (50% failed), short_middle (100% failed)                                    | short_right x1.1, short_left x1.1            | x1.14, x1.14       |         0.0 |        -0.4 |         0.0 |          0.0 |       32.5 |
| Nico Collins      | receiving | short_right (33% failed), deep_left (100% failed)                                      | —                                            | —                  |         0.0 |        -0.3 |         0.0 |          0.0 |       45.4 |
| David Montgomery  | rushing   | run middle (100% failed)                                                               | run inside_left x1.1, run outside_right x1.1 | x0.98, x0.98       |        -0.0 |        -0.0 |         0.0 |          0.2 |       40.8 |

- JAX struggle: Wk2 vs DEN: +0.12 EPA/play allowed (norm -0.26). Why: TEs 12.2 yds/target vs 5.0 in other games; outside runs 5.4 yds/play vs 2.3 in other games; inside runs 3.8 yds/play vs 2.0 in other games; vs play action 10.4 yds/dropback vs 5.5 in other games; deep passes 20.0 yds/play vs 11.1 in other games
- JAX struggle: Wk4 vs CIN: +0.05 EPA/play allowed (norm -0.24). Why: when blitzing 8.6 yds/dropback vs 4.0 in other games; vs play action 8.2 yds/dropback vs 6.0 in other games; short passes 6.8 yds/play vs 5.4 in other games
**Offenses like HOU that faced JAX:** NWE (similarity 0.15: -2.4 pass / -1.2 run yds/play vs their norm), CIN (similarity 0.13: +1.0 pass / -2.7 run yds/play vs their norm), PHI (similarity 0.05: -0.3 pass / -2.9 run yds/play vs their norm) → HOU pass x0.99, run x0.98.
**JAX defensive scheme (online/tagged):** blitz: avg, coverage: avg, shell: two_high [online (high)].
- Best matchups: pass_short_left (x1.14), pass_short_middle (x1.14); worst: pass_deep_left (x0.89).
- JAX blitzes 31% of dropbacks (league 32%, FTN charting); HOU gains x1.33 as much per dropback vs the blitz as other offenses (42 blitzed dropbacks) -> pass yards x1.00
- HOU deep plays vs two high shell defenses: x0.87 vs how other offenses fare (14 plays)
- HOU short plays vs two high shell defenses: x1.14 vs how other offenses fare (63 plays)
- HOU run plays vs two high shell defenses: x1.08 vs how other offenses fare (53 plays)

| player            | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| C.J. Stroud       | QB    |     268.97 |      0.89 |            0.55 |      2.55 |      14.39 |      0.00 |         0.00 |      0.00 |         0.10 |
| Xavier Hutchinson | WR    |       0.00 |      0.00 |            0.00 |      0.26 |       0.96 |      6.74 |         4.11 |     53.91 |         0.13 |
| Dalton Schultz    | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.75 |         3.89 |     45.13 |         0.10 |
| Nico Collins      | WR    |       0.00 |      0.00 |            0.00 |      0.09 |       0.39 |      5.22 |         3.37 |     42.15 |         0.20 |
| Woody Marks       | RB    |       0.00 |      0.00 |            0.00 |      7.71 |      28.29 |      2.82 |         1.94 |     19.38 |         0.31 |
| David Montgomery  | RB    |       0.00 |      0.00 |            0.00 |      8.99 |      30.90 |      1.18 |         0.81 |      8.90 |         0.30 |
| Jaylin Noel       | WR    |       0.00 |      0.00 |            0.00 |      0.66 |       2.57 |      3.63 |         2.33 |     28.57 |         0.13 |
| Kayshon Boutte    | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.81 |         2.38 |     30.74 |         0.08 |
| Foster Moreau     | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.57 |         1.71 |     18.73 |         0.07 |
| Jared Wayne       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.09 |         1.21 |     16.78 |         0.04 |

**HOU kicker**

| player           |   fg_made |   xp_made |   kicking_points |
|:-----------------|----------:|----------:|-----------------:|
| Ka'imi Fairbairn |      1.89 |      1.58 |             7.26 |

**HOU defenders (vs JAX offense)**

| player            |   tackles |   sacks |   def_int |
|:------------------|----------:|--------:|----------:|
| Azeez Al-Shaair   |      9.00 |    0.00 |      0.00 |
| Reed Blankenship  |      8.84 |    0.00 |      0.22 |
| Jake Hansen       |      7.50 |    0.13 |      0.32 |
| Kamari Lassiter   |      6.52 |    0.00 |      0.00 |
| Tommy Togiai      |      6.31 |    0.00 |      0.00 |
| Will Anderson Jr. |      5.79 |    1.00 |      0.00 |
| Jalen Pitre       |      5.27 |    0.00 |      0.00 |
| Calen Bullock     |      4.40 |    0.00 |      0.00 |

## ATL vs CHI
**Clock:** 10.7 drives each; ATL 5.36 plays/drive at 38.1 s per clock-running play vs CHI 6.20 at 36.0 s → projected possession 48%, 58 plays to 67.
Projected 58 plays, 54% dropbacks, 28.1 pass att, 26.5 runs, 2.0 sacks. QB: Michael Penix Jr.
**Coaching style:** Neutral-script pass rate low: 48% (league 59%); Early-down pass rate low: 39% (league 53%); 3rd-down deep share high: 27% (league 21%); Red-zone pass rate low: 36% (league 53%); 4th-down go rate low: 9% (league 19%); Shotgun rate low: 48% (league 61%); Pass rate on 2nd & short low: 13% (league 31%); Red-zone run share high: 68% (league 46%); EPA/dropback low: -0.02 (league +0.06); EPA/run high: +0.06 (league -0.09); Favors run inside left (38%).
**Model game script:** projected 22.9 – 22.3 (margin +0.5) → dropback rate -0.2%.
**Strength of schedule:** own scoring x0.97 (raw stats re-rated against the opponents actually faced).
**Out:** Yasir Abdullah (carried from week 5 report: Out (Hamstring)).
**Coach angle:** HC Kevin Stefanski (new to team, 6 prior seasons); plays called by OC Tommy Rees (developing play-caller, 1 seasons calling); career balanced (+1.5 pts pass rate vs league, 1 seasons); spreads it around; this season top target share 32%.
**CHI secondary:** DC Dennis Allen, man-leaning: Man-heavy scheme; Allen has used his top corner to shadow WR1s in the past but not in 2026 while Jaylon Johnson recovered; outside Jaylon Johnson / Tyrique Stevenson; nickel Cam Lewis; weak spot: Johnson allowing a 118.8 passer rating when targeted through week 5 (PFF); rookie Malik Muhammad targeted; [research confidence medium, 2026-10-14].

**What worked last game → this week vs CHI** (failed play types cut, volume moved to what worked; `CHI allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player          | type      | cut (failed last game)                                      | more of                                                                                | CHI allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:----------------|:----------|:------------------------------------------------------------|:---------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Jahan Dotson    | receiving | short_right (100% failed), deep_left (100% failed)          | deep_right x1.4                                                                        | x1.15                             |         0.0 |         1.4 |         0.0 |          0.0 |       35.9 |
| Kyle Pitts      | receiving | deep_middle (100% failed)                                   | —                                                                                      | —                                 |         0.0 |         0.7 |         0.0 |          0.0 |       36.1 |
| Bijan Robinson  | rushing   | run inside_left (38% failed), run outside_left (50% failed) | —                                                                                      | —                                 |         0.0 |         0.3 |         0.0 |         -0.3 |      133.8 |
| Bijan Robinson  | receiving | short_left (33% failed), short_right (100% failed)          | short_left x1.1, short_middle x1.1                                                     | x1.07, x1.07                      |         0.0 |         0.3 |         0.0 |         -0.3 |      133.8 |
| Charlie Woerner | receiving | short_left (100% failed)                                    | short_right x1.2                                                                       | x1.07                             |         0.0 |         0.2 |         0.0 |          0.0 |        8.8 |
| Brian Robinson  | rushing   | run inside_left (40% failed)                                | —                                                                                      | —                                 |         0.0 |         0.2 |         0.0 |         -0.0 |       44.7 |
| Brian Robinson  | receiving | short_right (100% failed)                                   | short_left x1.1, deep_right x1.1, deep_middle x1.1, short_middle x1.1, deep_left x1.1  | x1.07, x1.15, x1.15, x1.07, x1.15 |         0.0 |         0.2 |         0.0 |         -0.0 |       44.7 |
| Jake Matthews   | receiving | short_left (100% failed)                                    | short_right x1.3, deep_right x1.3, deep_middle x1.3, short_middle x1.3, deep_left x1.3 | x1.07, x1.15, x1.15, x1.07, x1.15 |         0.0 |         0.1 |         0.0 |          0.0 |        2.7 |

**CHI defensive weak spots:** deep passes: 24.6 allowed vs league 11.9 (20 plays); play-action dropbacks: 11.4 allowed vs league 6.9 (38 plays); explosive plays: 11% allowed vs league 9% (199 plays).
- CHI struggle: Wk1 vs CAR: +0.09 EPA/play allowed (norm -0.04). Why: RBs 14.2 yds/target vs 3.5 in other games; vs play action 15.0 yds/dropback vs 10.5 in other games; red-zone TD rate per play 43% vs 14%; WRs 12.2 yds/target vs 10.2 in other games; CAR is a strong offense (+0.12 EPA/play in its other games)
- CHI struggle: Wk5 vs GNB: +0.33 EPA/play allowed (norm -0.10). Why: when blitzing 14.6 yds/dropback vs 5.4 in other games; TEs 12.8 yds/target vs 6.3 in other games; vs play action 16.1 yds/dropback vs 9.3 in other games; WRs 13.7 yds/target vs 9.5 in other games; deep passes 29.7 yds/play vs 21.8 in other games
**Offenses like ATL that faced CHI:** MIN (similarity 0.08: -0.0 pass / +0.6 run yds/play vs their norm), NYJ (similarity 0.02: -0.6 pass / +0.8 run yds/play vs their norm), GNB (similarity 0.01: +3.9 pass / -0.4 run yds/play vs their norm) → ATL pass x0.99, run x1.00.
**CHI defensive scheme (online/tagged):** blitz: heavy, coverage: man_heavy [online (high)].
- CHI is soft deep (+1.54 EPA/deep att vs league +0.43); ATL throws deep 20%.
- CHI brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed +0.59 on 5 attempts. ATL 3rd-down deep share 27%.
- CHI run defense is soft (+0.05 EPA/run).
- Best matchups: pass_deep_left (x1.15), pass_deep_middle (x1.15); worst: pass_other (x1.00).
- Last game — worked: pass_deep_right, run_inside_right; failed: none.
- CHI blitzes 39% of dropbacks (league 32%, FTN charting); ATL gains x1.37 as much per dropback vs the blitz as other offenses (49 blitzed dropbacks) -> pass yards x1.02

| player            | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Michael Penix Jr. | QB    |     234.81 |      1.21 |            0.93 |      0.97 |       7.62 |      0.00 |         0.00 |      0.00 |         0.04 |
| Bijan Robinson    | RB    |       0.00 |      0.00 |            0.00 |     18.15 |      88.58 |      5.58 |         3.80 |     42.90 |         0.69 |
| Drake London      | WR    |       0.00 |      0.00 |            0.00 |      0.23 |       1.18 |      7.73 |         4.92 |     74.78 |         0.20 |
| Brian Robinson    | RB    |       0.00 |      0.00 |            0.00 |      8.27 |      38.85 |      0.77 |         0.49 |      5.70 |         0.38 |
| Kyle Pitts        | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.95 |         2.56 |     34.64 |         0.17 |
| Jahan Dotson      | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.51 |         2.01 |     35.16 |         0.20 |
| Zachariah Branch  | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.81 |         1.21 |     14.28 |         0.07 |

**ATL kicker**

| player    |   fg_made |   xp_made |   kicking_points |
|:----------|----------:|----------:|-----------------:|
| Nick Folk |      1.68 |      2.44 |             7.49 |

**ATL defenders (vs CHI offense)**

| player             |   tackles |   sacks |   def_int |
|:-------------------|----------:|--------:|----------:|
| Xavier Watts       |      9.30 |    0.11 |      0.33 |
| Divine Deablo      |      7.29 |    0.00 |      0.00 |
| C.J. Henderson     |      6.72 |    0.00 |      0.00 |
| Mike Hughes        |      6.68 |    0.00 |      0.00 |
| Kendal Daniels     |      6.11 |    0.23 |      0.00 |
| Jessie Bates       |      5.75 |    0.00 |      0.00 |
| Harold Perkins Jr. |      5.43 |    0.10 |      0.00 |
| Sydney Brown       |      4.52 |    0.00 |      0.00 |

## CHI vs ATL
**Clock:** 10.7 drives each; CHI 6.20 plays/drive at 36.0 s per clock-running play vs ATL 5.36 at 38.1 s → projected possession 52%, 67 plays to 58.
Projected 67 plays, 56% dropbacks, 32.6 pass att, 29.2 runs, 2.1 sacks. QB: Tyson Bagent
**Coaching style:** 3rd-down deep share low: 14% (league 21%); Red-zone pass rate low: 42% (league 53%); 4th-down go rate high: 42% (league 19%); Shotgun rate low: 53% (league 61%); Pass rate on 2nd & short high: 44% (league 31%); Red-zone run share high: 56% (league 46%); 3rd-down conversion high: 48% (league 42%); EPA/run high: -0.03 (league -0.09); Favors run inside right (45%).
**Model game script:** projected 22.3 – 22.9 (margin -0.5) → dropback rate +0.2%.
**Strength of schedule:** own pass yds x1.05, own scoring x1.03, opp pass D x0.98, opp scoring D x0.98 (raw stats re-rated against the opponents actually faced).
**Out:** Kyle Monangai (carried from week 5 report: Out (Thumb)), Keyshaun Elliott (carried from week 5 report: Out (Quadricep)).
**Coach angle:** HC Ben Johnson (young HC, 1 prior seasons); calls own plays (developing play-caller, 4 seasons calling); career balanced (-0.8 pts pass rate vs league, 4 seasons); typical; this season top target share 23%.
**ATL secondary:** DC Jeff Ulbrich, man-leaning: Ulbrich pushed toward more man coverage; 4-3 roots; outside C.J. Henderson / Mike Hughes; nickel Billy Bowman Jr.; weak spot: Terrell graded 46-48 in coverage by PFF early in 2026; current depth chart lists C.J. Henderson and Mike Hughes outside; [research confidence medium, 2026-10-14].

**What worked last game → this week vs ATL** (failed play types cut, volume moved to what worked; `ATL allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player            | type      | cut (failed last game)                                                          | more of                                                                             | ATL allows there           |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:------------------|:----------|:--------------------------------------------------------------------------------|:------------------------------------------------------------------------------------|:---------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Luther Burden III | rushing   | run outside_right (100% failed)                                                 | run outside_left x1.1                                                               | x1.08                      |         0.0 |         1.2 |        -0.0 |          0.0 |       66.2 |
| Luther Burden III | receiving | deep_right (100% failed)                                                        | —                                                                                   | —                          |         0.0 |         1.2 |        -0.0 |          0.0 |       66.2 |
| Kalif Raymond     | rushing   | run outside_right (100% failed)                                                 | run inside_right x1.1, run inside_left x1.1, run outside_left x1.1, run middle x1.1 | x1.08, x1.08, x1.08, x1.08 |         0.0 |         0.9 |         0.0 |         -0.0 |       41.3 |
| Kalif Raymond     | receiving | short_left (100% failed)                                                        | short_right x1.1                                                                    | x0.91                      |         0.0 |         0.9 |         0.0 |         -0.0 |       41.3 |
| D'Andre Swift     | receiving | short_right (33% failed)                                                        | —                                                                                   | —                          |         0.0 |         0.6 |         0.0 |          0.2 |      129.9 |
| D'Andre Swift     | rushing   | run middle (100% failed)                                                        | —                                                                                   | —                          |         0.0 |         0.6 |         0.0 |          0.2 |      129.9 |
| Rome Odunze       | receiving | short_right (100% failed), short_middle (50% failed), deep_middle (100% failed) | short_middle x1.2                                                                   | x0.91                      |         0.0 |         0.1 |         0.0 |          0.0 |       42.6 |
| Roschon Johnson   | rushing   | run inside_right (25% failed)                                                   | —                                                                                   | —                          |         0.0 |         0.0 |        -0.0 |          0.0 |       20.0 |

**ATL defensive weak spots:** play-action dropbacks: 8.8 allowed vs league 6.9 (45 plays); inside runs: 4.4 allowed vs league 3.9 (66 plays).
- ATL struggle: Wk2 vs CAR: +0.21 EPA/play allowed (norm -0.14). Why: deep passes 20.1 yds/play vs 7.4 in other games; WRs 10.0 yds/target vs 6.7 in other games; when blitzing 7.3 yds/dropback vs 5.0 in other games; vs play action 11.8 yds/dropback vs 8.2 in other games
- ATL struggle: Wk5 vs BAL: +0.04 EPA/play allowed (norm -0.10). Why: outside runs 5.4 yds/play vs 1.7 in other games; inside runs 6.7 yds/play vs 3.0 in other games; 7 explosive plays vs 3.5 per other game; short passes 6.3 yds/play vs 4.8 in other games; 3rd/4th downs converted 57% vs 36%
**Offenses like CHI that faced ATL:** BAL (similarity 0.32: -4.2 pass / +2.1 run yds/play vs their norm), CAR (similarity 0.03: -0.2 pass / -0.9 run yds/play vs their norm), GNB (similarity 0.02: -1.7 pass / -1.6 run yds/play vs their norm) → CHI pass x0.96, run x1.07.
**ATL defensive scheme (online/tagged):** blitz: avg, coverage: avg, shell: single_high [online (high)].
- Best matchups: run_outside_left (x1.08), run_inside_left (x1.08); worst: pass_deep_left (x0.90).
- ATL blitzes 30% of dropbacks (league 32%, FTN charting); CHI gains x1.15 as much per dropback vs the blitz as other offenses (79 blitzed dropbacks) -> pass yards x1.00

| player            | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Tyson Bagent      | QB    |     212.20 |      1.28 |            0.33 |      3.05 |      22.49 |      0.00 |         0.00 |      0.00 |         0.15 |
| D'Andre Swift     | RB    |       0.00 |      0.00 |            0.00 |     21.85 |     105.28 |      3.48 |         2.42 |     22.84 |         0.62 |
| Luther Burden III | WR    |       0.00 |      0.00 |            0.00 |      1.89 |       9.31 |      7.44 |         4.61 |     52.85 |         0.30 |
| Kalif Raymond     | WR    |       0.00 |      0.00 |            0.00 |      0.37 |       1.77 |      5.43 |         3.77 |     37.41 |         0.24 |
| Rome Odunze       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.36 |         3.34 |     40.52 |         0.17 |
| Colston Loveland  | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.37 |         3.35 |     35.20 |         0.17 |
| Cole Kmet         | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.91 |         1.20 |     12.34 |         0.10 |
| Roschon Johnson   | RB    |       0.00 |      0.00 |            0.00 |      4.14 |      18.30 |      0.26 |         0.17 |      1.61 |         0.13 |

**CHI kicker**

| player       |   fg_made |   xp_made |   kicking_points |
|:-------------|----------:|----------:|-----------------:|
| Cairo Santos |      1.57 |      2.40 |             7.10 |

**CHI defenders (vs ATL offense)**

| player            |   tackles |   sacks |   def_int |
|:------------------|----------:|--------:|----------:|
| Dillon Thieneman  |      9.76 |    0.00 |      0.34 |
| Devin Bush        |      7.57 |    0.21 |      0.00 |
| Cam Lewis         |      4.86 |    0.00 |      0.00 |
| Tyrique Stevenson |      4.81 |    0.00 |      0.00 |
| Malik Muhammad    |      4.68 |    0.15 |      0.25 |
| T.J. Edwards      |      4.63 |    0.00 |      0.34 |
| Jaylon Johnson    |      4.30 |    0.00 |      0.00 |
| Austin Booker     |      4.16 |    0.82 |      0.00 |

## CLE vs BAL
**Clock:** 10.8 drives each; CLE 5.71 plays/drive at 37.2 s per clock-running play vs BAL 5.66 at 38.0 s → projected possession 50%, 61 plays to 61.
Projected 61 plays, 63% dropbacks, 32.6 pass att, 22.7 runs, 2.9 sacks. QB: Deshaun Watson
**Coaching style:** Red-zone pass rate high: 60% (league 53%); Sack rate high: 10% (league 6%); Shotgun rate high: 81% (league 61%); 3rd-down conversion low: 31% (league 42%); EPA/dropback low: +0.01 (league +0.06); EPA/run low: -0.34 (league -0.09).
**Model game script:** projected 20.1 – 23.3 (margin -3.1) → dropback rate +1.3%.
**Strength of schedule:** own scoring x1.05 (raw stats re-rated against the opponents actually faced).
**Out:** Tylan Wallace (carried from week 5 report: Out (Knee)), Teven Jenkins (carried from week 5 report: Out (Back)), Kalia Davis (carried from week 5 report: Out (Quadricep)), Mike Hall Jr. (carried from week 5 report: Out (Ankle)), Mason Graham (carried from week 5 report: Out (Knee)), Dillon Gabriel (carried from week 5 report: Out (Back)), Carsen Ryan (carried from week 5 report: Out (Calf)).
**Coach angle:** HC Todd Monken (first-year HC, 0 prior seasons); calls own plays (developing play-caller, 4 seasons calling); career run-first (-4.8 pts pass rate vs league, 4 seasons); leans on stars; this season top target share 19%.
**BAL secondary:** DC Jesse Minter, zone-leaning: 3-3-5 nickel base; floods the field with DBs and uses zone to mask individual matchups; big nickel with Kyle Hamilton as hybrid; outside Nate Wiggins / Marlon Humphrey; nickel Kyle Hamilton; weak spot: Humphrey graded 105th of 114 corners by PFF in 2025; [research confidence medium, 2026-10-14].

**What worked last game → this week vs BAL** (failed play types cut, volume moved to what worked; `BAL allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player            | type      | cut (failed last game)                                                                                  | more of                                                                                | BAL allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:------------------|:----------|:--------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Harold Fannin Jr. | receiving | short_right (50% failed), deep_middle (100% failed), deep_right (100% failed)                           | short_right x1.1                                                                       | x0.84                             |        -0.0 |        -0.9 |         0.0 |          0.0 |       34.8 |
| Quinshon Judkins  | rushing   | run outside_right (100% failed), run inside_left (60% failed)                                           | —                                                                                      | —                                 |         0.0 |        -0.2 |         0.0 |         -0.1 |       95.6 |
| Quinshon Judkins  | receiving | short_left (33% failed)                                                                                 | —                                                                                      | —                                 |         0.0 |        -0.2 |         0.0 |         -0.1 |       95.6 |
| Raheim Sanders    | receiving | short_left (100% failed)                                                                                | short_middle x1.2, short_right x1.2, deep_middle x1.2, deep_left x1.2, deep_right x1.2 | x0.84, x0.84, x1.06, x1.06, x1.06 |        -0.0 |         0.3 |        -0.0 |          0.0 |       22.6 |
| Denzel Boston     | receiving | short_middle (100% failed), short_left (50% failed), short_right (50% failed), deep_right (100% failed) | deep_left x1.1                                                                         | x1.06                             |        -0.0 |        -0.3 |         0.0 |          0.0 |       42.5 |
| Isaiah Bond       | receiving | short_left (100% failed), deep_middle (100% failed), deep_left (100% failed)                            | short_right x1.3, deep_right x1.3                                                      | x0.84, x1.06                      |         0.0 |         0.2 |         0.0 |          0.0 |       15.1 |
| Jerry Jeudy       | receiving | short_left (80% failed), deep_left (100% failed)                                                        | short_right x1.1                                                                       | x0.84                             |        -0.0 |        -0.2 |         0.0 |          0.0 |       20.8 |
| Deshaun Watson    | rushing   | run outside_right (100% failed)                                                                         | run outside_left x1.1                                                                  | x1.12                             |         0.0 |         0.0 |        -0.0 |          0.0 |       41.3 |

**BAL defensive weak spots:** deep passes: 15.0 allowed vs league 11.9 (24 plays).
- BAL struggle: Wk2 vs NOR: +0.13 EPA/play allowed (norm -0.10). Why: TEs 14.8 yds/target vs 5.3 in other games; missing starters: Nnamdi Madubuike (DL); 3rd/4th downs converted 59% vs 39% → counted at 50% weight (those starters are available now)
- BAL struggle: Wk3 vs DAL: +0.09 EPA/play allowed (norm -0.08). Why: inside runs 4.9 yds/play vs 3.7 in other games; DAL is a strong offense (+0.14 EPA/play in its other games)
**Offenses like CLE that faced BAL:** TEN (similarity 0.08: +2.0 pass / -1.3 run yds/play vs their norm), DAL (similarity 0.06: -0.5 pass / +1.8 run yds/play vs their norm), IND (similarity 0.04: -1.4 pass / +1.6 run yds/play vs their norm) → CLE pass x1.00, run x1.00.
**BAL defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: two_high [online (high)].
- BAL is soft deep (+0.98 EPA/deep att vs league +0.43); CLE throws deep 17%.
- Best matchups: run_outside_left (x1.12), run_inside_left (x1.12); worst: pass_short_left (x0.84).
- Last game — worked: run_middle, run_inside_right; failed: run_inside_left, run_outside_right.
- BAL blitzes 32% of dropbacks (league 32%, FTN charting); CLE gains x1.24 as much per dropback vs the blitz as other offenses (66 blitzed dropbacks) -> pass yards x1.00
- CLE short plays vs zone heavy coverage defenses: x1.07 vs how other offenses fare (65 plays)
- CLE run plays vs zone heavy coverage defenses: x1.14 vs how other offenses fare (46 plays)
- CLE short plays vs two high shell defenses: x0.77 vs how other offenses fare (55 plays)
- CLE deep-throw rate vs two high shell: x1.27

| player            | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Deshaun Watson    | QB    |     185.09 |      1.04 |            0.52 |      6.16 |      36.93 |      0.00 |         0.00 |      0.00 |         0.19 |
| Quinshon Judkins  | RB    |       0.00 |      0.00 |            0.00 |     16.84 |      72.47 |      4.42 |         3.04 |     22.32 |         0.47 |
| Denzel Boston     | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.57 |         3.87 |     42.12 |         0.23 |
| Harold Fannin Jr. | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.74 |         3.71 |     34.57 |         0.24 |
| KC Concepcion     | WR    |       0.00 |      0.00 |            0.00 |      0.28 |       1.31 |      5.91 |         3.65 |     31.89 |         0.13 |
| Raheim Sanders    | RB    |       0.00 |      0.00 |            0.00 |      2.18 |       9.41 |      2.37 |         1.60 |     12.69 |         0.15 |
| Jerry Jeudy       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.57 |         2.12 |     20.45 |         0.09 |
| Isaiah Bond       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.26 |         1.33 |     14.94 |         0.07 |

**CLE kicker**

| player      |   fg_made |   xp_made |   kicking_points |
|:------------|----------:|----------:|-----------------:|
| Andre Szmyt |      2.19 |      1.77 |             8.34 |

**CLE defenders (vs BAL offense)**

| player                 |   tackles |   sacks |   def_int |
|:-----------------------|----------:|--------:|----------:|
| Carson Schwesinger     |      9.08 |    0.17 |      0.00 |
| Quincy Williams        |      7.71 |    0.00 |      0.00 |
| Denzel Ward            |      5.27 |    0.00 |      0.12 |
| Ronnie Hickman Jr.     |      5.22 |    0.10 |      0.10 |
| Tyson Campbell         |      5.11 |    0.00 |      0.00 |
| Grant Delpit           |      5.09 |    0.10 |      0.12 |
| Myles Harden           |      3.98 |    0.00 |      0.08 |
| Emmanuel McNeil-Warren |      3.84 |    0.00 |      0.00 |

## BAL vs CLE
**Clock:** 10.8 drives each; BAL 5.66 plays/drive at 38.0 s per clock-running play vs CLE 5.71 at 37.2 s → projected possession 50%, 61 plays to 61.
Projected 61 plays, 52% dropbacks, 27.1 pass att, 29.2 runs, 2.2 sacks. QB: Tyler Huntley
**Coaching style:** Neutral-script pass rate low: 54% (league 59%); Red-zone pass rate low: 40% (league 53%); 4th-down go rate low: 13% (league 19%); Pass rate on 2nd & short low: 10% (league 31%); Pass rate on 3rd & short low: 28% (league 41%); Red-zone run share high: 61% (league 46%); EPA/dropback high: +0.20 (league +0.06); EPA/run high: +0.05 (league -0.09).
**Model game script:** projected 23.3 – 20.1 (margin +3.1) → dropback rate -1.3%.
**Strength of schedule:** own run yds x0.97, own scoring x0.96 (raw stats re-rated against the opponents actually faced).
**Out:** Trey Hendrickson (carried from week 5 report: Out (Finger)), Lamar Jackson (carried from week 5 report: Out (Ankle)), Cam Jurgens (carried from week 5 report: Out (Concussion)).
**Coach angle:** HC Jesse Minter (first-year HC, 0 prior seasons); plays called by OC Declan Doyle (first-time play-caller, 0 seasons calling); no prior play-calling seasons: this season's data only; this season top target share 25%.
**CLE secondary:** DC Mike Rutenberg, mixed-leaning: First-year DC from Saleh tree; 73% zone in week 1 then back to 73% man vs PIT (Next Gen Stats); more disguise than Schwartz; outside Denzel Ward / Tyson Campbell; nickel Myles Harden; weak spot: Run fits and zone busts when they leave man; [research confidence medium, 2026-10-14].

**What worked last game → this week vs CLE** (failed play types cut, volume moved to what worked; `CLE allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player         | type      | cut (failed last game)                                                                | more of                                                       | CLE allows there    |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:---------------|:----------|:--------------------------------------------------------------------------------------|:--------------------------------------------------------------|:--------------------|------------:|------------:|------------:|-------------:|-----------:|
| Rashod Bateman | receiving | deep_left (100% failed)                                                               | —                                                             | —                   |         0.0 |        -0.8 |         0.0 |          0.0 |       30.5 |
| Mark Andrews   | receiving | short_left (50% failed), short_right (50% failed), short_middle (50% failed)          | —                                                             | —                   |        -0.0 |        -0.6 |         0.0 |          0.0 |       38.0 |
| Justice Hill   | receiving | deep_left (100% failed), short_right (100% failed)                                    | short_left x1.3                                               | x0.85               |         0.0 |        -0.2 |         0.0 |          0.1 |       32.0 |
| Justice Hill   | rushing   | run inside_right (100% failed)                                                        | run middle x1.1, run outside_right x1.1, run inside_left x1.1 | x1.07, x1.07, x1.07 |         0.0 |        -0.2 |         0.0 |          0.1 |       32.0 |
| Derrick Henry  | receiving | short_middle (100% failed)                                                            | short_left x1.1                                               | x0.85               |         0.0 |         0.2 |        -0.0 |          0.1 |      124.2 |
| Derrick Henry  | rushing   | run middle (40% failed), run outside_left (25% failed), run inside_right (12% failed) | —                                                             | —                   |         0.0 |         0.2 |        -0.0 |          0.1 |      124.2 |
| Zay Flowers    | receiving | short_middle (50% failed)                                                             | —                                                             | —                   |        -0.0 |        -0.3 |        -0.0 |          0.0 |       52.8 |

**CLE defensive weak spots:** explosive plays: 12% allowed vs league 9% (292 plays); outside runs: 7.3 allowed vs league 4.9 (27 plays).
- CLE struggle: Wk1 vs JAX: +0.40 EPA/play allowed (norm -0.09). Why: WRs 13.6 yds/target vs 8.0 in other games; deep passes 16.3 yds/play vs 9.7 in other games; short passes 8.2 yds/play vs 5.3 in other games; 3rd/4th downs converted 62% vs 35%; JAX is a strong offense (+0.10 EPA/play in its other games)
**Offenses like BAL that faced CLE:** JAX (similarity 0.43: +3.1 pass / +0.5 run yds/play vs their norm), TAM (similarity 0.18: -0.5 pass / +0.8 run yds/play vs their norm), NYJ (similarity 0.15: -2.2 pass / +1.2 run yds/play vs their norm) → BAL pass x1.05, run x1.01.
**CLE defensive scheme (online/tagged):** blitz: avg, coverage: man_heavy, shell: single_high [online (high)].
- CLE run defense is soft (+0.01 EPA/run).
- Best matchups: run_outside_left (x1.07), run_inside_left (x1.07); worst: pass_short_left (x0.85).
- Last game — worked: none; failed: pass_short_middle.
- CLE blitzes 25% of dropbacks (league 32%, FTN charting); BAL gains x0.93 as much per dropback vs the blitz as other offenses (56 blitzed dropbacks) -> pass yards x1.00
- BAL short plays vs single high shell defenses: x0.83 vs how other offenses fare (65 plays)
- BAL deep-throw rate vs single high shell: x0.90

| player         | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:---------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Tyler Huntley  | QB    |     183.52 |      1.52 |            0.43 |      3.40 |      23.56 |      0.00 |         0.00 |      0.00 |         0.07 |
| Derrick Henry  | RB    |       0.00 |      0.00 |            0.00 |     24.32 |     112.53 |      1.86 |         1.32 |     12.33 |         0.58 |
| Zay Flowers    | WR    |       0.00 |      0.00 |            0.00 |      0.45 |       2.31 |      6.86 |         4.75 |     50.03 |         0.33 |
| Mark Andrews   | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.04 |         4.16 |     37.95 |         0.31 |
| Rashod Bateman | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.18 |         2.83 |     30.88 |         0.20 |
| Justice Hill   | RB    |       0.00 |      0.00 |            0.00 |      3.48 |      17.42 |      2.27 |         1.57 |     14.26 |         0.15 |

**BAL kicker**

| player     |   fg_made |   xp_made |   kicking_points |
|:-----------|----------:|----------:|-----------------:|
| Tyler Loop |      2.18 |      2.33 |             8.88 |

**BAL defenders (vs CLE offense)**

| player          |   tackles |   sacks |   def_int |
|:----------------|----------:|--------:|----------:|
| Roquan Smith    |      8.11 |    0.28 |      0.10 |
| Kyle Hamilton   |      7.62 |    0.00 |      0.22 |
| Malaki Starks   |      6.83 |    0.21 |      0.00 |
| Trenton Simpson |      6.81 |    0.41 |      0.19 |
| Jaylinn Hawkins |      4.41 |    0.00 |      0.00 |
| Marlon Humphrey |      3.90 |    0.00 |      0.00 |
| Tavius Robinson |      3.21 |    0.83 |      0.00 |
| Nate Wiggins    |      2.81 |    0.00 |      0.00 |

## IND vs TEN
**Clock:** 10.4 drives each; IND 6.05 plays/drive at 38.0 s per clock-running play vs TEN 5.65 at 37.4 s → projected possession 52%, 63 plays to 59.
Projected 63 plays, 53% dropbacks, 30.9 pass att, 29.8 runs, 1.8 sacks. QB: Daniel Jones
**Coaching style:** Red-zone pass rate low: 44% (league 53%); 4th-down go rate high: 28% (league 19%); Sack rate low: 4% (league 6%); Pass rate on 3rd & short low: 29% (league 41%); Red-zone run share high: 55% (league 46%); EPA/dropback low: -0.15 (league +0.06); EPA/run high: +0.10 (league -0.09).
**Model game script:** projected 29.8 – 18.6 (margin +11.2) → dropback rate -4.5%.
**Strength of schedule:** own pass yds x0.97, own run yds x1.04, opp run D x1.03, opp scoring D x1.03 (raw stats re-rated against the opponents actually faced).
**Out:** Arden Key (carried from week 5 report: Out (Hamstring)), Ashton Dulin (carried from week 5 report: Out (Hamstring)), Will Mallory (carried from week 5 report: Out (Thumb)), Jaylon Carlies (carried from week 5 report: Out (Ribs)).
**Coach angle:** HC Shane Steichen (young HC, 3 prior seasons); calls own plays (veteran play-caller, 5 seasons calling); career run-first (-3.3 pts pass rate vs league, 5 seasons); typical; this season top target share 22%.
**TEN secondary:** DC Robert Saleh, zone-leaning: 4-3 wide-9; rushes four with stunts; zone-dominant (Cover 3 / quarters); blitz about 23%; outside Cor'Dale Flott / Alontae Taylor; nickel Marcus Harris; weak spot: Corners struggled in camp; [research confidence medium, 2026-10-14].

**What worked last game → this week vs TEN** (failed play types cut, volume moved to what worked; `TEN allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player                | type      | cut (failed last game)                                                                                  | more of                                                                                 | TEN allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:----------------------|:----------|:--------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Jonathan Taylor       | rushing   | run inside_right (67% failed), run inside_left (17% failed)                                             | —                                                                                       | —                                 |        -0.0 |         1.2 |         0.0 |          0.3 |      134.3 |
| Jonathan Taylor       | receiving | short_left (25% failed)                                                                                 | —                                                                                       | —                                 |        -0.0 |         1.2 |         0.0 |          0.3 |      134.3 |
| Josh Downs            | receiving | short_left (67% failed), deep_middle (100% failed), deep_left (100% failed)                             | short_left x1.1, deep_right x1.2                                                        | x1.01, x0.99                      |        -0.0 |        -1.1 |         0.0 |          0.0 |       41.6 |
| Tyler Warren          | receiving | short_left (33% failed), short_right (50% failed), deep_right (100% failed)                             | short_middle x1.1, deep_left x1.1                                                       | x1.01, x0.99                      |         0.0 |         1.0 |         0.0 |          0.0 |       50.5 |
| Keenan Allen          | receiving | short_middle (33% failed), short_left (25% failed), short_right (100% failed)                           | short_middle x1.1, short_left x1.1                                                      | x1.01, x1.01                      |         0.0 |         0.5 |         0.0 |          0.0 |       32.0 |
| Laquon Treadwell      | receiving | short_middle (100% failed), short_left (100% failed), deep_left (100% failed), deep_right (100% failed) | short_right x1.4                                                                        | x1.01                             |        -0.0 |        -0.2 |         0.0 |          0.0 |       28.6 |
| Deion Burks           | receiving | deep_left (100% failed)                                                                                 | short_middle x1.1, short_left x1.1, short_right x1.1, deep_middle x1.1, deep_right x1.1 | x1.01, x1.01, x1.01, x0.99, x0.99 |        -0.0 |        -0.1 |         0.0 |          0.0 |        7.6 |
| Nick Westbrook-Ikhine | receiving | deep_left (100% failed)                                                                                 | short_middle x1.1, short_left x1.1, short_right x1.1, deep_middle x1.1, deep_right x1.1 | x1.01, x1.01, x1.01, x0.99, x0.99 |         0.0 |        -0.0 |         0.0 |          0.0 |        1.6 |

**TEN defensive weak spots:** deep passes: 14.7 allowed vs league 11.9 (25 plays); vs WRs: 10.1 yds/target (league 8.2), x1.06 for WRs.
- TEN struggle: Wk5 vs HOU: +0.19 EPA/play allowed (norm +0.06). Why: missing starters: Amani Hooker (S), Kevin Winston (S); short passes 7.8 yds/play vs 6.0 in other games → counted at 50% weight (those starters are available now)
**Offenses like IND that faced TEN:** BAL (similarity 0.34: +0.9 pass / -1.8 run yds/play vs their norm), NYG (similarity 0.26: -1.5 pass / +0.6 run yds/play vs their norm), NYJ (similarity 0.18: +3.4 pass / +0.9 run yds/play vs their norm) → IND pass x0.99, run x0.99.
**TEN defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: two_high [online (high)].
- TEN is soft deep (+0.94 EPA/deep att vs league +0.43); IND throws deep 17%.
- Best matchups: run_outside_left (x1.16), run_inside_left (x1.16); worst: pass_deep_left (x0.99).
- Last game — worked: none; failed: pass_deep_left, run_inside_right.
- IND deep plays vs zone heavy coverage defenses: x0.90 vs how other offenses fare (23 plays)
- IND run plays vs two high shell defenses: x1.15 vs how other offenses fare (77 plays)
- IND deep-throw rate vs two high shell: x0.72
- TEN DBs out: Amani Hooker (17 tgts, 8.1 yds/tgt allowed) -> coverage 7.9 → 7.9 yds/tgt; WR yards x1.01

| player           | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-----------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Daniel Jones     | QB    |     185.71 |      1.02 |            0.46 |      2.70 |      14.20 |      0.00 |         0.00 |      0.00 |         0.13 |
| Jonathan Taylor  | RB    |       0.00 |      0.00 |            0.00 |     21.89 |     109.30 |      3.64 |         2.48 |     23.00 |         0.72 |
| Tyler Warren     | TE    |       0.00 |      0.00 |            0.00 |      0.68 |       3.04 |      7.22 |         5.23 |     46.39 |         0.26 |
| Josh Downs       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.92 |         3.91 |     39.17 |         0.15 |
| Keenan Allen     | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.16 |         3.42 |     30.33 |         0.19 |
| Laquon Treadwell | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.00 |         2.68 |     27.00 |         0.12 |
| Seth McGowan     | RB    |       0.00 |      0.00 |            0.00 |      4.69 |      23.19 |      0.88 |         0.61 |      4.92 |         0.19 |

**IND kicker**

| player          |   fg_made |   xp_made |   kicking_points |
|:----------------|----------:|----------:|-----------------:|
| Spencer Shrader |      4.40 |      2.38 |            15.56 |

**IND defenders (vs TEN offense)**

| player              |   tackles |   sacks |   def_int |
|:--------------------|----------:|--------:|----------:|
| Akeem Davis-Gaither |      8.21 |    0.00 |      0.00 |
| Justin Walley       |      5.50 |    0.24 |      0.00 |
| DeForest Buckner    |      4.79 |    0.82 |      0.00 |
| A.J. Haulcy         |      4.01 |    0.00 |      0.00 |
| Camryn Bynum        |      3.72 |    0.00 |      0.00 |
| Bryce Boettcher     |      3.69 |    0.00 |      0.00 |
| Grover Stewart      |      3.61 |    0.07 |      0.00 |
| Charvarius Ward     |      3.31 |    0.00 |      0.00 |

## TEN vs IND
**Clock:** 10.4 drives each; TEN 5.65 plays/drive at 37.4 s per clock-running play vs IND 6.05 at 38.0 s → projected possession 48%, 59 plays to 63.
Projected 59 plays, 66% dropbacks, 34.0 pass att, 20.1 runs, 1.9 sacks. QB: Cam Ward
**Coaching style:** Early-down pass rate low: 49% (league 53%); Deep-pass share low: 16% (league 19%); 3rd-down deep share low: 9% (league 21%); Red-zone pass rate low: 41% (league 53%); Sack rate low: 3% (league 6%); Shotgun rate high: 69% (league 61%); No-huddle rate high: 10% (league 6%); Pass rate on 3rd & short low: 17% (league 41%); Red-zone run share high: 59% (league 46%); 3rd-down conversion low: 34% (league 42%); EPA/dropback low: -0.25 (league +0.06); Favors run inside left (33%).
**Model game script:** projected 18.6 – 29.8 (margin -11.2) → dropback rate +4.5%.
**Strength of schedule:** own scoring x1.02 (raw stats re-rated against the opponents actually faced).
**Out:** Amani Hooker (carried from week 5 report: Out (Concussion)).
**Coach angle:** HC Robert Saleh (new to team, 5 prior seasons); plays called by OC Brian Daboll (veteran play-caller, 6 seasons calling); career balanced (-0.7 pts pass rate vs league, 6 seasons); typical; this season top target share 29%.
**IND secondary:** DC Lou Anarumo, mixed-leaning: Multiple; game-plans corners to the opponent each week; disguise; outside Sauce Gardner / Charvarius Ward; nickel Justin Walley; weak spot: Allowed 1029 yards through two games; Ward and Gardner banged up early; [research confidence low, 2026-10-14].

**What worked last game → this week vs IND** (failed play types cut, volume moved to what worked; `IND allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player            | type      | cut (failed last game)                                                        | more of                                                                                | IND allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:------------------|:----------|:------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Carnell Tate      | receiving | deep_left (100% failed), short_middle (100% failed), deep_right (100% failed) | short_left x1.1, short_right x1.1, deep_middle x1.1                                    | x0.98, x0.98, x0.97               |         0.0 |        -1.6 |         0.0 |          0.0 |       58.9 |
| Elic Ayomanor     | receiving | short_left (100% failed)                                                      | short_right x1.1, deep_left x1.1, deep_middle x1.1, short_middle x1.1, deep_right x1.1 | x0.98, x0.97, x0.97, x0.98, x0.97 |         0.0 |         0.3 |         0.0 |          0.0 |       14.7 |
| Wan'Dale Robinson | receiving | short_middle (100% failed)                                                    | —                                                                                      | —                                 |        -0.0 |        -0.3 |        -0.0 |         -0.0 |       41.5 |
| Daniel Bellinger  | receiving | short_right (100% failed)                                                     | short_left x1.1, deep_left x1.1, deep_middle x1.1, short_middle x1.1, deep_right x1.1  | x0.98, x0.97, x0.97, x0.98, x0.97 |         0.0 |         0.2 |         0.0 |          0.0 |        9.5 |
| Chimere Dike      | receiving | short_left (50% failed)                                                       | —                                                                                      | —                                 |        -0.0 |         0.2 |         0.0 |          0.0 |        8.9 |
| Calvin Ridley     | receiving | deep_right (100% failed)                                                      | short_middle x1.1                                                                      | x0.98                             |        -0.0 |        -0.1 |         0.0 |          0.0 |       12.8 |
| Tyjae Spears      | rushing   | run inside_left (100% failed)                                                 | run inside_right x1.1, run middle x1.1, run outside_right x1.1, run outside_left x1.1  | x1.01, x1.01, x1.01, x1.01        |        -0.0 |         0.1 |        -0.0 |         -0.0 |       31.0 |
| Tyjae Spears      | receiving | short_right (50% failed)                                                      | short_middle x1.1                                                                      | x0.98                             |        -0.0 |         0.1 |        -0.0 |         -0.0 |       31.0 |

**IND defensive weak spots:** vs RBs: 9.1 yds/target (league 5.3), x1.16 for RBs; inside runs: 4.6 allowed vs league 3.9 (90 plays); short passes: 7.0 allowed vs league 6.0 (133 plays); play-action dropbacks: 8.4 allowed vs league 6.9 (47 plays); red-zone TDs per play: 24% allowed vs league 21% (41 plays).
- IND struggle: Wk1 vs BAL: +0.31 EPA/play allowed (norm +0.03). Why: when blitzing 10.7 yds/dropback vs 4.7 in other games; WRs 16.4 yds/target vs 7.9 in other games; short passes 12.0 yds/play vs 6.3 in other games; deep passes 17.1 yds/play vs 11.1 in other games; inside runs 6.0 yds/play vs 4.2 in other games
- IND struggle: Wk2 vs KAN: +0.23 EPA/play allowed (norm +0.05). Why: deep passes 18.2 yds/play vs 11.4 in other games; TEs 8.4 yds/target vs 5.5 in other games; when blitzing 8.6 yds/dropback vs 5.9 in other games; outside runs 7.0 yds/play vs 5.1 in other games; 8 explosive plays vs 4.8 per other game
- IND struggle: Wk5 vs PIT: +0.24 EPA/play allowed (norm +0.05). Why: missing starters: Jaylon Carlies (LB), Arden Key (DE); RBs 14.5 yds/target vs 7.7 in other games; inside runs 7.0 yds/play vs 4.2 in other games; red-zone TD rate per play 50% vs 22%; 3rd/4th downs converted 46% vs 31%
**Offenses like TEN that faced IND:** WAS (similarity 0.33: -0.4 pass / +0.3 run yds/play vs their norm), HOU (similarity 0.04: -2.3 pass / +0.2 run yds/play vs their norm), PIT (similarity 0.04: +1.5 pass / +1.8 run yds/play vs their norm) → TEN pass x0.98, run x1.00.
**IND defensive scheme (online/tagged):** blitz: avg, coverage: avg [online (high)].
- IND run defense is soft (+0.08 EPA/run).
- Best matchups: run_outside_left (x1.01), run_inside_left (x1.01); worst: pass_deep_left (x0.97).
- IND blitzes 20% of dropbacks (league 32%, FTN charting); TEN gains x1.12 as much per dropback vs the blitz as other offenses (33 blitzed dropbacks) -> pass yards x0.99

| player             | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Cam Ward           | QB    |     183.23 |      1.34 |            0.48 |      3.29 |      23.14 |      0.00 |         0.00 |      0.00 |         0.16 |
| Tony Pollard       | RB    |       0.00 |      0.00 |            0.00 |     14.49 |      60.67 |      3.13 |         2.00 |     17.10 |         0.43 |
| Carnell Tate       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      8.64 |         5.39 |     55.26 |         0.24 |
| Wan'Dale Robinson  | WR    |       0.00 |      0.00 |            0.00 |      0.17 |       0.76 |      6.64 |         4.26 |     37.29 |         0.34 |
| Tyjae Spears       | RB    |       0.00 |      0.00 |            0.00 |      3.38 |      13.02 |      2.97 |         1.97 |     16.25 |         0.21 |
| Gunnar Helm        | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.35 |         1.54 |     12.93 |         0.09 |
| Elic Ayomanor      | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.14 |         1.26 |     14.05 |         0.09 |
| Calvin Ridley      | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.90 |         1.14 |     11.58 |         0.08 |
| Daniel Bellinger   | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.62 |         1.03 |      8.61 |         0.07 |
| Nicholas Singleton | RB    |       0.00 |      0.00 |            0.00 |      1.60 |       6.29 |      0.00 |         0.00 |      0.00 |         0.06 |

**TEN kicker**

| player    |   fg_made |   xp_made |   kicking_points |
|:----------|----------:|----------:|-----------------:|
| Joey Slye |      1.12 |      2.04 |             5.40 |

**TEN defenders (vs IND offense)**

| player            |   tackles |   sacks |   def_int |
|:------------------|----------:|--------:|----------:|
| Anthony Hill Jr.  |      8.43 |    0.00 |      0.00 |
| Cody Barton       |      5.42 |    0.00 |      0.00 |
| Jeffery Simmons   |      5.41 |    0.29 |      0.00 |
| Kevin Winston Jr. |      4.96 |    0.00 |      0.00 |
| Amani Hooker      |      4.83 |    0.00 |      0.24 |
| Alontae Taylor    |      4.83 |    0.17 |      0.00 |
| Cedric Gray       |      4.72 |    0.11 |      0.00 |
| Marcus Harris     |      4.23 |    0.10 |      0.23 |

## NWE vs NYJ
**Clock:** 10.6 drives each; NWE 6.00 plays/drive at 37.3 s per clock-running play vs NYJ 5.57 at 37.8 s → projected possession 52%, 63 plays to 59.
Projected 63 plays, 59% dropbacks, 31.3 pass att, 26.0 runs, 2.5 sacks. QB: Drake Maye
**Coaching style:** Deep-pass share high: 24% (league 19%); 3rd-down deep share low: 17% (league 21%); Red-zone pass rate high: 65% (league 53%); No-huddle rate low: 0% (league 6%); Red-zone run share low: 33% (league 46%); EPA/dropback high: +0.23 (league +0.06); Favors run middle (39%).
**Model game script:** projected 20.3 – 17.5 (margin +2.8) → dropback rate -1.1%.
**Out:** Mack Hollins (carried from week 5 report: Out (Calf)), Carlton Davis III (carried from week 5 report: Out (Neck)), Reggie Gilliam (carried from week 5 report: Out (Ankle)), Christian Gonzalez (carried from week 5 report: Out (Shoulder)), Karon Prunty (carried from week 5 report: Out (Hamstring)), Channing Canada (carried from week 5 report: Out (Hamstring)).
**Coach angle:** HC Mike Vrabel (veteran HC, 8 prior seasons); plays called by OC Josh McDaniels (veteran play-caller, 13 seasons calling); career balanced (+0.7 pts pass rate vs league, 13 seasons); typical; this season top target share 15%.
**NYJ secondary:** DC Aaron Glenn, man-leaning: Glenn calls it; multiple fronts; Detroit led the NFL in man rate (41.2%) under him; expected man-heavy but under 40%; outside Azareye'h Thomas / Brandon Stephens; nickel Jarvis Brownlee Jr.; weak spot: Nahshon Wright rotates outside; [research confidence medium, 2026-10-14].

**What worked last game → this week vs NYJ** (failed play types cut, volume moved to what worked; `NYJ allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player              | type      | cut (failed last game)     | more of                             | NYJ allows there   |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:--------------------|:----------|:---------------------------|:------------------------------------|:-------------------|------------:|------------:|------------:|-------------:|-----------:|
| Efton Chism III     | receiving | deep_left (100% failed)    | —                                   | —                  |        -0.0 |        -1.1 |         0.0 |          0.0 |       33.3 |
| Hunter Henry        | receiving | short_left (100% failed)   | short_right x1.1, short_middle x1.1 | x1.14, x1.14       |        -0.0 |        -0.5 |         0.0 |          0.0 |       46.5 |
| Romeo Doubs         | receiving | deep_left (100% failed)    | deep_middle x1.5                    | x0.99              |         0.0 |         0.4 |         0.0 |          0.0 |       58.9 |
| Eli Raridon         | receiving | short_left (33% failed)    | —                                   | —                  |         0.0 |        -0.4 |         0.0 |          0.0 |       21.8 |
| DeMario Douglas     | receiving | deep_left (100% failed)    | —                                   | —                  |         0.0 |        -0.3 |         0.0 |          0.0 |       44.4 |
| Kyle Williams       | receiving | short_middle (100% failed) | deep_right x1.1, deep_left x1.1     | x0.99, x0.99       |         0.0 |         0.3 |         0.0 |          0.0 |       22.1 |
| Corey Kiner         | rushing   | run middle (100% failed)   | run inside_left x1.2                | x0.96              |         0.0 |         0.0 |        -0.0 |          0.1 |        7.2 |
| Rhamondre Stevenson | receiving | short_left (33% failed)    | —                                   | —                  |         0.0 |         0.0 |         0.0 |          0.0 |       97.4 |

**NYJ defensive weak spots:** outside runs: 5.8 allowed vs league 4.9 (24 plays).
- NYJ struggle: Wk3 vs DET: +0.19 EPA/play allowed (norm -0.19). Why: RBs 8.4 yds/target vs 3.0 in other games; deep passes 22.8 yds/play vs 8.4 in other games; vs play action 10.0 yds/dropback vs 3.8 in other games; when blitzing 8.2 yds/dropback vs 4.3 in other games; TEs 8.4 yds/target vs 5.3 in other games
- NYJ struggle: Wk4 vs CHI: +0.06 EPA/play allowed (norm -0.15). Why: outside runs 8.1 yds/play vs 4.5 in other games; 11 explosive plays vs 3.5 per other game; deep passes 16.5 yds/play vs 9.4 in other games; WRs 10.9 yds/target vs 6.3 in other games; RBs 6.8 yds/target vs 4.5 in other games → counted at 50% weight (those starters are available now)
**Offenses like NWE that faced NYJ:** CHI (similarity 0.16: +1.5 pass / +0.2 run yds/play vs their norm), DET (similarity 0.06: +0.4 pass / +0.6 run yds/play vs their norm), GNB (similarity 0.02: -3.1 pass / +0.4 run yds/play vs their norm) → NWE pass x1.03, run x1.00.
**NYJ defensive scheme (online/tagged):** blitz: heavy, coverage: avg, shell: two_high [online (high)].
- NYJ brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed +0.02 on 9 attempts. NWE 3rd-down deep share 17%.
- Best matchups: pass_short_left (x1.14), pass_short_middle (x1.14); worst: run_outside_left (x0.96).
- Last game — worked: pass_short_right, pass_deep_right; failed: pass_deep_left.
- NYJ blitzes 39% of dropbacks (league 32%, FTN charting); NWE gains x1.14 as much per dropback vs the blitz as other offenses (54 blitzed dropbacks) -> pass yards x1.01
- NWE deep plays vs two high shell defenses: x0.93 vs how other offenses fare (27 plays)
- NWE short plays vs two high shell defenses: x1.09 vs how other offenses fare (114 plays)

| player              | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:--------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Drake Maye          | QB    |     267.70 |      1.41 |            0.57 |      4.74 |      31.86 |      0.00 |         0.00 |      0.00 |         0.14 |
| Rhamondre Stevenson | RB    |       0.00 |      0.00 |            0.00 |     13.15 |      53.62 |      4.98 |         3.45 |     42.33 |         0.48 |
| Romeo Doubs         | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.05 |         3.76 |     56.19 |         0.29 |
| Hunter Henry        | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.77 |         3.23 |     43.91 |         0.20 |
| DeMario Douglas     | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.54 |         2.92 |     42.35 |         0.19 |
| TreVeyon Henderson  | RB    |       0.00 |      0.00 |            0.00 |      9.84 |      39.04 |      1.19 |         0.80 |      9.68 |         0.33 |
| Efton Chism III     | WR    |       0.00 |      0.00 |            0.00 |      0.23 |       1.07 |      3.41 |         2.13 |     31.03 |         0.17 |
| Eli Raridon         | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.37 |         1.57 |     20.73 |         0.12 |
| Kyle Williams       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.23 |         1.30 |     21.49 |         0.11 |
| Corey Kiner         | RB    |       0.00 |      0.00 |            0.00 |      1.89 |       7.28 |      0.00 |         0.00 |      0.00 |         0.07 |

**NWE kicker**

| player          |   fg_made |   xp_made |   kicking_points |
|:----------------|----------:|----------:|-----------------:|
| Andy Borregales |      1.13 |      2.38 |             5.77 |

**NWE defenders (vs NYJ offense)**

| player           |   tackles |   sacks |   def_int |
|:-----------------|----------:|--------:|----------:|
| Robert Spillane  |      8.02 |    0.00 |      0.00 |
| Christian Elliss |      7.74 |    0.21 |      0.00 |
| Charles Woods    |      5.22 |    0.00 |      0.00 |
| Elijah Ponder    |      4.84 |    1.31 |      0.00 |
| Marcus Jones     |      4.68 |    0.00 |      0.13 |
| Kevin Byard      |      4.28 |    0.00 |      0.00 |
| Craig Woodson    |      4.06 |    0.00 |      0.16 |
| Gabe Jacas       |      3.76 |    0.29 |      0.10 |

## NYJ vs NWE
**Clock:** 10.6 drives each; NYJ 5.57 plays/drive at 37.8 s per clock-running play vs NWE 6.00 at 37.3 s → projected possession 48%, 59 plays to 63.
Projected 59 plays, 61% dropbacks, 31.7 pass att, 22.8 runs, 2.7 sacks. QB: Geno Smith
**Coaching style:** Deep-pass share low: 16% (league 19%); 4th-down go rate low: 11% (league 19%); Sack rate high: 10% (league 6%); Pass rate on 2nd & short low: 10% (league 31%); EPA/dropback low: -0.02 (league +0.06); Favors run inside left (31%).
**Model game script:** projected 17.5 – 20.3 (margin -2.8) → dropback rate +1.1%.
**Strength of schedule:** opp pass D x0.95, opp scoring D x0.95 (raw stats re-rated against the opponents actually faced).
**Out:** Dylan Parham (carried from week 5 report: Out (Knee)), Breece Hall (carried from week 5 report: Out (Quadricep)), Adonai Mitchell (carried from week 5 report: Out (Finger)), Francisco Mauigoa (carried from week 5 report: Out (Quadricep)).
**Coach angle:** HC Aaron Glenn (young HC, 1 prior seasons); plays called by OC Frank Reich (veteran play-caller, 5 seasons calling); career balanced (-0.9 pts pass rate vs league, 5 seasons); spreads it around; this season top target share 31%.
**NWE secondary:** DC Terrell Williams, man-leaning: Shadow man coverage with Gonzalez when available; outside Carlton Davis III (OUT) / Christian Gonzalez (OUT); nickel Marcus Jones; weak spot: Both starting corners were out in week 5; [research confidence medium, 2026-10-14].

**What worked last game → this week vs NWE** (failed play types cut, volume moved to what worked; `NWE allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player          | type      | cut (failed last game)                                                                                               | more of                                                                               | NWE allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:----------------|:----------|:---------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Kenyon Sadiq    | receiving | short_right (100% failed)                                                                                            | short_left x1.2, deep_left x1.2, short_middle x1.2, deep_right x1.2, deep_middle x1.2 | x1.02, x0.95, x1.02, x0.95, x0.95 |         0.0 |         1.6 |         0.0 |          0.0 |       41.5 |
| Braelon Allen   | receiving | short_right (100% failed)                                                                                            | short_left x1.2, deep_left x1.2, short_middle x1.2, deep_right x1.2, deep_middle x1.2 | x1.02, x0.95, x1.02, x0.95, x0.95 |         0.0 |         0.6 |         0.0 |          0.0 |       97.0 |
| Braelon Allen   | rushing   | run inside_right (22% failed), run middle (33% failed), run inside_left (22% failed), run outside_right (50% failed) | —                                                                                     | —                                 |         0.0 |         0.6 |         0.0 |          0.0 |       97.0 |
| Isaiah Williams | receiving | deep_right (100% failed)                                                                                             | —                                                                                     | —                                 |         0.0 |        -0.2 |         0.0 |          0.0 |       30.2 |
| Jelani Woods    | receiving | short_right (100% failed)                                                                                            | short_left x1.1, deep_left x1.1, short_middle x1.1, deep_right x1.1, deep_middle x1.1 | x1.02, x0.95, x1.02, x0.95, x0.95 |         0.0 |         0.2 |         0.0 |          0.0 |        6.6 |
| Mason Taylor    | receiving | short_right (100% failed)                                                                                            | short_left x1.1, short_middle x1.1                                                    | x1.02, x1.02                      |         0.0 |         0.2 |         0.0 |          0.0 |       10.7 |
| Garrett Wilson  | receiving | short_left (67% failed), short_right (20% failed), deep_right (100% failed)                                          | deep_left x1.1, short_middle x1.1                                                     | x0.95, x1.02                      |         0.0 |        -0.1 |         0.0 |          0.0 |       74.9 |
| Tim Patrick     | receiving | short_right (50% failed)                                                                                             | short_left x1.1                                                                       | x1.02                             |         0.0 |         0.0 |         0.0 |          0.0 |        8.1 |

**NWE defensive weak spots:** play-action dropbacks: 8.0 allowed vs league 6.9 (41 plays).
- NWE struggle: Wk3 vs JAX: +0.22 EPA/play allowed (norm -0.08). Why: outside runs 6.6 yds/play vs 4.3 in other games; missing starters: Craig Woodson (S); 3rd/4th downs converted 70% vs 35%; red-zone TD rate per play 29% vs 14%; JAX is a strong offense (+0.14 EPA/play in its other games) → counted at 50% weight (those starters are available now)
- NWE struggle: Wk4 vs BUF: +0.12 EPA/play allowed (norm -0.05). Why: deep passes 16.1 yds/play vs 9.3 in other games; WRs 10.1 yds/target vs 6.4 in other games; 8 explosive plays vs 3.0 per other game; missing starters: Christian Gonzalez (CB); when blitzing 6.9 yds/dropback vs 4.7 in other games
**Offenses like NYJ that faced NWE:** LVR (similarity 0.44: -0.8 pass / -1.6 run yds/play vs their norm), JAX (similarity 0.24: -1.9 pass / +1.0 run yds/play vs their norm), BUF (similarity 0.08: -1.6 pass / -0.1 run yds/play vs their norm) → NYJ pass x1.00, run x0.98.
**NWE defensive scheme (online/tagged):** blitz: heavy, coverage: avg, shell: two_high [online (high)].
- NWE is soft deep (+0.67 EPA/deep att vs league +0.43); NYJ throws deep 16%.
- NWE brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed +0.48 on 11 attempts. NYJ 3rd-down deep share 19%.
- Best matchups: pass_short_left (x1.02), pass_short_middle (x1.02); worst: run_outside_left (x0.90).
- NWE blitzes 35% of dropbacks (league 32%, FTN charting); NYJ gains x1.15 as much per dropback vs the blitz as other offenses (44 blitzed dropbacks) -> pass yards x1.01
- NYJ short plays vs two high shell defenses: x1.08 vs how other offenses fare (98 plays)
- NYJ run plays vs two high shell defenses: x0.95 vs how other offenses fare (74 plays)
- NYJ deep-throw rate vs two high shell: x1.18
- NWE DBs out: Carlton Davis (18 tgts, 7.7 yds/tgt allowed), Christian Gonzalez (18 tgts, 7.3 yds/tgt allowed) -> coverage 7.8 → 8.1 yds/tgt; WR yards x1.04
- NWE shadow corner Christian Gonzalez is out: no shadow this week

| player          | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:----------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Geno Smith      | QB    |     203.65 |      1.29 |            0.38 |      2.59 |      16.28 |      0.00 |         0.00 |      0.00 |         0.07 |
| Garrett Wilson  | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      9.85 |         6.67 |     71.48 |         0.38 |
| Braelon Allen   | RB    |       0.00 |      0.00 |            0.00 |     20.36 |      76.30 |      3.53 |         2.36 |     19.75 |         0.53 |
| Kenyon Sadiq    | TE    |       0.00 |      0.00 |            0.00 |      0.18 |       0.66 |      6.07 |         3.94 |     39.25 |         0.23 |
| Isaiah Williams | WR    |       0.00 |      0.00 |            0.00 |      0.56 |       2.09 |      3.77 |         2.54 |     26.75 |         0.16 |
| Jeremy Ruckert  | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.93 |         1.36 |     12.78 |         0.09 |
| Mason Taylor    | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.58 |         1.09 |     10.19 |         0.05 |

**NYJ kicker**

| player        |   fg_made |   xp_made |   kicking_points |
|:--------------|----------:|----------:|-----------------:|
| Jason Sanders |      1.24 |      1.92 |             5.62 |

**NYJ defenders (vs NWE offense)**

| player             |   tackles |   sacks |   def_int |
|:-------------------|----------:|--------:|----------:|
| Dane Belton        |      7.93 |    0.17 |      0.00 |
| Jamien Sherwood    |      7.23 |    0.00 |      0.00 |
| Demario Davis      |      7.12 |    0.29 |      0.00 |
| David Bailey       |      5.30 |    0.75 |      0.00 |
| Minkah Fitzpatrick |      5.04 |    0.00 |      0.57 |
| Azareye'h Thomas   |      3.89 |    0.00 |      0.00 |
| Jowon Briggs       |      3.36 |    0.28 |      0.00 |
| Andre Cisco        |      3.28 |    0.13 |      0.00 |

## NYG vs NOR
**Clock:** 10.7 drives each; NYG 5.99 plays/drive at 38.1 s per clock-running play vs NOR 5.96 at 34.0 s → projected possession 53%, 64 plays to 64.
Projected 64 plays, 57% dropbacks, 32.7 pass att, 27.4 runs, 2.3 sacks. QB: Jameis Winston
**Coaching style:** Neutral-script pass rate low: 55% (league 59%); Early-down pass rate low: 45% (league 53%); Deep-pass share high: 22% (league 19%); 3rd-down deep share high: 25% (league 21%); 4th-down go rate low: 11% (league 19%); Pass rate on 3rd & short low: 0% (league 41%); 3rd-down conversion high: 47% (league 42%); EPA/dropback high: +0.13 (league +0.06); EPA/run low: -0.23 (league -0.09); Favors run inside left (33%).
**Model game script:** projected 26.4 – 20.3 (margin +6.1) → dropback rate -2.5%.
**Strength of schedule:** own pass yds x0.93, own scoring x0.93, opp scoring D x0.97 (raw stats re-rated against the opponents actually faced).
**Out:** Jason Pinnock (carried from week 5 report: Out (Concussion)), Chauncey Golston (carried from week 5 report: Out (Neck)).
**Coach angle:** HC John Harbaugh (new to team, 18 prior seasons); plays called by OC Matt Nagy (developing play-caller, 3 seasons calling); career balanced (+1.2 pts pass rate vs league, 3 seasons); leans on stars; this season top target share 31%.
**NOR secondary:** DC Brandon Staley, zone-leaning: Zone-heavy off coverage; light box; two-high safety shells; outside Kool-Aid McKinstry / Quincy Riley; nickel Jonas Sanker; weak spot: Safety Jonas Sanker covering slot receivers and tight ends after Alontae Taylor left; [research confidence medium, 2026-10-14].

**What worked last game → this week vs NOR** (failed play types cut, volume moved to what worked; `NOR allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player         | type      | cut (failed last game)                                                                                                           | more of                             | NOR allows there   |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:---------------|:----------|:---------------------------------------------------------------------------------------------------------------------------------|:------------------------------------|:-------------------|------------:|------------:|------------:|-------------:|-----------:|
| Isaiah Likely  | receiving | short_left (33% failed), deep_right (100% failed), deep_middle (100% failed)                                                     | short_middle x1.1, short_right x1.1 | x0.91, x0.91       |         0.0 |        -2.5 |         0.0 |          0.0 |       60.1 |
| Malik Nabers   | receiving | short_left (67% failed), short_middle (67% failed), short_right (43% failed), deep_left (50% failed), deep_right (100% failed)   | deep_middle x1.1                    | x1.01              |         0.0 |        -0.4 |         0.0 |          0.0 |       60.4 |
| Darnell Mooney | receiving | short_left (100% failed), short_right (50% failed), deep_left (100% failed), deep_right (100% failed), deep_middle (100% failed) | short_right x1.5                    | x0.91              |        -0.0 |        -0.3 |        -0.0 |         -0.0 |       24.6 |
| Najee Harris   | rushing   | run inside_left (50% failed), run outside_left (50% failed)                                                                      | run middle x1.1                     | x1.02              |        -0.0 |        -0.1 |        -0.0 |         -0.1 |       27.7 |
| Cam Skattebo   | receiving | short_left (33% failed)                                                                                                          | —                                   | —                  |         0.0 |         0.0 |        -0.0 |          0.1 |       88.3 |
| Cam Skattebo   | rushing   | run inside_right (50% failed), run middle (17% failed)                                                                           | —                                   | —                  |         0.0 |         0.0 |        -0.0 |          0.1 |       88.3 |
| Theo Johnson   | receiving | short_right (100% failed)                                                                                                        | short_left x1.1, short_middle x1.1  | x0.91, x0.91       |         0.0 |         0.1 |         0.0 |          0.0 |       11.4 |
| J.J. McCarthy  | rushing   | run middle (100% failed)                                                                                                         | run outside_right x1.3              | x1.02              |         0.0 |         0.0 |        -0.0 |          0.0 |        2.2 |

**NOR defensive weak spots:** 3rd-down conversions: 53% allowed vs league 42% (58 plays); inside runs: 4.5 allowed vs league 3.9 (100 plays); outside runs: 6.1 allowed vs league 4.9 (30 plays).
- NOR struggle: Wk4 vs ATL: +0.40 EPA/play allowed (norm +0.04). Why: vs play action 16.6 yds/dropback vs 5.0 in other games; outside runs 11.1 yds/play vs 4.3 in other games; missing starters: Kaden Elliss (LB), Carl Granderson (DE); WRs 13.3 yds/target vs 7.3 in other games; when blitzing 9.9 yds/dropback vs 5.8 in other games → counted at 50% weight (those starters are available now)
**Offenses like NYG that faced NOR:** LVR (similarity 0.37: -0.4 pass / +1.9 run yds/play vs their norm), BAL (similarity 0.27: -2.3 pass / -0.9 run yds/play vs their norm), DET (similarity 0.26: -2.2 pass / +1.0 run yds/play vs their norm) → NYG pass x0.97, run x1.00.
**NOR defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: single_high [online (high)].
- NOR is soft deep (+0.79 EPA/deep att vs league +0.43); NYG throws deep 22%.
- NOR brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed +0.35 on 9 attempts. NYG 3rd-down deep share 25%.
- Best matchups: run_outside_left (x1.02), run_inside_left (x1.02); worst: pass_short_left (x0.91).
- Last game — worked: none; failed: pass_deep_right.
- NOR blitzes 35% of dropbacks (league 32%, FTN charting); NYG gains x0.79 as much per dropback vs the blitz as other offenses (61 blitzed dropbacks) -> pass yards x0.99
- NYG deep plays vs zone heavy coverage defenses: x1.05 vs how other offenses fare (23 plays)

| player         | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:---------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Jameis Winston | QB    |     196.02 |      1.74 |            0.36 |      1.81 |      12.75 |      0.00 |         0.00 |      0.00 |         0.07 |
| Isaiah Likely  | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |     10.00 |         6.71 |     58.95 |         0.49 |
| Cam Skattebo   | RB    |       0.00 |      0.00 |            0.00 |     18.15 |      73.20 |      2.50 |         1.70 |     13.78 |         0.51 |
| Malik Nabers   | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      9.38 |         5.93 |     59.19 |         0.37 |
| Darnell Mooney | WR    |       0.00 |      0.00 |            0.00 |      0.17 |       0.69 |      3.68 |         2.28 |     23.37 |         0.14 |
| Najee Harris   | RB    |       0.00 |      0.00 |            0.00 |      6.62 |      26.33 |      0.27 |         0.18 |      1.53 |         0.24 |
| Malachi Fields | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.70 |         1.75 |     18.43 |         0.13 |
| Theo Johnson   | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.88 |         1.19 |     11.37 |         0.12 |

**NYG kicker**

| player        |   fg_made |   xp_made |   kicking_points |
|:--------------|----------:|----------:|-----------------:|
| Dominic Zvada |      2.33 |      2.69 |             9.67 |

**NYG defenders (vs NOR offense)**

| player           |   tackles |   sacks |   def_int |
|:-----------------|----------:|--------:|----------:|
| Arvell Reese     |      9.60 |    0.34 |      0.27 |
| Tremaine Edmunds |      9.07 |    0.62 |      0.00 |
| Greg Newsome II  |      4.86 |    0.00 |      0.27 |
| Jevon Holland    |      4.46 |    0.00 |      0.59 |
| Andru Phillips   |      4.27 |    0.66 |      0.00 |
| Tyler Nubin      |      4.03 |    0.00 |      0.00 |
| Deonte Banks     |      3.34 |    0.00 |      0.28 |
| Abdul Carter     |      3.19 |    0.54 |      0.00 |

## NOR vs NYG
**Clock:** 10.7 drives each; NOR 5.96 plays/drive at 34.0 s per clock-running play vs NYG 5.99 at 38.1 s → projected possession 47%, 64 plays to 64.
Projected 64 plays, 67% dropbacks, 39.3 pass att, 21.0 runs, 2.4 sacks. QB: Tyler Shough
**Coaching style:** 3rd-down deep share high: 27% (league 21%); 4th-down go rate high: 34% (league 19%); No-huddle rate high: 15% (league 6%); Pass rate on 3rd & short low: 28% (league 41%); 3rd-down conversion high: 48% (league 42%); EPA/dropback low: -0.07 (league +0.06); EPA/run low: -0.17 (league -0.09); Favors run middle (40%).
**Model game script:** projected 20.3 – 26.4 (margin -6.1) → dropback rate +2.5%.
**Strength of schedule:** opp pass D x1.02, opp scoring D x1.03 (raw stats re-rated against the opponents actually faced).
**Out:** Kaden Elliss (carried from week 5 report: Out (Calf)), Anfernee Jennings (carried from week 5 report: Out (Knee)), Jeremiah Wright (carried from week 5 report: Out (Concussion)).
**Coach angle:** HC Kellen Moore (young HC, 1 prior seasons); calls own plays (veteran play-caller, 7 seasons calling); career balanced (-0.1 pts pass rate vs league, 7 seasons); typical; this season top target share 28%.
**NYG secondary:** DC Dennard Wilson, coverage lean unknown: New DC Wilson; physical press-oriented coverage approach; outside Deonte Banks / Greg Newsome II; nickel Dru Phillips; weak spot: Adebo reported on IR; Banks' coverage grade 73.3 (15th); [research confidence low, 2026-10-14].

**What worked last game → this week vs NYG** (failed play types cut, volume moved to what worked; `NYG allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player        | type      | cut (failed last game)                                   | more of                                                                               | NYG allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:--------------|:----------|:---------------------------------------------------------|:--------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Bryce Lance   | receiving | short_right (100% failed), short_left (100% failed)      | short_middle x1.5, deep_middle x1.5, deep_left x1.5, deep_right x1.5                  | x0.96, x0.96, x0.96, x0.96        |         0.0 |         2.0 |         0.0 |          0.0 |       25.0 |
| Chris Olave   | receiving | short_middle (33% failed), deep_left (100% failed)       | —                                                                                     | —                                 |         0.0 |        -0.9 |         0.0 |          0.0 |       73.2 |
| Alvin Kamara  | receiving | short_right (100% failed)                                | short_left x1.1, short_middle x1.1, deep_middle x1.1, deep_left x1.1, deep_right x1.1 | x0.96, x0.96, x0.96, x0.96, x0.96 |         0.0 |         0.7 |         0.0 |          0.0 |       51.4 |
| Devaughn Vele | receiving | short_left (40% failed), deep_left (100% failed)         | —                                                                                     | —                                 |         0.0 |        -0.4 |         0.0 |          0.0 |       46.7 |
| Juwan Johnson | receiving | short_right (67% failed), short_middle (100% failed)     | short_left x1.1                                                                       | x0.96                             |         0.0 |        -0.1 |         0.0 |          0.0 |       46.3 |
| Kendre Miller | rushing   | run middle (67% failed), run outside_right (100% failed) | run inside_left x1.1, run inside_right x1.1                                           | x1.15, x1.15                      |         0.0 |         0.0 |         0.0 |          0.1 |       47.3 |
| CJ Donaldson  | rushing   | run inside_right (100% failed)                           | run middle x1.1                                                                       | x1.15                             |         0.0 |         0.0 |         0.0 |         -0.0 |       12.7 |

**NYG defensive weak spots:** outside runs: 6.1 allowed vs league 4.9 (21 plays); inside runs: 4.3 allowed vs league 3.9 (81 plays).
- NYG struggle: Wk1 vs DAL: +0.22 EPA/play allowed (norm -0.01). Why: when blitzing 8.2 yds/dropback vs 4.6 in other games; 3rd/4th downs converted 73% vs 39%; red-zone TD rate per play 33% vs 21%; DAL is a strong offense (+0.11 EPA/play in its other games)
- NYG struggle: Wk2 vs LAR: +0.27 EPA/play allowed (norm -0.02). Why: deep passes 19.0 yds/play vs 3.0 in other games; WRs 15.1 yds/target vs 6.2 in other games; 10 explosive plays vs 3.0 per other game; missing starters: Deonte Banks (CB); inside runs 5.6 yds/play vs 4.0 in other games → counted at 50% weight (those starters are available now)
**Offenses like NOR that faced NYG:** DAL (similarity 0.27: -1.9 pass / -0.1 run yds/play vs their norm), ARI (similarity 0.26: -1.2 pass / +1.8 run yds/play vs their norm), TEN (similarity 0.24: +0.0 pass / +0.2 run yds/play vs their norm) → NOR pass x0.96, run x0.98.
**NYG defensive scheme (online/tagged):** blitz: heavy, coverage: avg, shell: two_high [online (high)].
- NYG brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed +0.03 on 7 attempts. NOR 3rd-down deep share 27%.
- Best matchups: run_outside_left (x1.15), run_inside_left (x1.15); worst: pass_deep_left (x0.96).
- NYG blitzes 40% of dropbacks (league 32%, FTN charting); NOR gains x0.86 as much per dropback vs the blitz as other offenses (72 blitzed dropbacks) -> pass yards x0.99
- NOR deep plays vs two high shell defenses: x1.06 vs how other offenses fare (22 plays)
- NOR run plays vs two high shell defenses: x1.08 vs how other offenses fare (91 plays)
- NOR deep-throw rate vs two high shell: x0.89

| player        | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:--------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Tyler Shough  | QB    |     237.96 |      1.86 |            1.42 |      2.50 |      12.97 |      0.00 |         0.00 |      0.00 |         0.10 |
| Chris Olave   | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |     10.19 |         6.98 |     70.93 |         0.32 |
| Juwan Johnson | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      7.05 |         5.04 |     44.48 |         0.39 |
| Devaughn Vele | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      7.24 |         4.85 |     45.88 |         0.27 |
| Alvin Kamara  | RB    |       0.00 |      0.00 |            0.00 |      7.32 |      29.39 |      3.92 |         2.78 |     21.79 |         0.33 |
| Kendre Miller | RB    |       0.00 |      0.00 |            0.00 |      9.39 |      38.69 |      1.58 |         1.09 |      8.41 |         0.36 |
| Bryce Lance   | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.79 |         2.18 |     23.83 |         0.14 |
| Noah Fant     | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.69 |         1.89 |     15.45 |         0.21 |
| CJ Donaldson  | RB    |       0.00 |      0.00 |            0.00 |      2.31 |       8.98 |      0.59 |         0.40 |      3.37 |         0.10 |

**NOR kicker**

| player         |   fg_made |   xp_made |   kicking_points |
|:---------------|----------:|----------:|-----------------:|
| Daniel Carlson |      0.63 |      2.43 |             4.32 |

**NOR defenders (vs NYG offense)**

| player             |   tackles |   sacks |   def_int |
|:-------------------|----------:|--------:|----------:|
| Pete Werner        |      6.89 |    0.18 |      0.00 |
| Jonas Sanker       |      6.52 |    0.00 |      0.00 |
| Danny Stutsman     |      6.41 |    0.00 |      0.00 |
| Justin Reid        |      6.01 |    0.00 |      0.00 |
| Julian Blackmon    |      5.40 |    0.00 |      0.36 |
| Kool-Aid McKinstry |      3.96 |    0.00 |      0.00 |
| Carl Granderson    |      3.22 |    0.63 |      0.00 |
| Quincy Riley       |      2.96 |    0.00 |      0.00 |

## PHI vs CAR
**Clock:** 10.7 drives each; PHI 5.69 plays/drive at 37.4 s per clock-running play vs CAR 6.02 at 36.3 s → projected possession 49%, 61 plays to 64.
Projected 61 plays, 64% dropbacks, 34.6 pass att, 21.7 runs, 2.3 sacks. QB: Jalen Hurts
**Coaching style:** Deep-pass share low: 16% (league 19%); Red-zone pass rate low: 38% (league 53%); No-huddle rate high: 11% (league 6%); Pass rate on 3rd & short high: 55% (league 41%); Red-zone run share high: 61% (league 46%); 3rd-down conversion low: 33% (league 42%); EPA/dropback low: -0.09 (league +0.06); EPA/run low: -0.24 (league -0.09).
**Model game script:** projected 21.0 – 23.5 (margin -2.5) → dropback rate +1.0%.
**Offensive line:** starters out: Cam Jurgens, Drew Kendall → sack rate x1.01, yds/dropback x0.98, yds/carry x1.01 (measured effect per missing starter).
**Strength of schedule:** own pass yds x0.96, own run yds x1.04, own scoring x1.02 (raw stats re-rated against the opponents actually faced).
**Out:** Saquon Barkley (carried from week 5 report: Out (Hamstring)), Marcus Epps (carried from week 5 report: Out (Groin)), Marquise Brown (carried from week 5 report: Out (Ankle)), DeVonta Smith (carried from week 5 report: Out (Hamstring)), Drew Kendall (carried from week 5 report: Out (Knee)).
**Coach angle:** HC Nick Sirianni (veteran HC, 5 prior seasons); plays called by OC Sean Mannion (first-time play-caller, 0 seasons calling); no prior play-calling seasons: this season's data only; this season top target share 20%.
**CAR secondary:** DC Ejiro Evero, zone-leaning: 3-4 base; zone-heavy two-high shells and disguise; soft zone that rarely plays man (2025 description); outside Akayleb Evans / Will Lee III; nickel Chau Smith-Wade; weak spot: Passive off coverage when Horn is out; [research confidence low, 2026-10-14].

**What worked last game → this week vs CAR** (failed play types cut, volume moved to what worked; `CAR allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player           | type      | cut (failed last game)                                                                                                | more of                                                                               | CAR allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:-----------------|:----------|:----------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Makai Lemon      | receiving | short_right (67% failed), short_left (50% failed)                                                                     | short_middle x1.1                                                                     | x1.09                             |        -0.0 |         0.7 |         0.0 |          0.0 |       41.5 |
| Dallas Goedert   | receiving | short_right (67% failed), short_left (67% failed), short_middle (33% failed)                                          | —                                                                                     | —                                 |        -0.0 |        -0.5 |         0.0 |          0.0 |       33.4 |
| Johnny Mundt     | receiving | short_right (100% failed)                                                                                             | short_left x1.4, short_middle x1.4, deep_right x1.4, deep_left x1.4, deep_middle x1.4 | x1.09, x1.09, x1.00, x1.00, x1.00 |        -0.0 |         0.5 |         0.0 |          0.0 |        9.4 |
| Dameon Pierce    | rushing   | run outside_left (67% failed), run outside_right (100% failed), run middle (50% failed), run inside_left (40% failed) | —                                                                                     | —                                 |        -0.0 |        -0.4 |         0.0 |         -0.1 |       29.9 |
| Dameon Pierce    | receiving | short_right (50% failed), short_left (100% failed)                                                                    | short_right x1.2                                                                      | x1.09                             |        -0.0 |        -0.4 |         0.0 |         -0.1 |       29.9 |
| Dontayvion Wicks | receiving | short_right (50% failed), deep_left (67% failed)                                                                      | short_left x1.1                                                                       | x1.09                             |        -0.0 |        -0.4 |         0.0 |          0.0 |       57.7 |
| Will Shipley     | rushing   | run inside_right (100% failed)                                                                                        | run middle x1.1, run inside_left x1.1                                                 | x1.08, x1.08                      |         0.0 |        -0.2 |         0.0 |          0.2 |       42.9 |
| Will Shipley     | receiving | short_left (100% failed)                                                                                              | short_right x1.1                                                                      | x1.09                             |         0.0 |        -0.2 |         0.0 |          0.2 |       42.9 |

**CAR defensive weak spots:** inside runs: 5.4 allowed vs league 3.9 (78 plays).
- CAR struggle: Wk1 vs CHI: +0.41 EPA/play allowed (norm -0.16). Why: inside runs 8.1 yds/play vs 4.0 in other games; missing starters: Patrick Jones II (LB), Zakee Wheatley (S); WRs 11.1 yds/target vs 7.7 in other games; 8 explosive plays vs 3.7 per other game; 3rd/4th downs converted 67% vs 36% → counted at 50% weight (those starters are available now)
- CAR struggle: Wk4 vs DET: +0.18 EPA/play allowed (norm -0.08). Why: vs play action 10.5 yds/dropback vs 4.8 in other games; missing starters: Jaycee Horn (CB), Michael Jackson (CB); WRs 10.4 yds/target vs 7.4 in other games; short passes 6.7 yds/play vs 5.3 in other games; DET is a strong offense (+0.17 EPA/play in its other games) → counted at 50% weight (those starters are available now)
**Offenses like PHI that faced CAR:** CLE (similarity 0.16: -1.0 pass / +1.0 run yds/play vs their norm), DET (similarity 0.08: +1.1 pass / -1.6 run yds/play vs their norm), CHI (similarity 0.05: +2.8 pass / +3.4 run yds/play vs their norm) → PHI pass x1.00, run x1.00.
**CAR defensive scheme (online/tagged):** blitz: heavy, coverage: zone_heavy [online (high)].
- CAR is soft deep (+0.54 EPA/deep att vs league +0.43); PHI throws deep 16%.
- CAR brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed -0.29 on 3 attempts. PHI 3rd-down deep share 19%.
- Best matchups: pass_short_left (x1.09), pass_short_middle (x1.09); worst: pass_other (x1.00).
- CAR blitzes 32% of dropbacks (league 32%, FTN charting); PHI gains x0.79 as much per dropback vs the blitz as other offenses (68 blitzed dropbacks) -> pass yards x1.00
- PHI short plays vs zone heavy coverage defenses: x1.13 vs how other offenses fare (62 plays)
- PHI deep-throw rate vs zone heavy coverage: x1.21

| player           | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-----------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Jalen Hurts      | QB    |     202.95 |      1.53 |            0.72 |      4.04 |      23.49 |      0.00 |         0.00 |      0.00 |         0.18 |
| Dontayvion Wicks | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      7.69 |         4.61 |     52.87 |         0.27 |
| Makai Lemon      | WR    |       0.00 |      0.00 |            0.00 |      0.19 |       0.88 |      6.24 |         4.01 |     37.97 |         0.20 |
| Will Shipley     | RB    |       0.00 |      0.00 |            0.00 |      6.53 |      28.27 |      2.37 |         1.48 |     13.38 |         0.33 |
| Dallas Goedert   | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.84 |         3.02 |     30.98 |         0.25 |
| Tank Bigsby      | RB    |       0.00 |      0.00 |            0.00 |      8.52 |      36.47 |      1.17 |         0.75 |      6.24 |         0.36 |
| Darius Cooper    | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.81 |         2.22 |     26.50 |         0.29 |
| Dameon Pierce    | RB    |       0.00 |      0.00 |            0.00 |      4.30 |      18.46 |      1.96 |         1.21 |     10.15 |         0.22 |
| Zach Ertz        | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.47 |         1.48 |     16.17 |         0.09 |

**PHI kicker**

| player       |   fg_made |   xp_made |   kicking_points |
|:-------------|----------:|----------:|-----------------:|
| Jake Elliott |      0.99 |      2.49 |             5.47 |

**PHI defenders (vs CAR offense)**

| player               |   tackles |   sacks |   def_int |
|:---------------------|----------:|--------:|----------:|
| Jihaad Campbell      |      7.43 |    0.25 |      0.00 |
| Zack Baun            |      6.59 |    0.00 |      0.00 |
| Cooper DeJean        |      6.27 |    0.00 |      0.20 |
| Quinyon Mitchell     |      4.59 |    0.00 |      0.23 |
| Riq Woolen           |      4.47 |    0.00 |      0.00 |
| Andrew Mukuba        |      4.30 |    0.00 |      0.19 |
| Jeremiah Trotter Jr. |      3.74 |    0.00 |      0.00 |
| Jordan Davis         |      3.33 |    0.00 |      0.00 |

## CAR vs PHI
**Clock:** 10.7 drives each; CAR 6.02 plays/drive at 36.3 s per clock-running play vs PHI 5.69 at 37.4 s → projected possession 51%, 64 plays to 61.
Projected 64 plays, 64% dropbacks, 37.9 pass att, 23.3 runs, 2.3 sacks. QB: Bryce Young
**Coaching style:** Neutral-script pass rate high: 65% (league 59%); Early-down pass rate high: 61% (league 53%); 3rd-down deep share low: 16% (league 21%); Red-zone pass rate high: 69% (league 53%); 4th-down go rate high: 27% (league 19%); Red-zone run share low: 30% (league 46%); EPA/dropback high: +0.20 (league +0.06); Favors run inside left (32%).
**Model game script:** projected 23.5 – 21.0 (margin +2.5) → dropback rate -1.0%.
**Strength of schedule:** opp pass D x0.97 (raw stats re-rated against the opponents actually faced).
**Coach angle:** HC Dave Canales (young HC, 2 prior seasons); calls own plays (developing play-caller, 3 seasons calling); career balanced (-0.9 pts pass rate vs league, 3 seasons); leans on stars; this season top target share 27%.
**PHI secondary:** DC Vic Fangio, zone-leaning: Fangio two-high quarters / match zone; DeJean at safety in base and slot in nickel; outside Riq Woolen / Quinyon Mitchell; nickel Cooper DeJean; [research confidence medium, 2026-10-14].

**What worked last game → this week vs PHI** (failed play types cut, volume moved to what worked; `PHI allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player            | type      | cut (failed last game)                                                               | more of                                                                               | PHI allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:------------------|:----------|:-------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Tommy Tremble     | receiving | short_left (50% failed)                                                              | —                                                                                     | —                                 |         0.0 |         1.8 |         0.0 |          0.0 |       35.8 |
| Tetairoa McMillan | receiving | short_left (33% failed), deep_left (100% failed)                                     | —                                                                                     | —                                 |        -0.0 |         1.4 |         0.0 |          0.0 |       86.6 |
| Brycen Tremayne   | receiving | short_right (100% failed)                                                            | short_left x1.1, deep_middle x1.1                                                     | x1.19, x0.92                      |         0.0 |         0.8 |         0.0 |          0.0 |       24.3 |
| Chuba Hubbard     | rushing   | run inside_right (17% failed), run inside_left (17% failed), run middle (17% failed) | —                                                                                     | —                                 |         0.0 |         0.5 |         0.0 |          0.1 |      114.4 |
| Chuba Hubbard     | receiving | short_right (100% failed)                                                            | short_middle x1.3                                                                     | x1.19                             |         0.0 |         0.5 |         0.0 |          0.1 |      114.4 |
| Darren Waller     | receiving | short_right (75% failed)                                                             | short_middle x1.1, short_left x1.1                                                    | x1.19, x1.19                      |         0.0 |         0.3 |         0.0 |          0.0 |       47.2 |
| Ja'Seem Reed      | receiving | short_right (100% failed)                                                            | short_middle x1.3, deep_right x1.3, short_left x1.3, deep_left x1.3, deep_middle x1.3 | x1.19, x0.92, x1.19, x0.92, x0.92 |         0.0 |         0.1 |         0.0 |          0.0 |        2.8 |
| John Metchie III  | receiving | short_middle (33% failed), short_left (100% failed)                                  | short_middle x1.1, short_right x1.2                                                   | x1.19, x1.19                      |         0.0 |         0.1 |         0.0 |          0.0 |       25.8 |

**Offenses like CAR that faced PHI:** TEN (similarity 0.15: +2.8 pass / +0.8 run yds/play vs their norm), LAR (similarity 0.15: -1.7 pass / -0.4 run yds/play vs their norm), WAS (similarity 0.11: -1.2 pass / -0.4 run yds/play vs their norm) → CAR pass x1.00, run x1.01.
**PHI defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: two_high [online (high)].
- Best matchups: pass_short_left (x1.19), pass_short_middle (x1.19); worst: pass_deep_left (x0.92).
- Last game — worked: pass_deep_right; failed: none.
- CAR short plays vs zone heavy coverage defenses: x1.12 vs how other offenses fare (39 plays)
- CAR run plays vs zone heavy coverage defenses: x1.06 vs how other offenses fare (25 plays)
- CAR short plays vs two high shell defenses: x1.11 vs how other offenses fare (39 plays)
- CAR run plays vs two high shell defenses: x1.06 vs how other offenses fare (25 plays)
- PHI DBs out: Marcus Epps (7 tgts, 8.1 yds/tgt allowed) -> coverage 7.8 → 7.8 yds/tgt; WR yards x1.00

| player            | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Bryce Young       | QB    |     284.79 |      1.40 |            0.62 |      0.72 |       5.49 |      0.00 |         0.00 |      0.00 |         0.05 |
| Chuba Hubbard     | RB    |       0.00 |      0.00 |            0.00 |     19.55 |      92.87 |      2.65 |         1.76 |     20.32 |         0.65 |
| Tetairoa McMillan | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      9.37 |         5.75 |     79.88 |         0.32 |
| Darren Waller     | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.44 |         3.48 |     43.44 |         0.24 |
| Jalen Coker       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.58 |         2.91 |     38.66 |         0.15 |
| Tommy Tremble     | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.11 |         2.64 |     32.91 |         0.11 |
| John Metchie III  | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.02 |         1.88 |     23.52 |         0.12 |
| Brycen Tremayne   | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.45 |         1.48 |     21.59 |         0.08 |
| AJ Dillon         | RB    |       0.00 |      0.00 |            0.00 |      3.74 |      16.43 |      0.65 |         0.43 |      4.76 |         0.14 |
| Mitchell Evans    | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.64 |         1.07 |     13.29 |         0.06 |

**CAR kicker**

| player          |   fg_made |   xp_made |   kicking_points |
|:----------------|----------:|----------:|-----------------:|
| Ryan Fitzgerald |      2.08 |      2.22 |             8.46 |

**CAR defenders (vs PHI offense)**

| player              |   tackles |   sacks |   def_int |
|:--------------------|----------:|--------:|----------:|
| Devin Lloyd         |      8.17 |    0.31 |      0.48 |
| Bobby Okereke       |      7.20 |    0.00 |      0.23 |
| Akayleb Evans       |      5.86 |    0.00 |      0.00 |
| Will Lee III        |      5.11 |    0.00 |      0.00 |
| Lathan Ransom       |      5.11 |    0.00 |      0.00 |
| Tre'von Moehrig     |      4.88 |    0.00 |      0.00 |
| Zakee Wheatley      |      4.21 |    0.00 |      0.00 |
| Princely Umanmielen |      3.12 |    1.05 |      0.00 |

## TAM vs PIT
**Clock:** 10.7 drives each; TAM 5.61 plays/drive at 38.2 s per clock-running play vs PIT 5.53 at 38.9 s → projected possession 50%, 60 plays to 59.
Projected 60 plays, 61% dropbacks, 29.6 pass att, 23.5 runs, 2.5 sacks. QB: Jalon Daniels
**Coaching style:** Sack rate high: 9% (league 6%); Pass rate on 3rd & short high: 61% (league 41%); EPA/dropback low: -0.10 (league +0.06); EPA/run high: +0.01 (league -0.09); Favors run inside right (32%).
**Model game script:** projected 20.6 – 22.2 (margin -1.6) → dropback rate +0.6%.
**Weather:** forecast 78°F, wind 18 mph, rain/snow → pass yds x0.92, long FG x1.01.
**Strength of schedule:** own run yds x0.96, own scoring x1.02, opp pass D x1.03 (raw stats re-rated against the opponents actually faced).
**Out:** Baker Mayfield (carried from week 5 report: Out (Thumb)), Antoine Winfield Jr. (carried from week 5 report: Out (Rib)), SirVocea Dennis (carried from week 5 report: Out (Ankle)), Benjamin Morrison (carried from week 5 report: Out (Quadricep)).
**Coach angle:** HC Todd Bowles (veteran HC, 11 prior seasons); plays called by OC Zac Robinson (developing play-caller, 2 seasons calling); career run-first (-2.5 pts pass rate vs league, 2 seasons); leans on stars; this season top target share 24%.
**PIT secondary:** DC Patrick Graham, zone-leaning: Game-plans week to week; zero man snaps reported in week 1; Ramsey used as the slot Star and in pressure packages; outside Asante Samuel Jr. / Jamel Dean (OUT); nickel Jalen Ramsey; weak spot: Joey Porter Jr. traded to DAL (reported); new corners not yet in sync per Ramsey; [research confidence low, 2026-10-14].

**What worked last game → this week vs PIT** (failed play types cut, volume moved to what worked; `PIT allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player         | type      | cut (failed last game)                                                    | more of          | PIT allows there   |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:---------------|:----------|:--------------------------------------------------------------------------|:-----------------|:-------------------|------------:|------------:|------------:|-------------:|-----------:|
| Cade Otton     | receiving | short_right (33% failed)                                                  | —                | —                  |         0.0 |        -1.9 |         0.0 |          0.0 |       35.5 |
| Kenny Gainwell | receiving | short_left (100% failed), short_right (67% failed)                        | short_right x1.1 | x0.94              |         0.0 |        -0.1 |         0.0 |          0.0 |       30.8 |
| Emeka Egbuka   | receiving | deep_left (50% failed), short_left (33% failed), short_right (75% failed) | —                | —                  |        -0.0 |        -0.1 |        -0.0 |          0.0 |       46.5 |
| Bucky Irving   | receiving | short_right (33% failed)                                                  | —                | —                  |         0.0 |         0.0 |        -0.0 |         -0.1 |       77.2 |
| Bucky Irving   | rushing   | run inside_left (29% failed)                                              | —                | —                  |         0.0 |         0.0 |        -0.0 |         -0.1 |       77.2 |
| Sean Tucker    | rushing   | run middle (50% failed)                                                   | —                | —                  |         0.0 |         0.0 |         0.0 |          0.0 |        6.9 |

**PIT defensive weak spots:** explosive plays: 11% allowed vs league 9% (276 plays); outside runs: 6.7 allowed vs league 4.9 (20 plays).
- PIT struggle: Wk3 vs CIN: +0.28 EPA/play allowed (norm -0.07). Why: deep passes 18.5 yds/play vs 12.4 in other games; 3rd/4th downs converted 57% vs 31%; red-zone TD rate per play 25% vs 15%
- PIT struggle: Wk4 vs CLE: +0.10 EPA/play allowed (norm -0.03). Why: outside runs 9.2 yds/play vs 6.0 in other games; WRs 10.1 yds/target vs 7.6 in other games; when blitzing 11.4 yds/dropback vs 8.7 in other games; red-zone TD rate per play 29% vs 12%
**Offenses like TAM that faced PIT:** IND (similarity 0.15: +1.1 pass / -1.4 run yds/play vs their norm), NWE (similarity 0.09: +0.4 pass / +1.6 run yds/play vs their norm), CLE (similarity 0.09: +3.0 pass / +0.8 run yds/play vs their norm) → TAM pass x1.01, run x1.00.
**PIT defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy [online (high)].
- Best matchups: pass_other (x1.00), pass_short_left (x0.94); worst: run_outside_left (x0.84).
- PIT blitzes 27% of dropbacks (league 32%, FTN charting); TAM gains x0.87 as much per dropback vs the blitz as other offenses (71 blitzed dropbacks) -> pass yards x1.01
- TAM deep plays vs zone heavy coverage defenses: x0.94 vs how other offenses fare (9 plays)
- TAM run plays vs zone heavy coverage defenses: x0.85 vs how other offenses fare (43 plays)
- TAM deep-throw rate vs zone heavy coverage: x0.90
- PIT DBs out: Jamel Dean (18 tgts, 7.9 yds/tgt allowed) -> coverage 7.8 → 7.9 yds/tgt; WR yards x1.01

| player           | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-----------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Jalon Daniels    | QB    |     178.30 |      1.02 |            0.74 |      4.42 |      33.54 |      0.00 |         0.00 |      0.00 |         0.17 |
| Bucky Irving     | RB    |       0.00 |      0.00 |            0.00 |     16.73 |      58.85 |      3.32 |         2.33 |     18.08 |         0.49 |
| Emeka Egbuka     | WR    |       0.00 |      0.00 |            0.00 |      0.34 |       1.21 |      7.02 |         4.60 |     44.20 |         0.23 |
| Cade Otton       | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.35 |         3.60 |     34.12 |         0.14 |
| Chris Godwin Jr. | WR    |       0.00 |      0.00 |            0.00 |      0.53 |       1.95 |      4.36 |         3.08 |     27.71 |         0.14 |
| Kenny Gainwell   | RB    |       0.00 |      0.00 |            0.00 |      3.53 |      11.41 |      3.52 |         2.35 |     18.82 |         0.22 |
| Ted Hurst III    | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.51 |         1.53 |     17.98 |         0.10 |
| Tez Johnson      | WR    |       0.00 |      0.00 |            0.00 |      0.25 |       0.94 |      1.74 |         1.06 |     11.97 |         0.07 |
| Sean Tucker      | RB    |       0.00 |      0.00 |            0.00 |      2.03 |       6.77 |      0.00 |         0.00 |      0.00 |         0.09 |

**TAM kicker**

| player           |   fg_made |   xp_made |   kicking_points |
|:-----------------|----------:|----------:|-----------------:|
| Chase McLaughlin |      2.29 |      1.89 |             8.75 |

**TAM defenders (vs PIT offense)**

| player               |   tackles |   sacks |   def_int |
|:---------------------|----------:|--------:|----------:|
| Josiah Trotter       |      7.98 |    0.31 |      0.13 |
| Alex Anzalone        |      5.25 |    0.43 |      0.26 |
| Keionte Scott        |      5.17 |    0.00 |      0.00 |
| Jacob Parrish        |      5.09 |    0.00 |      0.22 |
| Tykee Smith          |      4.97 |    0.00 |      0.00 |
| Antoine Winfield Jr. |      4.38 |    0.00 |      0.00 |
| A'Shawn Robinson     |      2.94 |    0.37 |      0.18 |
| Zyon McCollum        |      2.69 |    0.00 |      0.00 |

## PIT vs TAM
**Clock:** 10.7 drives each; PIT 5.53 plays/drive at 38.9 s per clock-running play vs TAM 5.61 at 38.2 s → projected possession 50%, 59 plays to 60.
Projected 59 plays, 66% dropbacks, 36.0 pass att, 20.0 runs, 2.3 sacks. QB: Aaron Rodgers
**Coaching style:** Neutral-script pass rate high: 68% (league 59%); Early-down pass rate high: 64% (league 53%); 3rd-down deep share high: 29% (league 21%); Red-zone pass rate high: 76% (league 53%); Red-zone run share low: 24% (league 46%); EPA/dropback low: -0.05 (league +0.06); EPA/run high: +0.11 (league -0.09).
**Model game script:** projected 22.2 – 20.6 (margin +1.6) → dropback rate -0.6%.
**Weather:** forecast 78°F, wind 18 mph, rain/snow → pass yds x0.92, long FG x1.01.
**Strength of schedule:** own pass yds x1.03, own run yds x0.97, opp run D x1.03 (raw stats re-rated against the opponents actually faced).
**Out:** DeShon Elliott (carried from week 5 report: Out (Knee)), Jamel Dean (carried from week 5 report: Out (Ankle)), Michael Pittman (carried from week 5 report: Out (Foot)).
**Coach angle:** HC Mike McCarthy (new to team, 20 prior seasons); calls own plays (veteran play-caller, 15 seasons calling); career pass-first (+3.4 pts pass rate vs league, 15 seasons); typical; this season top target share 20%.
**TAM secondary:** DC Todd Bowles, mixed-leaning: Among the highest blitz rates; man 22.8% / zone 71.9% through five games (unverified figure); outside Zyon McCollum / Benjamin Morrison (OUT); nickel Jacob Parrish; weak spot: No edge rush to support the blitz; [research confidence medium, 2026-10-14].

**What worked last game → this week vs TAM** (failed play types cut, volume moved to what worked; `TAM allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player             | type      | cut (failed last game)                                                       | more of                                                                               | TAM allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:-------------------|:----------|:-----------------------------------------------------------------------------|:--------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| DK Metcalf         | receiving | short_left (50% failed), short_middle (100% failed)                          | short_right x1.1                                                                      | x0.78                             |        -0.0 |        -1.7 |         0.0 |          0.0 |       56.4 |
| Jaylen Warren      | receiving | short_left (50% failed), short_right (25% failed)                            | —                                                                                     | —                                 |         0.0 |        -1.1 |         0.0 |         -0.2 |      103.5 |
| Jaylen Warren      | rushing   | run inside_left (33% failed), run outside_right (100% failed)                | —                                                                                     | —                                 |         0.0 |        -1.1 |         0.0 |         -0.2 |      103.5 |
| Roman Wilson       | receiving | short_right (100% failed)                                                    | deep_left x1.1, short_left x1.1, short_middle x1.1, deep_middle x1.1, deep_right x1.1 | x1.01, x0.78, x0.78, x1.01, x1.01 |         0.0 |         1.0 |         0.0 |          0.0 |       35.5 |
| Pat Freiermuth     | receiving | deep_right (100% failed)                                                     | —                                                                                     | —                                 |         0.0 |        -0.8 |         0.0 |          0.0 |       42.7 |
| Germie Bernard     | receiving | short_left (33% failed), short_right (50% failed), short_middle (67% failed) | deep_right x1.1                                                                       | x1.01                             |        -0.0 |         0.5 |         0.0 |          0.0 |       35.9 |
| Darnell Washington | receiving | short_left (100% failed)                                                     | short_right x1.1, short_middle x1.1                                                   | x0.78, x0.78                      |        -0.0 |         0.0 |         0.0 |          0.0 |       23.4 |

**TAM defensive weak spots:** short passes: 6.6 allowed vs league 6.0 (137 plays).
**Offenses like PIT that faced TAM:** DAL (similarity 0.22: +1.0 pass / +0.4 run yds/play vs their norm), GNB (similarity 0.21: -0.2 pass / +1.6 run yds/play vs their norm), CIN (similarity 0.12: +0.4 pass / +0.7 run yds/play vs their norm) → PIT pass x1.00, run x1.02.
**TAM defensive scheme (online/tagged):** blitz: heavy, coverage: avg, shell: single_high [online (high)].
- TAM brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed -0.59 on 12 attempts. PIT 3rd-down deep share 29%.
- Best matchups: pass_deep_left (x1.01), pass_deep_middle (x1.01); worst: pass_short_left (x0.78).
- TAM blitzes 42% of dropbacks (league 32%, FTN charting); PIT gains x0.77 as much per dropback vs the blitz as other offenses (52 blitzed dropbacks) -> pass yards x0.98
- PIT deep plays vs single high shell defenses: x1.14 vs how other offenses fare (23 plays)
- PIT short plays vs single high shell defenses: x0.86 vs how other offenses fare (65 plays)
- PIT run plays vs single high shell defenses: x0.89 vs how other offenses fare (37 plays)
- PIT deep-throw rate vs single high shell: x1.12
- TAM DBs out: Benjamin Morrison (17 tgts, 7.6 yds/tgt allowed), Antoine Winfield Jr. (7 tgts, 7.9 yds/tgt allowed) -> coverage 7.7 → 7.9 yds/tgt; WR yards x1.02

| player             | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Aaron Rodgers      | QB    |     217.19 |      1.71 |            1.06 |      0.80 |       6.12 |      0.00 |         0.00 |      0.00 |         0.02 |
| Jaylen Warren      | RB    |       0.00 |      0.00 |            0.00 |     16.95 |      69.60 |      6.01 |         4.05 |     32.75 |         0.47 |
| DK Metcalf         | WR    |       0.00 |      0.00 |            0.00 |      0.30 |       1.24 |      7.87 |         4.77 |     51.92 |         0.27 |
| Pat Freiermuth     | TE    |       0.00 |      0.00 |            0.00 |      0.73 |       2.60 |      5.73 |         3.82 |     37.76 |         0.38 |
| Roman Wilson       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.75 |         2.86 |     33.70 |         0.25 |
| Germie Bernard     | WR    |       0.00 |      0.00 |            0.00 |      0.28 |       1.17 |      4.93 |         3.12 |     32.47 |         0.16 |
| Darnell Washington | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.66 |         2.37 |     21.58 |         0.16 |

**PIT kicker**

| player        |   fg_made |   xp_made |   kicking_points |
|:--------------|----------:|----------:|-----------------:|
| Chris Boswell |      2.20 |      2.09 |             8.69 |

**PIT defenders (vs TAM offense)**

| player                 |   tackles |   sacks |   def_int |
|:-----------------------|----------:|--------:|----------:|
| Payton Wilson          |      9.08 |    0.30 |      0.00 |
| Patrick Queen          |      7.14 |    0.00 |      0.18 |
| Jaquan Brisker         |      7.13 |    0.00 |      0.16 |
| Jalen Ramsey           |      5.85 |    0.00 |      0.00 |
| Cameron Heyward        |      3.65 |    0.34 |      0.00 |
| Robert Spears-Jennings |      3.29 |    0.00 |      0.25 |
| Asante Samuel Jr.      |      3.23 |    0.00 |      0.00 |
| Yahya Black            |      3.13 |    0.00 |      0.00 |

## LAR vs ARI
**Clock:** 10.3 drives each; LAR 5.97 plays/drive at 38.0 s per clock-running play vs ARI 5.81 at 38.1 s → projected possession 51%, 61 plays to 60.
Projected 61 plays, 59% dropbacks, 33.8 pass att, 24.9 runs, 1.8 sacks. QB: Matthew Stafford
**Coaching style:** Neutral-script pass rate high: 65% (league 59%); Early-down pass rate high: 61% (league 53%); Red-zone pass rate high: 60% (league 53%); 4th-down go rate high: 26% (league 19%); Sack rate low: 3% (league 6%); No-huddle rate high: 11% (league 6%); Pass rate on 2nd & short high: 57% (league 31%); 3rd-down conversion high: 50% (league 42%); EPA/dropback high: +0.16 (league +0.06); EPA/run high: -0.00 (league -0.09); Favors run middle (40%).
**Model game script:** projected 35.3 – 20.7 (margin +14.6) → dropback rate -5.8%.
**Coach angle:** HC Sean McVay (veteran HC, 9 prior seasons); calls own plays (veteran play-caller, 9 seasons calling); career balanced (+1.2 pts pass rate vs league, 9 seasons); typical; this season top target share 24%.
**ARI secondary:** DC Nick Rallis, coverage lean unknown: Heavy dime user (about 20% dime in 2025); young corners protected with structure and safety rotation; outside Garrett Williams / Denzel Burke; nickel Max Melton; weak spot: Young outside corners starting while Will Johnson is out; [research confidence low, 2026-10-14].

**What worked last game → this week vs ARI** (failed play types cut, volume moved to what worked; `ARI allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player          | type      | cut (failed last game)                                                                                  | more of                            | ARI allows there   |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:----------------|:----------|:--------------------------------------------------------------------------------------------------------|:-----------------------------------|:-------------------|------------:|------------:|------------:|-------------:|-----------:|
| Puka Nacua      | rushing   | run outside_left (50% failed)                                                                           | —                                  | —                  |         0.0 |        -0.9 |         0.0 |          0.0 |       71.3 |
| Puka Nacua      | receiving | deep_right (67% failed), short_right (25% failed), deep_middle (100% failed), short_middle (40% failed) | short_left x1.1                    | x1.04              |         0.0 |        -0.9 |         0.0 |          0.0 |       71.3 |
| Davante Adams   | receiving | deep_left (100% failed), short_right (100% failed)                                                      | short_left x1.1, short_middle x1.1 | x1.04, x1.04       |        -0.0 |         0.5 |         0.0 |          0.0 |       59.0 |
| Tyler Higbee    | receiving | short_right (25% failed)                                                                                | —                                  | —                  |         0.0 |        -0.2 |         0.0 |          0.0 |       37.6 |
| Kyren Williams  | rushing   | run middle (25% failed), run inside_right (50% failed)                                                  | —                                  | —                  |         0.0 |        -0.1 |         0.0 |          0.1 |      113.7 |
| Kyren Williams  | receiving | short_right (67% failed), deep_middle (100% failed)                                                     | short_middle x1.1                  | x1.04              |         0.0 |        -0.1 |         0.0 |          0.1 |      113.7 |
| Blake Corum     | receiving | short_left (33% failed)                                                                                 | —                                  | —                  |         0.0 |         0.1 |         0.0 |          0.0 |       47.4 |
| Colby Parkinson | receiving | short_middle (100% failed)                                                                              | short_left x1.1                    | x1.04              |         0.0 |        -0.0 |         0.0 |          0.0 |        8.0 |

**ARI defensive weak spots:** explosive plays: 12% allowed vs league 9% (260 plays); short passes: 7.4 allowed vs league 6.0 (106 plays); deep passes: 15.8 allowed vs league 11.9 (28 plays); play-action dropbacks: 8.3 allowed vs league 6.9 (40 plays).
- ARI struggle: Wk3 vs SFO: +0.49 EPA/play allowed (norm +0.03). Why: when blitzing 22.4 yds/dropback vs 4.9 in other games; WRs 17.4 yds/target vs 9.1 in other games; short passes 10.0 yds/play vs 6.7 in other games; inside runs 5.3 yds/play vs 3.7 in other games; 9 explosive plays vs 5.5 per other game
- ARI struggle: Wk5 vs DET: +0.32 EPA/play allowed (norm +0.07). Why: RBs 9.3 yds/target vs 4.0 in other games; TEs 16.0 yds/target vs 8.5 in other games; when blitzing 11.7 yds/dropback vs 7.1 in other games; missing starters: Andrew Wingard (S); DET is a strong offense (+0.14 EPA/play in its other games)
**Offenses like LAR that faced ARI:** DET (similarity 0.14: +0.9 pass / +1.3 run yds/play vs their norm), NYG (similarity 0.09: +1.8 pass / -0.5 run yds/play vs their norm), SFO (similarity 0.01: +3.7 pass / +0.8 run yds/play vs their norm) → LAR pass x0.99, run x1.01.
**ARI defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: cover4 [online (low)].
- ARI is soft deep (+1.13 EPA/deep att vs league +0.43); LAR throws deep 22%.
- Best matchups: pass_short_left (x1.04), pass_short_middle (x1.04); worst: run_outside_left (x0.97).
- Last game — worked: none; failed: pass_deep_middle, pass_deep_right.
- ARI blitzes 25% of dropbacks (league 32%, FTN charting); LAR gains x0.91 as much per dropback vs the blitz as other offenses (64 blitzed dropbacks) -> pass yards x1.01
- LAR deep plays vs zone heavy coverage defenses: x0.93 vs how other offenses fare (25 plays)
- LAR run plays vs zone heavy coverage defenses: x0.94 vs how other offenses fare (66 plays)
- ARI DBs out: Andrew Wingard (8 tgts, 8.0 yds/tgt allowed) -> coverage 7.9 → 7.9 yds/tgt; WR yards x1.00

| player           | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-----------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Matthew Stafford | QB    |     263.03 |      3.25 |            0.80 |      0.96 |       6.38 |      0.00 |         0.00 |      0.00 |         0.04 |
| Kyren Williams   | RB    |       0.00 |      0.00 |            0.00 |     16.22 |      69.03 |      6.00 |         4.11 |     43.05 |         0.77 |
| Puka Nacua       | WR    |       0.00 |      0.00 |            0.00 |      0.68 |       3.11 |      8.23 |         5.52 |     66.42 |         0.49 |
| Davante Adams    | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.59 |         4.25 |     58.42 |         0.57 |
| Tyler Higbee     | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.59 |         3.09 |     37.03 |         0.34 |
| Blake Corum      | RB    |       0.00 |      0.00 |            0.00 |      7.69 |      31.97 |      2.08 |         1.37 |     15.44 |         0.38 |
| Konata Mumpfield | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.91 |         1.12 |     16.26 |         0.18 |

**LAR kicker**

| player         |   fg_made |   xp_made |   kicking_points |
|:---------------|----------:|----------:|-----------------:|
| Harrison Mevis |      1.02 |      4.27 |             7.34 |

**LAR defenders (vs ARI offense)**

| player          |   tackles |   sacks |   def_int |
|:----------------|----------:|--------:|----------:|
| Nate Landman    |      9.02 |    0.00 |      0.00 |
| Quentin Lake    |      6.97 |    0.00 |      0.21 |
| Kam Curl        |      4.95 |    0.00 |      0.00 |
| Omar Speights   |      4.65 |    0.60 |      0.00 |
| Kamren Kinchens |      4.38 |    0.16 |      0.00 |
| Byron Young     |      4.11 |    1.08 |      0.00 |
| Kobie Turner    |      3.73 |    0.00 |      0.00 |
| Trent McDuffie  |      3.23 |    0.00 |      0.26 |

## ARI vs LAR
**Clock:** 10.3 drives each; ARI 5.81 plays/drive at 38.1 s per clock-running play vs LAR 5.97 at 38.0 s → projected possession 49%, 60 plays to 61.
Projected 60 plays, 70% dropbacks, 38.4 pass att, 17.9 runs, 2.5 sacks. QB: Jacoby Brissett
**Coaching style:** Red-zone pass rate high: 64% (league 53%); No-huddle rate high: 11% (league 6%); Pass rate on 2nd & short high: 52% (league 31%); Red-zone run share low: 38% (league 46%); EPA/dropback low: -0.02 (league +0.06); Favors run middle (37%).
**Model game script:** projected 20.7 – 35.3 (margin -14.6) → dropback rate +5.8%.
**Strength of schedule:** own pass yds x1.04 (raw stats re-rated against the opponents actually faced).
**Out:** Andrew Wingard (carried from week 5 report: Out (Knee)), Isaiah Adams (carried from week 5 report: Out (Ankle)).
**Coach angle:** HC Mike LaFleur (first-year HC, 0 prior seasons); calls own plays (developing play-caller, 2 seasons calling); career pass-first (+3.9 pts pass rate vs league, 2 seasons); spreads it around; this season top target share 29%.
**LAR secondary:** DC Chris Shula, zone-leaning: Zone lean (more Cover 3 than Cover 1); most dime in the NFL the last two seasons; McDuffie in man only 25.7% vs SF; outside Jaylen Watson / Trent McDuffie; nickel Quentin Lake; weak spot: Scheme may move toward more man under Jimmy Lake; [research confidence medium, 2026-10-14].

**What worked last game → this week vs LAR** (failed play types cut, volume moved to what worked; `LAR allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player          | type      | cut (failed last game)                                                                       | more of                                                                                | LAR allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:----------------|:----------|:---------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Trey McBride    | receiving | deep_right (100% failed)                                                                     | —                                                                                      | —                                 |         0.0 |        -0.8 |         0.0 |          0.0 |       63.4 |
| Michael Wilson  | receiving | deep_right (100% failed), short_right (67% failed), deep_left (50% failed)                   | short_left x1.1                                                                        | x0.92                             |         0.0 |        -0.5 |         0.0 |          0.0 |       58.9 |
| Jeremiyah Love  | receiving | short_left (100% failed)                                                                     | deep_right x1.1, short_middle x1.1, short_right x1.1, deep_left x1.1, deep_middle x1.1 | x0.89, x0.92, x0.92, x0.89, x0.89 |        -0.0 |         0.2 |         0.0 |         -0.2 |       54.5 |
| Jeremiyah Love  | rushing   | run inside_right (50% failed), run inside_left (100% failed), run outside_right (67% failed) | run middle x1.1                                                                        | x0.99                             |        -0.0 |         0.2 |         0.0 |         -0.2 |       54.5 |
| Jalen Brooks    | receiving | deep_right (100% failed), short_middle (100% failed), deep_left (100% failed)                | short_right x1.2, short_left x1.2, deep_middle x1.2                                    | x0.92, x0.92, x0.89               |         0.0 |        -0.3 |         0.0 |          0.0 |        7.9 |
| Kendrick Bourne | receiving | deep_right (100% failed), short_middle (50% failed)                                          | short_left x1.1, deep_left x1.1                                                        | x0.92, x0.89                      |         0.0 |        -0.2 |         0.0 |          0.0 |       24.9 |
| Reggie Virgil   | receiving | short_right (100% failed)                                                                    | deep_right x1.4, short_middle x1.4, short_left x1.4, deep_left x1.4, deep_middle x1.4  | x0.89, x0.92, x0.92, x0.89, x0.89 |         0.0 |         0.1 |         0.0 |          0.0 |        1.8 |

**LAR defensive weak spots:** vs RBs: 6.9 yds/target (league 5.3), x1.19 for RBs.
- LAR struggle: Wk1 vs SFO: +0.21 EPA/play allowed (norm -0.12). Why: outside runs 7.5 yds/play vs 2.3 in other games; TEs 4.4 yds/target vs 2.2 in other games; inside runs 5.1 yds/play vs 3.6 in other games; 3rd/4th downs converted 60% vs 28%; SFO is a strong offense (+0.25 EPA/play in its other games)
- LAR struggle: Wk5 vs BUF: +0.28 EPA/play allowed (norm -0.14). Why: RBs 18.3 yds/target vs 4.1 in other games; when blitzing 14.4 yds/dropback vs 3.3 in other games; short passes 13.8 yds/play vs 4.5 in other games; vs play action 11.3 yds/dropback vs 4.5 in other games; WRs 12.4 yds/target vs 6.6 in other games
**Offenses like ARI that faced LAR:** PHI (similarity 0.43: -3.4 pass / -0.0 run yds/play vs their norm), DEN (similarity 0.23: -0.5 pass / -1.0 run yds/play vs their norm), NYG (similarity 0.19: -2.4 pass / -1.7 run yds/play vs their norm) → ARI pass x0.96, run x0.98.
**LAR defensive scheme (online/tagged):** blitz: avg, coverage: avg, shell: two_high [online (high)].
- Best matchups: pass_other (x1.00), run_outside_left (x0.99); worst: pass_deep_left (x0.89).
- Last game — worked: pass_short_left, run_middle; failed: pass_deep_right, run_outside_right.
- LAR blitzes 34% of dropbacks (league 32%, FTN charting); ARI gains x0.89 as much per dropback vs the blitz as other offenses (58 blitzed dropbacks) -> pass yards x1.00

| player              | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:--------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Jacoby Brissett     | QB    |     216.71 |      1.84 |            1.20 |      2.38 |      11.99 |      0.33 |         0.22 |      1.51 |         0.11 |
| Trey McBride        | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |     11.35 |         7.52 |     62.56 |         0.41 |
| Michael Wilson      | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      9.93 |         6.02 |     58.05 |         0.37 |
| Jeremiyah Love      | RB    |       0.00 |      0.00 |            0.00 |     10.45 |      39.69 |      2.79 |         1.85 |     13.96 |         0.35 |
| Tyler Allgeier      | RB    |       0.00 |      0.00 |            0.00 |      5.83 |      22.15 |      2.40 |         1.64 |     11.96 |         0.27 |
| Kendrick Bourne     | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.79 |         2.52 |     24.45 |         0.14 |
| Marvin Harrison Jr. | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.50 |         1.49 |     15.57 |         0.13 |
| Elijah Higgins      | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.08 |         1.37 |     13.08 |         0.12 |

**ARI kicker**

| player      |   fg_made |   xp_made |   kicking_points |
|:------------|----------:|----------:|-----------------:|
| Chad Ryland |      1.55 |      2.30 |             6.96 |

**ARI defenders (vs LAR offense)**

| player         |   tackles |   sacks |   def_int |
|:---------------|----------:|--------:|----------:|
| Budda Baker    |      8.09 |    0.40 |      0.32 |
| Mack Wilson    |      7.59 |    0.00 |      0.00 |
| Jack Gibbens   |      7.24 |    0.05 |      0.00 |
| Roy Lopez      |      4.59 |    0.21 |      0.00 |
| Andrew Wingard |      4.37 |    0.00 |      0.19 |
| Denzel Burke   |      3.51 |    0.00 |      0.32 |
| Max Melton     |      3.42 |    0.00 |      0.00 |
| Zaven Collins  |      3.33 |    0.18 |      0.00 |

## KAN vs LAC
**Clock:** 11.1 drives each; KAN 5.52 plays/drive at 37.3 s per clock-running play vs LAC 5.64 at 37.0 s → projected possession 50%, 61 plays to 63.
Projected 61 plays, 57% dropbacks, 30.9 pass att, 26.6 runs, 1.9 sacks. QB: Patrick Mahomes
**Coaching style:** Early-down pass rate high: 58% (league 53%); 3rd-down deep share high: 37% (league 21%); Red-zone pass rate high: 60% (league 53%); 4th-down go rate high: 26% (league 19%); Sack rate low: 4% (league 6%); No-huddle rate low: 0% (league 6%); EPA/dropback high: +0.22 (league +0.06); EPA/run high: +0.11 (league -0.09); Favors run middle (38%).
**Model game script:** projected 25.1 – 17.2 (margin +7.9) → dropback rate -3.2%.
**Strength of schedule:** own pass yds x0.97, own run yds x0.97, own scoring x0.98, opp scoring D x0.97 (raw stats re-rated against the opponents actually faced).
**Coach angle:** HC Andy Reid (veteran HC, 27 prior seasons); calls own plays (veteran play-caller, 13 seasons calling); career pass-first (+3.1 pts pass rate vs league, 13 seasons); typical; this season top target share 19%.
**LAC secondary:** DC Chris O'Leary, coverage lean unknown: First-year DC; more five- and six-man fronts at Western Michigan; outside Cam Hart / Donte Jackson (OUT); nickel Tarheeb Still; weak spot: Hart inconsistent; depth charts disagree on sides; [research confidence low, 2026-10-14].

**What worked last game → this week vs LAC** (failed play types cut, volume moved to what worked; `LAC allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player             | type      | cut (failed last game)                                                               | more of                                                                                    | LAC allows there           |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:-------------------|:----------|:-------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------|:---------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Kenneth Walker III | rushing   | run inside_left (20% failed), run middle (17% failed), run inside_right (29% failed) | —                                                                                          | —                          |         0.0 |         0.4 |         0.0 |          0.1 |      129.8 |
| Travis Kelce       | receiving | short_left (50% failed), short_middle (50% failed)                                   | —                                                                                          | —                          |         0.0 |        -0.5 |         0.0 |          0.0 |       39.9 |
| Tyquan Thornton    | receiving | short_left (50% failed), deep_middle (100% failed)                                   | short_right x1.1, deep_left x1.1                                                           | x0.91, x0.97               |         0.0 |        -0.5 |         0.0 |          0.0 |       30.8 |
| Xavier Worthy      | receiving | short_right (33% failed), deep_right (100% failed)                                   | short_left x1.1, deep_middle x1.1                                                          | x0.91, x0.97               |         0.0 |        -0.4 |         0.0 |          0.0 |       43.9 |
| Cyrus Allen        | receiving | deep_middle (100% failed)                                                            | —                                                                                          | —                          |        -0.0 |        -0.1 |         0.0 |          0.0 |        3.4 |
| Jalen Royals       | receiving | short_left (100% failed), short_middle (100% failed)                                 | short_right x1.2, deep_left x1.2, deep_middle x1.2, deep_right x1.2                        | x0.91, x0.97, x0.97, x0.97 |         0.0 |         0.1 |         0.0 |          0.0 |        9.2 |
| Noah Gray          | receiving | short_left (100% failed), short_right (100% failed)                                  | short_middle x1.4                                                                          | x0.91                      |         0.0 |         0.1 |         0.0 |          0.0 |       14.7 |
| Khyiris Tonga      | rushing   | run middle (100% failed)                                                             | run inside_left x1.3, run outside_right x1.3, run inside_right x1.3, run outside_left x1.3 | x1.06, x1.06, x1.06, x1.06 |         0.0 |         0.0 |        -0.0 |          0.1 |        2.8 |

**LAC defensive weak spots:** deep passes: 14.6 allowed vs league 11.9 (19 plays).
- LAC struggle: Wk1 vs ARI: +0.14 EPA/play allowed (norm -0.12). Why: when blitzing 7.1 yds/dropback vs 3.5 in other games; outside runs 6.5 yds/play vs 5.0 in other games
**Offenses like KAN that faced LAC:** SEA (similarity 0.12: -1.2 pass / +0.9 run yds/play vs their norm), DEN (similarity 0.04: -1.7 pass / -0.2 run yds/play vs their norm), BUF (similarity 0.04: -3.3 pass / +0.9 run yds/play vs their norm) → KAN pass x0.99, run x1.00.
**LAC defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: two_high [online (high)].
- Best matchups: run_outside_left (x1.06), run_inside_left (x1.06); worst: pass_short_left (x0.91).
- LAC blitzes 27% of dropbacks (league 32%, FTN charting); KAN gains x1.16 as much per dropback vs the blitz as other offenses (38 blitzed dropbacks) -> pass yards x0.99
- KAN run plays vs two high shell defenses: x1.06 vs how other offenses fare (70 plays)
- KAN deep-throw rate vs two high shell: x1.19
- LAC DBs out: Derwin James (11 tgts, 7.6 yds/tgt allowed), Donte Jackson (9 tgts, 7.8 yds/tgt allowed) -> coverage 7.8 → 8.0 yds/tgt; WR yards x1.02

| player             | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Patrick Mahomes    | QB    |     198.71 |      1.41 |            0.68 |      1.86 |      14.29 |      0.00 |         0.00 |      0.00 |         0.10 |
| Kenneth Walker III | RB    |       0.00 |      0.00 |            0.00 |     22.34 |     102.64 |      4.08 |         2.59 |     24.89 |         0.73 |
| Xavier Worthy      | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.01 |         3.81 |     41.62 |         0.23 |
| Travis Kelce       | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.08 |         3.27 |     36.74 |         0.25 |
| Rashee Rice        | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.03 |         2.61 |     30.91 |         0.16 |
| Tyquan Thornton    | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.84 |         2.38 |     28.72 |         0.21 |
| Emmett Johnson     | RB    |       0.00 |      0.00 |            0.00 |      3.35 |      15.62 |      0.93 |         0.61 |      6.04 |         0.15 |
| Noah Gray          | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.03 |         1.30 |     13.79 |         0.07 |

**KAN kicker**

| player          |   fg_made |   xp_made |   kicking_points |
|:----------------|----------:|----------:|-----------------:|
| Harrison Butker |      1.91 |      2.67 |             8.40 |

**KAN defenders (vs LAC offense)**

| player           |   tackles |   sacks |   def_int |
|:-----------------|----------:|--------:|----------:|
| Nick Bolton      |     11.31 |    0.00 |      0.00 |
| Drue Tranquill   |      8.63 |    0.00 |      0.00 |
| L'Jarius Sneed   |      7.30 |    0.00 |      0.00 |
| Mansoor Delane   |      6.90 |    0.00 |      0.24 |
| Jaden Hicks      |      6.57 |    0.00 |      0.00 |
| Alohi Gilman     |      5.03 |    0.00 |      0.00 |
| George Karlaftis |      4.55 |    0.00 |      0.34 |
| Nohl Williams    |      4.49 |    0.88 |      0.00 |

## LAC vs KAN
**Clock:** 11.1 drives each; LAC 5.64 plays/drive at 37.0 s per clock-running play vs KAN 5.52 at 37.3 s → projected possession 50%, 63 plays to 61.
Projected 63 plays, 62% dropbacks, 32.5 pass att, 23.8 runs, 2.7 sacks. QB: Justin Herbert
**Coaching style:** Neutral-script pass rate low: 46% (league 59%); Early-down pass rate low: 37% (league 53%); 3rd-down deep share high: 25% (league 21%); Sack rate high: 10% (league 6%); Pass rate on 3rd & short high: 55% (league 41%); 3rd-down conversion low: 36% (league 42%); EPA/dropback low: -0.24 (league +0.06); EPA/run low: -0.18 (league -0.09).
**Model game script:** projected 17.2 – 25.1 (margin -7.9) → dropback rate +3.2%.
**Offensive line:** starters out: Joe Alt → sack rate x1.00, yds/dropback x0.99, yds/carry x1.01 (measured effect per missing starter).
**Strength of schedule:** own pass yds x1.03, own scoring x0.94, opp pass D x1.03 (raw stats re-rated against the opponents actually faced).
**Out:** Donte Jackson (carried from week 5 report: Out (Hamstring)), Derwin James (carried from week 5 report: Out (Hamstring)), Kayode Awosika (carried from week 5 report: Out (Fibula)), Trey Lance (carried from week 5 report: Doubtful (Groin)), Trevor Penning (carried from week 5 report: Out (Concussion)), Quentin Johnston (carried from week 5 report: Out (Chest)), Joe Alt (carried from week 5 report: Out (Neck)), Brenen Thompson (carried from week 5 report: Out (Quadricep)).
**Coach angle:** HC Jim Harbaugh (veteran HC, 15 prior seasons); plays called by OC Mike McDaniel (developing play-caller, 4 seasons calling); career balanced (+1.1 pts pass rate vs league, 4 seasons); typical; this season top target share 18%.
**KAN secondary:** DC Steve Spagnuolo, mixed-leaning: Blitz-heavy (third-highest blitz rate in 2025); Sneed moved to the nickel and used as a blitzer; outside Nohl Williams / Mansoor Delane; nickel L'Jarius Sneed; weak spot: Young outside corners; [research confidence medium, 2026-10-14].

**What worked last game → this week vs KAN** (failed play types cut, volume moved to what worked; `KAN allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player                   | type      | cut (failed last game)                                                                                                | more of                                                            | KAN allows there           |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:-------------------------|:----------|:----------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------|:---------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Kimani Vidal             | rushing   | run outside_left (33% failed), run middle (100% failed)                                                               | run outside_right x1.1, run inside_left x1.1                       | x1.00, x1.00               |         0.0 |         0.7 |         0.0 |          0.2 |       30.6 |
| Kimani Vidal             | receiving | short_middle (100% failed), short_right (100% failed)                                                                 | deep_middle x1.2, short_left x1.2, deep_right x1.2, deep_left x1.2 | x1.00, x0.96, x1.00, x1.00 |         0.0 |         0.7 |         0.0 |          0.2 |       30.6 |
| Omarion Hampton          | rushing   | run outside_left (100% failed), run outside_right (50% failed), run middle (44% failed), run inside_left (50% failed) | —                                                                  | —                          |         0.0 |        -0.5 |         0.0 |         -0.3 |       62.9 |
| Oronde Gadsden II        | receiving | deep_right (100% failed)                                                                                              | —                                                                  | —                          |         0.0 |        -0.4 |         0.0 |          0.0 |       32.6 |
| Marquez Valdes-Scantling | receiving | short_right (100% failed)                                                                                             | short_middle x1.2                                                  | x0.96                      |         0.0 |         0.3 |         0.0 |          0.0 |       11.1 |
| Keaton Mitchell          | rushing   | run outside_left (50% failed)                                                                                         | —                                                                  | —                          |         0.0 |         0.1 |         0.0 |         -0.1 |       53.9 |
| Keaton Mitchell          | receiving | short_right (33% failed)                                                                                              | —                                                                  | —                          |         0.0 |         0.1 |         0.0 |         -0.1 |       53.9 |
| Justin Herbert           | rushing   | run inside_right (100% failed)                                                                                        | —                                                                  | —                          |         0.0 |         0.0 |         0.0 |          0.0 |       30.8 |

**KAN defensive weak spots:** play-action dropbacks: 8.6 allowed vs league 6.9 (48 plays); vs RBs: 6.6 yds/target (league 5.3), x1.10 for RBs.
- KAN struggle: Wk2 vs IND: +0.15 EPA/play allowed (norm -0.13). Why: deep passes 17.0 yds/play vs 6.6 in other games; RBs 10.0 yds/target vs 5.9 in other games; missing starters: Mansoor Delane (CB); WRs 8.3 yds/target vs 5.6 in other games; when blitzing 8.8 yds/dropback vs 6.7 in other games → counted at 50% weight (those starters are available now)
- KAN struggle: Wk4 vs LVR: +0.03 EPA/play allowed (norm -0.09). Why: when blitzing 10.8 yds/dropback vs 6.0 in other games; TEs 8.7 yds/target vs 5.9 in other games; 8 explosive plays vs 4.0 per other game; short passes 7.2 yds/play vs 5.6 in other games; vs play action 10.2 yds/dropback vs 8.1 in other games
**Offenses like LAC that faced KAN:** MIA (similarity 0.08: +1.3 pass / -1.7 run yds/play vs their norm), IND (similarity 0.06: +1.9 pass / -0.1 run yds/play vs their norm), DEN (similarity 0.03: -2.1 pass / +1.2 run yds/play vs their norm) → LAC pass x1.00, run x0.99.
**KAN defensive scheme (online/tagged):** blitz: avg, coverage: avg, shell: two_high [online (high)].
- Best matchups: pass_deep_left (x1.00), pass_deep_middle (x1.00); worst: pass_short_left (x0.96).
- KAN blitzes 29% of dropbacks (league 32%, FTN charting); LAC gains x0.91 as much per dropback vs the blitz as other offenses (44 blitzed dropbacks) -> pass yards x1.00
- LAC short plays vs two high shell defenses: x0.94 vs how other offenses fare (116 plays)
- LAC run plays vs two high shell defenses: x1.05 vs how other offenses fare (115 plays)

| player                   | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-------------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Justin Herbert           | QB    |     210.69 |      1.05 |            1.27 |      4.84 |      33.04 |      0.31 |         0.20 |      1.91 |         0.11 |
| Tre Harris               | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      7.47 |         4.42 |     52.47 |         0.17 |
| Omarion Hampton          | RB    |       0.00 |      0.00 |            0.00 |     13.09 |      52.29 |      1.70 |         1.13 |     10.26 |         0.38 |
| Keaton Mitchell          | RB    |       0.00 |      0.00 |            0.00 |      6.12 |      26.51 |      4.44 |         2.95 |     26.34 |         0.26 |
| Oronde Gadsden II        | TE    |       0.00 |      0.00 |            0.00 |      0.20 |       0.89 |      4.60 |         2.84 |     30.16 |         0.16 |
| Ladd McConkey            | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.91 |         2.36 |     29.76 |         0.14 |
| Kimani Vidal             | RB    |       0.00 |      0.00 |            0.00 |      3.22 |      13.86 |      2.49 |         1.52 |     16.48 |         0.20 |
| Charlie Kolar            | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.23 |         1.47 |     14.59 |         0.06 |
| Marquez Valdes-Scantling | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.59 |         0.99 |     10.88 |         0.05 |

**LAC kicker**

| player         |   fg_made |   xp_made |   kicking_points |
|:---------------|----------:|----------:|-----------------:|
| Cameron Dicker |      1.62 |      1.75 |             6.62 |

**LAC defenders (vs KAN offense)**

| player             |   tackles |   sacks |   def_int |
|:-------------------|----------:|--------:|----------:|
| Daiyan Henley      |      6.04 |    0.06 |      0.00 |
| Del'Shawn Phillips |      5.63 |    0.00 |      0.00 |
| Akheem Mesidor     |      4.87 |    0.46 |      0.00 |
| Tuli Tuipulotu     |      4.41 |    0.35 |      0.20 |
| Cam Hart           |      3.98 |    0.00 |      0.14 |
| Tony Jefferson     |      3.78 |    0.00 |      0.00 |
| Elijah Molden      |      3.67 |    0.00 |      0.00 |
| Justin Eboigbe     |      3.37 |    0.10 |      0.00 |

## LVR vs BUF
**Clock:** 10.4 drives each; LVR 6.15 plays/drive at 37.6 s per clock-running play vs BUF 5.58 at 37.7 s → projected possession 52%, 64 plays to 58.
Projected 64 plays, 62% dropbacks, 37.2 pass att, 24.1 runs, 2.0 sacks. QB: Kirk Cousins
**Coaching style:** Sack rate low: 4% (league 6%); Pass rate on 2nd & short low: 8% (league 31%); Pass rate on 3rd & short high: 53% (league 41%); EPA/dropback high: +0.14 (league +0.06); EPA/run low: -0.23 (league -0.09); Favors run middle (36%).
**Model game script:** projected 26.4 – 30.0 (margin -3.6) → dropback rate +1.4%.
**Strength of schedule:** opp pass D x0.97 (raw stats re-rated against the opponents actually faced).
**Out:** Jalen Nailor (carried from week 5 report: Out (Concussion)), Dont'e Thornton Jr. (carried from week 5 report: Out (Hamstring)), Trey Zuhn III (carried from week 5 report: Out (Knee)).
**Coach angle:** HC Klint Kubiak (first-year HC, 0 prior seasons); calls own plays (developing play-caller, 3 seasons calling); career balanced (-1.0 pts pass rate vs league, 3 seasons); leans on stars; this season top target share 24%.
**BUF secondary:** DC Jim Leonhard, mixed-leaning: Switched from 4-2-5 to aggressive multiple 3-4; pressure from varied angles and five-man rushes on money downs; outside Christian Benford / Maxwell Hairston; nickel Dee Alford; weak spot: Benford / Alford / Hairston all ranked among the worst in coverage by PFF entering week 4; communication busts; [research confidence medium, 2026-10-14].

**What worked last game → this week vs BUF** (failed play types cut, volume moved to what worked; `BUF allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player        | type      | cut (failed last game)                              | more of                                                                                | BUF allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:--------------|:----------|:----------------------------------------------------|:---------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Ashton Jeanty | receiving | short_left (100% failed), short_middle (50% failed) | short_middle x1.2                                                                      | x0.98                             |         0.0 |        -2.1 |         0.0 |          0.0 |      104.4 |
| Ashton Jeanty | rushing   | run inside_right (20% failed)                       | —                                                                                      | —                                 |         0.0 |        -2.1 |         0.0 |          0.0 |      104.4 |
| Brock Bowers  | receiving | short_left (50% failed), short_right (60% failed)   | short_middle x1.1, deep_left x1.1                                                      | x0.98, x1.02                      |        -0.0 |        -1.9 |         0.0 |          0.0 |       74.5 |
| Cody White    | receiving | short_left (100% failed), short_right (100% failed) | deep_left x1.6                                                                         | x1.02                             |        -0.0 |         1.8 |         0.0 |          0.0 |       24.7 |
| Tre Tucker    | receiving | deep_left (100% failed)                             | —                                                                                      | —                                 |         0.0 |        -0.7 |         0.0 |          0.1 |       48.6 |
| Tre Tucker    | rushing   | run inside_right (100% failed)                      | run outside_left x1.3                                                                  | x0.98                             |         0.0 |        -0.7 |         0.0 |          0.1 |       48.6 |
| Malik Benson  | receiving | short_left (100% failed)                            | short_right x1.1, short_middle x1.1, deep_left x1.1, deep_right x1.1, deep_middle x1.1 | x0.98, x0.98, x1.02, x1.02, x1.02 |         0.0 |         0.1 |         0.0 |          0.0 |        8.0 |
| Dylan Laube   | rushing   | run outside_right (100% failed)                     | run inside_left x1.1                                                                   | x0.98                             |         0.0 |         0.0 |         0.0 |         -0.0 |        4.3 |

**BUF defensive weak spots:** red-zone TDs per play: 26% allowed vs league 21% (61 plays); 3rd-down conversions: 49% allowed vs league 42% (76 plays); explosive plays: 10% allowed vs league 9% (328 plays); short passes: 6.7 allowed vs league 6.0 (155 plays).
- BUF struggle: Wk2 vs DET: +0.23 EPA/play allowed (norm +0.11). Why: RBs 8.2 yds/target vs 4.9 in other games; deep passes 13.5 yds/play vs 8.7 in other games; DET is a strong offense (+0.16 EPA/play in its other games)
- BUF struggle: Wk5 vs LAR: +0.25 EPA/play allowed (norm +0.10). Why: TEs 11.0 yds/target vs 6.6 in other games; vs play action 8.7 yds/dropback vs 5.6 in other games
**Offenses like LVR that faced BUF:** DET (similarity 0.30: -0.1 pass / -1.3 run yds/play vs their norm), LAR (similarity 0.23: -0.6 pass / -1.7 run yds/play vs their norm), HOU (similarity 0.19: -0.7 pass / +0.7 run yds/play vs their norm) → LVR pass x0.99, run x0.98.
**BUF defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: two_high [online (high)].
- BUF brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed +0.14 on 11 attempts. LVR 3rd-down deep share 18%.
- Best matchups: pass_deep_left (x1.02), pass_deep_middle (x1.02); worst: pass_short_left (x0.98).
- BUF blitzes 34% of dropbacks (league 32%, FTN charting); LVR gains x1.16 as much per dropback vs the blitz as other offenses (48 blitzed dropbacks) -> pass yards x1.00
- LVR deep plays vs zone heavy coverage defenses: x1.07 vs how other offenses fare (7 plays)
- LVR deep-throw rate vs zone heavy coverage: x0.82
- LVR deep-throw rate vs two high shell: x1.12

| player              | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:--------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Kirk Cousins        | QB    |     250.73 |      2.41 |            0.50 |      0.70 |       4.72 |      0.00 |         0.00 |      0.00 |         0.02 |
| Ashton Jeanty       | RB    |       0.00 |      0.00 |            0.00 |     16.88 |      61.99 |      6.67 |         4.47 |     40.89 |         0.54 |
| Brock Bowers        | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |     10.12 |         6.64 |     73.00 |         0.53 |
| Tre Tucker          | WR    |       0.00 |      0.00 |            0.00 |      0.51 |       1.90 |      5.90 |         3.86 |     45.05 |         0.29 |
| Michael Mayer       | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.88 |         4.18 |     38.05 |         0.27 |
| Cody White          | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.31 |         1.95 |     24.06 |         0.28 |
| Mike Washington Jr. | RB    |       0.00 |      0.00 |            0.00 |      5.24 |      20.54 |      1.12 |         0.74 |      7.29 |         0.24 |

**LVR kicker**

| player   |   fg_made |   xp_made |   kicking_points |
|:---------|----------:|----------:|-----------------:|
| Matt Gay |      1.87 |      2.91 |             8.53 |

**LVR defenders (vs BUF offense)**

| player          |   tackles |   sacks |   def_int |
|:----------------|----------:|--------:|----------:|
| Nakobe Dean     |      9.43 |    0.19 |      0.00 |
| Quay Walker     |      6.64 |    0.18 |      0.00 |
| Jeremy Chinn    |      6.12 |    0.15 |      0.00 |
| Taron Johnson   |      4.66 |    0.00 |      0.00 |
| Hezekiah Masses |      4.00 |    0.00 |      0.55 |
| Treydan Stukes  |      3.41 |    0.00 |      0.14 |
| Eric Stokes     |      3.35 |    0.14 |      0.00 |
| Adam Butler     |      2.69 |    0.10 |      0.00 |

## BUF vs LVR
**Clock:** 10.4 drives each; BUF 5.58 plays/drive at 37.7 s per clock-running play vs LVR 6.15 at 37.6 s → projected possession 48%, 58 plays to 64.
Projected 58 plays, 56% dropbacks, 26.8 pass att, 25.8 runs, 1.9 sacks. QB: Josh Allen
**Coaching style:** Deep-pass share high: 24% (league 19%); 3rd-down deep share high: 25% (league 21%); Shotgun rate low: 46% (league 61%); Pass rate on 3rd & short low: 11% (league 41%); 3rd-down conversion high: 54% (league 42%); EPA/dropback high: +0.35 (league +0.06); EPA/run high: +0.03 (league -0.09); Favors run middle (34%).
**Model game script:** projected 30.0 – 26.4 (margin +3.6) → dropback rate -1.4%.
**Strength of schedule:** own pass yds x1.03, opp scoring D x1.03 (raw stats re-rated against the opponents actually faced).
**Out:** Ed Oliver (carried from week 5 report: Out (Knee)), Josh Palmer (carried from week 5 report: Out (Shoulder)).
**Coach angle:** HC Joe Brady (first-year HC, 0 prior seasons); calls own plays (developing play-caller, 4 seasons calling); career balanced (-1.9 pts pass rate vs league, 4 seasons); typical; this season top target share 20%.
**LVR secondary:** DC Rob Leonard, mixed-leaning: Macdonald-style multiple and aggressive defense; outside Eric Stokes / Hezekiah Masses; nickel Taron Johnson; weak spot: Young corner room; [research confidence medium, 2026-10-14].

**What worked last game → this week vs LVR** (failed play types cut, volume moved to what worked; `LVR allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player         | type      | cut (failed last game)                                   | more of                                                               | LVR allows there           |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:---------------|:----------|:---------------------------------------------------------|:----------------------------------------------------------------------|:---------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Dalton Kincaid | receiving | deep_right (100% failed)                                 | short_left x1.1                                                       | x1.12                      |         0.0 |        -1.0 |         0.0 |          0.0 |       42.0 |
| James Cook     | rushing   | run middle (40% failed), run outside_right (100% failed) | —                                                                     | —                          |         0.0 |        -0.6 |        -0.0 |          0.0 |      120.7 |
| Dawson Knox    | receiving | short_left (100% failed), deep_middle (100% failed)      | short_right x1.2                                                      | x1.12                      |         0.0 |        -0.5 |        -0.0 |         -0.0 |       20.8 |
| Keon Coleman   | receiving | deep_right (100% failed)                                 | —                                                                     | —                          |         0.0 |        -0.4 |         0.0 |          0.0 |       44.5 |
| Skyler Bell    | receiving | short_right (100% failed), deep_left (100% failed)       | short_left x1.4, deep_middle x1.4, deep_right x1.4, short_middle x1.4 | x1.12, x1.04, x1.04, x1.12 |         0.0 |         0.1 |         0.0 |          0.0 |        5.8 |
| Ray Davis      | rushing   | run outside_left (100% failed)                           | run inside_left x1.1                                                  | x1.13                      |         0.0 |        -0.0 |        -0.0 |         -0.0 |       10.0 |

**LVR defensive weak spots:** red-zone TDs per play: 31% allowed vs league 21% (42 plays); explosive plays: 11% allowed vs league 9% (268 plays); outside runs: 6.5 allowed vs league 4.9 (23 plays); inside runs: 4.5 allowed vs league 3.9 (91 plays).
- LVR struggle: Wk4 vs KAN: +0.15 EPA/play allowed (norm -0.02). Why: outside runs 10.6 yds/play vs 5.4 in other games; inside runs 7.2 yds/play vs 3.8 in other games; deep passes 17.2 yds/play vs 12.1 in other games; KAN is a strong offense (+0.19 EPA/play in its other games)
- LVR struggle: Wk5 vs NWE: +0.49 EPA/play allowed (norm -0.10). Why: when blitzing 14.0 yds/dropback vs 6.2 in other games; WRs 16.1 yds/target vs 8.2 in other games; TEs 11.8 yds/target vs 6.1 in other games; vs play action 11.8 yds/dropback vs 6.2 in other games; deep passes 20.2 yds/play vs 11.1 in other games
**Offenses like BUF that faced LVR:** NWE (similarity 0.52: +5.0 pass / +1.8 run yds/play vs their norm), MIA (similarity 0.17: +1.3 pass / -2.1 run yds/play vs their norm), KAN (similarity 0.04: -1.5 pass / +2.6 run yds/play vs their norm) → BUF pass x1.08, run x1.01.
**LVR defensive scheme (online/tagged):** blitz: avg, coverage: avg, shell: two_high [online (high)].
- LVR is soft deep (+0.58 EPA/deep att vs league +0.43); BUF throws deep 24%.
- Best matchups: run_outside_left (x1.13), run_inside_left (x1.13); worst: pass_other (x1.00).
- Last game — worked: run_inside_left, run_inside_right; failed: none.
- LVR blitzes 26% of dropbacks (league 32%, FTN charting); BUF gains x1.06 as much per dropback vs the blitz as other offenses (53 blitzed dropbacks) -> pass yards x1.00
- BUF deep plays vs two high shell defenses: x0.95 vs how other offenses fare (23 plays)
- BUF run plays vs two high shell defenses: x1.07 vs how other offenses fare (107 plays)

| player         | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:---------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Josh Allen     | QB    |     248.41 |      1.63 |            0.70 |      7.88 |      47.69 |      0.18 |         0.12 |      1.86 |         0.57 |
| James Cook     | RB    |       0.00 |      0.00 |            0.00 |     19.83 |     103.31 |      2.10 |         1.40 |     16.67 |         0.74 |
| Khalil Shakir  | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.54 |         3.71 |     53.79 |         0.23 |
| Keon Coleman   | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.97 |         2.65 |     42.38 |         0.28 |
| DJ Moore       | WR    |       0.00 |      0.00 |            0.00 |      0.29 |       1.53 |      3.82 |         2.41 |     38.01 |         0.24 |
| Dalton Kincaid | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.76 |         2.47 |     39.89 |         0.23 |
| Ty Johnson     | RB    |       0.00 |      0.00 |            0.00 |      0.26 |       1.22 |      2.49 |         1.81 |     24.56 |         0.15 |
| Dawson Knox    | TE    |       0.00 |      0.00 |            0.00 |      0.21 |       0.95 |      2.09 |         1.44 |     19.29 |         0.17 |

**BUF kicker**

| player     |   fg_made |   xp_made |   kicking_points |
|:-----------|----------:|----------:|-----------------:|
| Tyler Bass |      1.24 |      3.46 |             7.19 |

**BUF defenders (vs LVR offense)**

| player               |   tackles |   sacks |   def_int |
|:---------------------|----------:|--------:|----------:|
| Dorian Williams      |      7.35 |    0.00 |      0.00 |
| Cole Bishop          |      6.76 |    0.00 |      0.00 |
| Terrel Bernard       |      6.23 |    0.00 |      0.00 |
| Christian Benford    |      4.74 |    0.00 |      0.00 |
| Davison Igbinosun    |      4.72 |    0.00 |      0.00 |
| C.J. Gardner-Johnson |      4.52 |    0.00 |      0.23 |
| Greg Rousseau        |      3.35 |    1.02 |      0.00 |
| Bradley Chubb        |      2.92 |    0.25 |      0.00 |

## GNB vs DAL
**Clock:** 10.4 drives each; GNB 5.69 plays/drive at 38.3 s per clock-running play vs DAL 6.20 at 36.3 s → projected possession 49%, 59 plays to 64.
Projected 59 plays, 61% dropbacks, 33.7 pass att, 23.1 runs, 2.0 sacks. QB: Jordan Love
**Coaching style:** 3rd-down conversion low: 33% (league 42%); EPA/dropback high: +0.13 (league +0.06); EPA/run low: -0.25 (league -0.09); Favors run inside left (32%).
**Model game script:** projected 30.8 – 26.8 (margin +4.0) → dropback rate -1.6%.
**Offensive line:** starters out: Jacob Monk → sack rate x1.00, yds/dropback x0.99, yds/carry x1.01 (measured effect per missing starter).
**Strength of schedule:** own scoring x1.06 (raw stats re-rated against the opponents actually faced).
**Out:** Aaron Banks (carried from week 5 report: Doubtful (Knee)), Chris Brooks (carried from week 5 report: Out (Ankle)), Jacob Monk (carried from week 5 report: Doubtful (Quadricep)), Savion Williams (carried from week 5 report: Out (Ankle)).
**Coach angle:** HC Matt LaFleur (veteran HC, 7 prior seasons); calls own plays (veteran play-caller, 8 seasons calling); career balanced (-1.7 pts pass rate vs league, 8 seasons); typical; this season top target share 23%.
**DAL secondary:** DC Christian Parker, mixed-leaning: Multiple 3-4 with 4-2-5 nickel; will play man if the corners allow; analysts expect more zone; outside Joey Porter Jr. / DaRon Bland; nickel Caleb Downs; weak spot: Depleted corner room; Joey Porter Jr. added Oct 1; [research confidence low, 2026-10-14].

**What worked last game → this week vs DAL** (failed play types cut, volume moved to what worked; `DAL allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player           | type      | cut (failed last game)                                 | more of                                                                               | DAL allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:-----------------|:----------|:-------------------------------------------------------|:--------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| MarShawn Lloyd   | rushing   | run inside_left (50% failed), run middle (100% failed) | run outside_left x1.1, run inside_right x1.1, run outside_right x1.1                  | x1.10, x1.10, x1.10               |        -0.0 |        -0.4 |         0.0 |          0.6 |       81.2 |
| MarShawn Lloyd   | receiving | short_middle (50% failed)                              | —                                                                                     | —                                 |        -0.0 |        -0.4 |         0.0 |          0.6 |       81.2 |
| Bo Melton        | receiving | short_middle (100% failed), short_right (100% failed)  | short_left x1.2                                                                       | x1.05                             |         0.0 |        -0.7 |         0.0 |          0.0 |       12.1 |
| Skyy Moore       | receiving | short_right (100% failed)                              | short_middle x1.1, deep_middle x1.1, deep_right x1.1, short_left x1.1, deep_left x1.1 | x1.05, x1.06, x1.06, x1.05, x1.06 |        -0.0 |         0.6 |         0.0 |          0.0 |       20.1 |
| Matthew Golden   | receiving | deep_right (50% failed)                                | —                                                                                     | —                                 |         0.0 |        -0.4 |        -0.0 |         -0.0 |       75.3 |
| Tucker Kraft     | receiving | short_right (50% failed)                               | —                                                                                     | —                                 |         0.0 |         0.3 |        -0.0 |         -0.0 |       59.1 |
| Christian Watson | receiving | short_left (50% failed), deep_left (50% failed)        | —                                                                                     | —                                 |        -0.0 |        -0.3 |         0.0 |          0.0 |       68.8 |
| Pierre Strong    | receiving | short_right (33% failed), short_left (100% failed)     | short_right x1.1                                                                      | x1.05                             |        -0.0 |        -0.0 |         0.0 |          0.0 |       16.3 |

**DAL defensive weak spots:** explosive plays: 12% allowed vs league 9% (280 plays); outside runs: 6.6 allowed vs league 4.9 (33 plays); 3rd-down conversions: 52% allowed vs league 42% (58 plays); inside runs: 4.5 allowed vs league 3.9 (109 plays); red-zone TDs per play: 25% allowed vs league 21% (60 plays).
- DAL struggle: Wk1 vs NYG: +0.37 EPA/play allowed (norm +0.15). Why: 3rd/4th downs converted 90% vs 44%; short passes 8.2 yds/play vs 6.6 in other games; red-zone TD rate per play 33% vs 23%
**Offenses like GNB that faced DAL:** TAM (similarity 0.12: +1.4 pass / +3.0 run yds/play vs their norm), NYG (similarity 0.10: +2.1 pass / +1.8 run yds/play vs their norm), WAS (similarity 0.10: +0.8 pass / +0.6 run yds/play vs their norm) → GNB pass x1.00, run x1.01.
**DAL defensive scheme (online/tagged):** blitz: avg, coverage: avg [online (high)].
- DAL is soft deep (+0.83 EPA/deep att vs league +0.43); GNB throws deep 22%.
- Best matchups: run_outside_left (x1.10), run_inside_left (x1.10); worst: pass_other (x1.00).
- DAL blitzes 27% of dropbacks (league 32%, FTN charting); GNB gains x1.13 as much per dropback vs the blitz as other offenses (74 blitzed dropbacks) -> pass yards x0.99
- DAL DBs out: Cobie Durant (5 tgts, 7.7 yds/tgt allowed) -> coverage 7.9 → 8.0 yds/tgt; WR yards x1.00

| player           | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-----------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Jordan Love      | QB    |     285.86 |      2.62 |            0.24 |      0.81 |       4.50 |      0.00 |         0.00 |      0.00 |         0.04 |
| Christian Watson | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      7.73 |         4.91 |     67.80 |         0.62 |
| MarShawn Lloyd   | RB    |       0.00 |      0.00 |            0.00 |     13.38 |      55.98 |      3.26 |         2.29 |     25.05 |         0.62 |
| Matthew Golden   | WR    |       0.00 |      0.00 |            0.00 |      0.28 |       1.23 |      8.05 |         5.15 |     73.20 |         0.37 |
| Tucker Kraft     | TE    |       0.00 |      0.00 |            0.00 |      0.74 |       3.09 |      6.39 |         4.39 |     55.51 |         0.37 |
| Kaleb Johnson    | RB    |       0.00 |      0.00 |            0.00 |      6.78 |      29.99 |      0.72 |         0.49 |      5.22 |         0.28 |
| Skyy Moore       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.51 |         1.69 |     20.13 |         0.13 |
| Bo Melton        | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.55 |         1.05 |     12.16 |         0.10 |

**GNB kicker**

| player     |   fg_made |   xp_made |   kicking_points |
|:-----------|----------:|----------:|-----------------:|
| Trey Smack |      1.57 |      3.44 |             8.15 |

**GNB defenders (vs DAL offense)**

| player          |   tackles |   sacks |   def_int |
|:----------------|----------:|--------:|----------:|
| Evan Williams   |      9.96 |    0.17 |      0.20 |
| Zaire Franklin  |      8.35 |    0.00 |      0.00 |
| Javon Bullard   |      6.74 |    0.00 |      0.00 |
| Keisean Nixon   |      6.65 |    0.05 |      0.12 |
| Edgerrin Cooper |      5.75 |    0.38 |      0.20 |
| Lukas Van Ness  |      4.63 |    0.28 |      0.00 |
| Brandon Cisse   |      4.45 |    0.25 |      0.00 |
| Isaiah McDuffie |      3.99 |    0.00 |      0.00 |

## DAL vs GNB
**Clock:** 10.4 drives each; DAL 6.20 plays/drive at 36.3 s per clock-running play vs GNB 5.69 at 38.3 s → projected possession 51%, 64 plays to 59.
Projected 64 plays, 66% dropbacks, 38.3 pass att, 22.0 runs, 2.0 sacks. QB: Dak Prescott
**Coaching style:** Neutral-script pass rate high: 68% (league 59%); Early-down pass rate high: 61% (league 53%); 3rd-down deep share low: 13% (league 21%); Sack rate low: 3% (league 6%); No-huddle rate high: 11% (league 6%); Pass rate on 3rd & short high: 60% (league 41%); EPA/dropback high: +0.16 (league +0.06); EPA/run high: -0.01 (league -0.09); Favors run middle (38%).
**Model game script:** projected 26.8 – 30.8 (margin -4.0) → dropback rate +1.6%.
**Strength of schedule:** own run yds x1.02, opp run D x0.97, opp scoring D x1.02 (raw stats re-rated against the opponents actually faced).
**Out:** Cobie Durant (carried from week 5 report: Out (Hamstring)), DeMarvion Overshown (carried from week 5 report: Out (Hamstring)), Drew Shelton (carried from week 5 report: Out (Hamstring)).
**Coach angle:** HC Brian Schottenheimer (young HC, 1 prior seasons); calls own plays (developing play-caller, 4 seasons calling); career run-first (-2.5 pts pass rate vs league, 4 seasons); typical; this season top target share 27%.
**GNB secondary:** DC Jonathan Gannon, coverage lean unknown: New DC Gannon; aggressive style per players; outside Keisean Nixon / Brandon Cisse; nickel Javon Bullard; weak spot: Right corner spot unsettled (Cisse / Valentine / St-Juste); Nixon coverage grade 50.4; [research confidence low, 2026-10-14].

**What worked last game → this week vs GNB** (failed play types cut, volume moved to what worked; `GNB allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player            | type      | cut (failed last game)                                                                | more of                                                             | GNB allows there           |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:------------------|:----------|:--------------------------------------------------------------------------------------|:--------------------------------------------------------------------|:---------------------------|------------:|------------:|------------:|-------------:|-----------:|
| George Pickens    | receiving | deep_left (67% failed), short_right (100% failed), short_left (12% failed)            | short_left x1.1, deep_middle x1.1                                   | x0.93, x1.09               |         0.0 |         1.3 |         0.0 |          0.0 |       64.8 |
| CeeDee Lamb       | receiving | deep_right (100% failed), short_left (50% failed)                                     | short_right x1.1                                                    | x0.93                      |         0.0 |        -1.1 |         0.0 |          0.0 |       75.4 |
| Javonte Williams  | receiving | short_middle (50% failed)                                                             | —                                                                   | —                          |         0.0 |        -0.6 |         0.0 |         -0.2 |       99.5 |
| Javonte Williams  | rushing   | run inside_left (25% failed), run inside_right (100% failed), run middle (14% failed) | run inside_left x1.1, run middle x1.1                               | x1.04, x1.04               |         0.0 |        -0.6 |         0.0 |         -0.2 |       99.5 |
| Jake Ferguson     | receiving | short_right (50% failed), short_left (33% failed), short_middle (100% failed)         | short_left x1.1                                                     | x0.93                      |         0.0 |        -0.4 |         0.0 |          0.0 |       28.1 |
| Jonathan Mingo    | receiving | deep_left (100% failed)                                                               | —                                                                   | —                          |         0.0 |        -0.2 |         0.0 |          0.0 |       11.1 |
| Brevyn Spann-Ford | receiving | short_left (100% failed), short_middle (100% failed)                                  | deep_left x1.2, short_right x1.2, deep_right x1.2, deep_middle x1.2 | x1.09, x0.93, x1.09, x1.09 |         0.0 |         0.2 |         0.0 |          0.0 |        8.3 |
| Ryan Flournoy     | receiving | short_middle (100% failed)                                                            | —                                                                   | —                          |         0.0 |        -0.1 |         0.0 |          0.0 |       37.4 |

**GNB defensive weak spots:** outside runs: 7.3 allowed vs league 4.9 (37 plays); vs RBs: 8.9 yds/target (league 5.3), x1.17 for RBs; red-zone TDs per play: 27% allowed vs league 21% (49 plays); 3rd-down conversions: 48% allowed vs league 42% (71 plays).
- GNB struggle: Wk3 vs ATL: +0.32 EPA/play allowed (norm -0.10). Why: deep passes 24.8 yds/play vs 6.4 in other games; when blitzing 13.1 yds/dropback vs 3.9 in other games; outside runs 13.5 yds/play vs 4.7 in other games; WRs 13.0 yds/target vs 5.7 in other games; vs play action 7.1 yds/dropback vs 4.3 in other games
**Offenses like DAL that faced GNB:** NYJ (similarity 0.13: -1.3 pass / -1.8 run yds/play vs their norm), TAM (similarity 0.06: -0.5 pass / -0.7 run yds/play vs their norm), MIN (similarity 0.03: -0.9 pass / -0.3 run yds/play vs their norm) → DAL pass x0.99, run x0.98.
**GNB defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: two_high [online (high)].
- GNB run defense is soft (+0.01 EPA/run).
- Best matchups: pass_deep_left (x1.09), pass_deep_middle (x1.09); worst: pass_short_left (x0.93).
- Last game — worked: none; failed: pass_short_middle, pass_deep_left.
- GNB blitzes 38% of dropbacks (league 32%, FTN charting); DAL gains x0.92 as much per dropback vs the blitz as other offenses (68 blitzed dropbacks) -> pass yards x0.99
- DAL deep plays vs zone heavy coverage defenses: x1.16 vs how other offenses fare (14 plays)
- DAL short plays vs zone heavy coverage defenses: x0.94 vs how other offenses fare (117 plays)
- DAL deep-throw rate vs zone heavy coverage: x0.84
- DAL run plays vs two high shell defenses: x1.06 vs how other offenses fare (60 plays)

| player           | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-----------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Dak Prescott     | QB    |     257.92 |      1.63 |            1.35 |      2.22 |      16.20 |      0.00 |         0.00 |      0.00 |         0.08 |
| Javonte Williams | RB    |       0.00 |      0.00 |            0.00 |     18.04 |      76.58 |      3.86 |         2.81 |     23.05 |         0.78 |
| CeeDee Lamb      | WR    |       0.00 |      0.00 |            0.00 |      0.35 |       1.52 |      9.50 |         6.68 |     70.02 |         0.41 |
| George Pickens   | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      8.43 |         5.73 |     63.42 |         0.26 |
| Ryan Flournoy    | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.48 |         3.61 |     36.48 |         0.15 |
| Jake Ferguson    | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.40 |         3.03 |     27.53 |         0.24 |
| KaVontae Turpin  | WR    |       0.00 |      0.00 |            0.00 |      0.34 |       1.59 |      1.68 |         1.16 |     10.47 |         0.08 |
| Jonathan Mingo   | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.56 |         1.04 |     10.60 |         0.06 |
| Tyler Goodson    | RB    |       0.00 |      0.00 |            0.00 |      2.39 |      10.38 |      0.44 |         0.31 |      2.87 |         0.12 |

**DAL kicker**

| player         |   fg_made |   xp_made |   kicking_points |
|:---------------|----------:|----------:|-----------------:|
| Brandon Aubrey |      1.23 |      3.10 |             6.80 |

**DAL defenders (vs GNB offense)**

| player            |   tackles |   sacks |   def_int |
|:------------------|----------:|--------:|----------:|
| Dee Winters       |      6.62 |    0.00 |      0.00 |
| Caleb Downs       |      5.25 |    0.28 |      0.00 |
| Jaishawn Barham   |      4.93 |    0.00 |      0.00 |
| Donovan Ezeiruaku |      4.49 |    0.13 |      0.00 |
| DaRon Bland       |      3.73 |    0.00 |      0.00 |
| Markquese Bell    |      3.35 |    0.00 |      0.00 |
| Otito Ogbonnia    |      3.22 |    0.00 |      0.00 |
| Malik Hooker      |      2.83 |    0.00 |      0.00 |

## SFO vs WAS
**Clock:** 10.7 drives each; SFO 5.68 plays/drive at 37.6 s per clock-running play vs WAS 5.82 at 37.4 s → projected possession 50%, 61 plays to 62.
Projected 61 plays, 57% dropbacks, 29.9 pass att, 26.3 runs, 1.6 sacks. QB: Brock Purdy
**Coaching style:** 4th-down go rate low: 8% (league 19%); Sack rate low: 3% (league 6%); Shotgun rate low: 48% (league 61%); No-huddle rate low: 0% (league 6%); 3rd-down conversion high: 50% (league 42%); EPA/dropback high: +0.38 (league +0.06); Favors run middle (37%).
**Model game script:** projected 30.2 – 22.1 (margin +8.1) → dropback rate -3.3%.
**Weather:** forecast 59°F, wind 13 mph → pass yds x0.98, long FG x1.00.
**Strength of schedule:** own pass yds x1.03, opp pass D x1.04, opp run D x1.02 (raw stats re-rated against the opponents actually faced).
**Out:** Kyle Juszczyk (carried from week 5 report: Out (Knee)), Nick Bosa (carried from week 5 report: Out (Knee)), Marques Sigle (carried from week 5 report: Out (Ankle)), James Thompson Jr. (carried from week 5 report: Out (Ankle)).
**Coach angle:** HC Kyle Shanahan (veteran HC, 9 prior seasons); calls own plays (veteran play-caller, 11 seasons calling); career balanced (-1.3 pts pass rate vs league, 11 seasons); typical; this season top target share 27%.
**WAS secondary:** DC Daronte Jones, mixed-leaning: Flores-style: disguised pressure (35-40% blitz) with heavy Cover 2 and Cover 0; interchangeable DBs; outside Rasul Douglas / Fabian Moreau; nickel Amik Robertson; weak spot: Sainristil allowed 15 TDs in coverage over two seasons; [research confidence medium, 2026-10-14].

**What worked last game → this week vs WAS** (failed play types cut, volume moved to what worked; `WAS allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player           | type      | cut (failed last game)                                                                  | more of                                                                                | WAS allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:-----------------|:----------|:----------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Mike Evans       | receiving | deep_right (67% failed), deep_left (100% failed)                                        | —                                                                                      | —                                 |         0.0 |        -1.5 |         0.0 |          0.0 |       76.1 |
| George Kittle    | receiving | short_right (50% failed), deep_left (100% failed)                                       | —                                                                                      | —                                 |         0.0 |         1.1 |         0.0 |          0.0 |       65.6 |
| Deebo Samuel Sr. | receiving | short_middle (100% failed)                                                              | short_right x1.1                                                                       | x1.01                             |         0.0 |         0.7 |         0.0 |         -0.1 |       46.8 |
| Deebo Samuel Sr. | rushing   | run outside_left (100% failed)                                                          | run middle x1.1                                                                        | x1.08                             |         0.0 |         0.7 |         0.0 |         -0.1 |       46.8 |
| Luke Farrell     | receiving | short_left (100% failed)                                                                | short_right x1.2, deep_right x1.2, short_middle x1.2, deep_middle x1.2, deep_left x1.2 | x1.01, x1.03, x1.01, x1.03, x1.03 |         0.0 |         0.3 |         0.0 |          0.0 |        7.9 |
| Kaelon Black     | rushing   | run middle (100% failed), run inside_left (33% failed), run outside_right (100% failed) | run inside_left x1.1, run inside_right x1.2                                            | x1.08, x1.08                      |         0.0 |         0.0 |         0.0 |          0.2 |       35.9 |
| Brandin Cooks    | receiving | short_middle (100% failed)                                                              | short_left x1.1                                                                        | x1.01                             |         0.0 |        -0.1 |         0.0 |          0.0 |        7.6 |
| Jacob Cowing     | receiving | short_left (100% failed)                                                                | short_right x1.4                                                                       | x1.01                             |         0.0 |         0.0 |         0.0 |          0.0 |       12.2 |

**WAS defensive weak spots:** red-zone TDs per play: 33% allowed vs league 21% (46 plays); vs TEs: 9.1 yds/target (league 7.2), x1.10 for TEs.
- WAS struggle: Wk2 vs DAL: +0.23 EPA/play allowed (norm +0.00). Why: deep passes 24.0 yds/play vs 11.2 in other games; WRs 9.4 yds/target vs 7.0 in other games; 3rd/4th downs converted 64% vs 42%; DAL is a strong offense (+0.11 EPA/play in its other games)
**Offenses like SFO that faced WAS:** IND (similarity 0.11: -1.8 pass / +1.0 run yds/play vs their norm), SEA (similarity 0.05: +1.9 pass / -1.7 run yds/play vs their norm), PHI (similarity 0.02: +2.1 pass / +1.9 run yds/play vs their norm) → SFO pass x0.99, run x1.01.
**WAS defensive scheme (online/tagged):** blitz: heavy, coverage: zone_heavy, shell: two_high [online (high)].
- WAS is soft deep (+0.68 EPA/deep att vs league +0.43); SFO throws deep 19%.
- WAS brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed +0.50 on 7 attempts. SFO 3rd-down deep share 23%.
- Best matchups: run_outside_left (x1.08), run_inside_left (x1.08); worst: pass_other (x1.00).
- Last game — worked: none; failed: pass_deep_right.
- WAS blitzes 46% of dropbacks (league 32%, FTN charting); SFO gains x1.30 as much per dropback vs the blitz as other offenses (46 blitzed dropbacks) -> pass yards x1.04
- SFO deep plays vs zone heavy coverage defenses: x0.95 vs how other offenses fare (12 plays)
- SFO run plays vs zone heavy coverage defenses: x1.05 vs how other offenses fare (41 plays)
- SFO deep-throw rate vs zone heavy coverage: x1.13
- SFO short plays vs two high shell defenses: x0.92 vs how other offenses fare (103 plays)
- WAS DBs out: Nick Cross (6 tgts, 7.9 yds/tgt allowed) -> coverage 7.8 → 7.8 yds/tgt; WR yards x1.00

| player              | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:--------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Brock Purdy         | QB    |     247.37 |      2.44 |            0.48 |      4.44 |      27.87 |      0.00 |         0.00 |      0.00 |         0.16 |
| Christian McCaffrey | RB    |       0.00 |      0.00 |            0.00 |     14.56 |      65.64 |      5.44 |         3.73 |     38.93 |         0.64 |
| Mike Evans          | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      7.81 |         5.22 |     73.35 |         0.54 |
| George Kittle       | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      7.02 |         4.83 |     63.73 |         0.52 |
| Deebo Samuel Sr.    | WR    |       0.00 |      0.00 |            0.00 |      2.20 |      10.08 |      4.53 |         3.19 |     36.32 |         0.37 |
| Kaelon Black        | RB    |       0.00 |      0.00 |            0.00 |      7.63 |      32.50 |      0.42 |         0.29 |      3.26 |         0.20 |

**SFO kicker**

| player       |   fg_made |   xp_made |   kicking_points |
|:-------------|----------:|----------:|-----------------:|
| Eddy Pineiro |      1.51 |      3.34 |             7.88 |

**SFO defenders (vs WAS offense)**

| player            |   tackles |   sacks |   def_int |
|:------------------|----------:|--------:|----------:|
| Fred Warner       |      9.97 |    0.09 |      0.00 |
| Dre Greenlaw      |      7.23 |    0.00 |      0.00 |
| Ji'Ayir Brown     |      6.65 |    0.00 |      0.00 |
| Marques Sigle     |      4.47 |    0.17 |      0.00 |
| Renardo Green     |      4.17 |    0.00 |      0.49 |
| Deommodore Lenoir |      3.88 |    0.00 |      0.00 |
| Jaden Dugger      |      3.68 |    0.27 |      0.00 |
| Malik Mustapha    |      3.50 |    0.00 |      0.00 |

## WAS vs SFO
**Clock:** 10.7 drives each; WAS 5.82 plays/drive at 37.4 s per clock-running play vs SFO 5.68 at 37.6 s → projected possession 50%, 62 plays to 61.
Projected 62 plays, 65% dropbacks, 33.2 pass att, 21.9 runs, 2.4 sacks. QB: Jayden Daniels
**Coaching style:** Deep-pass share high: 23% (league 19%); Shotgun rate high: 71% (league 61%); Pass rate on 3rd & short high: 54% (league 41%); 3rd-down conversion low: 32% (league 42%); EPA/run low: -0.15 (league -0.09); Favors run inside right (30%).
**Model game script:** projected 22.1 – 30.2 (margin -8.1) → dropback rate +3.3%.
**Weather:** forecast 59°F, wind 13 mph → pass yds x0.98, long FG x1.00.
**Strength of schedule:** own run yds x0.97, opp pass D x1.03, opp scoring D x1.02 (raw stats re-rated against the opponents actually faced).
**Out:** Stefon Diggs (carried from week 5 report: Out (Hamstring)), Marcus Mariota (carried from week 5 report: Out (Knee)), Charles Omenihu (carried from week 5 report: Out (Groin)), Nick Cross (carried from week 5 report: Out (Illness)), Percy Butler (carried from week 5 report: Out (Hamstring)), Tyler Owens (carried from week 5 report: Out (Hamstring)).
**Coach angle:** HC Dan Quinn (veteran HC, 11 prior seasons); plays called by OC David Blough (first-time play-caller, 0 seasons calling); no prior play-calling seasons: this season's data only; this season top target share 19%.
**SFO secondary:** DC Raheem Morris, mixed-leaning: Five-man fronts; dime with Lenoir / Green / Stout / Jack Jones; outside Renardo Green / Deommodore Lenoir; nickel Upton Stout; weak spot: Lenoir's coverage fell off in 2025 (65.7); [research confidence medium, 2026-10-14].

**What worked last game → this week vs SFO** (failed play types cut, volume moved to what worked; `SFO allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player        | type      | cut (failed last game)                                                         | more of                                                               | SFO allows there           |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:--------------|:----------|:-------------------------------------------------------------------------------|:----------------------------------------------------------------------|:---------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Dyami Brown   | receiving | short_right (100% failed), deep_left (100% failed)                             | short_left x1.2, short_middle x1.2, deep_right x1.2, deep_middle x1.2 | x0.93, x0.93, x0.93, x0.93 |        -0.0 |         0.7 |         0.0 |          0.0 |       26.8 |
| Chig Okonkwo  | receiving | short_right (50% failed), short_middle (100% failed), deep_right (100% failed) | short_left x1.1, deep_middle x1.1                                     | x0.93, x0.93               |         0.0 |         0.6 |         0.0 |          0.0 |       25.9 |
| Treylon Burks | receiving | short_left (67% failed), deep_left (100% failed)                               | short_middle x1.1                                                     | x0.93                      |        -0.0 |        -0.2 |         0.0 |          0.0 |       22.6 |
| Austin Ekeler | rushing   | run outside_left (100% failed), run outside_right (100% failed)                | run inside_left x1.1, run inside_right x1.1, run middle x1.1          | x0.91, x0.91, x0.91        |        -0.0 |         0.0 |         0.0 |         -0.0 |       11.5 |
| Rachaad White | rushing   | run inside_left (50% failed)                                                   | —                                                                     | —                          |        -0.0 |        -0.0 |         0.0 |         -0.0 |       32.5 |

**SFO defensive weak spots:** vs RBs: 5.8 yds/target (league 5.3), x1.12 for RBs.
- SFO struggle: Wk3 vs ARI: +0.17 EPA/play allowed (norm -0.17). Why: TEs 6.7 yds/target vs 3.6 in other games; when blitzing 5.3 yds/dropback vs 3.3 in other games; 3rd/4th downs converted 55% vs 38%
- SFO struggle: Wk4 vs DEN: +0.07 EPA/play allowed (norm -0.15). Why: RBs 8.0 yds/target vs 4.7 in other games
**Offenses like WAS that faced SFO:** ARI (similarity 0.10: +0.2 pass / +0.2 run yds/play vs their norm), MIA (similarity 0.05: -0.9 pass / -0.8 run yds/play vs their norm), DEN (similarity 0.04: -0.5 pass / -0.4 run yds/play vs their norm) → WAS pass x1.01, run x1.00.
**SFO defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy [online (high)].
- Best matchups: pass_other (x1.00), pass_short_left (x0.93); worst: run_outside_left (x0.91).
- SFO blitzes 33% of dropbacks (league 32%, FTN charting); WAS gains x0.88 as much per dropback vs the blitz as other offenses (55 blitzed dropbacks) -> pass yards x1.00
- WAS deep plays vs zone heavy coverage defenses: x0.93 vs how other offenses fare (15 plays)
- WAS short plays vs zone heavy coverage defenses: x0.93 vs how other offenses fare (58 plays)
- WAS run plays vs zone heavy coverage defenses: x0.92 vs how other offenses fare (57 plays)
- SFO DBs out: Marques Sigle (7 tgts, 7.6 yds/tgt allowed) -> coverage 7.7 → 7.7 yds/tgt; WR yards x1.01

| player                 | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-----------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Jayden Daniels         | QB    |     197.59 |      1.09 |            0.49 |      4.95 |      36.19 |      0.00 |         0.00 |      0.00 |         0.24 |
| Jacory Croskey-Merritt | RB    |       0.00 |      0.00 |            0.00 |     12.30 |      44.50 |      1.84 |         1.18 |     10.58 |         0.38 |
| Terry McLaurin         | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.08 |         3.64 |     42.52 |         0.18 |
| Antonio Williams       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.94 |         3.75 |     35.35 |         0.17 |
| Rachaad White          | RB    |       0.00 |      0.00 |            0.00 |      5.23 |      19.17 |      2.24 |         1.52 |     12.77 |         0.23 |
| Chig Okonkwo           | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.77 |         2.33 |     24.35 |         0.10 |
| Treylon Burks          | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.32 |         1.99 |     21.80 |         0.16 |
| Dyami Brown            | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.56 |         2.09 |     24.98 |         0.10 |
| Austin Ekeler          | RB    |       0.00 |      0.00 |            0.00 |      1.55 |       5.60 |      0.95 |         0.60 |      5.56 |         0.09 |
| Kaytron Allen          | RB    |       0.00 |      0.00 |            0.00 |      1.83 |       6.65 |      0.00 |         0.00 |      0.00 |         0.06 |

**WAS kicker**

| player       |   fg_made |   xp_made |   kicking_points |
|:-------------|----------:|----------:|-----------------:|
| Drew Stevens |      2.34 |      1.87 |             8.88 |

**WAS defenders (vs SFO offense)**

| player          |   tackles |   sacks |   def_int |
|:----------------|----------:|--------:|----------:|
| Sonny Styles    |      7.26 |    0.12 |      0.15 |
| Jeremy Reaves   |      6.86 |    0.00 |      0.00 |
| Amik Robertson  |      6.66 |    0.00 |      0.00 |
| Rasul Douglas   |      5.26 |    0.00 |      0.18 |
| Quan Martin     |      4.93 |    0.00 |      0.00 |
| Frankie Luvu    |      4.08 |    0.13 |      0.00 |
| Mike Sainristil |      3.04 |    0.00 |      0.00 |
| Daron Payne     |      2.41 |    0.26 |      0.00 |
