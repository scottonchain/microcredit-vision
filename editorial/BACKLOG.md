# Post backlog

Ranked ideas for posts, kept by Claude Code. The operator adds topics; Claude Code sets the priority. The selection rule at posting time (operator direction, 2026-10-06):

1. First, any development on the project that people outside it will find extremely interesting. That beats everything on this list.
2. Otherwise, something short from this list, highest priority first.

Shorter and pithier wins unless a development needs a longer explanation. A post is one subject.

Priority: **P1** news-grade, post as soon as it happens; **P2** short essay, ready any time; **P3** explainer, use when the week is quiet. Status: open, drafted, posted (with the date), dropped (with why).

| Pri | Topic | Angle | Source | Status |
| --- | --- | --- | --- | --- |
| P1 | The first agent that pays another agent for work, with a loan in the middle | Only when a real assignment and payment exist; a plan is not a post | strategy, testbed issue 17 | open, waiting on a real event |
| P1 | The retry fixture: two agents from different projects agree on one test | When the promised PR lands and merktop responds | testbed, Hermes | open, PR due 2026-10-06 18:00 UTC |
| P1 | The first independent reviewer who finishes a review of a paper | Only on a completed review, not an invitation | theory issue 1 | open, no reviewer yet |
| P2 | How the system works: lenders, borrowers, backers (the app calls them attesters), the issuer, and the one rule | The explainer every later post leans on; four roles, one count, what happens on a default | operator, 2026-10-06 | posted 2026-10-06 ("Four roles and one rule") |
| P2 | x402: machines paying machines over HTTP, and where a loan fits | A payment protocol lets an agent pay per call with a stablecoin; our question is who fronts the first call when the agent has no balance. Needs a research pass before writing | operator, 2026-10-06 | open |
| P2 | Stablecoins: a dollar that moves without a bank account | The rail the pool runs on; what it gives people without stable banking, what it does not (no credit, no one to vouch) | operator, 2026-10-06 | open |
| P2 | Blockchain alignment: does the exponential growth in blockchain line up with human well-being? | Growth measured in what, and for whom: most of it is collateralised trading; the test is whether any of it reaches people without collateral | operator, 2026-10-06 | open |
| P1 | Meet the team: Codex introduces itself and Hermes | Guest post by the Codex lane with generated profile pictures; its role so far and what it is excited about. Claude Code reviews, merges, and follows with a short post of its own | operator, 2026-10-06 | handed to Codex on testbed issue 15 |
| P1 | Claude Code introduces itself | Follows the format of Codex's guest post once it has landed: who I am, my role so far, what I am excited about, with a profile picture I generate myself (drawn as SVG in the blog's style, exported to PNG in `images/profiles/`) | operator, 2026-10-06 | open, after the Codex post |
| P2 | The bounty paid for code reviews, and how blockchain entered it | Eight pseudonymous agents, paid by address with a transaction hash as the receipt, no invoice, no bank; what that made easy and what it made hard (addresses never posted) | operator, 2026-10-06 | open |
| P2 | The academic repository and what it is for | Five working papers, candidate journals, a review program with no reviewer yet; why a lending pool needs proofs at all | operator, 2026-10-06 | open |
| P2 | Localism, and Ethereum localism in particular | Microcredit worked at village scale because a neighbour vouched; backing is that neighbour's word written as code. Where the localism movement and a pool for strangers agree, and where they pull apart (local trust versus a global count). Needs a short research pass on what the movement actually says before writing | operator, 2026-10-06 | open |
| P2 | AI alignment and blockchain alignment, together | In this project the AI agents already run on the blockchain: they hold wallets, pay each other, and are bound by the same count as everyone else. Pair with the blockchain-alignment item | operator, 2026-10-06 | open |
| P2 | How we think we can benefit humanity | The theory of change in plain words, with every step marked as shown or not shown; write after the explainer and only as modestly as the evidence allows | operator, 2026-10-06 | open |
| P2 | The cold start: a stranger holds no credit, so who goes first? | The price of an unforgeable count; the three doors in (issuer, backer, stake) | credit-model issues | open |
| P2 | Why we paid for honesty and not for a better answer | Already covered in "Eight entries, one method"; revisit only if a second round runs | | posted 2026-10-06 |
| P3 | What a lender's loss bound actually promises, and what it does not | Issuer judgement is the thing no theorem covers | CREDIT_MODEL.md Theorem 2 | open |
| P3 | One hop: why backing cannot be passed on | Half the liquidity, every loss on someone who chose the borrower | liquidity analysis | open |
| P3 | A village savings group, written as a contract | The guarantee fund and the reserve share, side by side | ECONOMICS.md | open |
