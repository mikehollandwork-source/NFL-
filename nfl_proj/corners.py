"""Cornerback matchups: who covers whom, and how well.

Inputs
  coverage       PFR charting per defender per game (targets, yards, TDs allowed)
  depth_db       latest depth chart: LCB / RCB (outside), NB (nickel / slot)
  personnel      data/external/defense_personnel.csv: researched scheme notes and
                 shadow corners, each with sources, date and confidence
  overrides      who is out this week (injury report + your manual file)

A defense's season stats were earned with its usual corners. Two things
change that for a given week, and only these feed the projection:

  1. Missing corners. Each defender's yards allowed per target is shrunk
     toward league average (``corners.shrink_targets``). The group's season
     quality is the target-weighted average of everyone who covered; this
     week's quality replaces the out players' share with a replacement-level
     corner. Wide receivers' yards per target move by this week / season.
  2. Shadow assignments. When the researched file names a shadow corner and
     he is available, the offense's top wide receiver spends
     ``corners.shadow_share`` of his routes against that corner instead of
     the group; the other receivers face the group without him.

Tight ends get ``te_weight`` of the group effect (linebackers and safeties
cover them more); running backs none.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def load_personnel(path: Path) -> pd.DataFrame:
    if not Path(path).exists():
        return pd.DataFrame(columns=["team"])
    return pd.read_csv(path, dtype=str).fillna("")


def _norm(name: str) -> str:
    s = str(name).lower().replace(".", "").replace("'", "")
    for suf in (" jr", " sr", " iii", " ii", " iv"):
        s = s.removesuffix(suf)
    return s.strip()


class Corners:
    def __init__(self, coverage: pd.DataFrame | None, depth_db: pd.DataFrame | None,
                 personnel: pd.DataFrame | None, out_ids: set, out_names: set, cfg: dict):
        c = cfg.get("corners", {})
        self.enabled = c.get("enabled", True) and coverage is not None and not coverage.empty
        self.k = c.get("shrink_targets", 30.0)
        self.repl = c.get("replacement_ypt_mult", 1.08)
        self.shadow_share = c.get("shadow_share", 0.7)
        self.te_weight = c.get("te_weight", 0.5)
        self.clip = (c.get("min_factor", 0.8), c.get("max_factor", 1.2))
        self.depth = depth_db if depth_db is not None else pd.DataFrame(columns=["team", "player_id", "player", "role", "rank"])
        self.personnel = (personnel.set_index("team") if personnel is not None and not personnel.empty
                          else pd.DataFrame())
        self.out_ids, self.out_names = set(out_ids), {_norm(n) for n in out_names}
        if not self.enabled:
            return
        # Defensive backs only: linebackers mostly cover backs and tight ends.
        cov = coverage[coverage["pos"].isin(["CB", "DB", "S", "FS", "SS", "SAF"])].copy()
        g = cov.groupby(["team", "pfr_id"]).agg(player=("player", "last"), player_id=("player_id", "last"),
                                                targets=("targets", "sum"), yards=("yards", "sum"),
                                                td=("td", "sum")).reset_index()
        self.lg_ypt = g["yards"].sum() / max(g["targets"].sum(), 1)
        g["ypt_raw"] = g["yards"] / g["targets"].where(g["targets"] > 0)
        g["ypt"] = (g["yards"] + self.k * self.lg_ypt) / (g["targets"] + self.k)
        self.players = g

    # ------------------------------------------------------------------
    def _is_out(self, pid, name) -> bool:
        return (isinstance(pid, str) and pid in self.out_ids) or _norm(name) in self.out_names

    def group(self, team: str) -> dict:
        """Season vs this-week coverage quality (yards per target allowed)."""
        p = self.players[self.players["team"] == team]
        if p.empty or p["targets"].sum() == 0:
            return {"season": self.lg_ypt, "week": self.lg_ypt, "out": []}
        w = p["targets"]
        season = float((w * p["ypt"]).sum() / w.sum())
        out = p.apply(lambda r: self._is_out(r["player_id"], r["player"]), axis=1)
        week_ypt = np.where(out, self.lg_ypt * self.repl, p["ypt"])
        week = float((w * week_ypt).sum() / w.sum())
        missing = p[out].sort_values("targets", ascending=False)
        return {"season": season, "week": week,
                "out": [(r.player, r.targets, r.ypt) for r in missing.itertuples() if r.targets >= 5]}

    def shadow(self, team: str) -> dict | None:
        """Researched shadow corner for this defense, if he's available."""
        if self.personnel.empty or team not in self.personnel.index:
            return None
        name = self.personnel.at[team, "shadow_cb"]
        if not name:
            return None
        p = self.players[(self.players["team"] == team) & (self.players["player"].map(_norm) == _norm(name))]
        pid = p["player_id"].iloc[0] if len(p) else None
        active = not self._is_out(pid, name)
        ypt = float(p["ypt"].iloc[0]) if len(p) else self.lg_ypt
        return {"player": name, "active": active, "ypt": ypt,
                "targets": float(p["targets"].iloc[0]) if len(p) else 0.0,
                "confidence": self.personnel.at[team, "confidence"]}

    def receiver_factors(self, opp: str, receivers: pd.DataFrame) -> tuple[dict, list[str]]:
        """Yards-per-target multipliers for one offense's receivers facing
        ``opp``. ``receivers``: player_id, player, pos, share (season target share)."""
        if not self.enabled:
            return {}, []
        g = self.group(opp)
        base = g["week"] / g["season"] if g["season"] > 0 else 1.0
        f = {}
        notes = []
        for r in receivers.itertuples():
            pos = str(r.pos).upper()
            if pos == "WR":
                f[r.player_id] = base
            elif pos == "TE":
                f[r.player_id] = 1 + self.te_weight * (base - 1)
        if g["out"]:
            notes.append(f"{opp} DBs out: " + ", ".join(f"{n} ({t:.0f} tgts, {y:.1f} yds/tgt allowed)"
                                                              for n, t, y in g["out"])
                         + f" -> coverage {g['season']:.1f} → {g['week']:.1f} yds/tgt; WR yards x{base:.2f}")
        sh = self.shadow(opp)
        if sh is not None:
            wrs = receivers[receivers["pos"].astype(str).str.upper() == "WR"].sort_values("share", ascending=False)
            if not sh["active"]:
                notes.append(f"{opp} shadow corner {sh['player']} is out: no shadow this week")
            elif len(wrs):
                wr1 = wrs.iloc[0]
                s = self.shadow_share
                # Group quality without the shadow corner for everyone else
                p = self.players[self.players["team"] == opp]
                rest = p[p["player"].map(_norm) != _norm(sh["player"])]
                rest_ypt = float((rest["targets"] * rest["ypt"]).sum() / rest["targets"].sum()) if rest["targets"].sum() else g["week"]
                wr1_f = (s * sh["ypt"] + (1 - s) * rest_ypt) / g["season"]
                f[wr1.player_id] = wr1_f
                for r in wrs.iloc[1:].itertuples():
                    f[r.player_id] = (rest_ypt / g["season"]) if g["season"] > 0 else 1.0
                notes.append(f"{opp} shadows with {sh['player']} ({sh['ypt']:.1f} yds/tgt allowed on "
                             f"{sh['targets']:.0f} targets, source confidence {sh['confidence']}): "
                             f"{wr1.player} yards x{np.clip(wr1_f, *self.clip):.2f}")
        return {k: float(np.clip(v, *self.clip)) for k, v in f.items()}, notes

    def describe(self, team: str) -> str | None:
        """One line for the report: alignment from the depth chart plus researched notes."""
        d = self.depth[self.depth["team"] == team]
        parts = []
        if len(d):
            first = d[d["rank"] == 1]
            outside = [x for x in first[first["role"] == "outside"]["player"]]
            slot = [x for x in first[first["role"] == "slot"]["player"]]
            def tag(n):
                pid = first[first["player"] == n]["player_id"]
                return n + (" (OUT)" if self._is_out(pid.iloc[0] if len(pid) else None, n) else "")
            if outside:
                parts.append("outside " + " / ".join(tag(n) for n in outside))
            if slot:
                parts.append("nickel " + " / ".join(tag(n) for n in slot))
            if not self.personnel.empty and team in self.personnel.index:
                notes = self.personnel.at[team, "scheme_notes"].lower()
                for n in outside:
                    if _norm(n).split()[-1] in notes and "nickel" in notes and _norm(n).split()[-1] in notes.split("nickel")[0]:
                        parts.append(f"note: depth chart lists {n} outside but reporting has him at nickel")
        if not self.personnel.empty and team in self.personnel.index:
            r = self.personnel.loc[team]
            lean = f"{r['coverage_lean']}-leaning" if r["coverage_lean"] not in ("", "unknown") else "coverage lean unknown"
            parts.insert(0, f"DC {r['coordinator']}, {lean}: {r['scheme_notes']}")
            if r["weak_spot"]:
                parts.append(f"weak spot: {r['weak_spot']}")
            parts.append(f"[research confidence {r['confidence']}, {r['as_of']}]")
        return "; ".join(parts) if parts else None
