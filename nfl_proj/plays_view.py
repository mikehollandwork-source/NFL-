"""Each player's individual plays from his last game, and what they're worth
against this week's defense.

Public play-by-play doesn't name the play call, so a play is described by
what it does record (its "signature"): pass depth and direction or run gap,
plus play action, screen and RPO when FTN charted them. Every play the
player was involved in last game is listed with its result:

  cancelled  netted zero or less, a turnover, or a failed 3rd/4th down
  kept       everything else

Next week his volume goes to the kind of plays he was kept on (see
Projector.usage_plan). This module adds the play-level matchup: for each
kept play, how this week's defense does against that signature (e.g.
play-action deep right, screens to the right) beyond what its overall
numbers in that direction already say. The average over a player's kept
plays in a play type becomes a yards multiplier for him there.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def _flag(df: pd.DataFrame, col: str) -> pd.Series:
    if col not in df:
        return pd.Series(False, index=df.index)
    return df[col].fillna(False).astype(bool)


def signature(df: pd.DataFrame) -> pd.Series:
    """Readable play signature: 'deep right, play action', 'run inside left'."""
    pa, sc, rpo = _flag(df, "play_action"), _flag(df, "screen"), _flag(df, "rpo")
    base = np.where(df["play_type"] == "pass",
                    df["depth"].fillna("?").astype(str) + " " + df["direction"].fillna("?").astype(str),
                    df["bucket"].fillna("run").astype(str).str.replace("run_", "run ").str.replace("_", " "))
    extra = (np.where(pa, ", play action", "") + np.where(sc, ", screen", "") + np.where(rpo, ", RPO", ""))
    return pd.Series(base, index=df.index) + pd.Series(extra, index=df.index)


class PlayView:
    def __init__(self, plays: pd.DataFrame, cfg: dict):
        c = cfg.get("player_adaptation", {})
        self.k = c.get("signature_shrink_plays", 15.0)
        self.dw = cfg["matchup"]["defense_weight"]
        self.clip = (c.get("signature_min_factor", 0.85), c.get("signature_max_factor", 1.15))
        p = plays[~plays["garbage"] & plays["play_type"].isin(["pass", "run"])].copy()
        p["pa"] = _flag(p, "play_action")
        p["scr"] = _flag(p, "screen")
        p["bkt"] = np.where(p["play_type"] == "pass", p["bucket"].fillna("pass_other"), p["bucket"])
        p["sig"] = signature(p)
        self.p = p
        key = ["bkt", "pa", "scr"]
        self.lg_sig = p.groupby(key)["yards"].mean()
        self.lg_bkt = p.groupby("bkt")["yards"].mean()
        self.def_sig = p.groupby(["defense"] + key)["yards"].agg(["mean", "size"])
        self.def_bkt = p.groupby(["defense", "bkt"])["yards"].mean()
        self.lg_flag = {}
        for fam in ("pass", "run"):
            f = p[p["play_type"] == fam]
            for flag in ("pa", "scr"):
                a, b = f[f[flag]]["yards"].mean(), f[~f[flag]]["yards"].mean()
                self.lg_flag[(fam, flag)] = (a / b) if b and a == a else 1.0

    def sig_factor(self, defense: str, bkt: str, pa: bool, scr: bool) -> float:
        """How this defense does on this exact signature beyond its numbers
        for the whole play type (relative to how the league does)."""
        if not (pa or scr):
            return 1.0
        k = (defense, bkt, pa, scr)
        lg_s = self.lg_sig.get((bkt, pa, scr), np.nan)
        lg_b = self.lg_bkt.get(bkt, np.nan)
        d_b = self.def_bkt.get((defense, bkt), np.nan)
        if k not in self.def_sig.index or not all(np.isfinite([lg_s, lg_b, d_b])) or min(lg_s, lg_b, d_b) <= 0:
            return 1.0
        d_s, n = self.def_sig.loc[k, "mean"], self.def_sig.loc[k, "size"]
        inter = (d_s / d_b) / (lg_s / lg_b)
        shrunk = (n * inter + self.k) / (n + self.k)
        return float(np.clip(1 + self.dw * (shrunk - 1), *self.clip))

    def last_game(self, team: str, player_id: str, family: str) -> pd.DataFrame:
        id_col = "target_id" if family == "pass" else "rusher_id"
        t = self.p[(self.p["offense"] == team) & (self.p[id_col] == player_id)]
        if t.empty:
            return t
        last_team_week = self.p[self.p["offense"] == team]["week"].max()
        t = t[t["week"] == last_team_week]
        return t.assign(kept=~t["negative"].astype(bool))

    def player_factors(self, team: str, opp: str, player_id: str, family: str) -> dict:
        """{bucket: yards multiplier} from the signatures of his kept plays."""
        g = self.last_game(team, player_id, family)
        if g.empty:
            return {}
        k = g[g["kept"]]
        out = {}
        for b, sub in k.groupby("bkt"):
            out[b] = float(np.mean([self.sig_factor(opp, b, bool(r.pa), bool(r.scr)) for r in sub.itertuples()]))
        return out

    def table(self, team: str, opp: str, player_id: str, family: str, week: int) -> pd.DataFrame:
        g = self.last_game(team, player_id, family)
        if g.empty:
            return g
        rows = []
        for r in g.sort_values(["quarter", "seq"]).itertuples():
            f = self.sig_factor(opp, r.bkt, bool(r.pa), bool(r.scr))
            rows.append({"qtr": r.quarter, "down": f"{int(r.down)}&{int(r.ytg)}" if pd.notna(r.down) else "",
                         "play": r.sig, "yds": r.yards, "result": "kept" if r.kept else "cancelled",
                         f"{opp} on this play": f"x{f:.2f}" if f != 1.0 else "—",
                         "description": str(r.detail)[:110]})
        return pd.DataFrame(rows)
