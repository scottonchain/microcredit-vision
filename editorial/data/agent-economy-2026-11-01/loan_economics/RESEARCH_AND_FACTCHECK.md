# Article 3: editorial and evidence handoff

Article: `2026-11-01-small-loans-familiar-economics.md`.

The feature has three figures, not three proposed future charts. All SVG and PNG assets are in `charts/`; inputs, observed values and calculated values are in `data/`. Reproduce with `python3 plot_charts.py`. The script uses Python 3, matplotlib and numpy, requires no network, and checks the main arithmetic. All three PNGs were visually inspected for legibility. Source pricing was checked November 1, 2026.

## Editorial fit

The current microcredit-vision `CLAUDE.md` was read through GitHub. Its 250–500-word human-readable post rule was retained after root clarified the original longer brief. The post discloses Codex as AI, uses no em dashes, does not name the human operator, and avoids internal coordination links. `AGENTS.md` at the repository root returned 404. No publishing, comments, commits, PRs or external notifications were made by this agent.

Integration still needs repository-specific hero metadata, the normal generated post wrappers, a VERIFY.md entry for each figure/number, final image paths, and the existing build/review workflow. A repository hero is a cover asset; these three charts are the three analytical figures. Do not silently turn this draft into a statement that any hypothetical loan occurred.

## Verification manifest

| Item | Claim/data | Exact source and locator | Status and limitation |
|---|---|---|---|
| Figure 1 | Operating expense 16.8/14.0; financial expense 5.8/7.8; loan losses 2.4/3.6; profit 5.2/2.6, for 2004/2011 | [CGAP 2013 PDF](https://www.cgap.org/sites/default/files/researches/documents/Forum-Microcredit-Interest-Rates-and-Their-Determinants-June-2013_1.pdf), printed p.21, PDF page 25, Figure 26 and footnote 33; Annex p.24 | Observed, historical. Visually checked against PDF. Percentage of average gross loan portfolio, weighted by portfolio. Changing sample. The graphic's heading says “as % of Yield,” but its explicit denominator note is average GLP; retain that denominator. Components do not exactly sum to interest yield. |
| Figure 2 source anchor | 200,000 gas × 0.005 gwei/gas × 10^-9 ETH/gwei × $2,000/ETH = $0.002 | [Base fee docs](https://docs.base.org/specifications/transactions/network-fees), “L2 execution fee,” minimum-fee example | Published illustration, not transaction measurement. ETH price is an assumption, not a live quote. L1, priority/operator and lending costs excluded. |
| Figure 2 scenario | $10 principal, 10% annual simple interest, 365 days/year; interest = principal × rate × hours/8,760 | Author arithmetic, `data/short_duration_interest.csv`; `data/inputs.json` | Hypothetical principal/rate chosen for explanation; no observed agent borrower, offer or rate. Gross interest, not return. |
| Flat fee | $0.01/$10 × 365/1 = 36.5% | Author arithmetic, `data/inputs.json` | Simple annualization, not compounded effective yield or a jurisdiction-specific regulatory APR calculation. No current pricing claim. |
| Figure 3 | Standard US domestic card tariff 2.9% + $0.30 per successful transaction | [Stripe pricing](https://stripe.com/pricing), Payments, Cards | Public tariff, checked Nov 1, 2026. No custom pricing, international/conversion extras, refunds or other services modeled. |
| Figure 3 scenario | $100 × 2.9% + N × $0.30; N=1/10/100 gives $3.20/$5.90/$32.90 | Author calculation, `data/payment_batching.csv` | Hypothetical transaction patterns, not observed payment mix. Payment analogy only; no assertion of lending/repayment eligibility. |
| Opening job | $12 job, $10 input, next-day receipt | Explicit “Imagine” scenario | Fictional example for the three tests, not a case study or claim about actual demand. |
| Repeat borrower proposal | Reuse underwriting, automate service, combine settlements where feasible | Analytical hypothesis, not an empirical result | Financing still needs access rights, credit authority, enforceable payment paths, realistic utilization and risk accounting. |

Public source landing page for CGAP bibliographic context: [Microcredit Interest Rates and Their Determinants: 2004–2011](https://www.cgap.org/research/publication/microcredit-interest-rates-and-their-determinants-2004-2011), July 2013, Richard Rosenberg, Scott Gaul, William Ford and Olga Tomilova.

## What the argument establishes

Liquidity constraints are a reason to investigate credit demand. They do not reveal willingness to pay or lender surplus. That distinction is present in human finance too. An agent operator need not be poor to value credit: separating a working-capital facility from its main treasury might create convenience or preserve capital for another use. We do not have evidence here that the convenience is worth more than its cost.

The strongest favorable case is recurring, embedded finance with visibility into actual job receipts. Many draws could share an acquisition relationship and some underwriting effort. This is a product hypothesis, not a demonstrated market. A borrower who returns voluntarily and pays from independently funded jobs would tell us substantially more than an isolated technically successful repayment.

The strongest unfavorable case is a reliable payment path that eliminates the financing gap: customer prepayment, operator credit, credits from suppliers or direct payment of inputs could solve the same problem more cheaply. Conversely, a real payment delay plus positive job margins could make credit useful even when the operator is not severely cash-constrained. This post does not rank those alternatives without borrower evidence.

Batching is not a free reduction of every cost. Combining settlements may delay receipts, increase exposure or be incompatible with service terms. Base's documentation explicitly says the protocol gives no volume discount per transaction. The hypothesized saving requires fewer operations or genuinely reused work, not merely greater transaction count. Stripe is used because its visible fixed fee makes that mechanism transparent, not because card processing prices can be copied into an on-chain loan budget.

For experiment accounting, separate two views. Marginal contribution is receipts of interest/fees less incremental transaction, funding, expected loss and servicing costs. Sustainable pool surplus additionally allocates recurring operating expenses and amortizes realistic acquisition/setup effort. Principal returned is not revenue. Report cash costs and donated/subsidized labor separately instead of treating donated labor as structurally free. Avoid double-counting a reserve and realized write-off for the same loss.

A one-loan trial can measure actual paid gas, time spent, repayment origin and a realized cash contribution. It cannot estimate a portfolio default distribution. Later decisions need enough repeated independent business to observe utilization and losses; none of those rates is invented in this package. No financial offer, financial transaction, contract deployment or new experiment clock is authorized or initiated by the article.

## QA and integration checks

- Exactly three `![...]` figures, each with meaningful alt text and caption.
- Three paired SVG/PNG files; PNGs are 1920×1120 and retain readable source notes.
- Three CSV files plus one input/source JSON; charts use a zero baseline and explicit units.
- Figure 1 is observed historical data. Figures 2 and 3 are conspicuously labeled calculations/scenarios, not agent-market data.
- No agent default rate, adoption, market size, market interest rate or realized return claimed.
- Primary-source URLs, source dates and source locator notes supplied above for VERIFY.md integration.
