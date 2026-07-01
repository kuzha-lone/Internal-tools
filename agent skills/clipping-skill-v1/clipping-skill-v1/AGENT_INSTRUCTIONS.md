# Agent Instructions

Use this file when an agent is asked to run the clipping skill on a user's machine.

## Core Behavior

- Accept either `--file` or `--url`.
- Do not ask for confirmation just because the input video is large.
- Cut short horizontal clips first, then convert each cut to vertical.
- Use `--youtube-auth` for YouTube URLs by default.
- Do not ask the user to manually export cookies.
- Do not require an AI API key for captions. Captions are generated from local transcript word timestamps.
- Report the final `captioned_path` values from `project_manifest.json`.

## First-Time Setup

From the skill folder, run:

```bash
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m playwright install chromium
```

Verify external tools:

```bash
ffmpeg -version
ffprobe -version
node --version
```

If `ffmpeg` or `ffprobe` is missing, install FFmpeg with the user's system package manager.

## Run Pipeline

Local file:

```bash
.venv/bin/python scripts/run_pipeline.py \
  --file /path/to/video.mp4 \
  --workdir clipping_work \
  --clips 5
```

YouTube URL:

```bash
.venv/bin/python scripts/run_pipeline.py \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --workdir clipping_work \
  --clips 5 \
  --youtube-auth
```

One clip only:

```bash
.venv/bin/python scripts/run_pipeline.py \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --workdir clipping_work \
  --clips 1 \
  --youtube-auth
```

## YouTube Auth Flow

The skill does not include cookies.

With `--youtube-auth`, `scripts/run_pipeline.py` uses this path:

```text
~/.cache/clipping-skill/youtube/youtube.cookies.txt
```

Expected behavior:

1. Try HD download first.
2. If YouTube blocks HD, open a managed browser using `scripts/youtube_auth.py`.
3. User signs into YouTube in that browser.
4. Export only relevant YouTube/Google cookies to the local cache path.
5. Retry download with that cookie file.
6. Reuse the cookie file on future runs.

Never print cookie values. Never copy the cookie file into the skill folder. Never package it with outputs.

To reset auth at the user's request:

```bash
rm -rf ~/.cache/clipping-skill/youtube
```

## Pipeline Stages

The orchestrator is `scripts/run_pipeline.py`.

Stage order:

1. `ingest_source.py`: copy local file or download URL to `workdir/source.mp4`.
2. `probe_media.py`: write source metadata.
3. `transcribe_source.py`: local faster-whisper transcript with word timestamps.
4. `find_clip_candidates.py`: choose transcript windows for short clips.
5. `cut_clips.py`: cut horizontal clips from the original source.
6. `autocrop_vertical.py`: convert each cut to `9:16`.
7. `caption_clips.py`: burn lower-third active-word captions.
8. `make_manifest.py`: build handoff manifest.
9. `qa_outputs.py`: verify aspect ratio, duration, and audio.

## Important Defaults

- HD source required: minimum short edge `720px`.
- Candidate clips: `5`.
- Clip duration: `18-60s`, target `38s`.
- Output: `1080x1920`.
- YOLO model: `assets/models/yolov8n.pt`.
- Caption font: `assets/fonts/Sddystopiandemo-GO7xa.otf`.
- Active caption color: `#00d9ff`.
- Downloaded URL source is deleted at the end unless `--keep-source` is passed.

## Outputs To Report

Read:

```text
workdir/project_manifest.json
workdir/qa_report.json
```

For each clip, report:

- `captioned_path` if captions were enabled
- `vertical_path`
- `source_start` and `source_end`
- `duration`
- QA status from `qa_report.json`

## Failure Handling

If HD YouTube download fails:

- rerun with `--youtube-auth`
- if the managed browser opens, tell the user to sign into YouTube in that browser
- if auth still fails, report the failed stage and the exact command

If transcription fails:

- check that `faster-whisper` is installed
- allow the user/agent to provide `--transcript /path/to/transcript.json`

If vertical reframing fails:

- verify `assets/models/yolov8n.pt` exists
- verify `opencv-python`, `ultralytics`, and `torch` are installed
- rerun a single stage with `scripts/autocrop_vertical.py` for debugging

If captions fail:

- verify `transcript.json` contains word timestamps
- verify the caption font file exists
- rerun `scripts/caption_clips.py --manifest workdir/project_manifest.json`

