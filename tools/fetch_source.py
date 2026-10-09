#!/usr/bin/env python3
"""Fetch a public source the session cannot reach, for the news watch. Runs in GitHub Actions.

Given a URL: if it is an RSS feed, list its newest items and fetch the newest item's page; otherwise
fetch the page. Writes source.html (raw) and source.txt (text with tags stripped, plus any
transcript-like JSON found in the page) into out/, which the workflow uploads as a short-lived
artifact. Nothing is committed to the repository.
"""
import html
import json
import os
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129 Safari/537.36"}


def get(url):
    """Fetch with a browser-like header; on refusal try a text-rendering reader as a fallback."""
    parsed = urlsplit(url)
    if parsed.scheme not in ("https", "http") or not parsed.netloc or parsed.username or parsed.password:
        raise ValueError("source URLs must be public http(s) URLs without embedded credentials")
    try:
        req = urllib.request.Request(url, headers={**UA, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.9"})
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read()
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"direct fetch failed for {url}: {e}\n")
        req = urllib.request.Request("https://r.jina.ai/" + url, headers=UA)
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.read()


def strip(htm):
    t = re.sub(r"(?is)<(script|style).*?</\1>", " ", htm)
    t = re.sub(r"(?s)<[^>]+>", " ", t)
    t = html.unescape(t)
    return re.sub(r"[ \t]+", " ", re.sub(r"\s*\n\s*", "\n", t)).strip()


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: fetch_source.py URL [title fragment]")
    url = sys.argv[1]
    pick = sys.argv[2] if len(sys.argv) > 2 else ""
    os.makedirs("out", exist_ok=True)
    # A later invocation with no matching enclosure must not reuse an earlier source's audio.
    Path("out/chosen.json").unlink(missing_ok=True)
    raw = get(url)
    notes = [f"fetched {url} ({len(raw)} bytes)"]
    page_url = url
    if raw.lstrip().startswith(b"<?xml") or b"<rss" in raw[:2000]:
        root = ET.fromstring(raw)
        items = root.findall(".//item")
        notes.append(f"rss with {len(items)} items; newest first:")
        chosen = None
        for index, it in enumerate(items):
            title = (it.findtext("title") or "").strip()
            link = (it.findtext("link") or "").strip()
            pub = (it.findtext("pubDate") or "").strip()
            enc = it.find("enclosure")
            audio = enc.get("url") if enc is not None else ""
            desc = strip(it.findtext("description") or "")[:600]
            if index < 15:
                notes.append(f"- {pub} | {title} | {link} | audio: {audio}\n  {desc}")
            if chosen is None and (not pick or pick.lower() in title.lower()):
                chosen = (title, link, audio)
        if chosen:
            Path("out/chosen.json").write_text(json.dumps({"title": chosen[0], "link": chosen[1], "audio": chosen[2]}), encoding="utf-8")
        elif pick:
            raise SystemExit(f"no RSS item matches {pick!r}; no source was selected")
        if chosen and chosen[1]:
            page_url = chosen[1]
            notes.append(f"fetching chosen item page: {page_url}")
            try:
                raw = get(page_url)
            except Exception as e:  # noqa: BLE001
                notes.append(f"page fetch failed: {e}")
                raw = b""
    Path("out/source.html").write_bytes(raw)
    text = strip(raw.decode("utf-8", "replace"))
    # transcript-like blobs embedded as JSON
    blobs = re.findall(r'"transcript"\s*:\s*(\{.*?\}|\[.*?\])', raw.decode("utf-8", "replace"), re.S)
    with open("out/source.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(notes) + "\n\n===== PAGE TEXT =====\n" + text + "\n")
        if blobs:
            f.write("\n===== TRANSCRIPT JSON =====\n" + "\n".join(b[:200000] for b in blobs))
    print("\n".join(notes[:20]))
    print("text chars", len(text), "transcript blobs", len(blobs))


if __name__ == "__main__":
    main()
