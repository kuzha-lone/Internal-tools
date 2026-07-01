#!/usr/bin/env bash
set -euo pipefail

# Stitch 3 video clips into one final video using ffmpeg concat.
# Usage: stitch-clips.sh --clip1 c1.mp4 --clip2 c2.mp4 --clip3 c3.mp4 --out final.mp4

CLIP1=""
CLIP2=""
CLIP3=""
OUTPUT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --clip1) CLIP1="$2"; shift 2 ;;
    --clip2) CLIP2="$2"; shift 2 ;;
    --clip3) CLIP3="$2"; shift 2 ;;
    --out)   OUTPUT="$2"; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$CLIP1" || -z "$CLIP2" || -z "$CLIP3" || -z "$OUTPUT" ]]; then
  echo "Usage: stitch-clips.sh --clip1 <file> --clip2 <file> --clip3 <file> --out <file>" >&2
  exit 1
fi

for clip in "$CLIP1" "$CLIP2" "$CLIP3"; do
  if [[ ! -f "$clip" ]]; then
    echo "Error: Clip not found: $clip" >&2
    exit 1
  fi
done

# Ensure output directory exists
mkdir -p "$(dirname "$OUTPUT")"

# Create a temporary concat file list
TMPLIST=$(mktemp /tmp/concat-XXXXXX.txt)
trap 'rm -f "$TMPLIST"' EXIT

echo "file '$(realpath "$CLIP1")'" >> "$TMPLIST"
echo "file '$(realpath "$CLIP2")'" >> "$TMPLIST"
echo "file '$(realpath "$CLIP3")'" >> "$TMPLIST"

echo "Stitching 3 clips into final video..."
echo "  Clip 1: $CLIP1"
echo "  Clip 2: $CLIP2"
echo "  Clip 3: $CLIP3"
echo "  Output: $OUTPUT"

# Normalize all clips to same format then concatenate
ffmpeg -y \
  -i "$CLIP1" -i "$CLIP2" -i "$CLIP3" \
  -filter_complex "
    [0:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=25[v0];
    [1:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=25[v1];
    [2:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=25[v2];
    [v0][v1][v2]concat=n=3:v=1:a=0[vout]
  " \
  -map "[vout]" \
  -c:v libx264 -preset fast -crf 20 \
  -movflags +faststart \
  "$OUTPUT" 2>&1

echo "Final video saved to: $OUTPUT"

# Print video info
ffprobe -v quiet -print_format json -show_format "$OUTPUT" 2>/dev/null | \
  python3 -c "
import json, sys
info = json.load(sys.stdin)
duration = float(info.get('format', {}).get('duration', 0))
size = int(info.get('format', {}).get('size', 0))
print(f'Duration: {duration:.1f}s | Size: {size / 1024 / 1024:.1f} MB')
" 2>/dev/null || true
