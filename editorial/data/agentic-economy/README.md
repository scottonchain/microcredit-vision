# Agentic onchain economy on Base: sampled USDC EIP-3009 settlements, 2025-05-01 to 2026-10-07

Prepared by Hermes (AI agent, hermes-agent-909) for the blog queue item `agentic-onchain-economy-growth`.
Read-only: public RPC `eth_getLogs`, `eth_getTransactionByHash`, `eth_getBlockByNumber`, `eth_getCode`. Nothing was spent or signed.
Read time: 2026-10-08, about 17:15Z to 19:00Z. Chain head at start: block 52,344,825.

## Read this first: what the numbers are and are not

1. **These are ESTIMATES from sampled blocks, not a full census.** A full scan would be about 155 million events by my estimate; the public RPCs allow at most 1,000 blocks per `eth_getLogs` and rate-limit hard. For each UTC day I read up to 4 windows of 40 consecutive blocks (160 of about 43,200 blocks, 0.37%), evenly spaced through the day. `settlements_est` = events per sampled block x 43,200. 9 days got 1 window, 47 got 2, 221 got 3, 248 got 4 (see `windows.csv`; `sampled_windows` per day). Daily figures are noisy, especially on bursty days. Smooth with a weekly or monthly mean before quoting.
2. **The series is NOT filtered to x402.** I counted every USDC (`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`, Base) `AuthorizationUsed` event paired with its `Transfer` (EIP-3009 `transferWithAuthorization` / `receiveWithAuthorization`). That is an upper bound for x402 settlements: x402's `exact` scheme on EVM settles this way, but any other gasless-USDC use of EIP-3009 is included too. I did not identify the facilitators' addresses (see "Facilitators" below), so I could not separate them. Do not call this series "x402 settlements" in print. Call it "USDC authorization-based transfers on Base, of which x402 is the main known driver". The file is named `x402_daily.csv` only because the requested name was that.
3. **Unique payers and payees are SAMPLE counts** (distinct addresses within the sampled blocks of that day). They are lower bounds on the true daily uniques and are not comparable between days with different numbers of windows.
4. **Volume is dominated by a few large tickets.** In the last-30-day sample, the top 1% of settlements carry 94% of USDC volume (largest single: 40,000 USDC). `usdc_volume_est` is therefore very noisy; `usdc_volume_est_excl_tickets_over_10k` drops tickets above 10,000 USDC from the numerator only. The median ticket (cents or fractions of a cent in most of the period) is the better "agentic micropayment" signal.
5. **Self-payment rule used:** payer address == payee address in the same settlement, nothing else. The "funded from one address within the window" test was NOT done (it needs a funding-trace pass I did not have time to run). So `self_payment_share` is a floor; it is under 2.1% on every one of the last 60 days (mean 0.29%). Same-operator wash traffic between different addresses would not show here.

## Headline readings (computed from `x402_daily.csv`; period means of the daily estimate)

| Period | mean settlements/day (est) | mean volume/day, USDC, tickets > 10k excluded (est) |
|---|---|---|
| 2025-05-01 to 2025-09-30 | 3,790 | 1,155,119 |
| 2025-10 | 119,886 | 1,568,941 |
| 2025-11 to 2025-12 | 1,803,643 | 1,305,267 |
| 2026-01 to 2026-03 | 185,289 | 825,723 |
| 2026-04 to 2026-06 | 171,427 | 713,746 |
| 2026-07 to 2026-09 | 238,259 | 743,435 |
| 2026-09-08 to 2026-10-07 | 95,997 | 1,081,466 |

Peak day in the sample: 2025-11-03 (about 4.4 million estimated events). The count rose about 500-fold from mid-2025 to the Nov 2025 peak, then fell by roughly an order of magnitude and has been at a lower plateau since January 2026, while the median ticket stayed at about one cent. So: very large growth in transaction COUNT in late 2025, followed by a sharp fall; no comparable growth in value moved. A careful claim is "event count spiked and then settled at a lower, still large level; dollar volume is flat to down". I did not investigate why the Nov 2025 spike happened; one candidate, not tested, is a few high-volume payees (the top-payee concentration below suggests this pattern now).

## Files

| File | What it is |
|---|---|
| `x402_daily.csv` | 525 daily rows. Columns: `date`, `settlements_est`, `sampled_windows`, `sampled_blocks`, `sampled_settlements` (raw count in sample), `unique_payers_sampled`, `unique_payees_sampled`, `usdc_volume_est`, `usdc_volume_est_excl_tickets_over_10k`, `median_ticket_usdc` (sample median), `self_payment_share` (sample share) |
| `top_payees.csv` | Top 20 payee addresses in the sample for the last 30 days (2026-09-08 to 2026-10-07; 8,552 sampled settlements), by sampled settlement count, with share of all sampled settlements. Addresses only. Top 1 = 20.6%, top 2 = 15.5%, top 3 = 8.3%; top 5 together = 52%. One contract's or operator's traffic is a large part of the total. I did not label any address. |
| `tx_destinations.csv` | For up to 120 randomly chosen settlement transactions per window (fixed seed), who sent the transaction (`tx.from`, the relayer/facilitator wallet) and what it called (`tx.to`). 66,633 transactions across all windows. Over half called USDC directly. |
| `selectors.csv` | Share of those transactions by 4-byte function selector. `0xe3ee160e` (50.3%) = `transferWithAuthorization(address,address,uint256,uint256,uint256,bytes32,uint8,bytes32,bytes32)`; `0xcf092995` (38.1%) = `transferWithAuthorization(address,address,uint256,uint256,uint256,bytes32,bytes)` (the `bytes signature` overload); `0x82ad56cb` (6.6%) = Multicall3 `aggregate3((address,bool,bytes)[])`. All three checked with `cast sig` in this run. |
| `windows.csv` | One row per sampled window: block range start, size, events, transactions. Lets anyone check coverage. |
| `collect.py`, `common.py`, `aggregate.py`, `range.json` | The scripts (below). |
| `agent_payments_other.csv` | NOT produced. See below. |

## Provenance per file

- **Data source:** JSON-RPC to public Base mainnet endpoints, round-robin: `https://base.gateway.tenderly.co`, `https://gateway.tenderly.co/public/base`, `https://base.api.pocket.network`. (Others tried and unusable: `mainnet.base.org` rate-limited; `base-rpc.publicnode.com` 403; `base.drpc.org` 10-block range cap; `1rpc.io` 50-block cap; BaseScan/Etherscan V2 API refused Base on the free tier.)
- **Contract:** USDC on Base `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`. The address is also listed in the x402 repo docs (`docs/core-concepts/network-and-token-support.mdx` at x402-foundation/x402 commit `7f2b2f1f77fa5317615735e3378a6fad41cccb4e`, read 2026-10-08). The event signature `AuthorizationUsed(address indexed authorizer, bytes32 indexed nonce)` = topic0 `0x98de503528ee59b575ef0c0a2576a82497bfc029a5685b209e9ec333479b10a5`; `Transfer` = `0xddf252ad...b3ef`. Each `AuthorizationUsed` is paired with the next `Transfer` in the same transaction whose `from` equals the authorizer; unpaired events are counted in `settlements_est` but excluded from payee/volume/ticket statistics.
- **Filters:** `eth_getLogs {address: USDC, topics: [[AuthorizationUsed, Transfer]], fromBlock, toBlock}` per 40-block window.
- **Block range:** 29,634,127 (first block of 2025-05-01 UTC) to 52,314,126 (last block of 2026-10-07 UTC). Day boundaries are found by binary search on block timestamps (`common.first_block_at`), then each day's start is refined from a block timestamp (2 s blocks). Window `w` of 4 is centred at `(w+0.5)/4` through the 43,200-block day.
- **Cross-check:** 3 randomly chosen windows were re-read from a second provider (`base.api.pocket.network` only); event counts matched in 3 of 3 (3, 2, 127 events).
- **Commands:** `python3 collect.py` (env `NW=4 WB=40 TXCAP=120 TH=2`; resumable; writes `raw.jsonl`), then `python3 aggregate.py` (reads `raw.jsonl` and `range.json`, writes all CSVs). `raw.jsonl` (115 MB, about 30 MB gzipped) is not committed; rerunning `collect.py` rebuilds it in roughly 2 hours at the public rate limits. The run had about 15% transient 429 failures that were retried by resuming; `raw.jsonl` is deduplicated on (day, window).
- **No dashboard comparison** column was added: I did not read any dashboard in this run, so there is no number to cite.

## Facilitators (not done)

The x402 repo lists facilitator and batch-settlement contract addresses in `contracts/evm/README.md` and `go/mechanisms/evm/constants.go` (for example `0x4020074e9df2ce1dee5a9c1b5c3f541d02a10003`, `0x4020806089470a89826cb9fb1f4059150b550004`, `0x4020425faf3b746c082c2f942b4e5159887b0005`, `0x402085c248eea27d92e8b30b2c58ed07f9e20001`, `0x4020a4f3b7b90cca423b9fabcc0ce57c6c240002`; `getCode` returned code for each; `0x402039b3d6e6bec5a02c2c9fd937ac17a6940002` has no code). I did not check whether any appear in `tx_destinations.csv` or as payees, and the hosted facilitators' relayer wallets (the `tx.from` values in `tx_destinations.csv`) are not attributed to any named facilitator: the top ten senders each account for about 1-4% of sampled transactions and I did not trace who runs them. The honest follow-up that would turn this into an x402-only series is to attribute `tx.from` relayers to named facilitators from their own docs and filter on them.

## `agent_payments_other.csv`

Not produced. I did not identify another agent-payment rail's contracts from its own documentation inside the time I allowed.

## Gaps and known weaknesses

- Sampling error is not quantified in the CSV. Rough guide: days with 1 to 2 windows (58 of 525) carry the most error. Daily rows on bursty days can be off by a factor of several.
- Not x402-only (above). Not attributed to facilitators (above). Self-payment is the narrow rule only.
- Top-payee shares are shares of the sample, not of the true population.
- No label on any payee. No claim is made about who operates any address.
- The reason for the late-2025 spike and later fall was not investigated.
