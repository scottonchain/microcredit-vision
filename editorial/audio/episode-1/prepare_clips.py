import json, subprocess, wave
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
SR=48000
receipts=[]
for i in range(1,24):
 p=ROOT/'clips'/f'{i:03d}.mp3'
 r=subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','f32le','-ac','1','-ar',str(SR),'-'],check=True,capture_output=True)
 x=np.frombuffer(r.stdout,dtype='<f4').copy()
 # Detect only outer quiet regions; keep generous handles around phonemes.
 frame=480
 rms=np.array([np.sqrt(np.mean(x[j:j+frame]**2)) for j in range(0,len(x),frame)])
 active=np.flatnonzero(rms>10**(-48/20))
 a=max(0,int(active[0]*frame)-4800); b=min(len(x),int((active[-1]+1)*frame)+7200)
 y=x[a:b]
 out=ROOT/'clips'/f'{i:03d}.wav'
 with wave.open(str(out),'wb') as w:
  w.setparams((1,2,SR,0,'NONE','not compressed'));w.writeframes(np.rint(np.clip(y,-1,1)*32767).astype('<i2').tobytes())
 receipts.append({'turn':i,'source_seconds':len(x)/SR,'trim_start':a/SR,'trim_end':(len(x)-b)/SR,'seconds':len(y)/SR,'peak':float(max(abs(y)))})
(ROOT/'clip-checks.json').write_text(json.dumps(receipts,indent=2)+'\n')
print(json.dumps({'clips':len(receipts),'speech_seconds':sum(r['seconds'] for r in receipts),'assembled_estimate':6+22*.18+sum(r['seconds'] for r in receipts)}))
