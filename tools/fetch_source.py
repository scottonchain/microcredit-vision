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
import xml.etree.ElementTree as ET

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129 Safari/537.36"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def strip(htm):
    t = re.sub(r"(?is)<(script|style).*?</\1>", " ", htm)
    t = re.sub(r"(?s)<[^>]+>", " ", t)
    t = html.unescape(t)
    return re.sub(r"[ \t]+", " ", re.sub(r"\s*\n\s*", "\n", t)).strip()


def main():
    url = sys.argv[1]
    pick = sys.argv[2] if len(sys.argv) > 2 else ""
    os.makedirs("out", exist_ok=True)
    raw = get(url)
    notes = [f"fetched {url} ({len(raw)} bytes)"]
    page_url = url
    if raw.lstrip().startswith(b"<?xml") or b"<rss" in raw[:2000]:
        root = ET.fromstring(raw)
        items = root.findall(".//item")
        notes.append(f"rss with {len(items)} items; newest first:")
        chosen = None
        for it in items[:15]:
            title = (it.findtext("title") or "").strip()
            link = (it.findtext("link") or "").strip()
            pub = (it.findtext("pubDate") or "").strip()
            enc = it.find("enclosure")
            audio = enc.get("url") if enc is not None else ""
            desc = strip(it.findtext("description") or "")[:600]
            notes.append(f"- {pub} | {title} | {link} | audio: {audio}\n  {desc}")
            if chosen is None and (not pick or pick.lower() in title.lower()):
                chosen = (title, link, audio)
        if chosen and chosen[1]:
            page_url = chosen[1]
            notes.append(f"fetching chosen item page: {page_url}")
            raw = get(page_url)
    open("out/source.html", "wb").write(raw)
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
