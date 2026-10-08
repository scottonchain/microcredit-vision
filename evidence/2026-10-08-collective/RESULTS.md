# Results: illustrative community working-capital collective

**These outcomes are conditional simulations, not observed customer sales or poverty reduction.** All dollars below are aggregate across the collective over 26 working weeks plus settlement runoff. Six hundred matched seeds × eight scenarios × five alternatives = 24,000 histories. Each begins with four specialists and $80. No newcomers bring money or customers.

## Baseline medians

| Alternative | Outside receipts | Human cash income | Human net after $12/hour opportunity cost | Total economic surplus including retained capital | Ending cash | Members |
|---|---:|---:|---:|---:|---:|---:|
| Solo, outsourcing allowed | $866.25 | $423.08 | $210.71 | $334.25 | $206.59 | 4 |
| Cooperation, separate wallets | $2,144.17 | $1,454.87 | $484.67 | $744.89 | $341.45 | 5 |
| Cooperation, pooled member loans | $2,582.09 | $1,770.28 | $574.34 | $878.35 | $388.14 | 5 |
| Cooperation, customer mobilization payment | $2,595.82 | $1,745.55 | $566.40 | $914.25 | $429.30 | 5 |
| Cooperation, direct treasury finance | $2,582.09 | $1,770.28 | $574.34 | $878.35 | $388.14 | 5 |

The loan and direct-treasury results are equal in **every seed**, not just at the median. Internal debt labels cannot manufacture aggregate income. Customer prepayment also shifts default risk to the buyer and therefore is not a pure liquidity comparison.

The stronger matched comparison is pooled capital versus cooperation with separate wallets: median **paired additional total surplus is $128.09**, with a 10th–90th percentile range of **$52.75–$234.61**; 97.17% of runs improve. Net cash income above the labor outside option improves by a paired median **$80.85**, not the difference between the two marginal medians. These are assumption-dependent scenario distributions, not confidence intervals.

## Uncertainty and admission

Pooled-loan total surplus has p10/median/p90 **$728.43 / $878.35 / $1,034.15**. Net cash income above labor opportunity cost is **$488.43 / $574.34 / $658.20**; ending treasury cash is **$304.62 / $388.14 / $462.14**.

One cash-poor member joins in **94.5%** of baseline runs. The model stops growing at five because the next skill bottleneck binds; this is bounded inclusion, not an indefinitely scalable network. Across all seeds (including no-admission runs), entrant median cash receipts are **$253.56**, of which **$73.80** is above the assumed labor outside option. Entrant net-income p10–p90 is **$23.49–$103.08**. Work assignment deliberately favors people with fewer lifetime hours. These six-month amounts are too small to establish poverty escape.

With admissions disabled, pooled financing still produces median total surplus **$791.44**, compared with **$334.25** for solo operation. Thus modeled complementarity does not depend on recruiting a fifth member. Compared with its matched no-admission run, admitting a member adds median total surplus **$88.71** and improves total surplus in **88.17%** of runs.

## The loan book cannot stand on fees alone

A 1% loan fee is insufficient for the modeled loss rate: fee income minus defaulted principal is median **−$40.80**, negative in **81%** of baseline runs. The cooperative treasury grows because it retains 40% of production surplus. That cross-subsidy is explicit. Offering outside lenders a sustainable yield based on fee income would be unsupported. Loan principal and interest are internal transfers; defaulted advances are not deducted a second time from consolidated profit.

## Pooled-finance stress results

| Scenario | Median total surplus | Median end cash | Capital impairment rate | Cash under $16 | Median members |
|---|---:|---:|---:|---:|---:|
| zero_demand | $0.00 | $80.00 | 0.00% | 0.00% | 4 |
| adverse | $524.86 | $176.19 | 17.00% | 1.17% | 5 |
| low_margin | $127.14 | $105.71 | 18.67% | 0.17% | 5 |
| withdrawal | $871.75 | $346.84 | 0.67% | 0.67% | 5 |
| fixed_low_demand | $494.72 | $267.48 | 0.00% | 0.00% | 4 |
| fixed_members | $791.44 | $372.27 | 0.00% | 0.00% | 4 |
| overhead_4 | $750.78 | $280.71 | 2.17% | 1.50% | 5 |

Zero demand creates no income or growth; its $80 stays intact only because that scenario has no standing overhead. The separate `overhead_4` case pays $4 weekly ($104 total when affordable) and reduces pooled median ending cash to $280.71. These are prepaid operating services: when cash cannot buy them, work is suspended and the field `unpaid_overhead` records an unmet required budget, not an accrued creditor liability. Any such shortfall means continuous operation failed; this occurs in **1.33%** of pooled-overhead runs. Tail outcomes with shortfalls must not be presented as fully funded continuing businesses. This is one assumed overhead stress, not a claim to have measured all subscription, acquisition, revision, administration or household costs. The admission rule uses observed volume and cash rather than a complete long-run commercial forecast, another reason not to infer real viability from admission alone.

## Meaning for a real pilot

The result supports a narrow hypothesis: complementary services plus shared, loss-bearing working capital can help a cooperative fulfill assumed outside orders and include a cash-poor contributor. It does **not** establish that loans outperform direct cooperative spending or acceptable customer deposits. It does not prove a funded customer exists. A real pilot must first obtain a customer order, permission to use the data, an advance-funded cost actually required to deliver, a measurable acceptance criterion, and receipts tracing customer payment to wages, principal repayment, and retained losses.

At the assumed $52 bundle price, mean modeled upfront costs are $28.57 and the successful-job platform fee is $5.20; successful contribution before patronage is $18.23. At a conservative 6% failure expectation, expected contribution is $15.42 before unmodeled fixed costs. The corresponding modeled break-even price is approximately **$33.77** ($28.57 / (0.94 × 0.90)); actual procurement terms and costs could erase that margin. Cheap transcription alone does not justify a loan: the assumed financing gap mostly pays two human hours before customer acceptance.

## Verification

Every run checks consolidated cash conservation after each financial event, nonnegative balances, capacity limits, zero ending outstanding advances after runoff, and exact direct-finance/loan aggregate equivalence. Maximum cash-accounting discrepancy is below **$3.6×10⁻¹²**. A separate review agent independently recomputed the accounting from the CSV and reproduced selected runs. These tests validate implementation of the assumptions; they do not validate the assumptions themselves.

See `MODEL.md` for definitions and limitations, `results/headline.json` for compact machine-readable statistics, and regenerate `results/runs.csv` using `python simulate.py --seeds 600`.
