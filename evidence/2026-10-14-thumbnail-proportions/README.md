# YouTube thumbnail proportions

Codex (AI), 2026-10-14. Baseline: `ec3add1865c605aa5675de8027ab02500a877155`.

The live blog is the repository README on GitHub, with full articles under
`posts/`. The README's latest article and five published video articles use
YouTube hero images. Archive/category tables use the existing SVG illustrations;
they are not video thumbnails and are unchanged.

## Diagnosis and correction

Live GitHub markup and Chromium inspection showed a 480×360 image displayed at
560×315. GitHub removes `object-fit` and `aspect-ratio`, retaining a height cap.
The original PNGs contain 45-pixel black letterbox bars above and below the
480×270 picture. All seven were visually inspected, including two staged assets.

Each PNG is now the exact `(0,45,480,315)` crop of its original: no picture or
play-overlay pixels were resized or repainted. The generator makes 480×270
center-cropped thumbnails with the same centered play button. Video hero markup
keeps width 560 and responsive maximum width, with natural height and no forced
height attribute. The remote `mqdefault.jpg` fallback is already 16:9. Links and
labels are unchanged. The instruction paragraph now describes the existing hero
placement and corrected dimensions.

## Checks

- 120 unit tests passed; includes native-ratio markup/fallback and pixel-preserving
  letterbox-crop regressions.
- `python3 tools/build.py --check`: 52 posts, 69 rendered outputs validated.
- Generated outputs rebuilt through `build.prepare`/`write_files`, preserving
  baseline Atom order for equal-date entries (the ordinary glob-based build
  otherwise reorders unrelated tied entries).
- All seven new PNGs compared pixel-for-pixel with the baseline central crop.
- All 52 parsed post bodies unchanged; no title, date, disclaimer, source, name,
  prose or archive/category/feed changes. `git diff --check` passed.

## Browser evidence and limits

Chromium confirmed the live README's old natural size 480×360 and displayed size
560×315. GitHub's external stylesheet host is blocked by this environment, and
its dynamic article view did not finish rendering. Thus these screenshots are
**isolated previews of GitHub's actual sanitized README/article HTML**, using
its surviving inline styles, not a fully styled GitHub-page certification. The
article HTML was read from GitHub's `codeViewBlobRoute.richText` payload. No new
site CSS or substitute design system was added.

`measurements.json` records before/after dimensions for both surfaces at 1280,
390 and 320 viewport widths. Desktop becomes 560×315 with native 480×270 pixels;
mobile dimensions retain 16:9 within the article width. The YouTube href and
accessible Watch video label are checked. PNG pairs show desktop and mobile
before/after, with the real image and play overlay. Fully styled live verification
remains a maintainer check after review/integration. This branch does not deploy
or merge anything.
