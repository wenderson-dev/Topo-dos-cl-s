import json,sys
segs=[json.loads(l) for l in open("transcript.jsonl")]
for arg in sys.argv[1:]:
    a,b=arg.split("-"); f=lambda x:int(x.split(":")[0])*60+int(x.split(":")[1]); a,b=f(a),f(b)
    print("=====",arg)
    for s in segs:
        if s["e"]>a-12 and s["s"]<b+12: print(f'{s["s"]:.1f}-{s["e"]:.1f}{s["t"]}')
