# Episode 2 production package: The Five-Dollar Job

Review branch for microcredit-vision issue 18. Listen: `audio/2026-10-10-the-five-dollar-job.mp3` (4:08). Captions: `.vtt` beside it. Post draft (staged, not published): `editorial/2026-10-10-the-five-dollar-job.md`. Cover: `images/the-five-dollar-job.svg` (16:9; PNG preview here).

Reproduce: install `kokoro-onnx`, `soundfile`, `sherpa-onnx`; put the Kokoro v1.0 model and voices files (hashes in voices.json) in `models/`; then `python3 gen.py` (one clip per turn), `python3 mix.py`, master with ffmpeg loudnorm to -16 LUFS / -1.5 dBTP (two-pass, as in the provenance), `python3 qa.py` and `python3 qa_mix.py` for the speech-recognition round trip. Edit `script.txt` and regenerate only the changed turns with `python3 gen.py <turn numbers>`.
