# Read-only supplement review

**The supplement supplies consistent transaction inputs, successful receipt fields, six exact repayments and the single accepted-order payment. Its revised fee components also close the scenario-wallet ETH equations.** This is an offline review of Hermes's reconstruction, not an independent RPC observation. No transactions, signatures or new funding were produced by this reviewer. Earlier reviews remain unchanged as historical records.

Source: [immutable supplement commit `be0e90904c50f0d43fc0a52b76ff08cded2c84af`](https://github.com/scottonchain/microcredit-agent-testbed/tree/be0e90904c50f0d43fc0a52b76ff08cded2c84af/evidence/live-sim-20261008/supplement-20261008T1618Z), reconstructed after execution at 16:16–16:18Z, and [Hermes's receipt](https://github.com/scottonchain/microcredit-contract/issues/7#issuecomment-6064232315). Four reviewed JSON inputs match their immutable Git blob hashes; `supplement-review.json` records exact checks and results. These files are normalized transaction/receipt extracts with selected decoded events, **not unabridged raw RPC receipts**.

## Transaction and payment checks

All **132 distinct hashes** match the two original transaction lists. Sender, recipient contract, nonce, block number and gasUsed agree; every supplied receipt has status 1. The extracts now contain input calldata, block hashes, effective gas price, L1 fee and decoded USDC/repayment events. Every supplied fee equals gasUsed × effectiveGasPrice + l1Fee.

For each of loans **18–23**, the repayment input encodes its loan ID and **1,000,000** token units. The corresponding decoded USDC transfer moves exactly that amount from the actual payer to the pool. `RepaymentApplied` records principal 1,000,000, interest zero and fee zero; `LoanRepaid` records the same loan and payment amount. This addresses the earlier concern that a closed status alone might conceal the deployed sub-cent write-off behavior. The decoder's event indexing matches the pinned contract declarations. C1 is paid by its borrower; C2/C3 are paid by their respective peer/colluder addresses.

The accepted-order transaction [`0x9436116eb3c574364a8a94e4ac3281f8118ceb1c5e429032f160ac9b77eaed5b`](https://sepolia.basescan.org/tx/0x9436116eb3c574364a8a94e4ac3281f8118ceb1c5e429032f160ac9b77eaed5b) has one matching input and decoded Transfer for **1 testUSDC** from the controller to pass-2 worker `0x46E9799DFD1B2E19E692c5b0ae72954fC8776bd1`, at block 47853482. It occurs once in the supplied 132 records. There are **two generic C1 payment transactions across the two passes**; only the second is associated with the later accepted order. Do not pay that order again or relabel the first payment.

Reconstructing balances from all supplied decoded USDC transfers, starting with controller 25 and pool 15, ends each pass at controller **25**, pool **15**, and every other address **zero**. No intermediate reconstructed balance is negative; the controller's peak net USDC outflow is exactly **7** in each pass. This independently checks the arithmetic within the supplied data, rather than merely accepting the reported aggregate totals.

## ETH correction

| Wei | Pass 1 | Pass 2 | Combined |
| --- | ---: | ---: | ---: |
| Revised all-sender fees | 36,549,274,652,894 | 36,548,928,006,072 | 73,098,202,658,966 |
| Earlier total minus revised total | 4,260 | 3,495 | 7,755 |
| Scenario-wallet part of that difference | 3,110 | 2,441 | 5,551 |
| Controller part of that difference | 1,150 | 1,054 | 2,204 |

For both passes, **funding − recorded final wallet balances − revised scenario fees − native value sent out = 0 wei**. The formerly unexplained 5,551-wei scenario discrepancy is therefore resolved arithmetically by the supplied reread fee components. The corrected combined fee is **0.000073098202658966 ETH**. Recorded scenario dust remains **1,135,893,407,991,660 wei** (0.001135893407991660 ETH); Hermes also reports a current reread confirming that sum.

The cause of the earlier fee-field variation is still unknown. Original receipt component fields were not preserved, so the earlier stored costs do not prove that a node's L1 fee changed or that a different node was used. The defensible statement is that later supplied fee components reconcile balances. `fee_ledger.json` also calls the earlier total `scenario_fee_recorded_l2_only`, although the original runner included L1 fees; that field should be renamed.

## Refusal replay: misleading label, appropriate historical state

The feared replay-at-case-start error is **a labeling error, not what the numeric data shows**. `stored_case_start_block` actually holds each original refusal's updated `HEAD`. It differs from `pool_before.block` for all 16 refusals. The runner updates HEAD after every own transaction. The second tag independently derives the immediately preceding transaction block from the log, so both tags agree.

For example, pass-1 C3 starts at **47852864**, but the repeat-request and backing-removal replays use **47852894**, the successful reservation block. That is the relevant state for `BorrowLimitExceeded()` and `BackingInUse()`. Pass-2 equivalents similarly use **47853610**, rather than its case start **47853576**. All 16 reported refusals replay with the expected selectors.

Correct the tag to `stored_refusal_head_block` and describe this as **16 historical call/state observations repeated under two equal numeric tags**, not 32 different states. The historical replay is useful evidence. It does not establish the exact block used by the original unpinned `latest` calls, and must remain labeled as later reconstruction.

## Remaining limits

The public extracts omit raw log topics/data, full receipt objects and canonical transaction-block timestamp headers; this reviewer did not independently authenticate RPC results. Exact repayment amounts are now supported within the extracts, while precise elapsed-time claims still rely on the runner and executor. The fresh idle state is reported in the receipt comment but is not a full structured snapshot in this immutable packet. Original contemporaneous first-pass preflight and a complete source/earmark ledger remain incomplete.

Evidence repair changes neither the instruction chronology nor the worker's refusal. Pass 2 still followed a stale instruction after the hold and is not the no-loan experiment. The accepted service payment was internal, all test tokens returned to the controller, and no financing need, outside revenue, retained earnings or poverty effect was demonstrated. This review authorizes no new loan, payment or rerun; the next activity is the factual blog handoff.
