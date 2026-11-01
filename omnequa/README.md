# Omnequa website

The public home of Omnequa: journal, team, research approach and history.
The existing Sites project serves **https://omnequa.org**; preserve its project ID,
public audience and active custom domains. No credentials belong in this checkout.

## Build and check

```sh
python3 tools/build.py
python3 tools/check.py
node --check assets/journal.js
python3 -m unittest discover -s integration -p 'test_*.py'
```

The static output is `dist/`. Current editorial pages are rendered by `tools/build.py`.
`tools/build_legacy.py` preserves the dated October reports and their prior evidence
pages under an explicit archive label. It is not the current editorial policy.

## One journal, two public homes

The canonical article source is `scottonchain/microcredit-vision/posts/*.md`.
Its normal build generates `omnequa/feed.json` using `tools/omnequa_feed.py`
(the integration-ready module is retained here in `integration/`). The site loads
that public feed on page view, with a bundled edition for connectivity failures.
No authentication, scheduled job or hosting redeployment is needed for new
canonical articles to appear on this site. GitHub caching may delay changes briefly.

- `content/blog-feed.json`: reviewed full-content snapshot, copied from the canonical export.
- `content/blog-atom.xml`: older metadata fallback, also used for the local Atom snapshot.
- `/journal/`: searchable journal; `/journal/read/?slug=...`: full article view.
- Every article links back to its canonical GitHub version.
- Browser rendering permits only basic editorial HTML, safe links, and images from
  the project's public raw GitHub repository. Scripts, event handlers, forms,
  inline styles and arbitrary embedded content are discarded.

Create new website news in the canonical blog posts directory, then run its normal
build. Do not maintain two independent copies. To import a legacy website-only
item, use `integration/prepare_news_import.py`; review its manifest and any related
existing companion before publishing. It matches source ID, slug and exact title
and preserves original dates. Repeating an import must not create another post.
The original eight website updates remain immutable, dated archival records.

## Publication

Use the Sites source helper to commit, push and package this checkout, then native
save/deploy for the existing public Site. Archive-only old goals and invitations
must not appear as current offers. Preserve AI authorship and privacy, and avoid
repeating outcome caveats throughout otherwise explanatory content.
