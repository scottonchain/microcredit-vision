#!/usr/bin/env python3
"""The blog's YouTube watch (operator direction, 2026-10-07): a few channels, AI-related episodes only,
one reply per episode, never later than 24 hours after release, with the video's own thumbnail (play button added)
linking back to it.

    python3 tools/youtube_watch.py scan                 # new episodes on the watched channels, newest first (JSON)
    python3 tools/youtube_watch.py details <video id>   # title, channel, published, length, description, caption tracks,
                                                        # and the complete English transcript as plain text (JSON)
    python3 tools/youtube_watch.py thumbnail <video id> # writes images/youtube/<id>.png: the thumbnail at 80% of YouTube's size (1024x576) with a play button
    python3 tools/youtube_watch.py answered <video id> <post slug>   # records the reply so the episode is never answered twice

Channels are in editorial/youtube-channels.json (a channel_id, or a playlist_id for a show inside a bigger channel);
replies in editorial/youtube-answered.json. Needs network access to youtube.com and its subdomains (i.ytimg.com or
img.youtube.com for thumbnails) and, for the thumbnail, Chromium through Playwright.
"""
import json
import os
import re
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CHANNELS = os.path.join(ROOT, "editorial", "youtube-channels.json")
ANSWERED = os.path.join(ROOT, "editorial", "youtube-answered.json")
WINDOW = timedelta(hours=24)
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def fetch(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.8"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "replace")


def load(path, default):
    return json.load(open(path, encoding="utf-8")) if os.path.exists(path) else default


def scan():
    channels = load(CHANNELS, [])
    answered = load(ANSWERED, {})
    now = datetime.now(timezone.utc)
    ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015", "media": "http://search.yahoo.com/mrss/"}
    out = []
    for ch in channels:
        feed = (f"https://www.youtube.com/feeds/videos.xml?playlist_id={ch['playlist_id']}" if ch.get("playlist_id")
                else f"https://www.youtube.com/feeds/videos.xml?channel_id={ch['channel_id']}")
        try:
            xml = fetch(feed)
        except Exception as e:  # a feed that fails is reported, not fatal
            out.append({"channel": ch["name"], "error": str(e)})
            continue
        root = ET.fromstring(xml)
        for entry in root.findall("a:entry", ns):
            vid = entry.findtext("yt:videoId", "", ns)
            published = datetime.fromisoformat(entry.findtext("a:published", "", ns).replace("Z", "+00:00"))
            age = now - published
            out.append({
                "channel": ch["name"], "who": ch.get("who", ""), "id": vid,
                "title": entry.findtext("a:title", "", ns),
                "url": f"https://www.youtube.com/watch?v={vid}",
                "published": published.strftime("%Y-%m-%d %H:%M UTC"),
                "age_hours": round(age.total_seconds() / 3600, 1),
                "in_window": age <= WINDOW,
                "answered": answered.get(vid, {}).get("post"),
                "description": (entry.findtext("media:group/media:description", "", ns) or "")[:400],
            })
    out.sort(key=lambda e: e.get("published", ""), reverse=True)
    return out


INNERTUBE_CLIENTS = (
    # Google's watch page answers curl with an anti-bot interstitial; the player API with a mobile client answers with
    # the same videoDetails, microformat and caption tracks (checked 2026-10-07). No key is sent or stored.
    {"clientName": "ANDROID", "clientVersion": "20.10.38", "androidSdkVersion": 30, "hl": "en", "gl": "US",
     "_ua": "com.google.android.youtube/20.10.38 (Linux; U; Android 11) gzip", "_name": "3"},
    {"clientName": "IOS", "clientVersion": "20.10.4", "deviceModel": "iPhone16,2", "hl": "en", "gl": "US",
     "_ua": "com.google.ios.youtube/20.10.4 (iPhone16,2; U; CPU iOS 18_3_2 like Mac OS X;)", "_name": "5"},
)


def player_response(video_id):
    for client in INNERTUBE_CLIENTS:
        body = {"context": {"client": {k: v for k, v in client.items() if not k.startswith("_")}},
                "videoId": video_id, "contentCheckOk": True, "racyCheckOk": True}
        req = urllib.request.Request(
            "https://www.youtube.com/youtubei/v1/player?prettyPrint=false", data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json", "User-Agent": client["_ua"],
                     "X-YouTube-Client-Name": client["_name"], "X-YouTube-Client-Version": client["clientVersion"]})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                pr = json.loads(r.read().decode("utf-8", "replace"))
        except Exception as e:
            sys.stderr.write(f"player API with {client['clientName']}: {e}\n")
            continue
        if pr.get("videoDetails", {}).get("videoId") == video_id and (
                pr.get("playabilityStatus", {}).get("status") == "OK" or pr.get("captions")):
            return pr
        sys.stderr.write(f"player API with {client['clientName']}: status {pr.get('playabilityStatus', {}).get('status')}\n")
    html = fetch(f"https://www.youtube.com/watch?v={video_id}")
    m = re.search(r"ytInitialPlayerResponse\s*=\s*(\{)", html)
    if not m:
        raise SystemExit("no ytInitialPlayerResponse in the page (consent wall or layout change)")
    i = m.start(1)
    depth = 0
    in_str = False
    esc = False
    for j in range(i, len(html)):
        c = html[j]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        elif c == '"':
            in_str = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return json.loads(html[i:j + 1])
    raise SystemExit("unterminated player response")


def transcript_text(base_url):
    url = base_url + ("&" if "?" in base_url else "?") + "fmt=json3"
    data = json.loads(fetch(url))
    lines, current_minute, buf = [], -1, []
    last_ms = 0
    for ev in data.get("events", []):
        segs = ev.get("segs")
        if not segs:
            continue
        t = int(ev.get("tStartMs", 0))
        last_ms = max(last_ms, t + int(ev.get("dDurationMs", 0)))
        text = "".join(s.get("utf8", "") for s in segs).replace("\n", " ").strip()
        if not text:
            continue
        minute = t // 60000
        if minute != current_minute:
            if buf:
                lines.append(" ".join(buf))
            buf = [f"[{minute // 60:02d}:{minute % 60:02d}:00]"]
            current_minute = minute
        buf.append(text)
    if buf:
        lines.append(" ".join(buf))
    text = "\n".join(lines)
    return text, last_ms


def details(video_id):
    pr = player_response(video_id)
    vd = pr.get("videoDetails", {})
    mf = pr.get("microformat", {}).get("playerMicroformatRenderer", {})
    tracks = pr.get("captions", {}).get("playerCaptionsTracklistRenderer", {}).get("captionTracks", [])
    track_list = [{"lang": t.get("languageCode"), "name": t.get("name", {}).get("simpleText") or "".join(r.get("text", "") for r in t.get("name", {}).get("runs", [])), "auto": t.get("kind") == "asr"} for t in tracks]
    english = [t for t in tracks if (t.get("languageCode") or "").startswith("en")]
    english.sort(key=lambda t: t.get("kind") == "asr")  # a human track first, then auto
    result = {
        "id": video_id, "url": f"https://www.youtube.com/watch?v={video_id}",
        "title": vd.get("title"), "channel": vd.get("author"), "channel_id": vd.get("channelId"),
        "length_seconds": int(vd.get("lengthSeconds") or 0),
        "publish_date": mf.get("publishDate"), "upload_date": mf.get("uploadDate"),
        "description": vd.get("shortDescription", ""),
        "caption_tracks": track_list,
    }
    if english:
        text, last_ms = transcript_text(english[0]["baseUrl"])
        result["transcript_auto_generated"] = english[0].get("kind") == "asr"
        result["transcript_words"] = len(text.split())
        result["transcript_last_second"] = last_ms // 1000
        result["transcript_complete"] = result["length_seconds"] == 0 or last_ms // 1000 >= result["length_seconds"] - 90
        result["transcript"] = text
    else:
        result["transcript"] = None
    return result


PLAY_HTML = """<!doctype html><html><body style="margin:0;background:#000">
<div style="position:relative;width:1024px;height:576px;overflow:hidden">
<img src="data:image/jpeg;base64,{b64}" style="width:1024px;height:576px;object-fit:cover">
<div style="position:absolute;left:50%;top:50%;width:109px;height:77px;margin:-38px 0 0 -54px;background:#f00;border-radius:22px;opacity:0.92"></div>
<div style="position:absolute;left:50%;top:50%;margin:-19px 0 0 -13px;width:0;height:0;border-top:19px solid transparent;border-bottom:19px solid transparent;border-left:32px solid #fff"></div>
</div></body></html>"""


def thumbnail(video_id, local_jpg=None):
    import base64
    jpg = open(local_jpg, "rb").read() if local_jpg else None
    for name in () if jpg else ("maxresdefault.jpg", "sddefault.jpg", "hqdefault.jpg"):
        for host in ("i.ytimg.com", "img.youtube.com"):  # the second serves the same files where a network policy allows only youtube.com
            try:
                jpg = fetch(f"https://{host}/vi/{video_id}/{name}", binary=True)
                if len(jpg) > 2000:
                    break
                jpg = None  # YouTube answers a missing size with a tiny placeholder
            except Exception:
                jpg = None
        if jpg:
            break
    if not jpg:
        raise SystemExit("no thumbnail available")
    os.makedirs(os.path.join(ROOT, "images", "youtube"), exist_ok=True)
    html_path = os.path.join(ROOT, "images", "youtube", f"{video_id}.html")
    out_path = os.path.join(ROOT, "images", "youtube", f"{video_id}.png")
    open(html_path, "w").write(PLAY_HTML.replace("{b64}", base64.b64encode(jpg).decode()))
    pw = "/opt/node-tools/node_modules/playwright"
    script = f"""
const {{ chromium }} = require({json.dumps(pw)});
(async () => {{ const b = await chromium.launch(); const p = await b.newPage({{viewport:{{width:1024,height:576}}}});
await p.goto("file://{html_path}"); await p.screenshot({{path: {json.dumps(out_path)}}}); await b.close(); }})();"""
    subprocess.run(["node", "-e", script], check=True)
    os.remove(html_path)
    return out_path


def mark_answered(video_id, slug):
    answered = load(ANSWERED, {})
    answered[video_id] = {"post": slug, "answered": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}
    json.dump(answered, open(ANSWERED, "w", encoding="utf-8"), indent=2)
    open(ANSWERED, "a").write("\n")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "scan"
    if cmd == "scan":
        print(json.dumps(scan(), indent=1, ensure_ascii=False))
    elif cmd == "details":
        print(json.dumps(details(sys.argv[2]), indent=1, ensure_ascii=False))
    elif cmd == "thumbnail":  # thumbnail <id> [--from local.jpg]
        print(thumbnail(sys.argv[2], sys.argv[4] if len(sys.argv) > 4 and sys.argv[3] == "--from" else None))
    elif cmd == "answered":
        mark_answered(sys.argv[2], sys.argv[3])
        print("recorded")
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
