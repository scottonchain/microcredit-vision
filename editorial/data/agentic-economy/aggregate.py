#!/usr/bin/env python3
"""Aggregate raw.jsonl (sampled windows) into per-day estimates. All per-day counts are ESTIMATES scaled from sampled blocks:
 settlements_est = mean AU events per sampled block * 43200 blocks/day (mean over that day's windows).
Unique payers/payees/median ticket are SAMPLE statistics (not scaled): unique_*_sampled = distinct addresses seen in that day's sampled blocks.
self_payment_share = share of sampled settlements where payer == payee.
facilitator_share (tx.to == a single contract) is output in top_payees / facilitators table."""
import json, csv, statistics, collections, datetime as dt, sys
R = json.load(open("range.json")); T0 = R["t0"]
days = collections.defaultdict(list)
for line in open("raw.jsonl"):
    r = json.loads(line); days[r["d"]].append(r)
rows = []
last30 = collections.Counter(); last30_n = 0
tx_to = collections.Counter(); tx_from = collections.Counter()
last30_start = max(days) - 29 if days else 0
for d in sorted(days):
    ws = days[d]
    blocks = sum(w["wb"] for w in ws)
    ev = [e for w in ws for e in w["ev"] if e[2] is not None]
    n = sum(w["n_au"] for w in ws)
    rate = n / blocks
    payers = {e[1] for e in ev}; payees = {e[2] for e in ev}
    vals = [e[3] for e in ev]
    selfp = sum(1 for e in ev if e[1] == e[2])
    date = (dt.datetime.fromtimestamp(T0, dt.timezone.utc) + dt.timedelta(days=d)).date().isoformat()
    rows.append([date, round(rate * 43200), len(ws), blocks, n, len(payers), len(payees),
                 round(sum(vals) / 1e6 / blocks * 43200, 2) if blocks else 0,
                 round(sum(v for v in vals if v <= 10_000_000_000) / 1e6 / blocks * 43200, 2) if blocks else 0,
                 round(statistics.median(vals) / 1e6, 6) if vals else "",
                 round(selfp / len(ev), 4) if ev else ""])
    if d >= last30_start:
        for e in ev: last30[e[2]] += 1
        last30_n += len(ev)
    for w in ws:
        for h, (f, t, sel) in w["meta"].items():
            tx_to[t] += 1; tx_from[f] += 1
with open("x402_daily.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["date", "settlements_est", "sampled_windows", "sampled_blocks", "sampled_settlements",
                "unique_payers_sampled", "unique_payees_sampled", "usdc_volume_est", "usdc_volume_est_excl_tickets_over_10k", "median_ticket_usdc", "self_payment_share"])
    w.writerows(rows)
with open("top_payees.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["rank", "payee_address", "sampled_settlements_last30d", "share_of_sampled_settlements"])
    for i, (a, c) in enumerate(last30.most_common(20), 1):
        w.writerow([i, a, c, round(c / last30_n, 4)])
with open("tx_destinations.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["kind", "address", "txs_in_sample"])
    for a, c in tx_to.most_common(25): w.writerow(["tx.to", a, c])
    for a, c in tx_from.most_common(25): w.writerow(["tx.from", a, c])
sel=collections.Counter(); seld=collections.defaultdict(collections.Counter)
for d in days:
    for w in days[d]:
        for h,(f,t,x) in w["meta"].items(): sel[x]+=1
with open("selectors.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["tx_input_selector","txs_in_sample","share"])
    tot=sum(sel.values())
    for a,c in sel.most_common(10): w.writerow([a,c,round(c/tot,4)])
print(len(rows), "days;", last30_n, "settlements in last-30d sample")

with open("windows.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["day_index","window","start_block","blocks","authorization_used_events","txs","txs_with_sender_lookup"])
    for d in sorted(days):
        for x in days[d]: w.writerow([d,x["w"],x["b"],x["wb"],x["n_au"],x["n_tx"],len(x["meta"])])
