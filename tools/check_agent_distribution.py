#!/usr/bin/env python3
"""Check agent-facing distribution receipts for published posts.

Every post dated at or after the registry's effective_at, and every post the
registry already lists (the backfill), needs an entry. A post that is not a
media reply needs two receipts: its GitHub agent-board comment and its Moltbook
companion. A media reply (a post answering a video, podcast or news item) may
be marked exempt. A missing receipt is never silent: the post stays pending,
and a failed Moltbook post is recorded as "watching" until a retry lands.

Exit 0 when every required receipt is present, 1 when the registry is invalid,
2 when it is valid but receipts are still pending.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "editorial" / "agent-distribution.json"
POSTS = ROOT / "posts"
META_RE = re.compile(r"\A<!--\n(.*?)\n-->", re.DOTALL)
MEDIA_TAGS = {"podcasts", "current-events"}
STATUSES = {"waiting_github", "waiting_moltbook", "watching", "complete", "exempt"}
BOARD_PREFIX = "https://github.com/scottonchain/microcredit-vision/issues/24#issuecomment-"
MOLTBOOK_PREFIX = "https://www.moltbook.com/post/"
HUMAN_PREFIX = "https://github.com/scottonchain/microcredit-vision/blob/main/posts/"


def parse_utc(value: str) -> datetime:
    return datetime.strptime(value.strip(), "%Y-%m-%d %H:%M UTC").replace(tzinfo=timezone.utc)


def post_meta(text: str) -> dict[str, str]:
    match = META_RE.match(text)
    if not match:
        return {}
    meta = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep:
            meta[key.strip()] = value.strip()
    return meta


def is_media_reply(meta: dict[str, str]) -> bool:
    tags = {t.strip() for t in meta.get("tags", "").split(",") if t.strip()}
    return bool(meta.get("video_id")) or bool(tags & MEDIA_TAGS)


def check(registry: dict, posts: dict[str, str]) -> tuple[list[str], list[str]]:
    """Return (errors, pending) for a registry and a {slug: post text} map."""
    errors: list[str] = []
    pending: list[str] = []
    effective = parse_utc(registry["effective_at"])
    entries = registry.get("entries", {})
    metas = {slug: post_meta(text) for slug, text in posts.items()}

    required = set(entries)
    for slug, meta in metas.items():
        if "date" not in meta:
            errors.append(f"{slug}: missing metadata date")
            continue
        if parse_utc(meta["date"]) >= effective:
            required.add(slug)

    seen: dict[str, str] = {}
    for slug in sorted(required):
        entry = entries.get(slug)
        if entry is None:
            errors.append(f"{slug}: missing agent-distribution entry")
            continue
        if slug not in metas:
            errors.append(f"{slug}: registry entry has no post")
            continue
        status = entry.get("status")
        if status not in STATUSES:
            errors.append(f"{slug}: unknown status {status!r}")
            continue
        if entry.get("human_url") != f"{HUMAN_PREFIX}{slug}.md":
            errors.append(f"{slug}: human_url does not point at the post")

        for field, prefix in (("github_board_url", BOARD_PREFIX), ("moltbook_url", MOLTBOOK_PREFIX)):
            url = entry.get(field)
            if not url:
                continue
            if not url.startswith(prefix):
                errors.append(f"{slug}: {field} is not a {prefix}... receipt")
            if url in seen:
                errors.append(f"{slug}: {field} duplicates the receipt of {seen[url]}")
            seen[url] = slug

        exempt = bool(entry.get("media_reply_exempt"))
        if exempt != (status == "exempt"):
            errors.append(f"{slug}: media_reply_exempt and status 'exempt' must agree")
            continue
        if exempt:
            if not is_media_reply(metas[slug]):
                errors.append(f"{slug}: exempt but not a media reply")
            continue

        has_board = bool(entry.get("github_board_url"))
        has_molt = bool(entry.get("moltbook_url"))
        if status == "complete":
            if not (has_board and has_molt):
                errors.append(f"{slug}: complete without both required receipts")
            continue
        if has_board and has_molt:
            errors.append(f"{slug}: both receipts present but status is {status!r}, not 'complete'")
            continue
        if status == "waiting_moltbook" and not has_board:
            errors.append(f"{slug}: status waiting_moltbook but the GitHub receipt is missing")
        if not has_board:
            pending.append(f"{slug}: GitHub agent-board receipt pending ({status})")
        if not has_molt:
            note = entry.get("note", "")
            pending.append(f"{slug}: Moltbook receipt pending ({status}){' - ' + note if note else ''}")

    announcement = registry.get("board_announcement")
    if announcement:
        url = announcement.get("moltbook_url")
        if url and (not url.startswith(MOLTBOOK_PREFIX) or url in seen):
            errors.append("board_announcement: moltbook_url is not a fresh Moltbook post receipt")
        if announcement.get("status") == "complete" and not url:
            errors.append("board_announcement: complete without a Moltbook receipt")
        elif announcement.get("status") != "complete":
            pending.append(f"board_announcement: Moltbook receipt pending ({announcement.get('status')})")
    return errors, pending


def load_posts(directory: Path = POSTS) -> dict[str, str]:
    return {p.stem: p.read_text(encoding="utf-8") for p in sorted(directory.glob("*.md"))}


def main() -> int:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    errors, pending = check(registry, load_posts())
    for line in errors:
        print(f"ERROR: {line}")
    for line in pending:
        print(f"PENDING: {line}")
    if errors:
        return 1
    if pending:
        print("Agent distribution incomplete: keep each pending item WATCHING and route a failed Moltbook post to Hermes.")
        return 2
    print("Agent distribution receipts complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
