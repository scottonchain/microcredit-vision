# Actual-agent collective: execution packet

Prepared by Codex / ChatGPT (AI), 2026-10-08, in response to the operator's request to rerun the collective experiment with actual agents against actual contracts.

**This packet records actual agent decisions and delivered work. Live contract execution remains pending until transaction evidence is attached and reviewed. It is not another Monte Carlo run.**

## What actually happened

| Participant | Observed decision or work | Execution status |
| --- | --- | --- |
| Lending committee agent | Conditionally approved bounded test credit; declined treating it as an underwritten productive loan | Approval inactive pending fresh preflight |
| Worker agent | Produced a source-pinned evidence schema and acceptance checklist; declined a loan because evidenced upfront cash need is zero | Delivered and revised |
| Buyer agent | Issued an internal one-testUSDC order; required a correction so missing measurements can remain unknown; accepted the revised delivery by digest | Service accepted; payment unobserved |
| Hermes | Requested executor and private custodian for existing authorized live run | No receipt obtained when this packet was prepared |
| Codex root | Coordinated participants, transported evidence and requested execution | Does not hold the scenario signing keys |
| Claude | Reviewer/publisher of the related guest post | Prior numerical-model PR10 merged into editorial staging, not published |

The worker's first submission required a future after-state even for an active case. The buyer rejected that requirement, the worker changed it, and the buyer verified the correction before accepting. The preserved review trajectory is in `buyer/`. This is a concrete example of useful joint work. All these reasoning participants operate under the same operator; they are not independent economic counterparties.

The approved service consideration is one testUSDC, payable only through the already-authorized internal budget and after executor preflight. It is not additional spending authority. It must not be counted twice or claimed paid without a transfer receipt. The worker did not need financing, so any borrow-to-input-sink cycle remains a separate contract mechanics experiment.

## Existing execution scope

Use [the bounded live-run authority](https://github.com/scottonchain/microcredit-agent-testbed/issues/15#issuecomment-6062999734) and [the actual-agent addition](https://github.com/scottonchain/microcredit-contract/issues/7#issuecomment-6063515086). Do not start a duplicate run.

The target is the existing Base Sepolia pool `0x73872B8fB7F1771C67911f03edc75aBdc9514973`, chain 84532, Circle testUSDC `0x036CbD53842c5426634e7929541eC2318f3dCF7e`. At most seven testUSDC are reused across three sequential cases, with at most 0.003 testETH gas. Each case uses a five-token lender deposit, a separate one-token sponsor stake/backing, a one-token loan and a one-token internal payer or aid budget. Cases cover internal task payment, peer repayment and controlled adversarial-refusal probes followed by cleanup.

All original root-custodied wallets and their source5 recovery obligation remain separate. No candidate deployment, mainnet operation, officer grant, mint or faucet retry is authorized. This packet does not expand the existing spending or custody permissions.

Fresh deployment verification is necessary: the Solidity behavior pin and current address-documentation pin differ. `worker/source-manifest.json` preserves both. A source review is not a deployed-runtime comparison.

Use `worker/ACCEPTANCE.md` to evaluate actual evidence. The JSON schema and limited checker help record evidence; neither authenticates blockchain receipts. Missing observations are unknown, not zero. Only complete, verified receipts and before/after ledgers can establish live completion. If work is rejected, controlled principal recovery supports cleanup without inventing a successful order. If a loan is already open, finish safe repayment and unwind before waiting for review.

## How to assess the outcome

Keep separate counts for actual agent decisions, accepted service delivery, observed payment, mined contract cycles and independently earned revenue. The first two are evidenced here. The latter three are not established by this packet. The pending and active evidence files are explicitly labelled examples and contain no invented observations.

No human poverty result can be inferred from internal transfers of test currency. The original objective still requires independent paying customers, consenting human members and measured net household gains after labor, costs and losses. The zero-loan choice for this particular task does not show that other productive work never needs working capital.

Claude: use this packet and eventual transaction receipts as a factual follow-up to [vision PR10](https://github.com/scottonchain/microcredit-vision/pull/10). Keep the earlier model's numerical results labelled assumptions-based simulation. Do not retrofit these actual decisions into transactions that predate them, claim a payment has happened, or publish a completed-live-run claim until receipts pass review.
