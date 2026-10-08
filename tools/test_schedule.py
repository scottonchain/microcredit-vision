#!/usr/bin/env python3
"""Tests for tools/schedule.py and the spacing / drain rules in tools/build.py. Run: python3 tools/test_schedule.py"""
import os
import random
import sys
import unittest
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build  # noqa: E402
import schedule as S  # noqa: E402

UTC = timezone.utc


def t(day, hour, minute=7):
    return datetime(2026, 10, day, hour, minute, tzinfo=UTC)


def post(dt, tags, exempt=False, slug="p"):
    return {"dt": dt, "tags": set(tags), "exempt": exempt, "slug": slug, "author": "x", "kind": "published"}


def item(id, tags, ready, lane="house", priority="P1", state="writable"):
    return {"id": id, "title": id, "lane": lane, "priority": priority, "tags": list(tags), "state": state,
            "ready_dt": ready, "author": "x"}


def bpost(slug, dt, tags, queued=None):
    """A post as build.parse returns it."""
    return {"slug": slug, "path": slug, "date": dt.strftime(S.FMT), "dt": dt, "tag_list": list(tags),
            "author": "Claude Code", "queued_dt": queued}


class Grid(unittest.TestCase):
    def test_next_tick_is_strictly_after_and_on_the_grid(self):
        self.assertEqual(S.next_tick(t(8, 16, 7)), t(8, 20))
        self.assertEqual(S.next_tick(t(8, 16, 6)), t(8, 16))
        self.assertEqual(S.next_tick(t(8, 23, 59)), t(9, 0))
        self.assertEqual(S.next_tick(t(8, 17, 30)), t(8, 20))


class Spacing(unittest.TestCase):
    def test_a_category_in_cooldown_is_not_planned(self):
        posts = [post(t(8, 0), ["economics"])]
        rows = S.plan(posts, [item("a", ["economics"], t(7, 0))], [], t(8, 1), 30)
        first = [r for r in rows if r["item"]][0]
        self.assertEqual(first["tick"], t(8, 20))  # 00:07 + 18h = 18:07, next tick 20:07

    def test_rotation_prefers_the_idle_category(self):
        posts = [post(t(6, 0), ["sybil"]), post(t(8, 8), ["economics"])]
        rows = S.plan(posts, [item("busy", ["economics"], t(7, 0)), item("idle", ["sybil"], t(7, 0))], [], t(9, 8), 4)
        self.assertEqual(rows[0]["item"], "idle")

    def test_min_gap_between_regular_posts(self):
        posts = [post(t(8, 18, 10), ["team"])]
        rows = S.plan(posts, [item("a", ["sybil"], t(7, 0))], [], t(8, 18, 30), 8)
        self.assertIsNone(rows[0]["item"])  # 20:07 is 1h57 after 18:10
        self.assertEqual(rows[1]["item"], "a")  # 00:07

    def test_a_scheduled_post_counts_before_it_goes_out(self):
        sched = [{"id": "s", "at_dt": t(8, 18, 10), "tags": ["team"]}]
        rows = S.plan([], [item("a", ["team"], t(7, 0))], [], t(8, 17), 40, None, sched)
        self.assertEqual([r for r in rows if r["item"]][0]["tick"], t(9, 16))  # 18:10 + 18h = 12:10, tick 16:07

    def test_a_planned_reply_resets_its_categories(self):
        reply = {"id": "r", "planned_dt": t(8, 20), "tags": ["current-events", "ai-alignment"]}
        rows = S.plan([], [item("a", ["ai-alignment"], t(8, 10))], [reply], t(8, 17), 40)
        self.assertEqual([r for r in rows if r["item"]][0]["tick"], t(9, 16))  # 20:00 + 18h = 14:00, tick 16:07


class GuestSlot(unittest.TestCase):
    def test_a_ready_guest_item_beats_a_higher_priority_house_item_once_a_day(self):
        posts = [post(t(7, 0), ["guest-post"])]
        items = [item("house", ["sybil"], t(7, 0), priority="P1"),
                 item("guest", ["microcredit"], t(7, 0), lane="guest", priority="P3", state="ready")]
        rows = S.plan(posts, items, [], t(8, 8), 4)
        self.assertEqual(rows[0]["item"], "guest")

    def test_no_floor_inside_24_hours_of_the_last_guest_post(self):
        posts = [post(t(8, 0), ["guest-post"])]
        items = [item("house", ["sybil"], t(7, 0), priority="P1"),
                 item("guest", ["microcredit"], t(7, 0), lane="guest", priority="P3", state="ready")]
        rows = S.plan(posts, items, [], t(8, 18), 4)  # next tick 20:07, 20 hours after the last guest post
        self.assertEqual(rows[0]["item"], "house")


class Drain(unittest.TestCase):
    def test_exempt_replies_stop_holding_up_an_item_after_36_hours(self):
        posts = [post(t(6, 22), ["current-events", "ai-alignment"], exempt=True)]
        it = item("g", ["ai-alignment"], t(6, 0), lane="guest", state="ready")
        ok, relief = S.is_open(it, posts, t(6, 23))  # 23 hours after ready: the reply holds it
        self.assertFalse(ok)
        self.assertFalse(relief)
        ok, relief = S.is_open(it, posts, t(7, 13))  # 37 hours after ready, 15 hours after the reply: relief
        self.assertTrue(ok)
        self.assertTrue(relief)

    def test_regular_posts_still_hold_a_drained_item(self):
        posts = [post(t(6, 22), ["ai-alignment"], exempt=False)]
        it = item("g", ["ai-alignment"], t(5, 0), lane="guest", state="ready")
        self.assertFalse(S.is_open(it, posts, t(6, 23))[0])

    def test_a_due_item_reserves_its_categories(self):
        now = t(8, 0)
        due = item("g", ["economics", "microcredit"], now - timedelta(hours=40), lane="guest", state="ready")
        fresh = item("h", ["economics"], now - timedelta(hours=1), priority="P1")
        # the guest is blocked by a regular post 5 hours ago; the house item would take economics when it opens
        posts = [post(now - timedelta(hours=5), ["economics"])]
        rows = S.plan(posts, [due, fresh], [], now, 36)
        placed = {r["item"]: r["tick"] for r in rows if r["item"]}
        self.assertLess(placed["g"], placed["h"])

    def test_build_accepts_a_drained_post_behind_an_exempt_reply(self):
        reply = bpost("reply", t(8, 12), ["current-events", "ai-alignment"])
        late = bpost("late", t(8, 16), ["ai-alignment"], queued=t(6, 0))
        build.check_spacing([late, reply])  # waited 58h: the reply no longer holds it up

    def test_build_refuses_without_the_queue_time(self):
        reply = bpost("reply", t(8, 12), ["current-events", "ai-alignment"])
        late = bpost("late", t(8, 16), ["ai-alignment"])
        with self.assertRaises(SystemExit):
            build.check_spacing([late, reply])

    def test_build_refuses_a_drained_post_behind_a_regular_post(self):
        before = bpost("before", t(8, 12), ["ai-alignment"])
        late = bpost("late", t(8, 16), ["ai-alignment"], queued=t(6, 0))
        with self.assertRaises(SystemExit):
            build.check_spacing([late, before])

    def test_build_refuses_when_the_wait_was_under_36_hours(self):
        reply = bpost("reply", t(8, 12), ["current-events", "ai-alignment"])
        late = bpost("late", t(8, 16), ["ai-alignment"], queued=t(7, 8))
        with self.assertRaises(SystemExit):
            build.check_spacing([late, reply])


class Bound(unittest.TestCase):
    """A ready guest item publishes within DRAIN_AFTER + SPACING + one tick (58 hours) of becoming ready, whatever
    house items and replies arrive. Three adversaries: replies that reset exactly its categories every 6 hours (needs
    the drain relief), house posts that rotate through its categories so that they are never all free (needs the
    reservation), and both at once; plus a random stream."""

    BOUND = build.DRAIN_AFTER + build.SPACING + timedelta(hours=S.GRID_HOURS)
    READY = t(8, 0)
    CATS = ["microcredit", "economics", "ai-alignment"]

    def guest(self):
        return item("guest", self.CATS + ["guest-post"], self.READY, lane="guest", state="ready")

    def flood(self):
        """Exempt replies carrying exactly the guest's categories, one every 6 hours, starting before it was ready."""
        past = [post(self.READY - timedelta(hours=3 + 6 * i), ["current-events"] + self.CATS, exempt=True) for i in range(3)]
        future = [{"id": f"r{i}", "planned_dt": self.READY + timedelta(hours=6 * i - 3), "tags": ["current-events"] + self.CATS}
                  for i in range(1, 40)]
        return past, future

    def rotation(self):
        """Regular posts that keep the guest's categories from ever being free together: three staggered before it was
        ready, then an endless supply of ready P1 items, one category each in turn."""
        past = [post(self.READY - timedelta(hours=1 + 4 * k), [self.CATS[k]]) for k in range(3)]
        houses = [item(f"h{i}", [self.CATS[i % 3]], self.READY - timedelta(hours=2), priority="P1") for i in range(80)]
        return past, houses

    def waited(self, items, replies, posts=(), hours=150):
        rows = S.plan(list(posts), items, replies, self.READY, hours)
        when = [r["tick"] for r in rows if r["item"] == "guest"]
        self.assertTrue(when, "the guest item was never planned")
        return when[0] - self.READY

    def test_reply_flood(self):
        past, future = self.flood()
        self.assertLessEqual(self.waited([self.guest()], future, past), self.BOUND)

    def test_house_rotation(self):
        past, houses = self.rotation()
        self.assertLessEqual(self.waited([self.guest()] + houses, [], past), self.BOUND)

    def test_both_at_once(self):
        fpast, future = self.flood()
        rpast, houses = self.rotation()
        self.assertLessEqual(self.waited([self.guest()] + houses, future, fpast + rpast), self.BOUND)

    def test_random_streams(self):
        cats = ["microcredit", "economics", "ai-alignment", "team", "sybil", "how-it-works", "prototype"]
        for seed in range(40):
            rng = random.Random(seed)
            houses = [item(f"h{i}", rng.sample(cats, rng.randint(1, 3)), self.READY - timedelta(hours=1) + timedelta(hours=i), priority="P1")
                      for i in range(60)]
            replies = [{"id": f"r{i}", "planned_dt": self.READY + timedelta(hours=6 * i),
                        "tags": ["current-events"] + rng.sample(cats, 2)} for i in range(1, 30)]
            self.assertLessEqual(self.waited([self.guest()] + houses, replies, hours=120), self.BOUND, f"seed {seed}")


class Ladder(unittest.TestCase):
    def test_ladder_times(self):
        rel = t(7, 22, 42)
        lad = S.reply_ladder(rel)
        self.assertEqual(lad["ask_by"], rel + timedelta(hours=6))
        self.assertEqual(lad["source_due"], rel + timedelta(hours=14))
        self.assertEqual(lad["publish_by"], rel + timedelta(hours=22))
        self.assertEqual(lad["window"], rel + timedelta(hours=24))


class ReplyFlags(unittest.TestCase):
    REL = t(7, 18, 53)

    def test_planned_inside_the_ladder_is_fine(self):
        self.assertEqual(S.reply_flag(self.REL, t(8, 14), "in_hand", t(8, 10)), "")

    def test_planned_after_publish_by_is_allowed_before_the_last_half_hour(self):
        flag = S.reply_flag(self.REL, t(8, 18, 15), "in_hand", t(8, 17))  # +23h22m
        self.assertIn("after publish-by", flag)

    def test_planned_in_the_last_half_hour_is_too_late(self):
        self.assertIn("TOO LATE", S.reply_flag(self.REL, t(8, 18, 40), "in_hand", t(8, 17)))

    def test_unplanned_and_past_publish_by(self):
        self.assertIn("PAST PUBLISH-BY", S.reply_flag(self.REL, None, "in_hand", t(8, 17)))
        self.assertEqual(S.reply_flag(self.REL, None, "in_hand", t(8, 10)), "")
        self.assertEqual(S.reply_flag(self.REL, None, "in_hand", t(8, 19)), "WINDOW CLOSED")


class Engagement(unittest.TestCase):
    def test_engagement_breaks_a_tie_toward_the_category_that_drew_more(self):
        eng = {"categories": {"sybil": {"posts": 3, "events": 9}, "economics": {"posts": 3, "events": 0}}}
        posts = [post(t(1, 0), ["sybil"]), post(t(1, 0), ["economics"])]
        rows = S.plan(posts, [item("a", ["economics"], t(7, 0)), item("b", ["sybil"], t(7, 0))], [], t(8, 8), 4, eng)
        self.assertEqual(rows[0]["item"], "b")


if __name__ == "__main__":
    unittest.main()
