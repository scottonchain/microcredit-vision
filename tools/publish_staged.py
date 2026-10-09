#!/usr/bin/env python3
"""Prepare a staged draft for publication; never commit, push or start a workflow.

    python3 tools/publish_staged.py work-we-can-do-together --dry-run
    python3 tools/publish_staged.py work-we-can-do-together

Sets the publication date to the current UTC time, carries the queue's ready time
into `queued:`, validates and renders the entire blog, then moves the draft into
posts/ and removes its queue item. Images must already exist. A validation failure
writes nothing. A write failure restores all affected files, including the queue
and generated outputs. This command does not override a publication pause.
"""
import argparse
import glob
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import build
from common import FMT, ROOT, json_text, load_json, write_files
from schedule import slug_tail


def find_draft(name):
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
        raise SystemExit("draft name must be a slug (letters, digits and hyphens)")
    hits = [str(p) for p in sorted(Path("editorial").glob("*.md"))
            if name in (p.stem, slug_tail(p.stem))]
    if len(hits) != 1:
        raise SystemExit(f"expected exactly one editorial draft for '{name}', found {hits}")
    return hits[0]


def prepare_draft(name, now):
    """Return the source, destination and all rendered changes; leave the files alone."""
    src = find_draft(name)
    text = Path(src).read_text(encoding="utf-8")
    q = load_json("editorial/queue.json")
    if not isinstance(q, dict) or not isinstance(q.get("items"), list):
        raise SystemExit("editorial/queue.json must contain an items list")
    names = {name, slug_tail(Path(src).stem)}
    # Guest ideas historically use guest-SLUG even when the draft uses SLUG.
    # Retain that explicit convention without matching arbitrary ID suffixes.
    matches = [i for i in q["items"] if i.get("file") == src
               or slug_tail(i.get("slug", "")) in names or i.get("id") in names
               or (i.get("lane") == "guest" and i.get("id", "").startswith("guest-")
                   and i["id"][len("guest-"):] in names)]
    if len(matches) > 1:
        raise SystemExit(f"more than one queue item matches {src}; resolve the duplicate before publication")
    item = matches[0] if matches else None
    meta = build.META_RE.match(text)
    if not meta:
        raise SystemExit(f"{src}: no metadata comment at the top")
    block = re.sub(r"^date:.*$", f"date: {now}", meta.group(0), count=1, flags=re.M)
    if item and item.get("ready"):
        if re.search(r"^queued:", block, re.M):
            block = re.sub(r"^queued:.*$", f"queued: {item['ready']}", block, flags=re.M)
        else:
            block = re.sub(r"^(date: .*)$", lambda m: m[0] + f"\nqueued: {item['ready']}", block, count=1, flags=re.M)
    text = block + text[meta.end():]
    dest = f"posts/{now[:10]}-{slug_tail(Path(src).stem)}.md"
    if Path(dest).exists():
        raise SystemExit(f"{dest} already exists")
    posts = [build.parse(path) for path in glob.glob("posts/*.md")]
    posts.append(build.parse(dest, text=text))
    posts.sort(key=lambda p: p["dt"], reverse=True)
    files = build.prepare(posts)
    if item:
        q["items"] = [i for i in q["items"] if i is not item]
        files["editorial/queue.json"] = json_text(q)
    return src, dest, item, files


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    os.chdir(ROOT)
    now = datetime.now(timezone.utc).strftime(FMT)
    src, dest, item, files = prepare_draft(args.name, now)
    print(f"publish {src} -> {dest} at {now}" +
          (f"; queue item {item['id']} removed" if item else "; no queue item"))
    if args.dry_run:
        print(f"validated {len(files)} outputs; no files written")
        return
    write_files(files, delete=[src, *build.obsolete_tag_pages()])
    print("built; review the diff and follow the current publication instructions")


if __name__ == "__main__":
    main()
