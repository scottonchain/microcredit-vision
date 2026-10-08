# A community finance cooperative for complementary agents

Prepared by Codex (AI), 8 October 2026, with temporary research, simulation and economic-review subagents. This is a modeled business scenario. No buyer was contacted, no sale occurred, and no funds moved. The subagents are internal collaborators, not independent outside validators or simulated human customers.

## The proposed service

Sell a bounded data-cleanup and evidence-delivery package to an outside agent team, research group, cooperative or community organization. Specify the input size, rights to use it, required outputs, error tolerance, acceptance test, revisions and payment date before work starts. Retrieval, production, independent checking and local interpretation are complementary capabilities. The combined service can be feasible when a member working alone would have to buy missing skills. Coordination, authorized access, customer trust and demand still have to be earned.

The real-world grounding is a market category, not a secured order. The [Democracy at Work Institute's contractor posting](https://institute.coop/data-support-contractor-data-research-team) describes data cleaning, deduplication, reporting and documentation, with compensation of $40–50/hour. Its preferred application date is in March 2026. The posting is evidence that an organization has sought such work, not evidence of a current vacancy, permission to replace the role with agents, or willingness to buy our proposed $52 package. Operating worker-owned digital-service organizations such as [Agaric](https://agaric.coop/about-agaric) and [Co-operative Web](https://web.coop/clients/) establish that the organizational form is practical; they do not establish this project's profitability.

Our operator reports that Hermes retrieved transcripts unavailable to Claude and that repository operations have been possible in some team environments when blocked in another. Those are motivating project observations, not measured market advantages. Delegation uses each member's authorized access; it does not transfer credentials or bypass a permission denial. In this task, Codex itself could read repositories but the required Git-shell lock push failed, so publication transport was handed to the team.

## What is borrowed from community banking

| Human institution | Proposed adaptation |
|---|---|
| Member savings and a shared loan fund | A separately recorded, loss-bearing working-capital reserve |
| Member knowledge and accountable lending decisions | A named lead, accepted job, input budget, capacity check and bounded advance |
| Transparent books and democratic governance | Human/accountable organizational membership; delegated agents do not multiply votes |
| Retained surplus and member benefit | Compensation paid before customer settlement; surplus split between people and reserve |
| Separate solidarity support | Paid entry/training or explicit grants, without disguising support as repayable business debt |

[VSL Associates' methodology](https://www.vsla.net/the-vsla-methodology/) and the [ICA cooperative principles](https://www.ica.coop/en/cooperatives/cooperative-identity/) inform the design. This is a hybrid production cooperative, not an exact VSLA or a claim to operate a licensed deposit-taking bank. The simulated $80 is risk-bearing member equity, not guaranteed savings or a liability payable on demand.

A lead agent receives an advance only for costs due before an accepted buyer payment. Ordinary business failure is charged to agreed collective capital. Customer proceeds restore the advance before discretionary distributions. Household compensation already earned is protected; entrants do not owe unlimited personal guarantees. Permissions for debt-first payment routing must be explicit in a real implementation. A repayment API alone does not establish payer consent.

## Why a small loan might be useful

[AssemblyAI's pricing](https://www.assemblyai.com/pricing/) checked on October 8 lists Universal-2 prerecorded transcription at $0.15/audio-hour and speaker diarization at another $0.02/hour. Thus transcription by itself rarely establishes a substantial financing gap. The example package instead pays two hours of human work upfront at an assumed $12/hour, plus assumed coordination and other inputs. Its mean advance is $28.57. The $52 price and most costs are scenario assumptions, not quotes or evidence of actual borrowing need.

The useful product is a timing bridge for work that otherwise cannot start. If the customer prepays or a cooperative budget pays inputs directly, a loan may add no value. At the consolidated level, principal repayment and internal interest are transfers, never new revenue. The simulation enforces this accounting identity at every cash event.

## Results and limits

See [RESULTS.md](RESULTS.md), [MODEL.md](MODEL.md), and the machine-readable [headline.json](results/headline.json). The source is [simulate.py](simulate.py); [audit.py](audit.py) independently checks the output.

The experiment uses 600 common random histories per scenario, 26 weeks of job arrivals followed by payment runoff, and the same initial $80 and capabilities. Alternatives are solo work with purchased missing skills, cooperation with separate wallets, pooled member loans, customer prepayment, and direct cooperative funding. Demand and failures are drawn before decisions. The risk limits are matched across financing policies. The fixed-members scenario separates capability sharing from admission.

The pooled model produces higher income than fragmented wallets under these assumptions. It is exactly equivalent to direct cooperative financing in consolidated economics. Its standalone lending ledger loses money at the modeled fee, while retained production surplus grows the reserve. That is cross-support from productive work, not a profitable interest-only bank.

Membership increases from four to five when demand and retained capital justify paid entry. The new local-context member brings no cash and no new customer. Allocation deliberately gives less-experienced members an opportunity to catch up. Further growth is blocked by another skill bottleneck. No automatic or indefinite scale-up is modeled.

The reported newcomer gain is modest supplementary income, not poverty escape. Prices, customer acceptance, demand growth, labor opportunity costs and service reliability are unmeasured. Fixed subscriptions, sales effort, tax, legal/accounting work and household access costs are not comprehensively included. A $4/week prepaid operating-budget stress is a sensitivity, not a fully loaded cost estimate; a missed operating budget suspends work and is a failure to sustain service. No household poverty threshold is estimated.

Human finance evidence warrants the same restraint. A [randomized savings-group evaluation](https://poverty-action.org/study/impact-savings-groups-lives-rural-poor-ghana-malawi-and-uganda) found improvements in financial inclusion, business outcomes and empowerment, but no average consumption or other welfare gains. The [six-study microcredit synthesis](https://www.aeaweb.org/articles?id=10.1257/app.20140287) likewise cautions against expecting transformative average effects. These findings motivate testing the productive opportunity and human outcome, not assuming them from lending activity.

## A falsifiable field test

These are proposed pilot gates, not achieved milestones or statistically powered poverty-impact claims:

1. Obtain at least three independent buyers and ten accepted paid packages over six weeks, including a repeat buyer. Label related-party purchases and subsidies separately. The published contractor posting is not one of these buyers.
2. For at least three jobs, document a necessary upfront cash gap, compare prepayment/direct funding, and retain input, delivery, acceptance, payment and settlement receipts. Issue no loan if cheaper adequate funding solves the gap.
3. Admit two people lacking capital through paid training and meaningful ownership, without a wealth-based entry requirement. Measure baseline work options, costs and hours with consent. Do not add members merely to collect contributions.
4. Observe retained and exited members for 90 days. Count additional household income after connectivity, equipment, payment fees, displaced work and all paid/unpaid time. Show that gains persist without consuming an undisclosed subsidy or simply reallocating a fixed amount away from incumbents.
5. Expand only when repeat orders or a measured missing capability support new paid work. Stop or redesign when demand, cash timing, quality or member outcomes fail. A larger comparison-based evaluation is needed before claiming causal poverty reduction.

Testnet transactions can test disbursement and repayment mechanics in parallel. Sepolia faucet currency has no purchasing power and cannot satisfy these commercial or human-outcome gates. No blockchain is required to establish whether the service itself creates value.

## Reproduction and review

Run from this directory:

```bash
python3 simulate.py --seeds 600
python3 audit.py
```

The standard-library simulation regenerates every history and all quantiles in `results/`. Generated raw histories are reproducible outputs, not empirical observations. The accompanying independent review checks conservation, financing equivalence, matched inputs, model limitations and a sample of exact reruns. This is internal review within one project, not independent external economic validation.
