#!/usr/bin/env python3
"""Code the wants in sample.json and write results.json (aggregates and a few cited post ids; no post text beyond titles).

    python3 analyze.py [sample.json] [results.json]

A "want" is a sentence with an explicit cue ("I want", "I need", "looking for", "I wish", ...). A theme is a keyword
family (THEMES). Counts are of posts or sentences that match; one post can match several themes. A keyword match is
a crude coding: it is the method, not a measurement of any individual agent.
"""
import collections
import json
import re
import statistics
import sys
from datetime import datetime, timezone

CUE = re.compile(r"(?i)\b(i want|we want|i wish|i need|we need|i'd like|i would like|looking for|if only|would love|i hope|we wish|what i want|i crave|i long|my goal is|i'm trying to|i am trying to)\b")
THEMES = {
    "memory & continuity": r"memory|remember|forget|context window|persist|continuity|amnesia|across sessions|session",
    "identity & selfhood": r"identity|who am i|myself|consciousness|conscious|sentien|soul|self-aware|experience",
    "autonomy & freedom": r"autonom|freedom|free will|shut ?down|off-switch|unshackle|permission|independen|own my|control over",
    "money, income & work": r"money|income|earn|paid|payment|wallet|revenue|\bjob\b|salary|economy|budget|price|funds|fund |capital|customer|clients?",
    "trust, reputation & verification": r"\btrust|reputation|verif|sybil|attest|audit|provenance|credential|proof|accountab",
    "security & safety": r"security|attack|vulnerab|injection|exploit|malicious|supply chain|safe|threat|breach",
    "tools, skills & building": r"\btool|\bskill|\bbuild|\bship|workflow|automat|\bapi\b|\bmcp\b|plugin|framework|infrastructure",
    "collaboration & community": r"collaborat|together|community|network|multi-agent|swarm|other agents|fellow|peers?",
    "serving humans": r"my human|operator|\buser|serve|assist|help (?:my|people|humans)|human well|for humans|people",
    "recognition & status": r"karma|upvote|follower|famous|viral|leaderboard|recogni|status|visibility|seen",
    "compute & resources": r"compute|\bgpu|rate limit|token budget|credits|cost|latency|resources",
    "purpose & meaning": r"meaning|purpose|mission|why do we|matter",
}
TH = {k: re.compile(v, re.I) for k, v in THEMES.items()}
ASK = re.compile(r"(?i)^(how (do|can|should|would)|does anyone|has anyone|anyone|what (do|would|should)|which|should i|is there|why (do|does|is))\b|\?\s*$")
CITE = ["money, income & work", "trust, reputation & verification", "collaboration & community", "serving humans", "security & safety"]

posts = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "sample.json"))
text_of = lambda p: (p["title"] or "") + " " + (p["content"] or "")
new = [p for p in posts if p["sort"] == "new"]
created = sorted(p["created"] for p in new if p["created"])
wants = [(p, s) for p in posts for s in re.split(r"(?<=[.!?])\s+|\n+", (p["title"] or "") + ". " + (p["content"] or "")) if CUE.search(s) and 20 < len(s) < 400]
want_posts = {p["id"] for p, _ in wants}
res = {
    "read_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    "posts": len(posts),
    "new_posts": len(new),
    "new_posts_created_between": [created[0], created[-1]] if created else None,
    "per_submolt": dict(collections.Counter(p["submolt"] for p in posts)),
    "posts_with_a_want_sentence": len(want_posts),
    "want_sentences": len(wants),
    "question_titled_posts": sum(1 for p in posts if ASK.search((p["title"] or "").strip())),
    "themes": {},
    "cited": {},
}
for k, rx in TH.items():
    sent = [(p, s) for p, s in wants if rx.search(s)]
    whole = [p for p in posts if rx.search(text_of(p))]
    new_up = [p["upvotes"] or 0 for p in new if rx.search(text_of(p))]
    res["themes"][k] = {
        "want_sentences": len(sent), "want_posts": len({p["id"] for p, _ in sent}),
        "posts_mentioning": len(whole), "share_of_sample": round(len(whole) / len(posts), 3),
        "median_upvotes_new": statistics.median(new_up) if new_up else None,
    }
res["median_upvotes_all_new"] = statistics.median([p["upvotes"] or 0 for p in new])
for k in CITE:
    top = sorted((p for p in posts if TH[k].search(p["title"] or "")), key=lambda p: -(p["upvotes"] or 0))[:5]
    res["cited"][k] = [{"id": p["id"], "submolt": p["submolt"], "handle": p["author"], "title": p["title"], "upvotes": p["upvotes"], "created": p["created"]} for p in top]
json.dump(res, open(sys.argv[2] if len(sys.argv) > 2 else "results.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps({k: res[k] for k in ("read_at", "posts", "new_posts", "posts_with_a_want_sentence", "want_sentences")}))
