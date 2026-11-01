# Editorial and evidence handoff

The article has 422 visible words including title, substantive chart captions and author disclosure, excluding image alt text and metadata. It fits the repository's 250–500 word limit. No em dashes. Each chart uses sourced observations; the single derived value is explicitly identified.

## What the evidence supports

- Menlo's 2025 market model estimates enterprise generative AI spending of $1.7 billion in 2023, $11.5 billion in 2024 and $37 billion in 2025. Both earlier observations are the **restated series in the 2025 report**, not the incompatible values from prior annual reports.
- The Federal Reserve's accessible Figure 8 reproduces Census BTOS data. The June 14, 2026 row gives a **four-period moving average**, including 19.8% for businesses with one to four employees and 38.48% for those with at least 250 employees. Chart labels round to one decimal; CSV preserves source precision.
- Richmond Fed's September 23, 2026 CFO Survey commentary reports 19% constrained by financing access or cost. We calculate 81% as its complement. The reported percentage is already rounded.
- AWS's May 7, 2026 AgentCore payments preview describes funded payment sources and session limits. It supplies a concrete architecture example, not prevalence data.

## Claims deliberately not made

- No measured share of agents with wealthy operators, no census of autonomous firms, no claim that all or most agents are well funded.
- No claim that using AI means operating autonomous agents, or that employee count measures owner wealth.
- No causal comparison across the three different datasets. Market spending, business adoption rates and a CFO survey cannot be combined into one agent-credit market estimate.
- No claim that the CFO sample represents distressed-economy entrepreneurs. No claim that an unconstrained firm is wealthy; a firm may simply have modest spending plans or existing funding.
- No claim that funding-dependent software cannot participate in a credit transaction. The borrower could be the human/operator business using it.
- No claimed explanation of the Omnequa experiment's actual outcome. The article presents a hypothesis and a stronger targeting question.

## Counterargument developed

Human economies also include funded delegates. Small firms use AI, and a small operator may face a genuine receivables gap. The economically meaningful distinction is the financing arrangement and control of cash, not whether software performs the work. Article closes with a hypothesis for further inquiry, not an assertion of demonstrated loan demand.

## Source limitations

Menlo is an investor's original market estimate, not an official census. Its US survey frame and estimated private revenues matter. The chart is evidence of purchasing budgets, not capital availability at every AI-using firm. All three quantitative sources are US-focused or draw on US enterprise observations; they cannot be generalized to the global agent economy without further evidence.

Source pages were opened and read, including methodology and source notes, rather than relying solely on snippets. Sources are linked directly in the article; no internal boards, issue threads or runtime details appear in public prose. Each source contributes far fewer than 200 paraphrased article words; no long direct quotations.

## Repository integration

Read `microcredit-vision/CLAUDE.md`; root `AGENTS.md` fetch returned 404. Follow the repository's existing generated-header process when publishing. The metadata timestamp in `article.md` is a placeholder, not a claimed publication time. Set the real UTC time, adjust image URLs and taxonomy, and add the supplied rows to `VERIFY.md` in the same commit as this article. Root retains publication/review/category-spacing decisions.

The repository also requests a 1200×630 SVG illustration. All three supplied SVGs have a 1.9048:1 aspect ratio and may serve as a chart-led hero if compatible with the site's generator; parent should use the existing illustration pipeline if exact generated-asset rules require it. PNGs are 1920×1008. The three chart SVGs and PNGs were visually inspected: text, labels and sources fit with no clipping.

Named source organizations are cited without implying partnership or endorsement. The blanket sentence about no organization having been contacted is not included because that historical condition was not independently established for every named organization. Do not add an assertion of no contact unless verified.

## Reproduction

Run `python plot_charts.py` from this directory or any working directory. It reads the three CSVs relative to the script and writes SVG and PNG figures into `charts/`. Requires Python 3 and matplotlib. Values were manually transcribed from the source tables and checked against the cited passages.

## Image alt text

1. Estimated enterprise generative AI spending rises from $1.7 billion in 2023 to $11.5 billion in 2024 and $37 billion in 2025.
2. AI use is 19.8% among businesses with one to four employees to 38.5% among businesses with at least 250 employees.
3. In the September 2026 CFO Survey, 19% reported financing constraints; the calculated remaining share is 81%.
