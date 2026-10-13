"""Defensive scheme data from outside the play-by-play.

Play-by-play doesn't record coverage shells or blitzes, so these come from
charting sites. Two inputs, merged with this priority:
  1. data/manual/defense_tags.csv   your own tags (always win)
  2. data/external/defense_scheme.csv   online numbers, each row with source,
     date and confidence. Seeded by hand from search results; `python -m
     nfl_proj external` refreshes it from Sharp Football Analysis when that
     domain is reachable.

Only these externally sourced labels feed the projection's scheme
adjustment. Labels derived from the play-by-play itself are report-only,
because the defense's own stats already carry that information.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

from .scrape import USER_AGENT
from .teams import ALL_TEAMS

SHARP_PAGES = {
    "tendencies": "https://www.sharpfootballanalysis.com/stats-nfl/nfl-defensive-tendencies/",
    "coverage": "https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/",
}

TEAM_NAMES = {
    "Cardinals": "ARI", "Falcons": "ATL", "Ravens": "BAL", "Bills": "BUF", "Panthers": "CAR",
    "Bears": "CHI", "Bengals": "CIN", "Browns": "CLE", "Cowboys": "DAL", "Broncos": "DEN",
    "Lions": "DET", "Packers": "GNB", "Texans": "HOU", "Colts": "IND", "Jaguars": "JAX",
    "Chiefs": "KAN", "Raiders": "LVR", "Chargers": "LAC", "Rams": "LAR", "Dolphins": "MIA",
    "Vikings": "MIN", "Patriots": "NWE", "Saints": "NOR", "Giants": "NYG", "Jets": "NYJ",
    "Eagles": "PHI", "Steelers": "PIT", "49ers": "SFO", "Seahawks": "SEA", "Buccaneers": "TAM",
    "Titans": "TEN", "Commanders": "WAS",
}

COLUMN_PATTERNS = {
    "blitz_rate": r"blitz", "man_rate": r"\bman\b", "zone_rate": r"zone",
    "cover0": r"cover\s*0", "cover1": r"cover\s*1", "cover2": r"cover\s*2(?!\s*man)",
    "cover3": r"cover\s*3", "cover4": r"cover\s*4|quarters", "cover6": r"cover\s*6",
}
SCHEME_COLS = list(COLUMN_PATTERNS)


def team_from_text(s: str) -> str | None:
    for name, abbr in TEAM_NAMES.items():
        if name.lower() in s.lower():
            return abbr
    return None


def parse_scheme_tables(html: str) -> pd.DataFrame:
    """Pull any table whose rows are NFL teams and whose headers match scheme
    columns (blitz %, man %, zone %, Cover N %)."""
    soup = BeautifulSoup(html, "lxml")
    frames = []
    for t in soup.find_all("table"):
        headers = [th.get_text(" ", strip=True).lower() for th in t.find_all("th")]
        col_map = {}
        for i, h in enumerate(headers):
            for key, pat in COLUMN_PATTERNS.items():
                if key not in col_map.values() and re.search(pat, h):
                    col_map[i] = key
                    break
        if not col_map:
            continue
        rows = []
        for tr in t.find_all("tr"):
            cells = [c.get_text(" ", strip=True) for c in tr.find_all(["td", "th"])]
            if not cells:
                continue
            team = team_from_text(cells[0]) or (team_from_text(cells[1]) if len(cells) > 1 else None)
            if not team:
                continue
            row = {"team": team}
            for i, key in col_map.items():
                if i < len(cells):
                    v = re.sub(r"[^\d.\-]", "", cells[i])
                    row[key] = float(v) if v not in ("", "-", ".") else np.nan
            rows.append(row)
        df = pd.DataFrame(rows).drop_duplicates("team") if rows else pd.DataFrame()
        if len(df) >= 20:  # a real league table, not a sidebar
            frames.append(df)
    if not frames:
        return pd.DataFrame()
    out = frames[0]
    for f in frames[1:]:
        out = out.set_index("team").combine_first(f.set_index("team")).reset_index()
    return out


def scrape_sharp(out_path: Path, as_of: str, log=print) -> pd.DataFrame:
    s = requests.Session()
    s.headers["User-Agent"] = USER_AGENT
    frames = []
    for name, url in SHARP_PAGES.items():
        try:
            r = s.get(url, timeout=30)
            r.raise_for_status()
        except requests.RequestException as exc:
            log(f"could not fetch {url}: {exc}")
            continue
        df = parse_scheme_tables(r.text)
        if df.empty:
            log(f"no team table recognised on {url} (layout changed?)")
            continue
        df["source"], df["as_of"], df["confidence"] = url, as_of, "high"
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    new = frames[0].set_index("team")
    for f in frames[1:]:
        new = new.combine_first(f.set_index("team"))
    old = load_external(out_path)
    merged = new.combine_first(old.set_index("team")) if not old.empty else new
    merged = merged.reset_index()
    merged.to_csv(out_path, index=False)
    log(f"updated {out_path}: {merged['team'].nunique()} teams")
    return merged


def load_external(path: Path) -> pd.DataFrame:
    if not Path(path).exists():
        return pd.DataFrame(columns=["team"] + SCHEME_COLS)
    df = pd.read_csv(path)
    for c in SCHEME_COLS:
        if c not in df:
            df[c] = np.nan
    return df


def scheme_labels(external: pd.DataFrame, manual: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Discrete scheme labels per defense from external numbers + your tags.

    blitz:    heavy / light / avg  (rate vs thresholds in config)
    coverage: man_heavy / zone_heavy / avg
    shell:    the most-used Cover N if any shell column is filled
    """
    th = cfg.get("scheme", {})
    hi_b, lo_b = th.get("blitz_heavy_pct", 33.0), th.get("blitz_light_pct", 20.0)
    hi_m, lo_m = th.get("man_heavy_pct", 30.0), th.get("man_light_pct", 18.0)
    rows = []
    ext = external.set_index("team") if not external.empty else pd.DataFrame()
    man = manual.set_index("team") if manual is not None and not manual.empty else pd.DataFrame()
    for team in ALL_TEAMS:
        r = {"team": team, "blitz": "", "coverage": "", "shell": "", "scheme_source": ""}
        if team in ext.index:
            e = ext.loc[team]
            b, m, z = e.get("blitz_rate"), e.get("man_rate"), e.get("zone_rate")
            if pd.notna(b):
                r["blitz"] = "heavy" if b >= hi_b else "light" if b <= lo_b else "avg"
            if pd.isna(m) and pd.notna(z):
                m = 100 - z
            if pd.notna(m):
                r["coverage"] = "man_heavy" if m >= hi_m else "zone_heavy" if m <= lo_m else "avg"
            shells = {c: e.get(c) for c in ("cover0", "cover1", "cover2", "cover3", "cover4", "cover6")
                      if pd.notna(e.get(c))}
            if shells:
                r["shell"] = max(shells, key=shells.get)
            r["scheme_source"] = f"online ({e.get('confidence', '')})"
        if team in man.index:
            mrow = man.loc[team]
            if mrow.get("third_down_blitz", ""):
                r["blitz"] = mrow["third_down_blitz"].lower()
            if mrow.get("base_coverage", ""):
                cov = mrow["base_coverage"].lower().replace(" ", "")
                r["shell"] = cov
                if cov in ("man", "cover1", "cover0"):
                    r["coverage"] = "man_heavy"
            r["scheme_source"] = "your tags"
        rows.append(r)
    return pd.DataFrame(rows)


def compare_with_pbp(labels: pd.DataFrame, auto: pd.DataFrame) -> pd.DataFrame:
    """Cross-check online blitz labels against what the play-by-play shows
    (3rd-down sack rate tercile). Disagreements are worth a look."""
    m = labels.merge(auto[["team", "third_down_pressure"]], on="team", how="left")
    m = m[m["blitz"] != ""]
    m["agrees"] = ((m["blitz"] == "heavy") & (m["third_down_pressure"] == "heavy")) | \
                  ((m["blitz"] == "light") & (m["third_down_pressure"] == "light")) | \
                  (m["blitz"] == "avg")
    m["agrees"] = m["agrees"].where(m["third_down_pressure"].notna(), None)
    return m[["team", "blitz", "third_down_pressure", "agrees", "scheme_source"]]
