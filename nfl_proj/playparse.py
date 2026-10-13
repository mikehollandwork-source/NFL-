"""Turn one play-by-play description into structured fields.

Examples of PFR detail text this handles:
  Josh Allen pass complete deep right to Khalil Shakir for 32 yards (tackle by X)
  Jalen Hurts pass incomplete short left intended for A.J. Brown
  Patrick Mahomes pass deep middle intended for Travis Kelce is intercepted by X at KAN 40
  Saquon Barkley left tackle for 5 yards (tackle by X)
  Derrick Henry up the middle for no gain
  Lamar Jackson sacked by X for -7 yards
  Penalty on X: False Start, 5 yards (no play)
"""

from __future__ import annotations

import re

PLAYER_LINK = re.compile(r'<a href="/players/\w/([A-Za-z0-9.\-]+)\.htm"')
TARGET_LINK = re.compile(
    r'(?:\bto|intended for)\s+<a href="/players/\w/([A-Za-z0-9.\-]+)\.htm"')

PASS_RE = re.compile(
    r"\bpass(?:\s+(complete|incomplete))?(?:\s+(short|deep))?(?:\s+(left|middle|right))?", re.I)
RUN_RE = re.compile(
    r"\b(left|right)\s+(end|tackle|guard)\b|\bup the middle\b|\bmiddle for\b", re.I)
YARDS_RE = re.compile(r"\bfor (-?\d+) yards?\b", re.I)

SPECIAL = re.compile(
    r"\bpunts?\b|\bkicks? off\b|\bkickoff\b|\bfield goal\b|\bextra point\b|"
    r"\btwo point attempt\b|\bonside\b", re.I)

RUN_GAP_BUCKET = {
    ("left", "end"): "run_outside_left",
    ("left", "tackle"): "run_inside_left",
    ("left", "guard"): "run_inside_left",
    ("right", "guard"): "run_inside_right",
    ("right", "tackle"): "run_inside_right",
    ("right", "end"): "run_outside_right",
}

PASS_BUCKETS = [f"pass_{d}_{s}" for d in ("short", "deep") for s in ("left", "middle", "right")]
RUN_BUCKETS = ["run_outside_left", "run_inside_left", "run_middle",
               "run_inside_right", "run_outside_right"]
ALL_BUCKETS = PASS_BUCKETS + RUN_BUCKETS


def parse_detail(text: str, html: str = "") -> dict:
    """Classify a play. ``play_type`` is one of pass, run, sack, scramble,
    penalty, special, kneel, spike, timeout, other."""
    t = text.strip()
    low = t.lower()
    ids = PLAYER_LINK.findall(html or "")
    out = {
        "play_type": "other", "bucket": None, "depth": None, "direction": None,
        "yards": None, "complete": None, "interception": False, "fumble": "fumbles" in low,
        "touchdown": "touchdown" in low, "penalty": "penalty" in low,
        "no_play": "(no play)" in low, "shotgun": "shotgun" in low,
        "no_huddle": "no huddle" in low, "passer_id": None, "target_id": None,
        "rusher_id": None, "first_player_id": ids[0] if ids else None,
    }

    m = YARDS_RE.search(t)
    if m:
        out["yards"] = float(m.group(1))
    elif "no gain" in low:
        out["yards"] = 0.0

    if out["no_play"]:
        out["play_type"] = "penalty"
        return out
    if low.startswith("timeout") or "timeout #" in low:
        out["play_type"] = "timeout"
        return out
    if SPECIAL.search(low):
        out["play_type"] = "special"
        return out
    if "kneels" in low:
        out["play_type"] = "kneel"
        return out
    if "spiked" in low:
        out["play_type"] = "spike"
        return out

    if "sacked" in low:
        out["play_type"] = "sack"
        out["passer_id"] = out["first_player_id"]
        if out["yards"] is None:
            out["yards"] = 0.0
        return out

    pm = PASS_RE.search(t)
    if pm and not re.search(r"\baborted\b", low):
        status, depth, direction = (g.lower() if g else None for g in pm.groups())
        out["play_type"] = "pass"
        out["passer_id"] = out["first_player_id"]
        tm = TARGET_LINK.search(html or "")
        out["target_id"] = tm.group(1) if tm else None
        out["interception"] = "intercepted" in low
        out["complete"] = status == "complete"
        if not out["complete"]:
            out["yards"] = 0.0
        out["depth"], out["direction"] = depth, direction
        if depth and direction:
            out["bucket"] = f"pass_{depth}_{direction}"
        return out

    if "scrambles" in low:
        out["play_type"] = "scramble"
        out["rusher_id"] = out["first_player_id"]
        return out

    rm = RUN_RE.search(t)
    if rm or (out["yards"] is not None and not out["penalty"] and ids):
        out["play_type"] = "run"
        out["rusher_id"] = out["first_player_id"]
        if rm and rm.group(1):
            side, gap = rm.group(1).lower(), rm.group(2).lower()
            out["direction"] = side
            out["bucket"] = RUN_GAP_BUCKET[(side, gap)]
        elif rm:
            out["direction"] = "middle"
            out["bucket"] = "run_middle"
        return out

    if out["penalty"]:
        out["play_type"] = "penalty"
    return out


def is_success(down, ytg, yards) -> bool | None:
    """Standard success rate: 40% of yards-to-go on 1st down, 60% on 2nd,
    100% on 3rd/4th."""
    if down is None or ytg is None or yards is None or ytg <= 0:
        return None
    need = {1: 0.4, 2: 0.6}.get(int(down), 1.0) * ytg
    return yards >= need
