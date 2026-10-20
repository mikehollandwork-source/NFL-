# Next session plan (after week 6 grading)

## 1. TD scorer model: backtest and tighten
- Build a 2021-25 out-of-sample test: predicted anytime-TD probability vs actual for every WR/TE/RB game.
- Check calibration by bucket (10-20%, 20-30%, ... 50%+). Week 6: 13 deep-target WRs summed 4.0 expected TDs, 4 scored, but the order was wrong.
- Candidate predictors, each kept only if it improves log-loss out of sample:
  red-zone target/carry share (inside 20 and inside 10), end-zone targets, goal-line carries,
  team implied points / projected TDs, air yards share, deep-target share, near-miss end-zone targets
  (catchable incompletions + DPI in the end zone), player size/position, defense TDs allowed by position (expect noise).
- Measure shrinkage (plays to 50% trust) for each share like the other factors.
- Add TD calls to the weekly grading ledger.

## 2. System-wide post-mortem
- Grade every lean in calls_ledger by stat, side, line size, p bucket, usage trend, position, and days since lock.
  Week 6 board leans were ~coin-flip (191-186 at 54%+) while locked bets went 12-6: find out why (line moves, injuries, select rules).
- Calibration check: is p_cal still right? Refit sigmoid on all graded leans + backtests.
- Unders vs overs, low lines (1.5/2.5 receptions) vs yardage.
- Game-level misses: passing TD distribution by game (ARI@LAR 5.1 proj -> 2; HOU@JAX 2.2 -> 7).
- Keep only changes that improve the 2021-25 backtest and don't hurt 2026 wks 2-6.

## 3. Ops
- Triggers fire into this session and were delivered ~20h late on Sun Oct 18 (4 games missed).
  Fix: env vars TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID / ODDS_API_KEY, then fresh-session triggers.

## 4. Weekly loss autopsy (build into `auto --mode grade`)
- Tag every loss: role/availability (snap share vs projected), volume (targets/carries vs projected share),
  efficiency (per-touch yards), game script (team plays / pass rate vs projected), market disagreed (line moved
  against us after lock = negative CLV), coin flip (lost by <= 1 rec / 1 carry / ~10% of yds line).
- Track CLV (needs a closing-line snapshot at kickoff), calibration by p bucket, splits by stat/side/line size, cumulative.
- Change gate: pattern over 3+ weeks / ~100 bets AND passes 2021-25 backtest. Rule tweaks (e.g. min_prob 0.54 -> 0.60;
  week 6: leans >=60% went 68-50 +7.7%, below 60% lost) can move faster than model changes. Log each change with evidence.
- Week 6 official: locked 13-7, +6.46u, +21.5% ROI at assumed -115.

## Done (Oct 20)
- Calibration by stat family + side (`[paper] calib_family`, tools/calibration_fit.py). Model is overconfident on
  overs: 2025 backtest over-leans on receptions hit 46%, targets 47%; week 6 real: receptions overs 43%, rec_yds overs 46%.
  Log-loss: 2026 wks 4-5 0.675 -> 0.662, week 6 real 0.706 -> 0.698 (P>0 = 93%). Carries also improve.
  Week 6 lock replay: 12-7 (+18%) vs actual 13-7 (+21.5%) -> selection noise; overs fall from 12/20 to 5/19.
- min_prob kept at 0.54: with the new calibration, higher floors don't clearly help on real lines.
- Anytime-TD calibration ([sim] td_calib): raw TD odds too extreme (50-60% calls scored 41% in 2025, 37% in 2026).
  Fit on 2025, 2026 log-loss 0.494 -> 0.485. TD study (2021-25, 16k player-games): volume + team scoring outlook
  carry nearly all the signal; red-zone/inside-10/end-zone usage add little; last-week end-zone near misses, deep
  share and air yards add nothing.
- Game script: model applies ~4-5x too much (pass-rate slope per point of projected margin -0.0056 vs actual -0.0012;
  big favorites' RB carries -17%, big underdogs' targets -19%, pass yds -18%). Testing pass_rate_per_point = 0.
