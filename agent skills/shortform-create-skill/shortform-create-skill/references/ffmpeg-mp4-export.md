# FFmpeg MP4 Export

Every video-producing pipeline must end with a high-quality `.mp4` export.

## Default Contract

- container: `.mp4`
- video codec: H.264
- audio codec: AAC when audio exists
- pixel format: `yuv420p`
- configurable width, height, and FPS
- preserve aspect ratio
- never stretch faces or footage
- verify with `ffprobe`

## Export Patterns

The generated export script should support the user's selected construction method:

- single full-screen video
- slideshow
- generated clip sequence
- montage
- voiceover plus visuals
- optional overlays/titles
- optional captions
- aspect-ratio conversion

## Scale/Crop Rule

Use scale-to-cover plus crop for full-frame outputs:

```text
scale=<w>:<h>:force_original_aspect_ratio=increase,crop=<w>:<h>
```

Use scale-to-contain plus pad only when the user wants no crop.

## QA

After export, check:

- file exists
- extension is `.mp4`
- dimensions match config
- duration is non-zero
- video stream exists
- audio stream exists when required
