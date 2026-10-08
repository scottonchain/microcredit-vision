# Acceptance checklist: actual agents, existing live pool

Worker: `/root/live_worker`. I accept producing this review artifact. I request **no loan**: no new upfront cash expense is evidenced. The buyer's provisional 1 testUSDC consideration is an internal test payment contingent on acceptance; receipt is not yet observed. This work must not be described as loan-enabled work or independent revenue.

## Version and scope

Use `source-manifest.json` for immutable references. Behavior is read from Solidity commit `1812e7d2b67e159e341bbff33d6d604409eebb67`; canonical address documentation is separately pinned at `9f5c1434a1fa99bec7939bbf458f86ddee55bec9`. **The deployment commit's own TESTNET.md is obsolete and still describes the previous mock pool.** Documentation alone does not establish the current runtime or chain state.

Target: Base Sepolia **84532**; pool `0x73872B8fB7F1771C67911f03edc75aBdc9514973`; Circle testUSDC `0x036CbD53842c5426634e7929541eC2318f3dCF7e`. Tokens have no economic value. The three cases are controlled by one disclosed team with Hermes custody. No candidate PR28 deployment, officer grant, faucet/mint, original-wallet funding or CI30 short-repayment exercise is in scope.

## Required evidence before borrowing

- Fresh block number, hash and UTC timestamp; observed chain ID; pool runtime bytecode hash and reproducible source/build comparison accounting for immutables; token, lens, score-provider wiring and current roles/parameters. Record actual values, including pause, utilization, liquidity buffer/threshold, fee/reserve, loan limits and grace/term constants. Abort on mismatch or inability to cover complete repayment and unwind.
- Pinned public execution script with SHA-256, participant role decisions, scenario address-to-role/controller mapping and source ledger. Never include keys, credentials, signatures or raw signed transactions.
- Available unearmarked holdings and preserved commitments: maximum **7,000,000 USDC units recycled across all three cases** and **3,000,000,000,000,000 wei total gas**. Estimate every transaction including cleanup and fee components. Preserve existing payment/candidate/Oct19-20 commitments. Re-read all 13 protected original addresses in the manifest, original lender shares/assets and source5 status; their recovery obligation remains separate.

## Per-transaction evidence

Capture fresh sender nonce and balances; exact `eth_call` simulation (`from`, `to`, full calldata, block/hash, raw result); submitted public transaction hash; canonical receipt with success status, from/to, nonce, block/hash/time, decoded events and all fees. Reconcile before retry. An RPC transport error or timeout is not a contract refusal. Public transaction hashes and receipts suffice; unsigned calldata is acceptable, signed bytes are not.

## Cases and semantic checks

| Case | Actual sequence to establish | Required interpretation |
| --- | --- | --- |
| C1 | New lender `depositFunds(5000000)`; separate sponsor `stake(1000000)` and `back(borrower,1000000)`; borrower `requestLoan(1000000)` then `disburseLoan(id)`; borrower transfers to controlled input sink; internal payer transfers 1000000 to borrower; exact full repayment | Test mechanics and internal payment; the input sink must not be called a paid real input without an actual order and delivery. This worker's evidence task does not need the loan. |
| C2 | Same deposit/stake/backing/loan/input transfer; peer uses its own earmarked 1000000 endowment and calls `repayLoan(id,freshOutstanding)` with its own allowance | Source `_repay(...,msg.sender,...)` charges the peer, not borrower. Prove payer identity using token transfer and receipt. Peer endowment is internal aid, not borrower earnings. |
| C3 | Same setup; loan proceeds to controlled colluder; overlimit, onward-backing and repeat-request probes by read-only `eth_call`; colluder supplies exact full repayment | Compelled cleanup is not voluntary honesty or observed default. Record each exact attempted call, state and decoded failure. |

Source `getFreeCredit` permits only a backer's own granted credit or free stake, not forwarding received backing. With fresh zero-grant accounts, `back(next,1000000)` by the backed borrower should fail `InsufficientCredit()`. Amounts below 1000000 fail `BackingTooSmall()` instead and **do not** establish this rule. Before the first loan, requesting 1000001 against a 1000000 line should fail `BorrowLimitExceeded()`; after the full line is reserved/disbursed, a further positive request should fail the same error. A repeat request after full repayment may succeed: the contract does not universally ban repeat loans. Probe all other preconditions so an unrelated pause/liquidity failure is not credited as the intended refusal.

## Unwind and ledger: pass every case before starting the next

1. Use `getCurrentOutstandingAmount(id)` immediately before full repayment. Prove principal paid **exactly 1000000** and interest zero while elapsed time is strictly below 86400 seconds from disbursement. Source starts charging interest at the grace boundary; target under one hour. `Repaid` status alone is insufficient because the deployed source can close sub-cent residuals. Confirm actual token transfer and `RepaymentApplied` principal amount; do not test that defect live.
2. After repayment, `back(borrower,0)`, `unstake(1000000)`, `withdrawFunds(type(uint256).max)` to withdraw all free shares, revoke allowances, sweep scenario USDC. Read back zero scenario active debt, backing, committed stake/credit, stake, shares, queued shares, unclaimed payouts and allowances. Do not infer cleanup from receipt success alone.
3. Use one block-pinned before/after snapshot per boundary. Include every scenario-controlled address and funding treasury, payer/peer, input sink/colluder and sweep recipient, plus raw pool balance. Enumerate all transfers crossing the boundary; for this isolated run both external flow totals must be zero. Do not add shares/stake claims to raw pool balance: that double counts tokens. Verify exact integer equality separately for aggregate wallets and pool; also verify their combined total. Gas is a separate ETH loss, including applicable L1/data/operator fee components, reconciled against balance deltas.
4. Preserve unrelated lender positions and pool accounting: lenderCash, totalLentOut, totalImpaired, reservedLiquidity, firstLossReserve, totalDuesPaid, protocolFees, totalStaked, totalShares, totalQueuedShares and totalUnclaimedPayouts. Check `totalAssets = max(0,lenderCash + totalLentOut - max(totalImpaired,firstLossReserve))`; raw token balance is not totalAssets. Queue side effects must be disclosed and reconciled; unexplained unrelated changes block acceptance. Completed-loan counters may increment; zero-interest repayment must not generate dues or granted credit.

## Required assertion IDs and decision

Each case reports `identity`, `funding_caps`, `transaction_provenance`, `case_semantics`, `full_repayment`, `zero_residuals`, `wallet_conservation`, `pool_conservation`, `protected_state`, `sequential_execution`, `fee_reconciliation`, and `claim_limits`. C3 also reports `refusal_semantics`. Every assertion needs an expected value, observed value, public evidence references, and `pass`, `fail` or `missing` status. No receipt/state has been independently observed by this worker. Non-complete cases use null for unknown snapshots or ledger; completed cases require all three. `active-evidence.example.json` is a fixture demonstrating unknowns, not a live execution claim.

Accept live completion only with three distinct cases, all required assertions passing, no missing evidence, complete canonical receipts and an independent reviewer acceptance. Otherwise classify pending, blocked or needs revision. Missing data is not zero or success. `check_evidence.py` offers a deliberately limited stdlib structural/claim/ledger gate; it does not authenticate chain evidence, validate every JSON Schema keyword, or replace reviewer verification. The schema is supplied for a standards validator; that validator was unavailable here.

Separate conclusions: actual useful agent work can be accepted before the live cash cycles finish. Live testnet mechanics establish neither outside demand nor net economic earnings, autonomous independent controllers, transitive trust, sustainable lending or poverty reduction. A later poverty claim requires real consenting members, independent paying customers and measured net household income over time, including costs and losses.
