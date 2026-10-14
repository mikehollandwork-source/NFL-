"""Possession and play volume from the game clock.

Time of possession itself is not a stable team trait (2025: a team's
possession share in weeks 1-9 vs 10-18, r = 0.06; it mostly follows the
scoreboard, r = 0.38 with final margin). What is stable is pace: seconds
used per clock-running play (runs and completed passes, Q1-3, close
score, outside the last two minutes of the half; split-half r = 0.70,
2025 -> 2026 r = 0.36).

So possession is modelled from the clock, which makes it emerge instead of
being assumed:

  seconds a team's drive uses  t = plays per drive x seconds per play
                                    (seconds per play scaled by its pace)
  drives in the game           D = league drives x 2 x league drive time / (t_A + t_B)
  team plays                   = D x plays per drive (offense x opponent defense)

A slow, drive-sustaining team uses more clock, which cuts drives for BOTH
teams, so its opponent gets fewer plays too. Plays per drive is barely
repeatable (split-half r = 0.05), so it is shrunk hard toward league
average (``volume.ppd_shrink_games``). Walk-forward test (projected vs
actual team plays): 2025 MAE 6.80 vs 6.91 for the old method and 6.85 for
the league average; 2026 weeks 2-5: 6.66 vs 6.86 and 6.66.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

CLOCK_PLAYS = (15, 50)  # plausible seconds between snaps on a clock-running play


def pace_table(plays: pd.DataFrame) -> pd.DataFrame:
    """Per team: summed seconds and count of clock-running plays (offense)."""
    need = {"game_secs_left", "drive", "complete", "quarter", "score_diff"}
    if not need <= set(plays.columns):
        return pd.DataFrame(columns=["s", "n"])
    sc = plays[plays["play_type"].isin(["pass", "run", "sack", "scramble"]) & ~plays["no_play"].astype(bool)]
    sc = sc.sort_values(["boxscore_id", "seq"])
    nxt = sc.groupby(["boxscore_id", "drive"])["game_secs_left"].shift(-1)
    spp = sc["game_secs_left"] - nxt
    run_clock = (sc["play_type"] == "run") | ((sc["play_type"] == "pass") & sc["complete"].fillna(False).astype(bool))
    late_half = (sc["quarter"] == 2) & (sc["game_secs_left"] < 1800 + 120)
    m = run_clock & (sc["quarter"] <= 3) & ~late_half & (sc["score_diff"].abs() <= 8) & spp.between(*CLOCK_PLAYS)
    return spp[m].groupby(sc.loc[m, "offense"]).agg(s="sum", n="size")


class Clock:
    def __init__(self, plays: pd.DataFrame, cfg: dict, prev_plays: pd.DataFrame | None = None):
        c = cfg.get("volume", {})
        self.enabled = c.get("method", "clock") == "clock" and "drive" in plays.columns
        self.k_ppd = c.get("ppd_shrink_games", 8.0)
        self.k_pace = c.get("pace_shrink_games", 3.0)
        self.r_pace_prev = c.get("pace_prior_regress", 0.7)
        if not self.enabled:
            return
        sc = plays[plays["play_type"].isin(["pass", "run", "sack", "scramble"]) & ~plays["no_play"].astype(bool)]
        g = sc.groupby(["boxscore_id", "offense", "defense"]).agg(plays=("play_type", "size"),
                                                                    drives=("drive", "nunique")).reset_index()
        d = plays.dropna(subset=["drive", "drive_top"]).drop_duplicates(["boxscore_id", "drive"])
        top = d.groupby(["boxscore_id", "offense"])["drive_top"].sum()
        g = g.join(top.rename("top"), on=["boxscore_id", "offense"])
        self.lg_ppd = g["plays"].sum() / g["drives"].sum()
        self.lg_drives = g["drives"].mean()
        self.lg_spp = g["top"].sum() / g["plays"].sum()
        self.off = g.groupby("offense").agg(n=("plays", "size"), p=("plays", "sum"), d=("drives", "sum"))
        self.dfn = g.groupby("defense").agg(n=("plays", "size"), p=("plays", "sum"), d=("drives", "sum"))
        pt = pace_table(plays)
        self.lg_pace = float(pt["s"].sum() / pt["n"].sum()) if len(pt) else 37.0
        self.pace_n_per_game = float(pt["n"].sum() / max(g["boxscore_id"].nunique() * 2, 1)) if len(pt) else 12.0
        self.pace = pt
        self.prev_pace = None
        if prev_plays is not None and not prev_plays.empty:
            pp = pace_table(prev_plays)
            if len(pp):
                self.prev_pace = (pp["s"] / pp["n"]) / (pp["s"].sum() / pp["n"].sum())

    def _shr(self, v, n, prior, k):
        return (n * v + k * prior) / (n + k)

    def pace_of(self, team: str) -> float:
        prior = self.lg_pace
        if self.prev_pace is not None and team in self.prev_pace.index:
            prior = self.lg_pace * (1 + self.r_pace_prev * (self.prev_pace[team] - 1))
        if team not in self.pace.index:
            return prior
        s, n = self.pace.loc[team, "s"], self.pace.loc[team, "n"]
        return float(self._shr(s / n, n / self.pace_n_per_game, prior, self.k_pace))

    def ppd(self, off: str, dfn: str) -> float:
        a = self.off.loc[off] if off in self.off.index else None
        b = self.dfn.loc[dfn] if dfn in self.dfn.index else None
        pa = self._shr(a["p"] / a["d"], a["n"], self.lg_ppd, self.k_ppd) if a is not None else self.lg_ppd
        pb = self._shr(b["p"] / b["d"], b["n"], self.lg_ppd, self.k_ppd) if b is not None else self.lg_ppd
        return float(pa * pb / self.lg_ppd)

    def game(self, a: str, b: str) -> dict:
        """Drives, plays and possession share for both teams in an A-B game."""
        pa, pb = self.ppd(a, b), self.ppd(b, a)
        ta = pa * self.lg_spp * self.pace_of(a) / self.lg_pace
        tb = pb * self.lg_spp * self.pace_of(b) / self.lg_pace
        drives = self.lg_drives * (2 * self.lg_ppd * self.lg_spp) / (ta + tb)
        return {"drives": drives, "plays": drives * pa, "opp_plays": drives * pb,
                "top_share": ta / (ta + tb), "pace": self.pace_of(a), "opp_pace": self.pace_of(b),
                "ppd": pa, "opp_ppd": pb}
