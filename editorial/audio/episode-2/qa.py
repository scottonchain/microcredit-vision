"""Objective per-clip QA (no agent can listen): ASR round trip with Whisper base.en, word error vs the script,
duration and speaking rate, leading/trailing silence, peak, clipping. Prints the worst clips."""
import json, re, sys, wave, numpy as np, soundfile as sf, sherpa_onnx
M = "models/sherpa-onnx-whisper-base.en/base.en-"
rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=M+"encoder.int8.onnx", decoder=M+"decoder.int8.onnx", tokens=M+"tokens.txt", num_threads=4)
NUM = {"5": "five", "20": "twenty", "40": "forty", "1": "one", "2": "two", "3": "three"}
def norm(s):
    s = s.lower().replace("—", " ")
    s = re.sub(r"\$(\d+)", lambda m: NUM.get(m.group(1), m.group(1)) + " dollars", s)
    s = re.sub(r"\b(\d+)\b", lambda m: NUM.get(m.group(1), m.group(1)), s)
    return re.sub(r"[^a-z0-9' ]", " ", s).split()
def wer(ref, hyp):
    d = list(range(len(hyp)+1))
    for i, r in enumerate(ref, 1):
        prev, d[0] = d[0], i
        for j, h in enumerate(hyp, 1):
            prev, d[j] = d[j], min(d[j]+1, d[j-1]+1, prev+(r != h))
    return d[len(hyp)] / max(1, len(ref))
meta = json.load(open("clips/meta.json")); out = []
for m in meta:
    x, sr = sf.read(m["file"], dtype="float32")
    s = rec.create_stream(); s.accept_waveform(sr, x); rec.decode_stream(s)
    hyp = s.result.text.strip()
    a = np.abs(x); thr = 0.01 * a.max()
    idx = np.where(a > thr)[0]
    lead = idx[0]/sr if len(idx) else 0; trail = (len(x)-idx[-1])/sr if len(idx) else 0
    dur = len(x)/sr; words = len(m["text"].split())
    r = dict(n=m["n"], who=m["speaker"], dur=round(dur,2), wps=round(words/dur,2), wer=round(wer(norm(m["text"]), norm(hyp)),2),
             peak=round(float(a.max()),3), lead=round(lead,2), trail=round(trail,2), hyp=hyp, ref=m["text"])
    out.append(r)
json.dump(out, open("clips/qa.json","w"), indent=1)
bad = [r for r in out if r["wer"] > 0.15 or r["wps"] > 3.6 or r["wps"] < 1.6 or r["peak"] > 0.99]
print("clips", len(out), "mean WER", round(sum(r["wer"] for r in out)/len(out),3), "flagged", len(bad))
for r in sorted(out, key=lambda r: -r["wer"])[:12]:
    print(r["n"], r["who"], "wer", r["wer"], "wps", r["wps"], "|", r["ref"][:70], "||", r["hyp"][:70])
