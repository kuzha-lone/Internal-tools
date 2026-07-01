# Clipping Skill

Turn a long video URL or local video file into short vertical `9:16` clip assets with captions.

This skill is designed for an agent to run locally on the user's computer. It does not ship with any YouTube/Google cookies, API keys, or private user data.

## What It Produces

For each selected clip, the pipeline creates:

- a horizontal source cut in `workdir/clips`
- a vertical `9:16` version in `workdir/vertical`
- a captioned vertical version in `workdir/captioned`
- `workdir/project_manifest.json`, which lists all generated files and the next editing steps
- `workdir/qa_report.json`, which verifies aspect ratio, duration, and audio

## Requirements

Install these system tools first:

- Python 3.11 or newer
- FFmpeg and FFprobe
- Node.js, recommended for YouTube JS challenges

On macOS with Homebrew:

```bash
brew install python ffmpeg node
```

On Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip ffmpeg nodejs npm
```

## Install

From inside this skill folder:

```bash
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m playwright install chromium
```

The skill includes `assets/models/yolov8n.pt` for YOLO person detection. If that file is removed, Ultralytics may download the model again on first use.

## Run With A Local File

```bash
.venv/bin/python scripts/run_pipeline.py \
  --file /path/to/video.mp4 \
  --workdir clipping_work \
  --clips 5
```

## Run With A YouTube URL

```bash
.venv/bin/python scripts/run_pipeline.py \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --workdir clipping_work \
  --clips 5 \
  --youtube-auth
```

HD is required by default. The downloader requests `720p-1080p` video plus best audio and rejects sources below `720p` short edge unless `--allow-low-res` is passed for debugging.

## YouTube Login And Cookies

No cookies are included with this skill.

When `--youtube-auth` is used:

1. The pipeline first tries to download HD directly.
2. If YouTube blocks HD, the skill opens a local managed browser window.
3. The user signs into YouTube in that browser window.
4. The skill writes the user's private cookies to:

```text
~/.cache/clipping-skill/youtube/youtube.cookies.txt
```

5. Future runs reuse that managed session automatically.

The cookie file is private to the user's machine. Do not upload it, package it, commit it, or send it to anyone.

To reset YouTube auth:

```bash
rm -rf ~/.cache/clipping-skill/youtube
```

## Caption Style

Default captions:

- centered in the lower third
- three-word groups
- active spoken word highlighted
- default font: `assets/fonts/Sddystopiandemo-GO7xa.otf`
- active word color: `#00d9ff`

Override style:

```bash
.venv/bin/python scripts/run_pipeline.py \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --workdir clipping_work \
  --clips 5 \
  --youtube-auth \
  --caption-active-word-color "#00d9ff" \
  --caption-font-file assets/fonts/Eightgon-OGn6p.ttf
```

## Useful Options

- `--clips 1`: generate one clip.
- `--min-duration 18 --max-duration 60 --target-duration 38`: control clip length.
- `--height 1920`: output `1080x1920`.
- `--wide-mode blur`: blurred background for wide scenes.
- `--wide-mode letterbox`: preserve the full frame with bars.
- `--no-captions`: skip caption burn-in.
- `--keep-source`: keep downloaded `source.mp4` in the workdir.
- `--allow-low-res`: allow below-HD sources for debugging only.

## Agent Instructions

For a step-by-step agent playbook, read `AGENT_INSTRUCTIONS.md`.
