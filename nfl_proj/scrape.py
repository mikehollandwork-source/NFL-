"""Polite HTML downloader for Pro-Football-Reference.

Only downloads and caches raw HTML; parsing happens in ``parse_pfr``. Sports
Reference blocks clients that exceed ~20 requests/minute for up to a day, so
every request waits ``delay`` seconds (default 4) and a 429 stops the run
instead of retrying into a longer ban.
"""

from __future__ import annotations

import random
import time
from pathlib import Path

import requests

BASE = "https://www.pro-football-reference.com"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


class RateLimited(RuntimeError):
    pass


class Fetcher:
    def __init__(self, cache_dir: Path, delay: float = 4.0):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.delay = delay
        self.session = requests.Session()
        self.session.headers["User-Agent"] = USER_AGENT
        self._last = 0.0

    def cache_path(self, path: str) -> Path:
        return self.cache_dir / path.strip("/").replace("/", "__")

    def get(self, path: str, refresh: bool = False) -> str:
        """Return HTML for ``path`` (e.g. ``/years/2026/games.htm``)."""
        cached = self.cache_path(path)
        if cached.exists() and not refresh:
            return cached.read_text(encoding="utf-8")

        wait = self.delay + random.uniform(0, 1.0) - (time.monotonic() - self._last)
        if wait > 0:
            time.sleep(wait)
        resp = self.session.get(BASE + path, timeout=30)
        self._last = time.monotonic()
        if resp.status_code == 429:
            raise RateLimited(
                "PFR returned 429 (rate limited). Stop and retry later; "
                "continuing can extend the block to 24h."
            )
        resp.raise_for_status()
        cached.write_text(resp.text, encoding="utf-8")
        return resp.text


def scrape_season(season: int, cache_dir: Path, delay: float = 4.0,
                  refresh_schedule: bool = True, log=print) -> list[str]:
    """Download the schedule, every completed box score, and the team
    defense page. Returns the list of boxscore ids that are cached."""
    from .parse_pfr import parse_schedule

    fetcher = Fetcher(cache_dir, delay=delay)
    schedule_html = fetcher.get(f"/years/{season}/games.htm", refresh=refresh_schedule)
    games = parse_schedule(schedule_html, season)
    done = [g for g in games if g["boxscore_id"]]
    log(f"{len(games)} games on schedule, {len(done)} completed")

    for i, g in enumerate(done, 1):
        path = f"/boxscores/{g['boxscore_id']}.htm"
        was_cached = fetcher.cache_path(path).exists()
        fetcher.get(path)
        if not was_cached:
            log(f"[{i}/{len(done)}] downloaded {g['boxscore_id']}")

    # Team defense page (includes the advanced defense table with blitz and
    # pressure counts). Refreshed every run because it changes weekly.
    try:
        fetcher.get(f"/years/{season}/opp.htm", refresh=True)
    except requests.HTTPError as exc:
        log(f"warning: could not fetch team defense page: {exc}")
    return [g["boxscore_id"] for g in done]
