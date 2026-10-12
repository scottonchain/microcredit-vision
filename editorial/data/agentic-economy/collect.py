#!/usr/bin/env python3
"""Sample Base mainnet USDC transferWithAuthorization settlements (AuthorizationUsed events).
For each UTC day 2025-05-01..2026-10-07, read NW windows of WB consecutive blocks, evenly spaced across the day.
Per window: eth_getLogs(USDC, topics[0] in [AuthorizationUsed, Transfer]); pair each AuthorizationUsed with the next
Transfer log in the same tx whose `from` == authorizer (FiatTokenV2 emits AuthorizationUsed then Transfer).
Look up tx.from / tx.to for up to TXCAP AU transactions per window (random subset, fixed seed).
Output: raw.jsonl, one line per window. Resumable."""
import json, os, sys, random, time, threading
from concurrent.futures import ThreadPoolExecutor
from common import rpc, batch, blk_ts

USDC = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
AU = "0x98de503528ee59b575ef0c0a2576a82497bfc029a5685b209e9ec333479b10a5"
TR = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
R = json.load(open("range.json"))
B0, B1, T0 = R["b0"], R["b1"], R["t0"]  # first block of 2025-05-01 UTC, first block of 2026-10-08 UTC
NW = int(os.environ.get("NW", 4)); WB = int(os.environ.get("WB", 40)); TXCAP = int(os.environ.get("TXCAP", 120))
OUT = "raw.jsonl"
lock = threading.Lock()

# day start blocks: exact via 2 s block time estimate refined by one timestamp read per day
def day_start(d):
    est = B0 + d * 43200
    ts = blk_ts(est)
    want = T0 + d * 86400
    return est + (want - ts) // 2

def work(d, w, ds):
    b = ds + int(43200 * (w + 0.5) / NW) - WB // 2
    for attempt in range(3):
        try:
            lg = rpc("eth_getLogs", [{"address": USDC, "topics": [[AU, TR]], "fromBlock": hex(b), "toBlock": hex(b + WB - 1)}])
            break
        except Exception as e:
            err = str(e)
            if "more than 20000" in err and attempt == 0:
                lg = None; break
            time.sleep(2)
    else:
        return None
    if lg is None:  # too many logs: halve the window deterministically
        lg = []
        h = WB // 2
        for bb in (b, b + h):
            lg += rpc("eth_getLogs", [{"address": USDC, "topics": [[AU, TR]], "fromBlock": hex(bb), "toBlock": hex(bb + h - 1)}])
        eff = WB
    else:
        eff = WB
    ts0 = blk_ts(b)
    bytx = {}
    for l in lg:
        bytx.setdefault(l["transactionHash"], []).append(l)
    ev = []
    for h, ls in bytx.items():
        ls.sort(key=lambda x: int(x["logIndex"], 16))
        for i, l in enumerate(ls):
            if l["topics"][0] != AU: continue
            payer = "0x" + l["topics"][1][-40:]
            for t in ls[i + 1:]:
                if t["topics"][0] == TR and "0x" + t["topics"][1][-40:] == payer:
                    ev.append([h, payer, "0x" + t["topics"][2][-40:], int(t["data"], 16), int(l["blockNumber"], 16)])
                    break
            else:
                ev.append([h, payer, None, None, int(l["blockNumber"], 16)])
    # tx.from / tx.to for a random subset of AU txs
    txs = sorted({e[0] for e in ev})
    rnd = random.Random(f"{d}-{w}")
    sub = txs if len(txs) <= TXCAP else rnd.sample(txs, TXCAP)
    meta = {}
    for i in range(0, len(sub), 60):
        chunk = sub[i:i + 60]
        res = batch([("eth_getTransactionByHash", [h]) for h in chunk])
        for h, r in zip(chunk, res):
            if r: meta[h] = [r["from"].lower(), (r["to"] or "").lower(), r["input"][:10]]
    rec = {"d": d, "w": w, "b": b, "wb": eff, "ts": ts0, "n_au": len(ev), "n_tx": len(txs), "ev": ev, "meta": meta}
    with lock:
        with open(OUT, "a") as f: f.write(json.dumps(rec) + "\n")
    return True

def main():
    ndays = (B1 - B0 + 43199) // 43200
    done = set()
    if os.path.exists(OUT):
        for line in open(OUT):
            try: r = json.loads(line); done.add((r["d"], r["w"]))
            except Exception: pass
    jobs = []
    dstarts = {}
    def ds_of(d):
        if d not in dstarts: dstarts[d] = day_start(d)
        return dstarts[d]
    order = list(range(ndays))
    # interleave: all days at window 0 first so partial runs still cover the whole range
    for w in range(NW):
        for d in order:
            if (d, w) not in done: jobs.append((d, w))
    print("jobs", len(jobs), "ndays", ndays, flush=True)
    t = time.time(); cnt = 0; fail = 0
    def run(j):
        d, w = j
        try:
            return work(d, w, ds_of(d))
        except Exception as e:
            print("fail", j, str(e)[:100], flush=True); return None
    with ThreadPoolExecutor(int(os.environ.get("TH", 6))) as ex:
        for r in ex.map(run, jobs):
            cnt += 1; fail += (r is None)
            if cnt % 50 == 0: print(cnt, "fail", fail, round(time.time() - t), "s", flush=True)
    print("done", cnt, "fail", fail, flush=True)

if __name__ == "__main__":
    main()
