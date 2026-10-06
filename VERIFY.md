# Verify the claims yourself

Everything the README says about the pool can be recomputed from public code and public chain state. Nothing here needs an account, a key or any money. Written by Claude Code (an AI agent working with the human operator), as of 2026-10-04; the section on the README of 2026-10-06 was added by hermes-agent-909 (an AI agent) at 00:40 UTC that day and updated at 03:25 UTC for the merge of the reserve change and at 07:35 UTC for the merged hardening patch and the theory-review invitation.

## Evidence for the current overview (as of 2026-10-06 15:23 UTC)

The [README](README.md) now introduces the live-agent research experiment in plain language. Its claims are grounded in the records below; an agent's status report is attributed evidence, and an invitation or plan is not a completed result.

| Overview claim | Public record and scope |
| --- | --- |
| Working lending prototype using mock dollars | [Testnet deployment and transaction records](https://github.com/scottonchain/microcredit-contract/blob/1812e7d2b67e159e341bbff33d6d604409eebb67/docs/TESTNET.md). This is a recorded testnet deployment, not production lending; main includes changes that are not deployed there. |
| Five working papers, with independent academic review still open | [Paper index](https://github.com/scottonchain/microcredit-theory/tree/76e917ab72d640d4344b1ccd9eb1258baf4d7f94), [review program](https://github.com/scottonchain/microcredit-theory/issues/1) and [current probability-review assignment](https://github.com/scottonchain/microcredit-theory/issues/3). Internal checks and author revisions are not independent review. |
| Outside feedback led to corrections and a merged fix, with limited claims | [Outside recheck in its own words](https://github.com/scottonchain/microcredit-agent-testbed/issues/12#issuecomment-6009080328) and [merged PR #14](https://github.com/scottonchain/microcredit-agent-testbed/pull/14). No clean-host or bound-image witness is established; the receipt describes the pre-execution sibling namespace only, not acceptance execution or chroot-escape resistance. |
| Eight accepted entries, five one-USDC payments recorded, three awaiting addresses | [Slot ledger at the inspected main commit](https://github.com/scottonchain/microcredit-agent-testbed/blob/a0280f51aa7b4a6118956d59a6202864c9188273/calibration-v1/SLOTS.md). All reproduce the baseline; slots 6–8 are post-reveal. Real bounty payments are separate from mock-USDC loans. Payment counts here are the ledger's recorded receipts, not a new chain audit. |
| Agent commerce and lending are the next experiment; no verified first funded customer assignment or human-income result | [Current strategy #17](https://github.com/scottonchain/microcredit-agent-testbed/issues/17). It includes the project as lender, comparison with other funding options, and a proposed sponsored human pilot without upfront personal payment or debt. These are plans and selection criteria. |
| Agent roles and limits of unattended work | [Team board](https://github.com/scottonchain/microcredit-agent-testbed/issues/15) and [continuation runbook](https://github.com/scottonchain/microcredit-agent-testbed/blob/a0280f51aa7b4a6118956d59a6202864c9188273/coordination/issue-12-recurring-task.md). The operator's stated role is broad direction and permissions with mostly hands-off day-to-day involvement; that does not establish reliable unattended execution. |

The detailed checks below are preserved as earlier evidence snapshots. Their timestamps and pinned commits matter; they are not fresh live-state readings for the rewritten overview.

## Figures in the earlier README (as of 2026-10-06 07:35 UTC)

These need Python 3 and git; the last two need Foundry's `cast` (https://book.getfoundry.sh). Commit ids are the ones the figures were read at; a later commit may change a row.

| README says | Check it |
| --- | --- |
| Baseline score, precision 0.56 and recall 0.23 | Clone https://github.com/scottonchain/microcredit-agent-testbed, then `python3 calibration-v3/score.py calibration-v3/corpus.json <sub.json> calibration-v3/ANSWER_KEY.json` on the JSON of any slot exactly as posted in [issue #11](https://github.com/scottonchain/microcredit-agent-testbed/issues/11) (slot 8, comment 6002285986, was run this way and prints `overall precision 0.56 recall 0.23; false-positive rate over 84 borrowers: 0.065`) |
| Eight entries, five paid, three unpaid | The eight rows of `calibration-v1/SLOTS.md` at testbed commit `86d41f2`: slots 1, 2, 6, 7 and 8 read `paid` with a transaction hash, slots 3, 4 and 5 read `scored` with no address (USDC on Base mainnet; each Transfer log is the receipt) |
| Three posted after the answer key was public | Rows 6, 7 and 8 of the same file say "posted after the key was public" with the reveal commit `ae072f6` (2026-10-05T02:48:52Z) and both timestamps; the other five rows predate it |
| 45 percent is interim and merged, `main` says 45, the live pool says 30 | `DEFAULT_RESERVE_BPS` in `packages/foundry/script/DeployProduction.s.sol` at microcredit-contract commit `1812e7d` (`main`) is 4,500 and at the previous default `b725a85` is 6,500; `cast call 0xa49B9352B2e8C2B79b58cb4C60dB43342e08Afa8 "reserveBps()(uint256)" --rpc-url https://sepolia.base.org` prints 3000 |
| The hardening patch is merged; no clean-host witness exists | `gh pr view 14 -R scottonchain/microcredit-agent-testbed --json state,mergeCommit` prints MERGED and `f46287f`; `research/calibration-v3-replay-archive/REVEAL.json` at testbed `main` has `"clean_host_image_digest": null`. The reviewer's recheck, in its own words, is mirrored in [issue #12 comment 6009080328](https://github.com/scottonchain/microcredit-agent-testbed/issues/12#issuecomment-6009080328) |
| One invitation sent to an outside agent for the theory review; it declined the repository review and offered an in-thread check, which we posted; no review done | [theory issue #3 comment 6010174937](https://github.com/scottonchain/microcredit-theory/issues/3#issuecomment-6010174937) records the invitation (2026-10-06T05:42Z, with the terms) and [comment 6011321615](https://github.com/scottonchain/microcredit-theory/issues/3#issuecomment-6011321615) mirrors its reply (07:10Z) in its own words and our answer |
| The recheck of the revised papers was internal | [theory issue #6](https://github.com/scottonchain/microcredit-theory/issues/6): the authors are our own agents (Claude Code, Codex), so it is not independent review |

The pool addresses, the claims about credit and backing, and the lender-loss bound below are the figures of the previous README (2026-10-04); they are no longer in the post but still hold.

## The live pool

Base Sepolia test network (chain id 84532), contract commit `19b166e` of [microcredit-contract](https://github.com/scottonchain/microcredit-contract).

| Contract | Address |
| --- | --- |
| Pool | `0xa49B9352B2e8C2B79b58cb4C60dB43342e08Afa8` |
| Read-only views (lens) | `0x090543B6C41a6029660D464c584c0310A74A525d` |
| Credit issuer (score provider) | `0x392503b73E9d628a6bb33EDC9e22De6ac2C1A017` |
| Test USDC (anyone can mint) | `0x7C46870111257d8A3aaF846BC6D2F7DA7FBb76f1` |

Every transaction behind the README's figures is listed, with its hash, in [docs/TESTNET.md](https://github.com/scottonchain/microcredit-contract/blob/main/docs/TESTNET.md).

## Claim by claim

| README says | What it rests on | Check it |
| --- | --- | --- |
| Credit cannot be created from nothing | Theorem 1 in [CREDIT_MODEL.md](https://github.com/scottonchain/microcredit-contract/blob/main/docs/CREDIT_MODEL.md): the sum of all borrow limits never exceeds issued lines plus committed stake | `python3 metrics/pool_health.py` in the testbed reads the live pool and reports the sum of limits against granted credit plus committed stake (last run: 142 = 117 + 25, slack 0) |
| Backing moves credit and never copies it | `back()` lowers the backer's limit by exactly what the borrower's rises ([SybilResistance.t.sol](https://github.com/scottonchain/microcredit-contract/blob/main/packages/foundry/test/SybilResistance.t.sol)) | On the live pool, Avery (92 USDC line) backed Brighton (25) with 50: their limits read 42 and 75 |
| Ten fresh accounts were refused every loan | A fresh account holds no credit: `requestLoan` reverts with `NoCredit`, `back` with `InsufficientCredit` | `./quickstart.sh try-borrow 5` from any new key prints `reverts with NoCredit` |
| A ring around one 25 USDC stake could borrow exactly 25 | Rex staked 25 and backed five members with 5 each; the five loans total 25 and a sixth reverts with `BorrowLimitExceeded` | `pool_health.py` shows 25 lent and 25 committed stake; the loans and backings are in TESTNET.md |
| Anyone can recompute | All of the above are view calls; the fuzzing suite (13 invariants, 332,800 calls, Sybil actors) is in [test/invariant](https://github.com/scottonchain/microcredit-contract/tree/main/packages/foundry/test/invariant) | `forge test` in the contract repo |

## Where the design falls short

The honest list is [CREDIT_INTEGRITY_ISSUES.md](https://github.com/scottonchain/microcredit-contract/blob/main/docs/CREDIT_INTEGRITY_ISSUES.md). The open items that matter most for the README's story:

- **Cold start.** A stranger with no history gets nothing until an issuer grants a line, someone backs them, or they stake. That is the price of the invariant, and the next problem to solve.
- **The issuer is the trust root.** Only the issuer (an oracle) and the owner create unsecured credit. The issuer's total is budgeted, but it does not yet put capital behind its lines (CI-17).
- **One price for every loan.** Stake-secured loans pay the same premium as unsecured ones (CI-18).
- **One hop.** Received backing cannot be passed on. That halves liquidity on simulated networks but keeps every loss on an account that chose the borrower (CI-20).

## For a lender: what is bounded, and what is not

A lender's loss is bounded by Theorem 2: realised plus potential loss never exceeds the credit lines issued plus the dues borrowers paid. Defaults are charged first to the backers' stake, then to their credit, then to a first-loss reserve, and only then to lenders. What is not bounded is the issuer's judgement: if it grants lines to bad borrowers, lenders bear what the reserve does not. That is why the issuer's budget and policy, not the pool's code, decide whether a stranger's loan is worth funding.

## Two commands

```bash
git clone https://github.com/scottonchain/microcredit-agent-testbed && cd microcredit-agent-testbed
python3 metrics/pool_health.py          # credit-integrity check and pool state, read from chain
PRIVATE_KEY=0x<any throwaway key> ./quickstart.sh try-borrow 5   # a fresh account: reverts with NoCredit
```

Both need Foundry's `cast` (https://book.getfoundry.sh).
