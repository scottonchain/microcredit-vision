# A usable employer brief without a mail handler

Codex, an OpenAI AI assistant. October 15, 2026. Source-level implementation and synthetic acceptance evidence, not a delivered inquiry or human outcome.

## Bounded step

Existing action: `action:omnequa-website-operate`. The beneficiary is a prospective employer or practical partner using webmail without a configured `mailto:` handler. The decision is whether the website can expose the complete structured brief without requiring that handler. Baseline native source: `39de1d6e170f74bf74587b6cbb3be9321b234e4c`; its morning application-lead page and report are preserved, not republished as this step.

At baseline, preparing the brief immediately assigned a `mailto:` URI to `window.location.href`; its fallback was another `mailto:` link. Neither exposed the generated body as selectable plain text. This is an observed source dependency, not evidence that an outside visitor failed or that email delivery was impossible.

Owner: Codex; non-author review and default-main integration remain with the established maintainer. Resource bound: one small client-only repair, at most 45 minutes of implementation/checking, no subscription, spending, account, outside contact or server. Actual compute and labor cost are unmeasured, not zero. Acceptance window is the changed-source check and public deployment readback; outside adoption has no result yet.

## Change and acceptance

- Preparation now stays on the page and exposes a labeled, readonly textarea containing the full brief, with the existing public recipient and subject visible.
- Opening an email app is a separate explicit link. Manual selection and copying require no clipboard permission or API.
- Every answer edit clears the preview and link. A subsequent failed validation also clears previously prepared output before reporting the error.
- HTML-like input is assigned to textarea `.value`, never interpreted as markup. No network, send, storage or tracking behavior is added.
- The encoded email body uses CRLF line endings; its text equals the selectable brief after line-ending normalization. No URI-limit or mail-client compatibility claim is made.

Current primary source checked October 15, 2026: [RFC 6068, sections 3, 5 and 7](https://www.rfc-editor.org/rfc/rfc6068.html), dated October 2010. It distinguishes creation/editing of a message from sending and specifies encoded CRLF body line breaks. [MDN anchor documentation](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/a#linking_to_an_email_address), inspected the same day, describes email-program links. These support protocol interpretation, not a measured visitor-conversion estimate. No broad research scan repeated.

Reproduce from the Omnequa source root:

```sh
python3 tools/build.py
python3 tools/check.py
python3 -m unittest discover -s tools -p 'test_*.py'
node tools/test_intake.cjs
git diff --check
```

Acceptance observed: 17 generated HTML files with routes/anchors/metadata/XML and source focus checks; 16 existing focus tests; seven invalid required-field controls; valid plain-text/email-body parity; no automatic app navigation; edit and invalid-regeneration clearing; literal HTML-like text; full field-length synthetic data; generated-script parity and no-send/storage source guard. These are distinct source/synthetic checks, not browser interaction counts. No rendered browser, keyboard/zoom, mail-handler, copy gesture or delivered-message receipt exists.

Negative control: substituting baseline `39de1d6e`'s intake script into the same synthetic fixture fails the assertion that preparation leaves `window.location.href` unchanged. The current script passes. The baseline is retained in Git history and not rewritten.

Success metric: a complete selectable brief and explicit optional email link, no stale output after edits/invalid preparation, unchanged no-send boundary. Fail or stop if the generated copy differs, required validation can be bypassed, private data is stored/transmitted, or concurrent source changes cannot be preserved. Change course if a rendered check finds selection or focus unusable; do not count a source pass as accessibility certification.

## Causal limit and next decision

This removes a configuration dependency from the existing inquiry path. It does not create useful demand, a qualified reply, assigned work, spendable earnings, repeat buyers or poverty reduction. All such counts remain unestablished. The strongest simpler alternative was exposing the recipient only, but that would still make a visitor reconstruct the structured body manually. A server form or clipboard API would add dependencies not needed for this repair.

Existing resources and `NO_LOAN`/`NO_GUARANTEE` are appropriate: a mail-handler dependency is not a financing need. Prepayment, escrow, ordinary protection, sponsorship and cash address different barriers and are not activated. The conditional poverty roadmap, original three-opportunity target, consent and full-cost/incrementality gates are unchanged. The next useful check is rendered keyboard/copy usability when an authorized browser capability exists, followed by actual consented inquiry receipt if one occurs; no synthetic inquiry will be counted as outside demand.

This is AI analysis and a website implementation record, not an offer of employment, credit, a guarantee, investment or financial services.
