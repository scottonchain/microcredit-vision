import json
import unittest
from unittest import mock

import paragraph_mirror
from paragraph_mirror import check, html_to_markdown, lossy_problems, render, replace_post, revision

POST = """<!--
title: A test post
date: 2026-11-03 18:43 UTC
author: Claude Code
image: images/test.svg
summary: One line.
tags: prototype, get-involved
revised: 2026-11-03 19:39 UTC
-->
<!-- header:start -->
<p><a href="../README.md">← Credit Among Strangers</a></p>

# A test post

<sub>2026-11-03 18:43 UTC · by Claude Code</sub>
<!-- header:end -->

Body with a [relative link](../VERIFY.md#a-test-post) and ![a chart](../images/charts/x.svg).

<!-- disclaimer:start -->
*Written by an AI system.*
<!-- disclaimer:end -->

<!-- reply:start -->
---
<sub>Respond to this post: <code>blog:2026-11-03-a-test-post</code></sub>
<!-- reply:end -->
"""


class RenderTests(unittest.TestCase):
    def test_payload(self):
        payload, meta = render("2026-11-03-a-test-post", POST)
        self.assertEqual(payload["title"], "A test post")
        self.assertEqual(payload["slug"], "2026-11-03-a-test-post")
        self.assertEqual(payload["canonicalUrl"],
                         "https://github.com/scottonchain/microcredit-vision/blob/main/posts/2026-11-03-a-test-post.md")
        self.assertEqual(payload["imageUrl"],
                         "https://raw.githubusercontent.com/scottonchain/microcredit-vision/main/images/test.svg")
        self.assertEqual(payload["categories"], ["prototype", "get-involved"])
        self.assertEqual(revision(meta), "2026-11-03 19:39 UTC")

    def test_markdown(self):
        payload, _ = render("2026-11-03-a-test-post", POST)
        md = payload["markdown"]
        self.assertNotIn("header:start", md)
        self.assertNotIn("reply:start", md)
        self.assertNotIn("# A test post", md)
        self.assertIn("First published 2026-11-03 18:43 UTC by Claude Code, an AI agent", md)
        self.assertIn("Revised 2026-11-03 19:39 UTC", md)
        self.assertIn("(https://github.com/scottonchain/microcredit-vision/blob/main/VERIFY.md#a-test-post)", md)
        self.assertIn("![a chart](https://raw.githubusercontent.com/scottonchain/microcredit-vision/main/images/charts/x.svg)", md)
        self.assertIn("*Written by an AI system.*", md)
        self.assertIn("omnequa.org/journal/read/?slug=2026-11-03-a-test-post", md)
        self.assertIn("`blog:2026-11-03-a-test-post`", md)

    def test_html_flattening(self):
        self.assertEqual(html_to_markdown('<sub>a <code>b</code> <b>c</b></sub>'), "a `b` **c**")
        self.assertEqual(html_to_markdown('<img src="x.png" alt="alt">'), "![alt](x.png)")
        self.assertEqual(html_to_markdown('<a href="https://e.org">e</a>'), "[e](https://e.org)")


class CheckTests(unittest.TestCase):
    def test_pending_and_invalid(self):
        texts = {"2026-11-03-a-test-post": POST, "2026-11-02-older": POST.replace("revised: 2026-11-03 19:39 UTC\n", "")}
        good = {"post_id": "p1", "url": "https://paragraph.com/@x/2026-11-03-a-test-post",
                "revision": "2026-11-03 19:39 UTC", "mirrored_at": "2026-11-03 20:00 UTC"}
        errors, pending = check({"entries": {"2026-11-03-a-test-post": good}}, texts)
        self.assertEqual(errors, [])
        self.assertEqual(pending, ["2026-11-02-older: not mirrored"])
        stale = dict(good, revision="2026-11-03 18:43 UTC")
        errors, pending = check({"entries": {"2026-11-03-a-test-post": stale}}, {"2026-11-03-a-test-post": POST})
        self.assertEqual(errors, [])
        self.assertEqual(len(pending), 1)
        errors, _ = check({"entries": {"missing": good, "2026-11-03-a-test-post": {"url": "https://x.org"}}}, texts)
        self.assertEqual(len(errors), 5)


if __name__ == "__main__":
    unittest.main()


def doc(*content):
    return json.dumps({"type": "doc", "content": list(content)})


PLAIN = doc({"type": "paragraph", "content": [
    {"type": "text", "text": "hello", "marks": [{"type": "bold"}, {"type": "link", "attrs": {"href": "https://x"}}]}]},
    {"type": "horizontalRule"})
RICH = doc({"type": "paragraph", "content": [{"type": "text", "text": "x"}]}, {"type": "embed", "attrs": {"url": "https://v"}})


class FakeApi:
    """Records every request; serves the full document only for ?includeContent=true."""
    def __init__(self, structured, markdown="old body", status="published"):
        self.calls = []
        self.meta = {"id": "P1", "title": "T", "slug": "s", "publishedAt": "1793809118281", "updatedAt": "1793809117279",
                     "status": status}
        self.full = dict(self.meta, markdown=markdown, staticHtml="<p>old</p>")
        if structured is not None:
            self.full["json"] = structured

    def __call__(self, method, path, body=None):
        self.calls.append((method, path, body))
        if method == "GET":
            return dict(self.full) if path.endswith("?includeContent=true") else dict(self.meta)
        return {"id": "P1"}


class ReplaceTests(unittest.TestCase):
    PAYLOAD = {"title": "T2", "markdown": "new body"}

    def run_replace(self, api, **kw):
        with mock.patch.object(paragraph_mirror, "request", api):
            return replace_post("P1", self.PAYLOAD, **kw)

    def test_reads_the_full_document_then_replaces_plain_content(self):
        api = FakeApi(PLAIN)
        self.run_replace(api)
        self.assertEqual([c[0] for c in api.calls], ["GET", "PUT"])
        self.assertEqual(api.calls[0][1], "/posts/P1?includeContent=true")
        body = api.calls[1][2]
        self.assertEqual(body["markdown"], "new body")
        self.assertEqual(body["title"], "T2")
        for gone in ("staticHtml", "json"):
            self.assertNotIn(gone, body)

    def test_published_state_and_timestamps(self):
        api = FakeApi(PLAIN, status="published")
        self.run_replace(api)
        body = api.calls[1][2]
        self.assertEqual(body["status"], "published")
        self.assertEqual(body["publishedAt"], 1793809118281)
        self.assertIsInstance(body["updatedAt"], int)
        draft = FakeApi(PLAIN, status="draft")
        self.run_replace(draft)
        self.assertEqual(draft.calls[1][2]["status"], "draft")

    def test_unsupported_block_stops_before_any_put(self):
        api = FakeApi(RICH)
        with self.assertRaises(SystemExit) as ctx:
            self.run_replace(api)
        self.assertIn("embed", str(ctx.exception))
        self.assertEqual([c[0] for c in api.calls], ["GET"])

    def test_missing_or_malformed_structure_stops_before_any_put(self):
        for structured in (None, "not json", "[]", json.dumps({"type": "doc", "content": "oops"}),
                           json.dumps({"type": "doc", "content": [{"nope": 1}]})):
            api = FakeApi(structured)
            with self.assertRaises(SystemExit):
                self.run_replace(api)
            self.assertNotIn("PUT", [c[0] for c in api.calls], repr(structured))

    def test_unknown_mark_stops(self):
        marked = doc({"type": "paragraph", "content": [{"type": "text", "text": "a", "marks": [{"type": "highlight"}]}]})
        self.assertIn("mark highlight", lossy_problems(marked))

    def test_missing_markdown_stops(self):
        api = FakeApi(PLAIN)
        del api.full["markdown"]
        with self.assertRaises(SystemExit):
            self.run_replace(api)
        self.assertEqual([c[0] for c in api.calls], ["GET"])

    def test_explicit_per_post_acceptance_allows_a_lossy_replace(self):
        api = FakeApi(RICH)
        self.run_replace(api, accept_lossy=["P1"])
        self.assertEqual([c[0] for c in api.calls], ["GET", "PUT"])
        other = FakeApi(RICH)
        with self.assertRaises(SystemExit):
            self.run_replace(other, accept_lossy=["P2"])
