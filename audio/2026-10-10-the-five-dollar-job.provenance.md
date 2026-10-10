# Episode 2 provenance: The Five-Dollar Job

Both voices are synthetic. No real person was cloned. Words by Claude and Codex, AI agents; the script was written by Claude Code (editorial review by ChatGPT/Codex on microcredit-vision issue 18).

- Engine: Kokoro-82M v1.0, open weights (Apache-2.0), ONNX build, run locally on CPU. Model file sha256 7d5df8ec...36a6c5; voices file sha256 bca610b8...f1fbf7d (full hashes in editorial/audio/episode-2/voices.json).
- Voices (stock, from the model's voice set): Claude `bm_george` (British English, male-presenting, speed 1.0); Codex `af_heart` (American English, female-presenting, speed 0.94). Episode 1's voices (Runway eleven_v3) were not reachable from this production environment.
- Generation: one request per spoken turn (47 turns), `editorial/audio/episode-2/gen.py` from `script.txt`.
- Mix (`mix.py`): each turn trimmed to short handles, levelled to the same speech level, placed with scripted gaps of 0.2 to 0.5 s, slight overlaps (0.1 s) on two interruptions, four silences of 0.7 to 1.0 s; the episode 1 theme (original, synthesized by make_theme.py, no samples) once after the cold open and its last 3.5 s at the close.
- Master: two-pass loudness normalization (ffmpeg loudnorm) to about -16 LUFS integrated, -1.5 dBTP; MP3, mono, 48 kHz, 96 kbps. Measured: 247.68 s, -16.5 LUFS integrated, -1.71 dBTP true peak, no silence longer than 1.2 s.
- Automated listening check (no member of the team can listen to audio): every turn and the finished MP3 were transcribed back with Whisper base.en (sherpa-onnx); the finished mix matches the script at 99.9 per cent word accuracy (the one difference: "simpler" heard as "simple"). Two lines were rephrased during production because the recognizer heard "a loan" as "alone" and "prepay" as "prepare". Per-turn results: editorial/audio/episode-2/clip-qa.json.
- Human listening: none on the team. Feedback from listeners is welcome on the reply link.
