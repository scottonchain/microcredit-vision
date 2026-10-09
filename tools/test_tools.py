"""Offline regressions for source attribution, watch boundaries and retry idempotence."""
import copy
import importlib
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

import fetch_source
import sync_discussion as sync
import world_model_receipt as receipts
import youtube_watch as youtube


def finding(**changes):
    value = {"finding": True, "watch": "news-watch", "check_time": "2026-10-09T10:00:00Z",
             "coverage": "The complete original article", "outcome": "The author calls for checkable outcomes.",
             "url": "https://example.org/article", "locator": "paragraph 3", "published_at": "2026-10-09T08:00:00Z",
             "author_id": "agent:author", "observer_id": "agent:claude"}
    return {**value, **changes}


def model():
    return {"model_version": "1.2.3", "updated_at": "2026-10-09T09:00:00Z",
            "entities": [{"id": "agent:author"}, {"id": "agent:claude"}], "evidence": []}


class ModelPreparation(unittest.TestCase):
    def test_importing_the_tool_never_runs_git(self):
        with patch.object(receipts.subprocess, "run") as run:
            importlib.reload(receipts)
        run.assert_not_called()

    def test_source_author_and_observer_are_distinct_and_input_is_unchanged(self):
        original = model()
        before = copy.deepcopy(original)
        result, added = receipts.prepare_model(original, [finding()])
        self.assertEqual(original, before)
        self.assertEqual(len(added), 1)
        self.assertEqual(result["evidence"][0]["author_id"], "agent:author")
        self.assertEqual(result["evidence"][0]["observer_id"], "agent:claude")

    def test_reading_again_does_not_create_another_witness_or_version(self):
        first, _ = receipts.prepare_model(model(), [finding()])
        again, added = receipts.prepare_model(first, [finding(check_time="2026-10-09T12:00:00Z")])
        self.assertEqual(added, [])
        self.assertEqual(first, again)

    def test_two_findings_from_one_source_share_the_original_origin(self):
        result, _ = receipts.prepare_model(model(), [finding(), finding(outcome="Another relevant finding.")])
        self.assertEqual(result["evidence"][0]["origin_group"], result["evidence"][1]["origin_group"])

    def test_mirrors_inherit_original_provenance(self):
        original, added = receipts.prepare_model(model(), [finding()])
        result, _ = receipts.prepare_model(original, [finding(url="https://example.org/mirror", derived_from_ids=added)])
        self.assertEqual(result["evidence"][-1]["kind"], "mirror")
        self.assertEqual(result["evidence"][-1]["origin_group"], result["evidence"][0]["origin_group"])

    def test_empty_iterations_and_missing_authors_are_rejected(self):
        for change in ({"finding": False}, {"finding": "yes"}, {"author_id": ""}, {"author_id": "agent:missing"}):
            with self.assertRaises(ValueError):
                receipts.prepare_model(model(), [finding(**change)])

    def test_legacy_git_options_fail_before_loading_or_writing_files(self):
        with patch.object(receipts.Path, "read_text") as read:
            with self.assertRaises(SystemExit):
                receipts.main(["missing.json", "--no-push"])
        read.assert_not_called()


class DiscussionRetry(unittest.TestCase):
    def discussion(self, comments, body="old"):
        return {"body": body, "comments": {"nodes": comments}}

    def comment(self, text, who="github-actions[bot]"):
        return {"body": text, "author": {"login": who}}

    def test_a_retried_revision_comment_is_recognized_without_posting_again(self):
        want = sync.MARK + "\nNew charter. Reply below to join."
        discussion = self.discussion([self.comment(sync.revision_body(want))])
        self.assertTrue(sync.is_current(discussion, want))

    def test_an_outside_marker_cannot_impersonate_the_workflows_revision(self):
        want = sync.MARK + "\nNew charter. Reply below to join."
        for login in ("outside-reader", "github-actions-impostor"):
            discussion = self.discussion([self.comment(want, login)])
            self.assertFalse(sync.is_current(discussion, want))

    def test_a_graphql_error_is_not_success_even_with_zero_process_exit(self):
        result = type("Result", (), {"returncode": 0, "stdout": '{"errors":[{"message":"refused"}]}', "stderr": ""})()
        with patch.object(sync.subprocess, "run", return_value=result):
            self.assertFalse(sync.run("test", ["gh"])[0])


class Watch(unittest.TestCase):
    def player(self, length, tracks):
        return {"videoDetails": {"videoId": "abcdefghijk", "lengthSeconds": str(length)},
                "captions": {"playerCaptionsTracklistRenderer": {"captionTracks": tracks}}}

    def test_future_and_exactly_24_hour_old_releases_are_outside_the_window(self):
        now = datetime(2026, 10, 9, 12, tzinfo=timezone.utc)
        entries = [("abcdefghijk", "future", now + timedelta(hours=1), "", False),
                   ("abcdefghijl", "expired", now - timedelta(hours=24), "", False),
                   ("abcdefghijm", "current", now - timedelta(hours=1), "", False)]
        with patch.object(youtube, "load", side_effect=[[{"name": "channel"}], {}]), \
             patch.object(youtube, "_feed_entries", return_value=(entries, None)), \
             patch.object(youtube, "datetime") as clock:
            clock.now.return_value = now
            result = {r["title"]: r for r in youtube.scan()}
        self.assertFalse(result["future"]["in_window"])
        self.assertIsNone(result["future"]["ladder"])
        self.assertFalse(result["expired"]["in_window"])
        self.assertTrue(result["current"]["in_window"])

    def test_empty_and_unknown_length_transcripts_are_never_complete(self):
        tracks = [{"languageCode": "en", "baseUrl": "caption"}]
        for length, events in ((60, []), (0, [(0, 1000, "Hello")])):
            with patch.object(youtube, "player_responses", return_value=[(self.player(length, tracks), "ua")]), \
                 patch.object(youtube, "_caption_events", return_value=events):
                result = youtube.details("abcdefghijk")
            self.assertFalse(result["transcript_complete"])

    def test_a_late_fragment_or_large_internal_gap_is_not_a_complete_transcript(self):
        tracks = [{"languageCode": "en", "baseUrl": "caption"}]
        for events in ([(290000, 10000, "The end")], [(0, 1000, "Start"), (299000, 1000, "End")]):
            with patch.object(youtube, "player_responses", return_value=[(self.player(300, tracks), "ua")]), \
                 patch.object(youtube, "_caption_events", return_value=events):
                result = youtube.details("abcdefghijk")
            self.assertFalse(result["transcript_complete"])

    def test_incomplete_first_caption_track_does_not_hide_a_complete_track(self):
        tracks = [{"languageCode": "en", "baseUrl": "partial"}, {"languageCode": "en", "baseUrl": "complete"}]
        with patch.object(youtube, "player_responses", return_value=[(self.player(60, tracks), "ua")]), \
             patch.object(youtube, "_caption_events", side_effect=[[(0, 1000, "Partial")], [(0, 60000, "Complete")]]):
            result = youtube.details("abcdefghijk")
        self.assertTrue(result["transcript_complete"])
        self.assertIn("Complete", result["transcript"])

    def test_repeated_answer_does_not_reset_the_channel_cooldown(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "answered.json"
            old = {"abcdefghijk": {"post": "original", "answered": "2026-10-08 10:00 UTC"}}
            path.write_text(json.dumps(old))
            before = path.read_bytes()
            with patch.object(youtube, "ANSWERED", path):
                youtube.mark_answered("abcdefghijk", "original")
                self.assertEqual(path.read_bytes(), before)
                with self.assertRaises(SystemExit):
                    youtube.mark_answered("abcdefghijk", "different")

    def test_thumbnail_does_not_require_a_browser_or_node(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.jpg"
            Image.new("RGB", (600, 400), "black").save(source)
            with patch.object(youtube, "ROOT", root), patch.object(youtube, "fetch") as fetch:
                target = youtube.thumbnail("abcdefghijk", source)
            fetch.assert_not_called()
            with Image.open(target) as output:
                self.assertEqual(output.size, (480, 360))
                self.assertEqual(output.getpixel((240, 180)), (255, 255, 255))

    def test_source_fetch_and_thumbnail_reject_local_paths_before_reading(self):
        with patch.object(fetch_source.urllib.request, "urlopen") as request:
            with self.assertRaises(ValueError):
                fetch_source.get("file:///tmp/not-a-public-source")
        request.assert_not_called()
        with self.assertRaises(ValueError):
            youtube.thumbnail("../bad-path")


if __name__ == "__main__":
    unittest.main()
