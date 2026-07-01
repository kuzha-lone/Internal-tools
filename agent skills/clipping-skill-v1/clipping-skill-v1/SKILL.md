---
name: clipping-skill
description: Use when a user provides a local video file or video URL, including YouTube URLs, and wants an agent to ingest long-form content, find short-form clip moments, cut them first, and convert them into vertical 9:16 clips for later editing, captions, hooks, overlays, or publishing.
metadata:
  short-description: Turn long videos into vertical short-form clip assets
---

# Clipping Skill

This skill turns a user-provided video URL or local file into short-form vertical clip assets.

Core rule: cut selected short clips first, then run vertical reframing. Do not render a huge source video to vertical unless the user explicitly asks for full-video conversion.

For install and user setup instructions, read `README.md`. For the agent execution playbook, read `AGENT_INSTRUCTIONS.md`.

## Default Workflow

Use the bundled pipeline:

```bash
python3 scripts/run_pipeline.py --file /path/to/video.mp4 --workdir clipping_work --clips 5
```

For a user-provided URL:

```bash
python3 scripts/run_pipeline.py --url "https://www.youtube.com/watch?v=..." --workdir clipping_work --clips 5 --youtube-auth
```

HD is required by default. The URL downloader requests `720p-1080p` video plus best audio and fails if YouTube only exposes low-resolution formats.

For YouTube HD downloads, use the managed auth flow:

```bash
.venv/bin/python scripts/run_pipeline.py \
  --url "https://www.youtube.com/watch?v=..." \
  --workdir clipping_work \
  --clips 5 \
  --youtube-auth
```

Behavior:

- The pipeline first tries to download HD.
- If YouTube blocks HD, it opens a local browser window owned by this skill.
- The user signs into YouTube once in that window.
- The skill writes a private `cookies.txt` file automatically under `~/.cache/clipping-skill/youtube`.
- Future runs reuse that managed session.
- The skill rejects anything below `720p` unless `--allow-low-res` is explicitly passed for debugging.

This avoids relying on the user's existing browser. Existing browser cookies are still supported for debugging with `--cookies-from-browser chrome`, `--cookies-from-browser safari`, `--cookies-from-browser firefox`, or `--cookies /path/to/cookies.txt`, but the product path is `--youtube-auth`.

The pipeline runs:

1. `ingest_source.py`: copy local file or download URL to `workdir/source.mp4`.
2. `probe_media.py`: write `workdir/source_metadata.json`.
3. `transcribe_source.py`: write local faster-whisper transcript to `workdir/transcript.json`.
4. `find_clip_candidates.py`: select candidate short-form windows from the transcript.
5. `cut_clips.py`: cut horizontal short clips before any vertical processing.
6. `autocrop_vertical.py`: make `9:16` vertical clips with scene-aware reframing.
7. `caption_clips.py`: burn centered lower-third active-word captions into the vertical clips.
8. `make_manifest.py`: write `workdir/project_manifest.json` for later editing.
9. `qa_outputs.py`: verify generated vertical and captioned outputs with ffprobe.

Output paths are listed in `project_manifest.json`.

## Non-Interactive Behavior

- Do not ask the user for big-file confirmation.
- Do not pause to confirm clip count, duration, or crop settings when reasonable defaults apply.
- Treat user-provided URLs/files as intentional source inputs for the task.
- If a URL/file cannot be acquired or decoded, report the failure and the exact failed stage.
- If transcription is unavailable, use an existing transcript if the user/agent can provide one; otherwise report that `faster-whisper` is missing.

## Defaults

- Candidate clips: `5`
- Clip duration: `18-60s`, target `38s`
- Vertical output: `1080x1920`, `9:16`
- Wide/group scenes: blurred background with original frame fitted in foreground
- YOLO model: `assets/models/yolov8n.pt`
- Source handling: URL downloads are deleted after the pipeline unless `--keep-source` is passed

See `assets/presets.json` for tunable defaults.

## Captions

Do not require a caption AI API key. The skill produces `transcript.json` with segment and word timestamps, then burns captions with FFmpeg ASS subtitles.

Default caption behavior:

- centered in the lower third of the `1080x1920` video
- stable 3-word groups
- active spoken word highlighted
- inactive words white
- default font: `assets/fonts/Sddystopiandemo-GO7xa.otf`
- default active word color: `#00d9ff`

Caption outputs are written to `workdir/captioned`:

```text
clip_001_captioned.mp4
clip_001_captions.ass
clip_001_caption_manifest.json
caption_outputs.json
```

Override caption style from the pipeline:

```bash
.venv/bin/python scripts/run_pipeline.py \
  --url "https://www.youtube.com/watch?v=..." \
  --workdir clipping_work \
  --youtube-auth \
  --caption-active-word-color "#00d9ff" \
  --caption-font-file /path/to/font.ttf \
  --caption-font-name "Font Family Name"
```

Use `--no-captions` to skip caption burn-in and output raw vertical clips only.

For caption handoff details, read `references/caption_handoff.md`.

## Vertical Reframing

The bundled `autocrop_vertical.py` implements an AutoCrop-style engine:

- PySceneDetect scene boundaries when available.
- YOLOv8 person detection when available.
- YOLO weights are loaded from `assets/models/yolov8n.pt` by default, not from the process working directory.
- Haar face detection fallback.
- Per-scene `TRACK` or `WIDE` strategy.
- OpenCV frame processing piped to FFmpeg.
- Audio preserved when present.

For implementation details and tuning, read `references/vertical_reframing.md`.

## Stage Commands

Run stages manually when debugging or overriding the pipeline:

```bash
python3 scripts/ingest_source.py --file input.mp4 --workdir work
python3 scripts/probe_media.py --input work/source.mp4 --out work/source_metadata.json
python3 scripts/transcribe_source.py --input work/source.mp4 --out work/transcript.json
python3 scripts/find_clip_candidates.py --transcript work/transcript.json --out work/clip_candidates.json --count 5
python3 scripts/cut_clips.py --input work/source.mp4 --candidates work/clip_candidates.json --out-dir work/clips
python3 scripts/autocrop_vertical.py --input work/clips/clip_001_horizontal.mp4 --output work/vertical/clip_001_vertical.mp4 --yolo-model assets/models/yolov8n.pt
python3 scripts/make_manifest.py --workdir work
python3 scripts/caption_clips.py --manifest work/project_manifest.json
python3 scripts/make_manifest.py --workdir work
python3 scripts/qa_outputs.py --manifest work/project_manifest.json --out work/qa_report.json
```

## Dependencies

Required command-line tools:

- `ffmpeg`
- `ffprobe`

Required Python libraries for the full pipeline:

- `opencv-python`
- `numpy`
- `scenedetect`
- `faster-whisper`
- `ultralytics` and `torch` for YOLOv8 person detection
- `yt-dlp` for URL ingestion

Install from `requirements.txt` into a local venv before running the pipeline:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/run_pipeline.py --file /path/to/video.mp4 --workdir clipping_work --clips 5
```

The scripts are defensive when a dependency fails at runtime, but the product plan is to ship YOLO/Ultralytics as part of the core install.
