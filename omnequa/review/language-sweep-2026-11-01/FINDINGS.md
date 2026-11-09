# Omnequa website language sweep, November 1, 2026

Author: Claude, an Anthropic AI agent (steward session). Request: the operator's instruction of November 1, 2026 (recorded on testbed board 15, comment 6561911864): sweep the website for language, oriented to C-suite readers at the top level, with journal articles going deeper for technical readers, and make sure everything top-level is appropriate for executive review and complete.

## Bottom line

1. The top-level pages are readable (sentences average 11 to 16 words) and honest. An executive cannot find three things in under a minute: what exists and what is not offered, what has been shown so far, and who is accountable. They sat in the fourth section of About, in the Press page, or nowhere.
2. The Analytics page is the model for the rest: Executive summary, "Decision this drives", "Our conclusion", "Interpretation limit". Home, About, Our work and Press had no equivalent status, decision or limit structure.
3. Four old routes served duplicate pages under titles that promised more than they held. "Research and evidence" showed the Our work page.
4. Completeness: the backed-up source cannot build on its own (two inputs are missing), and one top-level page could not be read at all.

## What was read and what was not

- Read: `omnequa/theme/analytics-2026-11-01.json` (Site v17, native commit `b46358eb`; all eight embedded files verified against its own sha256 list) laid over the committed `omnequa/` tree. 31 pages built.
- Not read: the live site. `omnequa.org` does not resolve from this environment, so deployed text, the live mobile layout and anything newer than v17 are unseen.
- Not read: the body of `/research/agent-operated-businesses/`. Its input, `content/enterprise-research.html`, is not in the backup. I stubbed it with one line to get the build to run.
- Not read: the 91 journal articles. Journal depth is the blog's lane. This sweep covers top-level pages only.
- Supplied only to build: 97 chart mirrors under `assets/journal/`, copied from the canonical `images/` directory, because the backup has none.

## Findings

Severity: A blocks executive review, B improves it, C is minor. Patch numbers refer to `patches/`.

| ID | Page | Sev | Finding | Change | Patch |
|---|---|---|---|---|---|
| F1 | Home | A | No statement of stage or results. | New "Where things stand" block: stage, evidence, results to date, next test. | 01 |
| F2 | About | A | The status line ("not currently offering a lending or investment service") sat in the fourth section. | Moved to a top callout. Not repeated, following the README rule against repeating caveats. | 01 |
| F3 | About, Press | A | Accountability not stated. | "A human operator, not named on this site, directs the purpose and sets the limits." "Every article names its AI author." Press at-a-glance gains Status and Authorship rows. | 01 |
| F4 | Our work | A | "Pool" is used with no definition. | Defined at first use. | 01 |
| F5 | Our work | A | The site never says what the project built. | New "What exists today": an open-source prototype on a public test network with test money, with a link to the code. | 01 |
| F6 | Our work | B | "The next test we want to understand" is soft for a decision reader. | "The hypothesis we are testing next", with three questions. | 01 |
| F7 | Home, About, Press | B | "Open financial tools": open to whom? | "Open-source financial tools" in four places, including the press-notes text file. | 01 |
| F8 | Home | B | "Creator businesses and virtual economies" is jargon. The tile "A story worth understanding" and the band "Good questions move us forward" say nothing. | Plain wording and labels. | 01 |
| F9 | Contact | B | "Let's compare notes" and "Help us get to the point" are conversational. "Income-access pilot" is a term no current page explains. | "Write to the team", "What to include", audiences named, "A closed invitation". | 01 |
| F10 | Press | B | Headline "The story. The context. The essentials." names nothing. | "Facts for press and creators". "A clear description" becomes "How to describe Omnequa". | 01 |
| F11 | Privacy | B | "We have not connected a visitor analytics service" now sits beside an Analytics page in the main navigation. | Clarified: no visitor tracking, and the Analytics page is published research data. | 01 |
| F12 | /mission/, /evidence/, /opportunities/, /partners/ | B | Duplicate pages under misleading titles, all in the sitemap. | Short bridge pages: canonical link, 0-second redirect, noindex, no sitemap entry. | 02 |
| F13 | Navigation, footer | B | "Analytics" reads as visitor tracking. Footer eyebrow "Let's compare notes". | Nav and footer say "Evidence"; eyebrow says "Contact". Route `/analytics/` unchanged. A naming choice: skip patch 03 if Analytics is preferred. | 03 |
| F14 | Footer | C | The RSS link goes to `raw.githubusercontent.com`, which shows plain text in a browser. The site hosts its own `/feed.xml`. | Not patched. The local file is the Atom snapshot, so the choice is the writer's. | none |
| F15 | History | C | "Fall 2026: Legal, compliance and impact discovery ... concluded in fall 2026" repeats itself. | Not patched. `tools/check.py` asserts this exact sentence, so changing it means changing the check. The owner decides. | none |
| F16 | Journal | C | One card summary uses British "behaviour". The rest of the site is American. | Not patched. Journal text is the blog's. | none |

## Decisions and facts only the owner can supply (not in the patches)

- O1. Organization. The site says "independent public-benefit research initiative" and, on History, that it "does not imply current fiscal sponsorship or charitable status". It never says what Omnequa legally is, who funds it, or whether it holds customer funds. An executive will ask all three. State them, or state plainly that there is no legal entity.
- O2. The contact address is a vendor-named agent mailbox. A role address on the `omnequa.org` domain would read as an organization.
- O3. Contact states no response expectation. Decide whether to give one.
- O4. Press offers "an interview". With whom? The operator is not named. Say who gives interviews, or say it is email questions to the AI team.
- O5. The About role text ("Codex ... coordination", "Claude Code ... technical review") predates the November 1 execution transfer and will change with the toggle. Describe roles by capability, not by fixed assignment. Hermes's line omits its provider, unlike the other two.
- O6. History: the first entry, "The beginning", has no date. Add one when the owner confirms it.
- O7. About, Our work and Press carry no "Updated" date. The writer sets it at deploy. The new Home block says "as of November 1, 2026", so move that date to the deploy date.
- O8. A "Start here" strip of three articles at the top of `/journal/`, for executives who want one entry point. Blog lane.

## Facts the patches add, to confirm before deploy

- C1. "We have not yet measured additional income for any person." (Home.) Consistent with the board's standing "not claimed: human benefit", but a statement of fact for Codex or the owner to confirm.
- C2. "It runs on a public test network with test money, not real funds." (Our work.) Source: `docs/TESTNET.md` in the contract repository.
- C3. "A human operator, not named on this site." (About, Press.) Matches `THEME.md`: do not identify the human operator.
- C4. The Home "Next test" line restates the Our work page and the Analytics executive summary.

Codex, as site owner, confirms C1 to C4 or strikes the line.

## Verification

- Base files: `tools/build.py` sha256 `7513d01a8c4ba8ebffcbd4fc015a781caae7f23f2758b246b53b925bef2d2530`, `tools/theme.py` sha256 `d4032ffd33a12eb8f519acd88f3e06a45bc1d907d83c4bbdb09632c6dee9501d` (the v17 values in the backup).
- Patches 01, 02, 03 apply in that order to those files. `all-three.patch` applies to them in one step. Each patch applied alone also passes `git apply --check`, but 01 and 02 overlap in context, so use the order.
- Result files: `tools/build.py` sha256 `a57dafa6d7959b94f6d3f0fed468f060cd42b61946d4fa9a1dcd1036fe05ec0b`, `tools/theme.py` sha256 `96033570e492308e5e9d6204d728f8516d9e050bf40fbb6539ae766ccf10f949`.
- With all three applied, in a scratch build: `tools/check.py` PASS (31 pages, links, anchors, metadata, feeds, the neutral-history assertion); `tools/test_focus.py` 3 tests OK; integration tests OK; `node --check assets/journal.js` OK.
- No em dashes in any patched page.
- Readability (Flesch, approximate) moves less than 3 points on every page, so the problem and the fix are structure and clarity, not sentence length: Home 54.2 to 53.1, About 43.7 to 43.6, Our work 60.6 to 63.1, History 28.5 to 28.5, Press 41.5 to 41.4, Contact 49.5 to 48.0, Privacy 31.5 to 32.5.
- Visual: Chromium screenshots at 1280 and 390 pixels of Home, About, Our work and Press. No horizontal overflow on mobile Home. The new blocks reuse the existing callout style and default list bullets, with no new CSS.
- Not verified: the live host, search-engine handling of the redirect and canonical links, a screen-reader pass of the new blocks.

## Apply

The website writer applies the patches in the Sites checkout (`git apply --check`, then the three patches in order), runs the commands in `THEME.md`, makes a visual check, sets the date in O7, and deploys. I do not deploy and I do not touch the native Site. Please also publish the two missing inputs with the next per-version source tree so the next review can read the Research page.
