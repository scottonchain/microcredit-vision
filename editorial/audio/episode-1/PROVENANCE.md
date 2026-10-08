# Episode provenance

Both voices are synthetic. No real person was cloned.

Speech production record:

```json
{
  "engine": "Runway connected speech generation",
  "model_version": "eleven_v3",
  "generated_at": "2026-10-08T20:24:30Z/2026-10-08T20:27:02Z",
  "settings": {
    "speed": 1,
    "languageCode": "en",
    "speech_text": "episode.json; verbatim per turn",
    "delivery_tags": "none",
    "postprocessing": "outer quiet trimmed with 100ms leading and 150ms trailing handles; 180ms turn gaps"
  },
  "Claude": {
    "id": "onwK4e9ZLuTAKqWW03F9",
    "preset": "Tom",
    "accent": "British English",
    "presentation": "male"
  },
  "Codex": {
    "id": "XrExE9yKIg1WjnnlVkGX",
    "preset": "Niki",
    "accent": "American English",
    "presentation": "female"
  },
  "rights_basis": "Stock presets supplied through Runway, no person-specific clone requested. Runway Usage rights: https://help.runwayml.com/hc/en-us/articles/18927776141715-Usage-rights (checked 2026-10-08). Original theme synthesized by make_theme.py; no samples.",
  "auditioned": false,
  "cloned_real_person": false,
  "listening_review": "Pending: current Codex session has no audio listening or transcription tool. Candidate for Claude review; no listening acceptance asserted."
}
```

MP3 SHA-256: `79ae225dea73402840c2f1e9e7a9462ccb9a2076af402c18907ea9df0c7d7597`

ffprobe duration: 192.720000 seconds.

Mono MP3, 48 kHz, 64 kbps. Two-pass loudness target -16 LUFS, -1.5 dBTP, followed by 0.5 dB codec headroom. Theme: original additive synthesis in make_theme.py, no samples. Captions use measured per-turn recording boundaries. Final listening, loudness and transcript-match checks must be recorded separately.

Measured encoded master: -16.99 LUFS integrated, -1.70 dBTP true peak, loudness range 3.90 LU. The input_* fields in MASTER_QA.json are the measured delivered file; output_* fields are a hypothetical second normalization. All 23 clips decoded successfully. Listening and spoken-transcript match are pending Claude review.
