"""Defensive weaknesses, struggle weeks and comparable offenses.

Three pieces, all measured from this season's play-by-play:

1. ``position_factor`` — how a defense does against WRs, TEs and RBs
   compared with its overall per-target average (relative to how the league
   splits by position). Only that interaction is used, because the defense's
   overall level is already in the bucket matchup. Shrunk by
   ``defense.shrink_targets``.

2. ``struggle_weeks`` — games where a defense allowed clearly more EPA per
   play than its own norm. Each gets a diagnosis: which play families and
   receiver groups broke down, 3rd-down and red-zone results, how the blitz
   fared, explosive plays, how good the opposing offense was, and which
   regular starters didn't play. When a struggle came with starters missing
   who are available this week, that game's plays count only
   ``defense.absent_game_weight`` toward the defense's allowed rates.

3. ``Comps`` — similar offenses. Offenses are described by structure
   (neutral pass rate, early-down pass rate, deep share, shotgun, no-huddle,
   play action, screens, motion, scrambles, outside-run share, box faced).
   For a matchup, the opposing defense's games against structurally similar
   offenses (kernel-weighted) show how such offenses did against it relative
   to their own norms. Only the part beyond how every offense did against it
   is used (shrunk by ``comps.shrink_games``).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

GROUPS = ("WR", "TE", "RB")


def _pos_map(player_games: pd.DataFrame) -> dict:
    pg = player_games.dropna(subset=["player_id"])
    pg = pg[pg["pos"].astype(str) != ""]
    return pg.groupby("player_id")["pos"].agg(lambda s: s.mode().iloc[0]).to_dict()


def _group(pos: str) -> str | None:
    pos = str(pos).upper()
    if pos in ("WR",):
        return "WR"
    if pos in ("TE",):
        return "TE"
    if pos in ("RB", "FB", "HB"):
        return "RB"
    return None


class DefenseAnalysis:
    def __init__(self, plays: pd.DataFrame, player_games: pd.DataFrame, def_snaps: pd.DataFrame | None,
                 cfg: dict, available_ids: set | None = None, available_names: set | None = None,
                 out_names: set | None = None):
        c = cfg.get("defense", {})
        self.k_t = c.get("shrink_targets", 40.0)
        self.dw = cfg["matchup"]["defense_weight"]
        self.absent_w = c.get("absent_game_weight", 0.5)
        self.struggle_epa = c.get("struggle_epa", 0.12)
        self.clip = (c.get("min_factor", 0.8), c.get("max_factor", 1.25))
        self.p = plays[~plays["garbage"]].copy()
        pos = _pos_map(player_games)
        self.p["tgt_group"] = self.p["target_id"].map(pos).map(_group)
        self.snaps = def_snaps if def_snaps is not None else pd.DataFrame()
        self.out_names = {str(n).lower() for n in (out_names or set())}
        self._pos = self._position_table()
        self.struggles = self._struggle_weeks()
        self.game_weight = self._game_weights()

    # ------------------------------------------------------------ positions
    def _position_table(self) -> pd.DataFrame:
        tg = self.p[self.p["is_pass"] & self.p["tgt_group"].notna()]
        lg_all = tg["yards"].mean()
        lg = tg.groupby("tgt_group")["yards"].mean()
        rows = []
        for d, g in tg.groupby("defense"):
            d_all = g["yards"].mean()
            for grp, gg in g.groupby("tgt_group"):
                inter = (gg["yards"].mean() / d_all) / (lg[grp] / lg_all) if d_all > 0 and lg[grp] > 0 else 1.0
                n = len(gg)
                shrunk = (n * inter + self.k_t) / (n + self.k_t)
                rows.append({"defense": d, "group": grp, "targets": n, "ypt": gg["yards"].mean(),
                             "lg_ypt": lg[grp], "factor": float(np.clip(1 + self.dw * (shrunk - 1), *self.clip))})
        return pd.DataFrame(rows)

    def position_factor(self, defense: str, pos: str) -> float:
        grp = _group(pos)
        if grp is None or self._pos.empty:
            return 1.0
        r = self._pos[(self._pos["defense"] == defense) & (self._pos["group"] == grp)]
        return float(r["factor"].iloc[0]) if len(r) else 1.0

    # ------------------------------------------------------------ struggles
    def _starters(self, team: str) -> pd.DataFrame:
        s = self.snaps[self.snaps["team"] == team] if not self.snaps.empty else pd.DataFrame()
        if s.empty:
            return s
        n_games = s["boxscore_id"].nunique()
        reg = s[s["pct"] >= 0.6].groupby(["pfr_id", "player", "pos"]).size().reset_index(name="games")
        return reg[reg["games"] >= max(2, int(np.ceil(0.5 * n_games)))]

    def _struggle_weeks(self) -> pd.DataFrame:
        p = self.p
        scrim = p[p["play_type"].isin(["pass", "run", "sack", "scramble"])]
        g = scrim.groupby(["defense", "boxscore_id", "week", "offense"])["epa"].mean().reset_index(name="epa")
        lg_epa = scrim["epa"].mean()
        # How good each opposing offense was in its other games
        off_game = scrim.groupby(["offense", "boxscore_id"])["epa"].agg(["sum", "size"])
        off_tot = off_game.groupby(level=0).sum()
        rows = []
        for d, gd in g.groupby("defense"):
            if len(gd) < 3:
                continue
            for r in gd.itertuples():
                others = gd[gd["boxscore_id"] != r.boxscore_id]["epa"].mean()
                if r.epa - others < self.struggle_epa or r.epa < lg_epa:
                    continue
                rows.append({"defense": d, "week": r.week, "opp": r.offense, "boxscore_id": r.boxscore_id,
                             "epa_allowed": r.epa, "norm": others,
                             "why": self._diagnose(d, r.boxscore_id, r.offense, off_game, off_tot, lg_epa)})
        return pd.DataFrame(rows)

    def _diagnose(self, d, box, opp, off_game, off_tot, lg_epa) -> dict:
        p = self.p
        dg = p[p["defense"] == d]
        this, rest = dg[dg["boxscore_id"] == box], dg[dg["boxscore_id"] != box]
        causes = []

        def cmp(mask_fn, label, unit="yds/play", col="yards", min_n=4, thr=1.5):
            a, b = this[mask_fn(this)], rest[mask_fn(rest)]
            if len(a) >= min_n and len(b) >= min_n:
                diff = a[col].mean() - b[col].mean()
                if diff >= thr:
                    causes.append((diff / max(abs(b[col].mean()), 1), f"{label} {a[col].mean():.1f} {unit} "
                                                                       f"vs {b[col].mean():.1f} in other games"))

        cmp(lambda x: x["is_pass"] & x["deep"], "deep passes", thr=3.0)
        cmp(lambda x: x["is_pass"] & (x["depth"] == "short"), "short passes", thr=1.2)
        cmp(lambda x: x["is_run"] & x["bucket"].fillna("").str.contains("outside"), "outside runs", thr=1.2)
        cmp(lambda x: x["is_run"] & ~x["bucket"].fillna("").str.contains("outside"), "inside runs", thr=1.0)
        for grp in GROUPS:
            cmp(lambda x, g=grp: x["is_pass"] & (x["tgt_group"] == g), f"{grp}s", unit="yds/target", thr=2.0)
        if "is_blitz" in p and p["is_blitz"].notna().any():
            cmp(lambda x: x["dropback"] & (x["is_blitz"] == 1), "when blitzing", unit="yds/dropback", thr=2.0)
        if "play_action" in p and p["play_action"].notna().any():
            cmp(lambda x: x["dropback"] & (x["play_action"] == True), "vs play action",  # noqa: E712
                unit="yds/dropback", thr=2.0)
        th = lambda x: x["third"]  # noqa: E731
        a, b = this[th(this)], rest[th(rest)]
        if len(a) >= 5 and len(b) >= 5 and a["converted"].mean() - b["converted"].mean() >= 0.15:
            causes.append((a["converted"].mean() - b["converted"].mean(),
                           f"3rd/4th downs converted {a['converted'].mean():.0%} vs {b['converted'].mean():.0%}"))
        rz = lambda x: x["redzone"]  # noqa: E731
        a, b = this[rz(this)], rest[rz(rest)]
        if len(a) >= 4 and len(b) >= 4 and a["touchdown"].mean() - b["touchdown"].mean() >= 0.1:
            causes.append((a["touchdown"].mean() - b["touchdown"].mean(),
                           f"red-zone TD rate per play {a['touchdown'].mean():.0%} vs {b['touchdown'].mean():.0%}"))
        exp_this = this["explosive"].sum()
        exp_rest = rest.groupby("boxscore_id")["explosive"].sum().mean() if len(rest) else 0
        if exp_this - exp_rest >= 3:
            causes.append(((exp_this - exp_rest) / 10, f"{exp_this} explosive plays vs {exp_rest:.1f} per other game"))
        # Opponent quality outside this game
        opp_note = None
        if opp in off_tot.index:
            s, n = off_tot.loc[opp]
            if (opp, box) in off_game.index:
                s -= off_game.loc[(opp, box), "sum"]
                n -= off_game.loc[(opp, box), "size"]
            if n > 20:
                o_epa = s / n
                if o_epa - lg_epa >= 0.08:
                    opp_note = f"{opp} is a strong offense ({o_epa:+.2f} EPA/play in its other games)"
                    causes.append((o_epa - lg_epa, opp_note))
        # Regular starters who didn't play
        absent = []
        st = self._starters(d)
        if not st.empty and not self.snaps.empty:
            played = set(self.snaps[(self.snaps["team"] == d) & (self.snaps["boxscore_id"] == box)]["pfr_id"])
            for r in st.itertuples():
                if r.pfr_id not in played:
                    absent.append({"player": r.player, "pos": r.pos})
            if absent:
                causes.append((0.5 * len(absent), "missing starters: " +
                               ", ".join(f"{a['player']} ({a['pos']})" for a in absent)))
        causes.sort(key=lambda x: -x[0])
        return {"causes": [c[1] for c in causes[:5]], "absent": absent, "strong_opp": opp_note is not None}

    def _game_weights(self) -> dict:
        """(defense, boxscore_id) -> weight for the defense's allowed rates.
        A struggle with starters missing who are available this week counts less."""
        w = {}
        if self.struggles.empty:
            return w
        for r in self.struggles.itertuples():
            absent = r.why["absent"]
            back = [a for a in absent if a["player"].lower() not in self.out_names]
            if back:
                w[(r.defense, r.boxscore_id)] = self.absent_w
        return w

    def describe_struggles(self, defense: str) -> list[str]:
        if self.struggles.empty:
            return []
        out = []
        for r in self.struggles[self.struggles["defense"] == defense].itertuples():
            wt = self.game_weight.get((r.defense, r.boxscore_id))
            tail = f" → counted at {wt:.0%} weight (those starters are available now)" if wt else ""
            out.append(f"Wk{r.week} vs {r.opp}: {r.epa_allowed:+.2f} EPA/play allowed (norm {r.norm:+.2f}). Why: "
                       + ("; ".join(r.why["causes"]) or "no single cause stands out") + tail)
        return out

    def weaknesses(self, defense: str, lg: dict | None = None) -> list[str]:
        """Persistent weak spots (shrunk), strongest first."""
        p = self.p
        dg = p[p["defense"] == defense]
        notes = []
        if not self._pos.empty:
            for r in self._pos[self._pos["defense"] == defense].itertuples():
                if r.factor >= 1.06 and r.targets >= 12:
                    notes.append((r.factor - 1, f"vs {r.group}s: {r.ypt:.1f} yds/target (league {r.lg_ypt:.1f}), "
                                                f"x{r.factor:.2f} for {r.group}s"))
        checks = [
            ("deep passes", lambda x: x["is_pass"] & x["deep"], "yards", 15),
            ("short passes", lambda x: x["is_pass"] & (x["depth"] == "short"), "yards", 40),
            ("outside runs", lambda x: x["is_run"] & x["bucket"].fillna("").str.contains("outside"), "yards", 15),
            ("inside runs", lambda x: x["is_run"] & ~x["bucket"].fillna("").str.contains("outside"), "yards", 30),
            ("3rd-down conversions", lambda x: x["third"], "converted", 20),
            ("red-zone TDs per play", lambda x: x["redzone"], "touchdown", 20),
            ("explosive plays", lambda x: x["play_type"].isin(["pass", "run"]), "explosive", 100),
        ]
        if "play_action" in p and p["play_action"].notna().any():
            checks.append(("play-action dropbacks", lambda x: x["dropback"] & (x["play_action"] == True),  # noqa: E712
                           "yards", 15))
        for label, fn, col, min_n in checks:
            a, lgs = dg[fn(dg)], p[fn(p)]
            if len(a) < min_n or len(lgs) == 0:
                continue
            v, l = a[col].astype(float).mean(), lgs[col].astype(float).mean()
            n = len(a)
            ratio = ((n * v + 30 * l) / (n + 30)) / l if l else 1
            if ratio >= 1.08:
                fmt = (lambda z: f"{z:.0%}") if col in ("converted", "touchdown", "explosive") else (lambda z: f"{z:.1f}")
                notes.append((ratio - 1, f"{label}: {fmt(v)} allowed vs league {fmt(l)} ({n} plays)"))
        notes.sort(key=lambda x: -x[0])
        return [n[1] for n in notes[:5]]


# --------------------------------------------------------------------------
# Comparable offenses
# --------------------------------------------------------------------------

FEATURES = ["neutral_pass", "early_pass", "deep_share", "shotgun", "no_huddle", "play_action",
            "screen", "motion", "scramble", "outside_run", "box"]


def offense_features(p: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for t, g in p.groupby("offense"):
        db, runs, passes = g[g["dropback"]], g[g["is_run"]], g[g["is_pass"]]
        rows.append({
            "team": t,
            "neutral_pass": g[g["neutral"]]["dropback"].mean(),
            "early_pass": g[g["early"]]["dropback"].mean(),
            "deep_share": passes["deep"].mean(),
            "shotgun": g["shotgun"].astype(float).mean(),
            "no_huddle": g["no_huddle"].astype(float).mean(),
            "play_action": db["play_action"].astype(float).mean() if "play_action" in g else np.nan,
            "screen": passes["screen"].astype(float).mean() if "screen" in g else np.nan,
            "motion": g["motion"].astype(float).mean() if "motion" in g else np.nan,
            "scramble": (db["play_type"] == "scramble").mean(),
            "outside_run": runs["bucket"].fillna("").str.contains("outside").mean(),
            "box": runs["box"].astype(float).mean() if "box" in g else np.nan,
        })
    f = pd.DataFrame(rows).set_index("team")
    return f[[c for c in FEATURES if f[c].notna().sum() > len(f) / 2]]


class Comps:
    def __init__(self, plays: pd.DataFrame, cfg: dict):
        c = cfg.get("comps", {})
        self.enabled = c.get("enabled", True)
        self.k = c.get("shrink_games", 2.0)
        self.dw = cfg["matchup"]["defense_weight"]
        self.clip = (c.get("min_factor", 0.88), c.get("max_factor", 1.12))
        p = plays[~plays["garbage"]]
        f = offense_features(p)
        z = (f - f.mean()) / f.std(ddof=0).replace(0, 1)
        z = z.fillna(0)
        dist = np.sqrt(((z.values[:, None, :] - z.values[None, :, :]) ** 2).sum(-1))
        bw = np.median(dist[np.triu_indices(len(z), 1)]) * c.get("bandwidth", 0.6) if len(z) > 2 else 1.0
        self.sim = pd.DataFrame(np.exp(-(dist / bw) ** 2), index=z.index, columns=z.index)
        self.features = f
        # Per offense-game performance relative to that offense's other games
        drop = p[p["dropback"]].groupby(["offense", "defense", "boxscore_id"])["yards"].mean().rename("pass")
        run = p[p["is_run"]].groupby(["offense", "defense", "boxscore_id"])["yards"].mean().rename("run")
        g = pd.concat([drop, run], axis=1).reset_index()
        for col in ("pass", "run"):
            tot = g.groupby("offense")[col].transform("sum")
            cnt = g.groupby("offense")[col].transform("count")
            g[f"{col}_res"] = g[col] - (tot - g[col]) / (cnt - 1).replace(0, np.nan)
        self.games = g
        self.lg = {"pass": p[p["dropback"]]["yards"].mean(), "run": p[p["is_run"]]["yards"].mean()}

    def effect(self, team: str, opp: str) -> dict:
        """Pass / run yards-per-play multipliers and the comparable games used."""
        out = {"pass": 1.0, "run": 1.0, "comps": []}
        if not self.enabled or team not in self.sim.index:
            return out
        g = self.games[(self.games["defense"] == opp) & (self.games["offense"] != team)]
        if g.empty:
            return out
        w = g["offense"].map(self.sim[team]).fillna(0.0)
        for col in ("pass", "run"):
            r = g[f"{col}_res"]
            m = r.notna()
            if not m.any():
                continue
            base = r[m].mean()  # how every offense did vs this defense
            inter = float((w[m] * (r[m] - base)).sum() / (w[m].sum() + self.k))
            out[col] = float(np.clip(1 + self.dw * inter / self.lg[col], *self.clip))
        top = g.assign(sim=w).sort_values("sim", ascending=False).head(3)
        out["comps"] = [(r.offense, float(r.sim), r.pass_res, r.run_res) for r in top.itertuples()]
        return out

    def most_similar(self, team: str, n: int = 3) -> list[tuple[str, float]]:
        if team not in self.sim.index:
            return []
        s = self.sim[team].drop(team).sort_values(ascending=False).head(n)
        return list(s.items())
