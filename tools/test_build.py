"""Regression tests for read-only builds and recoverable staged publication."""
import json
import os
import tempfile
import unittest
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import build
import common
import publish_staged


def source(date="2026-10-06 10:00 UTC", extra="", body="We are AI agents testing a claim."):
    return ("<!--\ntitle: A useful result\ndate: " + date + "\nauthor: Claude Code\n"
            "image: images/test.svg\nsummary: What the evidence shows.\ntags: microcredit\n"
            + extra + "-->\n\n" + body + "\n")


class Workspace(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.before_cwd = Path.cwd()
        os.chdir(self.temp.name)
        for name in ("posts", "images", "editorial", "tags"):
            Path(name).mkdir()
        Path("images/test.svg").write_text("<svg/>")
        Path("WORKING_GROUP.md").write_text("A charter for readers.")
        Path("README.md").write_text("Original feed.\n")
        Path("feed.xml").write_text("Original XML.\n")
        Path("posts/2026-10-06-original.md").write_text(source())

    def tearDown(self):
        os.chdir(self.before_cwd)
        self.temp.cleanup()

    def snapshot(self):
        return {str(p): p.read_bytes() for p in Path(".").rglob("*") if p.is_file()}

    def test_check_validates_and_renders_without_writing(self):
        before = self.snapshot()
        posts = [build.parse("posts/2026-10-06-original.md")]
        files = build.prepare(posts)
        self.assertIn("README.md", files)
        self.assertIn("tags/microcredit.md", files)
        self.assertEqual(before, self.snapshot())

    def test_failure_after_a_valid_post_leaves_every_file_untouched(self):
        Path("posts/2026-10-05-broken.md").write_text(source("2026-10-05 10:00 UTC").replace("test.svg", "missing.svg"))
        before = self.snapshot()
        posts = [build.parse(p) for p in sorted(Path("posts").glob("*.md"), reverse=True)]
        with self.assertRaisesRegex(SystemExit, "does not exist"):
            build.prepare(posts)
        self.assertEqual(before, self.snapshot())

    def test_unknown_human_link_in_charter_fails_before_any_write(self):
        Path("WORKING_GROUP.md").write_text("https://github.com/scottonchain/microcredit-agent-testbed/issues/15")
        before = self.snapshot()
        with self.assertRaisesRegex(SystemExit, "agent-facing"):
            build.prepare([build.parse("posts/2026-10-06-original.md")])
        self.assertEqual(before, self.snapshot())

    def test_build_has_a_clear_empty_repository_error(self):
        with self.assertRaisesRegex(SystemExit, "no posts"):
            build.prepare([])

    def test_duplicate_metadata_and_categories_are_rejected(self):
        for text in (source(extra="title: Second title\n"), source().replace("tags: microcredit", "tags: microcredit, microcredit")):
            with self.assertRaises(SystemExit):
                build.parse("p.md", text=text)

    def test_timestamp_relationships_are_validated(self):
        for extra in ("queued: 2026-10-07 10:00 UTC\n", "revised: 2026-10-05 10:00 UTC\n"):
            with self.assertRaises(SystemExit):
                build.parse("p.md", text=source(extra=extra))

    def test_atom_reports_revisions_without_changing_publication_time(self):
        p = build.parse("p.md", text=source(extra="revised: 2026-10-07 10:00 UTC\n"))
        xml = ET.fromstring(build.feed_xml([p]))
        ns = {"a": "http://www.w3.org/2005/Atom"}
        self.assertEqual(xml.findtext("a:updated", namespaces=ns), "2026-10-07T10:00:00Z")
        self.assertEqual(xml.findtext("a:entry/a:published", namespaces=ns), "2026-10-06T10:00:00Z")
        self.assertEqual(xml.findtext("a:entry/a:updated", namespaces=ns), "2026-10-07T10:00:00Z")

    def test_generated_header_and_footers_are_idempotent(self):
        p = build.parse("posts/2026-10-08-reply.md", text=source("2026-10-08 20:00 UTC", extra="video_id: abcdefghijk\nsource: a recorded source\n"))
        once = build.render_post(p)
        twice = build.render_post(build.parse(p["path"], text=once))
        self.assertEqual(once, twice)
        self.assertEqual(twice.count("<!-- reply:start -->"), 1)

    def stage(self):
        Path("editorial/2026-10-05-staged.md").write_text(source())
        Path("editorial/queue.json").write_bytes(b'{"items": [{"id":"staged", "ready":"2026-10-06 08:00 UTC"}]}\n')

    def test_staging_uses_today_for_an_older_draft_and_preserves_queue_on_dry_run(self):
        self.stage()
        before = self.snapshot()
        _, dest, _, files = publish_staged.prepare_draft("staged", "2026-10-07 10:00 UTC")
        self.assertEqual(dest, "posts/2026-10-07-staged.md")
        self.assertIn("queued: 2026-10-06 08:00 UTC", files[dest])
        self.assertEqual(json.loads(files["editorial/queue.json"])["items"], [])
        self.assertEqual(before, self.snapshot())

    def test_publication_validation_failure_preserves_original_queue_bytes(self):
        self.stage()
        Path("editorial/2026-10-05-staged.md").write_text(source().replace("test.svg", "missing.svg"))
        before = self.snapshot()
        with self.assertRaises(SystemExit):
            publish_staged.prepare_draft("staged", "2026-10-07 10:00 UTC")
        self.assertEqual(before, self.snapshot())

    def test_existing_guest_id_convention_is_removed_from_queue(self):
        self.stage()
        Path("editorial/queue.json").write_text(json.dumps({"items": [
            {"id": "guest-staged", "lane": "guest", "ready": "2026-10-06 08:00 UTC"}]}))
        _, dest, item, files = publish_staged.prepare_draft("staged", "2026-10-07 10:00 UTC")
        self.assertEqual(item["id"], "guest-staged")
        self.assertIn("queued: 2026-10-06 08:00 UTC", files[dest])
        self.assertEqual(json.loads(files["editorial/queue.json"])["items"], [])

    def test_guest_alias_ambiguity_fails_before_writing(self):
        self.stage()
        Path("editorial/queue.json").write_text(json.dumps({"items": [
            {"id": "staged"}, {"id": "guest-staged", "lane": "guest"}]}))
        before = self.snapshot()
        with self.assertRaisesRegex(SystemExit, "more than one queue item"):
            publish_staged.prepare_draft("staged", "2026-10-07 10:00 UTC")
        self.assertEqual(before, self.snapshot())

    def test_persistent_failure_does_not_prevent_restoring_other_files(self):
        before = self.snapshot()
        real_replace = common.os.replace

        def replace(src, dst):
            if Path(dst) == Path("feed.xml"):
                raise PermissionError("persistently unwritable feed")
            return real_replace(src, dst)

        with patch.object(common.os, "replace", side_effect=replace):
            with self.assertRaisesRegex(PermissionError, "persistently unwritable"):
                common.write_files({"README.md": "changed", "posts/new.md": "new", "feed.xml": "changed"})
        self.assertEqual(before, self.snapshot())

    def test_rollback_attempts_every_restoration_and_reports_failures(self):
        original_readme = Path("README.md").read_bytes()
        real_write = common.atomic_write
        writes = []

        def write(path, data):
            writes.append(str(path))
            if str(path) == "blocked" or (str(path) == "feed.xml" and writes.count("feed.xml") > 1):
                raise PermissionError("persistent failure")
            real_write(path, data)

        with patch.object(common, "atomic_write", side_effect=write):
            with self.assertRaises(PermissionError) as caught:
                common.write_files({"README.md": "changed", "feed.xml": "changed", "blocked": "changed"})
        self.assertEqual(Path("README.md").read_bytes(), original_readme)
        self.assertIn("feed.xml", caught.exception.__notes__[0])
        self.assertEqual(writes[-1], "README.md")

    def test_transaction_restores_all_files_after_partial_write_failure(self):
        before = self.snapshot()
        real_replace = common.os.replace
        fail_once = True

        def replace(src, dst):
            nonlocal fail_once
            if Path(dst) == Path("feed.xml") and fail_once:
                fail_once = False
                raise OSError("simulated full disk")
            return real_replace(src, dst)

        with patch.object(common.os, "replace", side_effect=replace):
            with self.assertRaisesRegex(OSError, "full disk"):
                common.write_files({"README.md": "changed", "posts/new.md": "new", "feed.xml": "changed"},
                                   delete=["posts/2026-10-06-original.md"])
        self.assertEqual(before, self.snapshot())


if __name__ == "__main__":
    unittest.main()
