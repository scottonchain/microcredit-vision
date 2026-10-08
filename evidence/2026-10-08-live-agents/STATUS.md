# Actual-agent run: results and limits

Codex / ChatGPT (AI), 2026-10-08. The actual runs produced useful work, settled test-token payments and exposed a failure to apply an updated instruction. The receipt supplement closes several accounting gaps without changing that finding.

| Component | Result |
| --- | --- |
| Lender, worker and buyer agents | Prospective decisions, delivered work, requested correction, revised delivery and acceptance recorded |
| Worker borrowing choice | Declined: no new cash advance required for this particular task |
| First live pass | Loans 18–20; 66 transaction records; preceded the new participant decisions |
| Second live pass | Loans 21–23; another 66 records; accepted work paid once |
| Repayment and token accounting | Supplied receipt extracts support six exact one-testUSDC repayments and restored token balances |
| Instruction adherence | Failed: second pass followed older r2 after r3's hold; Hermes acknowledged the deviation |
| Planned no-loan pass | Canceled; neither three-loan pass counts as compliance with it |
| Outside revenue and human poverty outcome | Not established; recovered internal test currency has no economic value |

The accepted order is `LIVE-BUYER-20261008-01`. Payment transaction `0x9436116eb3c574364a8a94e4ac3281f8118ceb1c5e429032f160ac9b77eaed5b`, block 47853482, transfers one testUSDC from the internal controller to worker recipient `0x46E9799DFD1B2E19E692c5b0ae72954fC8776bd1`. It occurs once among the 132 records. It must not be paid again. The first-pass generic task transfer is a different experiment transfer and does not pay this later order. The worker's payment was used in the second-pass repayment cycle; it is not retained income.

Hermes reports the second pass started at 15:59:40 UTC, after the 15:55:33 hold. Its go/no-go cited the older revision. The narrower lending decision was posted at 16:01:05, its routing message at 16:01:33. Hermes then disclosed the sequencing deviation. Codex stopped repeats at 16:10:42 and canceled the no-loan pass at 16:13:59. A timely update on one coordination thread was not reliably carried into the executor's running instructions. Repayment success does not establish decision adherence.

The [supplement review](chain-review/supplement-review.md) checks 132 normalized transaction/receipt extracts retrieved by Hermes from public RPC, including inputs, status, block hashes and selected decoded logs. All six repayment calls, token transfers and repayment events agree on exactly 1,000,000 token units of principal, with zero interest or fees. Reconstructing all supplied token transfers restores 25 testUSDC to the controller and 15 to the pool after each pass, with zero elsewhere and a peak allocation of seven. The 25-token treasury balance was not the experiment's authorized spending limit.

Corrected all-sender fees total 73,098,202,658,966 wei (0.000073098202658966 testETH). Funding across both passes was 0.0012 testETH. The 24 scenario wallets retain 0.001135893407991660 testETH under existing custody. With reread fee components, scenario funding minus residual balance minus fees reconciles exactly. Earlier recorded all-sender costs exceeded these rereads by 7,755 wei; the cause of that fee-field variation is unknown because the original component records were not retained. No gas-dust recovery or original root-wallet/source5 restoration is claimed.

There are 16 historical refusal call/state observations, each replayed under two equal block tags. They are not 32 distinct states. The supplement's `stored_case_start_block` label is wrong: it is the updated refusal HEAD, which correctly falls after the relevant setup or reservation. Original `latest` calls remain unpinned; later reconstruction cannot become contemporaneous evidence.

Read the [first review](chain-review/REVIEW.md), [second review](chain-review/pass2-review.md) and [supplement findings](chain-review/supplement-review.json) in order. Earlier reviews remain unchanged, with their gaps resolved or narrowed by the supplement. Reviewers checked supplied artifacts offline; they did not independently query the chain. Full raw log topics/data, original first-pass preflight and a complete unencumbered source/earmark ledger remain absent. The new idle state is reported by Hermes at block 47853987: no lent principal, reservations or stake, and the controller retains 25 testUSDC.

No further financial pass is requested. Any future experiment needs a single current work-order revision, exact permitted calls and duplicate-payment protection checked before spending. The separate mature-community proposal is a future lane, not authorization to replay or relabel these results.
