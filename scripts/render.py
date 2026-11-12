import json, sys, subprocess, os
V=os.path.dirname(os.path.abspath(__file__))+"/vod"
segs=[json.loads(l) for l in open(V+"/transcript.jsonl")]
words=[(w[0],w[1],w[2].strip()) for s in segs for w in s["w"] if w[2].strip()]
U=open(V+"/url1080.txt").read().strip()
OUT=os.path.dirname(V)+"/cortes"; os.makedirs(OUT,exist_ok=True)
def ts(t):
    t=max(t,0); h=int(t//3600); m=int(t%3600//60); s=t%60
    return f"{h}:{m:02d}:{s:05.2f}"
TITLES=dict(l.strip().split("|",1) for l in open(V+"/titles.txt"))
def ass(a,b,y,n=None):
    ws=[w for w in words if w[0]>=a-0.05 and w[1]<=b+0.3]
    chunks=[]; cur=[]
    for w in ws:
        if cur and (len(cur)>=3 or len(" ".join(x[2] for x in cur+[w]))>20 or w[0]-cur[-1][1]>0.6):
            chunks.append(cur); cur=[]
        cur.append(w)
    if cur: chunks.append(cur)
    lines=[]
    for i,c in enumerate(chunks):
        st=c[0][0]-a; en=c[-1][1]-a+0.25
        if i+1<len(chunks): en=min(en+0.4, chunks[i+1][0][0]-a)
        en=min(en,b-a)
        txt=" ".join(x[2] for x in c).upper().replace("{","").replace("}","")
        lines.append(f"Dialogue: 0,{ts(st)},{ts(en)},S,,0,0,0,,{{\\pos(540,{y})}}{txt}")
    head=f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: T,Inter Black,66,&H00000000,&H00000000,&H00FFFFFF,&H00000000,1,0,0,0,100,100,0,0,3,14,0,8,90,90,110,1
Style: S,Inter Black,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,7,3,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    if n: lines.insert(0,f"Dialogue: 1,{ts(0)},{ts(b-a)},T,,0,0,0,,{TITLES[n]}")
    return head+"\n".join(lines)+"\n"
def render(n,a,b,name):
    a=float(a); b=float(b); game=int(n)>=11
    y=770 if game else 1560
    af=f"{OUT}/{n}.ass"; open(af,"w").write(ass(a,b,y,n))
    if game:
        vf=(f"[0:v]split[c][g];[c]crop=446:318:1471:236,scale=1080:770[top];"
            f"[g]crop=1014:1080:453:0,scale=1080:1150[bot];[top][bot]vstack,fps=30,ass={af}[v]")
    else:
        vf=f"[0:v]crop=608:1080:716:0,scale=1080:1920:flags=lanczos,fps=30,ass={af}[v]"
    out=f"{OUT}/corte-{n}-{name}.mp4"
    env=dict(os.environ, http_proxy=os.environ["HTTPS_PROXY"])
    cmd=["ffmpeg","-nostdin","-loglevel","error","-y"]+(["-t","3"] if os.environ.get("TEST") else [])+["-ss",str(a),"-i",U,"-t",str(b-a),
         "-filter_complex",vf,"-map","[v]","-map","0:a","-c:v","libx264","-preset","medium","-crf","23",
         "-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-af","loudnorm=I=-14:TP=-1.5:LRA=11","-movflags","+faststart",out]
    r=subprocess.run(cmd,env=env,capture_output=True,text=True)
    print(n, "OK" if r.returncode==0 else r.stderr[-500:], flush=True)
sel=sys.argv[1:]
for l in open(V+"/clips.txt"):
    n,a,b,name=l.strip().split("|")
    if not sel or n in sel: render(n,a,b,name)
