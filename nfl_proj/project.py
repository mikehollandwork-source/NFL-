"""Player projections for upcoming games.

Pipeline for one team (offense T) facing defense D:
  1. Volume: T's plays per game, scaled by how many plays D faces.
  2. Pass/run split: T's dropback rate, nudged by D's pass rate faced.
  3. Play mix: T's recency-weighted share of each bucket (deep right,
     inside-left run, ...), adjusted by last game's results per the
     adaptation setting.
  4. Matchup: each bucket's efficiency multiplied by what D allows in that
     bucket relative to league (shrunk toward league average).
  5. Players: each player's share of targets / carries in each bucket times
     their own (shrunk) efficiency in that bucket.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from . import adaptation
from .playparse import PASS_BUCKETS, RUN_BUCKETS
from .profiles import shrink

OTHER_PASS = "pass_other"  # passes with no depth/direction (throwaways etc.)


def _wsum(s, w):
    return float((s * w).sum())


def bucket_rates(df: pd.DataFrame, by: list[str]) -> pd.DataFrame:
    """Recency-weighted per-bucket rates grouped by ``by``."""
    d = df.assign(
        wn=df["w"],
        wy=df["w"] * df["yards"].fillna(0),
        wc=df["w"] * df["complete"].fillna(False).astype(float),
        wtd=df["w"] * df["touchdown"].astype(float),
    )
    g = d.groupby(by)[["wn", "wy", "wc", "wtd"]].sum()
    g["n_raw"] = d.groupby(by).size()
    g["ypp"] = g["wy"] / g["wn"]
    g["cmp"] = g["wc"] / g["wn"]
    g["td"] = g["wtd"] / g["wn"]
    return g.reset_index()


def _pass_bucket(p: pd.DataFrame) -> pd.Series:
    return p["bucket"].fillna(OTHER_PASS)


class Projector:
    def __init__(self, plays: pd.DataFrame, player_games: pd.DataFrame, games: pd.DataFrame,
                 cfg: dict, labels: pd.DataFrame | None = None, overrides: pd.DataFrame | None = None,
                 scheme: pd.DataFrame | None = None, coach: pd.DataFrame | None = None,
                 corners=None, tables: dict | None = None, priors=None):
        self.cfg = cfg
        self.corners = corners
        from .clock import Clock
        self.clock = Clock(plays, cfg, getattr(priors, "plays_prev", None))
        self.playview = None
        self._sig_cache = {}
        sc = cfg.get("streaks", {})
        self.streak_cfg = {"enabled": sc.get("enabled", True), "method": sc.get("method", "equal_weight"),
                           "cap": {"rec": sc.get("cap_rec_yards", 40.0), "rush": sc.get("cap_rush_yards", 30.0)}}
        self.streak = (tables or {}).get("_streaks", {}) or {}
        from .priors import Priors
        self.priors = priors if priors is not None else Priors(None, cfg)
        self._cb_cache = {}
        self.scheme = scheme.set_index("team") if scheme is not None and not scheme.empty else None
        self.coach = coach.set_index("team") if coach is not None and not coach.empty else None
        self.k_coach = cfg.get("coach", {}).get("prior_games", 3.0)
        self.k_scheme = cfg.get("scheme", {}).get("shrink_plays", 40.0)
        self.all = plays
        self.p = plays[~plays["garbage"]].copy()
        self.pg = player_games
        self.games = games
        self.labels = labels
        self.overrides = overrides if overrides is not None else pd.DataFrame(columns=["team", "player", "status"])
        self.dw = cfg["matchup"]["defense_weight"]
        self.k_def = cfg["matchup"]["shrink_plays"]

        p = self.p
        self.passes = p[p["is_pass"]].assign(pb=lambda d: _pass_bucket(d))
        self.runs = p[p["is_run"] & p["bucket"].notna()]

        self.lg_pass = bucket_rates(self.passes, ["pb"]).set_index("pb")
        self.lg_run = bucket_rates(self.runs, ["bucket"]).set_index("bucket")
        from .defense import Comps, DefenseAnalysis
        tables = tables or {}
        ov = self.overrides
        out_names = set(ov[ov["status"].str.lower() == "out"]["player"]) if not ov.empty else set()
        self.defan = DefenseAnalysis(plays, player_games, tables.get("def_snaps"), cfg, out_names=out_names)
        self.comps = Comps(plays, cfg)
        # A defense's struggle games played without starters who are back now count less.
        gw = self.defan.game_weight

        def dweight(df):
            if not gw:
                return df
            f = pd.Series([gw.get(k, 1.0) for k in zip(df["defense"], df["boxscore_id"])], index=df.index)
            return df.assign(w=df["w"] * f)
        self.def_pass = bucket_rates(dweight(self.passes), ["defense", "pb"]).set_index(["defense", "pb"])
        self.def_run = bucket_rates(dweight(self.runs), ["defense", "bucket"]).set_index(["defense", "bucket"])
        self.off_pass = bucket_rates(self.passes, ["offense", "pb"]).set_index(["offense", "pb"])
        self.off_run = bucket_rates(self.runs, ["offense", "bucket"]).set_index(["offense", "bucket"])
        # Run defense by lane failed the out-of-sample test (output/<season>/factor_tests.md): a
        # defense's yards allowed in one lane doesn't repeat beyond its overall run defense. With
        # run_def_by_lane off, every lane uses the defense's overall rate (offense lane mix kept).
        self.run_def_by_lane = cfg["matchup"].get("run_def_by_lane", False)
        # method "measured": plays before a team rate is trusted at 50%, per side and stat,
        # measured 2021-25 (factor_tests.md section 0); zone / lane splits use the team's overall
        # rate because neither offense nor defense zone splits repeat. "legacy": one shrink_plays.
        self.measured = cfg["matchup"].get("method", "legacy") == "measured"
        self.k = cfg["matchup"].get("shrink", {}) if self.measured else {}
        self.lg_pass_all = bucket_rates(self.passes.assign(_all="p"), ["_all"]).set_index("_all").loc["p"]
        self.off_pass_all = bucket_rates(self.passes, ["offense"]).set_index("offense")
        self.def_pass_all = bucket_rates(dweight(self.passes), ["defense"]).set_index("defense")
        self.off_run_all = bucket_rates(self.runs, ["offense"]).set_index("offense")
        # Repeatable in-season pass-defense traits beyond overall rate (factor_tests section 7):
        # how often opponents throw deep against them, and deep efficiency allowed.
        pd_ = dweight(self.passes).assign(deep=lambda x: x["pb"].str.contains("_deep_").astype(float))
        pd_ = pd_.assign(wd=pd_["w"] * pd_["deep"], wyd=pd_["w"] * pd_["deep"] * pd_["yards"].fillna(0),
                         wy=pd_["w"] * pd_["yards"].fillna(0))
        g = pd_.groupby("defense")[["w", "wd", "wyd", "wy"]].sum()
        g["n"] = pd_.groupby("defense").size()
        g["n_deep"] = pd_.groupby("defense")["deep"].sum()
        self.def_deep = g
        tot = g.sum()
        self.lg_deep = {"share": tot["wd"] / tot["w"], "ypp": tot["wyd"] / tot["wd"] if tot["wd"] else np.nan,
                        "all": tot["wy"] / tot["w"]}
        self.lg_run_all = bucket_rates(self.runs.assign(_all="run"), ["_all"]).set_index("_all").loc["run"]
        self.def_run_all = bucket_rates(dweight(self.runs), ["defense"]).set_index("defense")

        self.est = adaptation.estimate(plays, cfg["adaptation"]["min_plays"])
        self.strength = adaptation.effective_strength(self.est, cfg)

        per_game = plays.groupby(["offense", "boxscore_id"]).size()
        self.lg_ppg = per_game.mean()
        self.lg_dropback = _wmean(p, "dropback")
        self.lg_sack = _wmean(p[p["dropback"]], "is_sack")
        self.lg_int = _wmean(self.passes, "interception")
        self.lg_pass_td = _wmean(self.passes, "touchdown")
        self.lg_run_td = _wmean(p[p["is_run"]], "touchdown")
        self.games_played = plays.groupby("offense")["boxscore_id"].nunique()
        self._scheme_cache = {}
        from .market import Market
        from .ratings import Schedule
        self.sos = Schedule(p, games, cfg)
        self.market = Market(games, cfg)
        self._market_on = True
        self._adj_cache = {}
        self.base_mode = False      # True: SOS only (first pass for model team totals)
        self.weather = {}           # team -> {"pass", "fg", "note"} (set by the pipeline)
        self.oline = {}             # team -> {"sack", "pass", "run", "missing"}
        self.pts_override = {}      # (team, opp) -> simulated model points
        pts = games.dropna(subset=["boxscore_id"])
        lg_pts = (pts[["home_score", "away_score"]].stack().mean()
                  if {"home_score", "away_score"} <= set(pts.columns) and len(pts) else np.nan)
        tds = plays[plays["touchdown"].astype(bool) & ~plays["no_play"].astype(bool)
                    & plays["play_type"].isin(["pass", "run", "scramble"])]
        lg_tds = len(tds) / max(plays.groupby(["offense", "boxscore_id"]).ngroups, 1)
        # Points per offensive TD (folds in FGs, XPs, safeties): turns model TDs into a points total
        self.pts_per_td = float(lg_pts / lg_tds) if lg_tds and pd.notna(lg_pts) else 10.0
        p["family"] = np.where(p["is_run"], "run", np.where(p["deep"], "deep", "short"))
        if self.scheme is not None:
            p = p.join(self.scheme[["blitz", "coverage", "shell"]], on="defense")
        self.p = p

    # ------------------------------------------------------------- coach
    def _coach(self, team):
        if self.coach is None or team not in self.coach.index:
            return None
        return self.coach.loc[team]

    def coach_volume_sd(self, team) -> float:
        """First-time / new play-callers are less predictable: wider volume spread."""
        c = self._coach(team)
        base = 6.5
        if c is not None and (c["caller_tier"] == "first-time play-caller" or c["new_caller_2026"]):
            return base * self.cfg.get("coach", {}).get("new_caller_sd_mult", 1.15)
        return base

    def star_target_share(self, team: str, kind: str, current: float) -> float | None:
        """Blend this season's top-player share with the play-caller's career
        tendency. Returns the blended top share, or None if no history."""
        c = self._coach(team)
        col = "star_target" if kind == "target" else "star_carry"
        if c is None or pd.isna(c.get(col, np.nan)) or pd.isna(current):
            return None
        from .coaches import LEAGUE_RB1_CARRY, LEAGUE_TOP_TARGET
        prior = (LEAGUE_TOP_TARGET if kind == "target" else LEAGUE_RB1_CARRY) + c[col]
        g = float(self.games_played.get(team, 0))
        return (g * current + self.k_coach * prior) / (g + self.k_coach)

    # ------------------------------------------------------------- scheme
    def scheme_effect(self, team: str, opp: str) -> dict:
        """Interaction between THIS offense and the opponent's scheme labels.

        For each label (blitz / coverage / shell) the opponent carries, compare
        how this offense performs vs defenses with that label against how
        every offense performs vs them. Only the offense-specific part is used,
        because the opponent's own stats already carry the league-wide part.
        Blitz labels use 3rd/4th-down plays and are applied in proportion to
        the offense's 3rd/4th-down share. Returns per-family yardage and
        deep-share multipliers plus readable notes.
        """
        key = (team, opp)
        if key in self._scheme_cache:
            return self._scheme_cache[key]
        res = {"ypp": {"deep": 1.0, "short": 1.0, "run": 1.0}, "deep_share": 1.0, "notes": []}
        if self.scheme is None or opp not in self.scheme.index:
            self._scheme_cache[key] = res
            return res
        p = self.p
        k = self.k_scheme
        off = p[p["offense"] == team]
        third_share = float(off["third"].mean()) if len(off) else 0.25
        ftn = "is_blitz" in p.columns and p["is_blitz"].notna().mean() > 0.5
        if ftn:
            self._ftn_blitz(team, opp, res)
        for label in ("blitz", "coverage", "shell"):
            if label == "blitz" and ftn:
                continue  # charted per-play blitzes replace the season label
            v = self.scheme.loc[opp, label]
            if not v or v == "avg" or pd.isna(v):
                continue
            sub = p[p["third"]] if label == "blitz" else p
            weight = third_share if label == "blitz" else 1.0
            vs = sub[sub[label] == v]
            ovs = vs[vs["offense"] == team]
            osub = sub[sub["offense"] == team]
            if len(ovs) == 0:
                continue
            for fam in ("deep", "short", "run"):
                lg_all = sub[sub["family"] == fam]["yards"].mean()
                lg_v = vs[vs["family"] == fam]["yards"].mean()
                o_all = osub[osub["family"] == fam]["yards"].mean()
                o_v_rows = ovs[ovs["family"] == fam]
                if o_v_rows.empty or not all(np.isfinite([lg_all, lg_v, o_all])) or min(lg_all, lg_v, o_all) <= 0:
                    continue
                inter = (o_v_rows["yards"].mean() / o_all) / (lg_v / lg_all)
                inter = float(shrink(inter, len(o_v_rows), 1.0, k))
                res["ypp"][fam] *= 1 + weight * (np.clip(inter, 0.6, 1.6) - 1)
                if abs(inter - 1) >= 0.05:
                    res["notes"].append(f"{team} {fam} plays vs {v.replace('_', ' ')} {label} defenses: "
                                        f"x{inter:.2f} vs how other offenses fare ({len(o_v_rows)} plays)")
            # Does this offense throw deep more often against this label?
            pv, po = vs[vs["is_pass"]], osub[osub["is_pass"]]
            ov_pass = ovs[ovs["is_pass"]]
            if len(ov_pass) and po["deep"].mean() > 0 and pv["deep"].mean() > 0 and sub[sub["is_pass"]]["deep"].mean() > 0:
                lg_ratio = pv["deep"].mean() / sub[sub["is_pass"]]["deep"].mean()
                o_ratio = ov_pass["deep"].mean() / po["deep"].mean()
                inter = float(shrink(o_ratio / lg_ratio, len(ov_pass), 1.0, k))
                res["deep_share"] *= 1 + weight * (np.clip(inter, 0.5, 2.0) - 1)
                if abs(inter - 1) >= 0.1:
                    res["notes"].append(f"{team} deep-throw rate vs {v.replace('_', ' ')} {label}: x{inter:.2f}")
        self._scheme_cache[key] = res
        return res

    def _ftn_blitz(self, team: str, opp: str, res: dict) -> None:
        """Per-play blitz effect from FTN charting. How much worse (or better)
        THIS offense does when blitzed, relative to how the league does when
        blitzed, applied in proportion to how often the opponent blitzes vs
        league. The league-wide blitz effect is already in the opponent's own
        allowed stats, so only the offense-specific part is used."""
        p = self.p
        db = p[(p["dropback"]) & p["is_blitz"].notna()]
        if db.empty:
            return
        lg_b, lg_nb = db[db["is_blitz"] == 1]["yards"].mean(), db[db["is_blitz"] == 0]["yards"].mean()
        o = db[db["offense"] == team]
        ob, onb = o[o["is_blitz"] == 1], o[o["is_blitz"] == 0]
        d = db[db["defense"] == opp]
        if len(ob) == 0 or len(onb) == 0 or len(d) == 0 or min(lg_b, lg_nb, onb["yards"].mean()) <= 0:
            return
        s = (ob["yards"].mean() / onb["yards"].mean()) / (lg_b / lg_nb)
        s = float(np.clip(shrink(s, len(ob), 1.0, self.k_scheme), 0.6, 1.6))
        rb, lb = d["is_blitz"].mean(), db["is_blitz"].mean()
        mult = (1 + rb * (s - 1)) / (1 + lb * (s - 1))
        res["ypp"]["deep"] *= mult
        res["ypp"]["short"] *= mult
        res["blitz_mult"] = mult
        if abs(s - 1) >= 0.05:
            res["notes"].append(
                f"{opp} blitzes {rb:.0%} of dropbacks (league {lb:.0%}, FTN charting); {team} gains "
                f"x{s:.2f} as much per dropback vs the blitz as other offenses ({len(ob)} blitzed dropbacks) "
                f"-> pass yards x{mult:.2f}")

    def scramble_td_rate(self, team: str) -> float:
        """QB scramble TD rate, shrunk toward the league scramble TD rate."""
        sc = self.all[(self.all["play_type"] == "scramble") & ~self.all["no_play"].astype(bool)]
        lg = float(sc["touchdown"].astype(float).mean()) if len(sc) else 0.03
        t = sc[sc["offense"] == team]
        return float(shrink(t["touchdown"].astype(float).mean() if len(t) else np.nan, len(t), lg, 40))

    def reset_adjustments(self):
        self._adj_cache = {}

    def corner_factors(self, team: str, opp: str) -> tuple[dict, list[str]]:
        """Per-receiver yards-per-target multipliers: the opponent's available
        corners and shadow assignment (corners.py) times how the defense does
        against this receiver's position group (defense.py)."""
        key = (team, opp)
        if key in self._cb_cache:
            return self._cb_cache[key]
        act = self.active_players(team)
        tp = self.passes[(self.passes["offense"] == team) & self.passes["target_id"].notna()]
        share = tp.groupby("target_id")["w"].sum()
        share = share / share.sum() if share.sum() else share
        rec = act.assign(share=act["player_id"].map(share).fillna(0.0))
        f, notes = ({}, [])
        if self.corners is not None and self.corners.enabled:
            f, notes = self.corners.receiver_factors(opp, rec)
        f = dict(f)
        moved = []
        use_pos = self.cfg.get("defense", {}).get("position_factor", True)
        for r in rec.itertuples():
            # Yards per target vs WR / TE / RB beyond the defense's overall rate doesn't repeat
            # (factor_tests: split-half r ~ 0), so [defense] position_factor = false skips it.
            pf = self.defan.position_factor(opp, r.pos) if use_pos else 1.0
            if pf != 1.0:
                f[r.player_id] = f.get(r.player_id, 1.0) * pf
                if abs(pf - 1) >= 0.05 and r.share >= 0.08:
                    moved.append(f"{r.player} x{pf:.2f}")
        if moved:
            notes = notes + [f"{opp} vs position groups: " + ", ".join(moved)]
        self._cb_cache[key] = (f, notes)
        return self._cb_cache[key]

    # ---------------------------------------------------------- adjustments
    def adjustments(self, team: str, opp: str, week: int) -> dict:
        """Strength of schedule, game script (model margin) and, for teams the
        market reads consistently, a blend with the implied team total."""
        key = (team, opp, week, self._market_on)
        if key in self._adj_cache:
            return self._adj_cache[key]
        dw = self.dw
        f = self.sos.factor
        a = {"sos": {"off_pass": f("pass", "off", team), "off_run": f("run", "off", team),
                     "off_pts": f("points", "off", team),
                     "def_pass": 1 + dw * (f("pass", "def", opp) - 1),
                     "def_run": 1 + dw * (f("run", "def", opp) - 1),
                     "def_pts": 1 + dw * (f("points", "def", opp) - 1)},
             "market": None, "td_factor": 1.0, "ypp_factor": 1.0, "dropback_shift": 0.0,
             "weather": self.weather.get(team, {"pass": 1.0, "fg": 1.0, "note": None}),
             "oline": self.oline.get(team, {"sack": 1.0, "pass": 1.0, "run": 1.0, "missing": []})}
        self._adj_cache[key] = a  # provisional, so the base projections below see no adjustment
        if not self._market_on or self.base_mode:
            return a
        line = self.market.line(team, week)
        script = self.cfg.get("script", {})
        if line is None and not script.get("enabled", True):
            return a
        self._market_on = False
        try:
            pts = self.model_points(team, opp, week)
            opp_pts = self.model_points(opp, team, week) if script.get("enabled", True) else None
        finally:
            self._market_on = True
        if opp_pts is not None:
            # Game script from our own projected margin: the team we project
            # to lead runs more, the trailing team throws more.
            margin = pts - opp_pts
            a["script"] = {"model_pts": pts, "opp_model_pts": opp_pts, "margin": margin}
            a["dropback_shift"] = -script.get("pass_rate_per_point", 0.004) * margin
        if line is not None:
            # Implied team total, only for teams the market has read consistently.
            m = self.market.blend(line, pts)
            a.update(market=m, td_factor=m["td_factor"], ypp_factor=m["ypp_factor"])
        return a

    def model_points(self, team: str, opp: str, week: int) -> float:
        """Projected points from the model alone. Uses the simulated team total
        (6 x TD + extra points + 3 x field goals, from a first simulation pass
        without game script or market) when available; otherwise projected
        TDs x league points per TD."""
        if (team, opp) in self.pts_override:
            return self.pts_override[(team, opp)]
        base, _ = self.project_team(team, opp, week)
        tds = float(base.get("pass_td", pd.Series(dtype=float)).sum()
                    + base.get("rush_td", pd.Series(dtype=float)).sum())
        return tds * self.pts_per_td

    def td_mults(self, team: str, opp: str, week: int) -> dict:
        """Opponent TD / INT multipliers after schedule and market adjustments."""
        d_pass = self.p[(self.p["defense"] == opp) & self.p["is_pass"]]
        d_run = self.p[(self.p["defense"] == opp) & self.p["is_run"]]
        a = self.adjustments(team, opp, week)
        s = a["sos"]["off_pts"] * a["sos"]["def_pts"] * a["td_factor"]
        pf = self.priors.factor
        return {"pass_td": self._ratio(_wmean(d_pass, "touchdown"), self.lg_pass_td, len(d_pass),
                                       pf("def", opp, "pass_td"), "def_pass_td") * s,
                "run_td": self._ratio(_wmean(d_run, "touchdown"), self.lg_run_td, len(d_run),
                                      pf("def", opp, "run_td"), "def_run_td") * s,
                "int": self._ratio(_wmean(d_pass, "interception"), self.lg_int, len(d_pass), key="def_int")}

    # ---------------------------------------------------------------- team
    def _ratio(self, d_val, lg_val, n, prior_mult: float = 1.0, key: str | None = None):
        """Opponent multiplier: shrunk D rate / league rate, weighted by dw.
        Small samples are pulled toward ``prior_mult`` x league (the
        defense's regressed 2025 rate when priors are on). With measured
        shrinkage (``key`` names the rate) the measured constant already
        sets how much to trust the defense, so dw isn't applied again."""
        if lg_val is None or pd.isna(lg_val) or lg_val == 0:
            return 1.0
        if self.measured and key in self.k:
            return float(shrink(d_val, n, lg_val * prior_mult, self.k[key]) / lg_val)
        d = shrink(d_val, n, lg_val * prior_mult, self.k_def)
        return float(1 + self.dw * (d / lg_val - 1))

    def team_volume(self, team: str, opp: str, week: int | None = None) -> dict:
        p, allp = self.p, self.all
        off_games = allp[allp["offense"] == team].groupby("boxscore_id").size()
        def_games = allp[allp["defense"] == opp].groupby("boxscore_id").size()
        g_n = len(off_games)
        k = self.priors.k_games if self.priors.enabled else 0.0
        own = (g_n * off_games.mean() + k * self.lg_ppg * self.priors.plays_factor(team)) / (g_n + k) \
            if g_n + k > 0 else self.lg_ppg
        plays = own * (1 + self.dw * (def_games.mean() / self.lg_ppg - 1))
        clock = None
        if self.clock is not None and self.clock.enabled:
            clock = self.clock.game(team, opp)
            plays = clock["plays"]

        t, d = p[p["offense"] == team], p[p["defense"] == opp]
        db_rate = _wmean(t, "dropback")
        if self.measured and "def_pass_rate" in self.k:
            # How much opponents throw against this defense, shrunk by its measured constant
            db_rate += shrink(_wmean(d, "dropback"), len(d), self.lg_dropback, self.k["def_pass_rate"]) - self.lg_dropback
        else:
            db_rate += self.dw * (_wmean(d, "dropback") - self.lg_dropback) * 0.5
        c = self._coach(team)
        if c is not None and not pd.isna(c.get("pass_lean", np.nan)):
            # Early in the season lean on the play-caller's career pass tendency.
            g = float(self.games_played.get(team, 0))
            prior = self.lg_dropback + c["pass_lean"]
            db_rate = (g * db_rate + self.k_coach * prior) / (g + self.k_coach)
        if week is not None:
            # Game script from the spread: favorites run more.
            db_rate = float(np.clip(db_rate + self.adjustments(team, opp, week)["dropback_shift"], 0.3, 0.8))
        dropbacks = plays * db_rate
        tdb, ddb = t[t["dropback"]], d[d["dropback"]]
        own_sack = _wmean(tdb, "is_sack")
        if self.measured and "off_sack" in self.k:
            own_sack = shrink(own_sack, len(tdb), self.lg_sack, self.k["off_sack"])
        sack_rate = own_sack * self._ratio(_wmean(ddb, "is_sack"), self.lg_sack, len(ddb), key="def_sack")
        if week is not None:
            sack_rate *= self.adjustments(team, opp, week)["oline"]["sack"]
        scramble_rate = _wmean(tdb, "play_type", fn=lambda s: s == "scramble")
        sacks = dropbacks * sack_rate
        scrambles = dropbacks * scramble_rate
        return {"plays": plays, "clock": clock, "dropback_rate": db_rate, "pass_att": dropbacks - sacks - scrambles,
                "sacks": sacks, "scrambles": scrambles, "runs": plays - dropbacks}

    def mix(self, team: str, family: str, opp: str | None = None) -> tuple[dict, dict]:
        """Bucket shares for the next game and the last-game signal used."""
        src = self.passes if family == "pass" else self.runs
        col = "pb" if family == "pass" else "bucket"
        t = src[src["offense"] == team]
        w = t.groupby(col)["w"].sum()
        buckets = (PASS_BUCKETS + [OTHER_PASS]) if family == "pass" else RUN_BUCKETS
        share = {b: float(w.get(b, 0.0)) for b in buckets}
        tot = sum(share.values()) or 1.0
        share = {b: v / tot for b, v in share.items()}

        signal = adaptation.last_game_signal(self.p, team, self.cfg["adaptation"]["min_plays"])
        if self.strength:
            for b in list(share):
                if b in signal:
                    share[b] *= float(np.clip(1 + self.strength * signal[b], 0.5, 1.5))
            tot = sum(share.values()) or 1.0
            share = {b: v / tot for b, v in share.items()}
        if family == "pass" and opp is not None:
            # Measured: the defense's own deep share faced this season (shrunk); legacy: scheme data
            ds = self.deep_factors(opp)["share"] if self.measured else self.scheme_effect(team, opp)["deep_share"]
            if ds != 1.0:
                share = {b: v * (ds if "_deep_" in b else 1.0) for b, v in share.items()}
                tot = sum(share.values()) or 1.0
                share = {b: v / tot for b, v in share.items()}
        return share, {b: v for b, v in signal.items() if b in share}

    def bucket_matchup(self, team: str, opp: str, family: str, b: str, week: int | None = None) -> dict:
        lg = self.lg_pass if family == "pass" else self.lg_run
        dd = self.def_pass if family == "pass" else self.def_run
        oo = self.off_pass if family == "pass" else self.off_run
        lgr = lg.loc[b] if b in lg.index else None
        if lgr is None:
            return {"ypp": 0.0, "cmp": 0.0, "td": 0.0, "m_ypp": 1.0, "m_cmp": 1.0}
        o = oo.loc[(team, b)] if (team, b) in oo.index else None
        d = dd.loc[(opp, b)] if (opp, b) in dd.index else None
        if self.measured:
            return self._matchup_measured(team, opp, family, b, lgr, week)
        if family != "pass" and not self.run_def_by_lane:
            d_all = self.def_run_all.loc[opp] if opp in self.def_run_all.index else None
            lane_lg = lgr
            lgr = lgr.copy()
            if d_all is not None:
                # Defense's overall ratio applied to this lane's league rate
                d = pd.Series({"ypp": d_all["ypp"] / self.lg_run_all["ypp"] * lane_lg["ypp"],
                               "n_raw": d_all["n_raw"]})
            else:
                d = None
        o_n = o["n_raw"] if o is not None else 0
        fam_p = "pass" if family == "pass" else "run"
        team_ypp = shrink(o["ypp"] if o is not None else np.nan, o_n,
                          lgr["ypp"] * self.priors.factor("off", team, fam_p), self.k_def)
        team_cmp = shrink(o["cmp"] if o is not None else np.nan, o_n, lgr["cmp"], self.k_def)
        m_ypp = (self._ratio(d["ypp"], lgr["ypp"], d["n_raw"], self.priors.factor("def", opp, fam_p))
                 if d is not None else self.priors.factor("def", opp, fam_p) ** self.dw)
        m_cmp = self._ratio(d["cmp"], lgr["cmp"], d["n_raw"]) if d is not None and family == "pass" else 1.0
        fam = "run" if family == "run" else ("deep" if "_deep_" in b else "short")
        m_ypp *= self.scheme_effect(team, opp)["ypp"][fam]
        m_ypp *= self.comps.effect(team, opp)["pass" if family == "pass" else "run"]
        if week is not None:
            a = self.adjustments(team, opp, week)
            side = "pass" if family == "pass" else "run"
            team_ypp *= a["sos"][f"off_{side}"]
            m_ypp *= a["sos"][f"def_{side}"] * a["ypp_factor"]
            m_ypp *= a["oline"][side] * (a["weather"]["pass"] if side == "pass" else 1.0)
        return {"ypp": float(team_ypp), "cmp": float(team_cmp), "td": float(lgr["td"]),
                "m_ypp": m_ypp, "m_cmp": m_cmp}

    def deep_factors(self, opp: str) -> dict:
        """Deep share faced and deep efficiency allowed (relative to the
        defense's overall pass rate), shrunk by their measured constants."""
        out = {"share": 1.0, "eff": 1.0}
        if not self.measured or opp not in self.def_deep.index or not self.lg_deep["share"]:
            return out
        g, lg = self.def_deep.loc[opp], self.lg_deep
        share = shrink(g["wd"] / g["w"] if g["w"] else np.nan, g["n"], lg["share"], self.k.get("def_deep_share", 830))
        out["share"] = float(share / lg["share"])
        if g["wd"] > 0 and g["wy"] > 0 and lg["ypp"] and np.isfinite(lg["ypp"]):
            rel = (g["wyd"] / g["wd"] / lg["ypp"]) / (g["wy"] / g["w"] / lg["all"])
            out["eff"] = float(shrink(rel, g["n_deep"], 1.0, self.k.get("def_deep_eff", 205)))
        return out

    def _matchup_measured(self, team, opp, family, b, lgr, week):
        """Bucket rate = league rate for this bucket x the offense's overall
        ratio x the defense's overall ratio, each shrunk by its measured
        constant toward the team's regressed 2025 rate."""
        fam = "pass" if family == "pass" else "run"
        lg_all = self.lg_pass_all if fam == "pass" else self.lg_run_all
        o_all = (self.off_pass_all if fam == "pass" else self.off_run_all)
        d_all = (self.def_pass_all if fam == "pass" else self.def_run_all)
        o = o_all.loc[team] if team in o_all.index else None
        d = d_all.loc[opp] if opp in d_all.index else None
        pf = self.priors.factor
        ko, kd = (self.k.get("off_pass_ypp", 150), self.k.get("def_pass_ypp", 1000)) if fam == "pass" else \
                 (self.k.get("off_run_ypp", 325), self.k.get("def_run_ypp", 380))
        o_ratio = shrink(o["ypp"] if o is not None else np.nan, o["n_raw"] if o is not None else 0,
                         lg_all["ypp"] * pf("off", team, fam), ko) / lg_all["ypp"]
        team_ypp = lgr["ypp"] * o_ratio
        if fam == "pass":
            o_cmp = shrink(o["cmp"] if o is not None else np.nan, o["n_raw"] if o is not None else 0,
                           lg_all["cmp"] * pf("off", team, "cmp"), self.k.get("off_cmp", 275)) / lg_all["cmp"]
            team_cmp = min(lgr["cmp"] * o_cmp, 0.95)
            m_cmp = self._ratio(d["cmp"] if d is not None else np.nan, lg_all["cmp"],
                                d["n_raw"] if d is not None else 0, pf("def", opp, "cmp"), "def_cmp")
        else:
            team_cmp, m_cmp = float(lgr["cmp"]), 1.0
        m_ypp = float(shrink(d["ypp"] if d is not None else np.nan, d["n_raw"] if d is not None else 0,
                             lg_all["ypp"] * pf("def", opp, fam), kd) / lg_all["ypp"])
        sfam = "run" if fam == "run" else ("deep" if "_deep_" in b else "short")
        if sfam == "deep":
            m_ypp *= self.deep_factors(opp)["eff"]
        m_ypp *= self.scheme_effect(team, opp)["ypp"][sfam]
        m_ypp *= self.comps.effect(team, opp)[fam]
        if week is not None:
            a = self.adjustments(team, opp, week)
            team_ypp *= a["sos"][f"off_{fam}"]
            m_ypp *= a["sos"][f"def_{fam}"] * a["ypp_factor"]
            m_ypp *= a["oline"][fam] * (a["weather"]["pass"] if fam == "pass" else 1.0)
        return {"ypp": float(team_ypp), "cmp": float(team_cmp), "td": float(lgr["td"]),
                "m_ypp": m_ypp, "m_cmp": m_cmp}

    # ------------------------------------------------------------- players
    def active_players(self, team: str) -> pd.DataFrame:
        pg = self.pg[self.pg["team"] == team]
        weeks = sorted(pg["week"].unique())[-self.cfg["players"]["active_within_games"]:]
        active = pg[pg["week"].isin(weeks)][["player_id", "player", "pos"]].drop_duplicates("player_id")
        ov = self.overrides[(self.overrides["team"] == team)
                            & (self.overrides["status"].str.lower() == "out")]
        ids = set(ov["player_id"]) if "player_id" in ov else set()
        return active[~active["player"].isin(set(ov["player"])) & ~active["player_id"].isin(ids)]

    def starting_qb(self, team: str) -> str | None:
        ov = self.overrides[(self.overrides["team"] == team)
                            & (self.overrides["status"].str.lower() == "starter")]
        pg = self.pg[self.pg["team"] == team]
        if not ov.empty:
            ids = set(ov["player_id"]) - {""} if "player_id" in ov else set()
            hit = pg[pg["player_id"].isin(ids) | pg["player"].isin(ov["player"])]
            if not hit.empty:
                return hit["player_id"].iloc[0]
        active = set(self.active_players(team)["player_id"])
        qbs = pg[(pg["pass_att"] > 0) & pg["player_id"].isin(active)]
        if qbs.empty:
            return None
        last = qbs[qbs["week"] == qbs["week"].max()]
        return last.sort_values("pass_att", ascending=False)["player_id"].iloc[0]

    def _shares(self, df: pd.DataFrame, id_col: str, bucket_col: str, active: set, k: float,
                team: str | None = None, kind: str | None = None) -> pd.DataFrame:
        """Per player per bucket: share of team volume, shrunk toward the
        player's overall share. Inactive players' volume is redistributed."""
        df = df[df[id_col].notna()]
        tot_b = df.groupby(bucket_col)["w"].sum()
        tot = df["w"].sum()
        pb = df.groupby([id_col, bucket_col])["w"].sum().rename("wb").reset_index()
        overall = (df.groupby(id_col)["w"].sum() / tot).rename("overall")
        pb = pb.merge(overall, left_on=id_col, right_index=True)
        pb["team_b"] = pb[bucket_col].map(tot_b)
        pb["share"] = shrink(pb["wb"] / pb["team_b"], pb["team_b"], pb["overall"], k)
        pb = pb[pb[id_col].isin(active)]
        # Players with season volume but none in a bucket still get their overall share there.
        players = overall[overall.index.isin(active)]
        grid = pd.MultiIndex.from_product([players.index, df[bucket_col].unique()], names=[id_col, bucket_col])
        pb = pb.set_index([id_col, bucket_col]).reindex(grid).reset_index()
        pb["share"] = pb["share"].fillna(pb[id_col].map(players) * 0.5)
        # Volume streaks: keep only the measured share of a two-game run
        vf = (self._streak_factors(df, id_col, "rec" if id_col == "target_id" else "rush", "vol")
              if self.streak_cfg["method"] == "factor" else {})
        if vf:
            pb["share"] = pb["share"] * pb[id_col].map(vf).fillna(1.0)
        pb["share"] = pb["share"] / pb.groupby(bucket_col)["share"].transform("sum")
        if team is not None and kind is not None and not players.empty:
            # Coach angle: pull the top player's share toward the play-caller's
            # career star reliance (fades as this season's games accumulate).
            top = players.idxmax()
            cur = players.max() / players.sum()
            target = self.star_target_share(team, kind, cur)
            if target is not None and cur > 0:
                f = float(np.clip(target / cur, 0.7, 1.4))
                pb.loc[pb[id_col] == top, "share"] *= f
                pb["share"] = pb["share"] / pb.groupby(bucket_col)["share"].transform("sum")
        return pb[[id_col, bucket_col, "share"]]

    def _player_eff(self, df, id_col, bucket_col, team_eff: dict, k: float) -> pd.DataFrame:
        """Per player and play type: yards per play and catch rate, shrunk
        toward the team's rate. Long plays are capped when measuring the
        player (they mostly don't repeat); the player's capped rate is
        compared with the team's capped rate and that ratio is applied to
        the team's normal rate, so the league level is unchanged. Then a
        recent hot / cold streak is kept only to the measured extent."""
        d = df[df[id_col].notna()]
        fam = "rec" if id_col == "target_id" else "rush"
        cap = self.streak_cfg["cap"][fam]
        dc = d.assign(yards=d["yards"].clip(upper=cap))
        if self.streak_cfg["method"] == "equal_weight":
            # Efficiency is noisy: every game counts the same (no recency boost for a hot stretch)
            dc = dc.assign(w=1.0)
        g = bucket_rates(dc, [id_col, bucket_col])
        team_c = bucket_rates(dc, [bucket_col]).set_index(bucket_col)["ypp"]
        g["team_ypp"] = g[bucket_col].map(lambda b: team_eff.get(b, {}).get("ypp", np.nan))
        g["team_cmp"] = g[bucket_col].map(lambda b: team_eff.get(b, {}).get("cmp", np.nan))
        tc = g[bucket_col].map(team_c)
        ratio = shrink(g["ypp"] / tc.replace(0, np.nan), g["n_raw"], 1.0, k)
        g["ypp_s"] = np.where(tc > 0, ratio * g["team_ypp"], shrink(g["ypp"], g["n_raw"], g["team_ypp"], k))
        g["cmp_s"] = shrink(g["cmp"], g["n_raw"], g["team_cmp"], k)
        f = self._streak_factors(dc, id_col, fam, "eff") if self.streak_cfg["method"] == "factor" else {}
        if f:
            g["ypp_s"] = g["ypp_s"] * g[id_col].map(f).fillna(1.0)
        td = d.groupby(id_col).agg(td=("touchdown", "sum"), n=("touchdown", "size"))
        return g.set_index([id_col, bucket_col]), td

    # ------------------------------------------------------ play-level matchup
    def sig_mult(self, team: str, opp: str, pid: str, family: str) -> dict:
        """{bucket: yards multiplier} from how this defense handles the exact
        kinds of plays (play action, screens) the player was kept on last game."""
        if not self.cfg.get("player_adaptation", {}).get("play_level", True) or self.player_cut() <= 0:
            return {}
        key = (team, opp, pid, family)
        if key not in self._sig_cache:
            if self.playview is None:
                from .plays_view import PlayView
                self.playview = PlayView(self.all, self.cfg)
            self._sig_cache[key] = self.playview.player_factors(team, opp, pid, family)
        return self._sig_cache[key]

    # ------------------------------------------------------ streak regression
    def _streak_factors(self, d: pd.DataFrame, id_col: str, fam: str, what: str) -> dict:
        """player -> multiplier that keeps only the measured share of a
        two-game streak. ``what`` = "eff" (yards per play) or "vol" (share
        of the team's targets / carries)."""
        p = self.streak.get(f"{fam}_{what}", {}).get("persist")
        if p is None or not self.streak_cfg["enabled"] or d.empty:
            return {}
        weeks = sorted(d["week"].unique())
        if len(weeks) < 3:
            return {}
        recent_w, base_w = weeks[-2:], weeks[:-2]
        out = {}
        if what == "eff":
            for pid, g in d.groupby(id_col):
                base, rec = g[g["week"].isin(base_w)], g[g["week"].isin(recent_w)]
                if len(base) < 4 or len(rec) < 4:
                    continue
                b, r = base["yards"].mean(), rec["yards"].mean()
                cur = np.average(g["yards"], weights=g["w"])
                target = b + p * (r - b)
                if cur > 0 and target > 0:
                    out[pid] = float(np.clip(target / cur, 0.7, 1.3))
        else:
            tot = d.groupby("week").size()
            for pid, g in d.groupby(id_col):
                n = g.groupby("week").size().reindex(weeks, fill_value=0)
                sh = n / tot.reindex(weeks)
                base, rec = sh[base_w].mean(), sh[recent_w].mean()
                if n[base_w].sum() < 4:
                    continue
                cur = float((g["w"].sum()) / d["w"].sum())
                target = base + p * (rec - base)
                if cur > 0 and target > 0:
                    out[pid] = float(np.clip(target / cur, 0.6, 1.4))
        return out

    # ------------------------------------------------------ player adaptation
    def player_signal(self, team: str, family: str) -> pd.DataFrame:
        """Each player's last game for this team, by play type (bucket): how
        many plays he got and what share failed (custom negative-play rule:
        netted zero or less, a turnover, or a failed 3rd/4th down)."""
        src = self.passes if family == "pass" else self.runs
        id_col, b_col = ("target_id", "pb") if family == "pass" else ("rusher_id", "bucket")
        t = src[(src["offense"] == team) & src[id_col].notna()]
        if t.empty:
            return pd.DataFrame(columns=["player_id", "bucket", "n", "fail", "yards"])
        last = t[t["week"] == t["week"].max()]
        g = last.groupby([id_col, b_col]).agg(n=("negative", "size"), fail=("negative", "mean"),
                                               yards=("yards", "sum")).reset_index()
        return g.rename(columns={id_col: "player_id", b_col: "bucket"})

    def player_cut(self) -> float:
        """How hard to cut a player's failed play types. ``assume``: the
        configured value (1.0 = cancel them); ``measured``: estimated from
        this season (does a player's share of a play type drop after it
        failed?); ``off``: 0."""
        c = self.cfg.get("player_adaptation", {})
        mode = c.get("mode", "assume")
        if mode == "off" or getattr(self, "_pa_off", False):
            return 0.0
        if mode == "assume":
            return float(c.get("cut", 1.0))
        if not hasattr(self, "_measured_cut"):
            self._measured_cut = measure_player_cut(self.p, c.get("min_plays", 1))
        return float(np.clip(self._measured_cut["cut"], 0.0, 1.0))

    def usage_plan(self, team: str, opp: str, family: str, base_shares: pd.DataFrame,
                   mix: dict) -> tuple[dict, pd.DataFrame, list[dict]]:
        """Apply player-level adaptation: each player's volume moves out of
        the play types that failed for him last game into the ones that
        worked (his total volume stays the same). The team's play mix is
        rebuilt from the players' new plans. Returns (mix, shares, changes)."""
        cut = self.player_cut()
        c = self.cfg.get("player_adaptation", {})
        min_n = c.get("min_plays", 1)
        id_col, b_col = ("target_id", "pb") if family == "pass" else ("rusher_id", "bucket")
        if cut <= 0 or base_shares.empty:
            return mix, base_shares, []
        sig = self.player_signal(team, family)
        sig = sig[sig["n"] >= min_n]
        if sig.empty:
            return mix, base_shares, []
        T = base_shares.assign(T=base_shares[b_col].map(mix).fillna(0) * base_shares["share"])
        fail = {(r.player_id, r.bucket): r.fail for r in sig.itertuples()}
        T["f"] = [1 - cut * fail.get((pid, b), 0.0) for pid, b in zip(T[id_col], T[b_col])]
        # Play types that worked for him last game (used, and not all failures)
        worked = {(r.player_id, r.bucket) for r in sig.itertuples() if r.fail < 1.0}
        T["worked"] = [(pid, b) in worked for pid, b in zip(T[id_col], T[b_col])]
        before = T.groupby(id_col)["T"].transform("sum")
        T["T2"] = T["T"] * T["f"]
        lost = before - T.groupby(id_col)["T2"].transform("sum")
        # What he loses in failed play types goes to the ones that worked last
        # game (in proportion to his usual use of them); if nothing worked,
        # to the play types that weren't cut.
        w_base = T["T2"].where(T["worked"], 0.0)
        w_sum = w_base.groupby(T[id_col]).transform("sum")
        alt = T["T2"].where(T["f"] >= 1.0, 0.0)
        alt_sum = alt.groupby(T[id_col]).transform("sum")
        T["T2"] = np.where(w_sum > 0, T["T2"] + lost * w_base / w_sum.replace(0, np.nan),
                           np.where(alt_sum > 0, T["T2"] + lost * alt / alt_sum.replace(0, np.nan), T["T"]))
        T["T2"] = T["T2"].fillna(T["T"])
        tot = T.groupby(b_col)["T2"].sum()
        new_mix = dict(mix)
        targeted_before = T.groupby(b_col)["T"].sum()
        for b in new_mix:
            if b in tot.index and targeted_before.get(b, 0) > 0:
                new_mix[b] = mix[b] * tot[b] / targeted_before[b]
        z = sum(new_mix.values()) or 1.0
        new_mix = {b: v / z for b, v in new_mix.items()}
        T["share"] = T["T2"] / T.groupby(b_col)["T2"].transform("sum").replace(0, np.nan)
        T["share"] = T["share"].fillna(0.0)
        changes = []
        for pid, g in T.groupby(id_col):
            moved = g[(g["f"] < 1) | (g["T2"] > g["T"] * 1.05)]
            if len(moved) and before[g.index[0]] > 0:
                changes.append({"player_id": pid,
                                "cut": [(r[b_col], fail.get((pid, r[b_col]), 0)) for _, r in g[g["f"] < 1].iterrows()],
                                "more": [(r[b_col], r["T2"] / max(r["T"], 1e-9)) for _, r in g[g["T2"] > g["T"] * 1.05].iterrows()]})
        return new_mix, T[[id_col, b_col, "share"]], changes

    def adaptation_view(self, team: str, opp: str, week: int, changes: list[dict]) -> pd.DataFrame:
        """Per player: what got cut / what he'll do more of, how this
        defense handles those play types, and the projected effect
        (with vs without player adaptation)."""
        if not changes:
            return pd.DataFrame()
        self._pa_off = True
        try:
            base, _ = self.project_team(team, opp, week)
        finally:
            self._pa_off = False
        adapted, _ = self.project_team(team, opp, week)
        cols = ["targets", "rec_yds", "carries", "rush_yds"]
        b = base.set_index("player_id").reindex(columns=cols).fillna(0)
        a = adapted.set_index("player_id").reindex(columns=cols).fillna(0)
        names = dict(zip(adapted["player_id"], adapted["player"]))
        rows = []
        for ch in changes:
            pid = ch["player_id"]
            if pid not in a.index:
                continue
            fam = "pass" if any(bk.startswith("pass") for bk, _ in ch["cut"] + ch["more"]) else "run"
            m = {bk: self.bucket_matchup(team, opp, fam, bk, week)["m_ypp"] for bk, _ in ch["more"]}
            d = a.loc[pid] - b.loc[pid] if pid in b.index else a.loc[pid]
            rows.append({
                "player": names.get(pid, pid), "type": "receiving" if fam == "pass" else "rushing",
                "cut (failed last game)": ", ".join(f"{bk.replace('pass_', '').replace('run_', 'run ')} "
                                                   f"({f:.0%} failed)" for bk, f in ch["cut"]) or "—",
                "more of": ", ".join(f"{bk.replace('pass_', '').replace('run_', 'run ')} x{r:.1f}"
                                     for bk, r in ch["more"]) or "—",
                f"{opp} allows there": ", ".join(f"x{v:.2f}" for v in m.values()) or "—",
                "Δ targets": d["targets"], "Δ rec yds": d["rec_yds"],
                "Δ carries": d["carries"], "Δ rush yds": d["rush_yds"],
                "proj yds": a.loc[pid, "rec_yds"] + a.loc[pid, "rush_yds"]})
        out = pd.DataFrame(rows)
        if out.empty:
            return out
        return out.reindex(out[["Δ rec yds", "Δ rush yds"]].abs().sum(axis=1).sort_values(ascending=False).index)

    def project_team(self, team: str, opp: str, week: int) -> tuple[pd.DataFrame, dict]:
        vol = self.team_volume(team, opp, week)
        pmix, psig = self.mix(team, "pass", opp)
        rmix, rsig = self.mix(team, "run", opp)
        peff = {b: self.bucket_matchup(team, opp, "pass", b, week) for b in pmix}
        reff = {b: self.bucket_matchup(team, opp, "run", b, week) for b in rmix}
        active_df = self.active_players(team)
        active = set(active_df["player_id"])
        names = dict(zip(active_df["player_id"], active_df["player"]))
        pos = dict(zip(active_df["player_id"], active_df["pos"]))

        tm = self.td_mults(team, opp, week)
        m_pass_td, m_run_td, m_int = tm["pass_td"], tm["run_td"], tm["int"]

        rows = {}

        def row(pid):
            return rows.setdefault(pid, {"player_id": pid, "player": names.get(pid, pid),
                                         "pos": pos.get(pid, ""), "team": team, "opp": opp,
                                         "week": week})

        # Receiving
        k_t = self.cfg["players"]["shrink_targets"]
        tp = self.passes[self.passes["offense"] == team]
        shares = self._shares(tp, "target_id", "pb", active, k_t, team, "target")
        pmix, shares, p_changes = self.usage_plan(team, opp, "pass", shares, pmix)
        eff, td = self._player_eff(tp, "target_id", "pb", peff, k_t)
        cbf, cb_notes = self.corner_factors(team, opp)
        lg_td_t = self.lg_pass_td
        rec_raw = rec_adj = 0.0
        for r in shares.itertuples():
            b, pid = r.pb, r.target_id
            tgts = vol["pass_att"] * pmix.get(b, 0) * r.share
            e = eff.loc[(pid, b)] if (pid, b) in eff.index else None
            ypt = e["ypp_s"] if e is not None else peff[b]["ypp"]
            cr = e["cmp_s"] if e is not None else peff[b]["cmp"]
            x = row(pid)
            x["targets"] = x.get("targets", 0) + tgts
            x["receptions"] = x.get("receptions", 0) + tgts * min(cr * peff[b]["m_cmp"], 0.98)
            yds = tgts * ypt * peff[b]["m_ypp"] * self.sig_mult(team, opp, pid, "pass").get(b, 1.0)
            rec_raw += yds
            rec_adj += yds * cbf.get(pid, 1.0)
            x["rec_yds"] = x.get("rec_yds", 0) + yds * cbf.get(pid, 1.0)
        for pid, x in rows.items():
            if pid in td.index:
                rate = shrink(td.loc[pid, "td"] / td.loc[pid, "n"], td.loc[pid, "n"],
                              lg_td_t * self.priors.factor("off", team, "pass_td"), 60)
            else:
                rate = lg_td_t
            x["rec_td"] = x.get("targets", 0) * rate * m_pass_td

        # Rushing
        k_c = self.cfg["players"]["shrink_carries"]
        tr = self.runs[self.runs["offense"] == team]
        rshares = self._shares(tr, "rusher_id", "bucket", active, k_c, team, "carry")
        rmix, rshares, r_changes = self.usage_plan(team, opp, "run", rshares, rmix)
        reff_p, rtd = self._player_eff(tr, "rusher_id", "bucket", reff, k_c)
        for r in rshares.itertuples():
            b, pid = r.bucket, r.rusher_id
            car = vol["runs"] * rmix.get(b, 0) * r.share
            e = reff_p.loc[(pid, b)] if (pid, b) in reff_p.index else None
            ypc = e["ypp_s"] if e is not None else reff[b]["ypp"]
            x = row(pid)
            x["carries"] = x.get("carries", 0) + car
            x["rush_yds"] = x.get("rush_yds", 0) + car * ypc * reff[b]["m_ypp"] * \
                self.sig_mult(team, opp, pid, "run").get(b, 1.0)
        for pid, x in rows.items():
            if pid in rtd.index:
                rate = shrink(rtd.loc[pid, "td"] / rtd.loc[pid, "n"], rtd.loc[pid, "n"],
                              self.lg_run_td * self.priors.factor("off", team, "run_td"), 80)
            else:
                rate = self.lg_run_td
            x["rush_td"] = x.get("carries", 0) * rate * m_run_td

        # Passing (team level, credited to the starting QB)
        qb = self.starting_qb(team)
        if qb:
            x = row(qb)
            x["pass_att"] = vol["pass_att"]
            x["completions"] = sum(vol["pass_att"] * pmix[b] * min(peff[b]["cmp"] * peff[b]["m_cmp"], 0.98)
                                   for b in pmix)
            # QB yards = the receivers' yards, so corner adjustments carry through
            cb_ratio = rec_adj / rec_raw if rec_raw > 0 else 1.0
            x["pass_yds"] = cb_ratio * sum(vol["pass_att"] * pmix[b] * peff[b]["ypp"] * peff[b]["m_ypp"]
                                           for b in pmix)
            tp_td = _wmean(tp, "touchdown")
            tp_int = _wmean(tp, "interception")
            n = len(tp)
            x["pass_td"] = vol["pass_att"] * shrink(tp_td, n, self.lg_pass_td * self.priors.factor(
                "off", team, "pass_td"), self.k.get("off_pass_td", 150)) * m_pass_td
            x["interceptions"] = vol["pass_att"] * shrink(tp_int, n, self.lg_int, self.k.get("off_int", 200)) * m_int
            sc = self.p[(self.p["offense"] == team) & (self.p["play_type"] == "scramble")]
            sc_ypc = sc["yards"].mean() if len(sc) else 6.0
            x["rush_td"] = x.get("rush_td", 0) + vol["scrambles"] * self.scramble_td_rate(team) * m_run_td
            x["carries"] = x.get("carries", 0) + vol["scrambles"]
            x["rush_yds"] = x.get("rush_yds", 0) + vol["scrambles"] * sc_ypc
            x["sacks"] = vol["sacks"]

        out = pd.DataFrame(rows.values())
        context = {"team": team, "opp": opp, "volume": vol, "pass_mix": pmix, "run_mix": rmix,
                   "pass_signal": psig, "run_signal": rsig, "pass_eff": peff, "run_eff": reff,
                   "qb": names.get(qb, qb) if qb else None,
                   "scheme_notes": self.scheme_effect(team, opp)["notes"] + cb_notes,
                   "adjust": self.adjustments(team, opp, week) if self._market_on else None,
                   "player_changes": p_changes + r_changes}
        return out, context

    def project_week(self, week: int) -> tuple[pd.DataFrame, list[dict]]:
        sched = self.games[(self.games["week"] == week)]
        frames, contexts = [], []
        for g in sched.itertuples():
            for team, opp in ((g.home, g.away), (g.away, g.home)):
                df, ctx = self.project_team(team, opp, week)
                frames.append(df)
                contexts.append(ctx)
        stat_cols = ["pass_att", "completions", "pass_yds", "pass_td", "interceptions", "sacks",
                     "carries", "rush_yds", "rush_td", "targets", "receptions", "rec_yds", "rec_td"]
        out = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
        for c in stat_cols:
            if c not in out:
                out[c] = 0.0
        out[stat_cols] = out[stat_cols].fillna(0).round(2)
        keep = (out[["pass_att", "carries", "targets"]].sum(axis=1) >= 0.5)
        out = out[keep][["week", "team", "opp", "player", "pos", "player_id"] + stat_cols]
        return out.sort_values(["team", "pass_att", "rec_yds", "rush_yds"],
                               ascending=[True, False, False, False]), contexts


def measure_player_cut(plays: pd.DataFrame, min_plays: int = 1) -> dict:
    """Does a player get less of a play type after it failed for him?
    For each player, bucket and game: x = share of his plays in that bucket
    that failed; y = his share of that bucket next game / his share so far
    - 1. The slope of y on x (negative = cut after failure) gives the cut."""
    p = plays[~plays["garbage"]]
    rows = []
    for fam, id_col in (("pass", "target_id"), ("run", "rusher_id")):
        src = p[(p["is_pass"] if fam == "pass" else p["is_run"]) & p[id_col].notna() & p["bucket"].notna()]
        g = src.groupby(["offense", "week", id_col, "bucket"]).agg(n=("negative", "size"),
                                                                    fail=("negative", "mean")).reset_index()
        tot = src.groupby(["offense", "week", "bucket"]).size().rename("bn")
        g = g.join(tot, on=["offense", "week", "bucket"])
        g["sh"] = g["n"] / g["bn"]
        for (team, pid, b), sub in g.groupby(["offense", id_col, "bucket"]):
            sub = sub.sort_values("week")
            weeks = sorted(src[src["offense"] == team]["week"].unique())
            for _, cur in sub.iterrows():
                nxt_w = [w for w in weeks if w > cur["week"]]
                if not nxt_w or cur["n"] < min_plays:
                    continue
                nw = nxt_w[0]
                nxt = sub[sub["week"] == nw]
                prior = sub[sub["week"] <= cur["week"]]["sh"].mean()
                y = (float(nxt["sh"].iloc[0]) if len(nxt) else 0.0) / prior - 1 if prior > 0 else np.nan
                rows.append({"x": cur["fail"], "y": y, "n": cur["n"]})
    d = pd.DataFrame(rows).dropna()
    if len(d) < 50:
        return {"cut": 0.0, "slope": np.nan, "t": np.nan, "n": len(d)}
    X = np.column_stack([np.ones(len(d)), d["x"]])
    w = d["n"].to_numpy(float)
    W = np.diag(w)
    coef = np.linalg.solve(X.T @ W @ X, X.T @ W @ d["y"].to_numpy(float))
    resid = d["y"].to_numpy(float) - X @ coef
    se = np.sqrt(np.diag(np.linalg.inv(X.T @ W @ X)) * (w * resid ** 2).sum() / (len(d) - 2))
    slope, t = coef[1], coef[1] / se[1]
    return {"cut": float(max(0.0, -slope) * min(1.0, abs(t) / 2)), "slope": float(slope), "t": float(t),
            "n": len(d)}


def _wmean(df, col, fn=None):
    if df.empty:
        return np.nan
    s = df[col]
    if fn is not None:
        s = fn(s)
    m = s.notna()
    if not m.any():
        return np.nan
    return float(np.average(s[m].astype(float), weights=df.loc[m, "w"]))
