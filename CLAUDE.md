# CLAUDE.md: NFL player-prop projection system

Read this first in every new session. It holds the rules, the record so far, what has been proven or disproven, and how the automation runs. `README.md` explains how projections are built; `output/2026/factor_tests.md` holds every factor test with numbers.

## Owner preferences (how to talk to the user)
- No filler or preamble. Lead with the verdict, then the reasoning.
- If an idea is bad or unlikely to work, say so directly with a probability, and give one concrete alternative that will work.
- Rank options by likelihood of success. State confidence; never fake authority. Don't soften.
- The user is not a programmer, follows on a phone, and bets small (about a $50 bankroll). Use plain language.

## Hard rules (never break)
1. **Never mock or invent data.** Every number comes from real downloaded data.
2. **Market odds are never a model input.** Lines and prices (DraftKings via ESPN, Kalshi, spreads) are used only to grade, find edges or label results. Projections come from play and player data only.
3. **Every factor must be data-driven and tested out of sample** (fit on one span, check another, e.g. 2021-23 then 2024-26, or odd vs even weeks). A change ships only if it improves the backtest; otherwise it is recorded in `factor_tests.md` and left off.
4. **Scraping etiquette:** never lower the PFR 4-second-per-page rate limit; stop on HTTP 429. Same backoff and stop for Kalshi. Kalshi candlesticks are slow (~1.1 s per call) and cached in `data/odds/kalshi`.
5. **Git:** work only on branch `claude/nfl-player-projections-1fbjvo`. Never commit `data/raw` or the `.db` files. `output/` is gitignored, so use `git add -f` for outputs. No PR unless asked. Never put model names in commits. End every commit message with:
   ```
   Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
   Claude-Session: <current session URL>
   ```
6. **Secrets:** never ask the user to paste tokens or keys into chat. They go in GitHub repo secrets (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, optional `ODDS_API_KEY`). As of Oct 22 the user has **not** added them yet.
7. Scheduled runs never edit code, config or locked files, and never use `--force`.

## The record (as of Oct 22, 2026, week 7)
- **Paper bets (qualifying bets, -115 assumed):** week 6 went 13-7, +6.45 units on 30 staked (+21.5%). This is the only graded week so far. Source: `output/2026/paper/ledger.csv`, `summary.md`.
- **Daily grades:** Thu Oct 15 2-0 (+2.61u), Sun Oct 18 10-6 (+4.04u), Mon Oct 19 1-1 (-0.20u). Rush-attempt leans went 24-7 that week; every other stat was close to 50/50. See `output/2026/daily/`.
- **Every lean on a posted line:** 51% right (320 lines). By stat: carries 77%, all others 45-51%.
- **Money list (real money, carries vs Kalshi), week 7 picks so far** (NE @ CHI, in `output/2026/money/week_07.csv`):
  - Henderson 8+ rush attempts YES at 35¢, $2.50
  - Swift 15+ YES at 52¢, $2.50
  - Maye 2 or fewer rush attempts (NO on 3+) at 13¢, $1.69
- **Parlay backtest, weeks 2-6 (regraded Oct 21):** 65 tickets, 2 hits (both 9-13-leg milestone tickets), $11 back on $65 (-83%). First-TD tickets went 0-3. An earlier "first-TD hit" was a grading bug, now fixed.

- **Closing-line value (CLV)** is tracked on every money pick from week 7 on (`nfl_proj/clv.py`, `output/2026/money/week_NN_clv.csv`). It is the main test of whether the carries edge is real: beating the close on most picks over about 50 picks means yes.

## What is proven and what isn't (details in `output/2026/factor_tests.md`)
- **Only real edge: rush attempts (carries) vs the market.** Carries singles with edge ≥10 points vs the Kalshi close: +28% ROI over 157 bets, weeks 2-6 (90% range +10% to +52%). Against real lines, carries hit 0.508 + 0.64 × (p − 0.5).
- **Kalshi close beats the model on every other stat** (log-loss 0.638 vs 0.700). Against real lines, non-carries leans hit about 54% however confident the model is; 70%+ leans hit 46%. Model disagreement with the market is uninformative except on carries.
- **Rushing yards are excluded from bets** (`[paper] exclude_stats`): an early backtest hit 44%, it's 50% live, and there's no edge vs Kalshi. Long runs make it noise.
- **No edge on game lines:** ATS 144-135 (−1.8%), moneyline +1.5%, totals 46% (−11%); margin MAE 10.1 vs the spread's 9.5.
- **Parlays are lottery tickets.** Use profit boosts on 2-3-leg same-game parlays built from money-list carries legs. Never recommend big multi-leg tickets as value.
- **Anytime-TD probabilities are calibrated** (`[sim] td_calib`, 50/50 blend with `td_model.py`). **First-TD probabilities run high:** each game's top pick scored first 11.9% vs 16.4% predicted. Values above 10% are shrunk in `parlays.FIRST_TD_*`. First-TD tickets are removed from the board.
- **Kept ON:**
  - Star receiver efficiency prior (`[players] eff_prior = "rec"`): top WR/TE bias −5.8 → −3.4 yds.
  - `pass_rate_per_point = 0` (game script was double-counted).
  - Side-specific calibration `[paper] calib_side`.
  - Game-day inactives.
  - Team TD adjustment from last season (`data/models/td_team_adj.json`, section 18; refit each season).
  - Target-share flattening `[players] target_share_power = 0.9` (section 16). Carries left at 1.0 (hurt rush-attempt props).
  - Questionable-but-playing haircut `[players] questionable_carries = 0.85`, `questionable_targets = 0.95` (section 21): improves carries MAE and rush-attempt props in 2025 and 2026; Kalshi carries edge unchanged.
  - Money picks are frozen at each game's lock run (`week_NN_final.csv`, `week_NN_frozen_games.txt`); later runs show them unchanged, and grading/CLV use only the frozen picks.
  - Money-list HOLD rule: picks on a team whose lead back missed its last game are held until inactives post (section 14).
- **Tested and OFF or no signal:**
  - Defensive injuries (`def_injuries.enabled = false`)
  - Pass-zone matchups
  - Player/team accuracy persistence (players r 0.04, teams −0.30)
  - Backup-RB projected carries as a win tell
  - Recent-share blend (`recent_blend_*`, section 22): helped a share-only lab, hurt 2026 props. Share misses are mostly luck (at most ~4% left to win on targets, ~0 on carries).
  - Team pace models (section 22): our team volume already beats them; the rest is game script.
  - Underdog rushing signals (section 12; watchlist: "underdog's runs rising over the last 3 games" covered 57% on 227 games, best of 17 tries, so not a bet until paper-tracked)

## Commands (`python -m nfl_proj <cmd>`)
| Command | What it does |
|---|---|
| `scrape` / `build` | download nflverse data, build `data/nfl_<season>.db` (a fresh checkout needs these first; takes minutes) |
| `auto --mode lock` | lock paper bets for games kicking off soon (`output/2026/paper`) |
| `auto --mode grade` | weekly grade + review once the week is final |
| `daily [--date YYYY-MM-DD] [--force]` | win/loss on everything for the latest finished game day → `output/2026/daily/<date>.md` |
| `board [--refresh]` | prop board HTML (`output/2026/board/prop-board.html`): every line, lean, qualifying bets, 5 anytime-TD tickets, 1 same-game parlay per game; appends tickets to `week_NN_tickets.jsonl` (needed by `daily`) |
| `clv [--week N]` | closing-line value of money picks: price listed vs Kalshi's closing midpoint (public candlesticks, no key, cached); also shown in `daily` |
| `money [--refresh]` | real-money list: carries on Kalshi with edge ≥10, quarter Kelly, cap 5% of $50 (`[money]`) |
| `parlays` | weekly long-shot parlays (`output/2026/parlays`) |
| `backtest --weeks A-B --tag X [--config file]` | as-of backtest; for 2025 use a config with `season = 2025` and priors `season = 2024` |
| `paper-summary` | season ledger summary |

Useful tools:
- `tools/kalshi_backtest.py`: model vs Kalshi closes.
- `tools/parlay_backtest.py`: all parlay types, as-of.
- `tools/dog_rush_study.py`
- `tools/td_study.py`
- `tools/calibration_fit.py`

## Board
`output/2026/board/prop-board.html`, rebuilt by Actions and sent to Telegram as a file once its secrets exist.
The old claude.ai artifact (https://claude.ai/artifact/UNar8RW194dBtoQrQKQHw1) only updates when a Claude session republishes it.

## Automation (GitHub Actions on `main`, no Claude needed; live since Oct 27)
`.github/workflows/nfl-props.yml` runs everything from the default branch `main`. Every run commits its outputs to `main`.
Messages go to **issue #1** (built-in `GITHUB_TOKEN`) and to Telegram once `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` secrets exist (Telegram also gets the board HTML file).

| When (ET) | Mode | Runs |
|---|---|---|
| every 30 min around kickoffs | check | `due` (game <= 1.25 h out, after inactives): `auto --mode lock`, `board`, `money --send`, `board --resend`; else `soon --minutes 35`: `money --refresh --send` (final money list; freezes that game's picks) |
| 9:07 AM and 2:07 PM Sun/Mon/Tue/Fri | daily | `daily --send` |
| Tue 11:30 AM (Wed retry) | grade | `auto --mode grade` (incl. miss breakdown) + `parlays --once --send` |
| Wed/Fri/Sat ~6:30 PM | board | `board --refresh`, `money --send`, `board --resend` |
Manual: Actions -> NFL props -> Run workflow (board / lock / money / daily / grade / parlays).

The old claude.ai scheduled tasks are **disabled** (not deleted). The claude.ai board artifact is no longer updated.
Development: work on the feature branch, merge `origin/main` first (the bot commits outputs there), then PR to `main`.
Cost: roughly 1,000 of the 2,000 free Actions minutes a private repo gets per month.

## Key config (`config/projection.toml`)
- `[players] eff_prior = "rec"`, `eff_prior_k = 60` (default), `target_share_power = 0.9`, `questionable_carries = 0.85`, `questionable_targets = 0.95`
- `[sim] td_calib = {a=-0.248, b=0.781}`
- `[script] pass_rate_per_point = 0.0`
- `[paper]`:
  - `min_prob = 0.54`, `min_ev = 0.03`
  - `max_per_game = 99` (no per-game cap since Oct 23), `max_per_team_side = 1`, `max_bets = 100`
  - `exclude_stats = ["rush_yds"]`
  - `calib_side` per family and side (refit Oct 21 on alt lines 0.4×–1.8×)
- `[money]`: edge ≥0.10, spread ≤0.10, quarter Kelly, cap 5%, bankroll $50
- **Qualifying bet** = the model's lean that also passes `[paper]` rules (p ≥ 54%, EV ≥ 3% at −115, one per team per direction, no rushing yards). **Lean** = the model's side on any posted line.

## Data notes
- Free sources only:
  - nflverse (pbp, player stats, snaps, rosters, injuries, depth charts, FTN charting)
  - PFR (rate-limited)
  - ESPN public APIs: scoreboard, injuries, game rosters with game-day inactives, DK lines
  - Sleeper players
  - Kalshi public API (no key)
- nflverse updates overnight, so grading runs the next morning.
- Game-day inactives post about 90 minutes before kickoff (`espn_injuries.fetch_inactives`). Kalshi rush-attempt markets often open only about 40 minutes before kickoff.
- **Ideas ranked but not built:**
  0. QB rush attempts are over-projected ~20% in both seasons (section 22): the largest carries bias left; test a fix next.
  1. RB early-down and goal-line snap participation (check whether free nflverse participation data covers 2025-26).
  2. More graded weeks vs real prices.
  3. NGS rushing data (box counts, expected yards).

## Gotchas
- `pgrep -f <pattern>` inside a wait loop matches its own shell; wait on a PID instead.
- pandas `itertuples` renames columns that start with `_` (e.g. `_samples`); use `zip` over columns.
- Team codes are PFR style (NWE, SFO, KAN, LVR, TAM, GNB, NOR); `nflverse.team()` and `td_model.NV_TO_PFR` map nflverse codes.
