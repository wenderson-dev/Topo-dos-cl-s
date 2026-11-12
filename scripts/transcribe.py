import sys, json, time
from faster_whisper import WhisperModel
m=WhisperModel(sys.argv[3], device="cpu", compute_type="int8", cpu_threads=4)
import wave, numpy as np
w=wave.open(sys.argv[1]); audio=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
segs,info=m.transcribe(audio, language="pt", beam_size=1, vad_filter=True, word_timestamps=True, condition_on_previous_text=False)
with open(sys.argv[2],"w") as f:
    for s in segs:
        f.write(json.dumps({"s":s.start,"e":s.end,"t":s.text,"w":[(w.start,w.end,w.word) for w in s.words]},ensure_ascii=False)+"\n"); f.flush()
print("done")
