"""Notifications: Telegram and/or a GitHub issue thread.

Telegram (optional): TELEGRAM_BOT_TOKEN from @BotFather, TELEGRAM_CHAT_ID (your
chat with the bot: message the bot once, then
https://api.telegram.org/bot<token>/getUpdates shows it).

GitHub issue feed (needs no keys inside GitHub Actions): with GITHUB_TOKEN,
GITHUB_REPOSITORY and NFL_FEED_ISSUE set, every message is also posted as a
comment on that issue, so the GitHub app / email notifies you.

With neither, messages are printed.
"""

from __future__ import annotations

import os
from pathlib import Path

import requests


def _github(text: str, log=print) -> bool:
    tok, repo, issue = (os.environ.get("GITHUB_TOKEN"), os.environ.get("GITHUB_REPOSITORY"),
                        os.environ.get("NFL_FEED_ISSUE"))
    if not (tok and repo and issue):
        return False
    r = requests.post(f"https://api.github.com/repos/{repo}/issues/{issue}/comments", timeout=30,
                      headers={"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json"},
                      json={"body": text[:65000]})
    if r.status_code >= 300:
        log(f"github feed failed ({r.status_code}): {r.text[:200]}")
        return False
    return True


def send(text: str, log=print) -> bool:
    gh = _github(text, log)
    token, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        if not gh:
            log("[telegram not configured] " + text)
        return gh
    ok = True
    for i in range(0, len(text), 3900):  # Telegram's limit is 4096 characters
        r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", timeout=30,
                          data={"chat_id": chat, "text": text[i:i + 3900], "disable_web_page_preview": "true"})
        if r.status_code != 200:
            log(f"telegram failed ({r.status_code}): {r.text[:200]}")
            ok = False
    return ok or gh


def send_file(path: Path, caption: str = "", log=print) -> bool:
    """Send a file (e.g. the prop board HTML) to Telegram; opens in the phone's browser."""
    token, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat or not Path(path).exists():
        return False
    with open(path, "rb") as fh:
        r = requests.post(f"https://api.telegram.org/bot{token}/sendDocument", timeout=60,
                          data={"chat_id": chat, "caption": caption[:1000]}, files={"document": fh})
    if r.status_code != 200:
        log(f"telegram file failed ({r.status_code}): {r.text[:200]}")
        return False
    return True
