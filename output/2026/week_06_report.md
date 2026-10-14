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

|   rank | player         | team   | stat    | direction   |   baseline |   projected_median |   prob | signals                                                                                       |
|-------:|:---------------|:-------|:--------|:------------|-----------:|-------------------:|-------:|:----------------------------------------------------------------------------------------------|
|      1 | Jeremiyah Love | ARI    | carries | under       |      13.60 |              11.00 |   0.80 | usage trending down (13.7 → 13.0); game script +6.8% dropbacks                                |
|      2 | Tyler Higbee   | LAR    | targets | under       |       6.50 |               5.00 |   0.80 | usage trending down (6.5 → 6.0); game script -6.8% dropbacks                                  |
|      3 | Kyren Williams | LAR    | carries | over        |      14.50 |              18.00 |   0.79 | usage trending up (12.7 → 16.0); game script -6.8% dropbacks; team total +14.6 vs its average |
|      4 | Davante Adams  | LAR    | targets | under       |       9.00 |               7.00 |   0.74 | usage trending down (9.7 → 8.0); game script -6.8% dropbacks                                  |
|      5 | Trey McBride   | ARI    | rec_yds | under       |      59.60 |              50.60 |   0.63 | matchup pass x0.94; coverage x0.82; similar offenses x0.96                                    |

**ATL @ CHI**

|   rank | player           | team   | stat     | direction   |   baseline |   projected_median |   prob | signals                                                                                        |
|-------:|:-----------------|:-------|:---------|:------------|-----------:|-------------------:|-------:|:-----------------------------------------------------------------------------------------------|
|      1 | Bijan Robinson   | ATL    | rush_yds | under       |     117.90 |              75.70 |   0.89 | usage trending down (22.0 → 18.0); game script +1.0% dropbacks; team total -2.4 vs its average |
|      2 | Brian Robinson   | ATL    | carries  | under       |      10.10 |               7.00 |   0.87 | usage trending down (10.0 → 10.5); game script +1.0% dropbacks; team total -2.4 vs its average |
|      3 | Colston Loveland | CHI    | rec_yds  | over        |      24.90 |              36.30 |   0.67 | coverage x1.06; usage trending up (3.0 → 7.0)                                                  |

**BAL @ CLE**

|   rank | player           | team   | stat     | direction   |   baseline |   projected_median |   prob | signals                                                                         |
|-------:|:-----------------|:-------|:---------|:------------|-----------:|-------------------:|-------:|:--------------------------------------------------------------------------------|
|      1 | Zay Flowers      | BAL    | rec_yds  | under       |      94.00 |              44.50 |   0.90 | matchup pass x0.87; game script -1.7% dropbacks; team total -6.3 vs its average |
|      2 | Quinshon Judkins | CLE    | rush_yds | over        |      45.90 |              58.20 |   0.70 | matchup run x1.10; usage trending up (14.0 → 15.5)                              |
|      3 | Derrick Henry    | BAL    | rush_yds | over        |      93.00 |             111.30 |   0.70 | matchup run x1.07; game script -1.7% dropbacks                                  |

**BUF @ LVR**

|   rank | player        | team   | stat       | direction   |   baseline |   projected_median |   prob | signals                                                                    |
|-------:|:--------------|:-------|:-----------|:------------|-----------:|-------------------:|-------:|:---------------------------------------------------------------------------|
|      1 | Michael Mayer | LVR    | targets    | over        |       4.80 |               6.00 |   0.78 | coverage x1.03; usage trending up (4.7 → 5.5); game script +1.7% dropbacks |
|      2 | DJ Moore      | BUF    | targets    | under       |       6.20 |               4.00 |   0.92 | usage trending down (8.0 → 6.0); game script -1.7% dropbacks               |
|      3 | Ashton Jeanty | LVR    | receptions | over        |       4.30 |               5.00 |   0.59 | coverage x1.02; usage trending up (5.3 → 7.0); game script +1.7% dropbacks |
|      4 | Tre Tucker    | LVR    | receptions | over        |       3.90 |               4.00 |   0.65 | usage trending up (5.0 → 6.5); game script +1.7% dropbacks                 |
|      5 | James Cook    | BUF    | rush_yds   | over        |     107.50 |             113.60 |   0.57 | matchup run x1.13; game script -1.7% dropbacks                             |

**CAR @ PHI**

|   rank | player           | team   | stat     | direction   |   baseline |   projected_median |   prob | signals                                                                                           |
|-------:|:-----------------|:-------|:---------|:------------|-----------:|-------------------:|-------:|:--------------------------------------------------------------------------------------------------|
|      1 | Dontayvion Wicks | PHI    | targets  | over        |       5.80 |               8.00 |   0.83 | matchup pass x1.04; coverage x1.03; usage trending up (5.0 → 6.5); team total +3.6 vs its average |
|      2 | Makai Lemon      | PHI    | targets  | over        |       4.80 |               6.00 |   0.77 | matchup pass x1.04; coverage x1.03; usage trending up (3.0 → 6.5); team total +3.6 vs its average |
|      3 | Chuba Hubbard    | CAR    | carries  | over        |      16.00 |              20.00 |   0.81 | matchup run x1.10; usage trending up (11.0 → 19.5)                                                |
|      4 | Jalen Coker      | CAR    | targets  | under       |       7.00 |               5.00 |   0.88 | usage trending down (9.0 → 6.5); team total -6.3 vs its average                                   |
|      5 | Jalen Hurts      | PHI    | pass_yds | over        |     182.50 |             235.00 |   0.77 | matchup pass x1.04; team total +3.6 vs its average                                                |

**DAL @ GNB**

|   rank | player           | team   | stat     | direction   |   baseline |   projected_median |   prob | signals                                                                                                       |
|-------:|:-----------------|:-------|:---------|:------------|-----------:|-------------------:|-------:|:--------------------------------------------------------------------------------------------------------------|
|      1 | MarShawn Lloyd   | GNB    | rush_yds | over        |      22.00 |              55.30 |   0.95 | matchup run x1.08; usage trending up (7.7 → 8.5); game script -1.4% dropbacks; team total +9.7 vs its average |
|      2 | Christian Watson | GNB    | rec_yds  | under       |      95.60 |              60.80 |   0.77 | usage trending down (9.7 → 5.5); game script -1.4% dropbacks                                                  |
|      3 | Matthew Golden   | GNB    | rec_yds  | under       |      80.50 |              61.30 |   0.68 | usage trending down (10.0 → 7.0); game script -1.4% dropbacks                                                 |
|      4 | Ryan Flournoy    | DAL    | rec_yds  | under       |      44.30 |              33.10 |   0.66 | matchup pass x0.96; coverage x0.97; usage trending down (6.0 → 4.5)                                           |

**DEN @ SEA**

|   rank | player             | team   | stat        | direction   |   baseline |   projected_median |   prob | signals                                                                                       |
|-------:|:-------------------|:-------|:------------|:------------|-----------:|-------------------:|-------:|:----------------------------------------------------------------------------------------------|
|      1 | Emanuel Wilson     | SEA    | carries     | over        |      15.80 |              21.00 |   0.91 | usage trending up (10.7 → 20.5); game script -2.0% dropbacks                                  |
|      2 | RJ Harvey          | DEN    | receptions  | under       |       4.80 |               3.00 |   0.82 | matchup pass x0.88; usage trending down (5.5 → 5.5)                                           |
|      3 | Jaxon Smith-Njigba | SEA    | receptions  | under       |       7.00 |               6.00 |   0.69 | usage trending down (12.0 → 7.0); game script -2.0% dropbacks; team total -2.1 vs its average |
|      4 | Sam Darnold        | SEA    | completions | under       |      20.00 |              18.00 |   0.67 | game script -2.0% dropbacks; team total -2.1 vs its average                                   |

**HOU @ JAX**

|   rank | player          | team   | stat       | direction   |   baseline |   projected_median |   prob | signals                                                          |
|-------:|:----------------|:-------|:-----------|:------------|-----------:|-------------------:|-------:|:-----------------------------------------------------------------|
|      1 | Nico Collins    | HOU    | receptions | under       |       6.10 |               4.00 |   0.93 | usage trending down (10.0 → 7.5); team total -5.1 vs its average |
|      2 | Brenton Strange | JAX    | targets    | over        |       5.80 |               6.00 |   0.61 | coverage x1.03; usage trending up (3.3 → 8.0)                    |

**IND @ TEN**

|   rank | player          | team   | stat       | direction   |   baseline |   projected_median |   prob | signals                                                                                    |
|-------:|:----------------|:-------|:-----------|:------------|-----------:|-------------------:|-------:|:-------------------------------------------------------------------------------------------|
|      1 | Jonathan Taylor | IND    | rush_yds   | over        |      76.00 |             101.40 |   0.80 | matchup run x1.12; game script -5.2% dropbacks; team total +5.9 vs its average             |
|      2 | Carnell Tate    | TEN    | receptions | over        |       4.60 |               6.00 |   0.72 | usage trending up (6.7 → 8.5); game script +5.2% dropbacks; team total +6.1 vs its average |
|      3 | Josh Downs      | IND    | targets    | under       |       6.70 |               6.00 |   0.63 | usage trending down (8.0 → 5.0); game script -5.2% dropbacks                               |

**KAN @ LAC**

|   rank | player             | team   | stat     | direction   |   baseline |   projected_median |   prob | signals                                                                                                          |
|-------:|:-------------------|:-------|:---------|:------------|-----------:|-------------------:|-------:|:-----------------------------------------------------------------------------------------------------------------|
|      1 | Patrick Mahomes    | KAN    | pass_yds | under       |     258.20 |             204.40 |   0.78 | matchup pass x0.92; game script -3.2% dropbacks; team total -4.1 vs its average                                  |
|      2 | Travis Kelce       | KAN    | rec_yds  | under       |      56.70 |              35.30 |   0.74 | matchup pass x0.92; usage trending down (8.0 → 3.0); game script -3.2% dropbacks; team total -4.1 vs its average |
|      3 | Kenneth Walker III | KAN    | rush_yds | under       |     134.10 |             113.90 |   0.71 | usage trending down (23.5 → 20.0); team total -4.1 vs its average                                                |
|      4 | Ladd McConkey      | LAC    | rec_yds  | under       |      41.10 |              21.80 |   0.76 | coverage x0.93; usage trending down (5.0 → 3.5)                                                                  |
|      5 | Omarion Hampton    | LAC    | carries  | under       |      14.20 |              13.00 |   0.67 | usage trending down (16.7 → 11.5); game script +3.2% dropbacks                                                   |

**NOR @ NYG**

|   rank | player        | team   | stat       | direction   |   baseline |   projected_median |   prob | signals                                                                                                 |
|-------:|:--------------|:-------|:-----------|:------------|-----------:|-------------------:|-------:|:--------------------------------------------------------------------------------------------------------|
|      1 | Alvin Kamara  | NOR    | rec_yds    | over        |       9.90 |              21.70 |   0.75 | coverage x1.03; usage trending up (3.5 → 4.5); game script +2.9% dropbacks                              |
|      2 | Chris Olave   | NOR    | rec_yds    | under       |      99.20 |              64.30 |   0.82 | similar offenses x0.96; usage trending down (12.0 → 9.0); team total -4.0 vs its average                |
|      3 | Noah Fant     | NOR    | receptions | under       |       2.60 |               2.00 |   0.68 | coverage x0.95; similar offenses x0.96; usage trending down (8.0 → 2.5); team total -4.0 vs its average |
|      4 | Juwan Johnson | NOR    | receptions | under       |       5.10 |               5.00 |   0.63 | coverage x0.95; similar offenses x0.96; usage trending down (6.3 → 6.5); team total -4.0 vs its average |
|      5 | Cam Skattebo  | NYG    | rush_yds   | over        |      58.20 |              67.70 |   0.64 | game script -2.9% dropbacks; team total +5.0 vs its average                                             |

**NWE @ NYJ**

|   rank | player              | team   | stat       | direction   |   baseline |   projected_median |   prob | signals                                                                   |
|-------:|:--------------------|:-------|:-----------|:------------|-----------:|-------------------:|-------:|:--------------------------------------------------------------------------|
|      1 | Romeo Doubs         | NWE    | receptions | over        |       2.70 |               3.00 |   0.71 | matchup pass x1.04; similar offenses x1.03; usage trending up (3.7 → 6.0) |
|      2 | Rhamondre Stevenson | NWE    | carries    | over        |      11.40 |              13.00 |   0.67 | usage trending up (10.3 → 13.0); game script -1.6% dropbacks              |

**PIT @ TAM**

|   rank | player        | team   | stat       | direction   |   baseline |   projected_median |   prob | signals                                                 |
|-------:|:--------------|:-------|:-----------|:------------|-----------:|-------------------:|-------:|:--------------------------------------------------------|
|      1 | Ted Hurst III | TAM    | rec_yds    | under       |      31.50 |              10.20 |   0.83 | matchup pass x0.91; usage trending down (5.0 → 3.0)     |
|      2 | Bucky Irving  | TAM    | receptions | under       |       3.30 |               2.00 |   0.79 | matchup pass x0.91; usage trending down (5.5 → 3.5)     |
|      3 | Jaylen Warren | PIT    | carries    | over        |      14.50 |              15.00 |   0.59 | similar offenses x1.02; usage trending up (12.7 → 16.0) |

**SFO @ WAS**

|   rank | player                 | team   | stat     | direction   |   baseline |   projected_median |   prob | signals                                                                           |
|-------:|:-----------------------|:-------|:---------|:------------|-----------:|-------------------:|-------:|:----------------------------------------------------------------------------------|
|      1 | Antonio Williams       | WAS    | targets  | over        |       4.50 |               6.00 |   0.73 | usage trending up (3.7 → 5.5); game script +3.4% dropbacks                        |
|      2 | George Kittle          | SFO    | targets  | over        |       5.70 |               7.00 |   0.73 | coverage x1.10; usage trending up (5.3 → 6.0)                                     |
|      3 | Christian McCaffrey    | SFO    | carries  | over        |      12.40 |              14.00 |   0.67 | matchup run x1.07; usage trending up (11.7 → 13.0); game script -3.4% dropbacks   |
|      4 | Terry McLaurin         | WAS    | rec_yds  | under       |      54.70 |              39.20 |   0.69 | matchup pass x0.91; usage trending down (6.5 → 6.5)                               |
|      5 | Jacory Croskey-Merritt | WAS    | rush_yds | under       |      48.60 |              40.60 |   0.63 | matchup run x0.90; usage trending down (15.7 → 10.0); game script +3.4% dropbacks |

## Projected team totals (model)

`model_points` = simulated 6 x TD + extra points + 3 x field goals before game script; `final_points` = after game script (and the market blend for qualifying teams).

| team   | opp   |   model_points |   final_points |
|:-------|:------|---------------:|---------------:|
| DEN    | SEA   |           19.6 |           19.4 |
| SEA    | DEN   |           24.7 |           24.3 |
| JAX    | HOU   |           23.5 |           23.4 |
| HOU    | JAX   |           16.9 |           16.6 |
| ATL    | CHI   |           21.4 |           21.2 |
| CHI    | ATL   |           23.8 |           23.8 |
| CLE    | BAL   |           18.7 |           19.0 |
| BAL    | CLE   |           22.9 |           23.3 |
| IND    | TEN   |           30.7 |           29.6 |
| TEN    | IND   |           17.7 |           17.6 |
| NWE    | NYJ   |           20.9 |           20.4 |
| NYJ    | NWE   |           16.8 |           17.2 |
| NYG    | NOR   |           26.8 |           26.2 |
| NOR    | NYG   |           19.6 |           19.1 |
| PHI    | CAR   |           22.0 |           20.3 |
| CAR    | PHI   |           23.9 |           23.6 |
| TAM    | PIT   |           20.2 |           19.5 |
| PIT    | TAM   |           21.3 |           21.0 |
| LAR    | ARI   |           38.4 |           37.2 |
| ARI    | LAR   |           21.4 |           21.9 |
| KAN    | LAC   |           25.4 |           25.2 |
| LAC    | KAN   |           17.5 |           17.4 |
| LVR    | BUF   |           27.0 |           27.7 |
| BUF    | LVR   |           31.3 |           31.1 |
| GNB    | DAL   |           30.5 |           29.0 |
| DAL    | GNB   |           27.1 |           27.2 |
| SFO    | WAS   |           30.1 |           30.1 |
| WAS    | SFO   |           21.6 |           21.8 |

## Market team totals: which teams qualify

Only teams that landed within 4 points of their implied team total in at least 60% of their games (min 4) get the market blended in (60% market). Everyone else is model only. No spreads are used.

| team   |   games |   hit_rate |   abs_miss |   implied_avg |   scored_avg | qualifies   |
|:-------|--------:|-----------:|-----------:|--------------:|-------------:|:------------|
| PHI    |       5 |       0.80 |       3.60 |         21.50 |        18.40 | True        |
| NYJ    |       5 |       0.80 |       4.35 |         20.25 |        18.60 | True        |
| IND    |       5 |       0.60 |       3.65 |         21.55 |        24.80 | True        |
| TAM    |       5 |       0.60 |       4.35 |         21.35 |        20.00 | True        |
| GNB    |       5 |       0.60 |       5.35 |         22.75 |        20.80 | True        |
| DET    |       5 |       0.60 |       5.80 |         28.00 |        32.80 | True        |
| KAN    |       4 |       0.50 |       5.75 |         25.62 |        29.50 | False       |
| NOR    |       5 |       0.40 |       4.95 |         21.45 |        23.60 | False       |
| CIN    |       5 |       0.40 |       5.30 |         24.80 |        25.60 | False       |
| LAR    |       5 |       0.40 |       6.00 |         25.20 |        23.80 | False       |
| DEN    |       5 |       0.40 |       6.05 |         22.45 |        19.40 | False       |
| ARI    |       5 |       0.40 |       6.40 |         21.40 |        21.60 | False       |
| WAS    |       5 |       0.40 |       7.35 |         20.45 |        23.00 | False       |
| MIN    |       5 |       0.40 |       7.65 |         22.65 |        21.80 | False       |
| TEN    |       5 |       0.40 |       7.95 |         17.05 |        11.60 | False       |
| PIT    |       5 |       0.40 |       8.95 |         20.85 |        22.20 | False       |
| ATL    |       5 |       0.40 |      12.00 |         20.80 |        23.80 | False       |
| CAR    |       4 |       0.25 |       9.44 |         22.81 |        30.25 | False       |
| MIA    |       5 |       0.20 |       5.20 |         17.10 |        14.00 | False       |
| CLE    |       5 |       0.20 |       5.80 |         17.60 |        18.60 | False       |
| SFO    |       5 |       0.20 |       6.30 |         25.20 |        30.80 | False       |
| JAX    |       5 |       0.20 |       7.25 |         23.95 |        24.60 | False       |
| LVR    |       5 |       0.20 |       7.45 |         20.55 |        26.40 | False       |
| LAC    |       5 |       0.20 |       7.70 |         22.40 |        16.80 | False       |
| HOU    |       5 |       0.20 |       8.10 |         23.00 |        22.00 | False       |
| BUF    |       5 |       0.20 |       8.40 |         27.20 |        32.80 | False       |
| BAL    |       5 |       0.20 |       8.70 |         25.70 |        29.20 | False       |
| NWE    |       5 |       0.20 |      11.55 |         22.25 |        22.00 | False       |
| CHI    |       5 |       0.20 |      16.25 |         23.55 |        23.80 | False       |
| SEA    |       5 |       0.00 |       7.15 |         23.95 |        26.80 | False       |
| DAL    |       5 |       0.00 |       9.05 |         26.05 |        27.60 | False       |
| NYG    |       5 |       0.00 |      10.25 |         20.55 |        21.80 | False       |

## DEN vs SEA
Projected 58 plays, 62% dropbacks, 33.4 pass att, 22.0 runs, 1.3 sacks. QB: Bo Nix
**Coaching style:** Deep-pass share low: 12% (league 19%); 3rd-down deep share low: 14% (league 21%); 4th-down go rate low: 8% (league 19%); Sack rate low: 3% (league 6%); Pass rate on 2nd & short low: 0% (league 31%); EPA/dropback low: -0.08 (league +0.06); Favors run middle (35%).
**Model game script:** projected 19.6 – 24.7 (margin -5.1) → dropback rate +2.0%.
**Weather:** forecast 46°F, wind 5 mph → pass yds x1.00, long FG x1.00.
**Strength of schedule:** own pass yds x1.03, own run yds x1.04, own scoring x1.05 (raw stats re-rated against the opponents actually faced).
**Out:** Pat Surtain II (carried from week 5 report: Out (Ankle)), Riley Moss (carried from week 5 report: Out (Ribs)).
**Coach angle:** HC Sean Payton (veteran HC, 20 prior seasons); plays called by OC Davis Webb (first-time play-caller, 0 seasons calling); no prior play-calling seasons: this season's data only; this season top target share 22%.
**SEA secondary:** DC Mike Macdonald, mixed-leaning: Witherspoon stays at nickel (run fits / screens / blitzes); Emmanwori can also play inside; outside Devon Witherspoon / Josh Jobe; nickel Nick Emmanwori; note: depth chart lists Devon Witherspoon outside but reporting has him at nickel; weak spot: Outside corners tested (Mike Evans 113 yards in the SF loss); [research confidence medium, 2026-10-14].

**What worked last game → this week vs SEA** (failed play types cut, volume moved to what worked; `SEA allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player              | cut (failed last game)                                                         | more of                                                                                    | SEA allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:--------------------|:-------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Jaylen Waddle       | short_right (100% failed), short_left (33% failed), short_middle (100% failed) | deep_middle x2.5, short_left x1.6, deep_left x2.5, deep_right x2.5                         | x1.01, x0.90, x0.93, x0.96        |        -0.0 |        12.6 |         0.0 |          0.0 |       55.8 |
| Courtland Sutton    | short_left (100% failed)                                                       | deep_middle x1.8, short_right x1.8, deep_left x1.8, short_middle x1.8, deep_right x1.8     | x1.01, x0.85, x0.93, x0.83, x0.96 |        -0.0 |         4.9 |         0.0 |          0.0 |       34.3 |
| Evan Engram         | short_right (100% failed), short_left (50% failed)                             | deep_middle x2.2, short_left x1.1, deep_left x2.2, short_middle x2.2, deep_right x2.2      | x1.01, x0.90, x0.93, x0.83, x0.96 |         0.0 |         4.6 |         0.0 |          0.0 |       23.7 |
| Tyler Badie         | short_right (100% failed)                                                      | deep_middle x1.5, short_left x1.5, deep_left x1.5, short_middle x1.5, deep_right x1.5      | x1.01, x0.90, x0.93, x0.83, x0.96 |         0.0 |         2.3 |        -0.0 |          0.4 |       17.4 |
| Tyler Badie         | run middle (100% failed)                                                       | run outside_left x1.6, run inside_right x1.6, run outside_right x1.6, run inside_left x1.6 | x0.92, x1.02, x1.02, x0.96        |         0.0 |         2.3 |        -0.0 |          0.4 |       17.4 |
| RJ Harvey           | short_left (100% failed)                                                       | deep_middle x1.6, short_right x1.6, deep_left x1.6, short_middle x1.6, deep_right x1.6     | x1.01, x0.85, x0.93, x0.83, x0.96 |         0.0 |        -1.5 |         0.0 |          0.0 |       42.2 |
| Troy Franklin       | short_right (100% failed)                                                      | deep_middle x1.8, short_left x1.8, deep_left x1.8, short_middle x1.8, deep_right x1.8      | x1.01, x0.90, x0.93, x0.83, x0.96 |        -0.0 |         1.3 |         0.0 |         -0.0 |        9.1 |
| Lil'Jordan Humphrey | short_right (50% failed)                                                       | deep_middle x1.5, short_left x1.5, deep_left x1.5, short_middle x1.5, deep_right x1.5      | x1.01, x0.90, x0.93, x0.83, x0.96 |        -0.0 |         0.3 |         0.0 |          0.0 |        4.8 |

**SEA defensive weak spots:** red-zone TDs per play: 32% allowed vs league 21% (28 plays); vs RBs: 5.1 yds/target (league 5.3), x1.08 for RBs.
**Offenses like DEN that faced SEA:** ARI (similarity 0.23: -2.6 pass / -0.7 run yds/play vs their norm), SFO (similarity 0.06: -4.5 pass / +0.1 run yds/play vs their norm), WAS (similarity 0.04: -1.1 pass / -1.3 run yds/play vs their norm) → DEN pass x1.00, run x1.00.
**SEA defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: two_high [online (high)].
- Best matchups: run_inside_right (x1.02), run_outside_right (x1.02); worst: pass_short_middle (x0.83).
- SEA blitzes 21% of dropbacks (league 32%, FTN charting); DEN gains x0.75 as much per dropback vs the blitz as other offenses (57 blitzed dropbacks) -> pass yards x1.03
- DEN deep plays vs zone heavy coverage defenses: x0.95 vs how other offenses fare (7 plays)
- DEN deep plays vs two high shell defenses: x1.08 vs how other offenses fare (13 plays)
- SEA vs position groups: Evan Engram x0.92, RJ Harvey x1.08

| player           | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-----------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Bo Nix           | QB    |     195.22 |      1.45 |            1.01 |      2.85 |      14.20 |      0.00 |         0.00 |      0.00 |         0.09 |
| Jaylen Waddle    | WR    |       0.00 |      0.00 |            0.00 |      0.42 |       1.83 |      7.38 |         4.83 |     53.63 |         0.29 |
| J.K. Dobbins     | RB    |       0.00 |      0.00 |            0.00 |     14.57 |      56.26 |      1.50 |         1.04 |      8.68 |         0.33 |
| RJ Harvey        | RB    |       0.00 |      0.00 |            0.00 |      3.23 |      12.60 |      4.45 |         2.96 |     24.43 |         0.22 |
| Courtland Sutton | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.49 |         2.57 |     30.81 |         0.19 |
| Evan Engram      | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.54 |         2.19 |     22.48 |         0.18 |
| Pat Bryant       | WR    |       0.00 |      0.00 |            0.00 |      0.13 |       0.58 |      2.23 |         1.47 |     14.02 |         0.12 |
| Tyler Badie      | RB    |       0.00 |      0.00 |            0.00 |      0.99 |       4.06 |      1.70 |         1.26 |     12.85 |         0.10 |

**DEN kicker**

| player   |   fg_made |   xp_made |   kicking_points |
|:---------|----------:|----------:|-----------------:|
| Wil Lutz |      1.76 |      1.94 |             7.22 |

**DEN defenders (vs SEA offense)**

| player          |   tackles |   sacks |   def_int |
|:----------------|----------:|--------:|----------:|
| Alex Singleton  |     10.35 |    0.00 |      0.00 |
| Brandon Jones   |      7.11 |    0.00 |      0.44 |
| Justin Strnad   |      5.69 |    0.00 |      0.00 |
| Talanoa Hufanga |      4.27 |    0.19 |      0.43 |
| Pat Surtain II  |      3.93 |    0.00 |      0.00 |
| Que Robinson    |      3.91 |    0.16 |      0.00 |
| Zach Allen      |      3.27 |    0.74 |      0.00 |
| Malcolm Roach   |      3.27 |    0.17 |      0.00 |

## SEA vs DEN
Projected 62 plays, 52% dropbacks, 28.9 pass att, 29.5 runs, 2.8 sacks. QB: Sam Darnold
**Coaching style:** Neutral-script pass rate low: 55% (league 59%); Early-down pass rate low: 47% (league 53%); Sack rate high: 8% (league 6%); Shotgun rate low: 47% (league 61%); No-huddle rate low: 1% (league 6%); 3rd-down conversion low: 29% (league 42%); EPA/run low: -0.29 (league -0.09).
**Model game script:** projected 24.7 – 19.6 (margin +5.1) → dropback rate -2.0%.
**Weather:** forecast 46°F, wind 5 mph → pass yds x1.00, long FG x1.00.
**Strength of schedule:** opp pass D x0.96, opp run D x0.98 (raw stats re-rated against the opponents actually faced).
**Out:** Chazz Surratt (carried from week 5 report: Out (Calf)), Zach Charbonnet (carried from week 5 report: Out (Knee)), Julian Neal (carried from week 5 report: Out (Hamstring)).
**Coach angle:** HC Mike Macdonald (young HC, 2 prior seasons); plays called by OC Brian Fleury (first-time play-caller, 0 seasons calling); no prior play-calling seasons: this season's data only; this season top target share 34%.
**DEN secondary:** DC Vance Joseph, man-leaning: Man-heavy with Cover 1 among the league's most used; pressure plan built around Surtain's assignment; outside Pat Surtain II (OUT) / Riley Moss (OUT); nickel Ja'Quan McMillian; weak spot: Without Surtain the replacements (Barron / Abrams-Draine) take the boundary; Riley Moss also out; [research confidence medium, 2026-10-14].

**What worked last game → this week vs DEN** (failed play types cut, volume moved to what worked; `DEN allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player             | cut (failed last game)                                                                                                 | more of                                                                                 | DEN allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:-------------------|:-----------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Jaxon Smith-Njigba | short_right (50% failed), deep_left (50% failed)                                                                       | short_middle x1.3, short_left x1.3, deep_middle x1.3, deep_right x1.3                   | x1.03, x1.19, x0.92, x0.87        |         0.0 |         6.7 |        -0.0 |         -0.0 |       98.6 |
| George Holani      | short_right (100% failed), short_left (50% failed)                                                                     | short_middle x2.2, deep_left x2.2, short_left x1.1, deep_middle x2.2, deep_right x2.2   | x1.03, x0.79, x1.19, x0.92, x0.87 |         0.0 |         3.6 |        -0.0 |         -0.5 |       50.2 |
| George Holani      | run inside_left (100% failed), run outside_right (33% failed)                                                          | run inside_right x1.4, run middle x1.4, run outside_left x1.4                           | x0.89, x1.06, x0.99               |         0.0 |         3.6 |        -0.0 |         -0.5 |       50.2 |
| Emanuel Wilson     | run inside_right (20% failed), run middle (14% failed), run outside_right (25% failed), run outside_left (100% failed) | run inside_right x1.1, run middle x1.1, run inside_left x1.3                            | x0.89, x1.06, x1.04               |         0.0 |         0.0 |         0.0 |         -3.2 |       92.3 |
| AJ Barner          | short_right (67% failed)                                                                                               | short_middle x1.5, deep_left x1.5, short_left x1.5, deep_middle x1.5, deep_right x1.5   | x1.03, x0.79, x1.19, x0.92, x0.87 |         0.0 |         2.7 |        -0.0 |         -0.0 |       39.6 |
| Rashid Shaheed     | short_left (100% failed), deep_right (100% failed)                                                                     | short_middle x1.6, short_right x1.6, deep_left x1.6, deep_middle x1.6                   | x1.03, x0.95, x0.79, x0.92        |         0.0 |        -2.5 |        -0.0 |         -0.0 |       32.0 |
| Cooper Kupp        | short_middle (100% failed), short_left (100% failed)                                                                   | short_right x1.7, deep_left x1.7, deep_middle x1.7, deep_right x1.7                     | x0.95, x0.79, x0.92, x0.87        |         0.0 |        -1.4 |         0.0 |          0.0 |       24.0 |
| Elijah Arroyo      | deep_left (100% failed)                                                                                                | short_middle x1.3, short_right x1.3, short_left x1.3, deep_middle x1.3, deep_right x1.3 | x1.03, x0.95, x1.19, x0.92, x0.87 |         0.0 |        -0.0 |         0.0 |          0.0 |        3.3 |

**DEN defensive weak spots:** 3rd-down conversions: 49% allowed vs league 42% (76 plays); outside runs: 5.7 allowed vs league 4.9 (47 plays); vs TEs: 8.1 yds/target (league 7.2), x1.06 for TEs.
- DEN struggle: Wk1 vs KAN: +0.19 EPA/play allowed (norm -0.08). Why: outside runs 13.6 yds/play vs 4.1 in other games; TEs 13.2 yds/target vs 7.1 in other games; red-zone TD rate per play 33% vs 15%; KAN is a strong offense (+0.18 EPA/play in its other games)
- DEN struggle: Wk4 vs SFO: +0.12 EPA/play allowed (norm -0.06). Why: when blitzing 8.7 yds/dropback vs 5.2 in other games; TEs 11.7 yds/target vs 7.4 in other games; SFO is a strong offense (+0.28 EPA/play in its other games); short passes 7.3 yds/play vs 6.1 in other games
**Offenses like SEA that faced DEN:** JAX (similarity 0.32: -2.1 pass / -0.4 run yds/play vs their norm), KAN (similarity 0.12: -1.9 pass / +1.7 run yds/play vs their norm), LAC (similarity 0.05: -2.1 pass / +0.0 run yds/play vs their norm) → SEA pass x0.99, run x1.00.
**DEN defensive scheme (online/tagged):** blitz: heavy, coverage: avg, shell: two_high [online (high)].
- DEN brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed -1.10 on 7 attempts. SEA 3rd-down deep share 19%.
- Best matchups: pass_short_left (x1.19), run_middle (x1.06); worst: pass_deep_left (x0.79).
- SEA short plays vs two high shell defenses: x1.11 vs how other offenses fare (86 plays)
- DEN DBs out: Riley Moss (22 tgts, 7.3 yds/tgt allowed), Patrick Surtain II (18 tgts, 7.1 yds/tgt allowed) -> coverage 7.7 → 8.2 yds/tgt; WR yards x1.06
- DEN shadow corner Pat Surtain II is out: no shadow this week
- DEN vs position groups: AJ Barner x1.06

| player             | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Sam Darnold        | QB    |     236.61 |      1.70 |            1.06 |      0.81 |       6.26 |      0.00 |         0.00 |      0.00 |         0.02 |
| Jaxon Smith-Njigba | WR    |       0.00 |      0.00 |            0.00 |      0.32 |       1.36 |      9.73 |         6.34 |     93.22 |         0.57 |
| Emanuel Wilson     | RB    |       0.00 |      0.00 |            0.00 |     21.49 |      79.54 |      1.74 |         1.13 |     12.35 |         0.52 |
| George Holani      | RB    |       0.00 |      0.00 |            0.00 |      6.94 |      26.67 |      2.70 |         1.85 |     23.45 |         0.29 |
| AJ Barner          | TE    |       0.00 |      0.00 |            0.00 |      0.21 |       0.88 |      4.47 |         2.83 |     37.57 |         0.20 |
| Rashid Shaheed     | WR    |       0.00 |      0.00 |            0.00 |      0.63 |       2.97 |      3.81 |         2.36 |     28.18 |         0.14 |
| Cooper Kupp        | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.10 |         1.80 |     23.50 |         0.16 |

**SEA kicker**

| player      |   fg_made |   xp_made |   kicking_points |
|:------------|----------:|----------:|-----------------:|
| Jason Myers |      2.02 |      2.47 |             8.53 |

**SEA defenders (vs DEN offense)**

| player            |   tackles |   sacks |   def_int |
|:------------------|----------:|--------:|----------:|
| Ernest Jones      |      8.99 |    0.23 |      0.18 |
| Drake Thomas      |      6.05 |    0.07 |      0.19 |
| Devon Witherspoon |      5.76 |    0.00 |      0.00 |
| Julian Love       |      3.77 |    0.00 |      0.23 |
| Josh Jobe         |      3.61 |    0.00 |      0.10 |
| Byron Murphy II   |      3.51 |    0.36 |      0.00 |
| Nick Emmanwori    |      3.40 |    0.11 |      0.00 |
| Uchenna Nwosu     |      2.78 |    0.10 |      0.00 |

## JAX vs HOU
Projected 60 plays, 58% dropbacks, 30.8 pass att, 25.5 runs, 2.5 sacks. QB: Trevor Lawrence
**Coaching style:** Deep-pass share low: 15% (league 19%); Red-zone pass rate high: 61% (league 53%); Pass rate on 2nd & short high: 47% (league 31%); EPA/dropback high: +0.26 (league +0.06); EPA/run high: -0.02 (league -0.09).
**Model game script:** projected 23.5 – 16.9 (margin +6.6) → dropback rate -2.7%.
**Weather:** forecast 54°F, wind 9 mph → pass yds x1.00, long FG x1.00.
**Strength of schedule:** own pass yds x1.03, own scoring x1.03 (raw stats re-rated against the opponents actually faced).
**Out:** Eric Murray (carried from week 5 report: Doubtful (Concussion)), Jaylon Jones (carried from week 5 report: Out (Hamstring)).
**Coach angle:** HC Liam Coen (young HC, 1 prior seasons); calls own plays (developing play-caller, 2 seasons calling); career balanced (+1.1 pts pass rate vs league, 2 seasons); spreads it around; this season top target share 24%.
**HOU secondary:** DC DeMeco Ryans, mixed-leaning: Mixes zone and man; declined to shadow George Pickens with Stingley; outside Derek Stingley Jr. / Kamari Lassiter; nickel Jalen Pitre; weak spot: Receivers who move around avoid Stingley; [research confidence medium, 2026-10-14].

**What worked last game → this week vs HOU** (failed play types cut, volume moved to what worked; `HOU allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player              | cut (failed last game)                                                                                                     | more of                                                                                | HOU allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:--------------------|:---------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Brian Thomas Jr.    | deep_right (100% failed), short_right (100% failed), short_left (100% failed)                                              | short_middle x4.7, deep_left x4.7, deep_middle x4.7                                    | x1.07, x0.91, x1.06               |        -0.0 |         5.6 |         0.0 |          0.0 |       32.2 |
| Jakobi Meyers       | short_left (100% failed)                                                                                                   | short_middle x1.6, deep_right x1.6, short_right x1.6, deep_left x1.6, deep_middle x1.6 | x1.07, x1.07, x1.05, x0.91, x1.06 |         0.0 |         4.1 |        -0.0 |         -0.0 |       35.8 |
| Parker Washington   | short_right (67% failed), short_left (50% failed), deep_left (100% failed)                                                 | short_middle x1.9, deep_right x1.9, deep_middle x1.9                                   | x1.07, x1.07, x1.06               |        -0.0 |         3.5 |        -0.0 |          0.0 |       61.5 |
| Bhayshul Tuten      | run inside_right (25% failed), run outside_left (75% failed), run inside_left (25% failed), run outside_right (67% failed) | run inside_right x1.1, run middle x1.5, run inside_left x1.1                           | x0.88, x0.85, x0.84               |         0.0 |         1.0 |         0.0 |          1.1 |       75.9 |
| Bhayshul Tuten      | short_right (100% failed)                                                                                                  | short_middle x1.4, deep_right x1.4, short_left x1.4, deep_left x1.4, deep_middle x1.4  | x1.07, x1.07, x0.97, x0.91, x1.06 |         0.0 |         1.0 |         0.0 |          1.1 |       75.9 |
| Josh Cameron        | short_right (50% failed), short_left (67% failed)                                                                          | short_middle x1.7, deep_right x1.7, deep_left x1.7, deep_middle x1.7                   | x1.07, x1.07, x0.91, x1.06        |         0.0 |         1.5 |         0.0 |          0.0 |       26.5 |
| LeQuint Allen Jr.   | short_middle (100% failed), short_right (100% failed)                                                                      | deep_right x3.9, short_left x3.9, deep_left x3.9, deep_middle x3.9                     | x1.07, x0.97, x0.91, x1.06        |         0.0 |         0.8 |         0.0 |          0.0 |        8.7 |
| Chris Rodriguez Jr. | run inside_right (50% failed)                                                                                              | run middle x1.1, run outside_left x1.1, run inside_left x1.1, run outside_right x1.1   | x0.85, x0.76, x0.84, x0.88        |         0.0 |        -0.0 |         0.0 |          0.5 |       24.0 |

**HOU defensive weak spots:** deep passes: 15.6 allowed vs league 11.9 (30 plays).
- HOU struggle: Wk1 vs BUF: +0.25 EPA/play allowed (norm -0.15). Why: TEs 19.6 yds/target vs 4.1 in other games; vs play action 11.0 yds/dropback vs 5.6 in other games; when blitzing 8.8 yds/dropback vs 6.3 in other games; deep passes 19.0 yds/play vs 13.6 in other games; WRs 10.9 yds/target vs 8.1 in other games
- HOU struggle: Wk4 vs DAL: +0.14 EPA/play allowed (norm -0.12). Why: vs play action 10.7 yds/dropback vs 5.0 in other games; deep passes 24.2 yds/play vs 13.8 in other games; missing starters: Azeez Al-Shaair (LB); red-zone TD rate per play 31% vs 13%; DAL is a strong offense (+0.12 EPA/play in its other games) → counted at 50% weight (those starters are available now)
**Offenses like JAX that faced HOU:** IND (similarity 0.52: +0.2 pass / -1.1 run yds/play vs their norm), BUF (similarity 0.05: +2.8 pass / -1.5 run yds/play vs their norm), DAL (similarity 0.05: -0.2 pass / -0.7 run yds/play vs their norm) → JAX pass x1.01, run x0.98.
**HOU defensive scheme (online/tagged):** blitz: light, coverage: zone_heavy [online (high)].
- HOU is soft deep (+0.95 EPA/deep att vs league +0.43); JAX throws deep 15%.
- Best matchups: pass_deep_right (x1.07), pass_short_middle (x1.07); worst: run_outside_left (x0.76).
- Last game — worked: run_middle; failed: run_outside_left, run_outside_right.
- HOU blitzes 21% of dropbacks (league 32%, FTN charting); JAX gains x0.85 as much per dropback vs the blitz as other offenses (47 blitzed dropbacks) -> pass yards x1.02
- JAX short plays vs zone heavy coverage defenses: x1.08 vs how other offenses fare (40 plays)
- JAX run plays vs zone heavy coverage defenses: x0.92 vs how other offenses fare (24 plays)
- JAX deep-throw rate vs zone heavy coverage: x0.83

| player              | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:--------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Trevor Lawrence     | QB    |     249.31 |      1.37 |            0.54 |      2.36 |      13.74 |      0.00 |         0.00 |      0.00 |         0.09 |
| Bhayshul Tuten      | RB    |       0.00 |      0.00 |            0.00 |     16.60 |      58.81 |      2.41 |         1.73 |     16.95 |         0.44 |
| Parker Washington   | WR    |       0.00 |      0.00 |            0.00 |      0.22 |       0.64 |      6.53 |         4.34 |     58.06 |         0.33 |
| Brenton Strange     | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.29 |         4.31 |     53.79 |         0.22 |
| Jakobi Meyers       | WR    |       0.00 |      0.00 |            0.00 |      0.13 |       0.44 |      3.65 |         2.38 |     32.86 |         0.18 |
| Brian Thomas Jr.    | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.33 |         1.81 |     30.47 |         0.13 |
| Josh Cameron        | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.04 |         1.97 |     25.69 |         0.15 |
| Chris Rodriguez Jr. | RB    |       0.00 |      0.00 |            0.00 |      6.18 |      21.59 |      0.31 |         0.22 |      2.05 |         0.29 |

**JAX kicker**

| player     |   fg_made |   xp_made |   kicking_points |
|:-----------|----------:|----------:|-----------------:|
| Cam Little |      2.37 |      2.20 |             9.32 |

**JAX defenders (vs HOU offense)**

| player           |   tackles |   sacks |   def_int |
|:-----------------|----------:|--------:|----------:|
| Foyesade Oluokun |      8.08 |    0.00 |      0.19 |
| Ventrell Miller  |      6.80 |    0.17 |      0.00 |
| Antonio Johnson  |      5.30 |    0.16 |      0.00 |
| Travis Hunter    |      4.63 |    0.00 |      0.09 |
| Josh Hines-Allen |      4.10 |    0.24 |      0.00 |
| Jarrian Jones    |      3.92 |    0.00 |      0.09 |
| Rayuan Lane III  |      3.89 |    0.00 |      0.00 |
| Jourdan Lewis    |      3.71 |    0.00 |      0.19 |

## HOU vs JAX
Projected 61 plays, 69% dropbacks, 38.4 pass att, 18.7 runs, 2.2 sacks. QB: C.J. Stroud
**Coaching style:** Early-down pass rate high: 58% (league 53%); Deep-pass share high: 23% (league 19%); Pass rate on 2nd & short high: 60% (league 31%); EPA/dropback high: +0.17 (league +0.06); EPA/run low: -0.20 (league -0.09); Favors run inside right (35%).
**Model game script:** projected 16.9 – 23.5 (margin -6.6) → dropback rate +2.7%.
**Weather:** forecast 54°F, wind 9 mph → pass yds x1.00, long FG x1.00.
**Strength of schedule:** own pass yds x0.95, own scoring x0.95, opp pass D x1.03, opp run D x1.02, opp scoring D x1.02 (raw stats re-rated against the opponents actually faced).
**Out:** Tank Dell (carried from week 5 report: Out (Knee)).
**Coach angle:** HC DeMeco Ryans (young HC, 3 prior seasons); plays called by OC Nick Caley (developing play-caller, 1 seasons calling); career balanced (+1.8 pts pass rate vs league, 1 seasons); typical; this season top target share 18%.
**JAX secondary:** DC Anthony Campanile, coverage lean unknown: New coverage scheme with pass game coordinator Mathieu Araujo; outside Travis Hunter / Montaric Brown; nickel Jourdan Lewis; weak spot: Hunter is the least experienced starter (returning from LCL tear); [research confidence low, 2026-10-14].

**What worked last game → this week vs JAX** (failed play types cut, volume moved to what worked; `JAX allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player            | cut (failed last game)                                                                 | more of                                                                                | JAX allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:------------------|:---------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Kayshon Boutte    | deep_right (50% failed), short_middle (100% failed)                                    | short_right x1.5, short_left x1.5, deep_left x1.5, deep_middle x1.5                    | x1.12, x1.15, x0.86, x0.90        |         0.0 |        -2.6 |         0.0 |          0.0 |       31.3 |
| Dalton Schultz    | deep_middle (100% failed)                                                              | —                                                                                      | —                                 |         0.0 |        -1.1 |         0.0 |          0.0 |       50.0 |
| Xavier Hutchinson | short_middle (50% failed)                                                              | short_right x1.1, short_left x1.1, deep_right x1.1, deep_left x1.1, deep_middle x1.1   | x1.12, x1.15, x0.92, x0.86, x0.90 |         0.0 |        -1.1 |         0.0 |          0.0 |       62.7 |
| Woody Marks       | run inside_left (50% failed), run outside_right (100% failed), run middle (25% failed) | run inside_right x1.4, run outside_left x1.4                                           | x0.96, x1.00                      |        -0.0 |         0.3 |         0.0 |         -0.7 |       46.8 |
| Woody Marks       | short_right (33% failed)                                                               | short_left x1.2, deep_right x1.2, short_middle x1.2, deep_left x1.2, deep_middle x1.2  | x1.15, x0.92, x1.10, x0.86, x0.90 |        -0.0 |         0.3 |         0.0 |         -0.7 |       46.8 |
| Nico Collins      | short_right (33% failed), deep_left (100% failed)                                      | short_left x1.2, deep_right x1.2, short_middle x1.2, deep_middle x1.2                  | x1.15, x0.92, x1.10, x0.90        |         0.0 |         1.0 |         0.0 |          0.0 |       49.7 |
| Jaylin Noel       | short_left (33% failed), short_middle (100% failed)                                    | short_right x1.4, deep_right x1.4, deep_left x1.4, deep_middle x1.4                    | x1.12, x0.92, x0.86, x0.90        |         0.0 |        -0.7 |         0.0 |          0.0 |       35.1 |
| Foster Moreau     | deep_right (100% failed)                                                               | short_right x1.1, short_left x1.1, short_middle x1.1, deep_left x1.1, deep_middle x1.1 | x1.12, x1.15, x1.10, x0.86, x0.90 |         0.0 |        -0.6 |         0.0 |          0.0 |       19.1 |

- JAX struggle: Wk2 vs DEN: +0.12 EPA/play allowed (norm -0.26). Why: TEs 12.2 yds/target vs 5.0 in other games; outside runs 5.4 yds/play vs 2.3 in other games; inside runs 3.8 yds/play vs 2.0 in other games; vs play action 10.4 yds/dropback vs 5.5 in other games; deep passes 20.0 yds/play vs 11.1 in other games
- JAX struggle: Wk4 vs CIN: +0.05 EPA/play allowed (norm -0.24). Why: when blitzing 8.6 yds/dropback vs 4.0 in other games; vs play action 8.2 yds/dropback vs 6.0 in other games; short passes 6.8 yds/play vs 5.4 in other games
**Offenses like HOU that faced JAX:** NWE (similarity 0.15: -2.4 pass / -1.2 run yds/play vs their norm), CIN (similarity 0.13: +1.0 pass / -2.7 run yds/play vs their norm), PHI (similarity 0.05: -0.3 pass / -2.9 run yds/play vs their norm) → HOU pass x0.99, run x0.98.
**JAX defensive scheme (online/tagged):** blitz: avg, coverage: avg, shell: two_high [online (high)].
- Best matchups: pass_short_left (x1.15), pass_short_right (x1.12); worst: pass_deep_left (x0.86).
- JAX blitzes 31% of dropbacks (league 32%, FTN charting); HOU gains x1.33 as much per dropback vs the blitz as other offenses (42 blitzed dropbacks) -> pass yards x1.00
- HOU deep plays vs two high shell defenses: x0.87 vs how other offenses fare (14 plays)
- HOU short plays vs two high shell defenses: x1.14 vs how other offenses fare (63 plays)
- HOU run plays vs two high shell defenses: x1.08 vs how other offenses fare (53 plays)
- JAX vs position groups: Dalton Schultz x0.95

| player            | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| C.J. Stroud       | QB    |     279.81 |      0.89 |            0.56 |      2.62 |      14.68 |      0.00 |         0.00 |      0.00 |         0.09 |
| Xavier Hutchinson | WR    |       0.00 |      0.00 |            0.00 |      0.26 |       0.85 |      6.95 |         4.35 |     57.78 |         0.12 |
| Nico Collins      | WR    |       0.00 |      0.00 |            0.00 |      0.09 |       0.35 |      5.43 |         3.67 |     46.46 |         0.20 |
| Dalton Schultz    | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.03 |         4.31 |     46.90 |         0.10 |
| Woody Marks       | RB    |       0.00 |      0.00 |            0.00 |      7.62 |      25.28 |      3.00 |         2.08 |     21.16 |         0.29 |
| David Montgomery  | RB    |       0.00 |      0.00 |            0.00 |      9.01 |      28.34 |      1.22 |         0.87 |      8.96 |         0.28 |
| Jaylin Noel       | WR    |       0.00 |      0.00 |            0.00 |      0.65 |       2.38 |      3.82 |         2.52 |     30.75 |         0.11 |
| Kayshon Boutte    | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.87 |         2.50 |     28.25 |         0.08 |
| Foster Moreau     | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.71 |         1.94 |     17.95 |         0.08 |
| Jared Wayne       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.15 |         1.27 |     17.01 |         0.04 |

**HOU kicker**

| player           |   fg_made |   xp_made |   kicking_points |
|:-----------------|----------:|----------:|-----------------:|
| Ka'imi Fairbairn |      1.87 |      1.52 |             7.13 |

**HOU defenders (vs JAX offense)**

| player            |   tackles |   sacks |   def_int |
|:------------------|----------:|--------:|----------:|
| Azeez Al-Shaair   |      8.97 |    0.00 |      0.00 |
| Reed Blankenship  |      8.96 |    0.00 |      0.22 |
| Jake Hansen       |      7.46 |    0.16 |      0.33 |
| Kamari Lassiter   |      6.34 |    0.00 |      0.00 |
| Tommy Togiai      |      6.28 |    0.00 |      0.00 |
| Will Anderson Jr. |      5.78 |    1.16 |      0.00 |
| Jalen Pitre       |      5.16 |    0.00 |      0.00 |
| Calen Bullock     |      4.35 |    0.00 |      0.00 |

## ATL vs CHI
Projected 53 plays, 55% dropbacks, 25.6 pass att, 23.7 runs, 2.5 sacks. QB: Michael Penix Jr.
**Coaching style:** Neutral-script pass rate low: 48% (league 59%); Early-down pass rate low: 39% (league 53%); 3rd-down deep share high: 27% (league 21%); Red-zone pass rate low: 36% (league 53%); 4th-down go rate low: 9% (league 19%); Shotgun rate low: 48% (league 61%); Pass rate on 2nd & short low: 13% (league 31%); Red-zone run share high: 68% (league 46%); EPA/dropback low: -0.02 (league +0.06); EPA/run high: +0.06 (league -0.09); Favors run inside left (38%).
**Model game script:** projected 21.4 – 23.8 (margin -2.4) → dropback rate +1.0%.
**Strength of schedule:** own scoring x0.97 (raw stats re-rated against the opponents actually faced).
**Out:** Yasir Abdullah (carried from week 5 report: Out (Hamstring)).
**Coach angle:** HC Kevin Stefanski (new to team, 6 prior seasons); plays called by OC Tommy Rees (developing play-caller, 1 seasons calling); career balanced (+1.5 pts pass rate vs league, 1 seasons); spreads it around; this season top target share 32%.
**CHI secondary:** DC Dennis Allen, man-leaning: Man-heavy scheme; Allen has used his top corner to shadow WR1s in the past but not in 2026 while Jaylon Johnson recovered; outside Jaylon Johnson / Tyrique Stevenson; nickel Cam Lewis; weak spot: Johnson allowing a 118.8 passer rating when targeted through week 5 (PFF); rookie Malik Muhammad targeted; [research confidence medium, 2026-10-14].

**What worked last game → this week vs CHI** (failed play types cut, volume moved to what worked; `CHI allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player          | cut (failed last game)                                                                                  | more of                                                                                | CHI allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:----------------|:--------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Bijan Robinson  | short_left (33% failed), short_right (100% failed)                                                      | short_left x1.2, deep_right x1.8, deep_middle x1.8, short_middle x1.8, deep_left x1.8  | x0.97, x1.22, x1.19, x1.02, x1.13 |         0.0 |         6.8 |         0.0 |         -4.1 |      122.8 |
| Bijan Robinson  | run inside_left (38% failed), run outside_left (50% failed)                                             | run middle x1.3, run outside_right x1.3, run inside_right x1.3                         | x1.00, x1.07, x1.02               |         0.0 |         6.8 |         0.0 |         -4.1 |      122.8 |
| Jahan Dotson    | short_right (100% failed), deep_left (100% failed)                                                      | short_left x1.7, deep_right x1.7, deep_middle x1.7, short_middle x1.7                  | x0.97, x1.22, x1.19, x1.02        |        -0.0 |         5.0 |         0.0 |          0.0 |       36.9 |
| Drake London    | short_left (33% failed), short_right (50% failed), deep_middle (100% failed), short_middle (50% failed) | short_left x1.1, deep_right x1.6, deep_left x1.6                                       | x0.97, x1.22, x1.13               |        -0.0 |         4.6 |         0.0 |          0.0 |       77.4 |
| Kyle Pitts      | deep_middle (100% failed)                                                                               | short_left x1.1, short_right x1.1, deep_right x1.1, short_middle x1.1, deep_left x1.1  | x0.97, x1.01, x1.22, x1.02, x1.13 |         0.0 |        -1.8 |         0.0 |          0.0 |       27.6 |
| Brian Robinson  | short_right (100% failed)                                                                               | short_left x1.9, deep_right x1.9, deep_middle x1.9, short_middle x1.9, deep_left x1.9  | x0.97, x1.22, x1.19, x1.02, x1.13 |        -0.0 |         0.9 |         0.0 |          0.3 |       39.8 |
| Brian Robinson  | run inside_left (40% failed)                                                                            | run middle x1.2, run outside_left x1.2, run outside_right x1.2, run inside_right x1.2  | x1.00, x1.09, x1.07, x1.02        |        -0.0 |         0.9 |         0.0 |          0.3 |       39.8 |
| Charlie Woerner | short_left (100% failed)                                                                                | short_right x1.8, deep_right x1.8, deep_middle x1.8, short_middle x1.8, deep_left x1.8 | x1.01, x1.22, x1.19, x1.02, x1.13 |         0.0 |         1.0 |         0.0 |          0.0 |        8.0 |

**CHI defensive weak spots:** deep passes: 24.6 allowed vs league 11.9 (20 plays); play-action dropbacks: 11.4 allowed vs league 6.9 (38 plays); explosive plays: 11% allowed vs league 9% (199 plays).
- CHI struggle: Wk1 vs CAR: +0.09 EPA/play allowed (norm -0.04). Why: RBs 14.2 yds/target vs 3.5 in other games; vs play action 15.0 yds/dropback vs 10.5 in other games; red-zone TD rate per play 43% vs 14%; WRs 12.2 yds/target vs 10.2 in other games; CAR is a strong offense (+0.12 EPA/play in its other games)
- CHI struggle: Wk5 vs GNB: +0.33 EPA/play allowed (norm -0.10). Why: when blitzing 14.6 yds/dropback vs 5.4 in other games; TEs 12.8 yds/target vs 6.3 in other games; vs play action 16.1 yds/dropback vs 9.3 in other games; WRs 13.7 yds/target vs 9.5 in other games; deep passes 29.7 yds/play vs 21.8 in other games
**Offenses like ATL that faced CHI:** MIN (similarity 0.08: -0.0 pass / +0.6 run yds/play vs their norm), NYJ (similarity 0.02: -0.6 pass / +0.8 run yds/play vs their norm), GNB (similarity 0.01: +3.9 pass / -0.4 run yds/play vs their norm) → ATL pass x0.99, run x1.00.
**CHI defensive scheme (online/tagged):** blitz: heavy, coverage: man_heavy [online (high)].
- CHI is soft deep (+1.54 EPA/deep att vs league +0.43); ATL throws deep 20%.
- CHI brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed +0.59 on 5 attempts. ATL 3rd-down deep share 27%.
- CHI run defense is soft (+0.05 EPA/run).
- Best matchups: pass_deep_right (x1.22), pass_deep_middle (x1.19); worst: pass_short_left (x0.97).
- Last game — worked: pass_deep_right, run_inside_right; failed: none.
- CHI blitzes 39% of dropbacks (league 32%, FTN charting); ATL gains x1.37 as much per dropback vs the blitz as other offenses (49 blitzed dropbacks) -> pass yards x1.02

| player            | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Michael Penix Jr. | QB    |     223.65 |      1.11 |            0.84 |      0.93 |       7.17 |      0.00 |         0.00 |      0.00 |         0.04 |
| Bijan Robinson    | RB    |       0.00 |      0.00 |            0.00 |     16.21 |      78.92 |      5.07 |         3.23 |     41.89 |         0.64 |
| Drake London      | WR    |       0.00 |      0.00 |            0.00 |      0.21 |       1.16 |      7.15 |         4.49 |     75.44 |         0.20 |
| Brian Robinson    | RB    |       0.00 |      0.00 |            0.00 |      7.37 |      33.61 |      0.72 |         0.45 |      5.63 |         0.36 |
| Jahan Dotson      | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.11 |         1.87 |     35.62 |         0.18 |
| Kyle Pitts        | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.55 |         2.33 |     26.48 |         0.16 |
| Zachariah Branch  | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.64 |         1.04 |     13.31 |         0.06 |

**ATL kicker**

| player    |   fg_made |   xp_made |   kicking_points |
|:----------|----------:|----------:|-----------------:|
| Nick Folk |      1.70 |      2.22 |             7.33 |

**ATL defenders (vs CHI offense)**

| player             |   tackles |   sacks |   def_int |
|:-------------------|----------:|--------:|----------:|
| Xavier Watts       |     10.15 |    0.10 |      0.35 |
| Divine Deablo      |      7.92 |    0.00 |      0.00 |
| C.J. Henderson     |      7.25 |    0.00 |      0.00 |
| Mike Hughes        |      7.19 |    0.00 |      0.00 |
| Kendal Daniels     |      6.63 |    0.23 |      0.00 |
| Jessie Bates       |      6.29 |    0.00 |      0.00 |
| Harold Perkins Jr. |      5.87 |    0.10 |      0.00 |
| Sydney Brown       |      4.86 |    0.00 |      0.00 |

## CHI vs ATL
Projected 71 plays, 56% dropbacks, 34.9 pass att, 31.7 runs, 2.0 sacks. QB: Tyson Bagent
**Coaching style:** 3rd-down deep share low: 14% (league 21%); Red-zone pass rate low: 42% (league 53%); 4th-down go rate high: 42% (league 19%); Shotgun rate low: 53% (league 61%); Pass rate on 2nd & short high: 44% (league 31%); Red-zone run share high: 56% (league 46%); 3rd-down conversion high: 48% (league 42%); EPA/run high: -0.03 (league -0.09); Favors run inside right (45%).
**Model game script:** projected 23.8 – 21.4 (margin +2.4) → dropback rate -1.0%.
**Strength of schedule:** own pass yds x1.05, own scoring x1.03, opp pass D x0.98, opp scoring D x0.98 (raw stats re-rated against the opponents actually faced).
**Out:** Kyle Monangai (carried from week 5 report: Out (Thumb)), Keyshaun Elliott (carried from week 5 report: Out (Quadricep)).
**Coach angle:** HC Ben Johnson (young HC, 1 prior seasons); calls own plays (developing play-caller, 4 seasons calling); career balanced (-0.8 pts pass rate vs league, 4 seasons); typical; this season top target share 23%.
**ATL secondary:** DC Jeff Ulbrich, man-leaning: Ulbrich pushed toward more man coverage; 4-3 roots; outside C.J. Henderson / Mike Hughes; nickel Billy Bowman Jr.; weak spot: Terrell graded 46-48 in coverage by PFF early in 2026; current depth chart lists C.J. Henderson and Mike Hughes outside; [research confidence medium, 2026-10-14].

**What worked last game → this week vs ATL** (failed play types cut, volume moved to what worked; `ATL allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player            | cut (failed last game)                                                          | more of                                                                                    | ATL allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:------------------|:--------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Rome Odunze       | short_right (100% failed), short_middle (50% failed), deep_middle (100% failed) | deep_right x1.9, deep_left x1.9, short_left x1.9                                           | x0.88, x0.86, x0.93               |         0.0 |         3.2 |         0.0 |          0.0 |       48.6 |
| Luther Burden III | deep_right (100% failed)                                                        | short_right x1.1, short_middle x1.1, deep_left x1.1, deep_middle x1.1, short_left x1.1     | x0.86, x0.87, x0.86, x0.97, x0.93 |         0.0 |        -3.0 |        -0.0 |         -0.1 |       66.3 |
| Luther Burden III | run outside_right (100% failed)                                                 | run inside_right x1.2, run inside_left x1.2, run outside_left x1.2, run middle x1.2        | x1.08, x1.07, x0.98, x1.26        |         0.0 |        -3.0 |        -0.0 |         -0.1 |       66.3 |
| Colston Loveland  | short_right (100% failed), short_middle (50% failed), deep_middle (100% failed) | short_middle x1.2, deep_right x2.5, deep_left x2.5, short_left x2.5                        | x0.87, x0.88, x0.86, x0.93        |         0.0 |         2.5 |         0.0 |          0.0 |       43.1 |
| Kalif Raymond     | run outside_right (100% failed)                                                 | run inside_right x1.7, run inside_left x1.7, run outside_left x1.7, run middle x1.7        | x1.08, x1.07, x0.98, x1.26        |        -0.0 |         1.5 |         0.0 |         -0.1 |       44.1 |
| Kalif Raymond     | short_left (100% failed)                                                        | short_right x1.3, short_middle x1.3, deep_right x1.3, deep_left x1.3, deep_middle x1.3     | x0.86, x0.87, x0.88, x0.86, x0.97 |        -0.0 |         1.5 |         0.0 |         -0.1 |       44.1 |
| D'Andre Swift     | short_right (33% failed)                                                        | short_middle x1.2, deep_right x1.2, deep_left x1.2, deep_middle x1.2, short_left x1.2      | x0.87, x0.88, x0.86, x0.97, x0.93 |        -0.0 |         1.2 |         0.0 |         -0.4 |      136.3 |
| D'Andre Swift     | run middle (100% failed)                                                        | run inside_right x1.1, run outside_right x1.1, run inside_left x1.1, run outside_left x1.1 | x1.08, x1.05, x1.07, x0.98        |        -0.0 |         1.2 |         0.0 |         -0.4 |      136.3 |

**ATL defensive weak spots:** play-action dropbacks: 8.8 allowed vs league 6.9 (45 plays); inside runs: 4.4 allowed vs league 3.9 (66 plays).
- ATL struggle: Wk2 vs CAR: +0.21 EPA/play allowed (norm -0.14). Why: deep passes 20.1 yds/play vs 7.4 in other games; WRs 10.0 yds/target vs 6.7 in other games; when blitzing 7.3 yds/dropback vs 5.0 in other games; vs play action 11.8 yds/dropback vs 8.2 in other games
- ATL struggle: Wk5 vs BAL: +0.04 EPA/play allowed (norm -0.10). Why: outside runs 5.4 yds/play vs 1.7 in other games; inside runs 6.7 yds/play vs 3.0 in other games; 7 explosive plays vs 3.5 per other game; short passes 6.3 yds/play vs 4.8 in other games; 3rd/4th downs converted 57% vs 36%
**Offenses like CHI that faced ATL:** BAL (similarity 0.32: -4.2 pass / +2.1 run yds/play vs their norm), CAR (similarity 0.03: -0.2 pass / -0.9 run yds/play vs their norm), GNB (similarity 0.02: -1.7 pass / -1.6 run yds/play vs their norm) → CHI pass x0.96, run x1.07.
**ATL defensive scheme (online/tagged):** blitz: avg, coverage: avg, shell: single_high [online (high)].
- Best matchups: run_middle (x1.26), run_inside_right (x1.08); worst: pass_short_right (x0.86).
- ATL blitzes 30% of dropbacks (league 32%, FTN charting); CHI gains x1.15 as much per dropback vs the blitz as other offenses (79 blitzed dropbacks) -> pass yards x1.00
- ATL vs position groups: D'Andre Swift x0.90, Colston Loveland x1.06

| player            | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Tyson Bagent      | QB    |     228.79 |      1.38 |            0.35 |      3.32 |      24.46 |      0.00 |         0.00 |      0.00 |         0.15 |
| D'Andre Swift     | RB    |       0.00 |      0.00 |            0.00 |     23.79 |     112.69 |      3.80 |         2.71 |     22.19 |         0.67 |
| Luther Burden III | WR    |       0.00 |      0.00 |            0.00 |      2.03 |       9.61 |      7.96 |         5.31 |     53.51 |         0.33 |
| Kalif Raymond     | WR    |       0.00 |      0.00 |            0.00 |      0.40 |       1.74 |      5.90 |         4.10 |     40.50 |         0.26 |
| Rome Odunze       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.62 |         3.50 |     45.38 |         0.18 |
| Colston Loveland  | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.59 |         3.65 |     40.80 |         0.18 |
| Cole Kmet         | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.08 |         1.35 |     14.65 |         0.11 |
| Roschon Johnson   | RB    |       0.00 |      0.00 |            0.00 |      4.46 |      19.70 |      0.28 |         0.19 |      1.41 |         0.14 |

**CHI kicker**

| player       |   fg_made |   xp_made |   kicking_points |
|:-------------|----------:|----------:|-----------------:|
| Cairo Santos |      1.61 |      2.62 |             7.45 |

**CHI defenders (vs ATL offense)**

| player            |   tackles |   sacks |   def_int |
|:------------------|----------:|--------:|----------:|
| Dillon Thieneman  |      8.93 |    0.00 |      0.31 |
| Devin Bush        |      6.88 |    0.25 |      0.00 |
| Cam Lewis         |      4.44 |    0.00 |      0.00 |
| Tyrique Stevenson |      4.36 |    0.00 |      0.00 |
| Malik Muhammad    |      4.29 |    0.17 |      0.22 |
| T.J. Edwards      |      4.20 |    0.00 |      0.30 |
| Jaylon Johnson    |      3.90 |    0.00 |      0.00 |
| Austin Booker     |      3.76 |    0.98 |      0.00 |

## CLE vs BAL
Projected 59 plays, 63% dropbacks, 31.1 pass att, 21.7 runs, 3.5 sacks. QB: Deshaun Watson
**Coaching style:** Red-zone pass rate high: 60% (league 53%); Sack rate high: 10% (league 6%); Shotgun rate high: 81% (league 61%); 3rd-down conversion low: 31% (league 42%); EPA/dropback low: +0.01 (league +0.06); EPA/run low: -0.34 (league -0.09).
**Model game script:** projected 18.7 – 22.9 (margin -4.2) → dropback rate +1.7%.
**Weather:** forecast 60°F, wind 9 mph → pass yds x1.00, long FG x1.00.
**Strength of schedule:** own scoring x1.05 (raw stats re-rated against the opponents actually faced).
**Out:** Tylan Wallace (carried from week 5 report: Out (Knee)), Teven Jenkins (carried from week 5 report: Out (Back)), Kalia Davis (carried from week 5 report: Out (Quadricep)), Mike Hall Jr. (carried from week 5 report: Out (Ankle)), Mason Graham (carried from week 5 report: Out (Knee)), Dillon Gabriel (carried from week 5 report: Out (Back)), Carsen Ryan (carried from week 5 report: Out (Calf)).
**Coach angle:** HC Todd Monken (first-year HC, 0 prior seasons); calls own plays (developing play-caller, 4 seasons calling); career run-first (-4.8 pts pass rate vs league, 4 seasons); leans on stars; this season top target share 19%.
**BAL secondary:** DC Jesse Minter, zone-leaning: 3-3-5 nickel base; floods the field with DBs and uses zone to mask individual matchups; big nickel with Kyle Hamilton as hybrid; outside Nate Wiggins / Marlon Humphrey; nickel Kyle Hamilton; weak spot: Humphrey graded 105th of 114 corners by PFF in 2025; [research confidence medium, 2026-10-14].

**What worked last game → this week vs BAL** (failed play types cut, volume moved to what worked; `BAL allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player            | cut (failed last game)                                                                                  | more of                                                                                | BAL allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:------------------|:--------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Denzel Boston     | short_middle (100% failed), short_left (50% failed), short_right (50% failed), deep_right (100% failed) | deep_middle x2.0, deep_left x2.0                                                       | x0.97, x1.08                      |        -0.0 |         4.1 |         0.0 |          0.0 |       52.8 |
| Harold Fannin Jr. | short_right (50% failed), deep_middle (100% failed), deep_right (100% failed)                           | short_middle x1.4, short_left x1.4, deep_left x1.4                                     | x0.83, x0.81, x1.08               |        -0.0 |        -3.4 |         0.0 |          0.0 |       32.5 |
| Isaiah Bond       | short_left (100% failed), deep_middle (100% failed), deep_left (100% failed)                            | short_middle x2.6, short_right x2.6, deep_right x2.6                                   | x0.83, x0.81, x1.12               |        -0.0 |         2.5 |         0.0 |          0.0 |       19.3 |
| Quinshon Judkins  | run outside_right (100% failed), run inside_left (60% failed)                                           | run middle x1.3, run outside_left x1.3, run inside_right x1.3                          | x1.12, x1.10, x1.02               |        -0.0 |         0.6 |         0.0 |         -1.7 |       80.0 |
| Quinshon Judkins  | short_left (33% failed)                                                                                 | short_middle x1.2, short_right x1.2, deep_middle x1.2, deep_left x1.2, deep_right x1.2 | x0.83, x0.81, x0.97, x1.08, x1.12 |        -0.0 |         0.6 |         0.0 |         -1.7 |       80.0 |
| Raheim Sanders    | short_left (100% failed)                                                                                | short_middle x2.2, short_right x2.2, deep_middle x2.2, deep_left x2.2, deep_right x2.2 | x0.83, x0.81, x0.97, x1.08, x1.12 |        -0.0 |         2.0 |         0.0 |          0.0 |       20.4 |
| Jerry Jeudy       | short_left (80% failed), deep_left (100% failed)                                                        | short_middle x1.9, short_right x1.9, deep_middle x1.9, deep_right x1.9                 | x0.83, x0.81, x0.97, x1.12        |        -0.0 |         1.7 |         0.0 |          0.0 |       23.0 |
| Deshaun Watson    | run outside_right (100% failed)                                                                         | run middle x1.2, run outside_left x1.2, run inside_left x1.2, run inside_right x1.2    | x1.12, x1.10, x1.24, x1.02        |         0.0 |         0.0 |         0.0 |         -0.5 |       38.6 |

**BAL defensive weak spots:** deep passes: 15.0 allowed vs league 11.9 (24 plays).
- BAL struggle: Wk2 vs NOR: +0.13 EPA/play allowed (norm -0.10). Why: TEs 14.8 yds/target vs 5.3 in other games; missing starters: Nnamdi Madubuike (DL); 3rd/4th downs converted 59% vs 39% → counted at 50% weight (those starters are available now)
- BAL struggle: Wk3 vs DAL: +0.09 EPA/play allowed (norm -0.08). Why: inside runs 4.9 yds/play vs 3.7 in other games; DAL is a strong offense (+0.14 EPA/play in its other games)
**Offenses like CLE that faced BAL:** TEN (similarity 0.08: +2.0 pass / -1.3 run yds/play vs their norm), DAL (similarity 0.06: -0.5 pass / +1.8 run yds/play vs their norm), IND (similarity 0.04: -1.4 pass / +1.6 run yds/play vs their norm) → CLE pass x1.00, run x1.00.
**BAL defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: two_high [online (high)].
- BAL is soft deep (+0.98 EPA/deep att vs league +0.43); CLE throws deep 17%.
- Best matchups: run_inside_left (x1.24), pass_deep_right (x1.12); worst: pass_short_left (x0.81).
- Last game — worked: run_middle, run_inside_right; failed: run_inside_left, run_outside_right.
- BAL blitzes 32% of dropbacks (league 32%, FTN charting); CLE gains x1.24 as much per dropback vs the blitz as other offenses (66 blitzed dropbacks) -> pass yards x1.00
- CLE short plays vs zone heavy coverage defenses: x1.07 vs how other offenses fare (65 plays)
- CLE run plays vs zone heavy coverage defenses: x1.14 vs how other offenses fare (46 plays)
- CLE short plays vs two high shell defenses: x0.77 vs how other offenses fare (55 plays)
- CLE deep-throw rate vs two high shell: x1.27
- BAL vs position groups: Jerry Jeudy x1.05, Quinshon Judkins x0.81, Denzel Boston x1.05, KC Concepcion x1.05

| player            | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Deshaun Watson    | QB    |     195.62 |      0.98 |            0.51 |      5.94 |      34.58 |      0.00 |         0.00 |      0.00 |         0.19 |
| Quinshon Judkins  | RB    |       0.00 |      0.00 |            0.00 |     16.16 |      61.94 |      4.05 |         2.67 |     17.95 |         0.45 |
| Denzel Boston     | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.49 |         3.56 |     52.81 |         0.22 |
| Harold Fannin Jr. | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.54 |         3.64 |     31.87 |         0.23 |
| KC Concepcion     | WR    |       0.00 |      0.00 |            0.00 |      0.28 |       1.12 |      5.62 |         3.37 |     33.38 |         0.12 |
| Jerry Jeudy       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.46 |         2.08 |     23.15 |         0.08 |
| Raheim Sanders    | RB    |       0.00 |      0.00 |            0.00 |      2.14 |       8.95 |      2.24 |         1.32 |     11.67 |         0.13 |
| Isaiah Bond       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.24 |         1.36 |     19.33 |         0.06 |

**CLE kicker**

| player      |   fg_made |   xp_made |   kicking_points |
|:------------|----------:|----------:|-----------------:|
| Andre Szmyt |      2.17 |      1.67 |             8.19 |

**CLE defenders (vs BAL offense)**

| player                 |   tackles |   sacks |   def_int |
|:-----------------------|----------:|--------:|----------:|
| Carson Schwesinger     |      9.27 |    0.24 |      0.00 |
| Quincy Williams        |      7.91 |    0.00 |      0.00 |
| Denzel Ward            |      5.38 |    0.00 |      0.12 |
| Ronnie Hickman Jr.     |      5.27 |    0.14 |      0.10 |
| Tyson Campbell         |      5.16 |    0.00 |      0.00 |
| Grant Delpit           |      5.16 |    0.14 |      0.11 |
| Myles Harden           |      4.14 |    0.00 |      0.09 |
| Emmanuel McNeil-Warren |      3.92 |    0.00 |      0.00 |

## BAL vs CLE
Projected 62 plays, 52% dropbacks, 26.6 pass att, 29.7 runs, 3.0 sacks. QB: Tyler Huntley
**Coaching style:** Neutral-script pass rate low: 54% (league 59%); Red-zone pass rate low: 40% (league 53%); 4th-down go rate low: 13% (league 19%); Pass rate on 2nd & short low: 10% (league 31%); Pass rate on 3rd & short low: 28% (league 41%); Red-zone run share high: 61% (league 46%); EPA/dropback high: +0.20 (league +0.06); EPA/run high: +0.05 (league -0.09).
**Model game script:** projected 22.9 – 18.7 (margin +4.2) → dropback rate -1.7%.
**Weather:** forecast 60°F, wind 9 mph → pass yds x1.00, long FG x1.00.
**Strength of schedule:** own run yds x0.97, own scoring x0.96 (raw stats re-rated against the opponents actually faced).
**Out:** Trey Hendrickson (carried from week 5 report: Out (Finger)), Lamar Jackson (carried from week 5 report: Out (Ankle)), Cam Jurgens (carried from week 5 report: Out (Concussion)).
**Coach angle:** HC Jesse Minter (first-year HC, 0 prior seasons); plays called by OC Declan Doyle (first-time play-caller, 0 seasons calling); no prior play-calling seasons: this season's data only; this season top target share 25%.
**CLE secondary:** DC Mike Rutenberg, mixed-leaning: First-year DC from Saleh tree; 73% zone in week 1 then back to 73% man vs PIT (Next Gen Stats); more disguise than Schwartz; outside Denzel Ward / Tyson Campbell; nickel Myles Harden; weak spot: Run fits and zone busts when they leave man; [research confidence medium, 2026-10-14].

**What worked last game → this week vs CLE** (failed play types cut, volume moved to what worked; `CLE allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player         | cut (failed last game)                                                                | more of                                                                                 | CLE allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:---------------|:--------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Mark Andrews   | short_left (50% failed), short_right (50% failed), short_middle (50% failed)          | deep_left x1.8, deep_middle x1.8, deep_right x1.8                                       | x1.04, x1.00, x0.92               |         0.0 |         3.2 |         0.0 |          0.0 |       39.1 |
| Rashod Bateman | deep_left (100% failed)                                                               | short_left x1.1, short_right x1.1, short_middle x1.1, deep_middle x1.1, deep_right x1.1 | x0.80, x0.88, x0.85, x1.00, x0.92 |         0.0 |        -2.5 |         0.0 |          0.0 |       29.1 |
| Zay Flowers    | short_middle (50% failed)                                                             | deep_left x1.2, short_left x1.2, short_right x1.2, deep_middle x1.2, deep_right x1.2    | x1.04, x0.80, x0.88, x1.00, x0.92 |         0.0 |        -1.6 |         0.0 |          0.0 |       52.9 |
| Justice Hill   | run inside_right (100% failed)                                                        | run middle x1.4, run outside_left x1.4, run outside_right x1.4, run inside_left x1.4    | x0.99, x1.20, x1.08, x1.11        |         0.0 |         0.3 |         0.0 |          1.3 |       32.8 |
| Justice Hill   | deep_left (100% failed), short_right (100% failed)                                    | short_left x2.0, short_middle x2.0, deep_middle x2.0, deep_right x2.0                   | x0.80, x0.85, x1.00, x0.92        |         0.0 |         0.3 |         0.0 |          1.3 |       32.8 |
| Derrick Henry  | short_middle (100% failed)                                                            | deep_left x1.4, short_left x1.4, short_right x1.4, deep_middle x1.4, deep_right x1.4    | x1.04, x0.80, x0.88, x1.00, x0.92 |         0.0 |        -0.0 |         0.0 |         -0.3 |      125.4 |
| Derrick Henry  | run middle (40% failed), run outside_left (25% failed), run inside_right (12% failed) | run outside_right x1.1, run inside_left x1.1                                            | x1.08, x1.11                      |         0.0 |        -0.0 |         0.0 |         -0.3 |      125.4 |

**CLE defensive weak spots:** explosive plays: 12% allowed vs league 9% (292 plays); outside runs: 7.3 allowed vs league 4.9 (27 plays).
- CLE struggle: Wk1 vs JAX: +0.40 EPA/play allowed (norm -0.09). Why: WRs 13.6 yds/target vs 8.0 in other games; deep passes 16.3 yds/play vs 9.7 in other games; short passes 8.2 yds/play vs 5.3 in other games; 3rd/4th downs converted 62% vs 35%; JAX is a strong offense (+0.10 EPA/play in its other games)
**Offenses like BAL that faced CLE:** JAX (similarity 0.43: +3.1 pass / +0.5 run yds/play vs their norm), TAM (similarity 0.18: -0.5 pass / +0.8 run yds/play vs their norm), NYJ (similarity 0.15: -2.2 pass / +1.2 run yds/play vs their norm) → BAL pass x1.05, run x1.01.
**CLE defensive scheme (online/tagged):** blitz: avg, coverage: man_heavy, shell: single_high [online (high)].
- CLE run defense is soft (+0.01 EPA/run).
- Best matchups: run_outside_left (x1.20), run_inside_left (x1.11); worst: pass_short_left (x0.80).
- Last game — worked: none; failed: pass_short_middle.
- CLE blitzes 25% of dropbacks (league 32%, FTN charting); BAL gains x0.93 as much per dropback vs the blitz as other offenses (56 blitzed dropbacks) -> pass yards x1.00
- BAL short plays vs single high shell defenses: x0.83 vs how other offenses fare (65 plays)
- BAL deep-throw rate vs single high shell: x0.90
- CLE vs position groups: Justice Hill x0.90, Rashod Bateman x1.05, Zay Flowers x1.05

| player         | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:---------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Tyler Huntley  | QB    |     176.75 |      1.46 |            0.42 |      3.44 |      23.60 |      0.00 |         0.00 |      0.00 |         0.06 |
| Derrick Henry  | RB    |       0.00 |      0.00 |            0.00 |     24.76 |     115.28 |      1.85 |         1.31 |     10.46 |         0.59 |
| Zay Flowers    | WR    |       0.00 |      0.00 |            0.00 |      0.43 |       2.30 |      6.76 |         4.66 |     50.01 |         0.33 |
| Mark Andrews   | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.93 |         3.91 |     37.86 |         0.28 |
| Rashod Bateman | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.05 |         2.89 |     28.87 |         0.19 |
| Justice Hill   | RB    |       0.00 |      0.00 |            0.00 |      3.54 |      19.69 |      2.27 |         1.64 |     12.90 |         0.18 |

**BAL kicker**

| player     |   fg_made |   xp_made |   kicking_points |
|:-----------|----------:|----------:|-----------------:|
| Tyler Loop |      2.21 |      2.31 |             8.93 |

**BAL defenders (vs CLE offense)**

| player          |   tackles |   sacks |   def_int |
|:----------------|----------:|--------:|----------:|
| Roquan Smith    |      7.82 |    0.34 |      0.10 |
| Kyle Hamilton   |      7.26 |    0.00 |      0.21 |
| Trenton Simpson |      6.60 |    0.47 |      0.18 |
| Malaki Starks   |      6.59 |    0.24 |      0.00 |
| Jaylinn Hawkins |      4.23 |    0.00 |      0.00 |
| Marlon Humphrey |      3.74 |    0.00 |      0.00 |
| Tavius Robinson |      3.11 |    0.99 |      0.00 |
| Nate Wiggins    |      2.75 |    0.00 |      0.00 |

## IND vs TEN
Projected 63 plays, 51% dropbacks, 30.6 pass att, 30.7 runs, 1.4 sacks. QB: Daniel Jones
**Coaching style:** Red-zone pass rate low: 44% (league 53%); 4th-down go rate high: 28% (league 19%); Sack rate low: 4% (league 6%); Pass rate on 3rd & short low: 29% (league 41%); Red-zone run share high: 55% (league 46%); EPA/dropback low: -0.15 (league +0.06); EPA/run high: +0.10 (league -0.09).
**Market team total:** implied 25.8 (this team landed within the tolerance in 60% of its games, avg miss 3.6). Model 30.7 → blended 27.7: TD rates x0.90, yards x0.97.
**Model game script:** projected 30.7 – 17.7 (margin +13.0) → dropback rate -5.2%.
**Strength of schedule:** own pass yds x0.97, own run yds x1.04, opp run D x1.03, opp scoring D x1.03 (raw stats re-rated against the opponents actually faced).
**Out:** Arden Key (carried from week 5 report: Out (Hamstring)), Ashton Dulin (carried from week 5 report: Out (Hamstring)), Will Mallory (carried from week 5 report: Out (Thumb)), Jaylon Carlies (carried from week 5 report: Out (Ribs)).
**Coach angle:** HC Shane Steichen (young HC, 3 prior seasons); calls own plays (veteran play-caller, 5 seasons calling); career run-first (-3.3 pts pass rate vs league, 5 seasons); typical; this season top target share 22%.
**TEN secondary:** DC Robert Saleh, zone-leaning: 4-3 wide-9; rushes four with stunts; zone-dominant (Cover 3 / quarters); blitz about 23%; outside Cor'Dale Flott / Alontae Taylor; nickel Marcus Harris; weak spot: Corners struggled in camp; [research confidence medium, 2026-10-14].

**What worked last game → this week vs TEN** (failed play types cut, volume moved to what worked; `TEN allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player           | cut (failed last game)                                                                                  | more of                                                                                    | TEN allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:-----------------|:--------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Keenan Allen     | short_middle (33% failed), short_left (25% failed), short_right (100% failed)                           | short_middle x1.4, short_left x1.5, deep_middle x2.0, deep_left x2.0, deep_right x2.0      | x1.00, x1.03, x0.94, x0.98, x0.99 |         0.0 |         6.6 |         0.0 |          0.0 |       39.6 |
| Laquon Treadwell | short_middle (100% failed), short_left (100% failed), deep_left (100% failed), deep_right (100% failed) | short_right x2.8, deep_middle x2.8                                                         | x0.93, x0.94                      |         0.0 |         3.2 |         0.0 |          0.0 |       32.3 |
| Tyler Warren     | short_left (33% failed), short_right (50% failed), deep_right (100% failed)                             | short_middle x1.5, deep_middle x1.5, deep_left x1.5                                        | x1.00, x0.94, x0.98               |         0.0 |         2.0 |         0.0 |          0.0 |       44.6 |
| Jonathan Taylor  | short_left (25% failed)                                                                                 | short_middle x1.2, short_right x1.2, deep_middle x1.2, deep_left x1.2, deep_right x1.2     | x1.00, x0.93, x0.94, x0.98, x0.99 |        -0.0 |         0.1 |         0.0 |          1.2 |      128.4 |
| Jonathan Taylor  | run inside_right (67% failed), run inside_left (17% failed)                                             | run outside_right x1.3, run middle x1.3, run inside_left x1.1, run outside_left x1.3       | x1.07, x1.10, x1.12, x1.13        |        -0.0 |         0.1 |         0.0 |          1.2 |      128.4 |
| Josh Downs       | short_left (67% failed), deep_middle (100% failed), deep_left (100% failed)                             | short_middle x1.6, short_right x1.6, deep_right x1.6                                       | x1.00, x0.93, x0.99               |        -0.0 |         0.4 |         0.0 |          0.0 |       43.3 |
| Deion Burks      | deep_left (100% failed)                                                                                 | short_middle x1.4, short_left x1.4, short_right x1.4, deep_middle x1.4, deep_right x1.4    | x1.00, x1.03, x0.93, x0.94, x0.99 |        -0.0 |        -0.4 |         0.0 |          0.0 |        7.1 |
| Daniel Jones     | run middle (33% failed)                                                                                 | run inside_right x1.2, run outside_right x1.2, run inside_left x1.2, run outside_left x1.2 | x1.16, x1.07, x1.12, x1.13        |         0.0 |         0.0 |         0.0 |          0.3 |       11.6 |

**TEN defensive weak spots:** deep passes: 14.7 allowed vs league 11.9 (25 plays); vs WRs: 10.1 yds/target (league 8.2), x1.06 for WRs.
- TEN struggle: Wk5 vs HOU: +0.19 EPA/play allowed (norm +0.06). Why: missing starters: Amani Hooker (S), Kevin Winston (S); short passes 7.8 yds/play vs 6.0 in other games → counted at 50% weight (those starters are available now)
**Offenses like IND that faced TEN:** BAL (similarity 0.34: +0.9 pass / -1.8 run yds/play vs their norm), NYG (similarity 0.26: -1.5 pass / +0.6 run yds/play vs their norm), NYJ (similarity 0.18: +3.4 pass / +0.9 run yds/play vs their norm) → IND pass x0.99, run x0.99.
**TEN defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: two_high [online (high)].
- TEN is soft deep (+0.94 EPA/deep att vs league +0.43); IND throws deep 17%.
- Best matchups: run_inside_right (x1.16), run_outside_left (x1.13); worst: pass_short_right (x0.93).
- Last game — worked: none; failed: pass_deep_left, run_inside_right.
- IND deep plays vs zone heavy coverage defenses: x0.90 vs how other offenses fare (23 plays)
- IND run plays vs two high shell defenses: x1.15 vs how other offenses fare (77 plays)
- IND deep-throw rate vs two high shell: x0.72
- TEN DBs out: Amani Hooker (17 tgts, 8.8 yds/tgt allowed) -> coverage 8.1 → 8.0 yds/tgt; WR yards x0.99
- TEN vs position groups: Laquon Treadwell x1.06, Josh Downs x1.06, Tyler Warren x0.86, Keenan Allen x1.06

| player           | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-----------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Daniel Jones     | QB    |     188.02 |      0.91 |            0.46 |      2.76 |      14.49 |      0.00 |         0.00 |      0.00 |         0.13 |
| Jonathan Taylor  | RB    |       0.00 |      0.00 |            0.00 |     22.46 |     105.61 |      3.62 |         2.49 |     21.50 |         0.72 |
| Tyler Warren     | TE    |       0.00 |      0.00 |            0.00 |      0.70 |       2.99 |      7.18 |         5.22 |     39.42 |         0.23 |
| Josh Downs       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.83 |         4.12 |     41.22 |         0.14 |
| Keenan Allen     | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.34 |         3.55 |     38.59 |         0.17 |
| Laquon Treadwell | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.78 |         2.67 |     29.65 |         0.11 |
| Seth McGowan     | RB    |       0.00 |      0.00 |            0.00 |      4.91 |      23.25 |      0.87 |         0.62 |      4.71 |         0.20 |

**IND kicker**

| player          |   fg_made |   xp_made |   kicking_points |
|:----------------|----------:|----------:|-----------------:|
| Spencer Shrader |      4.24 |      2.28 |            14.98 |

**IND defenders (vs TEN offense)**

| player              |   tackles |   sacks |   def_int |
|:--------------------|----------:|--------:|----------:|
| Akeem Davis-Gaither |      7.86 |    0.00 |      0.00 |
| Justin Walley       |      5.33 |    0.14 |      0.00 |
| DeForest Buckner    |      4.60 |    0.49 |      0.00 |
| A.J. Haulcy         |      3.90 |    0.00 |      0.00 |
| Camryn Bynum        |      3.60 |    0.00 |      0.00 |
| Bryce Boettcher     |      3.59 |    0.00 |      0.00 |
| Grover Stewart      |      3.46 |    0.04 |      0.00 |
| Charvarius Ward     |      3.21 |    0.00 |      0.00 |

## TEN vs IND
Projected 56 plays, 67% dropbacks, 33.8 pass att, 18.7 runs, 1.1 sacks. QB: Cam Ward
**Coaching style:** Early-down pass rate low: 49% (league 53%); Deep-pass share low: 16% (league 19%); 3rd-down deep share low: 9% (league 21%); Red-zone pass rate low: 41% (league 53%); Sack rate low: 3% (league 6%); Shotgun rate high: 69% (league 61%); No-huddle rate high: 10% (league 6%); Pass rate on 3rd & short low: 17% (league 41%); Red-zone run share high: 59% (league 46%); 3rd-down conversion low: 34% (league 42%); EPA/dropback low: -0.25 (league +0.06); Favors run inside left (33%).
**Model game script:** projected 17.7 – 30.7 (margin -13.0) → dropback rate +5.2%.
**Strength of schedule:** own scoring x1.02 (raw stats re-rated against the opponents actually faced).
**Out:** Amani Hooker (carried from week 5 report: Out (Concussion)).
**Coach angle:** HC Robert Saleh (new to team, 5 prior seasons); plays called by OC Brian Daboll (veteran play-caller, 6 seasons calling); career balanced (-0.7 pts pass rate vs league, 6 seasons); typical; this season top target share 29%.
**IND secondary:** DC Lou Anarumo, mixed-leaning: Multiple; game-plans corners to the opponent each week; disguise; outside Sauce Gardner / Charvarius Ward; nickel Justin Walley; weak spot: Allowed 1029 yards through two games; Ward and Gardner banged up early; [research confidence low, 2026-10-14].

**What worked last game → this week vs IND** (failed play types cut, volume moved to what worked; `IND allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player           | cut (failed last game)                                                        | more of                                                                                 | IND allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:-----------------|:------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Carnell Tate     | deep_left (100% failed), short_middle (100% failed), deep_right (100% failed) | short_left x1.6, short_right x1.6, deep_middle x1.6                                     | x1.02, x1.04, x0.96               |        -0.0 |        -7.8 |         0.0 |          0.0 |       55.5 |
| Elic Ayomanor    | short_left (100% failed)                                                      | short_right x1.9, deep_left x1.9, deep_middle x1.9, short_middle x1.9, deep_right x1.9  | x1.04, x1.01, x0.96, x0.99, x0.96 |         0.0 |         1.7 |         0.0 |          0.0 |       16.8 |
| Daniel Bellinger | short_right (100% failed)                                                     | short_left x1.8, deep_left x1.8, deep_middle x1.8, short_middle x1.8, deep_right x1.8   | x1.02, x1.01, x0.96, x0.99, x0.96 |        -0.0 |         1.3 |         0.0 |          0.0 |       10.3 |
| Calvin Ridley    | deep_right (100% failed)                                                      | short_left x1.2, short_right x1.2, deep_left x1.2, deep_middle x1.2, short_middle x1.2  | x1.02, x1.04, x1.01, x0.96, x0.99 |        -0.0 |        -1.3 |         0.0 |          0.0 |       12.2 |
| Tyjae Spears     | run inside_left (100% failed)                                                 | run inside_right x1.6, run middle x1.6, run outside_right x1.6, run outside_left x1.6   | x0.87, x1.00, x0.91, x1.05        |         0.0 |         1.2 |        -0.0 |         -0.1 |       35.0 |
| Tyjae Spears     | short_right (50% failed)                                                      | short_left x1.5, deep_left x1.5, deep_middle x1.5, short_middle x1.5, deep_right x1.5   | x1.02, x1.01, x0.96, x0.99, x0.96 |         0.0 |         1.2 |        -0.0 |         -0.1 |       35.0 |
| Kylen Granson    | deep_left (100% failed)                                                       | short_left x1.6, short_right x1.6, deep_middle x1.6, short_middle x1.6, deep_right x1.6 | x1.02, x1.04, x0.96, x0.99, x0.96 |         0.0 |        -0.3 |         0.0 |          0.0 |        1.6 |
| Tony Pollard     | short_middle (100% failed)                                                    | short_left x1.3, short_right x1.3, deep_left x1.3, deep_middle x1.3, deep_right x1.3    | x1.02, x1.04, x1.01, x0.96, x0.96 |        -0.0 |         0.3 |        -0.0 |          0.0 |       75.3 |

**IND defensive weak spots:** vs RBs: 9.1 yds/target (league 5.3), x1.16 for RBs; inside runs: 4.6 allowed vs league 3.9 (90 plays); short passes: 7.0 allowed vs league 6.0 (133 plays); play-action dropbacks: 8.4 allowed vs league 6.9 (47 plays); red-zone TDs per play: 24% allowed vs league 21% (41 plays).
- IND struggle: Wk1 vs BAL: +0.31 EPA/play allowed (norm +0.03). Why: when blitzing 10.7 yds/dropback vs 4.7 in other games; WRs 16.4 yds/target vs 7.9 in other games; short passes 12.0 yds/play vs 6.3 in other games; deep passes 17.1 yds/play vs 11.1 in other games; inside runs 6.0 yds/play vs 4.2 in other games
- IND struggle: Wk2 vs KAN: +0.23 EPA/play allowed (norm +0.05). Why: deep passes 18.2 yds/play vs 11.4 in other games; TEs 8.4 yds/target vs 5.5 in other games; when blitzing 8.6 yds/dropback vs 5.9 in other games; outside runs 7.0 yds/play vs 5.1 in other games; 8 explosive plays vs 4.8 per other game
- IND struggle: Wk5 vs PIT: +0.24 EPA/play allowed (norm +0.05). Why: missing starters: Jaylon Carlies (LB), Arden Key (DE); RBs 14.5 yds/target vs 7.7 in other games; inside runs 7.0 yds/play vs 4.2 in other games; red-zone TD rate per play 50% vs 22%; 3rd/4th downs converted 46% vs 31%
**Offenses like TEN that faced IND:** WAS (similarity 0.33: -0.4 pass / +0.3 run yds/play vs their norm), HOU (similarity 0.04: -2.3 pass / +0.2 run yds/play vs their norm), PIT (similarity 0.04: +1.5 pass / +1.8 run yds/play vs their norm) → TEN pass x0.98, run x1.00.
**IND defensive scheme (online/tagged):** blitz: avg, coverage: avg [online (high)].
- IND run defense is soft (+0.08 EPA/run).
- Best matchups: run_inside_left (x1.18), run_outside_left (x1.05); worst: run_inside_right (x0.87).
- IND blitzes 20% of dropbacks (league 32%, FTN charting); TEN gains x1.12 as much per dropback vs the blitz as other offenses (33 blitzed dropbacks) -> pass yards x0.99
- IND vs position groups: Tony Pollard x1.16, Tyjae Spears x1.16

| player             | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Cam Ward           | QB    |     193.48 |      1.31 |            0.47 |      3.20 |      22.60 |      0.00 |         0.00 |      0.00 |         0.16 |
| Carnell Tate       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      8.52 |         6.02 |     51.32 |         0.23 |
| Tony Pollard       | RB    |       0.00 |      0.00 |            0.00 |     13.38 |      52.49 |      3.07 |         2.05 |     20.64 |         0.39 |
| Wan'Dale Robinson  | WR    |       0.00 |      0.00 |            0.00 |      0.17 |       0.61 |      6.53 |         4.34 |     40.40 |         0.34 |
| Tyjae Spears       | RB    |       0.00 |      0.00 |            0.00 |      3.22 |      11.87 |      3.00 |         1.97 |     21.26 |         0.20 |
| Gunnar Helm        | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.31 |         1.53 |     12.60 |         0.09 |
| Elic Ayomanor      | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.07 |         1.14 |     15.65 |         0.08 |
| Calvin Ridley      | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.87 |         1.20 |     11.18 |         0.07 |
| Daniel Bellinger   | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.72 |         1.12 |     10.03 |         0.07 |
| Nicholas Singleton | RB    |       0.00 |      0.00 |            0.00 |      1.56 |       5.66 |      0.00 |         0.00 |      0.00 |         0.06 |

**TEN kicker**

| player    |   fg_made |   xp_made |   kicking_points |
|:----------|----------:|----------:|-----------------:|
| Joey Slye |      1.13 |      1.95 |             5.33 |

**TEN defenders (vs IND offense)**

| player            |   tackles |   sacks |   def_int |
|:------------------|----------:|--------:|----------:|
| Anthony Hill Jr.  |      8.63 |    0.00 |      0.00 |
| Cody Barton       |      5.57 |    0.00 |      0.00 |
| Jeffery Simmons   |      5.49 |    0.24 |      0.00 |
| Kevin Winston Jr. |      5.10 |    0.00 |      0.00 |
| Amani Hooker      |      4.94 |    0.00 |      0.23 |
| Alontae Taylor    |      4.90 |    0.13 |      0.00 |
| Cedric Gray       |      4.76 |    0.09 |      0.00 |
| Marcus Harris     |      4.28 |    0.08 |      0.23 |

## NWE vs NYJ
Projected 63 plays, 58% dropbacks, 29.9 pass att, 26.3 runs, 3.1 sacks. QB: Drake Maye
**Coaching style:** Deep-pass share high: 24% (league 19%); 3rd-down deep share low: 17% (league 21%); Red-zone pass rate high: 65% (league 53%); No-huddle rate low: 0% (league 6%); Red-zone run share low: 33% (league 46%); EPA/dropback high: +0.23 (league +0.06); Favors run middle (39%).
**Model game script:** projected 20.9 – 16.8 (margin +4.1) → dropback rate -1.6%.
**Weather:** forecast 52°F, wind 6 mph → pass yds x1.00, long FG x1.00.
**Out:** Mack Hollins (carried from week 5 report: Out (Calf)), Carlton Davis III (carried from week 5 report: Out (Neck)), Reggie Gilliam (carried from week 5 report: Out (Ankle)), Christian Gonzalez (carried from week 5 report: Out (Shoulder)), Karon Prunty (carried from week 5 report: Out (Hamstring)), Channing Canada (carried from week 5 report: Out (Hamstring)).
**Coach angle:** HC Mike Vrabel (veteran HC, 8 prior seasons); plays called by OC Josh McDaniels (veteran play-caller, 13 seasons calling); career balanced (+0.7 pts pass rate vs league, 13 seasons); typical; this season top target share 15%.
**NYJ secondary:** DC Aaron Glenn, man-leaning: Glenn calls it; multiple fronts; Detroit led the NFL in man rate (41.2%) under him; expected man-heavy but under 40%; outside Azareye'h Thomas / Brandon Stephens; nickel Jarvis Brownlee Jr.; weak spot: Nahshon Wright rotates outside; [research confidence medium, 2026-10-14].

**What worked last game → this week vs NYJ** (failed play types cut, volume moved to what worked; `NYJ allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player              | cut (failed last game)                                       | more of                                                                                    | NYJ allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:--------------------|:-------------------------------------------------------------|:-------------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Hunter Henry        | short_left (100% failed)                                     | short_right x1.5, short_middle x1.5, deep_right x1.5, deep_left x1.5, deep_middle x1.5     | x1.11, x1.09, x1.00, x0.99, x0.99 |         0.0 |         4.4 |         0.0 |          0.0 |       46.1 |
| DeMario Douglas     | deep_left (100% failed)                                      | short_right x1.1, short_left x1.1, short_middle x1.1, deep_right x1.1, deep_middle x1.1    | x1.11, x1.00, x1.09, x1.00, x0.99 |         0.0 |        -1.9 |         0.0 |          0.0 |       39.8 |
| Romeo Doubs         | deep_left (100% failed)                                      | short_right x1.1, short_left x1.1, short_middle x1.1, deep_right x1.1, deep_middle x1.1    | x1.11, x1.00, x1.09, x1.00, x0.99 |         0.0 |        -1.6 |         0.0 |          0.0 |       51.9 |
| Rhamondre Stevenson | short_left (33% failed)                                      | short_right x1.2, short_middle x1.2, deep_right x1.2, deep_left x1.2, deep_middle x1.2     | x1.11, x1.09, x1.00, x0.99, x0.99 |         0.0 |         1.0 |         0.0 |         -0.2 |       92.2 |
| Rhamondre Stevenson | run middle (25% failed)                                      | run outside_left x1.1, run inside_left x1.1, run inside_right x1.1, run outside_right x1.1 | x0.99, x0.88, x1.02, x0.95        |         0.0 |         1.0 |         0.0 |         -0.2 |       92.2 |
| Efton Chism III     | deep_left (100% failed)                                      | short_right x1.1, short_left x1.1, short_middle x1.1, deep_right x1.1, deep_middle x1.1    | x1.11, x1.00, x1.09, x1.00, x0.99 |         0.0 |        -1.0 |         0.0 |          0.0 |       30.7 |
| Eli Raridon         | short_left (33% failed)                                      | short_right x1.2, short_middle x1.2, deep_right x1.2, deep_left x1.2, deep_middle x1.2     | x1.11, x1.09, x1.00, x0.99, x0.99 |         0.0 |         0.8 |         0.0 |          0.0 |       20.3 |
| TreVeyon Henderson  | run inside_left (100% failed), run inside_right (50% failed) | run middle x1.6, run outside_left x1.6, run outside_right x1.6                             | x0.99, x0.99, x0.95               |         0.0 |         0.0 |        -0.0 |          0.7 |       48.1 |

**NYJ defensive weak spots:** outside runs: 5.8 allowed vs league 4.9 (24 plays).
- NYJ struggle: Wk3 vs DET: +0.19 EPA/play allowed (norm -0.19). Why: RBs 8.4 yds/target vs 3.0 in other games; deep passes 22.8 yds/play vs 8.4 in other games; vs play action 10.0 yds/dropback vs 3.8 in other games; when blitzing 8.2 yds/dropback vs 4.3 in other games; TEs 8.4 yds/target vs 5.3 in other games
- NYJ struggle: Wk4 vs CHI: +0.06 EPA/play allowed (norm -0.15). Why: outside runs 8.1 yds/play vs 4.5 in other games; 11 explosive plays vs 3.5 per other game; deep passes 16.5 yds/play vs 9.4 in other games; WRs 10.9 yds/target vs 6.3 in other games; RBs 6.8 yds/target vs 4.5 in other games → counted at 50% weight (those starters are available now)
**Offenses like NWE that faced NYJ:** CHI (similarity 0.16: +1.5 pass / +0.2 run yds/play vs their norm), DET (similarity 0.06: +0.4 pass / +0.6 run yds/play vs their norm), GNB (similarity 0.02: -3.1 pass / +0.4 run yds/play vs their norm) → NWE pass x1.03, run x1.00.
**NYJ defensive scheme (online/tagged):** blitz: heavy, coverage: avg, shell: two_high [online (high)].
- NYJ brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed +0.02 on 9 attempts. NWE 3rd-down deep share 17%.
- Best matchups: pass_short_right (x1.11), pass_short_middle (x1.09); worst: run_inside_left (x0.88).
- Last game — worked: pass_short_right, pass_deep_right; failed: pass_deep_left.
- NYJ blitzes 39% of dropbacks (league 32%, FTN charting); NWE gains x1.14 as much per dropback vs the blitz as other offenses (54 blitzed dropbacks) -> pass yards x1.01
- NWE deep plays vs two high shell defenses: x0.93 vs how other offenses fare (27 plays)
- NWE short plays vs two high shell defenses: x1.09 vs how other offenses fare (114 plays)

| player              | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:--------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Drake Maye          | QB    |     245.37 |      1.37 |            0.55 |      4.66 |      32.15 |      0.00 |         0.00 |      0.00 |         0.13 |
| Rhamondre Stevenson | RB    |       0.00 |      0.00 |            0.00 |     13.18 |      52.81 |      4.77 |         3.13 |     37.57 |         0.50 |
| Romeo Doubs         | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.79 |         3.62 |     50.20 |         0.27 |
| Hunter Henry        | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.57 |         2.94 |     43.87 |         0.20 |
| DeMario Douglas     | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.31 |         2.82 |     37.93 |         0.19 |
| TreVeyon Henderson  | RB    |       0.00 |      0.00 |            0.00 |      9.80 |      38.84 |      1.15 |         0.71 |      8.45 |         0.32 |
| Efton Chism III     | WR    |       0.00 |      0.00 |            0.00 |      0.23 |       0.98 |      3.31 |         2.03 |     28.11 |         0.17 |
| Eli Raridon         | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.25 |         1.43 |     19.68 |         0.12 |
| Kyle Williams       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.10 |         1.13 |     19.57 |         0.10 |
| Corey Kiner         | RB    |       0.00 |      0.00 |            0.00 |      1.88 |       7.29 |      0.00 |         0.00 |      0.00 |         0.06 |

**NWE kicker**

| player          |   fg_made |   xp_made |   kicking_points |
|:----------------|----------:|----------:|-----------------:|
| Andy Borregales |      1.12 |      2.35 |             5.72 |

**NWE defenders (vs NYJ offense)**

| player            |   tackles |   sacks |   def_int |
|:------------------|----------:|--------:|----------:|
| Robert Spillane   |      7.49 |    0.00 |      0.00 |
| Christian Elliss  |      7.20 |    0.26 |      0.00 |
| Charles Woods     |      4.89 |    0.00 |      0.00 |
| Elijah Ponder     |      4.54 |    1.66 |      0.00 |
| Marcus Jones      |      4.37 |    0.00 |      0.12 |
| Kevin Byard       |      4.03 |    0.00 |      0.00 |
| Craig Woodson     |      3.73 |    0.00 |      0.14 |
| Carlton Davis III |      3.51 |    0.00 |      0.00 |

## NYJ vs NWE
Projected 56 plays, 62% dropbacks, 29.5 pass att, 21.0 runs, 3.5 sacks. QB: Geno Smith
**Coaching style:** Deep-pass share low: 16% (league 19%); 4th-down go rate low: 11% (league 19%); Sack rate high: 10% (league 6%); Pass rate on 2nd & short low: 10% (league 31%); EPA/dropback low: -0.02 (league +0.06); Favors run inside left (31%).
**Market team total:** implied 18.0 (this team landed within the tolerance in 80% of its games, avg miss 4.3). Model 16.8 → blended 17.5: TD rates x1.04, yards x1.01.
**Model game script:** projected 16.8 – 20.9 (margin -4.1) → dropback rate +1.6%.
**Weather:** forecast 52°F, wind 6 mph → pass yds x1.00, long FG x1.00.
**Strength of schedule:** opp pass D x0.95, opp scoring D x0.95 (raw stats re-rated against the opponents actually faced).
**Out:** Dylan Parham (carried from week 5 report: Out (Knee)), Breece Hall (carried from week 5 report: Out (Quadricep)), Adonai Mitchell (carried from week 5 report: Out (Finger)), Francisco Mauigoa (carried from week 5 report: Out (Quadricep)).
**Coach angle:** HC Aaron Glenn (young HC, 1 prior seasons); plays called by OC Frank Reich (veteran play-caller, 5 seasons calling); career balanced (-0.9 pts pass rate vs league, 5 seasons); spreads it around; this season top target share 31%.
**NWE secondary:** DC Terrell Williams, man-leaning: Shadow man coverage with Gonzalez when available; outside Carlton Davis III (OUT) / Christian Gonzalez (OUT); nickel Marcus Jones; weak spot: Both starting corners were out in week 5; [research confidence medium, 2026-10-14].

**What worked last game → this week vs NWE** (failed play types cut, volume moved to what worked; `NWE allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player          | cut (failed last game)                                                                                               | more of                                                                                | NWE allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:----------------|:---------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Kenyon Sadiq    | short_right (100% failed)                                                                                            | short_left x2.0, deep_left x2.0, short_middle x2.0, deep_right x2.0, deep_middle x2.0  | x0.96, x0.93, x1.18, x0.95, x1.00 |         0.0 |        10.7 |        -0.0 |         -0.0 |       49.5 |
| Braelon Allen   | short_right (100% failed)                                                                                            | short_left x2.2, deep_left x2.2, short_middle x2.2, deep_right x2.2, deep_middle x2.2  | x0.96, x0.93, x1.18, x0.95, x1.00 |         0.0 |         4.2 |         0.0 |          0.3 |       90.5 |
| Braelon Allen   | run inside_right (22% failed), run middle (33% failed), run inside_left (22% failed), run outside_right (50% failed) | run outside_left x1.3                                                                  | x0.92                             |         0.0 |         4.2 |         0.0 |          0.3 |       90.5 |
| Garrett Wilson  | short_left (67% failed), short_right (20% failed), deep_right (100% failed)                                          | deep_left x1.6, short_middle x1.6, short_right x1.3, deep_middle x1.6                  | x0.93, x1.18, x0.96, x1.00        |         0.0 |         4.1 |         0.0 |          0.0 |       78.7 |
| Mason Taylor    | short_right (100% failed)                                                                                            | short_left x1.6, deep_left x1.6, short_middle x1.6, deep_right x1.6, deep_middle x1.6  | x0.96, x0.93, x1.18, x0.95, x1.00 |         0.0 |         1.5 |         0.0 |          0.0 |       11.7 |
| Isaiah Williams | deep_right (100% failed)                                                                                             | short_left x1.1, deep_left x1.1, short_middle x1.1, short_right x1.1, deep_middle x1.1 | x0.96, x0.93, x1.18, x0.96, x1.00 |         0.0 |        -1.3 |        -0.0 |         -0.0 |       28.0 |
| Jelani Woods    | short_right (100% failed)                                                                                            | short_left x1.7, deep_left x1.7, short_middle x1.7, deep_right x1.7, deep_middle x1.7  | x0.96, x0.93, x1.18, x0.95, x1.00 |         0.0 |         1.0 |         0.0 |          0.0 |        7.3 |
| Tim Patrick     | short_right (50% failed)                                                                                             | short_left x1.4, deep_left x1.4, short_middle x1.4, deep_right x1.4, deep_middle x1.4  | x0.96, x0.93, x1.18, x0.95, x1.00 |        -0.0 |         0.4 |         0.0 |          0.0 |        7.7 |

**NWE defensive weak spots:** play-action dropbacks: 8.0 allowed vs league 6.9 (41 plays).
- NWE struggle: Wk3 vs JAX: +0.22 EPA/play allowed (norm -0.08). Why: outside runs 6.6 yds/play vs 4.3 in other games; missing starters: Craig Woodson (S); 3rd/4th downs converted 70% vs 35%; red-zone TD rate per play 29% vs 14%; JAX is a strong offense (+0.14 EPA/play in its other games) → counted at 50% weight (those starters are available now)
- NWE struggle: Wk4 vs BUF: +0.12 EPA/play allowed (norm -0.05). Why: deep passes 16.1 yds/play vs 9.3 in other games; WRs 10.1 yds/target vs 6.4 in other games; 8 explosive plays vs 3.0 per other game; missing starters: Christian Gonzalez (CB); when blitzing 6.9 yds/dropback vs 4.7 in other games
**Offenses like NYJ that faced NWE:** LVR (similarity 0.44: -0.8 pass / -1.6 run yds/play vs their norm), JAX (similarity 0.24: -1.9 pass / +1.0 run yds/play vs their norm), BUF (similarity 0.08: -1.6 pass / -0.1 run yds/play vs their norm) → NYJ pass x1.00, run x0.98.
**NWE defensive scheme (online/tagged):** blitz: heavy, coverage: avg, shell: two_high [online (high)].
- NWE is soft deep (+0.67 EPA/deep att vs league +0.43); NYJ throws deep 16%.
- NWE brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed +0.48 on 11 attempts. NYJ 3rd-down deep share 19%.
- Best matchups: pass_short_middle (x1.18), pass_deep_middle (x1.00); worst: run_inside_right (x0.84).
- NWE blitzes 35% of dropbacks (league 32%, FTN charting); NYJ gains x1.15 as much per dropback vs the blitz as other offenses (44 blitzed dropbacks) -> pass yards x1.01
- NYJ short plays vs two high shell defenses: x1.08 vs how other offenses fare (98 plays)
- NYJ run plays vs two high shell defenses: x0.95 vs how other offenses fare (74 plays)
- NYJ deep-throw rate vs two high shell: x1.18
- NWE DBs out: Carlton Davis (18 tgts, 7.4 yds/tgt allowed), Christian Gonzalez (18 tgts, 5.8 yds/tgt allowed) -> coverage 7.7 → 8.2 yds/tgt; WR yards x1.07
- NWE shadow corner Christian Gonzalez is out: no shadow this week

| player          | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:----------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Geno Smith      | QB    |     214.34 |      1.22 |            0.36 |      2.45 |      15.32 |      0.00 |         0.00 |      0.00 |         0.07 |
| Garrett Wilson  | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      9.20 |         6.21 |     73.70 |         0.38 |
| Braelon Allen   | RB    |       0.00 |      0.00 |            0.00 |     18.73 |      67.40 |      3.32 |         2.08 |     22.19 |         0.51 |
| Kenyon Sadiq    | TE    |       0.00 |      0.00 |            0.00 |      0.17 |       0.56 |      5.85 |         3.46 |     48.09 |         0.21 |
| Isaiah Williams | WR    |       0.00 |      0.00 |            0.00 |      0.53 |       2.06 |      3.48 |         2.26 |     24.26 |         0.16 |
| Jeremy Ruckert  | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.82 |         1.23 |     12.36 |         0.09 |

**NYJ kicker**

| player        |   fg_made |   xp_made |   kicking_points |
|:--------------|----------:|----------:|-----------------:|
| Jason Sanders |      1.25 |      1.81 |             5.54 |

**NYJ defenders (vs NWE offense)**

| player             |   tackles |   sacks |   def_int |
|:-------------------|----------:|--------:|----------:|
| Dane Belton        |      7.92 |    0.22 |      0.00 |
| Jamien Sherwood    |      7.09 |    0.00 |      0.00 |
| Demario Davis      |      6.98 |    0.33 |      0.00 |
| David Bailey       |      5.17 |    0.92 |      0.00 |
| Minkah Fitzpatrick |      5.01 |    0.00 |      0.55 |
| Azareye'h Thomas   |      3.85 |    0.00 |      0.00 |
| Jowon Briggs       |      3.34 |    0.34 |      0.00 |
| Andre Cisco        |      3.25 |    0.17 |      0.00 |

## NYG vs NOR
Projected 64 plays, 56% dropbacks, 31.9 pass att, 27.7 runs, 2.4 sacks. QB: Jameis Winston
**Coaching style:** Neutral-script pass rate low: 55% (league 59%); Early-down pass rate low: 45% (league 53%); Deep-pass share high: 22% (league 19%); 3rd-down deep share high: 25% (league 21%); 4th-down go rate low: 11% (league 19%); Pass rate on 3rd & short low: 0% (league 41%); 3rd-down conversion high: 47% (league 42%); EPA/dropback high: +0.13 (league +0.06); EPA/run low: -0.23 (league -0.09); Favors run inside left (33%).
**Model game script:** projected 26.8 – 19.6 (margin +7.2) → dropback rate -2.9%.
**Weather:** forecast 56°F, wind 7 mph → pass yds x1.00, long FG x1.00.
**Strength of schedule:** own pass yds x0.93, own scoring x0.93, opp scoring D x0.97 (raw stats re-rated against the opponents actually faced).
**Out:** Jason Pinnock (carried from week 5 report: Out (Concussion)), Chauncey Golston (carried from week 5 report: Out (Neck)).
**Coach angle:** HC John Harbaugh (new to team, 18 prior seasons); plays called by OC Matt Nagy (developing play-caller, 3 seasons calling); career balanced (+1.2 pts pass rate vs league, 3 seasons); leans on stars; this season top target share 31%.
**NOR secondary:** DC Brandon Staley, zone-leaning: Zone-heavy off coverage; light box; two-high safety shells; outside Kool-Aid McKinstry / Quincy Riley; nickel Jonas Sanker; weak spot: Safety Jonas Sanker covering slot receivers and tight ends after Alontae Taylor left; [research confidence medium, 2026-10-14].

**What worked last game → this week vs NOR** (failed play types cut, volume moved to what worked; `NOR allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player           | cut (failed last game)                                                                                                           | more of                                                                                | NOR allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:-----------------|:---------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Isaiah Likely    | short_left (33% failed), deep_right (100% failed), deep_middle (100% failed)                                                     | short_middle x1.4, short_right x1.4, deep_left x1.4                                    | x0.87, x0.92, x1.09               |        -0.0 |        -7.0 |         0.0 |          0.0 |       55.7 |
| Darnell Mooney   | short_left (100% failed), short_right (50% failed), deep_left (100% failed), deep_right (100% failed), deep_middle (100% failed) | short_middle x3.4, short_right x1.7                                                    | x0.87, x0.92                      |         0.0 |        -4.4 |        -0.0 |         -0.0 |       19.8 |
| Malik Nabers     | short_left (67% failed), short_middle (67% failed), short_right (43% failed), deep_left (50% failed), deep_right (100% failed)   | short_right x1.3, deep_left x1.2, deep_middle x2.3                                     | x0.92, x1.09, x0.99               |        -0.0 |         3.9 |         0.0 |          0.0 |       63.3 |
| Cam Skattebo     | run inside_right (50% failed), run middle (17% failed)                                                                           | run inside_left x1.2, run outside_left x1.2, run outside_right x1.2                    | x0.96, x1.11, x0.91               |         0.0 |         0.6 |        -0.0 |          0.9 |       87.2 |
| Cam Skattebo     | short_left (33% failed)                                                                                                          | short_middle x1.2, short_right x1.2, deep_left x1.2, deep_right x1.2, deep_middle x1.2 | x0.87, x0.92, x1.09, x0.96, x0.99 |         0.0 |         0.6 |        -0.0 |          0.9 |       87.2 |
| Theo Johnson     | short_right (100% failed)                                                                                                        | short_left x1.3, short_middle x1.3, deep_left x1.3, deep_right x1.3, deep_middle x1.3  | x0.97, x0.87, x1.09, x0.96, x0.99 |         0.0 |         1.2 |         0.0 |          0.0 |       13.0 |
| Tyrone Tracy Jr. | short_left (100% failed), short_middle (100% failed)                                                                             | short_right x2.4, deep_left x2.4, deep_right x2.4, deep_middle x2.4                    | x0.92, x1.09, x0.96, x0.99        |        -0.0 |         0.8 |        -0.0 |         -0.0 |       11.9 |
| Najee Harris     | run inside_left (50% failed), run outside_left (50% failed)                                                                      | run inside_right x1.4, run middle x1.4, run outside_right x1.4                         | x1.18, x0.99, x0.91               |         0.0 |         0.0 |        -0.0 |         -0.7 |       26.5 |

**NOR defensive weak spots:** 3rd-down conversions: 53% allowed vs league 42% (58 plays); inside runs: 4.5 allowed vs league 3.9 (100 plays); outside runs: 6.1 allowed vs league 4.9 (30 plays).
- NOR struggle: Wk4 vs ATL: +0.40 EPA/play allowed (norm +0.04). Why: vs play action 16.6 yds/dropback vs 5.0 in other games; outside runs 11.1 yds/play vs 4.3 in other games; missing starters: Kaden Elliss (LB), Carl Granderson (DE); WRs 13.3 yds/target vs 7.3 in other games; when blitzing 9.9 yds/dropback vs 5.8 in other games → counted at 50% weight (those starters are available now)
**Offenses like NYG that faced NOR:** LVR (similarity 0.37: -0.4 pass / +1.9 run yds/play vs their norm), BAL (similarity 0.27: -2.3 pass / -0.9 run yds/play vs their norm), DET (similarity 0.26: -2.2 pass / +1.0 run yds/play vs their norm) → NYG pass x0.97, run x1.00.
**NOR defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: single_high [online (high)].
- NOR is soft deep (+0.79 EPA/deep att vs league +0.43); NYG throws deep 22%.
- NOR brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed +0.35 on 9 attempts. NYG 3rd-down deep share 25%.
- Best matchups: run_inside_right (x1.18), run_outside_left (x1.11); worst: pass_short_middle (x0.87).
- Last game — worked: none; failed: pass_deep_right.
- NOR blitzes 35% of dropbacks (league 32%, FTN charting); NYG gains x0.79 as much per dropback vs the blitz as other offenses (61 blitzed dropbacks) -> pass yards x0.99
- NYG deep plays vs zone heavy coverage defenses: x1.05 vs how other offenses fare (23 plays)

| player         | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:---------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Jameis Winston | QB    |     195.99 |      1.67 |            0.35 |      1.84 |      12.94 |      0.00 |         0.00 |      0.00 |         0.07 |
| Isaiah Likely  | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      9.85 |         7.14 |     55.38 |         0.48 |
| Malik Nabers   | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      9.23 |         6.10 |     63.16 |         0.36 |
| Cam Skattebo   | RB    |       0.00 |      0.00 |            0.00 |     18.38 |      71.59 |      2.43 |         1.68 |     15.63 |         0.53 |
| Darnell Mooney | WR    |       0.00 |      0.00 |            0.00 |      0.17 |       0.68 |      3.53 |         2.50 |     18.48 |         0.13 |
| Najee Harris   | RB    |       0.00 |      0.00 |            0.00 |      6.75 |      25.11 |      0.27 |         0.19 |      1.68 |         0.25 |
| Malachi Fields | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.60 |         1.74 |     17.91 |         0.13 |
| Theo Johnson   | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.84 |         1.21 |     13.48 |         0.10 |

**NYG kicker**

| player        |   fg_made |   xp_made |   kicking_points |
|:--------------|----------:|----------:|-----------------:|
| Dominic Zvada |      2.30 |      2.65 |             9.54 |

**NYG defenders (vs NOR offense)**

| player           |   tackles |   sacks |   def_int |
|:-----------------|----------:|--------:|----------:|
| Arvell Reese     |      9.20 |    0.29 |      0.28 |
| Tremaine Edmunds |      8.68 |    0.54 |      0.00 |
| Greg Newsome II  |      4.65 |    0.00 |      0.30 |
| Jevon Holland    |      4.30 |    0.00 |      0.61 |
| Andru Phillips   |      4.10 |    0.58 |      0.00 |
| Tyler Nubin      |      3.88 |    0.00 |      0.00 |
| Deonte Banks     |      3.19 |    0.00 |      0.28 |
| Abdul Carter     |      3.07 |    0.47 |      0.00 |

## NOR vs NYG
Projected 62 plays, 68% dropbacks, 38.8 pass att, 20.1 runs, 2.1 sacks. QB: Tyler Shough
**Coaching style:** 3rd-down deep share high: 27% (league 21%); 4th-down go rate high: 34% (league 19%); No-huddle rate high: 15% (league 6%); Pass rate on 3rd & short low: 28% (league 41%); 3rd-down conversion high: 48% (league 42%); EPA/dropback low: -0.07 (league +0.06); EPA/run low: -0.17 (league -0.09); Favors run middle (40%).
**Model game script:** projected 19.6 – 26.8 (margin -7.2) → dropback rate +2.9%.
**Weather:** forecast 56°F, wind 7 mph → pass yds x1.00, long FG x1.00.
**Strength of schedule:** opp pass D x1.02, opp scoring D x1.03 (raw stats re-rated against the opponents actually faced).
**Out:** Kaden Elliss (carried from week 5 report: Out (Calf)), Anfernee Jennings (carried from week 5 report: Out (Knee)), Jeremiah Wright (carried from week 5 report: Out (Concussion)).
**Coach angle:** HC Kellen Moore (young HC, 1 prior seasons); calls own plays (veteran play-caller, 7 seasons calling); career balanced (-0.1 pts pass rate vs league, 7 seasons); typical; this season top target share 28%.
**NYG secondary:** DC Dennard Wilson, coverage lean unknown: New DC Wilson; physical press-oriented coverage approach; outside Deonte Banks / Greg Newsome II; nickel Dru Phillips; weak spot: Adebo reported on IR; Banks' coverage grade 73.3 (15th); [research confidence low, 2026-10-14].

**What worked last game → this week vs NYG** (failed play types cut, volume moved to what worked; `NYG allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player        | cut (failed last game)                                   | more of                                                                               | NYG allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:--------------|:---------------------------------------------------------|:--------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Bryce Lance   | short_right (100% failed), short_left (100% failed)      | short_middle x4.1, deep_middle x4.1, deep_left x4.1, deep_right x4.1                  | x1.02, x1.05, x0.92, x0.91        |        -0.0 |        13.0 |         0.0 |          0.0 |       35.7 |
| Alvin Kamara  | short_right (100% failed)                                | short_left x1.7, short_middle x1.7, deep_middle x1.7, deep_left x1.7, deep_right x1.7 | x0.96, x1.02, x1.05, x0.92, x0.91 |        -0.0 |         4.5 |         0.0 |          0.0 |       54.6 |
| Chris Olave   | short_middle (33% failed), deep_left (100% failed)       | short_right x1.1, short_left x1.1, deep_middle x1.1, deep_right x1.1                  | x1.01, x0.96, x1.05, x0.91        |        -0.0 |        -2.8 |         0.0 |          0.0 |       72.9 |
| Juwan Johnson | short_right (67% failed), short_middle (100% failed)     | short_left x1.6, deep_middle x1.6, deep_left x1.6, deep_right x1.6                    | x0.96, x1.05, x0.92, x0.91        |        -0.0 |         2.0 |         0.0 |          0.0 |       47.4 |
| Kendre Miller | run middle (67% failed), run outside_right (100% failed) | run inside_left x1.4, run inside_right x1.4, run outside_left x1.4                    | x1.05, x1.14, x1.17               |        -0.0 |        -0.0 |         0.0 |          0.7 |       45.7 |
| Devaughn Vele | short_left (40% failed), deep_left (100% failed)         | short_right x1.4, short_middle x1.4, deep_middle x1.4, deep_right x1.4                | x1.01, x1.02, x1.05, x0.91        |         0.0 |         0.3 |         0.0 |          0.0 |       47.7 |
| CJ Donaldson  | run inside_right (100% failed)                           | run inside_left x1.4, run middle x1.4, run outside_left x1.4, run outside_right x1.4  | x1.05, x1.30, x1.17, x1.17        |        -0.0 |        -0.0 |         0.0 |          0.1 |       12.9 |

**NYG defensive weak spots:** outside runs: 6.1 allowed vs league 4.9 (21 plays); inside runs: 4.3 allowed vs league 3.9 (81 plays).
- NYG struggle: Wk1 vs DAL: +0.22 EPA/play allowed (norm -0.01). Why: when blitzing 8.2 yds/dropback vs 4.6 in other games; 3rd/4th downs converted 73% vs 39%; red-zone TD rate per play 33% vs 21%; DAL is a strong offense (+0.11 EPA/play in its other games)
- NYG struggle: Wk2 vs LAR: +0.27 EPA/play allowed (norm -0.02). Why: deep passes 19.0 yds/play vs 3.0 in other games; WRs 15.1 yds/target vs 6.2 in other games; 10 explosive plays vs 3.0 per other game; missing starters: Deonte Banks (CB); inside runs 5.6 yds/play vs 4.0 in other games → counted at 50% weight (those starters are available now)
**Offenses like NOR that faced NYG:** DAL (similarity 0.27: -1.9 pass / -0.1 run yds/play vs their norm), ARI (similarity 0.26: -1.2 pass / +1.8 run yds/play vs their norm), TEN (similarity 0.24: +0.0 pass / +0.2 run yds/play vs their norm) → NOR pass x0.96, run x0.98.
**NYG defensive scheme (online/tagged):** blitz: heavy, coverage: avg, shell: two_high [online (high)].
- NYG brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed +0.03 on 7 attempts. NOR 3rd-down deep share 27%.
- Best matchups: run_middle (x1.30), run_outside_right (x1.17); worst: pass_deep_right (x0.91).
- NYG blitzes 40% of dropbacks (league 32%, FTN charting); NOR gains x0.86 as much per dropback vs the blitz as other offenses (72 blitzed dropbacks) -> pass yards x0.99
- NOR deep plays vs two high shell defenses: x1.06 vs how other offenses fare (22 plays)
- NOR run plays vs two high shell defenses: x1.08 vs how other offenses fare (91 plays)
- NOR deep-throw rate vs two high shell: x0.89
- NYG vs position groups: Juwan Johnson x0.95

| player        | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:--------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Tyler Shough  | QB    |     256.81 |      1.82 |            1.44 |      2.41 |      12.85 |      0.00 |         0.00 |      0.00 |         0.08 |
| Chris Olave   | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      9.92 |         7.10 |     69.23 |         0.29 |
| Juwan Johnson | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      7.13 |         4.88 |     46.48 |         0.40 |
| Devaughn Vele | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.98 |         4.71 |     45.73 |         0.26 |
| Alvin Kamara  | RB    |       0.00 |      0.00 |            0.00 |      6.93 |      27.68 |      3.96 |         2.63 |     26.64 |         0.31 |
| Kendre Miller | RB    |       0.00 |      0.00 |            0.00 |      9.06 |      36.37 |      1.58 |         1.08 |      9.07 |         0.32 |
| Bryce Lance   | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.90 |         1.60 |     36.35 |         0.13 |
| Noah Fant     | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.72 |         1.98 |     15.86 |         0.22 |
| CJ Donaldson  | RB    |       0.00 |      0.00 |            0.00 |      2.23 |       9.07 |      0.59 |         0.40 |      3.68 |         0.08 |

**NOR kicker**

| player         |   fg_made |   xp_made |   kicking_points |
|:---------------|----------:|----------:|-----------------:|
| Daniel Carlson |      0.63 |      2.29 |             4.16 |

**NOR defenders (vs NYG offense)**

| player             |   tackles |   sacks |   def_int |
|:-------------------|----------:|--------:|----------:|
| Pete Werner        |      7.13 |    0.20 |      0.00 |
| Danny Stutsman     |      6.62 |    0.00 |      0.00 |
| Jonas Sanker       |      6.58 |    0.00 |      0.00 |
| Justin Reid        |      6.18 |    0.00 |      0.00 |
| Julian Blackmon    |      5.46 |    0.00 |      0.35 |
| Kool-Aid McKinstry |      4.13 |    0.00 |      0.00 |
| Carl Granderson    |      3.30 |    0.68 |      0.00 |
| Quincy Riley       |      3.04 |    0.00 |      0.00 |

## PHI vs CAR
Projected 62 plays, 64% dropbacks, 36.1 pass att, 22.2 runs, 2.2 sacks. QB: Jalen Hurts
**Coaching style:** Deep-pass share low: 16% (league 19%); Red-zone pass rate low: 38% (league 53%); No-huddle rate high: 11% (league 6%); Pass rate on 3rd & short high: 55% (league 41%); Red-zone run share high: 61% (league 46%); 3rd-down conversion low: 33% (league 42%); EPA/dropback low: -0.09 (league +0.06); EPA/run low: -0.24 (league -0.09).
**Market team total:** implied 19.5 (this team landed within the tolerance in 80% of its games, avg miss 3.6). Model 22.0 → blended 20.5: TD rates x0.93, yards x0.98.
**Model game script:** projected 22.0 – 23.9 (margin -1.9) → dropback rate +0.8%.
**Weather:** forecast 56°F, wind 5 mph → pass yds x1.00, long FG x1.00.
**Offensive line:** starters out: Cam Jurgens, Drew Kendall → sack rate x1.01, yds/dropback x0.98, yds/carry x1.01 (measured effect per missing starter).
**Strength of schedule:** own pass yds x0.96, own run yds x1.04, own scoring x1.02 (raw stats re-rated against the opponents actually faced).
**Out:** Saquon Barkley (carried from week 5 report: Out (Hamstring)), Marcus Epps (carried from week 5 report: Out (Groin)), Marquise Brown (carried from week 5 report: Out (Ankle)), DeVonta Smith (carried from week 5 report: Out (Hamstring)), Drew Kendall (carried from week 5 report: Out (Knee)).
**Coach angle:** HC Nick Sirianni (veteran HC, 5 prior seasons); plays called by OC Sean Mannion (first-time play-caller, 0 seasons calling); no prior play-calling seasons: this season's data only; this season top target share 20%.
**CAR secondary:** DC Ejiro Evero, zone-leaning: 3-4 base; zone-heavy two-high shells and disguise; soft zone that rarely plays man (2025 description); outside Akayleb Evans / Will Lee III; nickel Chau Smith-Wade; weak spot: Passive off coverage when Horn is out; [research confidence low, 2026-10-14].

**What worked last game → this week vs CAR** (failed play types cut, volume moved to what worked; `CAR allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player           | cut (failed last game)                                                                                                | more of                                                                                | CAR allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:-----------------|:----------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Makai Lemon      | short_right (67% failed), short_left (50% failed)                                                                     | short_middle x1.7, deep_right x1.7, deep_left x1.7, deep_middle x1.7                   | x1.17, x0.99, x1.13, x0.91        |         0.0 |         7.9 |         0.0 |          0.0 |       50.3 |
| Dallas Goedert   | short_right (67% failed), short_left (67% failed), short_middle (33% failed)                                          | short_middle x1.3, deep_right x2.0, deep_left x2.0, deep_middle x2.0                   | x1.17, x0.99, x1.13, x0.91        |         0.0 |         7.6 |         0.0 |          0.0 |       40.3 |
| Johnny Mundt     | short_right (100% failed)                                                                                             | short_left x3.5, short_middle x3.5, deep_right x3.5, deep_left x3.5, deep_middle x3.5  | x0.98, x1.17, x0.99, x1.13, x0.91 |         0.0 |         4.8 |         0.0 |          0.0 |       12.7 |
| Zach Ertz        | short_middle (100% failed), deep_right (100% failed)                                                                  | short_right x1.8, short_left x1.8, deep_left x1.8, deep_middle x1.8                    | x1.01, x0.98, x1.13, x0.91        |        -0.0 |        -4.7 |         0.0 |          0.0 |       13.4 |
| Dameon Pierce    | run outside_left (67% failed), run outside_right (100% failed), run middle (50% failed), run inside_left (40% failed) | run inside_right x1.9, run inside_left x1.2                                            | x1.13, x1.09                      |         0.0 |         3.5 |         0.0 |         -0.3 |       33.2 |
| Dameon Pierce    | short_right (50% failed), short_left (100% failed)                                                                    | short_right x1.3, short_middle x2.6, deep_right x2.6, deep_left x2.6, deep_middle x2.6 | x1.01, x1.17, x0.99, x1.13, x0.91 |         0.0 |         3.5 |         0.0 |         -0.3 |       33.2 |
| Dontayvion Wicks | short_right (50% failed), deep_left (67% failed)                                                                      | short_left x1.3, short_middle x1.3, deep_right x1.3, deep_middle x1.3                  | x0.98, x1.17, x0.99, x0.91        |        -0.0 |         3.1 |         0.0 |          0.0 |       68.5 |
| Will Shipley     | short_left (100% failed)                                                                                              | short_right x1.6, short_middle x1.6, deep_right x1.6, deep_left x1.6, deep_middle x1.6 | x1.01, x1.17, x0.99, x1.13, x0.91 |        -0.0 |         0.9 |         0.0 |          1.4 |       44.0 |

**CAR defensive weak spots:** inside runs: 5.4 allowed vs league 3.9 (78 plays).
- CAR struggle: Wk1 vs CHI: +0.41 EPA/play allowed (norm -0.16). Why: inside runs 8.1 yds/play vs 4.0 in other games; missing starters: Patrick Jones II (LB), Zakee Wheatley (S); WRs 11.1 yds/target vs 7.7 in other games; 8 explosive plays vs 3.7 per other game; 3rd/4th downs converted 67% vs 36% → counted at 50% weight (those starters are available now)
- CAR struggle: Wk4 vs DET: +0.18 EPA/play allowed (norm -0.08). Why: vs play action 10.5 yds/dropback vs 4.8 in other games; missing starters: Jaycee Horn (CB), Michael Jackson (CB); WRs 10.4 yds/target vs 7.4 in other games; short passes 6.7 yds/play vs 5.3 in other games; DET is a strong offense (+0.17 EPA/play in its other games) → counted at 50% weight (those starters are available now)
**Offenses like PHI that faced CAR:** CLE (similarity 0.16: -1.0 pass / +1.0 run yds/play vs their norm), DET (similarity 0.08: +1.1 pass / -1.6 run yds/play vs their norm), CHI (similarity 0.05: +2.8 pass / +3.4 run yds/play vs their norm) → PHI pass x1.00, run x1.00.
**CAR defensive scheme (online/tagged):** blitz: heavy, coverage: zone_heavy [online (high)].
- CAR is soft deep (+0.54 EPA/deep att vs league +0.43); PHI throws deep 16%.
- CAR brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed -0.29 on 3 attempts. PHI 3rd-down deep share 19%.
- Best matchups: pass_short_middle (x1.17), pass_deep_left (x1.13); worst: pass_deep_middle (x0.91).
- CAR blitzes 32% of dropbacks (league 32%, FTN charting); PHI gains x0.79 as much per dropback vs the blitz as other offenses (68 blitzed dropbacks) -> pass yards x1.00
- PHI short plays vs zone heavy coverage defenses: x1.13 vs how other offenses fare (62 plays)
- PHI deep-throw rate vs zone heavy coverage: x1.21
- CAR vs position groups: Dallas Goedert x0.94

| player           | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-----------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Jalen Hurts      | QB    |     240.12 |      1.48 |            0.75 |      4.17 |      23.88 |      0.00 |         0.00 |      0.00 |         0.17 |
| Dontayvion Wicks | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      8.25 |         4.81 |     64.53 |         0.26 |
| Makai Lemon      | WR    |       0.00 |      0.00 |            0.00 |      0.19 |       0.76 |      6.39 |         3.79 |     45.99 |         0.19 |
| Dallas Goedert   | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.05 |         2.90 |     37.66 |         0.25 |
| Will Shipley     | RB    |       0.00 |      0.00 |            0.00 |      6.69 |      28.67 |      2.38 |         1.43 |     13.93 |         0.32 |
| Darius Cooper    | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.03 |         2.16 |     33.52 |         0.28 |
| Tank Bigsby      | RB    |       0.00 |      0.00 |            0.00 |      8.71 |      36.19 |      1.19 |         0.72 |      6.05 |         0.34 |
| Dameon Pierce    | RB    |       0.00 |      0.00 |            0.00 |      4.44 |      18.56 |      2.02 |         1.19 |     14.07 |         0.23 |
| Zach Ertz        | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.50 |         1.52 |     12.24 |         0.09 |
| Johnny Mundt     | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.57 |         0.86 |     12.13 |         0.06 |

**PHI kicker**

| player       |   fg_made |   xp_made |   kicking_points |
|:-------------|----------:|----------:|-----------------:|
| Jake Elliott |      0.97 |      2.40 |             5.30 |

**PHI defenders (vs CAR offense)**

| player               |   tackles |   sacks |   def_int |
|:---------------------|----------:|--------:|----------:|
| Jihaad Campbell      |      7.85 |    0.20 |      0.00 |
| Zack Baun            |      6.91 |    0.00 |      0.00 |
| Cooper DeJean        |      6.61 |    0.00 |      0.21 |
| Riq Woolen           |      4.78 |    0.00 |      0.00 |
| Quinyon Mitchell     |      4.77 |    0.00 |      0.26 |
| Andrew Mukuba        |      4.47 |    0.00 |      0.22 |
| Jeremiah Trotter Jr. |      3.98 |    0.00 |      0.00 |
| Jordan Davis         |      3.50 |    0.00 |      0.00 |

## CAR vs PHI
Projected 67 plays, 64% dropbacks, 40.4 pass att, 24.1 runs, 1.8 sacks. QB: Bryce Young
**Coaching style:** Neutral-script pass rate high: 65% (league 59%); Early-down pass rate high: 61% (league 53%); 3rd-down deep share low: 16% (league 21%); Red-zone pass rate high: 69% (league 53%); 4th-down go rate high: 27% (league 19%); Red-zone run share low: 30% (league 46%); EPA/dropback high: +0.20 (league +0.06); Favors run inside left (32%).
**Model game script:** projected 23.9 – 22.0 (margin +1.9) → dropback rate -0.8%.
**Weather:** forecast 56°F, wind 5 mph → pass yds x1.00, long FG x1.00.
**Strength of schedule:** opp pass D x0.97 (raw stats re-rated against the opponents actually faced).
**Coach angle:** HC Dave Canales (young HC, 2 prior seasons); calls own plays (developing play-caller, 3 seasons calling); career balanced (-0.9 pts pass rate vs league, 3 seasons); leans on stars; this season top target share 27%.
**PHI secondary:** DC Vic Fangio, zone-leaning: Fangio two-high quarters / match zone; DeJean at safety in base and slot in nickel; outside Riq Woolen / Quinyon Mitchell; nickel Cooper DeJean; [research confidence medium, 2026-10-14].

**What worked last game → this week vs PHI** (failed play types cut, volume moved to what worked; `PHI allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player            | cut (failed last game)                                                                | more of                                                                                | PHI allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:------------------|:--------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Darren Waller     | short_right (75% failed)                                                              | short_middle x1.5, deep_right x1.5, short_left x1.5, deep_left x1.5, deep_middle x1.5  | x1.19, x0.95, x1.30, x0.93, x0.86 |         0.0 |         4.3 |         0.0 |          0.0 |       54.9 |
| Brycen Tremayne   | short_right (100% failed)                                                             | short_middle x1.6, deep_right x1.6, short_left x1.6, deep_left x1.6, deep_middle x1.6  | x1.19, x0.95, x1.30, x0.93, x0.86 |         0.0 |         2.8 |         0.0 |          0.0 |       26.3 |
| John Metchie III  | short_middle (33% failed), short_left (100% failed)                                   | short_middle x1.3, deep_right x2.0, short_right x2.0, deep_left x2.0, deep_middle x2.0 | x1.19, x0.95, x1.23, x0.93, x0.86 |         0.0 |         2.7 |         0.0 |          0.0 |       30.0 |
| Chuba Hubbard     | short_right (100% failed)                                                             | short_middle x1.6, deep_right x1.6, short_left x1.6, deep_left x1.6, deep_middle x1.6  | x1.19, x0.95, x1.30, x0.93, x0.86 |         0.0 |         2.1 |         0.0 |          0.2 |      126.3 |
| Chuba Hubbard     | run inside_right (17% failed), run inside_left (17% failed), run middle (17% failed)  | run outside_left x1.2, run outside_right x1.2                                          | x1.08, x1.08                      |         0.0 |         2.1 |         0.0 |          0.2 |      126.3 |
| Tetairoa McMillan | short_left (33% failed), deep_left (100% failed)                                      | short_middle x1.2, deep_right x1.2, short_right x1.2, deep_middle x1.2                 | x1.19, x0.95, x1.23, x0.86        |         0.0 |         1.7 |         0.0 |          0.0 |       93.2 |
| Tommy Tremble     | short_left (50% failed)                                                               | short_middle x1.2, deep_right x1.2, short_right x1.2, deep_left x1.2, deep_middle x1.2 | x1.19, x0.95, x1.23, x0.93, x0.86 |         0.0 |         1.0 |         0.0 |          0.0 |       37.3 |
| AJ Dillon         | run outside_left (100% failed), run inside_left (50% failed), run middle (50% failed) | run inside_right x1.8, run outside_right x1.8                                          | x1.00, x1.08                      |         0.0 |         0.0 |         0.0 |         -0.8 |       22.3 |

**Offenses like CAR that faced PHI:** TEN (similarity 0.15: +2.8 pass / +0.8 run yds/play vs their norm), LAR (similarity 0.15: -1.7 pass / -0.4 run yds/play vs their norm), WAS (similarity 0.11: -1.2 pass / -0.4 run yds/play vs their norm) → CAR pass x1.00, run x1.01.
**PHI defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: two_high [online (high)].
- Best matchups: pass_short_left (x1.30), pass_short_right (x1.23); worst: pass_deep_middle (x0.86).
- Last game — worked: pass_deep_right; failed: none.
- CAR short plays vs zone heavy coverage defenses: x1.12 vs how other offenses fare (39 plays)
- CAR run plays vs zone heavy coverage defenses: x1.06 vs how other offenses fare (25 plays)
- CAR short plays vs two high shell defenses: x1.11 vs how other offenses fare (39 plays)
- CAR run plays vs two high shell defenses: x1.06 vs how other offenses fare (25 plays)
- PHI DBs out: Marcus Epps (7 tgts, 9.3 yds/tgt allowed) -> coverage 7.7 → 7.6 yds/tgt; WR yards x0.99

| player            | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Bryce Young       | QB    |     309.80 |      1.52 |            0.68 |      0.74 |       5.73 |      0.00 |         0.00 |      0.00 |         0.04 |
| Chuba Hubbard     | RB    |       0.00 |      0.00 |            0.00 |     20.13 |     101.49 |      2.85 |         1.97 |     21.81 |         0.63 |
| Tetairoa McMillan | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      9.95 |         6.38 |     86.17 |         0.34 |
| Darren Waller     | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.80 |         3.80 |     50.34 |         0.25 |
| Jalen Coker       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.88 |         3.17 |     41.14 |         0.17 |
| Tommy Tremble     | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.36 |         2.76 |     34.02 |         0.12 |
| John Metchie III  | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.36 |         2.03 |     27.56 |         0.13 |
| Brycen Tremayne   | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.59 |         1.57 |     23.77 |         0.08 |
| AJ Dillon         | RB    |       0.00 |      0.00 |            0.00 |      3.83 |      17.09 |      0.69 |         0.45 |      4.77 |         0.12 |
| Mitchell Evans    | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.75 |         1.14 |     13.61 |         0.06 |

**CAR kicker**

| player          |   fg_made |   xp_made |   kicking_points |
|:----------------|----------:|----------:|-----------------:|
| Ryan Fitzgerald |      2.08 |      2.25 |             8.48 |

**CAR defenders (vs PHI offense)**

| player              |   tackles |   sacks |   def_int |
|:--------------------|----------:|--------:|----------:|
| Devin Lloyd         |      8.25 |    0.28 |      0.49 |
| Bobby Okereke       |      7.33 |    0.00 |      0.25 |
| Akayleb Evans       |      5.89 |    0.00 |      0.00 |
| Will Lee III        |      5.18 |    0.00 |      0.00 |
| Lathan Ransom       |      5.17 |    0.00 |      0.00 |
| Tre'von Moehrig     |      4.86 |    0.00 |      0.00 |
| Zakee Wheatley      |      4.24 |    0.00 |      0.00 |
| Princely Umanmielen |      3.14 |    1.00 |      0.00 |

## TAM vs PIT
Projected 59 plays, 61% dropbacks, 28.7 pass att, 23.2 runs, 2.8 sacks. QB: Jalon Daniels
**Coaching style:** Sack rate high: 9% (league 6%); Pass rate on 3rd & short high: 61% (league 41%); EPA/dropback low: -0.10 (league +0.06); EPA/run high: +0.01 (league -0.09); Favors run inside right (32%).
**Market team total:** implied 18.5 (this team landed within the tolerance in 60% of its games, avg miss 4.3). Model 20.2 → blended 19.2: TD rates x0.95, yards x0.98.
**Model game script:** projected 20.2 – 21.3 (margin -1.2) → dropback rate +0.5%.
**Weather:** forecast 78°F, wind 18 mph, rain/snow → pass yds x0.92, long FG x1.01.
**Strength of schedule:** own run yds x0.96, own scoring x1.02, opp pass D x1.03 (raw stats re-rated against the opponents actually faced).
**Out:** Baker Mayfield (carried from week 5 report: Out (Thumb)), Antoine Winfield Jr. (carried from week 5 report: Out (Rib)), SirVocea Dennis (carried from week 5 report: Out (Ankle)), Benjamin Morrison (carried from week 5 report: Out (Quadricep)).
**Coach angle:** HC Todd Bowles (veteran HC, 11 prior seasons); plays called by OC Zac Robinson (developing play-caller, 2 seasons calling); career run-first (-2.5 pts pass rate vs league, 2 seasons); leans on stars; this season top target share 24%.
**PIT secondary:** DC Patrick Graham, zone-leaning: Game-plans week to week; zero man snaps reported in week 1; Ramsey used as the slot Star and in pressure packages; outside Asante Samuel Jr. / Jamel Dean (OUT); nickel Jalen Ramsey; weak spot: Joey Porter Jr. traded to DAL (reported); new corners not yet in sync per Ramsey; [research confidence low, 2026-10-14].

**What worked last game → this week vs PIT** (failed play types cut, volume moved to what worked; `PIT allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player         | cut (failed last game)                                                    | more of                                                                                    | PIT allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:---------------|:--------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Emeka Egbuka   | deep_left (50% failed), short_left (33% failed), short_right (75% failed) | short_left x1.2, short_middle x1.8, deep_middle x1.8, deep_right x1.8                      | x0.92, x0.93, x0.86, x0.94        |        -0.0 |         5.0 |         0.0 |          0.0 |       46.8 |
| Kenny Gainwell | short_left (100% failed), short_right (67% failed)                        | deep_left x3.0, short_middle x3.0, deep_middle x3.0, deep_right x3.0                       | x0.90, x0.93, x0.86, x0.94        |         0.0 |         4.9 |         0.0 |          0.0 |       35.6 |
| Bucky Irving   | run inside_left (29% failed)                                              | run inside_right x1.1, run outside_right x1.1, run outside_left x1.1, run middle x1.1      | x0.75, x0.98, x0.81, x0.77        |        -0.0 |         0.6 |         0.0 |         -1.5 |       78.8 |
| Bucky Irving   | short_right (33% failed)                                                  | deep_left x1.2, short_left x1.2, short_middle x1.2, deep_middle x1.2, deep_right x1.2      | x0.90, x0.92, x0.93, x0.86, x0.94 |        -0.0 |         0.6 |         0.0 |         -1.5 |       78.8 |
| Sean Tucker    | run middle (50% failed)                                                   | run inside_right x1.1, run inside_left x1.1, run outside_right x1.1, run outside_left x1.1 | x0.75, x0.84, x0.98, x0.81        |         0.0 |         0.0 |         0.0 |          0.3 |        6.9 |
| Cade Otton     | short_right (33% failed)                                                  | deep_left x1.2, short_left x1.2, short_middle x1.2, deep_middle x1.2, deep_right x1.2      | x0.90, x0.92, x0.93, x0.86, x0.94 |        -0.0 |         0.3 |         0.0 |          0.0 |       37.3 |

**PIT defensive weak spots:** explosive plays: 11% allowed vs league 9% (276 plays); outside runs: 6.7 allowed vs league 4.9 (20 plays).
- PIT struggle: Wk3 vs CIN: +0.28 EPA/play allowed (norm -0.07). Why: deep passes 18.5 yds/play vs 12.4 in other games; 3rd/4th downs converted 57% vs 31%; red-zone TD rate per play 25% vs 15%
- PIT struggle: Wk4 vs CLE: +0.10 EPA/play allowed (norm -0.03). Why: outside runs 9.2 yds/play vs 6.0 in other games; WRs 10.1 yds/target vs 7.6 in other games; when blitzing 11.4 yds/dropback vs 8.7 in other games; red-zone TD rate per play 29% vs 12%
**Offenses like TAM that faced PIT:** IND (similarity 0.15: +1.1 pass / -1.4 run yds/play vs their norm), NWE (similarity 0.09: +0.4 pass / +1.6 run yds/play vs their norm), CLE (similarity 0.09: +3.0 pass / +0.8 run yds/play vs their norm) → TAM pass x1.01, run x1.00.
**PIT defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy [online (high)].
- Best matchups: pass_other (x1.00), run_outside_right (x0.98); worst: run_inside_right (x0.75).
- PIT blitzes 27% of dropbacks (league 32%, FTN charting); TAM gains x0.87 as much per dropback vs the blitz as other offenses (71 blitzed dropbacks) -> pass yards x1.01
- TAM deep plays vs zone heavy coverage defenses: x0.94 vs how other offenses fare (9 plays)
- TAM run plays vs zone heavy coverage defenses: x0.85 vs how other offenses fare (43 plays)
- TAM deep-throw rate vs zone heavy coverage: x0.90
- PIT DBs out: Jamel Dean (18 tgts, 8.2 yds/tgt allowed) -> coverage 7.9 → 8.0 yds/tgt; WR yards x1.00

| player           | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-----------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Jalon Daniels    | QB    |     179.54 |      0.92 |            0.74 |      4.36 |      33.06 |      0.00 |         0.00 |      0.00 |         0.15 |
| Bucky Irving     | RB    |       0.00 |      0.00 |            0.00 |     16.45 |      60.53 |      3.23 |         2.36 |     17.84 |         0.46 |
| Emeka Egbuka     | WR    |       0.00 |      0.00 |            0.00 |      0.33 |       1.23 |      6.74 |         4.44 |     43.95 |         0.20 |
| Cade Otton       | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.14 |         3.37 |     36.03 |         0.12 |
| Kenny Gainwell   | RB    |       0.00 |      0.00 |            0.00 |      3.45 |      11.52 |      3.42 |         1.94 |     23.46 |         0.21 |
| Chris Godwin Jr. | WR    |       0.00 |      0.00 |            0.00 |      0.51 |       1.84 |      4.26 |         3.10 |     25.77 |         0.13 |
| Ted Hurst III    | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.35 |         1.49 |     16.06 |         0.09 |
| Tez Johnson      | WR    |       0.00 |      0.00 |            0.00 |      0.25 |       0.93 |      1.65 |         1.04 |     11.27 |         0.06 |
| Sean Tucker      | RB    |       0.00 |      0.00 |            0.00 |      1.97 |       6.96 |      0.00 |         0.00 |      0.00 |         0.08 |

**TAM kicker**

| player           |   fg_made |   xp_made |   kicking_points |
|:-----------------|----------:|----------:|-----------------:|
| Chase McLaughlin |      2.33 |      1.71 |             8.70 |

**TAM defenders (vs PIT offense)**

| player               |   tackles |   sacks |   def_int |
|:---------------------|----------:|--------:|----------:|
| Josiah Trotter       |      7.20 |    0.23 |      0.12 |
| Alex Anzalone        |      4.82 |    0.32 |      0.24 |
| Jacob Parrish        |      4.70 |    0.00 |      0.22 |
| Keionte Scott        |      4.68 |    0.00 |      0.00 |
| Tykee Smith          |      4.61 |    0.00 |      0.00 |
| Antoine Winfield Jr. |      4.09 |    0.00 |      0.00 |
| A'Shawn Robinson     |      2.68 |    0.27 |      0.17 |
| Zyon McCollum        |      2.49 |    0.00 |      0.00 |

## PIT vs TAM
Projected 56 plays, 67% dropbacks, 34.8 pass att, 18.6 runs, 1.8 sacks. QB: Aaron Rodgers
**Coaching style:** Neutral-script pass rate high: 68% (league 59%); Early-down pass rate high: 64% (league 53%); 3rd-down deep share high: 29% (league 21%); Red-zone pass rate high: 76% (league 53%); Red-zone run share low: 24% (league 46%); EPA/dropback low: -0.05 (league +0.06); EPA/run high: +0.11 (league -0.09).
**Model game script:** projected 21.3 – 20.2 (margin +1.2) → dropback rate -0.5%.
**Weather:** forecast 78°F, wind 18 mph, rain/snow → pass yds x0.92, long FG x1.01.
**Strength of schedule:** own pass yds x1.03, own run yds x0.97, opp run D x1.03 (raw stats re-rated against the opponents actually faced).
**Out:** DeShon Elliott (carried from week 5 report: Out (Knee)), Jamel Dean (carried from week 5 report: Out (Ankle)), Michael Pittman (carried from week 5 report: Out (Foot)).
**Coach angle:** HC Mike McCarthy (new to team, 20 prior seasons); calls own plays (veteran play-caller, 15 seasons calling); career pass-first (+3.4 pts pass rate vs league, 15 seasons); typical; this season top target share 20%.
**TAM secondary:** DC Todd Bowles, mixed-leaning: Among the highest blitz rates; man 22.8% / zone 71.9% through five games (unverified figure); outside Zyon McCollum / Benjamin Morrison (OUT); nickel Jacob Parrish; weak spot: No edge rush to support the blitz; [research confidence medium, 2026-10-14].

**What worked last game → this week vs TAM** (failed play types cut, volume moved to what worked; `TAM allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player             | cut (failed last game)                                                       | more of                                                                                | TAM allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:-------------------|:-----------------------------------------------------------------------------|:---------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| DK Metcalf         | short_left (50% failed), short_middle (100% failed)                          | deep_left x1.5, short_right x1.5, deep_middle x1.5, deep_right x1.5                    | x0.98, x0.85, x1.06, x1.01        |         0.0 |         6.5 |         0.0 |          0.0 |       63.7 |
| Roman Wilson       | short_right (100% failed)                                                    | deep_left x1.4, short_left x1.4, short_middle x1.4, deep_middle x1.4, deep_right x1.4  | x0.98, x0.82, x0.78, x1.06, x1.01 |        -0.0 |         3.8 |         0.0 |          0.0 |       38.7 |
| Germie Bernard     | short_left (33% failed), short_right (50% failed), short_middle (67% failed) | deep_left x1.7, short_left x1.1, deep_middle x1.7, deep_right x1.7                     | x0.98, x0.82, x1.06, x1.01        |        -0.0 |         3.7 |         0.0 |          0.0 |       38.6 |
| Jaylen Warren      | run inside_left (33% failed), run outside_right (100% failed)                | run middle x1.2, run outside_left x1.2, run inside_right x1.2                          | x0.97, x0.84, x0.88               |         0.0 |         2.8 |         0.0 |         -0.6 |      112.8 |
| Jaylen Warren      | short_left (50% failed), short_right (25% failed)                            | deep_left x1.3, short_middle x1.3, deep_middle x1.3, deep_right x1.3                   | x0.98, x0.78, x1.06, x1.01        |         0.0 |         2.8 |         0.0 |         -0.6 |      112.8 |
| Pat Freiermuth     | deep_right (100% failed)                                                     | deep_left x1.2, short_left x1.2, short_right x1.2, short_middle x1.2, deep_middle x1.2 | x0.98, x0.82, x0.85, x0.78, x1.06 |        -0.0 |        -2.6 |         0.0 |          0.0 |       39.3 |
| Darnell Washington | short_left (100% failed)                                                     | deep_left x1.3, short_right x1.3, short_middle x1.3, deep_middle x1.3, deep_right x1.3 | x0.98, x0.85, x0.78, x1.06, x1.01 |        -0.0 |         2.5 |         0.0 |          0.0 |       27.0 |

**TAM defensive weak spots:** short passes: 6.6 allowed vs league 6.0 (137 plays).
**Offenses like PIT that faced TAM:** DAL (similarity 0.22: +1.0 pass / +0.4 run yds/play vs their norm), GNB (similarity 0.21: -0.2 pass / +1.6 run yds/play vs their norm), CIN (similarity 0.12: +0.4 pass / +0.7 run yds/play vs their norm) → PIT pass x1.00, run x1.02.
**TAM defensive scheme (online/tagged):** blitz: heavy, coverage: avg, shell: single_high [online (high)].
- TAM brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed -0.59 on 12 attempts. PIT 3rd-down deep share 29%.
- Best matchups: pass_deep_middle (x1.06), pass_deep_right (x1.01); worst: pass_short_middle (x0.78).
- TAM blitzes 42% of dropbacks (league 32%, FTN charting); PIT gains x0.77 as much per dropback vs the blitz as other offenses (52 blitzed dropbacks) -> pass yards x0.98
- PIT deep plays vs single high shell defenses: x1.14 vs how other offenses fare (23 plays)
- PIT short plays vs single high shell defenses: x0.86 vs how other offenses fare (65 plays)
- PIT run plays vs single high shell defenses: x0.89 vs how other offenses fare (37 plays)
- PIT deep-throw rate vs single high shell: x1.12
- TAM DBs out: Benjamin Morrison (17 tgts, 6.9 yds/tgt allowed), Antoine Winfield Jr. (7 tgts, 8.2 yds/tgt allowed) -> coverage 7.6 → 7.8 yds/tgt; WR yards x1.03

| player             | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Aaron Rodgers      | QB    |     242.32 |      1.65 |            1.01 |      0.72 |       5.38 |      0.00 |         0.00 |      0.00 |         0.02 |
| Jaylen Warren      | RB    |       0.00 |      0.00 |            0.00 |     15.59 |      68.36 |      5.67 |         3.76 |     41.82 |         0.45 |
| DK Metcalf         | WR    |       0.00 |      0.00 |            0.00 |      0.27 |       1.31 |      7.68 |         4.26 |     60.12 |         0.26 |
| Pat Freiermuth     | TE    |       0.00 |      0.00 |            0.00 |      0.70 |       2.64 |      5.62 |         3.88 |     34.92 |         0.36 |
| Roman Wilson       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.75 |         2.49 |     36.99 |         0.23 |
| Germie Bernard     | WR    |       0.00 |      0.00 |            0.00 |      0.27 |       1.15 |      4.78 |         2.77 |     35.84 |         0.16 |
| Darnell Washington | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.51 |         2.27 |     25.83 |         0.16 |

**PIT kicker**

| player        |   fg_made |   xp_made |   kicking_points |
|:--------------|----------:|----------:|-----------------:|
| Chris Boswell |      2.14 |      2.01 |             8.42 |

**PIT defenders (vs TAM offense)**

| player                 |   tackles |   sacks |   def_int |
|:-----------------------|----------:|--------:|----------:|
| Payton Wilson          |      8.96 |    0.34 |      0.00 |
| Jaquan Brisker         |      7.00 |    0.00 |      0.15 |
| Patrick Queen          |      6.98 |    0.00 |      0.18 |
| Jalen Ramsey           |      5.72 |    0.00 |      0.00 |
| Cameron Heyward        |      3.57 |    0.42 |      0.00 |
| Robert Spears-Jennings |      3.26 |    0.00 |      0.26 |
| Asante Samuel Jr.      |      3.15 |    0.00 |      0.00 |
| Yahya Black            |      3.08 |    0.00 |      0.00 |

## LAR vs ARI
Projected 64 plays, 58% dropbacks, 35.1 pass att, 27.3 runs, 1.4 sacks. QB: Matthew Stafford
**Coaching style:** Neutral-script pass rate high: 65% (league 59%); Early-down pass rate high: 61% (league 53%); Red-zone pass rate high: 60% (league 53%); 4th-down go rate high: 26% (league 19%); Sack rate low: 3% (league 6%); No-huddle rate high: 11% (league 6%); Pass rate on 2nd & short high: 57% (league 31%); 3rd-down conversion high: 50% (league 42%); EPA/dropback high: +0.16 (league +0.06); EPA/run high: -0.00 (league -0.09); Favors run middle (40%).
**Model game script:** projected 38.4 – 21.4 (margin +17.0) → dropback rate -6.8%.
**Coach angle:** HC Sean McVay (veteran HC, 9 prior seasons); calls own plays (veteran play-caller, 9 seasons calling); career balanced (+1.2 pts pass rate vs league, 9 seasons); typical; this season top target share 24%.
**ARI secondary:** DC Nick Rallis, coverage lean unknown: Heavy dime user (about 20% dime in 2025); young corners protected with structure and safety rotation; outside Garrett Williams / Denzel Burke; nickel Max Melton; weak spot: Young outside corners starting while Will Johnson is out; [research confidence low, 2026-10-14].

**What worked last game → this week vs ARI** (failed play types cut, volume moved to what worked; `ARI allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player          | cut (failed last game)                                                                                  | more of                                                                                | ARI allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:----------------|:--------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Davante Adams   | deep_left (100% failed), short_right (100% failed)                                                      | short_left x1.6, deep_right x1.6, deep_middle x1.6, short_middle x1.6                  | x1.14, x1.03, x0.91, x0.98        |         0.0 |         9.3 |         0.0 |          0.0 |       72.0 |
| Kyren Williams  | short_right (67% failed), deep_middle (100% failed)                                                     | short_left x1.5, deep_left x1.5, deep_right x1.5, short_middle x1.5                    | x1.14, x1.02, x1.03, x0.98        |         0.0 |         4.8 |         0.0 |          1.7 |      132.0 |
| Kyren Williams  | run middle (25% failed), run inside_right (50% failed)                                                  | run inside_left x1.2, run outside_left x1.2, run outside_right x1.2                    | x0.98, x0.93, x1.05               |         0.0 |         4.8 |         0.0 |          1.7 |      132.0 |
| Puka Nacua      | deep_right (67% failed), short_right (25% failed), deep_middle (100% failed), short_middle (40% failed) | short_left x1.4, deep_left x1.4                                                        | x1.14, x1.02                      |        -0.0 |        -4.8 |         0.0 |         -0.1 |       71.9 |
| Puka Nacua      | run outside_left (50% failed)                                                                           | run inside_left x1.3, run middle x1.3, run inside_right x1.3, run outside_right x1.3   | x0.98, x0.92, x1.01, x1.05        |        -0.0 |        -4.8 |         0.0 |         -0.1 |       71.9 |
| Tyler Higbee    | short_right (25% failed)                                                                                | short_left x1.2, deep_left x1.2, deep_right x1.2, deep_middle x1.2, short_middle x1.2  | x1.14, x1.02, x1.03, x0.91, x0.98 |        -0.0 |         1.3 |         0.0 |          0.0 |       42.5 |
| Blake Corum     | short_left (33% failed)                                                                                 | deep_left x1.2, deep_right x1.2, short_right x1.2, deep_middle x1.2, short_middle x1.2 | x1.02, x1.03, x1.11, x0.91, x0.98 |         0.0 |        -0.3 |         0.0 |          0.0 |       53.1 |
| Colby Parkinson | short_middle (100% failed)                                                                              | short_left x1.2, deep_left x1.2, deep_right x1.2, short_right x1.2, deep_middle x1.2   | x1.14, x1.02, x1.03, x1.11, x0.91 |         0.0 |        -0.0 |         0.0 |          0.0 |        9.2 |

**ARI defensive weak spots:** explosive plays: 12% allowed vs league 9% (260 plays); short passes: 7.4 allowed vs league 6.0 (106 plays); deep passes: 15.8 allowed vs league 11.9 (28 plays); play-action dropbacks: 8.3 allowed vs league 6.9 (40 plays).
- ARI struggle: Wk3 vs SFO: +0.49 EPA/play allowed (norm +0.03). Why: when blitzing 22.4 yds/dropback vs 4.9 in other games; WRs 17.4 yds/target vs 9.1 in other games; short passes 10.0 yds/play vs 6.7 in other games; inside runs 5.3 yds/play vs 3.7 in other games; 9 explosive plays vs 5.5 per other game
- ARI struggle: Wk5 vs DET: +0.32 EPA/play allowed (norm +0.07). Why: RBs 9.3 yds/target vs 4.0 in other games; TEs 16.0 yds/target vs 8.5 in other games; when blitzing 11.7 yds/dropback vs 7.1 in other games; missing starters: Andrew Wingard (S); DET is a strong offense (+0.14 EPA/play in its other games)
**Offenses like LAR that faced ARI:** DET (similarity 0.14: +0.9 pass / +1.3 run yds/play vs their norm), NYG (similarity 0.09: +1.8 pass / -0.5 run yds/play vs their norm), SFO (similarity 0.01: +3.7 pass / +0.8 run yds/play vs their norm) → LAR pass x0.99, run x1.01.
**ARI defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: cover4 [online (low)].
- ARI is soft deep (+1.13 EPA/deep att vs league +0.43); LAR throws deep 22%.
- Best matchups: pass_short_left (x1.14), pass_short_right (x1.11); worst: pass_deep_middle (x0.91).
- Last game — worked: none; failed: pass_deep_middle, pass_deep_right.
- ARI blitzes 25% of dropbacks (league 32%, FTN charting); LAR gains x0.91 as much per dropback vs the blitz as other offenses (64 blitzed dropbacks) -> pass yards x1.01
- LAR deep plays vs zone heavy coverage defenses: x0.93 vs how other offenses fare (25 plays)
- LAR run plays vs zone heavy coverage defenses: x0.94 vs how other offenses fare (66 plays)
- ARI DBs out: Andrew Wingard (8 tgts, 8.9 yds/tgt allowed) -> coverage 8.1 → 8.1 yds/tgt; WR yards x1.00

| player           | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-----------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Matthew Stafford | QB    |     296.31 |      3.58 |            0.85 |      0.97 |       6.35 |      0.00 |         0.00 |      0.00 |         0.04 |
| Kyren Williams   | RB    |       0.00 |      0.00 |            0.00 |     17.80 |      80.54 |      6.32 |         4.50 |     50.43 |         0.80 |
| Puka Nacua       | WR    |       0.00 |      0.00 |            0.00 |      0.78 |       3.45 |      8.66 |         6.12 |     68.20 |         0.53 |
| Davante Adams    | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.90 |         4.88 |     71.03 |         0.59 |
| Tyler Higbee     | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.74 |         3.19 |     41.45 |         0.38 |
| Blake Corum      | RB    |       0.00 |      0.00 |            0.00 |      8.36 |      36.04 |      2.19 |         1.48 |     16.86 |         0.42 |
| Konata Mumpfield | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.00 |         1.21 |     18.26 |         0.21 |

**LAR kicker**

| player         |   fg_made |   xp_made |   kicking_points |
|:---------------|----------:|----------:|-----------------:|
| Harrison Mevis |      1.03 |      4.71 |             7.81 |

**LAR defenders (vs ARI offense)**

| player          |   tackles |   sacks |   def_int |
|:----------------|----------:|--------:|----------:|
| Nate Landman    |      9.48 |    0.00 |      0.00 |
| Quentin Lake    |      7.28 |    0.00 |      0.22 |
| Kam Curl        |      5.21 |    0.00 |      0.00 |
| Omar Speights   |      4.96 |    0.62 |      0.00 |
| Kamren Kinchens |      4.67 |    0.17 |      0.00 |
| Byron Young     |      4.31 |    1.08 |      0.00 |
| Kobie Turner    |      4.00 |    0.00 |      0.00 |
| Trent McDuffie  |      3.41 |    0.00 |      0.27 |

## ARI vs LAR
Projected 63 plays, 70% dropbacks, 40.6 pass att, 18.5 runs, 2.5 sacks. QB: Jacoby Brissett
**Coaching style:** Red-zone pass rate high: 64% (league 53%); No-huddle rate high: 11% (league 6%); Pass rate on 2nd & short high: 52% (league 31%); Red-zone run share low: 38% (league 46%); EPA/dropback low: -0.02 (league +0.06); Favors run middle (37%).
**Model game script:** projected 21.4 – 38.4 (margin -17.0) → dropback rate +6.8%.
**Strength of schedule:** own pass yds x1.04 (raw stats re-rated against the opponents actually faced).
**Out:** Andrew Wingard (carried from week 5 report: Out (Knee)), Isaiah Adams (carried from week 5 report: Out (Ankle)).
**Coach angle:** HC Mike LaFleur (first-year HC, 0 prior seasons); calls own plays (developing play-caller, 2 seasons calling); career pass-first (+3.9 pts pass rate vs league, 2 seasons); spreads it around; this season top target share 29%.
**LAR secondary:** DC Chris Shula, zone-leaning: Zone lean (more Cover 3 than Cover 1); most dime in the NFL the last two seasons; McDuffie in man only 25.7% vs SF; outside Jaylen Watson / Trent McDuffie; nickel Quentin Lake; weak spot: Scheme may move toward more man under Jimmy Lake; [research confidence medium, 2026-10-14].

**What worked last game → this week vs LAR** (failed play types cut, volume moved to what worked; `LAR allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player          | cut (failed last game)                                                                       | more of                                                                                | LAR allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:----------------|:---------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Michael Wilson  | deep_right (100% failed), short_right (67% failed), deep_left (50% failed)                   | short_middle x1.8, short_left x1.8, deep_middle x1.8                                   | x0.94, x0.92, x0.90               |         0.0 |        -4.4 |         0.0 |          0.0 |       61.7 |
| Trey McBride    | deep_right (100% failed)                                                                     | short_middle x1.1, short_right x1.1, short_left x1.1, deep_left x1.1, deep_middle x1.1 | x0.94, x0.98, x0.92, x0.89, x0.90 |        -0.0 |        -2.9 |         0.0 |          0.0 |       54.2 |
| Jeremiyah Love  | short_left (100% failed)                                                                     | deep_right x1.4, short_middle x1.4, short_right x1.4, deep_left x1.4, deep_middle x1.4 | x0.85, x0.94, x0.98, x0.89, x0.90 |        -0.0 |         2.0 |         0.0 |         -0.7 |       59.9 |
| Jeremiyah Love  | run inside_right (50% failed), run inside_left (100% failed), run outside_right (67% failed) | run outside_left x1.7, run middle x1.7                                                 | x0.95, x0.99                      |        -0.0 |         2.0 |         0.0 |         -0.7 |       59.9 |
| Jalen Brooks    | deep_right (100% failed), short_middle (100% failed), deep_left (100% failed)                | short_right x2.5, short_left x2.5, deep_middle x2.5                                    | x0.98, x0.92, x0.90               |        -0.0 |        -2.2 |         0.0 |          0.0 |        7.3 |
| Kendrick Bourne | deep_right (100% failed), short_middle (50% failed)                                          | short_right x1.3, short_left x1.3, deep_left x1.3, deep_middle x1.3                    | x0.98, x0.92, x0.89, x0.90        |         0.0 |        -1.3 |         0.0 |          0.0 |       26.8 |
| Reggie Virgil   | short_right (100% failed)                                                                    | deep_right x3.4, short_middle x3.4, short_left x3.4, deep_left x3.4, deep_middle x3.4  | x0.85, x0.94, x0.92, x0.89, x0.90 |        -0.0 |         0.5 |         0.0 |          0.0 |        2.5 |

**LAR defensive weak spots:** vs RBs: 6.9 yds/target (league 5.3), x1.19 for RBs.
- LAR struggle: Wk1 vs SFO: +0.21 EPA/play allowed (norm -0.12). Why: outside runs 7.5 yds/play vs 2.3 in other games; TEs 4.4 yds/target vs 2.2 in other games; inside runs 5.1 yds/play vs 3.6 in other games; 3rd/4th downs converted 60% vs 28%; SFO is a strong offense (+0.25 EPA/play in its other games)
- LAR struggle: Wk5 vs BUF: +0.28 EPA/play allowed (norm -0.14). Why: RBs 18.3 yds/target vs 4.1 in other games; when blitzing 14.4 yds/dropback vs 3.3 in other games; short passes 13.8 yds/play vs 4.5 in other games; vs play action 11.3 yds/dropback vs 4.5 in other games; WRs 12.4 yds/target vs 6.6 in other games
**Offenses like ARI that faced LAR:** PHI (similarity 0.43: -3.4 pass / -0.0 run yds/play vs their norm), DEN (similarity 0.23: -0.5 pass / -1.0 run yds/play vs their norm), NYG (similarity 0.19: -2.4 pass / -1.7 run yds/play vs their norm) → ARI pass x0.96, run x0.98.
**LAR defensive scheme (online/tagged):** blitz: avg, coverage: avg, shell: two_high [online (high)].
- Best matchups: run_inside_right (x1.05), run_inside_left (x1.03); worst: pass_deep_right (x0.85).
- Last game — worked: pass_short_left, run_middle; failed: pass_deep_right, run_outside_right.
- LAR blitzes 34% of dropbacks (league 32%, FTN charting); ARI gains x0.89 as much per dropback vs the blitz as other offenses (58 blitzed dropbacks) -> pass yards x1.00
- LAR vs position groups: Trey McBride x0.82

| player              | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:--------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Jacoby Brissett     | QB    |     223.04 |      1.90 |            1.28 |      2.51 |      12.04 |      0.35 |         0.24 |      2.07 |         0.11 |
| Trey McBride        | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |     11.95 |         8.20 |     53.56 |         0.42 |
| Michael Wilson      | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |     10.44 |         6.52 |     60.49 |         0.38 |
| Jeremiyah Love      | RB    |       0.00 |      0.00 |            0.00 |     10.84 |      38.36 |      2.93 |         1.93 |     20.74 |         0.36 |
| Tyler Allgeier      | RB    |       0.00 |      0.00 |            0.00 |      6.00 |      21.44 |      2.47 |         1.69 |     15.97 |         0.27 |
| Kendrick Bourne     | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.96 |         2.69 |     25.94 |         0.13 |
| Marvin Harrison Jr. | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.67 |         1.53 |     17.36 |         0.14 |
| Elijah Higgins      | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.20 |         1.43 |     11.70 |         0.12 |

**ARI kicker**

| player      |   fg_made |   xp_made |   kicking_points |
|:------------|----------:|----------:|-----------------:|
| Chad Ryland |      1.55 |      2.38 |             7.02 |

**ARI defenders (vs LAR offense)**

| player         |   tackles |   sacks |   def_int |
|:---------------|----------:|--------:|----------:|
| Budda Baker    |      8.75 |    0.29 |      0.33 |
| Mack Wilson    |      8.24 |    0.00 |      0.00 |
| Jack Gibbens   |      7.86 |    0.04 |      0.00 |
| Roy Lopez      |      4.93 |    0.17 |      0.00 |
| Andrew Wingard |      4.70 |    0.00 |      0.19 |
| Denzel Burke   |      3.78 |    0.00 |      0.33 |
| Max Melton     |      3.71 |    0.00 |      0.00 |
| Zaven Collins  |      3.57 |    0.13 |      0.00 |

## KAN vs LAC
Projected 61 plays, 56% dropbacks, 30.9 pass att, 27.1 runs, 1.4 sacks. QB: Patrick Mahomes
**Coaching style:** Early-down pass rate high: 58% (league 53%); 3rd-down deep share high: 37% (league 21%); Red-zone pass rate high: 60% (league 53%); 4th-down go rate high: 26% (league 19%); Sack rate low: 4% (league 6%); No-huddle rate low: 0% (league 6%); EPA/dropback high: +0.22 (league +0.06); EPA/run high: +0.11 (league -0.09); Favors run middle (38%).
**Model game script:** projected 25.4 – 17.5 (margin +7.9) → dropback rate -3.2%.
**Weather:** forecast 65°F, wind 9 mph → pass yds x1.00, long FG x1.00.
**Strength of schedule:** own pass yds x0.97, own run yds x0.97, own scoring x0.98, opp scoring D x0.97 (raw stats re-rated against the opponents actually faced).
**Coach angle:** HC Andy Reid (veteran HC, 27 prior seasons); calls own plays (veteran play-caller, 13 seasons calling); career pass-first (+3.1 pts pass rate vs league, 13 seasons); typical; this season top target share 19%.
**LAC secondary:** DC Chris O'Leary, coverage lean unknown: First-year DC; more five- and six-man fronts at Western Michigan; outside Cam Hart / Donte Jackson (OUT); nickel Tarheeb Still; weak spot: Hart inconsistent; depth charts disagree on sides; [research confidence low, 2026-10-14].

**What worked last game → this week vs LAC** (failed play types cut, volume moved to what worked; `LAC allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player             | cut (failed last game)                                                               | more of                                                                                    | LAC allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:-------------------|:-------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Noah Gray          | short_left (100% failed), short_right (100% failed)                                  | deep_left x2.4, short_middle x2.4, deep_middle x2.4, deep_right x2.4                       | x1.01, x0.85, x0.91, x1.01        |         0.0 |         4.2 |         0.0 |          0.0 |       19.0 |
| Xavier Worthy      | short_right (33% failed), deep_right (100% failed)                                   | short_left x1.4, deep_left x1.4, short_middle x1.4, deep_middle x1.4                       | x0.95, x1.01, x0.85, x0.91        |        -0.0 |        -2.1 |         0.0 |          0.0 |       44.2 |
| Travis Kelce       | short_left (50% failed), short_middle (50% failed)                                   | short_right x1.3, deep_left x1.3, deep_middle x1.3, deep_right x1.3                        | x0.91, x1.01, x0.91, x1.01        |         0.0 |         1.9 |         0.0 |          0.0 |       43.9 |
| Jalen Royals       | short_left (100% failed), short_middle (100% failed)                                 | short_right x2.0, deep_left x2.0, deep_middle x2.0, deep_right x2.0                        | x0.91, x1.01, x0.91, x1.01        |        -0.0 |         1.2 |         0.0 |          0.0 |       10.2 |
| Khyiris Tonga      | run middle (100% failed)                                                             | run inside_left x2.9, run outside_right x2.9, run inside_right x2.9, run outside_left x2.9 | x1.08, x1.03, x1.03, x1.16        |         0.0 |         0.0 |         0.0 |          0.9 |        3.5 |
| Kenneth Walker III | run inside_left (20% failed), run middle (17% failed), run inside_right (29% failed) | run outside_right x1.2, run outside_left x1.2                                              | x1.03, x1.16                      |        -0.0 |        -0.0 |         0.0 |          0.9 |      142.6 |
| Tyquan Thornton    | short_left (50% failed), deep_middle (100% failed)                                   | short_right x1.3, deep_left x1.3, short_middle x1.3, deep_right x1.3                       | x0.91, x1.01, x0.85, x1.01        |         0.0 |        -0.8 |         0.0 |          0.0 |       34.0 |
| Cyrus Allen        | deep_middle (100% failed)                                                            | short_left x1.3, short_right x1.3, deep_left x1.3, short_middle x1.3, deep_right x1.3      | x0.95, x0.91, x1.01, x0.85, x1.01 |        -0.0 |        -0.7 |         0.0 |          0.0 |        2.9 |

**LAC defensive weak spots:** deep passes: 14.6 allowed vs league 11.9 (19 plays).
- LAC struggle: Wk1 vs ARI: +0.14 EPA/play allowed (norm -0.12). Why: when blitzing 7.1 yds/dropback vs 3.5 in other games; outside runs 6.5 yds/play vs 5.0 in other games
**Offenses like KAN that faced LAC:** SEA (similarity 0.12: -1.2 pass / +0.9 run yds/play vs their norm), DEN (similarity 0.04: -1.7 pass / -0.2 run yds/play vs their norm), BUF (similarity 0.04: -3.3 pass / +0.9 run yds/play vs their norm) → KAN pass x0.99, run x1.00.
**LAC defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: two_high [online (high)].
- Best matchups: run_outside_left (x1.16), run_inside_left (x1.08); worst: pass_short_middle (x0.85).
- LAC blitzes 27% of dropbacks (league 32%, FTN charting); KAN gains x1.16 as much per dropback vs the blitz as other offenses (38 blitzed dropbacks) -> pass yards x0.99
- KAN run plays vs two high shell defenses: x1.06 vs how other offenses fare (70 plays)
- KAN deep-throw rate vs two high shell: x1.19
- LAC DBs out: Derwin James (11 tgts, 6.8 yds/tgt allowed), Donte Jackson (9 tgts, 7.8 yds/tgt allowed) -> coverage 8.0 → 8.2 yds/tgt; WR yards x1.03
- LAC vs position groups: Kenneth Walker III x0.94

| player             | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Patrick Mahomes    | QB    |     209.81 |      1.41 |            0.69 |      1.78 |      13.74 |      0.00 |         0.00 |      0.00 |         0.10 |
| Kenneth Walker III | RB    |       0.00 |      0.00 |            0.00 |     22.71 |     117.66 |      4.03 |         2.53 |     22.73 |         0.74 |
| Xavier Worthy      | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.05 |         3.87 |     42.01 |         0.24 |
| Travis Kelce       | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.10 |         3.25 |     41.27 |         0.24 |
| Tyquan Thornton    | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.92 |         2.52 |     31.57 |         0.20 |
| Rashee Rice        | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.05 |         2.59 |     31.80 |         0.16 |
| Emmett Johnson     | RB    |       0.00 |      0.00 |            0.00 |      3.44 |      15.87 |      0.95 |         0.63 |      5.98 |         0.15 |
| Noah Gray          | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.07 |         1.17 |     18.04 |         0.08 |

**KAN kicker**

| player          |   fg_made |   xp_made |   kicking_points |
|:----------------|----------:|----------:|-----------------:|
| Harrison Butker |      1.93 |      2.68 |             8.46 |

**KAN defenders (vs LAC offense)**

| player           |   tackles |   sacks |   def_int |
|:-----------------|----------:|--------:|----------:|
| Nick Bolton      |     11.24 |    0.00 |      0.00 |
| Drue Tranquill   |      8.55 |    0.00 |      0.00 |
| L'Jarius Sneed   |      7.24 |    0.00 |      0.00 |
| Mansoor Delane   |      6.89 |    0.00 |      0.23 |
| Jaden Hicks      |      6.48 |    0.00 |      0.00 |
| Alohi Gilman     |      5.05 |    0.00 |      0.00 |
| George Karlaftis |      4.54 |    0.00 |      0.34 |
| Nohl Williams    |      4.45 |    0.80 |      0.00 |

## LAC vs KAN
Projected 63 plays, 62% dropbacks, 33.1 pass att, 23.9 runs, 2.4 sacks. QB: Justin Herbert
**Coaching style:** Neutral-script pass rate low: 46% (league 59%); Early-down pass rate low: 37% (league 53%); 3rd-down deep share high: 25% (league 21%); Sack rate high: 10% (league 6%); Pass rate on 3rd & short high: 55% (league 41%); 3rd-down conversion low: 36% (league 42%); EPA/dropback low: -0.24 (league +0.06); EPA/run low: -0.18 (league -0.09).
**Model game script:** projected 17.5 – 25.4 (margin -7.9) → dropback rate +3.2%.
**Weather:** forecast 65°F, wind 9 mph → pass yds x1.00, long FG x1.00.
**Offensive line:** starters out: Joe Alt → sack rate x1.00, yds/dropback x0.99, yds/carry x1.01 (measured effect per missing starter).
**Strength of schedule:** own pass yds x1.03, own scoring x0.94, opp pass D x1.03 (raw stats re-rated against the opponents actually faced).
**Out:** Donte Jackson (carried from week 5 report: Out (Hamstring)), Derwin James (carried from week 5 report: Out (Hamstring)), Kayode Awosika (carried from week 5 report: Out (Fibula)), Trey Lance (carried from week 5 report: Doubtful (Groin)), Trevor Penning (carried from week 5 report: Out (Concussion)), Quentin Johnston (carried from week 5 report: Out (Chest)), Joe Alt (carried from week 5 report: Out (Neck)), Brenen Thompson (carried from week 5 report: Out (Quadricep)).
**Coach angle:** HC Jim Harbaugh (veteran HC, 15 prior seasons); plays called by OC Mike McDaniel (developing play-caller, 4 seasons calling); career balanced (+1.1 pts pass rate vs league, 4 seasons); typical; this season top target share 18%.
**KAN secondary:** DC Steve Spagnuolo, mixed-leaning: Blitz-heavy (third-highest blitz rate in 2025); Sneed moved to the nickel and used as a blitzer; outside Nohl Williams / Mansoor Delane; nickel L'Jarius Sneed; weak spot: Young outside corners; [research confidence medium, 2026-10-14].

**What worked last game → this week vs KAN** (failed play types cut, volume moved to what worked; `KAN allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player                   | cut (failed last game)                                  | more of                                                                                | KAN allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:-------------------------|:--------------------------------------------------------|:---------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Tre Harris               | short_right (75% failed)                                | deep_middle x1.5, short_middle x1.5, short_left x1.5, deep_right x1.5, deep_left x1.5  | x1.01, x0.97, x0.99, x0.99, x0.99 |         0.0 |         9.8 |         0.0 |          0.0 |       62.2 |
| Kimani Vidal             | short_middle (100% failed), short_right (100% failed)   | deep_middle x2.5, short_left x2.5, deep_right x2.5, deep_left x2.5                     | x1.01, x0.99, x0.99, x0.99        |         0.0 |         5.3 |         0.0 |          1.1 |       38.6 |
| Kimani Vidal             | run outside_left (33% failed), run middle (100% failed) | run outside_right x1.5, run inside_left x1.5, run inside_right x1.5                    | x1.01, x0.94, x0.90               |         0.0 |         5.3 |         0.0 |          1.1 |       38.6 |
| Oronde Gadsden II        | deep_right (100% failed)                                | deep_middle x1.1, short_middle x1.1, short_right x1.1, short_left x1.1, deep_left x1.1 | x1.01, x0.97, x0.99, x0.99, x0.99 |         0.0 |        -2.8 |         0.0 |          0.0 |       33.1 |
| Marquez Valdes-Scantling | short_right (100% failed)                               | deep_middle x1.8, short_middle x1.8, short_left x1.8, deep_right x1.8, deep_left x1.8  | x1.01, x0.97, x0.99, x0.99, x0.99 |        -0.0 |         2.7 |         0.0 |          0.0 |       13.1 |
| Keaton Mitchell          | short_right (33% failed)                                | deep_middle x1.2, short_middle x1.2, short_left x1.2, deep_right x1.2, deep_left x1.2  | x1.01, x0.97, x0.99, x0.99, x0.99 |         0.0 |         1.7 |         0.0 |          0.2 |       58.5 |
| Keaton Mitchell          | run outside_left (50% failed)                           | run outside_right x1.1, run middle x1.1, run inside_left x1.1, run inside_right x1.1   | x1.01, x1.05, x0.94, x0.90        |         0.0 |         1.7 |         0.0 |          0.2 |       58.5 |
| Charlie Kolar            | short_middle (50% failed), short_right (50% failed)     | deep_middle x1.6, short_left x1.6, deep_right x1.6, deep_left x1.6                     | x1.01, x0.99, x0.99, x0.99        |         0.0 |         1.1 |         0.0 |          0.0 |       17.0 |

**KAN defensive weak spots:** play-action dropbacks: 8.6 allowed vs league 6.9 (48 plays); vs RBs: 6.6 yds/target (league 5.3), x1.10 for RBs.
- KAN struggle: Wk2 vs IND: +0.15 EPA/play allowed (norm -0.13). Why: deep passes 17.0 yds/play vs 6.6 in other games; RBs 10.0 yds/target vs 5.9 in other games; missing starters: Mansoor Delane (CB); WRs 8.3 yds/target vs 5.6 in other games; when blitzing 8.8 yds/dropback vs 6.7 in other games → counted at 50% weight (those starters are available now)
- KAN struggle: Wk4 vs LVR: +0.03 EPA/play allowed (norm -0.09). Why: when blitzing 10.8 yds/dropback vs 6.0 in other games; TEs 8.7 yds/target vs 5.9 in other games; 8 explosive plays vs 4.0 per other game; short passes 7.2 yds/play vs 5.6 in other games; vs play action 10.2 yds/dropback vs 8.1 in other games
**Offenses like LAC that faced KAN:** MIA (similarity 0.08: +1.3 pass / -1.7 run yds/play vs their norm), IND (similarity 0.06: +1.9 pass / -0.1 run yds/play vs their norm), DEN (similarity 0.03: -2.1 pass / +1.2 run yds/play vs their norm) → LAC pass x1.00, run x0.99.
**KAN defensive scheme (online/tagged):** blitz: avg, coverage: avg, shell: two_high [online (high)].
- Best matchups: run_middle (x1.05), run_outside_right (x1.01); worst: run_inside_right (x0.90).
- KAN blitzes 29% of dropbacks (league 32%, FTN charting); LAC gains x0.91 as much per dropback vs the blitz as other offenses (44 blitzed dropbacks) -> pass yards x1.00
- LAC short plays vs two high shell defenses: x0.94 vs how other offenses fare (116 plays)
- LAC run plays vs two high shell defenses: x1.05 vs how other offenses fare (115 plays)
- KAN vs position groups: Keaton Mitchell x1.10, Ladd McConkey x0.93, Oronde Gadsden II x1.05, Tre Harris x0.93

| player                   | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-------------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Justin Herbert           | QB    |     237.64 |      1.05 |            1.27 |      4.82 |      33.26 |      0.31 |         0.20 |      2.16 |         0.12 |
| Tre Harris               | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      7.70 |         4.39 |     61.29 |         0.17 |
| Keaton Mitchell          | RB    |       0.00 |      0.00 |            0.00 |      6.08 |      24.92 |      4.59 |         3.01 |     31.64 |         0.26 |
| Omarion Hampton          | RB    |       0.00 |      0.00 |            0.00 |     13.05 |      51.28 |      1.75 |         1.13 |     12.64 |         0.37 |
| Oronde Gadsden II        | TE    |       0.00 |      0.00 |            0.00 |      0.18 |       0.68 |      4.69 |         2.98 |     30.90 |         0.15 |
| Kimani Vidal             | RB    |       0.00 |      0.00 |            0.00 |      3.21 |      14.70 |      2.55 |         1.40 |     23.73 |         0.19 |
| Ladd McConkey            | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.94 |         2.35 |     27.97 |         0.14 |
| Charlie Kolar            | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.24 |         1.38 |     16.38 |         0.07 |
| Marquez Valdes-Scantling | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.63 |         1.04 |     12.60 |         0.06 |

**LAC kicker**

| player         |   fg_made |   xp_made |   kicking_points |
|:---------------|----------:|----------:|-----------------:|
| Cameron Dicker |      1.62 |      1.73 |             6.60 |

**LAC defenders (vs KAN offense)**

| player             |   tackles |   sacks |   def_int |
|:-------------------|----------:|--------:|----------:|
| Daiyan Henley      |      5.99 |    0.04 |      0.00 |
| Del'Shawn Phillips |      5.66 |    0.00 |      0.00 |
| Akheem Mesidor     |      4.82 |    0.35 |      0.00 |
| Tuli Tuipulotu     |      4.46 |    0.26 |      0.20 |
| Cam Hart           |      3.97 |    0.00 |      0.14 |
| Tony Jefferson     |      3.77 |    0.00 |      0.00 |
| Elijah Molden      |      3.61 |    0.00 |      0.00 |
| Justin Eboigbe     |      3.40 |    0.08 |      0.00 |

## LVR vs BUF
Projected 68 plays, 63% dropbacks, 40.6 pass att, 25.3 runs, 1.5 sacks. QB: Kirk Cousins
**Coaching style:** Sack rate low: 4% (league 6%); Pass rate on 2nd & short low: 8% (league 31%); Pass rate on 3rd & short high: 53% (league 41%); EPA/dropback high: +0.14 (league +0.06); EPA/run low: -0.23 (league -0.09); Favors run middle (36%).
**Model game script:** projected 27.0 – 31.3 (margin -4.3) → dropback rate +1.7%.
**Strength of schedule:** opp pass D x0.97 (raw stats re-rated against the opponents actually faced).
**Out:** Jalen Nailor (carried from week 5 report: Out (Concussion)), Dont'e Thornton Jr. (carried from week 5 report: Out (Hamstring)), Trey Zuhn III (carried from week 5 report: Out (Knee)).
**Coach angle:** HC Klint Kubiak (first-year HC, 0 prior seasons); calls own plays (developing play-caller, 3 seasons calling); career balanced (-1.0 pts pass rate vs league, 3 seasons); leans on stars; this season top target share 24%.
**BUF secondary:** DC Jim Leonhard, mixed-leaning: Switched from 4-2-5 to aggressive multiple 3-4; pressure from varied angles and five-man rushes on money downs; outside Christian Benford / Maxwell Hairston; nickel Dee Alford; weak spot: Benford / Alford / Hairston all ranked among the worst in coverage by PFF entering week 4; communication busts; [research confidence medium, 2026-10-14].

**What worked last game → this week vs BUF** (failed play types cut, volume moved to what worked; `BUF allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player        | cut (failed last game)                              | more of                                                                                 | BUF allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:--------------|:----------------------------------------------------|:----------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Cody White    | short_left (100% failed), short_right (100% failed) | short_middle x2.7, deep_left x2.7, deep_right x2.7, deep_middle x2.7                    | x0.99, x1.07, x1.02, x0.95        |         0.0 |         7.9 |         0.0 |          0.0 |       34.1 |
| Brock Bowers  | short_left (50% failed), short_right (60% failed)   | short_middle x1.5, deep_left x1.5, deep_right x1.5, deep_middle x1.5                    | x0.99, x1.07, x1.02, x0.95        |         0.0 |         6.7 |         0.0 |          0.0 |       97.1 |
| Tre Tucker    | deep_left (100% failed)                             | short_left x1.2, short_right x1.2, short_middle x1.2, deep_right x1.2, deep_middle x1.2 | x1.02, x1.03, x0.99, x1.02, x0.95 |         0.0 |        -4.6 |         0.0 |          0.2 |       49.9 |
| Tre Tucker    | run inside_right (100% failed)                      | run middle x1.6, run outside_left x1.6, run inside_left x1.6, run outside_right x1.6    | x1.03, x1.07, x0.89, x1.01        |         0.0 |        -4.6 |         0.0 |          0.2 |       49.9 |
| Ashton Jeanty | short_left (100% failed), short_middle (50% failed) | short_right x2.1, deep_left x2.1, deep_right x2.1, deep_middle x2.1                     | x1.03, x1.07, x1.02, x0.95        |         0.0 |         4.0 |         0.0 |          0.5 |      119.5 |
| Ashton Jeanty | run inside_right (20% failed)                       | run middle x1.1, run outside_left x1.1, run inside_left x1.1, run outside_right x1.1    | x1.03, x1.07, x0.89, x1.01        |         0.0 |         4.0 |         0.0 |          0.5 |      119.5 |
| Malik Benson  | short_left (100% failed)                            | short_right x1.5, short_middle x1.5, deep_left x1.5, deep_right x1.5, deep_middle x1.5  | x1.03, x0.99, x1.07, x1.02, x0.95 |         0.0 |         0.8 |         0.0 |          0.0 |        9.3 |
| Dylan Laube   | run outside_right (100% failed)                     | run middle x1.3, run outside_left x1.3, run inside_left x1.3, run inside_right x1.3     | x1.03, x1.07, x0.89, x0.95        |         0.0 |         0.0 |         0.0 |         -0.1 |        4.6 |

**BUF defensive weak spots:** red-zone TDs per play: 26% allowed vs league 21% (61 plays); 3rd-down conversions: 49% allowed vs league 42% (76 plays); explosive plays: 10% allowed vs league 9% (328 plays); short passes: 6.7 allowed vs league 6.0 (155 plays).
- BUF struggle: Wk2 vs DET: +0.23 EPA/play allowed (norm +0.11). Why: RBs 8.2 yds/target vs 4.9 in other games; deep passes 13.5 yds/play vs 8.7 in other games; DET is a strong offense (+0.16 EPA/play in its other games)
- BUF struggle: Wk5 vs LAR: +0.25 EPA/play allowed (norm +0.10). Why: TEs 11.0 yds/target vs 6.6 in other games; vs play action 8.7 yds/dropback vs 5.6 in other games
**Offenses like LVR that faced BUF:** DET (similarity 0.30: -0.1 pass / -1.3 run yds/play vs their norm), LAR (similarity 0.23: -0.6 pass / -1.7 run yds/play vs their norm), HOU (similarity 0.19: -0.7 pass / +0.7 run yds/play vs their norm) → LVR pass x0.99, run x0.98.
**BUF defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: two_high [online (high)].
- BUF brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed +0.14 on 11 attempts. LVR 3rd-down deep share 18%.
- Best matchups: pass_deep_left (x1.07), run_outside_left (x1.07); worst: run_inside_left (x0.89).
- BUF blitzes 34% of dropbacks (league 32%, FTN charting); LVR gains x1.16 as much per dropback vs the blitz as other offenses (48 blitzed dropbacks) -> pass yards x1.00
- LVR deep plays vs zone heavy coverage defenses: x1.07 vs how other offenses fare (7 plays)
- LVR deep-throw rate vs zone heavy coverage: x0.82
- LVR deep-throw rate vs two high shell: x1.12

| player              | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:--------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Kirk Cousins        | QB    |     312.60 |      2.58 |            0.58 |      0.76 |       5.18 |      0.00 |         0.00 |      0.00 |         0.03 |
| Ashton Jeanty       | RB    |       0.00 |      0.00 |            0.00 |     17.64 |      61.71 |      7.41 |         5.16 |     56.12 |         0.56 |
| Brock Bowers        | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |     10.89 |         7.14 |     94.63 |         0.56 |
| Michael Mayer       | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.49 |         4.76 |     46.88 |         0.30 |
| Tre Tucker          | WR    |       0.00 |      0.00 |            0.00 |      0.55 |       2.06 |      6.32 |         4.45 |     46.36 |         0.29 |
| Cody White          | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.66 |         2.07 |     33.77 |         0.29 |
| Mike Washington Jr. | RB    |       0.00 |      0.00 |            0.00 |      5.49 |      20.69 |      1.25 |         0.85 |      8.46 |         0.24 |

**LVR kicker**

| player   |   fg_made |   xp_made |   kicking_points |
|:---------|----------:|----------:|-----------------:|
| Matt Gay |      1.84 |      3.07 |             8.58 |

**LVR defenders (vs BUF offense)**

| player          |   tackles |   sacks |   def_int |
|:----------------|----------:|--------:|----------:|
| Nakobe Dean     |      9.69 |    0.18 |      0.00 |
| Quay Walker     |      6.78 |    0.20 |      0.00 |
| Jeremy Chinn    |      6.26 |    0.17 |      0.00 |
| Taron Johnson   |      4.81 |    0.00 |      0.00 |
| Hezekiah Masses |      4.11 |    0.00 |      0.55 |
| Treydan Stukes  |      3.48 |    0.00 |      0.15 |
| Eric Stokes     |      3.47 |    0.14 |      0.00 |
| Adam Butler     |      2.76 |    0.10 |      0.00 |

## BUF vs LVR
Projected 59 plays, 55% dropbacks, 27.2 pass att, 26.5 runs, 2.0 sacks. QB: Josh Allen
**Coaching style:** Deep-pass share high: 24% (league 19%); 3rd-down deep share high: 25% (league 21%); Shotgun rate low: 46% (league 61%); Pass rate on 3rd & short low: 11% (league 41%); 3rd-down conversion high: 54% (league 42%); EPA/dropback high: +0.35 (league +0.06); EPA/run high: +0.03 (league -0.09); Favors run middle (34%).
**Model game script:** projected 31.3 – 27.0 (margin +4.3) → dropback rate -1.7%.
**Strength of schedule:** own pass yds x1.03, opp scoring D x1.03 (raw stats re-rated against the opponents actually faced).
**Out:** Ed Oliver (carried from week 5 report: Out (Knee)), Josh Palmer (carried from week 5 report: Out (Shoulder)).
**Coach angle:** HC Joe Brady (first-year HC, 0 prior seasons); calls own plays (developing play-caller, 4 seasons calling); career balanced (-1.9 pts pass rate vs league, 4 seasons); typical; this season top target share 20%.
**LVR secondary:** DC Rob Leonard, mixed-leaning: Macdonald-style multiple and aggressive defense; outside Eric Stokes / Hezekiah Masses; nickel Taron Johnson; weak spot: Young corner room; [research confidence medium, 2026-10-14].

**What worked last game → this week vs LVR** (failed play types cut, volume moved to what worked; `LVR allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player         | cut (failed last game)                                   | more of                                                                                | LVR allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:---------------|:---------------------------------------------------------|:---------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| James Cook     | run middle (40% failed), run outside_right (100% failed) | run inside_left x1.2, run inside_right x1.2, run outside_left x1.2                     | x1.06, x1.32, x1.14               |         0.0 |         0.0 |         0.0 |          2.3 |      135.4 |
| Dalton Kincaid | deep_right (100% failed)                                 | short_right x1.1, short_left x1.1, deep_middle x1.1, deep_left x1.1, short_middle x1.1 | x1.24, x1.04, x0.99, x1.14, x1.07 |         0.0 |        -1.5 |         0.0 |          0.0 |       38.3 |
| Keon Coleman   | deep_right (100% failed)                                 | short_right x1.1, short_left x1.1, deep_middle x1.1, deep_left x1.1, short_middle x1.1 | x1.24, x1.04, x0.99, x1.14, x1.07 |         0.0 |        -1.4 |         0.0 |          0.0 |       41.0 |
| Skyler Bell    | short_right (100% failed), deep_left (100% failed)       | short_left x3.4, deep_middle x3.4, deep_right x3.4, short_middle x3.4                  | x1.04, x0.99, x1.02, x1.07        |         0.0 |         0.9 |         0.0 |          0.0 |        6.3 |
| Dawson Knox    | short_left (100% failed), deep_middle (100% failed)      | short_right x1.9, deep_left x1.9, deep_right x1.9, short_middle x1.9                   | x1.24, x1.14, x1.02, x1.07        |        -0.0 |        -0.8 |         0.0 |          0.0 |       19.4 |
| Ray Davis      | run outside_left (100% failed)                           | run inside_left x1.1, run middle x1.1, run inside_right x1.1, run outside_right x1.1   | x1.06, x1.06, x1.32, x1.14        |         0.0 |         0.0 |         0.0 |         -0.1 |       10.6 |

**LVR defensive weak spots:** red-zone TDs per play: 31% allowed vs league 21% (42 plays); explosive plays: 11% allowed vs league 9% (268 plays); outside runs: 6.5 allowed vs league 4.9 (23 plays); inside runs: 4.5 allowed vs league 3.9 (91 plays).
- LVR struggle: Wk4 vs KAN: +0.15 EPA/play allowed (norm -0.02). Why: outside runs 10.6 yds/play vs 5.4 in other games; inside runs 7.2 yds/play vs 3.8 in other games; deep passes 17.2 yds/play vs 12.1 in other games; KAN is a strong offense (+0.19 EPA/play in its other games)
- LVR struggle: Wk5 vs NWE: +0.49 EPA/play allowed (norm -0.10). Why: when blitzing 14.0 yds/dropback vs 6.2 in other games; WRs 16.1 yds/target vs 8.2 in other games; TEs 11.8 yds/target vs 6.1 in other games; vs play action 11.8 yds/dropback vs 6.2 in other games; deep passes 20.2 yds/play vs 11.1 in other games
**Offenses like BUF that faced LVR:** NWE (similarity 0.52: +5.0 pass / +1.8 run yds/play vs their norm), MIA (similarity 0.17: +1.3 pass / -2.1 run yds/play vs their norm), KAN (similarity 0.04: -1.5 pass / +2.6 run yds/play vs their norm) → BUF pass x1.08, run x1.01.
**LVR defensive scheme (online/tagged):** blitz: avg, coverage: avg, shell: two_high [online (high)].
- LVR is soft deep (+0.58 EPA/deep att vs league +0.43); BUF throws deep 24%.
- Best matchups: run_inside_right (x1.32), pass_short_right (x1.24); worst: pass_deep_middle (x0.99).
- Last game — worked: run_inside_left, run_inside_right; failed: none.
- LVR blitzes 26% of dropbacks (league 32%, FTN charting); BUF gains x1.06 as much per dropback vs the blitz as other offenses (53 blitzed dropbacks) -> pass yards x1.00
- BUF deep plays vs two high shell defenses: x0.95 vs how other offenses fare (23 plays)
- BUF run plays vs two high shell defenses: x1.07 vs how other offenses fare (107 plays)

| player         | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:---------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Josh Allen     | QB    |     238.21 |      1.69 |            0.70 |      8.08 |      50.36 |      0.17 |         0.12 |      1.60 |         0.59 |
| James Cook     | RB    |       0.00 |      0.00 |            0.00 |     20.27 |     117.30 |      2.13 |         1.43 |     16.95 |         0.76 |
| Khalil Shakir  | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.70 |         3.90 |     55.10 |         0.26 |
| Keon Coleman   | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.86 |         2.59 |     37.45 |         0.29 |
| DJ Moore       | WR    |       0.00 |      0.00 |            0.00 |      0.30 |       1.62 |      3.81 |         2.41 |     35.95 |         0.25 |
| Dalton Kincaid | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.72 |         2.50 |     36.29 |         0.22 |
| Ty Johnson     | RB    |       0.00 |      0.00 |            0.00 |      0.26 |       1.30 |      2.56 |         1.86 |     25.09 |         0.16 |
| Dawson Knox    | TE    |       0.00 |      0.00 |            0.00 |      0.23 |       1.09 |      2.04 |         1.41 |     16.85 |         0.16 |

**BUF kicker**

| player     |   fg_made |   xp_made |   kicking_points |
|:-----------|----------:|----------:|-----------------:|
| Tyler Bass |      1.21 |      3.66 |             7.28 |

**BUF defenders (vs LVR offense)**

| player               |   tackles |   sacks |   def_int |
|:---------------------|----------:|--------:|----------:|
| Dorian Williams      |      7.89 |    0.00 |      0.00 |
| Cole Bishop          |      7.19 |    0.00 |      0.00 |
| Terrel Bernard       |      6.64 |    0.00 |      0.00 |
| Davison Igbinosun    |      5.11 |    0.00 |      0.00 |
| Christian Benford    |      5.08 |    0.00 |      0.00 |
| C.J. Gardner-Johnson |      4.84 |    0.00 |      0.27 |
| Greg Rousseau        |      3.59 |    0.72 |      0.00 |
| Bradley Chubb        |      3.11 |    0.19 |      0.00 |

## GNB vs DAL
Projected 58 plays, 60% dropbacks, 33.5 pass att, 23.1 runs, 1.4 sacks. QB: Jordan Love
**Coaching style:** 3rd-down conversion low: 33% (league 42%); EPA/dropback high: +0.13 (league +0.06); EPA/run low: -0.25 (league -0.09); Favors run inside left (32%).
**Market team total:** implied 27.5 (this team landed within the tolerance in 60% of its games, avg miss 5.3). Model 30.5 → blended 28.7: TD rates x0.94, yards x0.98.
**Model game script:** projected 30.5 – 27.1 (margin +3.4) → dropback rate -1.4%.
**Weather:** forecast 54°F, wind 9 mph → pass yds x1.00, long FG x1.00.
**Offensive line:** starters out: Jacob Monk → sack rate x1.00, yds/dropback x0.99, yds/carry x1.01 (measured effect per missing starter).
**Strength of schedule:** own scoring x1.06 (raw stats re-rated against the opponents actually faced).
**Out:** Aaron Banks (carried from week 5 report: Doubtful (Knee)), Chris Brooks (carried from week 5 report: Out (Ankle)), Jacob Monk (carried from week 5 report: Doubtful (Quadricep)), Savion Williams (carried from week 5 report: Out (Ankle)).
**Coach angle:** HC Matt LaFleur (veteran HC, 7 prior seasons); calls own plays (veteran play-caller, 8 seasons calling); career balanced (-1.7 pts pass rate vs league, 8 seasons); typical; this season top target share 23%.
**DAL secondary:** DC Christian Parker, mixed-leaning: Multiple 3-4 with 4-2-5 nickel; will play man if the corners allow; analysts expect more zone; outside Joey Porter Jr. / DaRon Bland; nickel Caleb Downs; weak spot: Depleted corner room; Joey Porter Jr. added Oct 1; [research confidence low, 2026-10-14].

**What worked last game → this week vs DAL** (failed play types cut, volume moved to what worked; `DAL allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player         | cut (failed last game)                                 | more of                                                                                | DAL allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:---------------|:-------------------------------------------------------|:---------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| MarShawn Lloyd | run inside_left (50% failed), run middle (100% failed) | run outside_left x1.7, run inside_right x1.7, run outside_right x1.7                   | x1.13, x1.18, x1.05               |         0.0 |        -0.1 |         0.0 |          6.0 |       80.0 |
| MarShawn Lloyd | short_middle (50% failed)                              | deep_middle x1.1, deep_right x1.1, short_right x1.1, short_left x1.1, deep_left x1.1   | x1.08, x1.05, x1.06, x1.03, x1.04 |         0.0 |        -0.1 |         0.0 |          6.0 |       80.0 |
| Tucker Kraft   | short_right (50% failed)                               | short_middle x1.2, deep_middle x1.2, deep_right x1.2, short_left x1.2, deep_left x1.2  | x1.09, x1.08, x1.05, x1.03, x1.04 |         0.0 |         4.7 |         0.0 |         -0.0 |       60.4 |
| Skyy Moore     | short_right (100% failed)                              | short_middle x1.6, deep_middle x1.6, deep_right x1.6, short_left x1.6, deep_left x1.6  | x1.09, x1.08, x1.05, x1.03, x1.04 |         0.0 |         4.3 |         0.0 |          0.0 |       22.7 |
| Matthew Golden | deep_right (50% failed)                                | short_middle x1.1, deep_middle x1.1, short_right x1.1, short_left x1.1, deep_left x1.1 | x1.09, x1.08, x1.06, x1.03, x1.04 |         0.0 |        -3.5 |         0.0 |          0.0 |       68.6 |
| Bo Melton      | short_middle (100% failed), short_right (100% failed)  | deep_middle x1.9, deep_right x1.9, short_left x1.9, deep_left x1.9                     | x1.08, x1.05, x1.03, x1.04        |         0.0 |         2.2 |         0.0 |          0.0 |       14.5 |
| Pierre Strong  | short_right (33% failed), short_left (100% failed)     | short_middle x1.8, deep_middle x1.8, deep_right x1.8, short_right x1.2, deep_left x1.8 | x1.09, x1.08, x1.05, x1.06, x1.04 |         0.0 |         0.9 |        -0.0 |          0.0 |       15.4 |
| Pierre Strong  | run inside_right (33% failed)                          | run inside_left x1.2, run outside_left x1.2, run middle x1.2, run outside_right x1.2   | x1.06, x1.13, x0.99, x1.05        |         0.0 |         0.9 |        -0.0 |          0.0 |       15.4 |

**DAL defensive weak spots:** explosive plays: 12% allowed vs league 9% (280 plays); outside runs: 6.6 allowed vs league 4.9 (33 plays); 3rd-down conversions: 52% allowed vs league 42% (58 plays); inside runs: 4.5 allowed vs league 3.9 (109 plays); red-zone TDs per play: 25% allowed vs league 21% (60 plays).
- DAL struggle: Wk1 vs NYG: +0.37 EPA/play allowed (norm +0.15). Why: 3rd/4th downs converted 90% vs 44%; short passes 8.2 yds/play vs 6.6 in other games; red-zone TD rate per play 33% vs 23%
**Offenses like GNB that faced DAL:** TAM (similarity 0.12: +1.4 pass / +3.0 run yds/play vs their norm), NYG (similarity 0.10: +2.1 pass / +1.8 run yds/play vs their norm), WAS (similarity 0.10: +0.8 pass / +0.6 run yds/play vs their norm) → GNB pass x1.00, run x1.01.
**DAL defensive scheme (online/tagged):** blitz: avg, coverage: avg [online (high)].
- DAL is soft deep (+0.83 EPA/deep att vs league +0.43); GNB throws deep 22%.
- Best matchups: run_inside_right (x1.18), run_outside_left (x1.13); worst: run_middle (x0.99).
- DAL blitzes 27% of dropbacks (league 32%, FTN charting); GNB gains x1.13 as much per dropback vs the blitz as other offenses (74 blitzed dropbacks) -> pass yards x0.99
- DAL DBs out: Cobie Durant (5 tgts, 7.2 yds/tgt allowed) -> coverage 8.2 → 8.3 yds/tgt; WR yards x1.01
- DAL vs position groups: MarShawn Lloyd x0.91

| player           | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-----------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Jordan Love      | QB    |     281.46 |      2.46 |            0.24 |      0.79 |       4.29 |      0.00 |         0.00 |      0.00 |         0.03 |
| Christian Watson | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      7.64 |         4.85 |     68.00 |         0.61 |
| MarShawn Lloyd   | RB    |       0.00 |      0.00 |            0.00 |     13.35 |      58.81 |      3.27 |         2.33 |     21.56 |         0.61 |
| Matthew Golden   | WR    |       0.00 |      0.00 |            0.00 |      0.27 |       1.25 |      8.04 |         5.29 |     67.65 |         0.36 |
| Tucker Kraft     | TE    |       0.00 |      0.00 |            0.00 |      0.75 |       2.71 |      6.38 |         4.41 |     57.03 |         0.35 |
| Kaleb Johnson    | RB    |       0.00 |      0.00 |            0.00 |      6.76 |      28.47 |      0.71 |         0.46 |      4.20 |         0.26 |
| Skyy Moore       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      2.58 |         1.72 |     22.93 |         0.13 |
| Pierre Strong    | RB    |       0.00 |      0.00 |            0.00 |      1.50 |       6.28 |      1.32 |         0.86 |      9.03 |         0.14 |
| Bo Melton        | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.51 |         1.02 |     13.96 |         0.09 |

**GNB kicker**

| player     |   fg_made |   xp_made |   kicking_points |
|:-----------|----------:|----------:|-----------------:|
| Trey Smack |      1.49 |      3.23 |             7.71 |

**GNB defenders (vs DAL offense)**

| player          |   tackles |   sacks |   def_int |
|:----------------|----------:|--------:|----------:|
| Evan Williams   |      9.97 |    0.11 |      0.19 |
| Zaire Franklin  |      8.34 |    0.00 |      0.00 |
| Javon Bullard   |      6.67 |    0.00 |      0.00 |
| Keisean Nixon   |      6.58 |    0.03 |      0.11 |
| Edgerrin Cooper |      5.85 |    0.24 |      0.19 |
| Lukas Van Ness  |      4.68 |    0.18 |      0.00 |
| Brandon Cisse   |      4.50 |    0.17 |      0.00 |
| Isaiah McDuffie |      4.01 |    0.00 |      0.00 |

## DAL vs GNB
Projected 64 plays, 65% dropbacks, 38.5 pass att, 22.5 runs, 1.3 sacks. QB: Dak Prescott
**Coaching style:** Neutral-script pass rate high: 68% (league 59%); Early-down pass rate high: 61% (league 53%); 3rd-down deep share low: 13% (league 21%); Sack rate low: 3% (league 6%); No-huddle rate high: 11% (league 6%); Pass rate on 3rd & short high: 60% (league 41%); EPA/dropback high: +0.16 (league +0.06); EPA/run high: -0.01 (league -0.09); Favors run middle (38%).
**Model game script:** projected 27.1 – 30.5 (margin -3.4) → dropback rate +1.4%.
**Weather:** forecast 54°F, wind 9 mph → pass yds x1.00, long FG x1.00.
**Strength of schedule:** own run yds x1.02, opp run D x0.97, opp scoring D x1.02 (raw stats re-rated against the opponents actually faced).
**Out:** Cobie Durant (carried from week 5 report: Out (Hamstring)), DeMarvion Overshown (carried from week 5 report: Out (Hamstring)), Drew Shelton (carried from week 5 report: Out (Hamstring)).
**Coach angle:** HC Brian Schottenheimer (young HC, 1 prior seasons); calls own plays (developing play-caller, 4 seasons calling); career run-first (-2.5 pts pass rate vs league, 4 seasons); typical; this season top target share 27%.
**GNB secondary:** DC Jonathan Gannon, coverage lean unknown: New DC Gannon; aggressive style per players; outside Keisean Nixon / Brandon Cisse; nickel Javon Bullard; weak spot: Right corner spot unsettled (Cisse / Valentine / St-Juste); Nixon coverage grade 50.4; [research confidence low, 2026-10-14].

**What worked last game → this week vs GNB** (failed play types cut, volume moved to what worked; `GNB allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player            | cut (failed last game)                                                                | more of                                                                                 | GNB allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:------------------|:--------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Javonte Williams  | short_middle (50% failed)                                                             | deep_left x1.1, short_right x1.1, deep_right x1.1, short_left x1.1, deep_middle x1.1    | x1.15, x0.99, x1.07, x0.91, x1.06 |         0.0 |         0.5 |         0.0 |          7.7 |      109.9 |
| Javonte Williams  | run inside_left (25% failed), run inside_right (100% failed), run middle (14% failed) | run inside_left x1.2, run outside_left x1.6, run middle x1.4, run outside_right x1.6    | x0.92, x1.19, x0.96, x1.09        |         0.0 |         0.5 |         0.0 |          7.7 |      109.9 |
| George Pickens    | deep_left (67% failed), short_right (100% failed), short_left (12% failed)            | deep_right x1.8, short_left x1.5, short_middle x1.8, deep_middle x1.8                   | x1.07, x0.91, x0.89, x1.06        |         0.0 |         7.1 |         0.0 |          0.0 |       70.3 |
| Jake Ferguson     | short_right (50% failed), short_left (33% failed), short_middle (100% failed)         | deep_left x2.1, deep_right x2.1, short_left x1.4, deep_middle x2.1                      | x1.15, x1.07, x0.91, x1.06        |         0.0 |         4.1 |         0.0 |          0.0 |       29.6 |
| Ryan Flournoy     | short_middle (100% failed)                                                            | deep_left x1.2, short_right x1.2, deep_right x1.2, short_left x1.2, deep_middle x1.2    | x1.15, x0.99, x1.07, x0.91, x1.06 |         0.0 |         1.6 |         0.0 |          0.0 |       39.3 |
| Brevyn Spann-Ford | short_left (100% failed), short_middle (100% failed)                                  | deep_left x2.3, short_right x2.3, deep_right x2.3, deep_middle x2.3                     | x1.15, x0.99, x1.07, x1.06        |         0.0 |         1.5 |         0.0 |          0.0 |        9.2 |
| CeeDee Lamb       | deep_right (100% failed), short_left (50% failed)                                     | deep_left x1.3, short_right x1.3, short_middle x1.3, deep_middle x1.3                   | x1.15, x0.99, x0.89, x1.06        |         0.0 |        -1.3 |         0.0 |          0.0 |       73.2 |
| Jonathan Mingo    | deep_left (100% failed)                                                               | short_right x1.2, deep_right x1.2, short_left x1.2, short_middle x1.2, deep_middle x1.2 | x0.99, x1.07, x0.91, x0.89, x1.06 |         0.0 |        -1.1 |         0.0 |          0.0 |       10.1 |

**GNB defensive weak spots:** outside runs: 7.3 allowed vs league 4.9 (37 plays); vs RBs: 8.9 yds/target (league 5.3), x1.17 for RBs; red-zone TDs per play: 27% allowed vs league 21% (49 plays); 3rd-down conversions: 48% allowed vs league 42% (71 plays).
- GNB struggle: Wk3 vs ATL: +0.32 EPA/play allowed (norm -0.10). Why: deep passes 24.8 yds/play vs 6.4 in other games; when blitzing 13.1 yds/dropback vs 3.9 in other games; outside runs 13.5 yds/play vs 4.7 in other games; WRs 13.0 yds/target vs 5.7 in other games; vs play action 7.1 yds/dropback vs 4.3 in other games
**Offenses like DAL that faced GNB:** NYJ (similarity 0.13: -1.3 pass / -1.8 run yds/play vs their norm), TAM (similarity 0.06: -0.5 pass / -0.7 run yds/play vs their norm), MIN (similarity 0.03: -0.9 pass / -0.3 run yds/play vs their norm) → DAL pass x0.99, run x0.98.
**GNB defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy, shell: two_high [online (high)].
- GNB run defense is soft (+0.01 EPA/run).
- Best matchups: run_outside_left (x1.19), pass_deep_left (x1.15); worst: pass_short_middle (x0.89).
- Last game — worked: none; failed: pass_short_middle, pass_deep_left.
- GNB blitzes 38% of dropbacks (league 32%, FTN charting); DAL gains x0.92 as much per dropback vs the blitz as other offenses (68 blitzed dropbacks) -> pass yards x0.99
- DAL deep plays vs zone heavy coverage defenses: x1.16 vs how other offenses fare (14 plays)
- DAL short plays vs zone heavy coverage defenses: x0.94 vs how other offenses fare (117 plays)
- DAL deep-throw rate vs zone heavy coverage: x0.84
- DAL run plays vs two high shell defenses: x1.06 vs how other offenses fare (60 plays)
- GNB vs position groups: Javonte Williams x1.17, Jake Ferguson x0.92

| player           | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-----------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Dak Prescott     | QB    |     270.41 |      1.63 |            1.34 |      2.18 |      16.25 |      0.00 |         0.00 |      0.00 |         0.09 |
| Javonte Williams | RB    |       0.00 |      0.00 |            0.00 |     18.38 |      80.44 |      3.89 |         2.89 |     28.57 |         0.80 |
| CeeDee Lamb      | WR    |       0.00 |      0.00 |            0.00 |      0.36 |       1.55 |      9.54 |         6.79 |     68.53 |         0.41 |
| George Pickens   | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      8.45 |         5.78 |     68.81 |         0.26 |
| Ryan Flournoy    | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      5.47 |         3.71 |     38.30 |         0.15 |
| Jake Ferguson    | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      4.37 |         3.02 |     28.08 |         0.24 |
| KaVontae Turpin  | WR    |       0.00 |      0.00 |            0.00 |      0.36 |       1.62 |      1.68 |         1.18 |     10.82 |         0.09 |
| Jonathan Mingo   | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      1.65 |         1.17 |     10.06 |         0.06 |
| Tyler Goodson    | RB    |       0.00 |      0.00 |            0.00 |      2.46 |       9.85 |      0.43 |         0.28 |      3.08 |         0.13 |

**DAL kicker**

| player         |   fg_made |   xp_made |   kicking_points |
|:---------------|----------:|----------:|-----------------:|
| Brandon Aubrey |      1.25 |      3.16 |             6.91 |

**DAL defenders (vs GNB offense)**

| player            |   tackles |   sacks |   def_int |
|:------------------|----------:|--------:|----------:|
| Dee Winters       |      6.50 |    0.00 |      0.00 |
| Caleb Downs       |      5.21 |    0.18 |      0.00 |
| Jaishawn Barham   |      4.89 |    0.00 |      0.00 |
| Donovan Ezeiruaku |      4.36 |    0.10 |      0.00 |
| DaRon Bland       |      3.72 |    0.00 |      0.00 |
| Markquese Bell    |      3.33 |    0.00 |      0.00 |
| Otito Ogbonnia    |      3.19 |    0.00 |      0.00 |
| Malik Hooker      |      2.79 |    0.00 |      0.00 |

## SFO vs WAS
Projected 59 plays, 57% dropbacks, 30.4 pass att, 25.5 runs, 0.7 sacks. QB: Brock Purdy
**Coaching style:** 4th-down go rate low: 8% (league 19%); Sack rate low: 3% (league 6%); Shotgun rate low: 48% (league 61%); No-huddle rate low: 0% (league 6%); 3rd-down conversion high: 50% (league 42%); EPA/dropback high: +0.38 (league +0.06); Favors run middle (37%).
**Model game script:** projected 30.1 – 21.6 (margin +8.5) → dropback rate -3.4%.
**Weather:** forecast 59°F, wind 13 mph → pass yds x0.98, long FG x1.00.
**Strength of schedule:** own pass yds x1.03, opp pass D x1.04, opp run D x1.02 (raw stats re-rated against the opponents actually faced).
**Out:** Kyle Juszczyk (carried from week 5 report: Out (Knee)), Nick Bosa (carried from week 5 report: Out (Knee)), Marques Sigle (carried from week 5 report: Out (Ankle)), James Thompson Jr. (carried from week 5 report: Out (Ankle)).
**Coach angle:** HC Kyle Shanahan (veteran HC, 9 prior seasons); calls own plays (veteran play-caller, 11 seasons calling); career balanced (-1.3 pts pass rate vs league, 11 seasons); typical; this season top target share 27%.
**WAS secondary:** DC Daronte Jones, mixed-leaning: Flores-style: disguised pressure (35-40% blitz) with heavy Cover 2 and Cover 0; interchangeable DBs; outside Rasul Douglas / Fabian Moreau; nickel Amik Robertson; weak spot: Sainristil allowed 15 TDs in coverage over two seasons; [research confidence medium, 2026-10-14].

**What worked last game → this week vs WAS** (failed play types cut, volume moved to what worked; `WAS allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player           | cut (failed last game)                                                                  | more of                                                                                | WAS allows there                  |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:-----------------|:----------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------|:----------------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Kaelon Black     | run middle (100% failed), run inside_left (33% failed), run outside_right (100% failed) | run inside_left x1.4, run inside_right x2.1, run outside_left x2.1                     | x1.12, x1.10, x1.03               |        -0.0 |        -0.0 |        -0.0 |          3.1 |       37.9 |
| George Kittle    | short_right (50% failed), deep_left (100% failed)                                       | short_left x1.2, deep_right x1.2, short_middle x1.2, deep_middle x1.2                  | x0.92, x1.06, x1.09, x1.03        |         0.0 |         2.8 |         0.0 |          0.0 |       75.5 |
| Mike Evans       | deep_right (67% failed), deep_left (100% failed)                                        | short_left x1.2, short_right x1.2, short_middle x1.2, deep_middle x1.2                 | x0.92, x1.02, x1.09, x1.03        |        -0.0 |        -2.3 |         0.0 |          0.0 |       75.5 |
| Luke Farrell     | short_left (100% failed)                                                                | short_right x2.4, deep_right x2.4, short_middle x2.4, deep_middle x2.4, deep_left x2.4 | x1.02, x1.06, x1.09, x1.03, x1.01 |         0.0 |         2.3 |         0.0 |          0.0 |       10.5 |
| Jacob Cowing     | short_left (100% failed)                                                                | short_right x2.0, deep_right x2.0, short_middle x2.0, deep_middle x2.0, deep_left x2.0 | x1.02, x1.06, x1.09, x1.03, x1.01 |        -0.0 |         2.1 |         0.0 |          0.0 |       13.5 |
| Deebo Samuel Sr. | short_middle (100% failed)                                                              | short_left x1.2, short_right x1.2, deep_right x1.2, deep_middle x1.2, deep_left x1.2   | x0.92, x1.02, x1.06, x1.03, x1.01 |        -0.0 |         0.1 |         0.0 |         -0.5 |       43.8 |
| Deebo Samuel Sr. | run outside_left (100% failed)                                                          | run middle x1.3, run inside_left x1.3, run outside_right x1.3, run inside_right x1.3   | x1.04, x1.12, x1.08, x1.10        |        -0.0 |         0.1 |         0.0 |         -0.5 |       43.8 |
| Brandin Cooks    | short_middle (100% failed)                                                              | short_left x1.4, short_right x1.4, deep_right x1.4, deep_middle x1.4, deep_left x1.4   | x0.92, x1.02, x1.06, x1.03, x1.01 |         0.0 |        -0.1 |         0.0 |          0.0 |        7.0 |

**WAS defensive weak spots:** red-zone TDs per play: 33% allowed vs league 21% (46 plays); vs TEs: 9.1 yds/target (league 7.2), x1.10 for TEs.
- WAS struggle: Wk2 vs DAL: +0.23 EPA/play allowed (norm +0.00). Why: deep passes 24.0 yds/play vs 11.2 in other games; WRs 9.4 yds/target vs 7.0 in other games; 3rd/4th downs converted 64% vs 42%; DAL is a strong offense (+0.11 EPA/play in its other games)
**Offenses like SFO that faced WAS:** IND (similarity 0.11: -1.8 pass / +1.0 run yds/play vs their norm), SEA (similarity 0.05: +1.9 pass / -1.7 run yds/play vs their norm), PHI (similarity 0.02: +2.1 pass / +1.9 run yds/play vs their norm) → SFO pass x0.99, run x1.01.
**WAS defensive scheme (online/tagged):** blitz: heavy, coverage: zone_heavy, shell: two_high [online (high)].
- WAS is soft deep (+0.68 EPA/deep att vs league +0.43); SFO throws deep 19%.
- WAS brings heavy 3rd-down pressure (source: blitz_pct); 3rd-down deep EPA allowed +0.50 on 7 attempts. SFO 3rd-down deep share 23%.
- Best matchups: run_inside_left (x1.12), run_inside_right (x1.10); worst: pass_short_left (x0.92).
- Last game — worked: none; failed: pass_deep_right.
- WAS blitzes 46% of dropbacks (league 32%, FTN charting); SFO gains x1.30 as much per dropback vs the blitz as other offenses (46 blitzed dropbacks) -> pass yards x1.04
- SFO deep plays vs zone heavy coverage defenses: x0.95 vs how other offenses fare (12 plays)
- SFO run plays vs zone heavy coverage defenses: x1.05 vs how other offenses fare (41 plays)
- SFO deep-throw rate vs zone heavy coverage: x1.13
- SFO short plays vs two high shell defenses: x0.92 vs how other offenses fare (103 plays)
- WAS DBs out: Nick Cross (6 tgts, 8.1 yds/tgt allowed) -> coverage 7.8 → 7.8 yds/tgt; WR yards x1.00
- WAS vs position groups: Mike Evans x0.95, George Kittle x1.10, Deebo Samuel Sr. x0.95

| player              | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:--------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Brock Purdy         | QB    |     258.75 |      2.54 |            0.48 |      4.38 |      27.29 |      0.00 |         0.00 |      0.00 |         0.16 |
| Christian McCaffrey | RB    |       0.00 |      0.00 |            0.00 |     14.13 |      64.80 |      5.40 |         3.59 |     39.53 |         0.64 |
| Mike Evans          | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      8.03 |         5.55 |     73.64 |         0.55 |
| George Kittle       | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      7.20 |         4.89 |     73.58 |         0.54 |
| Deebo Samuel Sr.    | WR    |       0.00 |      0.00 |            0.00 |      2.12 |       9.29 |      4.50 |         3.03 |     33.71 |         0.36 |
| Kaelon Black        | RB    |       0.00 |      0.00 |            0.00 |      7.35 |      34.25 |      0.42 |         0.26 |      3.29 |         0.19 |

**SFO kicker**

| player       |   fg_made |   xp_made |   kicking_points |
|:-------------|----------:|----------:|-----------------:|
| Eddy Pineiro |      1.50 |      3.41 |             7.91 |

**SFO defenders (vs WAS offense)**

| player            |   tackles |   sacks |   def_int |
|:------------------|----------:|--------:|----------:|
| Fred Warner       |     10.30 |    0.09 |      0.00 |
| Dre Greenlaw      |      7.52 |    0.00 |      0.00 |
| Ji'Ayir Brown     |      6.95 |    0.00 |      0.00 |
| Marques Sigle     |      4.72 |    0.18 |      0.00 |
| Renardo Green     |      4.37 |    0.00 |      0.49 |
| Deommodore Lenoir |      4.06 |    0.00 |      0.00 |
| Jaden Dugger      |      3.80 |    0.30 |      0.00 |
| Malik Mustapha    |      3.65 |    0.00 |      0.00 |

## WAS vs SFO
Projected 64 plays, 65% dropbacks, 34.1 pass att, 22.5 runs, 2.6 sacks. QB: Jayden Daniels
**Coaching style:** Deep-pass share high: 23% (league 19%); Shotgun rate high: 71% (league 61%); Pass rate on 3rd & short high: 54% (league 41%); 3rd-down conversion low: 32% (league 42%); EPA/run low: -0.15 (league -0.09); Favors run inside right (30%).
**Model game script:** projected 21.6 – 30.1 (margin -8.5) → dropback rate +3.4%.
**Weather:** forecast 59°F, wind 13 mph → pass yds x0.98, long FG x1.00.
**Strength of schedule:** own run yds x0.97, opp pass D x1.03, opp scoring D x1.02 (raw stats re-rated against the opponents actually faced).
**Out:** Stefon Diggs (carried from week 5 report: Out (Hamstring)), Marcus Mariota (carried from week 5 report: Out (Knee)), Charles Omenihu (carried from week 5 report: Out (Groin)), Nick Cross (carried from week 5 report: Out (Illness)), Percy Butler (carried from week 5 report: Out (Hamstring)), Tyler Owens (carried from week 5 report: Out (Hamstring)).
**Coach angle:** HC Dan Quinn (veteran HC, 11 prior seasons); plays called by OC David Blough (first-time play-caller, 0 seasons calling); no prior play-calling seasons: this season's data only; this season top target share 19%.
**SFO secondary:** DC Raheem Morris, mixed-leaning: Five-man fronts; dime with Lenoir / Green / Stout / Jack Jones; outside Renardo Green / Deommodore Lenoir; nickel Upton Stout; weak spot: Lenoir's coverage fell off in 2025 (65.7); [research confidence medium, 2026-10-14].

**What worked last game → this week vs SFO** (failed play types cut, volume moved to what worked; `SFO allows there` = yards-per-play multiplier on those play types; Δ = effect on this week's projection):

| player        | cut (failed last game)                                                         | more of                                                                               | SFO allows there           |   Δ targets |   Δ rec yds |   Δ carries |   Δ rush yds |   proj yds |
|:--------------|:-------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------|:---------------------------|------------:|------------:|------------:|-------------:|-----------:|
| Dyami Brown   | short_right (100% failed), deep_left (100% failed)                             | short_left x2.0, short_middle x2.0, deep_right x2.0, deep_middle x2.0                 | x0.99, x0.88, x0.93, x0.96 |        -0.0 |         3.3 |         0.0 |          0.0 |       29.3 |
| Treylon Burks | short_left (67% failed), deep_left (100% failed)                               | short_right x1.5, short_middle x1.5, deep_right x1.5, deep_middle x1.5                | x0.85, x0.88, x0.93, x0.96 |        -0.0 |        -1.2 |         0.0 |          0.0 |       22.7 |
| Austin Ekeler | run outside_left (100% failed), run outside_right (100% failed)                | run inside_left x1.4, run inside_right x1.4, run middle x1.4                          | x0.89, x0.88, x0.92        |         0.0 |        -0.0 |        -0.0 |         -0.6 |       12.1 |
| Chig Okonkwo  | short_right (50% failed), short_middle (100% failed), deep_right (100% failed) | short_left x1.9, deep_middle x1.9, deep_left x1.9                                     | x0.99, x0.96, x0.90        |        -0.0 |         0.5 |         0.0 |          0.0 |       25.2 |
| Rachaad White | run inside_left (50% failed)                                                   | run inside_right x1.1, run middle x1.1, run outside_left x1.1, run outside_right x1.1 | x0.88, x0.92, x0.91, x0.96 |         0.0 |         0.0 |         0.0 |          0.1 |       35.1 |

**SFO defensive weak spots:** vs RBs: 5.8 yds/target (league 5.3), x1.12 for RBs.
- SFO struggle: Wk3 vs ARI: +0.17 EPA/play allowed (norm -0.17). Why: TEs 6.7 yds/target vs 3.6 in other games; when blitzing 5.3 yds/dropback vs 3.3 in other games; 3rd/4th downs converted 55% vs 38%
- SFO struggle: Wk4 vs DEN: +0.07 EPA/play allowed (norm -0.15). Why: RBs 8.0 yds/target vs 4.7 in other games
**Offenses like WAS that faced SFO:** ARI (similarity 0.10: +0.2 pass / +0.2 run yds/play vs their norm), MIA (similarity 0.05: -0.9 pass / -0.8 run yds/play vs their norm), DEN (similarity 0.04: -0.5 pass / -0.4 run yds/play vs their norm) → WAS pass x1.01, run x1.00.
**SFO defensive scheme (online/tagged):** blitz: avg, coverage: zone_heavy [online (high)].
- Best matchups: pass_other (x1.00), pass_short_left (x0.99); worst: pass_short_right (x0.85).
- SFO blitzes 33% of dropbacks (league 32%, FTN charting); WAS gains x0.88 as much per dropback vs the blitz as other offenses (55 blitzed dropbacks) -> pass yards x1.00
- WAS deep plays vs zone heavy coverage defenses: x0.93 vs how other offenses fare (15 plays)
- WAS short plays vs zone heavy coverage defenses: x0.93 vs how other offenses fare (58 plays)
- WAS run plays vs zone heavy coverage defenses: x0.92 vs how other offenses fare (57 plays)
- SFO DBs out: Marques Sigle (7 tgts, 6.8 yds/tgt allowed) -> coverage 7.3 → 7.4 yds/tgt; WR yards x1.01
- SFO vs position groups: Chig Okonkwo x0.94

| player                 | pos   |   pass_yds |   pass_td |   interceptions |   carries |   rush_yds |   targets |   receptions |   rec_yds |   anytime_td |
|:-----------------------|:------|-----------:|----------:|----------------:|----------:|-----------:|----------:|-------------:|----------:|-------------:|
| Jayden Daniels         | QB    |     210.30 |      1.11 |            0.49 |      5.05 |      36.98 |      0.00 |         0.00 |      0.00 |         0.25 |
| Jacory Croskey-Merritt | RB    |       0.00 |      0.00 |            0.00 |     12.68 |      44.00 |      1.89 |         1.24 |     13.03 |         0.39 |
| Terry McLaurin         | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.35 |         3.87 |     44.41 |         0.18 |
| Antonio Williams       | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      6.15 |         3.83 |     38.04 |         0.19 |
| Rachaad White          | RB    |       0.00 |      0.00 |            0.00 |      5.37 |      19.16 |      2.33 |         1.61 |     15.27 |         0.22 |
| Chig Okonkwo           | TE    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.92 |         2.64 |     24.52 |         0.11 |
| Dyami Brown            | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.78 |         2.15 |     27.32 |         0.10 |
| Treylon Burks          | WR    |       0.00 |      0.00 |            0.00 |      0.00 |       0.00 |      3.41 |         1.98 |     21.61 |         0.15 |
| Austin Ekeler          | RB    |       0.00 |      0.00 |            0.00 |      1.55 |       5.04 |      0.98 |         0.63 |      6.87 |         0.09 |
| Kaytron Allen          | RB    |       0.00 |      0.00 |            0.00 |      1.87 |       6.42 |      0.00 |         0.00 |      0.00 |         0.07 |

**WAS kicker**

| player       |   fg_made |   xp_made |   kicking_points |
|:-------------|----------:|----------:|-----------------:|
| Drew Stevens |      2.36 |      1.90 |             8.98 |

**WAS defenders (vs SFO offense)**

| player          |   tackles |   sacks |   def_int |
|:----------------|----------:|--------:|----------:|
| Sonny Styles    |      7.04 |    0.06 |      0.15 |
| Jeremy Reaves   |      6.56 |    0.00 |      0.00 |
| Amik Robertson  |      6.39 |    0.00 |      0.00 |
| Rasul Douglas   |      5.09 |    0.00 |      0.18 |
| Quan Martin     |      4.76 |    0.00 |      0.00 |
| Frankie Luvu    |      3.98 |    0.05 |      0.00 |
| Mike Sainristil |      2.89 |    0.00 |      0.00 |
| Daron Payne     |      2.24 |    0.11 |      0.00 |
