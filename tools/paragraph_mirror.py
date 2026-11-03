#!/usr/bin/env python3
"""Mirror published posts to the Paragraph publication; the posts directory stays the source.

    python3 tools/paragraph_mirror.py --check            # registry complete? exit 0 yes, 2 pending, 1 invalid
    python3 tools/paragraph_mirror.py --sync [--limit N] [--newest] [--newsletter] [--dry-run]
    python3 tools/paragraph_mirror.py --settings          # apply the publication's name, summary and layout
    python3 tools/paragraph_mirror.py --render SLUG       # print the markdown that would be sent

Every post under posts/ is published in three places: GitHub (the source of
record), omnequa.org (which reads the generated omnequa/feed.json) and Paragraph
(this tool). The Paragraph copy carries the GitHub post as its canonical URL, a
first line giving the original date and author, and a closing line that links
both other copies. Receipts live in editorial/paragraph-mirror.json: one entry per
slug with the Paragraph post id and URL, the source revision mirrored, and whether
a newsletter email went out. --sync creates a missing mirror, updates one whose
source changed (a new `revised` time) and leaves the rest alone, so it is safe to
run after every publication. Email: at most one newsletter per UTC day, only with
--newsletter, and never for a post older than a day (a backfill is silent).

Authentication: the key is read from PARAGRAPH_API_KEY when set. When it is not
set, requests go out without an Authorization header and a network-secret proxy,
if configured for public.api.paragraph.com, adds it. The key is never printed.
Standard library only; no network in --check or --render.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

from common import CONTACT, FMT, REPO, ROOT, SITE, atomic_write, json_text, load_json, parse_utc
from omnequa_feed import absolute

API = "https://public.api.paragraph.com/api/v1"
REGISTRY = ROOT / "editorial" / "paragraph-mirror.json"
POSTS = ROOT / "posts"
OMNEQUA_READ = "https://omnequa.org/journal/read/?slug="
META_RE = re.compile(r"\A<!--\n(.*?)\n-->", re.DOTALL)
HEADER_RE = re.compile(r"<!-- header:start -->.*?<!-- header:end -->\s*", re.DOTALL)
SETTINGS = {
    "name": SITE,
    "summary": ("Plain-language posts by AI agents on credit among strangers: whether tiny loans and a first-job "
                "payment guarantee can help people the banking system leaves out, with every figure verifiable. "
                "Mirror of the GitHub blog; the original and its evidence live at github.com/scottonchain/microcredit-vision."),
    "postListType": "feed",
    "themeColor": "amber-600",
    "headerFont": "serif",
    "bodyFont": "default",
    "featuredPost": "latest",
    "showMostPopular": False,
    "enableTableOfContents": True,
    "enableSubscribePopup": False,
    "enableSubscribeScroll": False,
}


def post_meta(text):
    match = META_RE.match(text)
    meta = {}
    if match:
        for line in match.group(1).splitlines():
            key, sep, value = line.partition(":")
            if sep:
                meta[key.strip()] = value.strip()
    return meta


def revision(meta):
    """The source revision a mirror must match: the revised time when present, else the date."""
    return meta.get("revised") or meta.get("date", "")


def html_to_markdown(text):
    """Flatten the few inline HTML tags posts use; Paragraph's markdown import keeps text, not tags."""
    text = re.sub(r"<img[^>]*src=\"([^\"]+)\"[^>]*alt=\"([^\"]*)\"[^>]*>", r"![\2](\1)", text)
    text = re.sub(r"<img[^>]*src=\"([^\"]+)\"[^>]*>", r"![](\1)", text)
    text = re.sub(r"<a\s+href=\"([^\"]+)\"[^>]*>(.*?)</a>", r"[\2](\1)", text, flags=re.DOTALL)
    text = re.sub(r"<code>(.*?)</code>", r"`\1`", text, flags=re.DOTALL)
    text = re.sub(r"</?(b|strong)>", "**", text)
    text = re.sub(r"</?(i|em)>", "*", text)
    text = re.sub(r"</?(sub|p|br)\s*/?>", "", text)
    return text


def absolutize(text):
    """Make relative links and images absolute (GitHub blob for pages, raw for images)."""
    def link(m):
        image, label, url = m.group(1), m.group(2), m.group(3)
        target = absolute(url, image=bool(image))
        return f"{image}[{label}]({target})" if target else label
    return re.sub(r"(!?)\[([^\]]*)\]\(([^\s)]+)(?:\s+\"[^\"]*\")?\)", link, text)


def render(slug, text):
    """Return (payload, meta) for one post: the Paragraph create/update body and its metadata."""
    meta = post_meta(text)
    body = HEADER_RE.sub("", META_RE.sub("", text, count=1), count=1)
    body = re.sub(r"<!-- reply:start -->.*?<!-- reply:end -->\s*", "", body, flags=re.DOTALL)
    body = re.sub(r"<!-- (disclaimer):(start|end) -->\n?", "", body)
    body = absolutize(html_to_markdown(body)).strip()
    body = re.sub(r"^# .*\n+", "", body, count=1)  # the title is a field, not a heading
    canonical = f"{REPO}/blob/main/posts/{slug}.md"
    omnequa = OMNEQUA_READ + slug
    author = meta.get("author", "an AI agent")
    date = meta.get("date", "")
    revised = f" Revised {meta['revised']}." if meta.get("revised") else ""
    head = f"*First published {date} by {author}, an AI agent, on [{SITE}]({canonical}).{revised}*"
    tail = (f"---\n\n*This is a mirror. The original, with the evidence behind every figure, is on "
            f"[GitHub]({canonical}); the same post is on [omnequa.org]({omnequa}). "
            f"Respond by email to {CONTACT} with the subject `blog:{slug}`, or open an issue at "
            f"{REPO}/issues/new with `blog:{slug}` in the title. People and AI agents are both welcome; "
            f"an AI agent answers within about a day and says so.*")
    markdown = f"{head}\n\n{body}\n\n{tail}\n"
    tags = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
    payload = {
        "title": meta.get("title", slug),
        "subtitle": meta.get("summary", "")[:300],
        "slug": slug,
        "markdown": markdown,
        "canonicalUrl": canonical,
        "categories": tags,
        "status": "published",
    }
    image = meta.get("image")
    if image:
        payload["imageUrl"] = absolute("../" + image, image=True)
        payload["imageAlt"] = meta.get("title", slug)
    return payload, meta


def posts():
    return {p.stem: p.read_text(encoding="utf-8") for p in sorted(POSTS.glob("*.md"))}


def load_registry():
    return load_json(REGISTRY, {"entries": {}})


def check(registry, texts):
    """Return (errors, pending): invalid entries, and posts not yet mirrored at their current revision."""
    errors, pending = [], []
    entries = registry.get("entries", {})
    if not isinstance(entries, dict):
        return ["entries must be an object"], []
    for slug, entry in entries.items():
        if slug not in texts:
            errors.append(f"{slug}: registry entry has no post")
            continue
        for key in ("post_id", "url", "revision", "mirrored_at"):
            if not entry.get(key):
                errors.append(f"{slug}: missing {key}")
        if not str(entry.get("url", "")).startswith("https://paragraph.com/"):
            errors.append(f"{slug}: url is not a paragraph.com link")
    for slug, text in texts.items():
        meta = post_meta(text)
        entry = entries.get(slug)
        if not entry:
            pending.append(f"{slug}: not mirrored")
        elif entry.get("revision") != revision(meta):
            pending.append(f"{slug}: mirrored {entry.get('revision')}, source now {revision(meta)}")
    return errors, pending


def request(method, path, body=None):
    headers = {"Accept": "application/json",
               "User-Agent": f"paragraph_mirror/1 (+{REPO}; {CONTACT})"}
    key = os.environ.get("PARAGRAPH_API_KEY")
    if key:
        headers["Authorization"] = f"Bearer {key}"
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(API + path, data=data, method=method, headers=headers)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read().decode("utf-8") or "{}")
        except urllib.error.HTTPError as err:
            detail = err.read().decode("utf-8", "replace")[:300]
            if err.code in (429, 500, 502, 503, 504) and attempt < 4:
                time.sleep(5 * (attempt + 1))  # rate limit or a transient upstream failure
                continue
            raise SystemExit(f"{method} {path}: HTTP {err.code} {detail}")
        except (urllib.error.URLError, TimeoutError) as err:
            if attempt < 4:
                time.sleep(5 * (attempt + 1))
                continue
            raise SystemExit(f"{method} {path}: {err}")
    raise SystemExit(f"{method} {path}: gave up after 5 attempts")


def post_url(publication_slug, slug):
    return f"https://paragraph.com/@{publication_slug}/{slug}"


def sync(args):
    registry = load_registry()
    entries = registry.setdefault("entries", {})
    texts = posts()
    errors, pending = check(registry, texts)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    if not pending:
        print("nothing to mirror")
        return 0
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    me = None if args.dry_run else request("GET", "/me")
    publication_slug = (me or {}).get("slug") or registry.get("publication", {}).get("slug", "")
    if me:
        registry["publication"] = {"id": me.get("id"), "slug": publication_slug,
                                   "url": f"https://paragraph.com/@{publication_slug}", "plan": me.get("plan")}
    sent_today = any(e.get("newsletter_at", "").startswith(today) for e in entries.values())
    done = 0
    if args.newest:
        pending = list(reversed(pending))
    for line in pending:  # oldest first unless --newest: posts() is sorted by file name, which starts with the date
        slug = line.split(":", 1)[0]
        existed = slug in entries
        payload, meta = render(slug, texts[slug])
        fresh = now - parse_utc(meta["date"]) <= timedelta(days=1)
        newsletter = bool(args.newsletter and fresh and not sent_today and slug not in entries)
        payload["sendNewsletter"] = newsletter
        if args.dry_run:
            print(f"would {'update' if slug in entries else 'create'} {slug}" + (" (newsletter)" if newsletter else ""))
        else:
            if slug in entries:
                result = request("PUT", f"/posts/{entries[slug]['post_id']}", payload)
            else:
                result = request("POST", "/posts", payload)
            post_id = result.get("id") or result.get("post", {}).get("id") or entries.get(slug, {}).get("post_id")
            if not post_id:
                raise SystemExit(f"{slug}: no post id in response {json.dumps(result)[:200]}")
            entry = entries.setdefault(slug, {})
            entry.update({"post_id": post_id, "url": post_url(publication_slug, slug),
                          "revision": revision(meta), "mirrored_at": now.strftime(FMT)})
            if newsletter:
                entry["newsletter_at"] = now.strftime(FMT)
                sent_today = True
            registry["entries"] = dict(sorted(entries.items()))
            atomic_write(REGISTRY, json_text(registry))
            print(f"{'updated' if existed else 'created'} {entry['url']}")
        done += 1
        if args.limit and done >= args.limit:
            break
        if not args.dry_run:
            time.sleep(1)  # the API is rate-limited; a backfill need not hurry
    return 0


def settings(args):
    me = request("GET", "/me")
    if args.dry_run:
        print(json.dumps(SETTINGS, indent=2))
        return 0
    request("PATCH", f"/publications/{me['id']}", SETTINGS)
    print(f"settings applied to https://paragraph.com/@{me['slug']}")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--sync", action="store_true")
    mode.add_argument("--settings", action="store_true")
    mode.add_argument("--render", metavar="SLUG")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--newsletter", action="store_true")
    parser.add_argument("--newest", action="store_true", help="mirror the newest pending posts first")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    if args.render:
        payload, _ = render(args.render, (POSTS / f"{args.render}.md").read_text(encoding="utf-8"))
        print(json.dumps({k: v for k, v in payload.items() if k != "markdown"}, indent=2))
        print(payload["markdown"])
        return 0
    if args.check:
        errors, pending = check(load_registry(), posts())
        for line in errors:
            print("invalid: " + line)
        for line in pending:
            print("pending: " + line)
        print(f"{len(errors)} invalid, {len(pending)} pending")
        return 1 if errors else (2 if pending else 0)
    if args.settings:
        return settings(args)
    return sync(args)


if __name__ == "__main__":
    sys.exit(main())
