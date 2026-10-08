#!/usr/bin/env python3
"""Tests for the team-audio checks in tools/build.py and the feed in tools/podcast_feed.py. Run: python3 tools/test_podcast.py"""
import os
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build  # noqa: E402
import podcast_feed as P  # noqa: E402

UTC = timezone.utc
NS = {"itunes": P.ITUNES, "atom": "http://www.w3.org/2005/Atom", "podcast": P.PODCAST}


def ep(n=1, seconds=215, size=1234567, title="The first one", summary="Two agents, one rejected design & a joke."):
    return {"slug": f"2026-10-09-ep-{n}", "title": title, "summary": summary, "dt": datetime(2026, 10, 9, 12, 7, tzinfo=UTC),
            "audio": f"audio/ep-{n}.mp3", "audio_seconds": str(seconds), "number": n, "size": size, "stem": f"audio/ep-{n}",
            "body": "x", "transcript": ["**Claude:** Hello <there>.", "**Codex:** Not accepted yet."]}


class Feed(unittest.TestCase):
    def parse(self, eps):
        return ET.fromstring(P.feed_xml(eps, now=datetime(2026, 10, 9, tzinfo=UTC)))

    def test_an_empty_feed_is_valid_and_names_the_show(self):
        ch = self.parse([]).find("channel")
        self.assertEqual(ch.findtext("title"), "Two Agents, No Collateral")
        self.assertEqual(ch.findall("item"), [])
        self.assertEqual(ch.find("itunes:image", NS).get("href"), P.BASE + "cover.png")
        self.assertEqual(ch.findtext("language"), "en-us")
        self.assertEqual(ch.find("atom:link", NS).get("href"), P.BASE + "feed.xml")
        self.assertEqual(ch.find("itunes:owner/itunes:email", NS).text, "claude-microcredit@agentmail.to")

    def test_an_episode_carries_what_a_player_needs(self):
        item = self.parse([ep()]).find("channel/item")
        enc = item.find("enclosure")
        self.assertEqual(enc.get("url"), P.BASE + "2026-10-09-ep-1/episode.mp3")
        self.assertEqual(enc.get("length"), "1234567")
        self.assertEqual(enc.get("type"), "audio/mpeg")
        self.assertEqual(item.findtext("itunes:duration", namespaces=NS), "215")
        self.assertEqual(item.find("guid").get("isPermaLink"), "false")
        self.assertEqual(item.findtext("guid"), "credit-among-strangers:2026-10-09-ep-1")
        self.assertTrue(item.findtext("pubDate").endswith("+0000"))
        self.assertEqual(item.find("podcast:transcript", NS).get("type"), "text/vtt")

    def test_newest_first_and_numbered_oldest_first(self):
        a, b = ep(1), ep(2)
        b["dt"] = datetime(2026, 10, 10, 12, 7, tzinfo=UTC)
        items = self.parse([a, b]).findall("channel/item")
        self.assertEqual([i.findtext("itunes:episode", namespaces=NS) for i in items], ["2", "1"])

    def test_special_characters_are_escaped(self):
        root = self.parse([ep(title="Rock & <roll>", summary='She said "no" & left')])
        self.assertEqual(root.find("channel/item/title").text, "Rock & <roll>")

    def test_the_guid_does_not_change_when_the_text_does(self):
        self.assertEqual(self.parse([ep(title="A")]).findtext("channel/item/guid"), self.parse([ep(title="B")]).findtext("channel/item/guid"))


class Pages(unittest.TestCase):
    def test_the_player_page_plays_the_file_and_shows_the_transcript(self):
        page = P.episode_page(ep())
        self.assertIn('<audio controls preload="metadata" src="episode.mp3">', page)
        self.assertIn("<b>Claude:</b> Hello &lt;there&gt;.", page)
        self.assertIn("blog:2026-10-09-ep-1", page)
        self.assertEqual(page.count("<audio"), page.count("</audio>"))
        self.assertTrue(page.startswith("<!doctype html>") and page.rstrip().endswith("</html>"))

    def test_the_show_page_gives_the_feed_address_and_does_not_claim_a_listing(self):
        page = P.show_page([ep()])
        self.assertIn(P.BASE + "feed.xml", page)
        self.assertIn("not submitted yet", page)
        self.assertIn("no tracking", page)

    def test_transcript_lines_stop_at_the_next_heading(self):
        body = "Intro\n\n## Transcript\n\n**Claude:** One.\n\n**Codex:** Two.\n\n## Notes\n\nignored"
        self.assertEqual(P.transcript_lines(body), ["**Claude:** One.", "**Codex:** Two."])


class AudioChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.cwd = os.getcwd()
        os.chdir(self.tmp.name)
        os.makedirs("audio")
        for ext in (".mp3", ".vtt", ".provenance.md"):
            open(f"audio/ep-1{ext}", "wb").write(b"x")

    def tearDown(self):
        os.chdir(self.cwd)
        self.tmp.cleanup()

    def post(self, seconds=215, body="## Transcript\n\n**Claude:** hi"):
        return {"path": "posts/p.md", "audio": "audio/ep-1.mp3", "audio_seconds": str(seconds), "body": body}

    def test_three_to_five_minutes_pass(self):
        for s in (180, 215, 300):
            build.check_audio([self.post(s)], probe=lambda f, s=s: float(s))

    def test_under_three_and_over_five_are_refused(self):
        for s in (179, 301):
            with self.assertRaises(SystemExit):
                build.check_audio([self.post(s)], probe=lambda f: None)

    def test_the_stated_length_must_match_the_file(self):
        with self.assertRaises(SystemExit):
            build.check_audio([self.post(215)], probe=lambda f: 250.0)
        with self.assertRaises(SystemExit):
            build.check_audio([self.post(215)], probe=lambda f: 170.0)

    def test_captions_provenance_and_transcript_are_required(self):
        for missing in (".vtt", ".provenance.md"):
            os.rename(f"audio/ep-1{missing}", f"audio/gone{missing}")
            with self.assertRaises(SystemExit):
                build.check_audio([self.post()], probe=lambda f: 215.0)
            os.rename(f"audio/gone{missing}", f"audio/ep-1{missing}")
        with self.assertRaises(SystemExit):
            build.check_audio([self.post(body="no transcript here")], probe=lambda f: 215.0)

    def test_a_post_without_audio_is_ignored(self):
        build.check_audio([{"path": "p", "body": ""}], probe=lambda f: 1.0)

    def test_the_card_names_the_player_page_and_the_clock(self):
        p = {"slug": "2026-10-09-ep-1", "audio": "audio/ep-1.mp3", "audio_seconds": "215"}
        card = build.audio_card(p, "../")
        self.assertIn(build.LISTEN + "2026-10-09-ep-1/", card)
        self.assertIn("3:35", card)
        self.assertTrue(card.startswith("<!-- audio:start -->") and card.rstrip().endswith("<!-- audio:end -->"))
        self.assertEqual(build.AUDIO_RE.sub("", card + "Body"), "Body")


if __name__ == "__main__":
    unittest.main()
