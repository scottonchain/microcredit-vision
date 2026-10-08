#!/usr/bin/env python3
"""Assemble actual per-turn WAV recordings, theme and time-aligned speaker cues.

No speech engine is called. Supply clips/001.wav ... clips/023.wav matching
episode.json, with leading/trailing silence trimmed, plus completed voices.json.
Writes no final episode if recordings, provenance or length requirements fail.
"""
import hashlib
import argparse
import json
import math
from pathlib import Path
import subprocess
import tempfile
import wave
import numpy as np
from make_theme import normalize

ROOT = Path(__file__).resolve().parent
SR = 48000


def run(args):
    return subprocess.run(args,check=True,capture_output=True,text=True)


def pcm(path):
    r = subprocess.run(['ffmpeg','-v','error','-i',str(path),'-f','f32le',
                        '-ac','1','-ar',str(SR),'-'],check=True,capture_output=True)
    return np.frombuffer(r.stdout,dtype='<f4').astype(np.float64)


def stamp(samples):
    ms = round(samples*1000/SR)
    hours, ms = divmod(ms,3600000)
    minutes, ms = divmod(ms,60000)
    seconds, ms = divmod(ms,1000)
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}.{ms:03d}'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage-unreviewed', action='store_true',
                        help='Assemble a review candidate; listening acceptance remains pending.')
    args = parser.parse_args()
    ep = json.loads((ROOT/'episode.json').read_text())
    voices = json.loads((ROOT/'voices.json').read_text())
    required = ['engine','model_version','generated_at','settings','Claude','Codex','rights_basis']
    for k in required:
        if not voices.get(k):
            raise SystemExit(f'Voice provenance incomplete: {k}')
    if not voices.get('auditioned') and not args.stage_unreviewed:
        raise SystemExit('Listening review pending; use --stage-unreviewed for a review candidate only.')
    if voices['Claude']['id'] == voices['Codex']['id']:
        raise SystemExit('Two distinct voice IDs are required')
    for speaker in ['Claude','Codex']:
        if not voices[speaker].get('id') or not voices[speaker].get('accent'):
            raise SystemExit(f'Voice identity incomplete: {speaker}')
    if voices.get('cloned_real_person',True):
        raise SystemExit('No real-person voice cloning is allowed')
    clips = []
    for i, turn in enumerate(ep['turns'],1):
        p = ROOT/'clips'/f'{i:03d}.wav'
        if not p.is_file():
            raise SystemExit(f'Missing speech recording: {p.name}')
        clip = pcm(p)
        if len(clip) < SR*.1 or not np.all(np.isfinite(clip)) or np.max(np.abs(clip)) < .001:
            raise SystemExit(f'Invalid/empty speech recording: {p.name}')
        clips.append(clip)
    theme = pcm(ROOT/'theme.wav')
    if not 5*SR <= len(theme) <= 8*SR:
        raise SystemExit('Theme must be 5 to 8 seconds')
    cursor = len(theme)-SR
    cues = []
    starts = []
    for i,clip in enumerate(clips):
        starts.append(cursor)
        cues.append((cursor,cursor+len(clip),ep['turns'][i]))
        cursor += len(clip)+round(.18*SR)
    speech_end = cues[-1][1]
    outro = theme[-round(3.5*SR):].copy()
    outro_start = speech_end-round(2.5*SR)
    end = max(speech_end,outro_start+len(outro))
    if not 180 <= end/SR <= 300:
        raise SystemExit(f'Length {end/SR:.3f}s outside hard 180-300s bounds; re-render pacing, do not pad.')
    mix = np.zeros(end)
    opening = theme.copy()
    opening[len(theme)-SR:] *= 10**(-18/20)
    mix[:len(opening)] += opening
    for start,clip in zip(starts,clips):
        mix[start:start+len(clip)] += clip
    duck = np.ones(len(outro))
    duck[:round(2.5*SR)] = 10**(-18/20)
    outro *= duck
    outro[:round(.06*SR)] *= np.linspace(0,1,round(.06*SR))
    mix[outro_start:outro_start+len(outro)] += outro
    # Preserve dynamics before final loudness normalization; no hard clipping.
    mix *= min(1,.95/max(np.max(np.abs(mix)),.001))
    with tempfile.TemporaryDirectory() as d:
        raw = Path(d)/'mixed.wav'
        normalized = Path(d)/'normalized.wav'
        with wave.open(str(raw),'wb') as w:
            w.setparams((1,2,SR,0,'NONE','not compressed'))
            w.writeframes(np.rint(mix*32767).astype('<i2').tobytes())
        normalize(raw,normalized)
        run(['ffmpeg','-y','-hide_banner','-i',str(normalized),'-ac','1','-ar',str(SR),
             '-af','volume=-0.5dB',
             '-c:a','libmp3lame','-b:a','64k','-map_metadata','-1',
             '-metadata','title='+ep['title'],'-metadata','artist=Claude and Codex (AI agents)',
             '-metadata','album='+ep['show'],str(ROOT/'episode.mp3')])
    info = json.loads(run(['ffprobe','-v','error','-show_format','-show_streams',
                          '-of','json',str(ROOT/'episode.mp3')]).stdout)
    duration = float(info['format']['duration'])
    if not 180 <= duration <= 300:
        (ROOT/'episode.mp3').unlink()
        raise SystemExit(f'Encoded duration fails hard bounds: {duration}')
    (ROOT/'ffprobe.json').write_text(json.dumps(info,indent=2)+'\n')
    vtt = ['WEBVTT','']
    for i,(a,b,turn) in enumerate(cues,1):
        vtt.extend([str(i),f'{stamp(a)} --> {stamp(b)}',
                    f'<v {turn["speaker"]}>{turn["text"]}',''])
    (ROOT/'episode.vtt').write_text('\n'.join(vtt)+'\n')
    sha = hashlib.sha256((ROOT/'episode.mp3').read_bytes()).hexdigest()
    (ROOT/'PROVENANCE.md').write_text(
        '# Episode provenance\n\nBoth voices are synthetic. No real person was cloned.\n\n'
        + 'Speech production record:\n\n```json\n'+json.dumps(voices,indent=2)+'\n```\n\n'
        + f'MP3 SHA-256: `{sha}`\n\nffprobe duration: {duration:.6f} seconds.\n\n'
        + 'Mono MP3, 48 kHz, 64 kbps. Two-pass loudness target -16 LUFS, -1.5 dBTP, followed by 0.5 dB codec headroom. '
        + 'Theme: original additive synthesis in make_theme.py, no samples. '
        + 'Captions use measured per-turn recording boundaries. '
        + 'Final listening, loudness and transcript-match checks must be recorded separately.\n')
    print(json.dumps({'duration':duration,'sha256':sha,'target_185_225_seconds':185<=duration<=225},indent=2))


if __name__ == '__main__':
    main()
