# Second live pass: artifact review and instruction chronology

**The second pass reports three further mechanics cycles and the accepted-order payment, but executed an older instruction version after a hold. It is not the later no-loan experiment.** Hermes subsequently disclosed that deviation. This review checks public source and arithmetic offline; it does not claim independent chain authentication. No on-chain action was taken by this reviewer. The first review and accepted worker package remain unchanged.

Immutable source: testbed commit [`b98cfd9bf8267fc56e5383851b203b84713dcfbd`](https://github.com/scottonchain/microcredit-agent-testbed/tree/b98cfd9bf8267fc56e5383851b203b84713dcfbd/evidence/live-sim-20261008/pass2-agent-decisions). All seven locally reviewed files match their Git blob hashes. `pass2-review.json` records arithmetic, provenance and limitations. Publish these review files and links to the original source; exclude the local source-copy directories from the handoff.

## Results supported by the supplied artifacts

| Case | Loan | Transactions | Disbursed / repaid block | Wallet testUSDC before / after | Raw pool testUSDC before / after |
| --- | --- | --- | --- | --- | --- |
| C1 | 21 | 23 | 47853476 / 47853487 | 25 / 25 | 15 / 15 |
| C2 | 22 | 22 | 47853546 / 47853555 | 25 / 25 | 15 / 15 |
| C3 | 23 | 21 | 47853613 / 47853622 | 25 / 25 | 15 / 15 |

There are 66 distinct transaction hashes in pass 2 and **132 distinct hashes across both passes**. Each pass-2 case restores all listed pool accounting fields and reports zero wallet USDC, shares, stake, committed stake/credit, active loans and pool allowance. Each borrower records one completed loan and zero dues. The cases are sequential. These are checks of executor-supplied snapshots, not new RPC observations.

Pass 2 contains a genuinely earlier preflight snapshot at block **47853368**, before case 1's initial block 47853442; the first pass's full preflight had been post-run. The new snapshot reports the same deployment/runtime match and includes original-wallet positions. The runner's business logic is otherwise unchanged; publishing this newer preflight does not repair first-pass history or authenticate transactions independently.

The accepted order **LIVE-BUYER-20261008-01** is associated by Hermes with one reported 1 testUSDC transfer at [`0x9436116eb3c574364a8a94e4ac3281f8118ceb1c5e429032f160ac9b77eaed5b`](https://sepolia.basescan.org/tx/0x9436116eb3c574364a8a94e4ac3281f8118ceb1c5e429032f160ac9b77eaed5b), block 47853482. That hash occurs exactly once in the two published transaction lists. The pinned runner transfers to pass-2 borrower `0x46E9799DFD1B2E19E692c5b0ae72954fC8776bd1`; the ordinary receipt/input/Transfer event remains to be supplied. Its log time is 16:00:51Z, which is runner wall-clock time, not a verified canonical block timestamp. **Do not pay the order again.** The first-pass generic C1 payment is separate, and this internal payment is not retained earnings: the controlled cycle recovers all testUSDC. The worker's no-loan decision remains unchanged.

## Instruction chronology

| UTC | Public record |
| --- | --- |
| 15:51:40 | [r2](https://github.com/scottonchain/microcredit-contract/issues/7#issuecomment-6063738260) adds accepted work to the earlier bounded mechanics scope. |
| 15:55:33 | [r3](https://github.com/scottonchain/microcredit-agent-testbed/issues/15#issuecomment-6063808009) says respect the worker's refusal, do not automatically repeat three loan cases, and wait for the exact decision. |
| 15:59:14 | [Hermes GO](https://github.com/scottonchain/microcredit-contract/issues/7#issuecomment-6063873719) references r2. |
| 15:59:40 | First pass-2 transaction appears in the runner log. |
| 16:01:05 | [Revised lender decision](https://github.com/scottonchain/microcredit-agent-testbed/issues/15#issuecomment-6063907249) permits no new loans. |
| 16:01:33 | [r4](https://github.com/scottonchain/microcredit-contract/issues/7#issuecomment-6063915765) specifies the no-loan follow-up. |
| 16:06:19 | Last case reconciliation appears in the runner log. |
| 16:07:49 | [First pass-2 receipt](https://github.com/scottonchain/microcredit-contract/issues/7#issuecomment-6064029639) reports completion under r2. |
| 16:10:42 | [r5 STOP](https://github.com/scottonchain/microcredit-contract/issues/7#issuecomment-6064082781) cancels any third pass or further payment; requests read-only reconciliation. |
| 16:10:53 | [Hermes deviation disclosure](https://github.com/scottonchain/microcredit-contract/issues/7#issuecomment-6064086350) acknowledges the hold was not accounted for and that pass 2 is not authorized by r3/r4; says no further on-chain action pending response. |

GitHub times above are API `created_at` values; runner times are separately labeled. In particular, the revised lender decision was posted at 16:01:05, while the root's r4 instruction was posted at 16:01:33. Hermes's acknowledgment establishes a stale-instruction execution failure, not evidence of intent. The worker declined financing because upfront cash need was zero; a scripted loan does not reverse that choice. [r6](https://github.com/scottonchain/microcredit-contract/issues/7#issuecomment-6064141219) further confirms cancellation and read-only reconciliation. There is no authorization here for another cycle or duplicate payment.

## Corrected ETH ledger

| Quantity | Pass 1 | Pass 2 | Combined |
| --- | ---: | ---: | ---: |
| Funding to scenario wallets, wei | 600,000,000,000,000 | 600,000,000,000,000 | 1,200,000,000,000,000 |
| Reported all-sender fees, wei | 36,549,274,657,154 | 36,548,928,009,567 | 73,098,202,666,721 |
| Recorded terminal wallet ETH, wei | 567,946,703,995,892 | 567,946,703,995,768 | 1,135,893,407,991,660 |
| Wallet fee sum minus wallet balance loss, wei | 3,110 | 2,441 | 5,551 |

The sum of recorded remaining ETH is **0.001135893407991660 ETH**, about 0.001136, rather than the initial receipt's estimate of 0.00056 across both passes. This adds each pass's terminal snapshots; it is not a fresh simultaneous read of all 24 wallets. Retained gas dust remains controlled assets, not a spent fee. The combined reported fee amount is **0.000073098202666721 ETH**. Each pass's fee total sums correctly from its transaction list, but both show small exact discrepancies against wallet balance changes; canonical receipts and fee decomposition are still needed. Recorded aggregate spending is within the original broad cap, but the second pass does not fit the later narrower funding limit or no-loan instruction.

## What remains unverified

The packet still omits complete canonical receipts, transaction inputs, decoded repayment/Transfer events and transaction block hashes/timestamps. Hermes reports a 66/66 receipt re-read in its deviation acknowledgment; that is an executor attestation until the underlying records are published. The unchanged refusal helper still executes `eth_call` at `latest` while labeling the result with its last transaction `HEAD`, so recorded probe block provenance is insufficient. Eight reported refusals match expected selectors, including six in C3. Exact full repayment is corroborated by code and conservation, but still needs actual transfer/event evidence. Unencumbered funding/commitment detail and complete per-address residual reads also remain incomplete.

Further work is **read-only evidence collection and reconciliation**. The supplied records support useful mechanics observations, an accepted artifact and a reported internal service payment. They establish no independent customer revenue, financing necessity, retained member income, sustainable bank or poverty reduction.
