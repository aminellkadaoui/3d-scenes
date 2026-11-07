#!/bin/zsh
# Usage: ingest_video.sh <youtube-id-or-url> [lang]   (lang default: en ; use ar for Arabic videos)
# Produces sources/raw/<id>/: info.json, captions .vtt, transcript.txt (15s buckets), 480p mp4, frames/contact sheets
set -u
ROOT="${0:A:h:h}"
in="$1"; lang="${2:-en}"
id=$(python3 -c "import re,sys;u=sys.argv[1];m=re.search(r'(?:v=|youtu\.be/|shorts/)([\w-]{11})',u);print(m.group(1) if m else u)" "$in")
export SSL_CERT_FILE=$(python3 -m certifi)
FF=$(python3 -c "import imageio_ffmpeg as f;print(f.get_ffmpeg_exe())")
D="$sources/raw/$id"; mkdir -p "$D/frames"
# captions (retry on 429)
for t in 1 2 3; do
  python3 -m yt_dlp -q --no-warnings --skip-download --write-info-json --write-auto-subs --write-subs \
    --sub-langs "${lang}-orig,${lang}" --sub-format vtt -o "$D/%(id)s.%(ext)s" "https://youtu.be/$id" && break
  sleep 45
done
# video 480p (no subs, so caption errors can't block it)
python3 -m yt_dlp -q --no-warnings --no-write-subs -f "bv*[height<=480][ext=mp4]/b[height<=480]/worst" -o "$D/%(id)s.%(ext)s" "https://youtu.be/$id"
python3 -I "$scripts/vtt2txt.py" "$sources/raw" >/dev/null
# one frame every 20s + 4x4 contact sheets for quick visual scan
mp4=$(ls "$D"/*.mp4 2>/dev/null | head -1)
if [ -n "$mp4" ]; then
  "$FF" -loglevel error -y -i "$mp4" -vf "fps=1/20,scale=640:-2" "$D/frames/f_%03d.jpg"
  "$FF" -loglevel error -y -i "$mp4" -vf "fps=1/20,scale=320:-2,tile=4x4" "$D/frames/sheet_%02d.jpg"
fi
echo "$id -> $D"; ls "$D" | tr '\n' ' '; echo
