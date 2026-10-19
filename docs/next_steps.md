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
