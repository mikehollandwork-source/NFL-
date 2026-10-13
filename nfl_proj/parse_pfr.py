"""Parse cached Pro-Football-Reference HTML into plain Python rows.

PFR hides most box score tables inside HTML comments (they are rendered
client-side), so every table lookup also searches comment blocks.
"""

from __future__ import annotations

import re

from bs4 import BeautifulSoup, Comment

from .teams import FRANCHISE_TO_ABBR, abbr_from_href

PLAYER_HREF = re.compile(r"/players/\w/([A-Za-z0-9.\-]+)\.htm")
BOX_HREF = re.compile(r"/boxscores/(\w+)\.htm")


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "lxml")


def all_tables(html: str) -> dict[str, "BeautifulSoup"]:
    """Every ``<table id=...>`` in the page, including commented-out ones."""
    soup = _soup(html)
    tables = {t["id"]: t for t in soup.find_all("table", id=True)}
    for c in soup.find_all(string=lambda s: isinstance(s, Comment)):
        if "<table" in c:
            for t in _soup(str(c)).find_all("table", id=True):
                tables.setdefault(t["id"], t)
    return tables


def table_rows(table) -> list[dict]:
    """Rows of a PFR stats table as ``{data-stat: cell}`` dicts, skipping
    repeated header rows. Each cell maps to its BeautifulSoup tag."""
    body = table.find("tbody") or table
    out = []
    for tr in body.find_all("tr", recursive=False):
        classes = tr.get("class") or []
        if "thead" in classes or "over_header" in classes:
            continue
        cells = {c.get("data-stat"): c for c in tr.find_all(["th", "td"], recursive=False)
                 if c.get("data-stat")}
        if cells:
            cells["_classes"] = classes
            out.append(cells)
    return out


def _text(cell) -> str:
    return cell.get_text(" ", strip=True) if cell is not None else ""


def _num(cell) -> float | None:
    t = _text(cell).replace(",", "").replace("%", "")
    try:
        return float(t)
    except ValueError:
        return None


def _player_id(cell) -> str | None:
    if cell is None:
        return None
    if cell.get("data-append-csv"):
        return cell["data-append-csv"]
    a = cell.find("a", href=PLAYER_HREF)
    return PLAYER_HREF.search(a["href"]).group(1) if a else None


# --------------------------------------------------------------------------
# Schedule
# --------------------------------------------------------------------------

def parse_schedule(html: str, season: int) -> list[dict]:
    tables = all_tables(html)
    table = tables.get("games")
    if table is None:
        raise ValueError("schedule page has no table#games — PFR layout changed?")
    games = []
    for r in table_rows(table):
        wk = _text(r.get("week_num"))
        if not wk.isdigit():
            continue  # playoff rows / blanks
        box_cell = r.get("boxscore_word")
        link = box_cell.find("a", href=BOX_HREF) if box_cell else None
        played = bool(link) and _text(box_cell).lower() == "boxscore"

        if "home_team" in r and "visitor_team" in r:
            away_cell, home_cell = r["visitor_team"], r["home_team"]
        else:
            # Winner/Loser layout. '@' means the winner (first team) was away.
            first, second = r.get("winner"), r.get("loser")
            if _text(r.get("game_location")) == "@":
                away_cell, home_cell = first, second
            else:
                away_cell, home_cell = second, first

        def team(cell):
            a = cell.find("a", href=True) if cell else None
            return abbr_from_href(a["href"]) if a else None

        away, home = team(away_cell), team(home_cell)
        box_id = BOX_HREF.search(link["href"]).group(1) if played else None
        if box_id:
            # Boxscore id suffix is the home franchise code: trust it.
            home_code = box_id[-3:]
            if home_code in FRANCHISE_TO_ABBR and FRANCHISE_TO_ABBR[home_code] != home:
                away, home = home, FRANCHISE_TO_ABBR[home_code]
        games.append({
            "season": season,
            "week": int(wk),
            "date": _text(r.get("game_date")),
            "away": away,
            "home": home,
            "boxscore_id": box_id,
            "neutral": _text(r.get("game_location")) == "N",
        })
    return games


# --------------------------------------------------------------------------
# Box score
# --------------------------------------------------------------------------

PLAYER_OFFENSE_STATS = [
    "pass_cmp", "pass_att", "pass_yds", "pass_td", "pass_int", "pass_sacked",
    "pass_sacked_yds", "pass_long", "rush_att", "rush_yds", "rush_td",
    "rush_long", "targets", "rec", "rec_yds", "rec_td", "rec_long",
    "fumbles", "fumbles_lost",
]


def parse_player_offense(tables) -> list[dict]:
    t = tables.get("player_offense")
    if t is None:
        return []
    rows = []
    for r in table_rows(t):
        pid = _player_id(r.get("player"))
        if not pid:
            continue
        row = {"player_id": pid, "player": _text(r.get("player")),
               "team": _text(r.get("team"))}
        for s in PLAYER_OFFENSE_STATS:
            row[s] = _num(r.get(s)) or 0.0
        rows.append(row)
    return rows


def parse_snap_counts(tables, home: str, away: str) -> list[dict]:
    rows = []
    for tid, team in (("home_snap_counts", home), ("vis_snap_counts", away)):
        t = tables.get(tid)
        if t is None:
            continue
        for r in table_rows(t):
            pid = _player_id(r.get("player"))
            if not pid:
                continue
            rows.append({
                "player_id": pid, "player": _text(r.get("player")), "team": team,
                "pos": _text(r.get("pos")),
                "off_snaps": _num(r.get("offense")) or 0.0,
                "off_pct": _num(r.get("off_pct")) or 0.0,
                "def_snaps": _num(r.get("defense")) or 0.0,
            })
    return rows


def parse_game_info(tables) -> dict:
    t = tables.get("game_info")
    info = {}
    if t is None:
        return info
    for tr in t.find_all("tr"):
        th, td = tr.find("th"), tr.find("td")
        if th and td:
            info[_text(th).lower()] = _text(td)
    return info


def parse_pbp(tables) -> list[dict]:
    """Raw play-by-play rows. ``detail_html`` keeps the player links so the
    play parser can identify passer / receiver / rusher by player id."""
    t = tables.get("pbp")
    if t is None:
        return []
    plays = []
    for idx, r in enumerate(table_rows(t)):
        detail = r.get("detail")
        if detail is None:
            continue
        q = _text(r.get("quarter"))
        plays.append({
            "seq": idx,
            "quarter": int(q) if q.isdigit() else (5 if q.upper() == "OT" else None),
            "clock": _text(r.get("qtr_time_remain")),
            "down": int(_num(r.get("down"))) if _num(r.get("down")) else None,
            "ytg": _num(r.get("yds_to_go")),
            "location": _text(r.get("location")),
            "score_away": _num(r.get("pbp_score_aw")),
            "score_home": _num(r.get("pbp_score_hm")),
            "detail": _text(detail),
            "detail_html": detail.decode_contents(),
            "ep_before": _num(r.get("exp_pts_before")),
            "ep_after": _num(r.get("exp_pts_after")),
            "row_class": " ".join(r.get("_classes", [])),
        })
    return plays


def parse_boxscore(html: str, box_id: str, game: dict) -> dict:
    tables = all_tables(html)
    home, away = game["home"], game["away"]
    return {
        "player_offense": parse_player_offense(tables),
        "snaps": parse_snap_counts(tables, home, away),
        "pbp": parse_pbp(tables),
        "info": parse_game_info(tables),
    }


# --------------------------------------------------------------------------
# Team defense page (/years/YYYY/opp.htm)
# --------------------------------------------------------------------------

def parse_team_defense(html: str) -> list[dict]:
    """Return rows from the advanced defense table (blitz / pressure counts).

    The table id is matched loosely because PFR has renamed it before: any
    table with a column whose data-stat mentions blitz is used.
    """
    tables = all_tables(html)
    candidates = [tables[k] for k in ("advanced_defense", "team_advanced_defense") if k in tables]
    if not candidates:
        candidates = [t for t in tables.values()
                      if t.find(attrs={"data-stat": re.compile("blitz|bltz", re.I)})]
    if not candidates:
        return []
    out = []
    for r in table_rows(candidates[0]):
        team_cell = r.get("team") or r.get("team_name")
        a = team_cell.find("a", href=True) if team_cell else None
        abbr = abbr_from_href(a["href"]) if a else None
        if not abbr:
            continue
        row = {"team": abbr}
        for k, cell in r.items():
            if k in ("team", "team_name", "_classes", "ranker"):
                continue
            v = _num(cell)
            if v is not None:
                row[k] = v
        out.append(row)
    return out
