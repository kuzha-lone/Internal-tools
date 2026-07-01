# Vertical Reframing

`scripts/autocrop_vertical.py` converts one already-cut clip into a vertical video.

Use it after `cut_clips.py`, not against the full long-form source.

Default command:

```bash
python3 scripts/autocrop_vertical.py \
  --input work/clips/clip_001_horizontal.mp4 \
  --output work/vertical/clip_001_vertical.mp4
```

Useful options:

- `--height 1920`: platform-ready `1080x1920` output for `9:16`.
- `--native-height`: use the source clip height instead of upscaling.
- `--wide-mode blur`: use blurred background for wide/group scenes.
- `--wide-mode letterbox`: preserve the full frame with bars.
- `--yolo-model assets/models/yolov8n.pt`: explicit YOLO weights path. The default is the skill-owned model asset.
- `--scene-samples 1`: faster scene analysis.
- `--scene-samples 3`: more stable scene decisions.

Strategy behavior:

- `TRACK`: crop around the detected person, face, or group.
- `WIDE`: preserve the full frame with blur or letterbox.

If YOLO is unavailable, the script falls back to Haar face detection. If scene detection is unavailable, the clip is treated as one scene.
