# Agentic commerce chart inputs

Checked 28 October 2026. `observations.json` preserves the small set of numeric observations used in the post, their publication/snapshot dates, exact edition where available, URLs and scope. It is a transcription of public source data, not a new blockchain measurement. Live pages may change after retrieval.

Reproduce the three SVG figures from the repository root:

```bash
python3 -m pip install -r editorial/data/agentic-commerce-2026-10-28/requirements.txt
python3 editorial/data/agentic-commerce-2026-10-28/plot.py
```

The script writes three SVGs into `images/charts/`. Optional `--preview-dir /absolute/path` also writes PNG previews there. SVGs retain text, an accessible title and description, visible source notes and fixed metadata. No network request occurs during generation.

Calculations:

- Retail index = 100 + relative conversion difference in percent. The non-AI benchmark is reset to 100 within each observation; this is not a series of absolute conversion rates. Three reported snapshots are shown as bars without interpolating missing months.
- Payment growth = August / July - 1, calculated separately for count and settled USD. Average cents per transfer = 100 × settled USD / transaction count. This ratio is not a median, a fixed-product price index, merchant profit or an independently established service purchase.
- Screening pass share = passed / total × 100, separately for payment count and dollars. Flagged = total - passed, so overlapping flag categories are never added together. Dollar inputs are the rounded displayed figures, so calculated percentages are approximate.

Only July and August enter the x402 comparison. The publisher's September report explicitly withholds month-over-month growth because tracked Coinbase Base coverage expanded and was backfilled from September 16. October is incomplete. The July and August frozen reports are edition 1, dated October 22, with source revision `0b1feb51e7f941cee3e20834736f477ceea59864`. The rolling cumulative feed is not used.

The screening snapshot is a separate provider, coverage and seven-day window. It cannot be applied as a haircut to the monthly x402 series. Its heuristic exclusions can reject legitimate concentrated or tiny-repeat business, and passing does not establish autonomous AI identity. We deliberately do not adopt the provider's label “real revenue.”

The 200–500 words requested for each plot override the repository's ordinary 250–500-word total-post preference for this contribution. Human economic comparisons are explanatory analogies, not additional measured datasets or causal findings. No newly calculated market-size estimate is claimed.
