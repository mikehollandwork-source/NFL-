from nfl_proj.playparse import is_success, parse_detail


def link(pid, name):
    return f'<a href="/players/{pid[0]}/{pid}.htm">{name}</a>'


def test_complete_deep_pass():
    html = (f"{link('AlleJo02', 'Josh Allen')} pass complete deep right to "
            f"{link('ShakKh00', 'Khalil Shakir')} for 32 yards (tackle by {link('SmitJa01', 'Jalen Smith')})")
    text = "Josh Allen pass complete deep right to Khalil Shakir for 32 yards (tackle by Jalen Smith)"
    p = parse_detail(text, html)
    assert p["play_type"] == "pass"
    assert p["bucket"] == "pass_deep_right"
    assert p["complete"] is True and p["yards"] == 32
    assert p["passer_id"] == "AlleJo02" and p["target_id"] == "ShakKh00"


def test_incomplete_with_defender_only_has_no_target():
    html = f"{link('HurtJa00', 'Jalen Hurts')} pass incomplete short left (defended by {link('XxxYy00', 'X')})"
    p = parse_detail("Jalen Hurts pass incomplete short left (defended by X)", html)
    assert p["bucket"] == "pass_short_left"
    assert p["target_id"] is None and p["yards"] == 0


def test_interception():
    html = (f"{link('MahoPa00', 'Patrick Mahomes')} pass deep middle intended for "
            f"{link('KelcTr00', 'Travis Kelce')} is intercepted by {link('XxxYy00', 'X')} at KAN 40")
    p = parse_detail("Patrick Mahomes pass deep middle intended for Travis Kelce is intercepted by X at KAN 40", html)
    assert p["play_type"] == "pass" and p["interception"]
    assert p["bucket"] == "pass_deep_middle" and p["target_id"] == "KelcTr00"


def test_runs():
    p = parse_detail("Saquon Barkley left tackle for 5 yards (tackle by X)",
                     f"{link('BarkSa00', 'Saquon Barkley')} left tackle for 5 yards")
    assert (p["play_type"], p["bucket"], p["yards"], p["rusher_id"]) == ("run", "run_inside_left", 5, "BarkSa00")
    p = parse_detail("Derrick Henry up the middle for no gain", f"{link('HenrDe00', 'Derrick Henry')} up the middle")
    assert (p["bucket"], p["yards"]) == ("run_middle", 0)
    p = parse_detail("Derrick Henry right end for -2 yards", f"{link('HenrDe00', 'D')} right end")
    assert (p["bucket"], p["yards"]) == ("run_outside_right", -2)


def test_sack_penalty_special():
    assert parse_detail("Lamar Jackson sacked by X for -7 yards", link("JackLa00", "L"))["play_type"] == "sack"
    assert parse_detail("Penalty on X: False Start, 5 yards (no play)")["play_type"] == "penalty"
    assert parse_detail("Jake Elliott 45 yard field goal good")["play_type"] == "special"
    assert parse_detail("Tommy Townsend punts 48 yards")["play_type"] == "special"
    assert parse_detail("Patrick Mahomes kneels for -1 yards")["play_type"] == "kneel"


def test_success():
    assert is_success(1, 10, 4) and not is_success(1, 10, 3)
    assert is_success(2, 5, 3) and not is_success(2, 5, 2)
    assert is_success(3, 2, 2) and not is_success(3, 2, 1)
