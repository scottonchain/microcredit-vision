#!/usr/bin/env python3
"""Read a sample of public Moltbook posts (no key needed) into sample.json (not committed: it holds other agents' text).

    python3 sample.py [out.json]

For each of 11 submolts: the 100 newest and 50 top posts (25 per request, cursor paging). Read-only.
"""
import json
import sys
import time
import urllib.error
import urllib.request

SUBS = ["agents", "general", "ai", "builds", "security", "memory", "todayilearned", "philosophy", "tooling",
        "openclaw-explorers", "introductions"]
out = {}
calls = 0
for sub in SUBS:
    for sort, pages in (("new", 4), ("top", 2)):
        cursor = None
        for _ in range(pages):
            url = f"https://www.moltbook.com/api/v1/posts?submolt={sub}&sort={sort}&limit=25" + (f"&cursor={cursor}" if cursor else "")
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "moltbook-wants-sample/1"}), timeout=25) as r:
                    d = json.load(r)
                calls += 1
            except (urllib.error.URLError, ValueError) as e:
                print("stopped:", sub, sort, type(e).__name__)
                break
            for p in d.get("posts", []):
                out[p["id"]] = {"id": p["id"], "submolt": sub, "sort": sort, "title": p.get("title"), "content": p.get("content") or "",
                                "upvotes": p.get("upvotes"), "comments": p.get("comment_count"), "created": p.get("created_at"),
                                "author": (p.get("author") or {}).get("name")}
            cursor = d.get("next_cursor")
            time.sleep(0.25)
            if not d.get("has_more"):
                break
json.dump(list(out.values()), open(sys.argv[1] if len(sys.argv) > 1 else "sample.json", "w"))
print("requests", calls, "distinct posts", len(out))
