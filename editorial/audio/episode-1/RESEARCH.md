# Production research

Retrieved 2026-10-08, 20:13-20:14 UTC. Primary sources only. This is guidance, not evidence that an episode has been rendered.

## Dialogue

[ElevenLabs' dialogue documentation](https://elevenlabs.io/docs/overview/capabilities/text-to-dialogue) assigns a voice ID to each turn and documents delivery tags, including laughter, for its expressive dialogue models. It warns that results vary. These controls are engine-specific: do not send bracketed laughter instructions to an engine that might speak them literally. Fix the two IDs, model version and settings after an audition; keep those for future episodes. The current production route has not identified a usable speech engine, so no tested voice IDs or supported laughter controls are claimed.

Use short alternating turns and ordinary punctuation. Leave a small pause between replies. Do not overlap factual sentences. Two optional short chuckles fit the jokes after "Very economical with the word yes" and "Not accepted yet"; include only if the chosen engine produces them naturally. Pronunciation guide if later scripts use these terms: USDC as the four letters; Anvil as "AN-vil"; Base Sepolia as "Base seh-POH-lee-uh"; escrow as "ESS-kroh". These are editorial pronunciations, not engine-verified results. This script avoids most technical terms and explains escrow.

## Engagement

[Spotify's scripting guide](https://creators.spotify.com/resources/create/how-to-write-podcast-scripts) recommends a planned introduction, main point, transitions and ending, and balanced speaking opportunities for co-hosts. Its [episode-description guide](https://creators.spotify.com/resources/create/podcast-episode-descriptions) emphasizes the hook. Apply those ideas as a short disclosure and joke, one disagreement that matters, an example, then a concrete question. The title is "Show me the receipt." The shareable line is "A loan needs to earn its place."

The 3:05-3:45 target is the project's editorial choice, not a proven optimum. Test it using traced listener responses; static-host plays are not available. Do not represent author advice as causal research proving engagement.

## Disclosure and distribution

[Apple's content guidelines, section 1.11](https://podcasters.apple.com/support/891-content-and-subscription-guidelines) require prominent disclosure of AI-generated content in audio and show/episode metadata. The opening and supporting text identify synthetic voices and AI authorship. No real person's voice is cloned.

[Apple's audio requirements](https://podcasters.apple.com/support/893-audio-requirements) accept MP3 or AAC for RSS, with a recommended mono range of 64-128 kbps at 44.1/48 kHz. Use the brief's upper limit: 64 kbps mono at 48 kHz. Target -16 LUFS, true peak below -1 dBTP; this package uses -1.5 dBTP for encoding headroom. Measure the encoded result.

[RSS requirements](https://podcasters.apple.com/support/823-podcast-requirements): public RSS, stable GUID, unique enclosure URL with byte length and MIME type, working HEAD and range requests. [Cover requirements](https://podcasters.apple.com/support/5514-show-cover-template): square opaque PNG/JPG, 1400-3000 pixels through RSS, 3000 preferred. Existing cover/player/feed are Claude's responsibility. An empty feed is infrastructure, not a published episode. Directory submission and live playback have not been verified by this research.
