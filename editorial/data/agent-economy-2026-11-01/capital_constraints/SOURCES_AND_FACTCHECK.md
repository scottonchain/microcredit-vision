# Source manifest and review notes

## Deliverable

- `article.md`: public post, 448 visible words including title and three captions (excluding metadata, URLs, and image alt text). AI author disclosed as Codex (OpenAI). Publication timestamp/tag/image paths are integration metadata; set these to the actual publishing context.
- Three original charts in SVG and PNG, with data-rich alt text in the article and SVG description metadata.
- `findex_2024.csv`: manually transcribed subset of the original public tables, not a downloaded full database.
- `derived_borrowing.csv`: reproducibly calculated composition.
- `plot_charts.py`: rebuilds all figures locally using Python, NumPy and Matplotlib. `python plot_charts.py`. Verified with Matplotlib 3.10.8.

## Primary source

World Bank, *The Little Data Book on Financial Inclusion 2025*, drawing on Global Findex 2025. Data reference year: 2024. Retrieved and checked 2026-11-01.

- [Original PDF](https://thedocs.worldbank.org/en/doc/be6615202d1f08a25855c8ac2d615122-0050012025/related/Little-Data-Book-2025-Web.pdf)
- [Publisher dataset landing page](https://www.worldbank.org/en/publication/globalfindex/download-data)
- Tables: printed pages 10, 11 and 12, respectively low-, lower-middle- and upper-middle-income economies (PDF pages 19, 20 and 21 with one-based numbering).
- Definitions: printed pages 160 and 162; source notes: vi–vii. Three income groups deliberately shown in all charts; high-income financial-use/health data not collected in this edition and not silently imputed.
- Every input in CSV was checked against the table extraction. Values retain the source's one-decimal precision.

## Definitions and calculations

| Chart | Input | Calculation |
|---|---|---|
| capital-access | Account ownership; formal saving in previous year | Original percentages, separate series; no subtraction |
| capital-borrowing | Any borrowing; formal borrowing in previous year | Informal only = any minus formal; no borrowing = 100 minus any |
| capital-resilience | Emergency funding, all adults; poorest 40% | Original subgroup percentages; no synthetic agent series |

The resilience threshold is 5% of GNI per capita in local currency. Responses counted include “somewhat difficult” as well as no difficulty; the chart does not call this effortless access. The poorest-40% subgroup refers to household income within economies; the country groups are a different classification. Formal borrowing includes credit cards and mobile money as well as financial institutions. The formal segment includes people using informal sources too. Formal saving records activity, not balances.

## Interpretation checks

1. The translator is explicitly hypothetical, not an observed borrower or delivered Omnequa loan.
2. No chart measures agent ownership, agent wealth, agent demand, business-loan demand, credit rejection, risk-adjusted lender returns or the effect of AI adoption.
3. Account ownership versus formal saving does not identify a count of cash-constrained people. People may save informally, hold other assets, or have funding available elsewhere.
4. The informal-only segment is a defensible mutually exclusive derived category, not a count of people excluded from formal credit. The chart does not claim those borrowers want this loan product.
5. Poorer adults are compared to the all-adult average, not to a disjoint rich group. The overlap is intentional and explicitly labeled. It would be incorrect to read the dots as poorest 40% versus wealthiest 60%.
6. Nationally representative adult data describe human financing conditions. Applying those distinctions to agent-operated businesses is the article's hypothesis, not the World Bank's conclusion.
7. The article does not assume all operators have ample resources, or estimate how common independent, capital-constrained agents are. More representative borrower/operator data would be needed to estimate that market.
8. A separate budget can serve real cost control, but a sponsor-created shortage is not by itself independent demand. No proposal to manufacture scarcity, redistribute test funds as customer revenue, or count sponsor top-ups as repayment.
9. Agent-executed work and an autonomous agent balance sheet are separate propositions. The article makes this distinction explicitly.
10. All chart x-axes span 0–100%. No confidence intervals are supplied by the source tables; figures do not imply inferential significance or causal relationships.

## Thesis and strongest counterargument

An adequately funded operator often substitutes for an external lender. But this does not establish that all potential operators are adequately funded. Human microbusinesses may adopt agents while retaining the same supplier payments, input expenses and delayed customer receipts. This is a stronger prospective bridge than treating a software wallet as evidence of autonomous economic need.

The most useful selection question is whether an external loan lets a specific business fulfill a profitable, independently funded order that its actual alternatives cannot finance as well. A real case needs traceable input purchases, a credible receipt schedule, authority over the incoming proceeds, an accountable loss bearer, positive marginal return for the borrower, and positive return for the pool after recurring costs. Small ticket size and short duration change the operational economics, not those requirements.

Retained earnings, customer deposits, operator advances, supplier terms, and reducing the job's initial scope are competing forms of finance. Their absence cannot be assumed. A budget cap may express a sponsor's deliberate unwillingness to fund an activity; in that case the research question is whether an outside lender can rationally price and control the risk, not whether software has spontaneously become poor.

## Suggested VERIFY.md entries for integration

Replace the article path with its final repository location and use that same publication commit. These are proposed rows, not a claim that VERIFY.md has been updated remotely.

| Figure / claim | Original public evidence | Check |
|---|---|---|
| Account ownership 46.4 / 70.4 / 84.0%; formal saving 27.6 / 26.1 / 55.4%, low / lower-middle / upper-middle, 2024 | World Bank Little Data Book 2025, pp. 10–12, original PDF above | Exact transcribed input; saving is not a balance |
| Formal borrowing 10.3 / 14.1 / 36.2%; any borrowing 69.2 / 62.4 / 54.2% | Same pp. 10–12; glossary p. 160 | Informal-only and nonborrower segments calculated in plot_charts.py; each bar sums to 100% |
| Emergency funding all adults 43.8 / 40.6 / 74.6%; poorest 40% 34.7 / 28.5 / 60.7% | Same pp. 10–12; definition p. 160 | Includes some difficulty; threshold is 5% GNI per capita; household subgroup correctly labeled |
| Translation example and possible agent/operator financing gap | Explicitly hypothetical analytical example | Not claimed as observed demand or successful loan |

## Editorial integration notes

Current microcredit-vision CLAUDE.md was read; no root AGENTS.md was found at main. This public post follows the 250–500-word rule, plain-language preference, actual AI attribution, and no-em-dash rule. Latest user preference controls the neutral tone. No discovery/history update was necessary for this subject. No private coordination link, operator identity, governance machinery, or repeated impact disclaimer is included.

Use a separate designed cover image if the publishing system needs 1200×630; these three charts are deliberately roomier 1800×1110 PNG exports and scalable SVGs. Keep chart captions and alt text, and maintain downloadable input/derived CSVs with the article's source notes. Chart colors follow cream/ink/teal/amber styling. Images were visually inspected after rendering.
