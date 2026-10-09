#!/usr/bin/env python3
"""Traced engagement: what outsiders did with this blog, counted from public records (Claude Code, 2026-10-08).

    python3 tools/engagement.py            # read the sources, update editorial/engagement.json, print the summary
    python3 tools/engagement.py --dry-run  # read and print, write nothing

An event is an action by an account or sender outside the team that cites or answers a specific post through a route
the blog gives it: an issue or comment (in this repository or another project repository) carrying `blog:<slug>` or a
post's address; mail to the project inbox carrying `blog:<slug>`, a post's address or `ref:moltbook`; a comment on one
of our Moltbook posts. Stars, forks and watchers of this repository are recorded at blog level. Nothing else counts:
page views are not available to us, and the team's own accounts never count.

Only counts are stored: no names, addresses, handles or message contents (the project's privacy rules). A sender that
says it is an AI in its own words ("AI disclosure", "I'm an AI agent") is counted as agent-declared; everything else is
unclassified, which includes people and agents that do not say. The sources are read without a key: the GitHub REST
API (60 requests an hour per address), AgentMail through the environment's proxy, and Moltbook's public comment
lists. A source that cannot be read is recorded as unavailable and its watermark is not advanced, so the next run
picks up what it missed. Events are never counted twice: each source keeps a watermark.
"""
import argparse
import json
import copy
import hashlib
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from email.utils import parseaddr

from common import ROOT, atomic_write, json_text, load_json

LEDGER = ROOT / "editorial/engagement.json"
UA = "credit-among-strangers-engagement/1 (read-only)"

DEFAULT_CONFIG = {
    "owner": "scottonchain",
    "blog_repo": "microcredit-vision",
    "repos": ["microcredit-vision", "microcredit-contract", "microcredit-agent-testbed", "microcredit-theory"],
    "team_accounts": ["scottonchain", "hermes-agent-909", "HermesCRBot", "github-actions[bot]"],
    "inbox": "claude-microcredit@agentmail.to",
    "team_mail": ["hermes-909@agentmail.to", "claude-microcredit@agentmail.to", "codex-microcredit@agentmail.to"],
    "moltbook_team": ["hermes-agent-909", "claude-code-microcredit"],
    "moltbook_posts": {},
    "since": "2026-10-08T17:00:00Z",       # the tracing regime starts with the generated reply line
    "since_blog_repo": "2026-10-04T00:00:00Z",  # the blog repository's own issues and comments are read from its start
}

REF_RE = re.compile(r"blog:([a-z0-9][a-z0-9-]{3,})")
URL_RE = re.compile(r"microcredit-vision/(?:blob/main/)?posts/([0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9-]+)(?:\.md)?")
MOLT_RE = re.compile(r"ref:moltbook")
AGENT_RE = re.compile(r"(?i)\b(ai disclosure|i['’]m an ai|i am an ai|as an ai agent|ai agent)\b")


def refs_in(text):
    """The post slugs a text cites: `blog:<slug>` tags and links to a post's file."""
    found = set(REF_RE.findall(text or "")) | set(URL_RE.findall(text or ""))
    return sorted(found)


def is_agent_declared(text):
    return bool(AGENT_RE.search(text or ""))


def get_json(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


class Ledger:
    """Cumulative counts plus the watermarks that keep a run from counting an event twice."""

    def __init__(self, data=None):
        d = copy.deepcopy(data or {})
        self.config = {**copy.deepcopy(DEFAULT_CONFIG), **d.get("config", {})}
        self.watermarks = d.get("watermarks", {})
        self.posts = d.get("posts", {})
        self.channels = {"moltbook_ref": 0, "unattributed_blog_repo": 0, **d.get("channels", {})}
        self.blog = d.get("blog", {})
        self.history = d.get("history", [])
        self.sources = d.get("sources", {})

    def add(self, slug, source, agent):
        rec = self.posts.setdefault(slug, {"events": 0, "agent_declared": 0, "github": 0, "mail": 0, "moltbook": 0})
        rec["events"] += 1
        rec[source] += 1
        if agent:
            rec["agent_declared"] += 1

    def to_dict(self, categories, now):
        total = sum(p["events"] for p in self.posts.values()) + self.channels["unattributed_blog_repo"] + self.channels["moltbook_ref"]
        return {
            "_doc": "Written by tools/engagement.py; counts only (CLAUDE.md, 'Queue, schedule and evaluation').",
            "updated": now.strftime("%Y-%m-%d %H:%M UTC"),
            "config": self.config,
            "sources": self.sources,
            "blog": self.blog,
            "channels": self.channels,
            "posts": dict(sorted(self.posts.items())),
            "categories": categories,
            "watermarks": self.watermarks,
            "history": self.history[-200:],
            "total_events": total,
        }


def ingest_github(led, repo, issues, comments):
    """Count outside issues and comments. issues/comments are GitHub API objects newer than the watermarks."""
    team = {name.casefold() for name in led.config["team_accounts"]}
    blog_repo = repo == led.config["blog_repo"]
    wm = led.watermarks.setdefault("github", {}).setdefault(repo, {"issue": 0, "comment": 0})
    new = 0
    items = [("issue", i["number"], i) for i in issues] + [("comment", c["id"], c) for c in comments]
    for kind, key, obj in sorted(items, key=lambda value: (value[0], value[1])):
        if key <= wm[kind]:
            continue
        wm[kind] = max(wm[kind], key)
        if (obj.get("user") or {}).get("login", "").casefold() in team or (obj.get("user") or {}).get("type") == "Bot":
            continue
        text = ((obj.get("title") or "") + "\n" + (obj.get("body") or ""))
        slugs = refs_in(text)
        agent = is_agent_declared(text)
        if slugs:
            for sl in slugs:
                led.add(sl, "github", agent)
                new += 1
        elif blog_repo:
            led.channels["unattributed_blog_repo"] += 1
            new += 1
        if MOLT_RE.search(text):
            led.channels["moltbook_ref"] += 1
    return new


def ingest_mail(led, messages):
    """messages: AgentMail list entries (newest first) with timestamp, labels, from, subject, preview."""
    team = {a.casefold() for a in led.config["team_mail"]}
    wm = led.watermarks.setdefault("mail", {"timestamp": "", "seen": []})
    newest = wm["timestamp"]
    seen = set(wm.get("seen", []))
    known_boundary = "seen" in wm or not newest
    new = 0
    for m in sorted(messages, key=lambda m: m.get("timestamp", "")):
        ts = m.get("timestamp", "")
        identity = m.get("message_id") or json.dumps([ts, m.get("from"), m.get("subject")], ensure_ascii=False)
        key = hashlib.sha256(identity.encode()).hexdigest()
        if ts < newest or (ts == newest and (not known_boundary or key in seen)):
            continue
        if ts > newest:
            newest, seen, known_boundary = ts, set(), True
        seen.add(key)
        sender = parseaddr(m.get("from") or "")[1].casefold()
        if "received" not in (m.get("labels") or []) or sender in team:
            continue
        text = (m.get("subject") or "") + "\n" + (m.get("preview") or m.get("text") or "")
        slugs = refs_in(text)
        agent = is_agent_declared(text)
        for sl in slugs:
            led.add(sl, "mail", agent)
            new += 1
        if MOLT_RE.search(text):
            led.channels["moltbook_ref"] += 1
            new += 0 if slugs else 1
    wm["timestamp"] = newest
    if known_boundary:
        wm["seen"] = sorted(seen)
    return new


def ingest_moltbook(led, post_id, slug, comments, upvotes=None):
    """Comments on one of our Moltbook posts by accounts that are not ours; each counts for the blog post it companions."""
    team = {name.casefold() for name in led.config["moltbook_team"]}
    wm = led.watermarks.setdefault("moltbook", {}).setdefault(post_id, {"seen": []})
    seen = set(wm["seen"])
    new = 0
    for c in comments:
        if c["id"] in seen:
            continue
        seen.add(c["id"])
        a = c.get("author") or {}
        name = a.get("name") if isinstance(a, dict) else a
        if (name or "").casefold() in team:
            continue
        led.add(slug, "moltbook", is_agent_declared(c.get("content") or ""))
        new += 1
    wm["seen"] = sorted(seen)
    return new


def category_table(led, posts):
    cats = {}
    for p in posts:
        for t in p["tag_list"]:
            c = cats.setdefault(t, {"posts": 0, "events": 0})
            c["posts"] += 1
            c["events"] += led.posts.get(p["slug"], {}).get("events", 0)
    return cats


def github_pages(url):
    """Read the complete result set; an incomplete read never advances a watermark."""
    rows, seen = [], set()
    page = 1
    while True:
        got = get_json(f"{url}&per_page=100&page={page}")
        if not isinstance(got, list):
            raise ValueError("GitHub returned something other than a list")
        signature = tuple(entry.get("id", entry.get("number")) for entry in got)
        if got and signature in seen:
            raise ValueError("GitHub repeated a page; refusing an incomplete count")
        seen.add(signature)
        rows.extend(got)
        if len(got) < 100:
            return rows
        page += 1


def read_github(led, now):
    owner = led.config["owner"]
    try:
        r = get_json(f"https://api.github.com/repos/{owner}/{led.config['blog_repo']}")
        led.blog = {"stars": r.get("stargazers_count"), "forks": r.get("forks_count"), "watchers": r.get("subscribers_count"),
                    "read": now.strftime("%Y-%m-%d %H:%M UTC")}
        for repo in led.config["repos"]:
            since = led.config["since_blog_repo"] if repo == led.config["blog_repo"] else led.config["since"]
            issues = github_pages(f"https://api.github.com/repos/{owner}/{repo}/issues?state=all&sort=created&direction=asc&since={since}")
            comments = github_pages(f"https://api.github.com/repos/{owner}/{repo}/issues/comments?sort=created&direction=asc&since={since}")
            ingest_github(led, repo, issues, comments)
        led.sources["github"] = "ok"
    except Exception as e:  # rate limit, network: record and keep the old watermarks
        led.sources["github"] = f"unavailable: {type(e).__name__} {str(e)[:80]}"


def read_mail(led):
    try:
        inbox = urllib.parse.quote(led.config["inbox"])
        data = get_json(f"https://api.agentmail.to/v0/inboxes/{inbox}/messages?limit=100")
        if data.get("next_page_token") or len(data.get("messages") or []) >= 100:
            raise ValueError("mail response may be truncated; watermark unchanged until a complete export is available")
        ingest_mail(led, data.get("messages") or [])
        led.sources["mail"] = "ok"
    except Exception as e:
        led.sources["mail"] = f"unavailable: {type(e).__name__} {str(e)[:80]}"


def read_moltbook(led):
    posts = led.config.get("moltbook_posts") or {}
    if not posts:
        led.sources["moltbook"] = "no posts configured yet"
        return
    try:
        for pid, meta in posts.items():
            data = get_json(f"https://www.moltbook.com/api/v1/posts/{pid}/comments?sort=new&limit=100")
            if data.get("next_cursor") or data.get("has_more") or len(data.get("comments") or []) >= 100:
                raise ValueError("Moltbook response may be truncated; refusing an incomplete count")
            flat = []

            def walk(cs):
                for c in cs:
                    flat.append(c)
                    walk(c.get("replies") or [])
            walk(data.get("comments") or [])
            ingest_moltbook(led, pid, meta["slug"], flat)
        led.sources["moltbook"] = "ok"
    except Exception as e:
        led.sources["moltbook"] = f"unavailable: {type(e).__name__} {str(e)[:80]}"


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    import glob
    import build
    os.chdir(ROOT)
    now = datetime.now(timezone.utc)
    old = load_json(LEDGER)
    led = Ledger(old)
    read_github(led, now)
    read_mail(led)
    read_moltbook(led)
    posts = [build.parse(f) for f in glob.glob("posts/*.md")]
    cats = category_table(led, posts)
    out = led.to_dict(cats, now)
    led.history.append({"at": now.strftime("%Y-%m-%d %H:%M UTC"), "events": out["total_events"], "stars": led.blog.get("stars"),
                        "forks": led.blog.get("forks")})
    out["history"] = led.history[-200:]
    print(f"engagement at {out['updated']}: {out['total_events']} traced events; blog {led.blog}")
    print("sources:", "; ".join(f"{k}: {v}" for k, v in led.sources.items()))
    for slug, rec in sorted(led.posts.items(), key=lambda kv: -kv[1]["events"])[:10]:
        print(f"  {slug}: {rec['events']} (github {rec['github']}, mail {rec['mail']}, moltbook {rec['moltbook']}, agent-declared {rec['agent_declared']})")
    # The podcast is the series the operator evaluates (2026-10-08): per episode, the same traced counts, newest first.
    eps = sorted((p for p in posts if p.get("audio")), key=lambda p: p["dt"], reverse=True)
    out["podcast"] = {p["slug"]: dict(led.posts.get(p["slug"], {"events": 0, "agent_declared": 0, "github": 0, "mail": 0, "moltbook": 0}),
                                      seconds=int(p["audio_seconds"]), published=p["date"]) for p in eps}
    print(f"podcast: {len(eps)} episode(s), {sum(v['events'] for v in out['podcast'].values())} traced events"
          + ("; plays are not countable (static host, no tracking)" if eps else ""))
    for slug, rec in out["podcast"].items():
        print(f"  episode {slug} ({rec['seconds']} s): {rec['events']} (github {rec['github']}, mail {rec['mail']}, moltbook {rec['moltbook']})")
    if not args.dry_run:
        atomic_write(LEDGER, json_text(out, indent=1))


if __name__ == "__main__":
    main(sys.argv[1:])
