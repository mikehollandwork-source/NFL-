"""Team code mappings used by Pro-Football-Reference.

PFR uses two code sets: lowercase franchise codes in URLs and boxscore ids
(e.g. ``/boxscores/202609130rav.htm``) and uppercase abbreviations in tables
and play-by-play field locations (e.g. ``BAL 35``).
"""

FRANCHISE_TO_ABBR = {
    "crd": "ARI", "atl": "ATL", "rav": "BAL", "buf": "BUF", "car": "CAR",
    "chi": "CHI", "cin": "CIN", "cle": "CLE", "dal": "DAL", "den": "DEN",
    "det": "DET", "gnb": "GNB", "htx": "HOU", "clt": "IND", "jax": "JAX",
    "kan": "KAN", "rai": "LVR", "sdg": "LAC", "ram": "LAR", "mia": "MIA",
    "min": "MIN", "nwe": "NWE", "nor": "NOR", "nyg": "NYG", "nyj": "NYJ",
    "phi": "PHI", "pit": "PIT", "sfo": "SFO", "sea": "SEA", "tam": "TAM",
    "oti": "TEN", "was": "WAS",
}

ABBR_TO_FRANCHISE = {v: k for k, v in FRANCHISE_TO_ABBR.items()}

ALL_TEAMS = sorted(FRANCHISE_TO_ABBR.values())


def franchise_from_href(href: str) -> str | None:
    """``/teams/kan/2026.htm`` -> ``kan``."""
    parts = [p for p in href.split("/") if p]
    if len(parts) >= 2 and parts[0] == "teams":
        return parts[1]
    return None


def abbr_from_href(href: str) -> str | None:
    code = franchise_from_href(href)
    return FRANCHISE_TO_ABBR.get(code) if code else None
