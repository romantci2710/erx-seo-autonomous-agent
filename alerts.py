# -*- coding: utf-8 -*-
"""
Alerts for the ERX SEO daemon (standard library only).

Only *changes* are reported: a site-health flag that appears or clears, or an experiment that regressed.
Channels are configured with environment variables and are all optional:

    ALERT_WEBHOOK_URL            https URL of a Slack / Discord / generic webhook
    ALERT_WEBHOOK_FORMAT         slack (default) | discord | generic
    ALERT_TELEGRAM_BOT_TOKEN     Telegram bot token
    ALERT_TELEGRAM_CHAT_ID       Telegram chat id

Sending never raises; failures are logged.
"""
from __future__ import annotations

import json
import logging
import os
import urllib.request
from typing import Any, Callable, Mapping

logger = logging.getLogger("muse_seo_daemon.alerts")
HttpPost = Callable[[str, bytes, dict[str, str]], Any]


def default_post(url: str, data: bytes, headers: dict[str, str]) -> int:
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.status


def _normalise(flag: str) -> str:
    """'HTML_NOT_COMPRESSED (952 KB)' and '(975 KB)' are the same finding."""
    return flag.split(" (")[0]


def diff_flags(previous: list[str] | None, current: list[str]) -> dict[str, list[str]] | None:
    """None for the first observation or when nothing changed."""
    if previous is None:
        return None
    before = {_normalise(f) for f in previous}
    after = {_normalise(f) for f in current}
    added, cleared = sorted(after - before), sorted(before - after)
    if not added and not cleared:
        return None
    return {"added": added, "cleared": cleared}


def format_message(events: list[dict[str, Any]]) -> str:
    if not events:
        return ""
    lines = ["ERX SEO daemon: thay đổi cần chú ý"]
    for e in events:
        if e["type"] == "site_health":
            parts = []
            if e["added"]:
                parts.append("MỚI: " + ", ".join(e["added"]))
            if e["cleared"]:
                parts.append("đã hết: " + ", ".join(e["cleared"]))
            lines.append(f"- {e['domain']}: " + "; ".join(parts))
        elif e["type"] == "experiment_regressed":
            lines.append(f"- Thí nghiệm {e['id']} xấu đi sau {e['days']} ngày: {e['url']}")
    return "\n".join(lines)


def send(message: str, env: Mapping[str, str] | None = None, http_post: HttpPost = default_post) -> list[str]:
    """Send to every configured channel; returns the channels that succeeded."""
    env = os.environ if env is None else env
    sent: list[str] = []
    headers = {"Content-Type": "application/json; charset=utf-8"}

    url = env.get("ALERT_WEBHOOK_URL", "").strip()
    if url:
        if not url.lower().startswith("https://"):
            logger.warning("ALERT_WEBHOOK_URL must use https; ignored")
        else:
            fmt = env.get("ALERT_WEBHOOK_FORMAT", "slack").strip().lower()
            key = {"discord": "content", "generic": "message"}.get(fmt, "text")
            try:
                http_post(url, json.dumps({key: message}).encode("utf-8"), headers)
                sent.append("webhook")
            except Exception as exc:
                logger.warning("Webhook alert failed: %s", exc)

    token, chat = env.get("ALERT_TELEGRAM_BOT_TOKEN", "").strip(), env.get("ALERT_TELEGRAM_CHAT_ID", "").strip()
    if token and chat:
        try:
            http_post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json.dumps({"chat_id": chat, "text": message}).encode("utf-8"),
                headers,
            )
            sent.append("telegram")
        except Exception:
            logger.warning("Telegram alert failed")  # never log the URL: it contains the bot token
    return sent
