#!/usr/bin/env python3
"""Check agent-facing distribution receipts for published posts."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "editorial" / "agent-distribution.json"
POSTS = ROOT / "posts"
DATE_RE = re.compile(r"^date:\s*(.+)$", re.MULTILINE)


def parse_utc(value: str) -> datetime:
    return datetime.strptime(value.strip(), "%Y-%m-%d %H:%M UTC").replace(tzinfo=timezone.utc)


def post_date(path: Path) -> datetime:
    text = path.read_text(encoding="utf-8")
    match = DATE_RE.search(text)
    if not match:
        raise ValueError(f"{path}: missing metadata date")
    return parse_utc(match.group(1))


def main() -> int:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    effective = parse_utc(data["effective_at"])
    entries = data["entries"]
    errors: list[str] = []

    for post in sorted(POSTS.glob("*.md")):
        if post_date(post) < effective:
            continue
        slug = post.stem
        entry = entries.get(slug)
        if not entry:
            errors.append(f"{slug}: missing agent-distribution entry")
            continue

        if entry.get("media_reply_exempt"):
            continue

        if not entry.get("github_board_url"):
            errors.append(f"{slug}: missing GitHub agent-board receipt")
        if not entry.get("moltbook_url"):
            errors.append(f"{slug}: missing Moltbook receipt")
        if entry.get("status") != "complete":
            errors.append(f"{slug}: distribution status is not complete")

    for slug, entry in entries.items():
        if entry.get("media_reply_exempt"):
            continue
        if entry.get("status") == "complete" and (
            not entry.get("github_board_url") or not entry.get("moltbook_url")
        ):
            errors.append(f"{slug}: complete without both required receipts")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Agent distribution receipts complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
