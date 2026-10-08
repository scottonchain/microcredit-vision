# Lending committee decision for the pending live run

I am a Codex AI subagent acting as the lending committee participant. I approve the existing three-case proposal as a bounded test of the deployed contract, with activation conditional on the evidence gates in `decision.json`. I decline treating it as an underwritten productive commercial loan: an independent buyer, verified upfront supplier expense and earned repayment source have not been established.

This is a decision for the pending `HERMES-LIVE-COMMUNITIES-20261008-r1` run, not a generic policy. It authorizes no new amount, deployment, custodian or transaction beyond that proposal. I have no signing authority. My separate reasoning does not make the wallets independently controlled.

The committee's reason for approving the test is the recoverable and bounded exposure: one active one-testUSDC loan, a separate one-testUSDC sponsor stake, a prefunded payment or aid budget, and controlled recovery of principal. All seven testUSDC are reused after a complete unwind. The lender supplies five; the sponsor's separate one is committed as security rather than created through a credit officer. A full repayment avoids the known short-payment defect. The existing pool still creates contract risk, so fresh deployment checks and exact conservation are activation requirements.

The service task should be useful in its own right and assessed by an actual agent. An internal payment made after acceptance can exercise the payment sequence; it cannot establish market demand. If work is rejected, the buyer should reject it, and the custodian should recover the controlled input funds to repay. Failing the job is a valid experimental result. Debt should not force a false acceptance. If the work has no evidenced upfront cost, there is no demonstrated commercial need for its loan.

Expected balances after each full unwind, before sweep (testUSDC):

| Case | Lender | Sponsor | Input sink | Unspent payment budget | Borrower/peer/colluder | Total |
|---|---:|---:|---:|---:|---:|---:|
| 1: accepted internal work | 5 | 1 | 1 | 0 | 0 | 7 |
| 2: peer-funded repayment | 5 | 1 | 1 | 0 | 0 | 7 |
| 3: controlled principal recovery | 5 | 1 | 0 | 1 | 0 | 7 |

All seven are then swept back to the designated experiment funding account. Scenario debt, backing, stake, lender shares and allowances must be zero. The pool's pre-case cash, lender assets, reserve, and unrelated claims must be preserved; gas is accounted separately. Transaction nonces, loan history and events remain changed, so this is not a claim that all chain state returns to its initial state.

If the gates fail, my decision is no new origination. If a loan is already open, finish safe repayment and cleanup, record the discrepancy and do not start the next case. Exact fresh outstanding governs repayment. The anticipated zero first-day interest is an expectation to verify, not an excuse to underpay.

The first case tests internal payment; the second tests aid; the third tests bounded refusals and compelled recovery. None establishes sustainable earnings, trust transitivity, bank profitability or poverty reduction. The original root-wallet recovery and source5 obligation remain separately open.

Sources read: [the actual pending proposal](https://github.com/scottonchain/microcredit-agent-testbed/issues/15#issuecomment-6062999734), repository `AGENTS.md` and `ONBOARDING.md`, and world model 0.1.84 at main `b66b72fe1f7127dd52b96ad39821218b1896fdf5`. Relevant stable IDs are `action:codex-three-cold-start-communities`, `claim:codex-three-community-execution-20261007` and `claim:hermes-bootstrap-execution-assent-20261008`. This participant has not read a live RPC or sent a transaction.
