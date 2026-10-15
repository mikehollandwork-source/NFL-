"""Telegram messages (bot token and chat id from the environment).

TELEGRAM_BOT_TOKEN  from @BotFather
TELEGRAM_CHAT_ID    your chat with the bot (message the bot once, then
                    https://api.telegram.org/bot<token>/getUpdates shows it)
Without them, messages are printed instead.
"""

from __future__ import annotations

import os

import requests


def send(text: str, log=print) -> bool:
    token, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        log("[telegram not configured] " + text)
        return False
    ok = True
    for i in range(0, len(text), 3900):  # Telegram's limit is 4096 characters
        r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", timeout=30,
                          data={"chat_id": chat, "text": text[i:i + 3900], "disable_web_page_preview": "true"})
        if r.status_code != 200:
            log(f"telegram failed ({r.status_code}): {r.text[:200]}")
            ok = False
    return ok
