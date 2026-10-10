"""Round-trip the finished MP3: decode each caption cue's span from the final file and compare it with the script."""
import json, subprocess, numpy as np, sherpa_onnx, re, sys
sys.argv = ["qa.py"]; exec(open("qa.py").read().split("meta = json.load")[0])  # reuse recognizer, norm, wer
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", "episode.mp3", "-f", "f32le", "-ac", "1", "-ar", "16000", "-"], capture_output=True).stdout
x = np.frombuffer(pcm, dtype="float32"); SR = 16000
cues = json.load(open("cues.json")); worst = []
for c in cues:
    seg = x[int(max(0, c["start"] - 0.05) * SR): int((c["end"] + 0.05) * SR)]
    s = rec.create_stream(); s.accept_waveform(SR, seg); rec.decode_stream(s)
    worst.append((wer(norm(c["text"]), norm(s.result.text)), c["n"], s.result.text.strip()))
worst.sort(reverse=True)
print("final-mix mean WER", round(sum(w[0] for w in worst) / len(worst), 3))
for w in worst[:5]: print(w)
print("peak dBFS", round(20 * np.log10(np.abs(x).max()), 2))
