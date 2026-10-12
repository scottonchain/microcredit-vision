import json,urllib.request,time,random
EPS=["https://base.gateway.tenderly.co","https://gateway.tenderly.co/public/base","https://base.api.pocket.network"]
H={"content-type":"application/json","user-agent":"Mozilla/5.0 (hermes-research)"}
def post(u,body,to=90):
    return json.load(urllib.request.urlopen(urllib.request.Request(u,json.dumps(body).encode(),H),timeout=to))
def rpc(m,p,tries=8,eps=None):
    eps=eps or EPS; last=None
    for i in range(tries):
        u=eps[(i+random.randrange(len(eps)))%len(eps)]
        try:
            d=post(u,{"jsonrpc":"2.0","id":1,"method":m,"params":p})
            if "result" in d: return d["result"]
            last=d.get("error")
        except Exception as e: last=str(e)
        time.sleep(2+3*i)
    raise RuntimeError(f"{m} failed: {last}")
def batch(calls,tries=6):
    last=None
    for i in range(tries):
        u=EPS[(i+random.randrange(len(EPS)))%len(EPS)]
        try:
            d=post(u,[{"jsonrpc":"2.0","id":k,"method":m,"params":p} for k,(m,p) in enumerate(calls)])
            if isinstance(d,list) and all("result" in x for x in d):
                return [x["result"] for x in sorted(d,key=lambda x:x["id"])]
            last=str(d)[:200]
        except Exception as e: last=str(e)
        time.sleep(2+3*i)
    raise RuntimeError("batch failed: "+str(last))
def blk_ts(n): return int(rpc("eth_getBlockByNumber",[hex(n),False])["timestamp"],16)
def first_block_at(ts,lo=1,hi=None):
    hi=hi or int(rpc("eth_blockNumber",[]),16)
    while lo<hi:
        mid=(lo+hi)//2
        if blk_ts(mid)<ts: lo=mid+1
        else: hi=mid
    return lo
