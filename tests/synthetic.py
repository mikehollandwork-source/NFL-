"""Synthetic PFR-format pages for end-to-end tests.

These are generated, not real games: they exist only to exercise the full
scrape-cache -> build -> profile -> project path without network access.
Markup mirrors PFR (tables hidden in HTML comments, data-stat attributes).
"""

from __future__ import annotations

import random
from pathlib import Path

from nfl_proj.scrape import Fetcher
from nfl_proj.teams import ABBR_TO_FRANCHISE

TEAMS = ["KAN", "BUF", "PHI", "DAL"]
ROSTER = {"QB": "QB", "RB": "RB", "WR1": "WR", "WR2": "WR", "TE": "TE"}
SCHEDULE = [  # (week, away, home)
    (1, "KAN", "BUF"), (1, "PHI", "DAL"),
    (2, "BUF", "PHI"), (2, "DAL", "KAN"),
    (3, "KAN", "PHI"), (3, "BUF", "DAL"),
    (4, "BUF", "KAN"), (4, "DAL", "PHI"),
    (5, "PHI", "BUF"), (5, "KAN", "DAL"),
    (6, "PHI", "KAN"), (6, "DAL", "BUF"),
    (7, "BUF", "DAL"), (7, "KAN", "PHI"),  # unplayed
]
PLAYED_THROUGH = 6


def pid(team, slot):
    return f"{team.title()}{slot.title()}00"


def plink(team, slot):
    p = pid(team, slot)
    return f'<a href="/players/{p[0]}/{p}.htm">{team} {slot}</a>'


def tlink(team):
    return f'<a href="/teams/{ABBR_TO_FRANCHISE[team]}/2026.htm">{team}</a>'


def box_id(week, home):
    return f"202609{week:02d}0{ABBR_TO_FRANCHISE[home]}"


def dlink(team, n):
    p = f"{team.title()}Lb{n:02d}"
    return f'<a href="/players/{p[0]}/{p}.htm">{team} LB{n}</a>'


def tackle(rng, dfn):
    a = dlink(dfn, rng.choice([1, 1, 2, 3]))
    if rng.random() < 0.3:
        return f" (tackle by {a} and {dlink(dfn, 4)})"
    return f" (tackle by {a})"


def gen_drive_plays(rng, off, dfn, n):
    """Yield (text, html, yards, stats) tuples for n offensive plays."""
    soft_deep = dfn == "DAL"
    for _ in range(n):
        r = rng.random()
        if r < 0.55:
            depth = "deep" if rng.random() < 0.18 else "short"
            side = rng.choice(["left", "middle", "right"])
            slot = rng.choice(["WR1", "WR1", "WR2", "TE", "RB"])
            p_cmp = 0.5 if depth == "deep" else 0.68
            if soft_deep and depth == "deep":
                p_cmp = 0.7
            if rng.random() < p_cmp:
                y = rng.randint(16, 45) if depth == "deep" else rng.randint(2, 14)
                txt = f"{off} QB pass complete {depth} {side} to {off} {slot} for {y} yards"
                td = ", touchdown" if y >= 30 or rng.random() < 0.03 else tackle(rng, dfn)
                txt += td if td.startswith(",") else ""
                html = (f"{plink(off, 'QB')} pass complete {depth} {side} to {plink(off, slot)} "
                        f"for {y} yards{td}")
                yield txt, html, y, ("pass", slot, True, y)
            else:
                txt = f"{off} QB pass incomplete {depth} {side} intended for {off} {slot}"
                html = f"{plink(off, 'QB')} pass incomplete {depth} {side} intended for {plink(off, slot)}"
                yield txt, html, 0, ("pass", slot, False, 0)
        elif r < 0.6:
            y = -rng.randint(3, 9)
            yield (f"{off} QB sacked by X for {y} yards",
                   f"{plink(off, 'QB')} sacked by {dlink(dfn, 2)} for {y} yards",
                   y, ("sack", None, None, y))
        else:
            gap = rng.choice(["left end", "left tackle", "up the middle", "right guard", "right end"])
            y = rng.randint(-2, 9)
            end = ", touchdown" if rng.random() < 0.03 else tackle(rng, dfn)
            yield (f"{off} RB {gap} for {y} yards", f"{plink(off, 'RB')} {gap} for {y} yards{end}",
                   y, ("run", "RB", None, y))


def render_boxscore(rng, week, away, home):
    stats = {(t, s): {"pass_cmp": 0, "pass_att": 0, "pass_yds": 0, "rush_att": 0, "rush_yds": 0,
                      "targets": 0, "rec": 0, "rec_yds": 0} for t in (away, home) for s in ROSTER}
    rows = []
    ep = 1.0
    for q in range(1, 5):
        for off in (away, home):
            dfn = home if off == away else away
            for text, html, y, (kind, slot, cmp, yds) in gen_drive_plays(rng, off, dfn, 16):
                down = rng.choice([1, 2, 3])
                ytg = 10 if down == 1 else rng.randint(1, 10)
                ep_after = ep + y * 0.06 - 0.1
                rows.append(f'<tr><th data-stat="quarter">{q}</th><td data-stat="qtr_time_remain">10:00</td>'
                            f'<td data-stat="down">{down}</td><td data-stat="yds_to_go">{ytg}</td>'
                            f'<td data-stat="location">{dfn} 40</td><td data-stat="pbp_score_aw">0</td>'
                            f'<td data-stat="pbp_score_hm">0</td><td data-stat="detail">{html}</td>'
                            f'<td data-stat="exp_pts_before">{ep:.2f}</td>'
                            f'<td data-stat="exp_pts_after">{ep_after:.2f}</td></tr>')
                if kind == "pass":
                    stats[(off, "QB")]["pass_att"] += 1
                    stats[(off, slot)]["targets"] += 1
                    if cmp:
                        stats[(off, "QB")]["pass_cmp"] += 1
                        stats[(off, "QB")]["pass_yds"] += yds
                        stats[(off, slot)]["rec"] += 1
                        stats[(off, slot)]["rec_yds"] += yds
                elif kind == "run":
                    stats[(off, "RB")]["rush_att"] += 1
                    stats[(off, "RB")]["rush_yds"] += yds
            kicker = f'<a href="/players/{off[0]}/{off.title()}Kk00.htm">{off} K</a>'
            dist = rng.randint(25, 55)
            res = "good" if rng.random() < 0.85 else "no good"
            rows.append(f'<tr><th data-stat="quarter">{q}</th><td data-stat="detail">'
                        f'{kicker} {dist} yard field goal {res}</td></tr>')
            if q % 2 == 0:
                rows.append(f'<tr><th data-stat="quarter">{q}</th><td data-stat="detail">'
                            f'{kicker} kicks extra point good</td></tr>')
    pbp = '<table id="pbp"><tbody>' + "".join(rows) + "</tbody></table>"

    po = []
    for (t, s), st in stats.items():
        cells = "".join(f'<td data-stat="{k}">{v}</td>' for k, v in st.items())
        po.append(f'<tr><th data-stat="player" data-append-csv="{pid(t, s)}">{plink(t, s)}</th>'
                  f'<td data-stat="team">{t}</td>{cells}</tr>')
    player_offense = '<table id="player_offense"><tbody>' + "".join(po) + "</tbody></table>"

    def snaps(team, tid):
        trs = "".join(f'<tr><th data-stat="player">{plink(team, s)}</th><td data-stat="pos">{pos}</td>'
                      f'<td data-stat="offense">60</td><td data-stat="off_pct">90%</td>'
                      f'<td data-stat="defense">0</td></tr>' for s, pos in ROSTER.items())
        return f'<table id="{tid}"><tbody>{trs}</tbody></table>'

    return ("<html><body><div id='all_player_offense'><!--" + player_offense + "--></div>"
            "<div><!--" + snaps(home, "home_snap_counts") + "--></div>"
            "<div><!--" + snaps(away, "vis_snap_counts") + "--></div>"
            "<div><!--" + pbp + "--></div></body></html>")


def render_schedule():
    rows = []
    for week, away, home in SCHEDULE:
        played = week <= PLAYED_THROUGH
        word = (f'<a href="/boxscores/{box_id(week, home)}.htm">boxscore</a>' if played else "preview")
        rows.append(f'<tr><th data-stat="week_num">{week}</th><td data-stat="game_date">2026-09-{week:02d}</td>'
                    f'<td data-stat="winner">{tlink(away)}</td><td data-stat="game_location">@</td>'
                    f'<td data-stat="loser">{tlink(home)}</td><td data-stat="boxscore_word">{word}</td></tr>')
    rows.insert(4, '<tr class="thead"><th data-stat="week_num">Week</th></tr>')
    return '<html><table id="games"><tbody>' + "".join(rows) + "</tbody></table></html>"


def write_cache(cache_dir: Path, seed: int = 7):
    rng = random.Random(seed)
    f = Fetcher(cache_dir)
    f.cache_path("/years/2026/games.htm").write_text(render_schedule())
    for week, away, home in SCHEDULE:
        if week <= PLAYED_THROUGH:
            f.cache_path(f"/boxscores/{box_id(week, home)}.htm").write_text(
                render_boxscore(rng, week, away, home))
