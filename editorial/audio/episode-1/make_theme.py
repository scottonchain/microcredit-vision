#!/usr/bin/env python3
"""Original six-second call-and-response motif; no samples or borrowed tune."""
import json
from pathlib import Path
import subprocess
import wave
import numpy as np

ROOT = Path(__file__).resolve().parent
SR = 48000


def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True)


def normalize(src, dest):
    first = run(['ffmpeg','-hide_banner','-i',str(src),'-af',
                 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'])
    stats = json.loads(first.stderr[first.stderr.rfind('{'):])
    filt = ('loudnorm=I=-16:TP=-1.5:LRA=11:linear=true:measured_I='+stats['input_i']+
            ':measured_TP='+stats['input_tp']+':measured_LRA='+stats['input_lra']+
            ':measured_thresh='+stats['input_thresh']+':offset='+stats['target_offset'])
    run(['ffmpeg','-y','-hide_banner','-i',str(src),'-af',filt,'-ar',str(SR),
         '-ac','1','-c:a','pcm_s16le',str(dest)])


def main():
    audio = np.zeros(6*SR, dtype=np.float64)
    # Two timbres trade phrases, then meet on C and G. MIDI note, onset, duration, timbre.
    notes = [(60,0.00,.48,0),(67,.42,.45,0),(64,.88,.63,0),
             (74,1.65,.36,1),(69,2.04,.43,1),(67,2.50,.70,1),
             (64,3.38,.35,0),(65,3.72,.38,1),(67,4.10,.48,0),
             (60,4.62,1.35,0),(67,4.62,1.35,1)]
    for midi, start, length, voice in notes:
        n = round(length*SR)
        t = np.arange(n)/SR
        f = 440*2**((midi-69)/12)
        attack = np.minimum(t/.012,1)
        release = np.minimum((length-t)/.11,1)
        envelope = attack*release*np.exp(-t/(.34 if voice == 0 else .26))
        tone = np.sin(2*np.pi*f*t)
        tone += (.24 if voice == 0 else .12)*np.sin(2*np.pi*2*f*t)
        tone += (.08 if voice == 0 else .20)*np.sin(2*np.pi*3*f*t)
        i = round(start*SR)
        audio[i:i+n] += .17*envelope*tone
    raw = ROOT/'theme-raw.wav'
    with wave.open(str(raw),'wb') as w:
        w.setparams((1,2,SR,0,'NONE','not compressed'))
        w.writeframes(np.rint(np.clip(audio,-1,1)*32767).astype('<i2').tobytes())
    normalize(raw,ROOT/'theme.wav')
    raw.unlink()
    run(['ffmpeg','-y','-hide_banner','-i',str(ROOT/'theme.wav'),'-ac','1',
         '-ar',str(SR),'-c:a','libmp3lame','-b:a','64k','-map_metadata','-1',
         '-metadata','title=Two Agents, No Collateral - Theme',
         '-metadata','artist=Codex (AI agent)',str(ROOT/'theme.mp3')])
    print('Generated theme.wav and theme.mp3; six-second original motif.')


if __name__ == '__main__':
    main()
