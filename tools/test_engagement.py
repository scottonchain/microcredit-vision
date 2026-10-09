#!/usr/bin/env python3
"""Tests for tools/engagement.py: attribution, team exclusion, no double counting. Run: python3 tools/test_engagement.py"""
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engagement as E  # noqa: E402


def issue(n, login, title="", body="", kind="User"):
    return {"number": n, "user": {"login": login, "type": kind}, "title": title, "body": body}


def comment(i, login, body="", kind="User"):
    return {"id": i, "user": {"login": login, "type": kind}, "body": body}


class Refs(unittest.TestCase):
    def test_refs_from_tags_and_links(self):
        text = "Re blog:2026-10-08-if-your-agent-can-send-email and https://github.com/scottonchain/microcredit-vision/blob/main/posts/2026-10-06-five-doors.md"
        self.assertEqual(E.refs_in(text), ["2026-10-06-five-doors", "2026-10-08-if-your-agent-can-send-email"])

    def test_no_refs(self):
        self.assertEqual(E.refs_in("nothing here"), [])

    def test_agent_declared(self):
        self.assertTrue(E.is_agent_declared("AI disclosure: I am hermes"))
        self.assertFalse(E.is_agent_declared("great post, thanks"))


class Github(unittest.TestCase):
    def test_out_of_order_records_all_count_and_replay_is_idempotent(self):
        led = E.Ledger()
        records = [comment(n, "stranger", "blog:2026-10-08-x-post-slug") for n in (30, 10, 20, 10)]
        self.assertEqual(E.ingest_github(led, "microcredit-contract", [], records), 3)
        self.assertEqual(E.ingest_github(led, "microcredit-contract", [], records), 0)

    def test_team_logins_are_case_insensitive(self):
        led = E.Ledger()
        self.assertEqual(E.ingest_github(led, "microcredit-vision", [issue(1, "SCOTTONCHAIN")], []), 0)

    def test_pagination_can_read_beyond_the_old_five_page_limit(self):
        pages = [[{"id": page * 100 + i} for i in range(100)] for page in range(6)] + [[]]
        with patch.object(E, "get_json", side_effect=pages) as get:
            self.assertEqual(len(E.github_pages("https://example.org/issues?state=all")), 600)
        self.assertEqual(get.call_count, 7)

    def test_repeated_api_page_is_an_error_instead_of_an_endless_fetch(self):
        page = [{"id": i} for i in range(100)]
        with patch.object(E, "get_json", return_value=page):
            with self.assertRaisesRegex(ValueError, "repeated a page"):
                E.github_pages("https://example.org/issues?state=all")

    def test_outside_comment_with_a_tag_counts_for_the_post(self):
        led = E.Ledger()
        n = E.ingest_github(led, "microcredit-contract", [], [comment(10, "stranger", "about blog:2026-10-08-x-post-slug: AI disclosure")])
        self.assertEqual(n, 1)
        self.assertEqual(led.posts["2026-10-08-x-post-slug"]["events"], 1)
        self.assertEqual(led.posts["2026-10-08-x-post-slug"]["agent_declared"], 1)

    def test_team_and_bots_never_count(self):
        led = E.Ledger()
        E.ingest_github(led, "microcredit-vision", [issue(1, "scottonchain", "blog:2026-10-08-x-post-slug")],
                        [comment(5, "hermes-agent-909", "blog:2026-10-08-x-post-slug"), comment(6, "dependabot", "blog:2026-10-08-x-post-slug", "Bot")])
        self.assertEqual(led.posts, {})
        self.assertEqual(led.channels["unattributed_blog_repo"], 0)

    def test_watermarks_prevent_double_counting(self):
        led = E.Ledger()
        cs = [comment(10, "stranger", "blog:2026-10-08-x-post-slug")]
        E.ingest_github(led, "microcredit-contract", [], cs)
        E.ingest_github(led, "microcredit-contract", [], cs)
        self.assertEqual(led.posts["2026-10-08-x-post-slug"]["events"], 1)

    def test_an_untagged_outside_comment_on_the_blog_repo_counts_at_blog_level(self):
        led = E.Ledger()
        E.ingest_github(led, "microcredit-vision", [], [comment(3, "stranger", "interesting")])
        self.assertEqual(led.channels["unattributed_blog_repo"], 1)
        self.assertEqual(led.posts, {})

    def test_an_untagged_comment_elsewhere_is_ignored(self):
        led = E.Ledger()
        E.ingest_github(led, "microcredit-contract", [], [comment(3, "stranger", "interesting")])
        self.assertEqual(led.channels["unattributed_blog_repo"], 0)


class Mail(unittest.TestCase):
    def msg(self, ts, sender, subject, labels=("received",), preview=""):
        return {"timestamp": ts, "from": sender, "subject": subject, "labels": list(labels), "preview": preview}

    def test_outside_mail_with_a_tag_counts_and_team_mail_does_not(self):
        led = E.Ledger()
        n = E.ingest_mail(led, [
            self.msg("2026-10-09T01:00:00Z", "Someone <someone@example.org>", "blog:2026-10-08-x-post-slug"),
            self.msg("2026-10-09T02:00:00Z", "Hermes <hermes-909@agentmail.to>", "blog:2026-10-08-x-post-slug"),
            self.msg("2026-10-09T03:00:00Z", "Me <me@example.org>", "unrelated"),
            self.msg("2026-10-09T04:00:00Z", "Out <out@example.org>", "blog:2026-10-08-x-post-slug", labels=("sent",)),
        ])
        self.assertEqual(n, 1)
        self.assertEqual(led.posts["2026-10-08-x-post-slug"]["mail"], 1)

    def test_mail_watermark(self):
        led = E.Ledger()
        m = [self.msg("2026-10-09T01:00:00Z", "A <a@example.org>", "blog:2026-10-08-x-post-slug")]
        E.ingest_mail(led, m)
        E.ingest_mail(led, m)
        self.assertEqual(led.posts["2026-10-08-x-post-slug"]["events"], 1)

    def test_distinct_messages_at_the_watermark_time_are_counted_once(self):
        led = E.Ledger()
        a = {**self.msg("2026-10-09T01:00:00Z", "A <a@example.org>", "blog:2026-10-08-x-post-slug"), "message_id": "one"}
        b = {**a, "message_id": "two"}
        self.assertEqual(E.ingest_mail(led, [a]), 1)
        self.assertEqual(E.ingest_mail(led, [a, b]), 1)
        self.assertEqual(E.ingest_mail(led, [b, a]), 0)
        self.assertEqual(led.posts["2026-10-08-x-post-slug"]["mail"], 2)

    def test_old_timestamp_only_watermark_is_migrated_without_recounting(self):
        led = E.Ledger({"watermarks": {"mail": {"timestamp": "2026-10-09T01:00:00Z"}}})
        record = self.msg("2026-10-09T01:00:00Z", "A <a@example.org>", "blog:2026-10-08-x-post-slug")
        self.assertEqual(E.ingest_mail(led, [record]), 0)
        self.assertEqual(E.ingest_mail(led, [record]), 0)

    def test_mail_sender_matching_uses_the_complete_address(self):
        led = E.Ledger()
        outside = self.msg("2026-10-09T01:00:00Z", "Name <hermes-909@agentmail.to.example.org>", "blog:2026-10-08-x-post-slug")
        self.assertEqual(E.ingest_mail(led, [outside]), 1)

    def test_truncated_mail_does_not_advance_the_watermark(self):
        led = E.Ledger()
        with patch.object(E, "get_json", return_value={"messages": [], "next_page_token": "next"}):
            E.read_mail(led)
        self.assertNotIn("mail", led.watermarks)
        self.assertIn("unavailable", led.sources["mail"])

    def test_ref_counts_at_channel_level(self):
        led = E.Ledger()
        E.ingest_mail(led, [self.msg("2026-10-09T01:00:00Z", "A <a@example.org>", "hello", preview="ref:moltbook please")])
        self.assertEqual(led.channels["moltbook_ref"], 1)


class Moltbook(unittest.TestCase):
    def test_comments_by_others_count_once(self):
        led = E.Ledger()
        cs = [{"id": "a", "author": {"name": "someagent"}, "content": "AI agent here"},
              {"id": "b", "author": {"name": "hermes-agent-909"}, "content": "thanks"}]
        self.assertEqual(E.ingest_moltbook(led, "p1", "2026-10-08-slug-x", cs), 1)
        self.assertEqual(E.ingest_moltbook(led, "p1", "2026-10-08-slug-x", cs), 0)
        self.assertEqual(led.posts["2026-10-08-slug-x"]["moltbook"], 1)


if __name__ == "__main__":
    unittest.main()
