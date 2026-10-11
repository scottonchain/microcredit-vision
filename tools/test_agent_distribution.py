import json
import unittest
from pathlib import Path

from check_agent_distribution import HUMAN_PREFIX, REGISTRY, check, load_posts

BOARD = "https://github.com/scottonchain/microcredit-vision/issues/24#issuecomment-"
MOLT = "https://www.moltbook.com/post/"


def post(date, tags="economics", extra=""):
    return f"<!--\ntitle: T\ndate: {date}\nauthor: Claude Code\ntags: {tags}\n{extra}-->\nbody\n"


def entry(slug, status, board=None, molt=None, exempt=False):
    return {
        "human_url": f"{HUMAN_PREFIX}{slug}.md",
        "media_reply_exempt": exempt,
        "github_board_url": board,
        "moltbook_url": molt,
        "status": status,
    }


def registry(**entries):
    return {"effective_at": "2026-10-11 17:23 UTC", "entries": entries}


class AgentDistributionTest(unittest.TestCase):
    def test_non_media_post_needs_both_receipts(self):
        posts = {"a": post("2026-10-12 09:00 UTC")}
        errors, pending = check(registry(a=entry("a", "complete", BOARD + "1", MOLT + "x")), posts)
        self.assertEqual((errors, pending), ([], []))
        errors, _ = check(registry(a=entry("a", "complete", BOARD + "1")), posts)
        self.assertIn("a: complete without both required receipts", errors)

    def test_new_post_without_an_entry_is_an_error(self):
        errors, _ = check(registry(), {"a": post("2026-10-12 09:00 UTC")})
        self.assertIn("a: missing agent-distribution entry", errors)

    def test_media_reply_is_exempt_but_an_essay_is_not(self):
        reply = post("2026-10-12 09:00 UTC", "podcasts, current-events", "video_id: abc\n")
        errors, pending = check(registry(r=entry("r", "exempt", exempt=True)), {"r": reply})
        self.assertEqual((errors, pending), ([], []))
        essay = post("2026-10-12 09:00 UTC")
        errors, _ = check(registry(e=entry("e", "exempt", exempt=True)), {"e": essay})
        self.assertIn("e: exempt but not a media reply", errors)

    def test_missing_receipt_is_pending_not_silent(self):
        posts = {"a": post("2026-10-12 09:00 UTC")}
        errors, pending = check(registry(a=entry("a", "waiting_moltbook", BOARD + "1")), posts)
        self.assertEqual(errors, [])
        self.assertEqual(pending, ["a: Moltbook receipt pending (waiting_moltbook)"])
        errors, pending = check(registry(a=entry("a", "watching", BOARD + "1")), posts)
        self.assertEqual(errors, [])
        self.assertEqual(len(pending), 1)

    def test_backfilled_entry_before_effective_time_still_counts(self):
        posts = {"old": post("2026-10-11 16:10 UTC")}
        _, pending = check(registry(old=entry("old", "waiting_moltbook", BOARD + "1")), posts)
        self.assertEqual(len(pending), 1)
        errors, pending = check(registry(), posts)
        self.assertEqual((errors, pending), ([], []))

    def test_duplicate_receipt_is_refused(self):
        posts = {"a": post("2026-10-12 09:00 UTC"), "b": post("2026-10-12 10:00 UTC")}
        reg = registry(
            a=entry("a", "complete", BOARD + "1", MOLT + "x"),
            b=entry("b", "complete", BOARD + "2", MOLT + "x"),
        )
        errors, _ = check(reg, posts)
        self.assertIn("b: moltbook_url duplicates the receipt of a", errors)

    def test_receipt_must_be_the_right_kind_of_link(self):
        posts = {"a": post("2026-10-12 09:00 UTC")}
        errors, _ = check(registry(a=entry("a", "complete", BOARD + "1", BOARD + "9")), posts)
        self.assertTrue(any("moltbook_url is not" in e for e in errors))

    def test_status_must_move_to_complete_when_both_receipts_land(self):
        posts = {"a": post("2026-10-12 09:00 UTC")}
        errors, _ = check(registry(a=entry("a", "watching", BOARD + "1", MOLT + "x")), posts)
        self.assertIn("a: both receipts present but status is 'watching', not 'complete'", errors)

    def test_board_announcement_is_tracked(self):
        reg = registry()
        reg["board_announcement"] = {"moltbook_url": None, "status": "waiting_moltbook"}
        errors, pending = check(reg, {})
        self.assertEqual(errors, [])
        self.assertEqual(pending, ["board_announcement: Moltbook receipt pending (waiting_moltbook)"])
        reg["board_announcement"] = {"moltbook_url": MOLT + "y", "status": "complete"}
        self.assertEqual(check(reg, {}), ([], []))

    def test_repository_registry_is_valid(self):
        errors, _ = check(json.loads(Path(REGISTRY).read_text(encoding="utf-8")), load_posts())
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
