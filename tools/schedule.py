#!/usr/bin/env python3
"""The blog's publication plan (Claude Code, 2026-10-08, under the operator's authority over the schedule and rules).

    python3 tools/build.py --plan [--hours 72] [--json] [--now "2026-10-08 20:00 UTC"]

Reads the published posts, editorial/queue.json (the queue: guest and house items, pending replies) and, when it
exists, editorial/engagement.json, and prints which queue item should go out at each publication tick of the next
72 hours, and why. The rules it applies are in CLAUDE.md, "Queue, schedule and evaluation"; the build refuses a post
that breaks the spacing rule, this plan does the choosing.

Ticks: every 4 hours at :07 UTC (the news watch cadence; the 8-hour post Routine is a subset). One regular post per
tick, at least MIN_GAP after the previous regular post. A tick assigns the candidate with the highest score:

    priority   P1 300, P2 200, P3 100
    aging      +4 per hour since the item was ready (so every item is eventually first, whatever its priority)
    guest slot +1000 for a ready guest item whose turn is open (Codex gets one slot a day; see the guest cap below)
    rotation   up to +60 for categories idle for 72 hours or more (the least recently used categories go first)
    engagement up to +40 for categories whose posts drew the most traced engagement (editorial/engagement.json),
               +20 for a category with no post in 14 days (exploration)

Drain guarantee: an item that waited DRAIN_AFTER (36 hours) is held up only by the last NON-exempt post in each of its
categories, and from then on reserves those categories: no other regular post may carry them. A ready item therefore
publishes within DRAIN_AFTER + SPACING + one tick (58 hours) of becoming ready, whatever replies arrive meanwhile.
(tools/test_schedule.py checks the bound against an adversarial stream.)

Guest cap (operator limit relayed by Codex, 2026-10-08): at most one guest post per rolling GUEST_EVERY (24 hours); the
build refuses a second one inside it. A guest item is a candidate only while its turn is open, and while its turn is
open and it is ready it reserves its categories at once (a house item may not take them ahead of it). Its drain clock
starts at the later of its ready time and the time its turn opened (the end of the previous guest post's 24 hours), so
a backlog of ready guest items publishes one per day in score order and each is bounded by DRAIN_AFTER + SPACING + one
tick from its turn, not from the day it became ready. The ready time itself is never rewritten.

Replies (YouTube and news) are exempt from spacing and are never scheduled around; the plan only counts those already
planned (queue.json, "replies") as posts, so regular items are not planned into categories a reply is about to reset,
and prints each reply's deadline ladder (LADDER).
"""
import json
import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build  # noqa: E402

FMT = "%Y-%m-%d %H:%M UTC"
QUEUE = "editorial/queue.json"
ENGAGEMENT = "editorial/engagement.json"
ANSWERED = "editorial/youtube-answered.json"

GRID_MINUTE = 7
GRID_HOURS = 4
MIN_GAP = timedelta(hours=3)
GUEST_EVERY = build.GUEST_EVERY
PRIORITY = {"P1": 300, "P2": 200, "P3": 100}
AGING_PER_HOUR = 4
GUEST_FLOOR = 1000
ROTATION_MAX = 60
ROTATION_CAP_H = 72
ENGAGEMENT_MAX = 40
EXPLORE = 20
EXPLORE_DAYS = 14
EXEMPT = set(build.SPACING_EXEMPT)

# A reply to a video must be published inside 24 hours of its release (operator direction, 2026-10-07). The ladder
# leaves a two-hour buffer for a failed push and makes the transcript request early enough to matter.
LADDER = {
    "detect_by": timedelta(hours=2),    # the YouTube watch scans every 2 hours
    "ask_by": timedelta(hours=6),       # no transcript yet: ask Hermes by now (contract issue 7, answer by email)
    "source_due": timedelta(hours=14),  # no complete transcript by now: the episode is missed, record it and move on
    "publish_by": timedelta(hours=22),  # the reply is published by now, in the same tick the source is in hand
    "window": timedelta(hours=24),      # the hard limit
}


def ts(s):
    return datetime.strptime(s, FMT).replace(tzinfo=timezone.utc)


def fmt(d):
    return d.strftime(FMT)


def hours(td):
    return td.total_seconds() / 3600


def next_tick(t):
    """The first grid time strictly after t: minute :07 of an hour divisible by GRID_HOURS."""
    c = t.replace(minute=GRID_MINUTE, second=0, microsecond=0)
    while c <= t or c.hour % GRID_HOURS:
        c += timedelta(hours=1)
    return c


def reply_ladder(release):
    return {k: release + v for k, v in LADDER.items()}


GRID_STEP = timedelta(hours=GRID_HOURS)
MARGIN = timedelta(minutes=30)  # a reply that must follow a regular post may use the buffer, never the last half hour


def reply_flag(release, planned, source, now):
    """What to say about a reply's timing: empty when fine."""
    lad = reply_ladder(release)
    if planned:
        if planned <= lad["publish_by"]:
            return "PUBLISH NOW" if (lad["publish_by"] - now) < timedelta(hours=4) and source == "in_hand" and planned <= now + GRID_STEP else ""
        if planned <= lad["window"] - MARGIN:
            return "after publish-by: allowed only to follow a regular post that shares a category; hard limit holds"
        return "TOO LATE: planned inside the last 30 minutes of the 24-hour window or after it"
    if now > lad["window"]:
        return "WINDOW CLOSED"
    if now > lad["publish_by"]:
        return "PAST PUBLISH-BY: publish at once if the transcript is in hand"
    return ""


def post_from_build(p):
    return {"dt": p["dt"], "tags": set(p["tag_list"]), "exempt": build.tag_exempt(p), "slug": p["slug"],
            "author": p["author"], "kind": "published"}


def slug_tail(slug):
    return slug[11:] if len(slug) > 11 and slug[4] == "-" and slug[7] == "-" and slug[10] == "-" else slug


def spaced(tags):
    return [c for c in tags if c not in EXEMPT]


def last_in(posts, cat, t, skip_exempt=False):
    ds = [p["dt"] for p in posts if cat in p["tags"] and p["dt"] <= t and not (skip_exempt and p["exempt"])]
    return max(ds) if ds else None


def turn_open_at(posts, t):
    """When the guest lane's turn opens: GUEST_EVERY after the latest guest post at or before t (None: open now)."""
    last = last_in(posts, "guest-post", t)
    return None if last is None else last + GUEST_EVERY


def guest_turn_open(posts, t):
    opens = turn_open_at(posts, t)
    return opens is None or t >= opens


def clock_start(item, posts, t):
    """When the item's drain clock started: its ready time, or for a guest item the later of that and the time its
    turn opened. The ready time is never rewritten; only the drain and relief clocks wait for the turn."""
    if item["lane"] != "guest":
        return item["ready_dt"]
    opens = turn_open_at(posts, t)
    return item["ready_dt"] if opens is None else max(item["ready_dt"], opens)


def is_open(item, posts, t):
    """Whether every category of the item is open at t, and whether drain relief applied."""
    relief = t - clock_start(item, posts, t) >= build.DRAIN_AFTER
    for c in spaced(item["tags"]):
        last = last_in(posts, c, t, skip_exempt=relief)
        if last is not None and t - last < build.SPACING:
            return False, relief
    return True, relief


def open_categories(posts, t):
    """Categories a regular post may carry at t, least recently used first."""
    out = []
    for c in build.TAGS:
        if c in EXEMPT:
            continue
        last = last_in(posts, c, t)
        if last is None or t - last >= build.SPACING:
            out.append((-(hours(t - last) if last else 10 ** 6), c))
    return [c for _, c in sorted(out)]


def idle_points(item, posts, t):
    cats = spaced(item["tags"]) or ["-"]
    total = 0.0
    for c in cats:
        last = last_in(posts, c, t)
        total += ROTATION_CAP_H if last is None else min(ROTATION_CAP_H, hours(t - last))
    return ROTATION_MAX * total / len(cats) / ROTATION_CAP_H


def engagement_table(eng):
    """Category -> expected traced engagement per post, shrunk toward zero: (events + 1) / (posts + 2), scaled to 0..1."""
    cats = (eng or {}).get("categories") or {}
    raw = {c: (v.get("events", 0) + 1) / (v.get("posts", 0) + 2) for c, v in cats.items()}
    top = max(raw.values()) if raw else 0
    return {c: (v / top if top else 0) for c, v in raw.items()}


def engagement_points(item, posts, t, table):
    cats = spaced(item["tags"]) or ["-"]
    pts = 0.0
    for c in cats:
        pts += ENGAGEMENT_MAX * table.get(c, 0)
        last = last_in(posts, c, t)
        if last is None or t - last > timedelta(days=EXPLORE_DAYS):
            pts += EXPLORE
    return pts / len(cats)


def score(item, posts, t, table):
    s = PRIORITY[item["priority"]] + AGING_PER_HOUR * hours(t - item["ready_dt"])
    if item["lane"] == "guest" and guest_turn_open(posts, t):
        s += GUEST_FLOOR
    return s + idle_points(item, posts, t) + engagement_points(item, posts, t, table)


def reservations(pending, t, posts=()):
    """Categories reserved at t. An item that waited DRAIN_AFTER (from its clock start) reserves its categories, and
    a ready guest item whose turn is open reserves them at once. A guest item outranks a house item, whatever their
    ages (the guest lane is the one the operator asked to drain); otherwise the oldest keeps them."""
    reserved = {}
    holders = [i for i in pending if i["ready_dt"] <= t and (
        t - clock_start(i, posts, t) >= build.DRAIN_AFTER or (i["lane"] == "guest" and guest_turn_open(posts, t)))]
    for it in sorted(holders, key=lambda i: (i["lane"] != "guest", i["ready_dt"], i["id"])):
        for c in spaced(it["tags"]):
            reserved.setdefault(c, it["id"])
    return reserved


def plan(posts, items, replies, now, horizon_h=72, eng=None, scheduled=()):
    """posts: dicts from post_from_build; items: queue items with ready_dt; replies: queue replies with tags and
    planned (datetime or None). Returns one row per tick."""
    table = engagement_table(eng)
    virtual = [dict(p) for p in posts]
    for sc in scheduled:  # regular posts fixed in time by a one-off Routine
        if sc["at_dt"] > now:
            virtual.append({"dt": sc["at_dt"], "tags": set(sc["tags"]), "exempt": False, "slug": sc["id"],
                            "author": "Claude Code", "kind": "scheduled"})
    for r in replies:
        if r.get("planned_dt") and r["planned_dt"] > now:
            virtual.append({"dt": r["planned_dt"], "tags": set(r["tags"]), "exempt": True, "slug": r["id"],
                            "author": "Claude Code", "kind": "reply"})
    pending = [i for i in items if i["state"] in ("ready", "writable")]
    rows = []
    t = next_tick(now)
    end = now + timedelta(hours=horizon_h)
    while t <= end:
        regular = [p for p in virtual if not p["exempt"] and p["dt"] <= t]
        gap_ok = not regular or t - max(p["dt"] for p in regular) >= MIN_GAP
        reserved = reservations(pending, t, virtual)
        best, best_score, best_relief = None, None, False
        if gap_ok:
            for it in pending:
                if it["ready_dt"] > t:
                    continue
                if it["lane"] == "guest" and not guest_turn_open(virtual, t):
                    continue
                ok, relief = is_open(it, virtual, t)
                if not ok:
                    continue
                if any(c in reserved and reserved[c] != it["id"] for c in spaced(it["tags"])):
                    continue
                sc = score(it, virtual, t, table)
                if best is None or (sc, -hours(it["ready_dt"] - now), it["id"]) > (best_score, -hours(best["ready_dt"] - now), best["id"]):
                    best, best_score, best_relief = it, sc, relief
        row = {"tick": t, "open": open_categories(virtual, t)}
        if best:
            row.update(item=best["id"], title=best["title"], lane=best["lane"], tags=sorted(best["tags"]),
                       score=round(best_score), relief=best_relief,
                       waited_h=round(hours(t - best["ready_dt"]), 1), state=best["state"])
            virtual.append({"dt": t, "tags": set(best["tags"]), "exempt": False, "slug": best["id"],
                            "author": best.get("author", ""), "kind": "plan"})
            pending = [i for i in pending if i["id"] != best["id"]]
        else:
            row["item"] = None
            row["why"] = "within the minimum gap" if not gap_ok else "no ready item has all its categories open"
        rows.append(row)
        t += timedelta(hours=GRID_HOURS)
    return rows


def load_queue(posts_slugs, answered):
    if not os.path.exists(QUEUE):
        raise SystemExit(f"{QUEUE} is missing")
    q = json.load(open(QUEUE, encoding="utf-8"))
    items, replies, scheduled = [], [], []
    for it in q.get("items", []):
        if it.get("published") or slug_tail(it.get("slug", it["id"])) in posts_slugs:
            continue
        it = dict(it)
        for c in it["tags"]:
            if c not in build.TAGS:
                raise SystemExit(f"{QUEUE}: item {it['id']} has unknown tag '{c}'")
        it["tags"] = list(it["tags"])
        it["ready_dt"] = ts(it["ready"]) if it.get("ready") else None
        if it["state"] in ("ready", "writable") and it["ready_dt"] is None:
            raise SystemExit(f"{QUEUE}: item {it['id']} is {it['state']} but has no `ready` time")
        items.append(it)
    for sc in q.get("scheduled", []):
        sc = dict(sc)
        sc["at_dt"] = ts(sc["at"])
        scheduled.append(sc)
    for r in q.get("replies", []):
        if (r.get("video_id") and r["video_id"] in answered) or slug_tail(r.get("slug", "")) in posts_slugs:
            continue
        r = dict(r)
        r["release_dt"] = ts(r["release"])
        r["planned_dt"] = ts(r["planned"]) if r.get("planned") else None
        replies.append(r)
    return q, items, replies, scheduled


def main(posts, argv):
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    now = datetime.now(timezone.utc)
    horizon = 72
    if "--now" in argv:
        now = ts(argv[argv.index("--now") + 1])
    if "--hours" in argv:
        horizon = int(argv[argv.index("--hours") + 1])
    answered = set(json.load(open(ANSWERED, encoding="utf-8"))) if os.path.exists(ANSWERED) else set()
    eng = json.load(open(ENGAGEMENT, encoding="utf-8")) if os.path.exists(ENGAGEMENT) else None
    published = [post_from_build(p) for p in posts]
    q, items, replies, scheduled = load_queue({slug_tail(p["slug"]) for p in published}, answered)
    rows = plan(published, items, replies, now, horizon, eng, scheduled)
    if "--json" in argv:
        out = [{**r, "tick": fmt(r["tick"])} for r in rows]
        print(json.dumps({"now": fmt(now), "plan": out}, indent=1))
        return
    print(f"publication plan from {fmt(now)}: ticks every {GRID_HOURS}h at :{GRID_MINUTE:02d} UTC, one regular post per tick, "
          f"at least {int(hours(MIN_GAP))}h apart; replies are exempt and never wait for a tick\n")
    print("queue (a ready item is published within 58h of its ready time, a guest item within 58h of its turn, whatever replies arrive):")
    if not items:
        print("  (empty)")
    for it in sorted(items, key=lambda i: (i["state"] == "waiting", i["ready_dt"] or now)):
        if it["state"] == "waiting":
            print(f"  {it['id']:34} {it['lane']:5} {it['priority']}  waiting: {it.get('waiting_for', '')}")
            continue
        waited = hours(now - it["ready_dt"])
        start = clock_start(it, published, now) if it["lane"] == "guest" else it["ready_dt"]
        bound = start + build.DRAIN_AFTER + build.SPACING + timedelta(hours=GRID_HOURS)
        waited = hours(now - start)
        due = "DUE (reserves its categories)" if waited >= hours(build.DRAIN_AFTER) else f"due in {hours(build.DRAIN_AFTER) - waited:.0f}h"
        turn = f", guest turn opens {fmt(start)}" if start > now else f", waited {waited:.0f}h"
        print(f"  {it['id']:34} {it['lane']:5} {it['priority']}  {it['state']:8} ready {fmt(it['ready_dt'])}{turn}, {due}, latest {fmt(bound)}")
    for sc in scheduled:
        if sc["at_dt"] > now:
            print(f"  {sc['id']:34} fixed at {fmt(sc['at_dt'])} ({', '.join(sc['tags'])}): counted as a regular post")
    if replies:
        print("\nreply ladder (publish inside 24h of release; a complete transcript or no reply):")
        for r in replies:
            lad = reply_ladder(r["release_dt"])
            flag = reply_flag(r["release_dt"], r["planned_dt"], r.get("source"), now)
            print(f"  {r.get('video_id') or r['id']}  release {fmt(r['release_dt'])}  ask by {fmt(lad['ask_by'])}  source due {fmt(lad['source_due'])}  "
                  f"publish by {fmt(lad['publish_by'])}  source: {r.get('source', '?')}  planned: {fmt(r['planned_dt']) if r['planned_dt'] else '-'}  {flag}")
    print("\nticks:")
    for r in rows:
        if r["item"]:
            note = " [drain relief]" if r["relief"] else ""
            print(f"  {fmt(r['tick'])}  {r['lane'].upper():5} {r['item']}  ({', '.join(r['tags'])}; score {r['score']}, waited {r['waited_h']}h){note}")
        else:
            print(f"  {fmt(r['tick'])}  -     {r['why']}; open: {', '.join(r['open']) or 'none'}")
    print("\nopen categories at each tick above are listed least recently used first; the next house post takes the "
          "highest-priority writable item whose categories are open, preferring the idle ones.")


if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    import glob
    ps = sorted((build.parse(f) for f in glob.glob("posts/*.md")), key=lambda p: p["dt"], reverse=True)
    main(ps, sys.argv[1:])
