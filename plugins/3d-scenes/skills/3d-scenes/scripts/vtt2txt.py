import sys,re,os,glob,json
root=sys.argv[1]
for d in sorted(glob.glob(os.path.join(root,'*'))):
    if not os.path.isdir(d): continue
    id=os.path.basename(d)
    vt=[f for f in glob.glob(d+'/*.vtt')]
    pref=[f for f in vt if f.endswith('.en-orig.vtt')] or [f for f in vt if f.endswith('.en.vtt')] or [f for f in vt if '.ar' in f]
    if not pref: print('NO SUBS',id); continue
    f=pref[0]; lines=open(f,encoding='utf-8').read().split('\n')
    out=[];last='';cur_t=None;buf=[];bucket=-1
    t=None
    for l in lines:
        m=re.match(r'(\d+):(\d+):(\d+)\.\d+ -->',l)
        if m: t=int(m[1])*3600+int(m[2])*60+int(m[3]); continue
        if not l.strip() or l.startswith(('WEBVTT','Kind:','Language:')) or t is None: continue
        txt=re.sub(r'<[^>]+>','',l).strip()
        if not txt or txt==last: continue
        last=txt
        b=t//15
        if b!=bucket:
            if buf: out.append(f'[{bucket*15//60:02d}:{bucket*15%60:02d}] '+' '.join(buf))
            buf=[];bucket=b
        if not buf or buf[-1]!=txt: buf.append(txt)
    if buf: out.append(f'[{bucket*15//60:02d}:{bucket*15%60:02d}] '+' '.join(buf))
    # dedupe rolling captions
    text='\n'.join(out)
    title=dur=chan=''
    ij=glob.glob(d+'/*.info.json')
    if ij:
        j=json.load(open(ij[0])); title=j.get('title');dur=j.get('duration_string');chan=j.get('channel')
        desc=(j.get('description') or '')[:1500]
    else: desc=''
    open(os.path.join(d,'transcript.txt'),'w').write(f'# {title}\nchannel: {chan}\nduration: {dur}\nurl: https://youtu.be/{id}\n\n## description\n{desc}\n\n## transcript (15s buckets)\n{text}\n')
    print(id,dur,len(text.split()),'words')
