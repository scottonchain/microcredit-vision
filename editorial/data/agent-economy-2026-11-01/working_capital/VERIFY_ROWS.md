# Verification rows for integration

Attach these to the final article/asset commit in the repository's preferred ledger format. Final publication revision must be supplied by the integrating editor; no revision is invented here.

| Asset or assertion | Public source and exact locator | Source edition or revision | Verification and transformation |
|---|---|---|---|
| `working-capital-payment-terms.svg/png` | [Federal Reserve report](https://www.fedsmallbusiness.org/-/media/project/clevelandfedtenant/fsbsite/reports/2024/2024-report-on-payments_sbcs.pdf), printed p. 1 / PDF p. 6 | Published 2024-12-05; SHA256 `e3dccc9a9387eb40beec378e7100df495d5508f4728f6e6adc73b3839f919924` | Values visually verified against PDF; direct percentages, shorter labels. CSV: `payment_terms.csv`. |
| `working-capital-two-clocks.svg/png` | [Federal Reserve report](https://www.fedsmallbusiness.org/-/media/project/clevelandfedtenant/fsbsite/reports/2024/2024-report-on-payments_sbcs.pdf), printed p. 6 / PDF p. 11 | Same report edition and hash | Two challenge series visually verified against PDF; direct percentages and group sample counts. CSV: `payment_challenges.csv`. |
| `working-capital-digital-receivables.svg/png` | [Microsoft 2026 annual report](https://www.microsoft.com/investor/reports/ar26/index.html), consolidated statements of cash flows, accounts-receivable row | FY2026 report, three-year comparative statement; retrieved 2026-11-01 | Published negative USD millions multiplied by −1 and divided by 1,000; labels rounded to one decimal. CSV: `microsoft_receivables.csv`. |
| x402 verification is not necessarily upfront usable funds | [README, Typical x402 flow](https://github.com/x402-foundation/x402/blob/f3cb4bb79a708bf5669f952d09fa404370263c76/README.md#typical-x402-flow), steps 5–10 and flexibility qualification | Commit `f3cb4bb79a708bf5669f952d09fa404370263c76` | Pinned source fetched and matched inspected content; stated as implementation-dependent possibility. |

No charts claim measured agent borrowing demand. All source retrieval and visual checks completed 2026-11-01 by Codex.
