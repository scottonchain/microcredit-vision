# Working-capital article: research and editorial notes

Prepared 2026-11-01 by Codex. This is an editorial support file, not the published article.

## Argument and limits

The article attacks a categorical claim, not the observed difficulty of recruiting a borrower. A business can have a funding gap whenever unavoidable input payments precede usable customer receipts. That mechanism is compatible with both human and automated production. It does not establish the frequency of gaps among agents, willingness to borrow, creditworthiness, or lender profitability.

The opening contractor/agent comparison is explicitly hypothetical. Concurrency, paid data and compute are proposed sources of a gap, not documented borrowers or a measured market. No agent cash-cycle distribution is inferred. No demand result or experiment state is asserted.

The rival explanations deserve real tests: the operator can contribute cash; the customer can advance funds; the supplier can invoice later; the agent can take fewer simultaneous jobs; the paid task is not sufficiently profitable to service credit; or the apparent budget shortage is an internal spending limit that a loan is not authorized to bypass. The existence of a receivable is insufficient evidence that external credit is useful.

A useful interview should trace one independent customer's payment obligation, the exact input bill, when each becomes payable or usable, and which alternatives the operator can actually access. It should ask who bears nonpayment, who owns job proceeds, and why a loan is preferable. A wallet balance alone cannot answer those questions.

## Chart methodology

All three charts are redrawn from source values in the adjacent CSVs. They are observational financial/payment data, not simulations. Chart 3 reverses the sign and changes units solely to display a negative cash-flow adjustment as a positive magnitude. No estimated time series or agent extrapolation is included.

The Federal Reserve survey is a weighted convenience sample of US employer firms, not a probability sample. Reported percentages describe firms and self-reported challenges, not the dollar value or count of payments. Arrangement categories describe the largest revenue share. The challenge comparison is descriptive, not causal; its two challenges can overlap. Advance-payment businesses are omitted from the source's selected comparison and are not added here.

The Microsoft series is a consolidated accounting adjustment. It is not accounts-receivable balance, financing cost, days sales outstanding, default rate, or a claim of financial distress. Microsoft also sells hardware and other offerings; the prose treats it as a technology-company illustration rather than a pure agent economy. The chart cannot establish how much outside financing the company needed.

## Protocol caution

x402's README documents a typical sequence with verification, fulfillment, then settlement, while explicitly permitting other flows. The article therefore says verification *can* precede work and settlement follow it. It does not claim all implementations do this, or that an authorization guarantees final payment. It does not treat a blockchain settlement benchmark as the time until a business customer approves a bill.

## Reproduction and review

Run `python3 plot_charts.py` with Python 3, matplotlib and numpy installed. Tested with matplotlib 3.10.8. The script reads local CSVs and writes three SVG/PNG pairs without network access. SVG text remains text. PNGs are 1920 by 1120 pixels; source labels and chart axes are embedded.

Values in the two survey charts were checked against rendered original pages 1 and 6, not solely PDF text extraction. The three financial values were checked against the annual report's consolidated cash-flow statement. Images were visually inspected after rendering; a legend/footer collision was corrected. Article length is 445 words under the repository's link-stripping counting method, including alt text and captions. No em dash is present.

The article metadata date is a drafting placeholder. The integrating editor should set its actual permitted publication time, update image paths to the repository layout, provide a 1200 by 630 hero in the established visual system, and add the accompanying verification rows at the same revision as the figures. Do not copy the downloaded source PDF or rendered source pages into the public post assets. No source organization is represented as a partner or prospective borrower.

## Files

- `article.md`: short public draft with captions, public links and image alt text.
- `charts/`: three SVG and PNG pairs.
- Three adjacent CSVs: directly transcribed numeric source values.
- `sources.json`: source editions, page/section locators, retrieval date and transformation notes.
- `VERIFY_ROWS.md`: rows for the integrating repository's verification ledger.
- `plot_charts.py`: reproducible chart generation.

Sources were retrieved on 2026-11-01. The 2024 survey publication is intentionally historical. No later survey is implied. The x402 source is pinned to a verified commit, and the fixed-edition annual report and survey PDF are linked in the manifest.
