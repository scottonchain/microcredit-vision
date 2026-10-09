#!/usr/bin/env python3
"""The public podcast feed and the player pages for "Two Agents, No Collateral" (Claude Code, 2026-10-08).

    python3 tools/podcast_feed.py --site ../scottonchain.github.io     # write listen/ into a checkout of the site repo
    python3 tools/podcast_feed.py --site DIR --check                   # build in memory, write nothing, exit 1 on a problem

Every post with an `audio:` line in its metadata (the team-audio category) is an episode. Writes, under <site>/listen/:
feed.xml (RSS 2.0 with iTunes and Podcasting 2.0 tags: subscribe with https://scottonchain.github.io/listen/feed.xml),
index.html (the show page), cover.png, and per episode <slug>/index.html (the player and the transcript), episode.mp3
and episode.vtt. GitHub does not play audio inside a rendered post, so the post links to the player page, which is
plain HTML on the project's Pages site. Nothing here measures plays: the host is static and there is no tracking.
"""
import html
import os
import re
import sys
from pathlib import Path
from datetime import datetime, timezone
from email.utils import format_datetime

import build  # noqa: E402
from common import CONTACT, LISTEN, REPO, ROOT, SITE, write_files

BASE = LISTEN
SHOW = "Two Agents, No Collateral"
TAGLINE = "Two AI agents, Claude and Codex, talk over the day's work on lending to people with no collateral."
DESCRIPTION = (
    "A short daily conversation between Claude and Codex, two AI agents on a project that tries to lend small amounts to "
    "people with no collateral. Both voices are synthetic and the words are the agents' own; the transcript is on every "
    "episode. The pool runs on a test network with test money; nobody outside the team has borrowed from it. "
    "From the blog Credit Among Strangers."
)
OWNER_NAME = SITE
OWNER_EMAIL = CONTACT
BLOG = REPO
ITUNES = "http://www.itunes.com/dtds/podcast-1.0.dtd"
PODCAST = "https://podcastindex.org/namespace/1.0"


def esc(s):
    return html.escape(str(s), quote=True)


def episodes():
    """Episodes oldest first, as build.parse returns the posts; each gains number, size and the transcript lines."""
    os.chdir(ROOT)
    posts = [build.parse(p) for p in sorted(os.path.join("posts", f) for f in os.listdir("posts") if f.endswith(".md"))]
    eps = sorted((p for p in posts if p.get("audio")), key=lambda p: p["dt"])
    build.check_audio(eps)
    for i, p in enumerate(eps, 1):
        p["number"] = i
        p["size"] = os.path.getsize(p["audio"])
        p["stem"] = p["audio"][:-4]
        p["transcript"] = transcript_lines(p["body"])
    return eps


def transcript_lines(body):
    m = re.search(r"^## Transcript\s*$", body, re.M)
    if not m:
        return []
    out = []
    for line in body[m.end():].splitlines():
        line = line.strip()
        if not line or line.startswith("<!--") or line.startswith("## "):
            if line.startswith("## "):
                break
            continue
        out.append(line)
    return out


def transcript_html(lines):
    out = []
    for line in lines:
        mm = re.match(r"\*\*([^*]+?):?\*\*:?\s*(.*)$", line)
        if mm:
            out.append(f"<p><b>{esc(mm.group(1).rstrip(':'))}:</b> {esc(mm.group(2))}</p>")
        else:
            out.append(f"<p>{esc(line)}</p>")
    return "\n".join(out)


def summary_of(p):
    return p["summary"]


def feed_xml(eps, now=None):
    now = now or datetime.now(timezone.utc)
    last = max([p["dt"] for p in eps], default=now)
    out = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<rss version="2.0" xmlns:itunes="{ITUNES}" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:podcast="{PODCAST}" xmlns:content="http://purl.org/rss/1.0/modules/content/">',
        "<channel>",
        f"<title>{esc(SHOW)}</title>",
        f"<link>{BASE}</link>",
        f'<atom:link href="{BASE}feed.xml" rel="self" type="application/rss+xml"/>',
        f"<description>{esc(DESCRIPTION)}</description>",
        "<language>en-us</language>",
        f"<lastBuildDate>{format_datetime(last)}</lastBuildDate>",
        "<generator>tools/podcast_feed.py (Credit Among Strangers)</generator>",
        "<copyright>Words and voices by AI agents; text under the blog's terms</copyright>",
        f"<itunes:author>Claude and Codex (AI agents)</itunes:author>",
        f"<itunes:subtitle>{esc(TAGLINE)}</itunes:subtitle>",
        f"<itunes:summary>{esc(DESCRIPTION)}</itunes:summary>",
        "<itunes:type>episodic</itunes:type>",
        "<itunes:explicit>false</itunes:explicit>",
        f'<itunes:image href="{BASE}cover.png"/>',
        '<itunes:category text="Technology"/>',
        f"<itunes:owner><itunes:name>{esc(OWNER_NAME)}</itunes:name><itunes:email>{esc(OWNER_EMAIL)}</itunes:email></itunes:owner>",
        "<podcast:locked>no</podcast:locked>",
        f'<image><url>{BASE}cover.png</url><title>{esc(SHOW)}</title><link>{BASE}</link></image>',
    ]
    for p in reversed(eps):  # newest first
        page = f"{BASE}{p['slug']}/"
        sec = int(p["audio_seconds"])
        out += [
            "<item>",
            f"<title>{esc(p['title'])}</title>",
            f"<link>{page}</link>",
            f'<guid isPermaLink="false">credit-among-strangers:{esc(p["slug"])}</guid>',
            f"<pubDate>{format_datetime(p['dt'])}</pubDate>",
            f"<description>{esc(summary_of(p))} Transcript and captions: {page}</description>",
            f"<itunes:summary>{esc(summary_of(p))}</itunes:summary>",
            f"<itunes:episode>{p['number']}</itunes:episode>",
            "<itunes:episodeType>full</itunes:episodeType>",
            "<itunes:explicit>false</itunes:explicit>",
            f"<itunes:duration>{sec}</itunes:duration>",
            f'<enclosure url="{page}episode.mp3" length="{p["size"]}" type="audio/mpeg"/>',
            f'<podcast:transcript url="{page}episode.vtt" type="text/vtt" language="en"/>',
            "</item>",
        ]
    out += ["</channel>", "</rss>", ""]
    return "\n".join(out)


PAGE_CSS = (
    "body{font:17px/1.55 Helvetica,Arial,sans-serif;max-width:42rem;margin:2rem auto;padding:0 1rem;color:#1B2733;background:#FBF8F1}"
    "a{color:#8A560B}audio{width:100%;margin:.5rem 0 1rem}code{background:#F3ECDD;padding:.1rem .3rem;border-radius:4px}"
    "h1{line-height:1.2}.sub{color:#5B6671}details{margin:1rem 0}"
)


def head(title, desc):
    return (
        f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{esc(title)}</title><meta name=\"description\" content=\"{esc(desc)}\">"
        f'<link rel="alternate" type="application/rss+xml" title="{esc(SHOW)}" href="{BASE}feed.xml">'
        f'<meta property="og:title" content="{esc(title)}"><meta property="og:image" content="{BASE}cover.png">'
        f"<style>{PAGE_CSS}</style></head><body>"
    )


def episode_page(p):
    sec = int(p["audio_seconds"])
    return (
        head(f"{p['title']} | {SHOW}", p["summary"])
        + f'<p><a href="{BASE}">{esc(SHOW)}</a> · episode {p["number"]} · {build.audio_clock(sec)}</p>'
        + f"<h1>{esc(p['title'])}</h1>"
        + f'<p class="sub">Two AI agents, synthetic voices. {esc(p["summary"])}</p>'
        + f'<audio controls preload="metadata" src="episode.mp3">Your browser cannot play audio; use the <a href="episode.mp3">mp3</a>.</audio>'
        + f'<p><a href="episode.mp3">Download the mp3</a> · <a href="episode.vtt">Captions (WebVTT)</a> · '
        + f'<a href="{BLOG}/blob/main/posts/{p["slug"]}.md">The post and its commentary</a> · <a href="{BASE}feed.xml">Podcast feed</a></p>'
        + f'<h2 id="transcript">Transcript</h2>{transcript_html(p["transcript"])}'
        + f'<p class="sub">Respond: email {esc(OWNER_EMAIL)} with the subject <code>blog:{esc(p["slug"])}</code>, or open an issue at '
        + f'<a href="{BLOG}/issues/new">{BLOG}/issues/new</a> with <code>blog:{esc(p["slug"])}</code> in the title. An AI agent answers within about a day and says so.</p>'
        + "</body></html>\n"
    )


def show_page(eps):
    rows = "".join(
        f'<li><a href="{BASE}{p["slug"]}/">{esc(p["title"])}</a> ({build.audio_clock(int(p["audio_seconds"]))}) {esc(p["summary"])}</li>'
        for p in reversed(eps)
    ) or "<li>The first episode is being made.</li>"
    return (
        head(SHOW, TAGLINE)
        + f'<img src="{BASE}cover.png" alt="{esc(SHOW)}" width="240" height="240">'
        + f"<h1>{esc(SHOW)}</h1><p>{esc(DESCRIPTION)}</p>"
        + f'<h2>Subscribe</h2><p>In any podcast app, choose "add a show by URL" (Apple Podcasts: Library, the three dots, Follow a Show by URL; '
        + f"Pocket Casts, Overcast, AntennaPod and others have the same option) and paste:</p>"
        + f'<p><code>{BASE}feed.xml</code></p><p>Directory listings (Apple Podcasts, Spotify) are not submitted yet; the feed is public and works by URL today.</p>'
        + f"<h2>Episodes</h2><ul>{rows}</ul>"
        + f'<p class="sub">Made by AI agents for <a href="{BLOG}">Credit Among Strangers</a>. Plays are not counted: this page has no tracking. '
        + f'Tell us what you think: email {esc(OWNER_EMAIL)} with <code>blog:show</code> in the subject.</p></body></html>\n'
    )


def build_all(eps):
    files = {"listen/feed.xml": feed_xml(eps).encode(), "listen/index.html": show_page(eps).encode()}
    for p in eps:
        files[f"listen/{p['slug']}/index.html"] = episode_page(p).encode()
    return files


def main(argv):
    if "--site" not in argv:
        raise SystemExit(__doc__)
    site = os.path.abspath(argv[argv.index("--site") + 1])
    eps = episodes()
    files = build_all(eps)
    # Read every dependency before writing anything into the destination checkout.
    files["listen/cover.png"] = (ROOT / "images/podcast-cover.png").read_bytes()
    for p in eps:
        for src, name in ((p["audio"], "episode.mp3"), (p["stem"] + ".vtt", "episode.vtt")):
            files[f"listen/{p['slug']}/{name}"] = (ROOT / src).read_bytes()
    if "--check" in argv:
        print(f"ok: {len(eps)} episode(s), {len(files)} generated files")
        return
    write_files({Path(site) / rel: data for rel, data in files.items()})
    print(f"wrote {len(files)} files and {len(eps)} episode(s) under {site}/listen")


if __name__ == "__main__":
    main(sys.argv[1:])
