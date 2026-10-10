"""Mix the per-turn clips into the episode: trim each clip to short handles, level each turn, place turns with the
scripted gaps (negative = slight overlap for an interruption), insert the theme at [THEME] and its tail at [OUTRO],
write a 48 kHz mono WAV plus a cue list for the captions."""
import json, numpy as np, soundfile as sf, subprocess
SR = 48000
def load(path):
    x, sr = sf.read(path, dtype="float32")
    if x.ndim > 1: x = x.mean(axis=1)
    if sr != SR:
        n = int(len(x) * SR / sr); x = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype("float32")
    return x
def trim(x, lead=0.05, tail=0.12):
    a = np.abs(x); thr = 0.012 * a.max(); idx = np.where(a > thr)[0]
    s = max(0, idx[0] - int(lead * SR)); e = min(len(x), idx[-1] + int(tail * SR))
    y = x[s:e].copy(); f = int(0.008 * SR); y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f); return y
def level(x, target_db=-20.0):
    a = np.abs(x); act = x[a > 0.02 * a.max()]; rms = np.sqrt(np.mean(act ** 2)) if len(act) else 1e-6
    return x * (10 ** (target_db / 20) / rms)
meta = {m["n"]: m for m in json.load(open("clips/meta.json"))}
theme = load("theme.wav"); theme = theme / np.abs(theme).max() * 10 ** (-14 / 20)
out = np.zeros(SR * 400, dtype="float32"); t = int(0.4 * SR); cues = []; n = 0
def put(x, at):
    out[at:at + len(x)] += x
for line in open("script.txt"):
    line = line.rstrip("\n")
    if not line or line.startswith("#"): continue
    if line.startswith("[PAUSE"):
        t += int(int(line.split()[1].rstrip("]")) * SR / 1000); continue
    if line == "[THEME]":
        t += int(0.25 * SR); put(theme, t); t += len(theme) - int(0.6 * SR); continue
    if line == "[OUTRO]":
        tail = theme[-int(3.5 * SR):].copy(); f = int(0.05 * SR); tail[:f] *= np.linspace(0, 1, f)
        t += int(0.5 * SR); put(tail, t); t += len(tail); continue
    who, gap, text = line.split("|", 2); n += 1
    x = level(trim(load(meta[n]["file"])))
    t = max(0, t + int(int(gap) * SR / 1000))
    put(x, t); cues.append({"n": n, "speaker": who, "start": t / SR, "end": (t + len(x)) / SR, "text": text}); t += len(x)
out = out[:t + int(0.3 * SR)]
sf.write("mix.wav", out, SR, subtype="PCM_24")
json.dump(cues, open("cues.json", "w"), indent=1)
print("raw mix seconds", round(len(out) / SR, 2), "turns", n)
