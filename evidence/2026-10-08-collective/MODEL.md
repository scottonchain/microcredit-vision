# An agent collective as a community finance cooperative

This is an illustrative agent-based cash-flow experiment, not an estimate of an existing business, a funded customer order, or evidence that poverty has been reduced. Four specialists jointly serve **outside customers** with transcript/source retrieval, data cleaning, quality checks, and locally informed delivery. The motivating observation is tool complementarity: one agent can retrieve a source another cannot, while another can execute an authorized GitHub change. Tool access is represented by different capabilities, not by an assumed productivity multiplier.

## Reproduce

Run `python simulate.py --seeds 600` with Python 3.10+; no external packages or network access are needed. The output contains every run in `results/runs.csv` and quantiles plus paired differences in `results/summary.json`. Seeds 0–599 are reused across all alternatives. Jobs, prices, payment outcomes and delays are generated before policy acts. Twenty-six weeks of new work are followed by a settlement-only runoff of up to three weeks.

The model has fixed decision rules, rather than live LLMs role-playing customers. Separate research and review agents specified and challenged its assumptions and audited its accounting.

## Assumed job and institution parameters

| Input | Model value | Status |
|---|---:|---|
| Initial collective resources | $80 total; four original members | Illustrative, identical total in every arm |
| Specialized roles | Retrieval, build/delivery, review, local context | Motivated by observed team complementarity; simplified representation |
| Working time capacity | Four skill units per member per week | Assumed; not a performance measurement |
| Integrated package | $52 ±15% customer price | Assumed, **not a customer quote** |
| Package human work | 0.4 +0.3 +0.6 +0.7 = 2 hours | Assumed |
| Human compensation and opportunity cost | $12/hour, paid upfront | Assumed; no measured local wage or poverty threshold |
| Package tools/access/connectivity | Mean $2.17 ±10% | $0.17/hour transcription-plus-diarization is a source-motivated example; $2 other costs assumed |
| Package coordination | $2.40 | Assumed external expense |
| Package total upfront cost | Mean $28.57 | $24 is worker pay; small API costs do not establish credit need by themselves |
| Customer platform charge | 10% of collected full job price | Assumed |
| Single-specialty job | $11 ±15%; 0.25 labor hours; $0.80 tools; $0.40 solo/$0.50 team coordination | Assumed |
| Outside subcontractors for solo work | Missing role's labor cost +$6 per missing role | Assumed retail premium; solo agents are not forbidden to buy missing skills |
| Package arrivals | Poisson mean 1.4/week initially to 2.9/week in week 26; capped at seven | Assumed exogenous booked opportunity stream; does not rise with membership |
| Single-specialty arrivals | Independent 70% chance per skill/week | Assumed |
| Payment delay | One week 75%; two weeks 25% | Assumed |
| Failure | 2.5% in ordinary weeks; 25% in common bad weeks, which occur 6% of weeks | Assumed; common weekly state creates correlated risk |
| Underwriting | Expected receipt must exceed modeled costs by $0.50 | Uses conservative 6% expected failure probability; does not peek at outcomes |
| Liquidity/exposure controls | $12 aggregate cash reserve, job advance ≤60% of cash plus outstanding advances, one outstanding financed job per lead | Applied in every comparison arm |
| Patronage | 60% of positive job surplus paid to humans; 40% retained | Assumed democratic cooperative policy |
| Member-loan fee | 1% of advance, carved from retained surplus | Internal transfer; **not** extra consolidated income |
| New-member onboarding | $6 external fee +1.5 paid training hours = $24 | Assumed; entrant brings no savings or new customers |

The package consumes retrieval/build/review/local skill capacity of 1/0.75/1/2 units. This makes the initial local specialist a two-package-per-week bottleneck. A second local member can increase feasible work to four packages, at which point the next bottleneck is retrieval/review. The present code can therefore grow **from four to five members only**. It does not model indefinite scaling.

All accounting is in illustrative US dollars. No blockchain transactions occur. Testnet Sepolia currency cannot pay modeled outside costs and is never revenue or economic backing.

## Alternatives

1. **Solo:** Four separate $20 wallets. A specialist may buy missing capabilities from outside suppliers at the stated retail premium. This is a modeled outside option, not an empirically measured best available subcontracting market. Recruitment is not available to independent businesses; the `fixed_members` scenario removes recruitment from every other arm for a cleaner capability comparison.
2. **Cooperation, separate wallets:** Same capabilities and $80, retained in separate wallets. Members can share capabilities and customer proceeds; an identified lead must personally fund the job's advance. They can voluntarily contribute to onboarding but do not make working-capital loans.
3. **Pooled member loans:** Members contribute their $80 to a loss-bearing cooperative treasury. A named lead borrows the actual upfront cost, pays suppliers and human workers, and assigns receipts to principal repayment before patronage. Losses are mutualized. These are equity-backed internal advances, **not insured deposits**.
4. **Customer prepayment:** Same separate wallets and cooperative operations. Customers pay a nonrefundable mobilization amount of up to 50% of price, capped at 95% of upfront costs; the rest is due on success. This funds initial work and reduces the collective's loss exposure. It is consequently a combined liquidity-and-risk-allocation alternative, not a pure timing experiment. The contract is a hypothetical commercial term, not evidence customers accept it.
5. **Direct treasury financing:** Same shared capital, expenses, distributions and risk controls as pooled loans, but the cooperative pays job expenses directly. Its aggregate cash, income, revenue and admissions are exactly identical to the loan arm for every seed. Credit is one governance/accountability design, not a source of additional aggregate money.

Financing policy is matched across arms: reserve, exposure, and outstanding-job limits are the same. Cash fragmentation, capability access, ownership of advances and payment terms are the modeled differences. Role assignments favor members with fewer lifetime paid hours, so entrants receive a deliberate opportunity to catch up. This work-sharing rule is a governance choice, not an observed labor-market result.

## Admission and democratic control

Each member has one vote; the model implements a pre-agreed admission rule rather than simulating political persuasion. Every other week after week six, incumbents accept one cash-poor local-context member only when the prior six weeks' outside package demand exceeds current local capacity by 10%, other capabilities can use the additional capacity, and free cash covers onboarding plus $72 of working-capital/reserve buffer. No share-purchase fee, unpaid trial, operator deposit or personal collateral is required. Paid training is real modeled human income, with an equal opportunity-cost charge. Demand is never created by admitting members.

A real cooperative would also require informed consent, withdrawal rules, contestable quality judgments, data permissions, rules against insider favoritism, and transparent votes. This simulation does not establish those protections or legal suitability.

## Accounting and what the income numbers mean

At every job start, settlement, onboarding and withdrawal, the code asserts:

`ending consolidated cash = $80 + outside customer receipts − nonhuman outside costs − worker pay − human patronage − returned member capital`.

Drawn loan principal, repayment, and internal interest are absent from this identity. An unpaid job has already consumed its outside inputs and paid wages; its principal write-off is reported for the lending subledger but is **not deducted a second time** from consolidated profit.

- **Human cash income:** Actual modeled upfront compensation plus cash patronage.
- **Human net income after opportunity cost:** Human cash income less all labor/training hours ×$12. Because labor is paid at the assumed opportunity cost, this equals patronage mathematically. It does not prove that a real household is better off at those wages.
- **Total surplus after opportunity cost:** Human net income plus change in collective capital, including capital returned. This measures member-owners' joint outcome and captures their capital losses as well as cash income. Retained capital is not treated as immediately spendable household income.
- **Entrant net income:** Entrant patronage above the same labor opportunity cost. It must be reported alongside actual hours, admission rate, and the preferential catch-up work rule.
- **Loan-book income:** Internal fee less principal losses. A growing cooperative treasury may still conceal a loss-making standalone loan book because business surplus replenishes it.
- **Capital impairment:** Ending cash plus returned capital below the initial $80.
- **Liquidity closure proxy:** Ending cash under $16, too little for the reserve plus an approximately $4 simple job. No negative cash is permitted. Therefore absence of literal insolvency is mechanically guaranteed by the no-external-borrowing model and is not evidence of banking safety.

Costs include job-specific tools, human labor, coordination, platform charges, onboarding, and failed-job costs. Separate fixed subscriptions, acquisition effort, lengthy revisions, legal/accounting infrastructure, household participation costs, exchange risk, taxes and sanctions/identity compliance are **not quantified**. Do not describe the simulated margins as empirically fully loaded business margins.

## Stress cases and limits

- `zero_demand`: No customer arrivals. No jobs, earned income or admissions; capital remains $80.
- `adverse`: More frequent shared bad weeks (18%); failure 40% within them/8% otherwise; some three-week settlement delays. Underwriting uses 16% expected risk.
- `low_margin`: Prices are 64% of baseline. The same positive-expected-contribution test rejects unattractive work; low wages are not used to rescue margins.
- `withdrawal`: $40 of available member capital redeemed at week eight. This is a capital return, never earned income or revenue.
- `fixed_low_demand`: Mean 0.55 packages per week throughout. No automatic market expansion as membership grows.
- `fixed_members`: Same baseline demand/outcomes, but no new members can join any arm; isolates cooperation from admission effects.
- `overhead_4`: Baseline with $4 of weekly external standing costs paid proportionally from available cash. These are prepaid operating services: if cash cannot buy them, the required-budget shortfall is recorded in the field `unpaid_overhead`, and no new work starts that week. The shortfall is an unmet service budget, not an accrued creditor payable: no service is consumed, no liability arises, and no arrears are repaid. Any shortfall is a continuous-operation failure. If the real costs are owed regardless of use, this treatment would be inappropriate and creditor liabilities must instead reduce net assets. This probes one possible fixed-cost burden, not all real overhead.

Quantiles describe uncertainty **conditional on chosen assumptions**, not a statistical confidence interval or forecast accuracy. No price elasticity, competition, repeat-purchase response, strategic misconduct, real agent demand or production uptime has been estimated. Broad poverty alleviation would require repeated customer purchases and meaningful, sustained household net income; a five-member six-month toy model cannot establish it.

This is an economic model, not a replica or verification of the deployed lending contract. The illustrative 1% internal fee is not a quotation of the contract's interest terms.
