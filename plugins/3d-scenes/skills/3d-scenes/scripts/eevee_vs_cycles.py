# usage: python3 eevee_vs_cycles.py cycles.png eevee.png out_heatmap.png
import sys, numpy as np
from PIL import Image
def _box(x,r,ax):
    c=np.cumsum(np.pad(x,[(r+1,r) if a==ax else (0,0) for a in range(2)],mode='edge'),axis=ax)
    n=x.shape[ax]; a=np.take(c,range(2*r+1,2*r+1+n),axis=ax); b=np.take(c,range(0,n),axis=ax); return (a-b)/(2*r+1)
def gaussian_filter(x,r):
    for _ in range(3): x=_box(_box(x,r,0),r,1)
    return x
def lum(p):
    a=(np.asarray(Image.open(p).convert("RGB")).astype(float)/255)**2.2
    return a, 0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]
ca,c=lum(sys.argv[1]); ea,e=lum(sys.argv[2])
cb,eb=gaussian_filter(c,12),gaussian_filter(e,12)
r=np.log2((eb+1e-4)/(cb+1e-4)); H,W=r.shape
print("ratio grid (1.00 = same):")
for i in range(4): print("  "+" ".join(f"{2**r[i*H//4:(i+1)*H//4, j*W//6:(j+1)*W//6].mean():4.2f}" for j in range(6)))
print("overall", round(e.mean()/c.mean(),3), " |log2 diff| mean", round(np.abs(r).mean(),3))
cc=ca.reshape(-1,3).mean(0); ec=ea.reshape(-1,3).mean(0); print("mean rgb cyc", np.round(cc,4), "eev", np.round(ec,4))
rr=np.clip(r,-2,2)/2; rgb=np.zeros(rr.shape+(3,)); rgb[...,2]=np.clip(-rr,0,1); rgb[...,0]=np.clip(rr,0,1); rgb[...,1]=0.15
base=Image.open(sys.argv[1]).convert("L").resize((960,540)).convert("RGB")
Image.blend(base,Image.fromarray((rgb*255).astype(np.uint8)).resize((960,540)),0.6).save(sys.argv[3])
