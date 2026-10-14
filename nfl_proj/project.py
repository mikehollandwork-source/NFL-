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
                 corners=None):
        self.cfg = cfg
        self.corners = corners
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
        self.def_pass = bucket_rates(self.passes, ["defense", "pb"]).set_index(["defense", "pb"])
        self.def_run = bucket_rates(self.runs, ["defense", "bucket"]).set_index(["defense", "bucket"])
        self.off_pass = bucket_rates(self.passes, ["offense", "pb"]).set_index(["offense", "pb"])
        self.off_run = bucket_rates(self.runs, ["offense", "bucket"]).set_index(["offense", "bucket"])

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

    def corner_factors(self, team: str, opp: str) -> tuple[dict, list[str]]:
        """Per-receiver yards-per-target multipliers from the opponent's
        available corners and shadow assignment (see corners.py)."""
        key = (team, opp)
        if key in self._cb_cache:
            return self._cb_cache[key]
        if self.corners is None or not self.corners.enabled:
            self._cb_cache[key] = ({}, [])
            return self._cb_cache[key]
        act = self.active_players(team)
        tp = self.passes[(self.passes["offense"] == team) & self.passes["target_id"].notna()]
        share = tp.groupby("target_id")["w"].sum()
        share = share / share.sum() if share.sum() else share
        rec = act.assign(share=act["player_id"].map(share).fillna(0.0))
        self._cb_cache[key] = self.corners.receiver_factors(opp, rec)
        return self._cb_cache[key]

    # ---------------------------------------------------------- adjustments
    def adjustments(self, team: str, opp: str, week: int) -> dict:
        """Strength-of-schedule factors and the market blend for one matchup."""
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
             "market": None, "td_factor": 1.0, "ypp_factor": 1.0, "dropback_shift": 0.0}
        self._adj_cache[key] = a  # provisional, so the base projection below sees no market
        line = self.market.line(team, week) if self._market_on else None
        if line is not None:
            self._market_on = False
            try:
                base, _ = self.project_team(team, opp, week)
            finally:
                self._market_on = True
            model_tds = float(base.get("pass_td", pd.Series(dtype=float)).sum()
                              + base.get("rush_td", pd.Series(dtype=float)).sum())
            m = self.market.blend(line, model_tds * self.pts_per_td)
            a.update(market=m, td_factor=m["td_factor"], ypp_factor=m["ypp_factor"],
                     dropback_shift=m["dropback_shift"])
        return a

    def td_mults(self, team: str, opp: str, week: int) -> dict:
        """Opponent TD / INT multipliers after schedule and market adjustments."""
        d_pass = self.p[(self.p["defense"] == opp) & self.p["is_pass"]]
        d_run = self.p[(self.p["defense"] == opp) & self.p["is_run"]]
        a = self.adjustments(team, opp, week)
        s = a["sos"]["off_pts"] * a["sos"]["def_pts"] * a["td_factor"]
        return {"pass_td": self._ratio(_wmean(d_pass, "touchdown"), self.lg_pass_td, len(d_pass)) * s,
                "run_td": self._ratio(_wmean(d_run, "touchdown"), self.lg_run_td, len(d_run)) * s,
                "int": self._ratio(_wmean(d_pass, "interception"), self.lg_int, len(d_pass))}

    # ---------------------------------------------------------------- team
    def _ratio(self, d_val, lg_val, n):
        """Opponent multiplier: shrunk D rate / league rate, weighted by dw."""
        if lg_val is None or pd.isna(lg_val) or lg_val == 0:
            return 1.0
        d = shrink(d_val, n, lg_val, self.k_def)
        return float(1 + self.dw * (d / lg_val - 1))

    def team_volume(self, team: str, opp: str, week: int | None = None) -> dict:
        p, allp = self.p, self.all
        off_games = allp[allp["offense"] == team].groupby("boxscore_id").size()
        def_games = allp[allp["defense"] == opp].groupby("boxscore_id").size()
        plays = off_games.mean() * (1 + self.dw * (def_games.mean() / self.lg_ppg - 1))

        t, d = p[p["offense"] == team], p[p["defense"] == opp]
        db_rate = _wmean(t, "dropback")
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
        sack_rate = _wmean(tdb, "is_sack") * self._ratio(_wmean(ddb, "is_sack"), self.lg_sack, len(ddb))
        scramble_rate = _wmean(tdb, "play_type", fn=lambda s: s == "scramble")
        sacks = dropbacks * sack_rate
        scrambles = dropbacks * scramble_rate
        return {"plays": plays, "dropback_rate": db_rate, "pass_att": dropbacks - sacks - scrambles,
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
            ds = self.scheme_effect(team, opp)["deep_share"]
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
        o_n = o["n_raw"] if o is not None else 0
        team_ypp = shrink(o["ypp"] if o is not None else np.nan, o_n, lgr["ypp"], self.k_def)
        team_cmp = shrink(o["cmp"] if o is not None else np.nan, o_n, lgr["cmp"], self.k_def)
        m_ypp = self._ratio(d["ypp"], lgr["ypp"], d["n_raw"]) if d is not None else 1.0
        m_cmp = self._ratio(d["cmp"], lgr["cmp"], d["n_raw"]) if d is not None and family == "pass" else 1.0
        fam = "run" if family == "run" else ("deep" if "_deep_" in b else "short")
        m_ypp *= self.scheme_effect(team, opp)["ypp"][fam]
        if week is not None:
            a = self.adjustments(team, opp, week)
            side = "pass" if family == "pass" else "run"
            team_ypp *= a["sos"][f"off_{side}"]
            m_ypp *= a["sos"][f"def_{side}"] * a["ypp_factor"]
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
        d = df[df[id_col].notna()]
        g = bucket_rates(d, [id_col, bucket_col])
        g["team_ypp"] = g[bucket_col].map(lambda b: team_eff.get(b, {}).get("ypp", np.nan))
        g["team_cmp"] = g[bucket_col].map(lambda b: team_eff.get(b, {}).get("cmp", np.nan))
        g["ypp_s"] = shrink(g["ypp"], g["n_raw"], g["team_ypp"], k)
        g["cmp_s"] = shrink(g["cmp"], g["n_raw"], g["team_cmp"], k)
        td = d.groupby(id_col).agg(td=("touchdown", "sum"), n=("touchdown", "size"))
        return g.set_index([id_col, bucket_col]), td

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
            yds = tgts * ypt * peff[b]["m_ypp"]
            rec_raw += yds
            rec_adj += yds * cbf.get(pid, 1.0)
            x["rec_yds"] = x.get("rec_yds", 0) + yds * cbf.get(pid, 1.0)
        for pid, x in rows.items():
            if pid in td.index:
                rate = shrink(td.loc[pid, "td"] / td.loc[pid, "n"], td.loc[pid, "n"], lg_td_t, 60)
            else:
                rate = lg_td_t
            x["rec_td"] = x.get("targets", 0) * rate * m_pass_td

        # Rushing
        k_c = self.cfg["players"]["shrink_carries"]
        tr = self.runs[self.runs["offense"] == team]
        rshares = self._shares(tr, "rusher_id", "bucket", active, k_c, team, "carry")
        reff_p, rtd = self._player_eff(tr, "rusher_id", "bucket", reff, k_c)
        for r in rshares.itertuples():
            b, pid = r.bucket, r.rusher_id
            car = vol["runs"] * rmix.get(b, 0) * r.share
            e = reff_p.loc[(pid, b)] if (pid, b) in reff_p.index else None
            ypc = e["ypp_s"] if e is not None else reff[b]["ypp"]
            x = row(pid)
            x["carries"] = x.get("carries", 0) + car
            x["rush_yds"] = x.get("rush_yds", 0) + car * ypc * reff[b]["m_ypp"]
        for pid, x in rows.items():
            if pid in rtd.index:
                rate = shrink(rtd.loc[pid, "td"] / rtd.loc[pid, "n"], rtd.loc[pid, "n"], self.lg_run_td, 80)
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
            x["pass_td"] = vol["pass_att"] * shrink(tp_td, n, self.lg_pass_td, 150) * m_pass_td
            x["interceptions"] = vol["pass_att"] * shrink(tp_int, n, self.lg_int, 200) * m_int
            sc = self.p[(self.p["offense"] == team) & (self.p["play_type"] == "scramble")]
            sc_ypc = sc["yards"].mean() if len(sc) else 6.0
            x["carries"] = x.get("carries", 0) + vol["scrambles"]
            x["rush_yds"] = x.get("rush_yds", 0) + vol["scrambles"] * sc_ypc
            x["sacks"] = vol["sacks"]

        out = pd.DataFrame(rows.values())
        context = {"team": team, "opp": opp, "volume": vol, "pass_mix": pmix, "run_mix": rmix,
                   "pass_signal": psig, "run_signal": rsig, "pass_eff": peff, "run_eff": reff,
                   "qb": names.get(qb, qb) if qb else None,
                   "scheme_notes": self.scheme_effect(team, opp)["notes"] + cb_notes,
                   "adjust": self.adjustments(team, opp, week) if self._market_on else None}
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
