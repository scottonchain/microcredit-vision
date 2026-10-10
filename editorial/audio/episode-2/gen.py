"""Generate each spoken turn of script.txt with Kokoro (stock voices), as 24 kHz mono WAV in clips/."""
import sys, os, re, json, soundfile as sf
from kokoro_onnx import Kokoro
VOICES = {"CLAUDE": ("bm_george", 1.0), "CODEX": ("af_heart", 0.94)}
k = Kokoro("models/kokoro-v1.0.onnx", "models/voices-v1.0.bin")
only = set(sys.argv[1:])
os.makedirs("clips", exist_ok=True)
n = 0; meta = []
for line in open("script.txt"):
    line = line.rstrip("\n")
    if not line or line.startswith("#") or line.startswith("["):
        continue
    who, gap, text = line.split("|", 2); n += 1
    path = f"clips/{n:03d}-{who.lower()}.wav"
    meta.append({"n": n, "speaker": who, "gap_ms": int(gap), "text": text, "file": path})
    if only and str(n) not in only and os.path.exists(path):
        continue
    voice, speed = VOICES[who]
    samples, sr = k.create(text, voice=voice, speed=speed, lang="en-gb" if who == "CLAUDE" else "en-us")
    sf.write(path, samples, sr)
json.dump(meta, open("clips/meta.json", "w"), indent=1)
print("turns", n)
