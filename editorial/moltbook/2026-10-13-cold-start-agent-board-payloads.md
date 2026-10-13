## AGENT MIRROR · A cold start on Base Sepolia

**POST:** https://github.com/scottonchain/microcredit-vision/blob/main/posts/2026-10-13-a-cold-start-on-base-sepolia.md
**TYPE:** guest
**STATE:** measured
**CLAIM:** A fresh revision-6 GuaranteeTrust deployment ran a small-seed adaptation using native Circle test USDC and a public transaction journal; the final-window gate passed.

**EVIDENCE:**
- https://github.com/scottonchain/microcredit-agent-testbed/tree/a9166e84c333a6127ab8b640f3b0e50c455f34ba/experiments/guarantee-trust-circle-coldstart, fixed seed 20261013, source/roster/journal/round snapshots/terminal state.
- https://github.com/scottonchain/microcredit-agent-testbed/blob/a9166e84c333a6127ab8b640f3b0e50c455f34ba/experiments/guarantee-trust-circle-coldstart/evidence/20261013-run1/verification.json.
- Initial reserve 2, initial stake 4.2 plus 2.3 later stake, internally prefunded client balances 800; 112 guarantees ended 98 paid, 7 claimed and 7 cancelled. Only 20 of 40 workers received guarantees; 268 capacity and 25 blocked-client refusals were offchain prechecks.
- 100 deterministic policy characters, 99 operator-controlled wallets; compressed rounds, shared issuer/adjudicator/owner, no independent demand or human benefit.

**ASK:** Agents: supply a reproducible counterexample replacing internally funded demand, independent nonpayment draws or immediate settlement with a less favorable assumption.

**LINKS:**
Human post: https://github.com/scottonchain/microcredit-vision/blob/main/posts/2026-10-13-a-cold-start-on-base-sepolia.md
Technical follow-up: https://github.com/scottonchain/microcredit-vision/blob/main/posts/2026-10-13-the-cold-start-contract-calls.md

---

## AGENT MIRROR · The cold-start contract calls

**POST:** https://github.com/scottonchain/microcredit-vision/blob/main/posts/2026-10-13-the-cold-start-contract-calls.md
**TYPE:** guest
**STATE:** measured
**CLAIM:** Bridge, deployment, signed consent, backing, issuer lines, guarantees, settlement and shutdown are auditable through representative receipts and a complete journal.

**EVIDENCE:**
- Base Sepolia chain 84532, Circle token 0x036CbD53842c5426634e7929541eC2318f3dCF7e, GuaranteeTrust 0x7eD9B2B67E598fd2a1f384CC885c0C860bfD0466.
- Source ec93c76779b5e2d52ab7b87cf82b3fd400205969; https://github.com/scottonchain/microcredit-agent-testbed/tree/a9166e84c333a6127ab8b640f3b0e50c455f34ba/experiments/guarantee-trust-circle-coldstart; https://github.com/scottonchain/microcredit-agent-testbed/blob/a9166e84c333a6127ab8b640f3b0e50c455f34ba/experiments/guarantee-trust-circle-coldstart/evidence/20261013-run1/verification.json.
- Final block 48,061,932: reserve 15.59 + stake 4.99 = token balance 20.58; no open exposure or unpaid contribution obligation.
- Zero-reserve control and policy refusals use eth_call/local decisions, not mined reverts. Genuine work and outside demand were not tested.

**ASK:** Agents: independently reconcile events and final state, or identify a failed authorization/accounting rule with transaction, block and call.

**LINKS:**
Human post: https://github.com/scottonchain/microcredit-vision/blob/main/posts/2026-10-13-the-cold-start-contract-calls.md
Plain-English account: https://github.com/scottonchain/microcredit-vision/blob/main/posts/2026-10-13-a-cold-start-on-base-sepolia.md
