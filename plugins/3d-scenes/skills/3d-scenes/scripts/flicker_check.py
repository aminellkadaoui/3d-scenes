# usage: python3 flicker_check.py <folder_with_PNG_frames>
# Temporal flicker: second difference per pixel f[t]-(f[t-1]+f[t+1])/2 on 4x-downsampled luminance.
# Smooth camera motion gives ~0; boiling/popping gives spikes. Reports per-region values (0-255 scale) and worst frames.
import sys, glob, numpy as np
from PIL import Image
fs=sorted(glob.glob(sys.argv[1]+"/*.png"))
def L(p):
    a=np.asarray(Image.open(p).convert("L").resize((480,270),Image.BOX)).astype(float); return a
F=np.stack([L(p) for p in fs])
d2=np.abs(F[1:-1]-(F[:-2]+F[2:])/2)
print("frames",len(fs)," mean temporal 2nd-diff:", round(float(d2.mean()),3), " p99:", round(float(np.percentile(d2,99)),2))
H,W=d2.shape[1:]
g=np.array([[d2[:,i*H//4:(i+1)*H//4,j*W//6:(j+1)*W//6].mean() for j in range(6)] for i in range(4)])
np.set_printoptions(precision=2,suppress=True); print("per region (4x6):\n",g)
per=d2.reshape(len(d2),-1).mean(1); worst=np.argsort(per)[-3:][::-1]
print("worst frames:", [(fs[k+1].split('/')[-1], round(float(per[k]),3)) for k in worst])
m=F.reshape(len(F),-1).mean(1); print("global brightness pumping (std of 2nd diff of mean):", round(float(np.abs(m[1:-1]-(m[:-2]+m[2:])/2).std()),4))
