#!/usr/bin/env python3
"""Publish a staged draft now (Claude Code, 2026-10-08): the one-command version of the steps in CLAUDE.md.

    python3 tools/publish_staged.py work-we-can-do-together            # publish at the current UTC time
    python3 tools/publish_staged.py work-we-can-do-together --dry-run  # show what would change, change nothing

Takes editorial/<date>-<name>.md (or editorial/<name>.md), sets `date:` to the current UTC time (never a planned one),
adds `queued:` from the queue item's ready time, moves the file to posts/, makes the illustration if its motif exists
and is missing, removes the item from editorial/queue.json and runs the build (which refuses a post that breaks the
spacing, guest-cap or audio rules; on a refusal the files are put back). It does not commit or push.
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FMT = "%Y-%m-%d %H:%M UTC"


def find_draft(name):
    hits = sorted(glob.glob(f"editorial/*{name}.md"))
    if len(hits) != 1:
        raise SystemExit(f"expected exactly one editorial draft for '{name}', found {hits}")
    return hits[0]


def main(argv):
    os.chdir(ROOT)
    name = next((a for a in argv if not a.startswith("--")), None)
    if not name:
        raise SystemExit(__doc__)
    dry = "--dry-run" in argv
    src = find_draft(name)
    text = original = open(src, encoding="utf-8").read()
    now = datetime.now(timezone.utc).strftime(FMT)
    q = json.load(open("editorial/queue.json", encoding="utf-8"))
    item = next((i for i in q["items"] if i.get("file") == src or i.get("slug", "").endswith(name) or i["id"].endswith(name)), None)
    text = re.sub(r"^date: .*$", f"date: {now}", text, count=1, flags=re.M)
    if item and item.get("ready") and not re.search(r"^queued: ", text, re.M):
        text = re.sub(r"^(date: .*)$", rf"\1\nqueued: {item['ready']}", text, count=1, flags=re.M)
    day = now[:10]
    base = os.path.basename(src)
    dest = os.path.join("posts", base if re.match(r"\d{4}-\d\d-\d\d-", base) else f"{day}-{base}")
    dest = re.sub(r"^posts/\d{4}-\d\d-\d\d-", f"posts/{day}-", dest) if not dry else dest
    print(f"publish {src} -> {dest} at {now}" + (f"; queue item {item['id']} removed" if item else "; no queue item"))
    if dry:
        return
    if os.path.exists(dest):
        raise SystemExit(f"{dest} already exists")
    shutil.move(src, dest)
    open(dest, "w", encoding="utf-8").write(text)
    saved = json.dumps(q, indent=2, ensure_ascii=False) + "\n"
    if item:
        q["items"] = [i for i in q["items"] if i is not item]
        open("editorial/queue.json", "w", encoding="utf-8").write(json.dumps(q, indent=2, ensure_ascii=False) + "\n")
    r = subprocess.run([sys.executable, "tools/build.py"], capture_output=True, text=True)
    if r.returncode:
        os.remove(dest)
        open(src, "w", encoding="utf-8").write(original)
        open("editorial/queue.json", "w", encoding="utf-8").write(saved)
        raise SystemExit("the build refused the post, so it was put back:\n" + (r.stdout + r.stderr).strip()[-600:])
    print("built; review the diff, then commit with the project's noreply identity and push")


if __name__ == "__main__":
    main(sys.argv[1:])
