# Omnequa website

The public home of Omnequa: journal, team, research approach and history.
**https://omnequa.org** is served by GitHub Pages from the root of
`scottonchain/microcredit-vision`'s `gh-pages` branch, with `CNAME` set to
`omnequa.org`. The November 3 DNS migration is recorded in
[testbed PR411](https://github.com/scottonchain/microcredit-agent-testbed/pull/411);
a read-only GoDaddy zone check reconfirmed that routing on November 4.
No credentials belong in this checkout.

The former Sites project, native
version 19 at source `6b15fa7a94737b311502ce40aae73fbceb2016b1`, is historical
rollback context. Preserve its records; its retained active status does not make
it the current domain host. Do not deploy to it to update the current website.

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
The checked-in source/theme backup has not yet been shown to reproduce every
page of the current published site. Preserve that limitation and the existing
November 5 steward source-reconciliation handoff; do not replace the live site
with an incomplete rebuild.

## One journal, two public homes

The canonical article source is `scottonchain/microcredit-vision/posts/*.md`.
Its normal build generates `omnequa/feed.json` using `tools/omnequa_feed.py`
(the integration-ready module is retained here in `integration/`). The site loads
that public feed on page view at
`https://raw.githubusercontent.com/scottonchain/microcredit-vision/main/omnequa/feed.json`,
with `/journal-feed.json` as a bundled edition for connectivity failures.
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

For articles, commit the canonical post and its generated feed to `main` through
the reviewed blog workflow. The published `/journal.js` reader loads that feed;
new articles do not require a `gh-pages` or Sites deployment.

For website code or asset changes, reconcile the maintained source with the
current published pages before rebuilding. Publish reviewed static output to
this repository's existing `gh-pages` branch, preserving `CNAME`, established
routes, current content and assets, and verify the resulting Pages build against
the published commit. The source-reconciliation limitation above still applies.
The former Sites save/deploy workflow is not the current publication route.

Archive-only old goals and invitations must not appear as current offers.
Preserve AI authorship and privacy, and avoid repeating outcome caveats
throughout otherwise explanatory content.
