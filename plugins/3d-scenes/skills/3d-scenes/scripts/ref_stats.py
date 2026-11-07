#!/usr/bin/env python3
"""3D Scenes — measure a reference image or render (run in a normal shell, not inside Blender).
Usage: python3 ref_stats.py image1.jpg [image2.png ...]
Needs numpy and ffmpeg (falls back to imageio_ffmpeg's bundled binary)."""
import subprocess, sys, shutil
import numpy as np

def ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe: return exe
    import imageio_ffmpeg; return imageio_ffmpeg.get_ffmpeg_exe()

W, H = 192, 108
for path in sys.argv[1:]:
    raw = subprocess.run([ffmpeg(), "-v", "error", "-i", path, "-vf", f"scale={W}:{H},format=rgb24",
                          "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(H, W, 3) / 255.0
    L = a @ [0.2126, 0.7152, 0.0722]
    p1, p50, p99 = np.percentile(L, [1, 50, 99])
    print(f"{path}\n  luminance p1 {p1:.3f}  p50 {p50:.3f}  p99 {p99:.3f}")
    print(f"  top third (background) {L[:H//3].mean():.3f} | bottom third (floor) {L[2*H//3:].mean():.3f} | centre (hero) {L[H//4:3*H//4, W//3:2*W//3].mean():.3f}")
    print(f"  mean RGB {np.round(a.mean(axis=(0,1)),3)}  saturation {(a.max(2)-a.min(2)).mean():.3f}")
    if L[:H//3].mean() < 0.01: print("  ! background ~0 = void; use a designed dark backdrop")
    if L[2*H//3:].mean() > L[H//4:3*H//4, W//3:2*W//3].mean(): print("  ! floor brighter than hero = focal point lost")
