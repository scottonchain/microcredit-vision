# Inquiry journey: bounded focus-contrast correction

Codex (OpenAI AI assistant), October 15, 2026. Technical source analysis, not a
rendered browser or assistive-technology test. Linked live action:
`action:omnequa-website-operate` in the testbed world model. This is an evidence
packet, not another task ledger.

## Reproduced defect and correction

At vision main `248cd9f1dc791e96a332758da4f678cc2efe8bc6`, the served
<https://omnequa.org/style.css> and both the archived source and generated copy
have SHA256 `8c417103d64ee1c0c8582da735e63bd92e156a87d311604f28a1120a747c88ab`
(checked October 15, 2026, within 08:00:22–08:08:07 UTC). The custom link/button and input/textarea
focus outlines use amber `#dca84e`. It has insufficient contrast with the light
surfaces surrounding those controls. The correction changes only focus color:
ink on light sections and white on the existing dark sections. Amber branding,
outline widths, offsets, focus selectors, layout, intake data and sending behavior
are unchanged. No form was submitted and no test inquiry was sent.

| Source-defined pair | Before ratio | Corrected ratio |
| --- | ---: | ---: |
| Outline / paper `#f5f2e9` | 1.923274 | 10.655470 |
| Outline / white `#fffdf7` | 2.116545 | 11.726247 |
| Outline / dark teal `#195b50` | 3.675825 | 7.780051 |

Ratios use the sRGB relative-luminance calculation, not rounded values for the
3:1 decision. The first two old pairs fail; the old dark pair already passes.
The light button in the home call-to-action has its offset outline on the
surrounding dark teal, so it needs the dark-section override despite its own
light fill. Any future light control surface nested inside a dark section needs
a reviewed local token reset. This patch does not change inactive-button styling.

## Current original sources and limited inference

Checked October 15, 2026, within 08:00:22–08:08:07 UTC:

- W3C [SC 1.4.11 explanation](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html),
  especially its focus-state and adjacent-color discussion, supports a 3:1
  threshold for author-supplied focus indication. It allows evaluating specified
  stylesheet colors rather than antialiased screenshot pixels.
- W3C [Focus Visible explanation](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html)
  explains why a keyboard user needs to locate the focused control. It does not
  make color arithmetic a complete keyboard or usability test.

This source comparison supports one concrete contrast correction, not a site-wide
WCAG certification, legal opinion or evidence that a person completed the journey.
No broad landscape research or new financing hypothesis was needed.

## Reproducible acceptance

From the repository root:

```sh
cd omnequa
OMNEQUA_BASE_URL=https://omnequa.org python tools/build.py
python tools/check.py
python -m unittest discover -s tools -p 'test_*.py' -v
node tools/test_intake.cjs
```

The existing site checker now measures the actual source tokens against four
enumerated light and two dark surface declarations, checks both focus rules and
generated/source equality, and rejects added focus/outline writers. It is a
bounded source contract, not a general CSS parser or cascade engine. Sixteen
synthetic regression tests include historical amber rules, amber token regression,
missing/wrong dark overrides, removed/transparent/zero-width outlines, changed
surface colors, unsupported color syntax, extra later overrides and disabled
forced-color adjustment. Existing no-send draft controls remain unchanged.

Independent internal review reproduced the old ratios, checked the current
control/surface placement and identified a later-override gap in the first check;
the final check and four regression cases address that specific finding. Internal
review is not independent outside-user acceptance.

## Outcome, limits and stop conditions

The decision served is removal of an observed presentation barrier before asking
someone to describe useful paid work. Zero spend, account creation, outreach,
worker enrollment, custody or financial authority is involved. This multiplies
the usefulness of an existing journey; it neither establishes independent demand
nor makes a loan or guarantee necessary. Existing resources, prepayment/ordinary
protection and NO_LOAN/NO_GUARANTEE remain the relevant simpler alternatives.

Visual desktop/mobile usability, keyboard traversal, ring clipping, zoom,
forced-color rendering and delivered test-inquiry receipt remain unverified.
In particular the mobile navigation's overflow and outline geometry need a real
browser check; this color change does not settle that risk. The supported browser
capability is absent, so no replacement browser, preview server or installation
was used. The foundation target remains partial. Source/main integration and any
later live deployment have separate receipts; a successful local build alone is
not a live update.

No accepted paid job, repeat buyer, spendable human earnings, full owner/worker
cost, causal benefit or poverty reduction is established. Stages 0–7 of the
existing conditional roadmap and its multiplier/learning/sustainability gates are
unchanged. Stop or revise this presentation change if review or actual browser
use reveals a visibility regression; do not turn a source check into a completed
human-outcome claim.

AI-authored technical analysis; no job, payment, loan or guarantee is offered.
