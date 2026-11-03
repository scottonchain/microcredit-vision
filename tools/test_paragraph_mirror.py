import unittest

from paragraph_mirror import check, html_to_markdown, render, revision

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
