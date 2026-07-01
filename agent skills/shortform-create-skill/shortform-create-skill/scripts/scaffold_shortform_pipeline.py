#!/usr/bin/env python3
"""Scaffold a custom short-form video pipeline skill from a pipeline spec."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import shutil
import textwrap
from typing import Any


MEDIA_EXTENSIONS = {".mp4", ".mov", ".m4v", ".avi", ".mkv", ".webm"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a custom short-form video pipeline folder.")
    parser.add_argument("--name", required=True, help="Pipeline display name.")
    parser.add_argument("--output", required=True, help="Target folder to create.")
    parser.add_argument("--spec", required=True, help="Pipeline spec JSON created after user discovery.")
    parser.add_argument("--force", action="store_true", help="Overwrite target folder if it already exists.")
    return parser.parse_args()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "shortform-pipeline"


def load_spec(path: pathlib.Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise SystemExit("Spec must be a JSON object.")
    return payload


def normalize_choice(spec: dict[str, Any], key: str, default: str) -> str:
    value = str(spec.get(key) or default).strip().lower().replace(" ", "_").replace("-", "_")
    return value or default


def list_value(spec: dict[str, Any], key: str) -> list[Any]:
    value = spec.get(key, [])
    if isinstance(value, list):
        return value
    if value in (None, ""):
        return []
    return [value]


def providers_from_spec(spec: dict[str, Any]) -> list[dict[str, Any]]:
    raw = spec.get("providers", [])
    providers: list[dict[str, Any]] = []
    if isinstance(raw, dict):
        raw = [
            {"name": name, **(value if isinstance(value, dict) else {"purpose": str(value)})}
            for name, value in raw.items()
        ]
    for item in raw if isinstance(raw, list) else []:
        if isinstance(item, str):
            providers.append({"name": item, "required": False, "env": [], "purpose": "selected provider"})
        elif isinstance(item, dict):
            name = str(item.get("name") or item.get("provider") or "").strip()
            if not name:
                continue
            env = item.get("env") or item.get("env_vars") or []
            if isinstance(env, str):
                env = [env]
            providers.append(
                {
                    "name": name,
                    "required": bool(item.get("required", False)),
                    "env": [str(value).strip() for value in env if str(value).strip()],
                    "purpose": str(item.get("purpose") or "selected provider"),
                    "approval_required": bool(item.get("approval_required", item.get("required", False))),
                }
            )
    return providers


def infer_stages(spec: dict[str, Any]) -> list[dict[str, Any]]:
    content_mode = normalize_choice(spec, "content_source_mode", "manual_script")
    script_mode = normalize_choice(spec, "script_mode", "manual_script")
    media_method = normalize_choice(spec, "media_construction_method", normalize_choice(spec, "media_method", "generated_clips"))
    audio_mode = normalize_choice(spec, "audio_mode", "none")
    captions_mode = normalize_choice(spec, "captions_mode", normalize_choice(spec, "caption_choice", "none"))

    stages: list[dict[str, Any]] = [
        {
            "slug": "content-input-skill",
            "name": "Content Input Skill",
            "purpose": f"Collect or produce the starting content using mode `{content_mode}`.",
            "inputs": "user brief, source files, recurring feed, or research target",
            "outputs": "approved content topic, source package, or source media manifest",
            "tool": "user input, browsing/research tools, source files, or configured feeds",
            "approval_required": content_mode in {"agent_research", "research_with_approval"},
            "success_condition": "A usable content input package exists.",
            "failure_condition": "No approved topic, script, source media, or source package exists.",
        }
    ]

    if script_mode not in {"none", "no_script", "source_audio_only"}:
        stages.append(
            {
                "slug": "script-skill",
                "name": "Script Skill",
                "purpose": f"Create or validate the production script using mode `{script_mode}`.",
                "inputs": "content input package and user style rules",
                "outputs": "approved script, outline, beat cards, scene cards, or clip notes",
                "tool": "agent writing, user script, validator, or structured scene-card workflow",
                "approval_required": bool(spec.get("script_approval_required", True)),
                "success_condition": "Script or beat plan is approved and saved.",
                "failure_condition": "Script is missing, unapproved, or fails validation.",
            }
        )

    stages.append(
        {
            "slug": "media-build-skill",
            "name": "Media Build Skill",
            "purpose": f"Build the visual media using method `{media_method}`.",
            "inputs": "approved script/beat plan and asset requirements",
            "outputs": "visual clips, images, screen recordings, generated media, or media manifest",
            "tool": "selected media tools/providers from config/providers.json",
            "approval_required": "provider" in media_method or bool(spec.get("media_approval_required", False)),
            "success_condition": "All required visual media files or provider outputs exist.",
            "failure_condition": "A required visual asset, clip, or manifest is missing.",
        }
    )

    if "hyperframes" in media_method or normalize_choice(spec, "animation_mode", "none") not in {"none", "no_animation"}:
        stages.append(
            {
                "slug": "animation-skill",
                "name": "Animation Skill",
                "purpose": "Create optional animation or motion graphics selected by the user.",
                "inputs": "script/beat plan, visual style, timing source",
                "outputs": "rendered animation clip or animation asset package",
                "tool": "HyperFrames, Remotion, HTML/CSS/GSAP, or selected animation provider",
                "approval_required": bool(spec.get("animation_approval_required", False)),
                "success_condition": "Animation output exists and matches timing/export requirements.",
                "failure_condition": "Animation output is missing, unreadable, or incompatible with FFmpeg export.",
            }
        )

    if audio_mode not in {"none", "silent", "no_voice"}:
        stages.append(
            {
                "slug": "audio-skill",
                "name": "Audio Skill",
                "purpose": f"Create or collect audio using mode `{audio_mode}`.",
                "inputs": "script, source media, user audio, music, or provider config",
                "outputs": "audio file, source audio segment, voiceover, or audio manifest",
                "tool": "user audio, TTS, avatar provider, source media extraction, or music source",
                "approval_required": "tts" in audio_mode or "provider" in audio_mode,
                "success_condition": "Required audio exists and has usable duration.",
                "failure_condition": "Audio is missing when required or cannot be probed.",
            }
        )

    if captions_mode not in {"none", "no_captions", "platform_native"}:
        stages.append(
            {
                "slug": "captions-skill",
                "name": "Captions Skill",
                "purpose": f"Create optional captions using mode `{captions_mode}`.",
                "inputs": "final or near-final video plus transcript/timing source",
                "outputs": "caption file or captioned MP4, depending on config",
                "tool": "Whisper, HyperFrames transcribe, ElevenLabs Scribe, manual transcript, ASS subtitles, or FFmpeg",
                "approval_required": bool(spec.get("captions_approval_required", False)),
                "success_condition": "Caption artifacts exist and pass readability rules.",
                "failure_condition": "Captions are missing, clipped, unreadable, or unsynced.",
            }
        )

    stages.extend(
        [
            {
                "slug": "export-skill",
                "name": "Export Skill",
                "purpose": "Assemble and export the final high-quality MP4.",
                "inputs": "selected visual media, optional audio, optional captions/overlays, export config",
                "outputs": "final .mp4",
                "tool": "FFmpeg and ffprobe",
                "approval_required": False,
                "success_condition": "Final MP4 exists and ffprobe verifies dimensions, duration, and required streams.",
                "failure_condition": "MP4 export is missing, wrong dimensions, zero duration, or missing required audio.",
            },
            {
                "slug": "qa-skill",
                "name": "QA Skill",
                "purpose": "Verify the pipeline run completed all required stages and produced a usable MP4.",
                "inputs": "stage artifacts, final MP4, config, and ffprobe result",
                "outputs": "QA pass/fail report",
                "tool": "audit script, ffprobe, and manual visual review when needed",
                "approval_required": False,
                "success_condition": "All required QA checks pass.",
                "failure_condition": "Any required stage artifact or final export check fails.",
            },
        ]
    )
    return stages


def write(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: pathlib.Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def env_example(providers: list[dict[str, Any]]) -> str:
    lines = [
        "# Copy this file to .env and fill in only the providers this pipeline uses.",
        "# Keep .env private. Do not commit or redistribute real values.",
        "",
    ]
    env_names: list[str] = []
    for provider in providers:
        for env_name in provider.get("env", []):
            if env_name not in env_names:
                env_names.append(env_name)
    if not env_names:
        lines.append("# No provider API keys are required by the current spec.")
    for env_name in env_names:
        lines.append(f'{env_name}=""')
    return "\n".join(lines) + "\n"


def central_skill_text(name: str, slug: str, stages: list[dict[str, Any]]) -> str:
    stage_lines = "\n".join(f"{idx}. `{stage['slug']}` - {stage['purpose']}" for idx, stage in enumerate(stages, start=1))
    return f"""---
name: {slug}
description: Run the repeatable short-form video pipeline defined by this folder and export a final MP4.
---

# {name}

Use this skill to run this specific short-form video pipeline.

## Inputs

Read:

- `../../../SYSTEM.md`
- `../../../AGENT_RUNBOOK.md`
- `../../../config/project.json`
- `../../../config/pipeline.json`
- `../../../config/video.json`
- `../../../config/providers.json`
- `../../../config/export.json`

## Stage Order

Follow this exact order. Optional stages are present only because the user selected them during pipeline creation.

{stage_lines}

## Contract

- Preserve the approved process for every run.
- Do not skip approval gates.
- Do not call paid/live provider APIs unless the user approved that run or config explicitly allows it.
- Keep provider secrets in `.env`; never write them into configs or docs.
- Every completed run must return a final `.mp4`.
- If a required artifact is missing, stop and report the missing stage.
"""


def root_skill_text(name: str, slug: str) -> str:
    return f"""---
name: {slug}
description: Run the {name} custom short-form video pipeline and export a final MP4.
---

# {name}

This is the root entrypoint for the generated pipeline.

Read `START_HERE.md`, `SYSTEM.md`, `AGENT_RUNBOOK.md`, and then `skills/{slug}/SKILL.md`.
"""


def subskill_text(stage: dict[str, Any]) -> str:
    return f"""---
name: {stage['slug']}
description: {stage['purpose']}
---

# {stage['name']}

## Contract

- Purpose: {stage['purpose']}
- Inputs: {stage['inputs']}
- Outputs: {stage['outputs']}
- Tool/provider: {stage['tool']}
- Approval required: {stage['approval_required']}
- Success condition: {stage['success_condition']}
- Failure condition: {stage['failure_condition']}

Do not continue to the next stage until this stage's required output exists or the stage is explicitly optional and disabled in config.
"""


def runbook_text(name: str, stages: list[dict[str, Any]]) -> str:
    stage_lines = "\n".join(f"{idx}. {stage['name']}: {stage['outputs']}" for idx, stage in enumerate(stages, start=1))
    return f"""# Agent Runbook

Use this file to run `{name}` consistently.

## Required Flow

{stage_lines}

## Rules

- Follow the stage order from the central skill.
- Use user approval gates exactly as configured.
- Provider keys must be loaded from `.env`.
- Optional stages run only when enabled.
- Final delivery is the exported `.mp4` plus a short artifact summary.
"""


def system_text(name: str) -> str:
    return f"""# System Rules

This folder defines the `{name}` short-form video pipeline.

- The pipeline is repeatable.
- The final export is `.mp4`.
- FFmpeg/ffprobe are the default local export tools.
- Never stretch media to fit; preserve aspect ratio with crop or pad rules.
- Never write real API keys into tracked files.
- Do not pretend a provider output exists unless the file or URL exists.
"""


def start_here_text(name: str) -> str:
    return f"""# Start Here

1. Copy `.env.example` to `.env`.
2. Fill only the provider keys selected for `{name}`.
3. Edit `config/*.json` if needed.
4. Run `python3 scripts/setup_check.py`.
5. Tell your agent to read `AGENT_RUNBOOK.md`, `SYSTEM.md`, and `skills/*/SKILL.md`.

The final export for this pipeline is always `.mp4`.
"""


def setup_check_script() -> str:
    return r'''#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import pathlib
import shutil
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_json(path: pathlib.Path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def load_dotenv(path: pathlib.Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def is_placeholder(value: str | None) -> bool:
    return value is None or value.strip() == "" or "insert" in value.lower() or "replace" in value.lower()


def main() -> int:
    errors: list[str] = []
    load_dotenv(ROOT / ".env")
    for binary in ("ffmpeg", "ffprobe"):
        if not shutil.which(binary):
            errors.append(f"Missing required binary: {binary}")
    for cfg in ("project.json", "pipeline.json", "video.json", "providers.json", "export.json"):
        path = ROOT / "config" / cfg
        if not path.exists():
            errors.append(f"Missing config/{cfg}")
        else:
            try:
                load_json(path)
            except Exception as exc:
                errors.append(f"Invalid config/{cfg}: {exc}")
    providers_path = ROOT / "config" / "providers.json"
    if providers_path.exists():
        providers = load_json(providers_path).get("providers", [])
        for provider in providers:
            if not provider.get("required"):
                continue
            for env_name in provider.get("env", []):
                if is_placeholder(os.environ.get(env_name)):
                    errors.append(f"Missing required provider env value: {env_name}")
    status = "blocked" if errors else "success"
    print(json.dumps({"status": status, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
'''


def export_mp4_script() -> str:
    return r'''#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import subprocess
import sys


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_export_config() -> dict:
    path = ROOT / "config" / "export.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    return {}


def parse_args() -> argparse.Namespace:
    config = load_export_config()
    parser = argparse.ArgumentParser(description="Export a final high-quality MP4 with FFmpeg.")
    parser.add_argument("--input", action="append", required=True, help="Input media file. Repeat for sequences/montages.")
    parser.add_argument("--output", required=True, help="Final .mp4 path.")
    parser.add_argument("--audio", help="Optional external audio/voice/music file.")
    parser.add_argument("--width", type=int, default=int(config.get("width", 1080)))
    parser.add_argument("--height", type=int, default=int(config.get("height", 1920)))
    parser.add_argument("--fps", type=int, default=int(config.get("fps", 30)))
    parser.add_argument("--image-duration", type=float, default=float(config.get("image_duration_seconds", 3.0)))
    parser.add_argument("--scale-mode", choices=("cover", "contain"), default=str(config.get("scale_mode", "cover")))
    parser.add_argument("--caption-file", help="Optional ASS/SRT caption file to burn in.")
    parser.add_argument("--audio-required", action="store_true", default=bool(config.get("audio_required", False)))
    parser.add_argument("--ffmpeg", default=str(config.get("ffmpeg_path", "ffmpeg")))
    parser.add_argument("--ffprobe", default=str(config.get("ffprobe_path", "ffprobe")))
    return parser.parse_args()


def resolve_binary(value: str) -> str:
    if "/" in value:
        path = pathlib.Path(value).expanduser()
        if path.exists():
            return str(path)
        raise SystemExit(f"Binary path does not exist: {path}")
    found = shutil.which(value)
    if not found:
        raise SystemExit(f"Required binary not found: {value}")
    return found


def vf(width: int, height: int, mode: str) -> str:
    if mode == "contain":
        return f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1"
    return f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},setsar=1"


def ffprobe_dimensions(ffprobe: str, path: pathlib.Path) -> tuple[int, int]:
    result = subprocess.run(
        [ffprobe, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    width, height = result.stdout.strip().split("x", 1)
    return int(width), int(height)


def ffprobe_duration(ffprobe: str, path: pathlib.Path) -> float:
    result = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip() or 0)


def has_audio(ffprobe: str, path: pathlib.Path) -> bool:
    result = subprocess.run(
        [ffprobe, "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=index", "-of", "csv=p=0", str(path)],
        check=False,
        capture_output=True,
        text=True,
    )
    return bool(result.stdout.strip())


def quote_filter_path(path: pathlib.Path) -> str:
    return str(path).replace("\\", "\\\\").replace("'", r"\'")


def main() -> int:
    args = parse_args()
    ffmpeg = resolve_binary(args.ffmpeg)
    ffprobe = resolve_binary(args.ffprobe)
    inputs = [pathlib.Path(item) for item in args.input]
    output = pathlib.Path(args.output)
    if output.suffix.lower() != ".mp4":
        raise SystemExit("Final export path must end in .mp4")
    for path in inputs:
        if not path.exists():
            raise SystemExit(f"Input not found: {path}")
    if args.audio and not pathlib.Path(args.audio).exists():
        raise SystemExit(f"Audio not found: {args.audio}")
    output.parent.mkdir(parents=True, exist_ok=True)

    cmd = [ffmpeg, "-y"]
    for media in inputs:
        if media.suffix.lower() in IMAGE_EXTENSIONS:
            cmd += ["-loop", "1", "-framerate", str(args.fps), "-t", f"{args.image_duration:.3f}", "-i", str(media)]
        else:
            cmd += ["-i", str(media)]
    audio_index = None
    if args.audio:
        audio_index = len(inputs)
        cmd += ["-i", str(args.audio)]

    filters = []
    labels = []
    for idx, _media in enumerate(inputs):
        label = f"v{idx}"
        filters.append(f"[{idx}:v]{vf(args.width, args.height, args.scale_mode)}[{label}]")
        labels.append(f"[{label}]")
    if len(labels) == 1:
        video_label = labels[0]
    else:
        filters.append("".join(labels) + f"concat=n={len(labels)}:v=1:a=0[vcat]")
        video_label = "[vcat]"

    final_label = "[vout]"
    if args.caption_file:
        caption = pathlib.Path(args.caption_file)
        if not caption.exists():
            raise SystemExit(f"Caption file not found: {caption}")
        filters.append(f"{video_label}subtitles=filename='{quote_filter_path(caption)}'{final_label}")
    else:
        filters.append(f"{video_label}null{final_label}")

    cmd += ["-filter_complex", ";".join(filters), "-map", final_label]
    if audio_index is not None:
        cmd += ["-map", f"{audio_index}:a:0"]
    elif len(inputs) == 1 and has_audio(ffprobe, inputs[0]):
        cmd += ["-map", "0:a?"]
    cmd += [
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", str(args.fps),
        "-preset", "medium",
        "-crf", "18",
        "-c:a", "aac",
        "-shortest",
        str(output),
    ]
    subprocess.run(cmd, check=True)

    width, height = ffprobe_dimensions(ffprobe, output)
    duration = ffprobe_duration(ffprobe, output)
    audio_present = has_audio(ffprobe, output)
    errors = []
    if (width, height) != (args.width, args.height):
        errors.append(f"wrong dimensions: {width}x{height}")
    if duration <= 0:
        errors.append("duration is zero")
    if args.audio_required and not audio_present:
        errors.append("audio is required but missing")
    if errors:
        print(json.dumps({"status": "failed", "output": str(output), "errors": errors}, indent=2))
        return 2
    print(json.dumps({"status": "success", "output": str(output), "width": width, "height": height, "duration": duration, "audio": audio_present}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


def audit_pipeline_script() -> str:
    return r'''#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import re
import sys


SECRET_RE = re.compile(r"(sk_[A-Za-z0-9_-]{12,}|api[_-]?key\s*[:=]\s*['\"][^'\"]{8,}|token\s*[:=]\s*['\"][^'\"]{8,})", re.IGNORECASE)
MEDIA_SUFFIXES = {".mp4", ".mov", ".m4v", ".wav", ".mp3", ".aac"}
ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_json(path: pathlib.Path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    errors: list[str] = []
    required = [
        "SKILL.md",
        "AGENT_RUNBOOK.md",
        "SYSTEM.md",
        "START_HERE.md",
        ".env.example",
        "config/project.json",
        "config/pipeline.json",
        "config/video.json",
        "config/providers.json",
        "config/export.json",
        "scripts/setup_check.py",
        "scripts/export_mp4.py",
    ]
    for rel in required:
        if not (ROOT / rel).exists():
            errors.append(f"Missing {rel}")
    try:
        pipeline = load_json(ROOT / "config" / "pipeline.json")
        export = load_json(ROOT / "config" / "export.json")
    except Exception as exc:
        errors.append(f"Config read failed: {exc}")
        pipeline = {}
        export = {}
    if export.get("container") != "mp4":
        errors.append("config/export.json container must be mp4")
    central = ROOT / "skills" / str(pipeline.get("pipeline_slug", "")) / "SKILL.md"
    if not central.exists():
        errors.append("Missing central nested skill SKILL.md")
    for stage in pipeline.get("stages", []):
        slug = stage.get("slug")
        if slug and not (central.parent / "subskills" / slug / "SKILL.md").exists():
            errors.append(f"Missing subskill for stage: {slug}")
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in MEDIA_SUFFIXES and ".gitkeep" not in path.name:
            errors.append(f"Generated media should not be in template: {path.relative_to(ROOT)}")
        if path.is_file() and path.suffix.lower() in {".md", ".json", ".txt", ".py", ".example"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
            if SECRET_RE.search(text):
                errors.append(f"Possible secret in {path.relative_to(ROOT)}")
    status = "blocked" if errors else "success"
    print(json.dumps({"status": status, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
'''


def scaffold(args: argparse.Namespace) -> pathlib.Path:
    spec_path = pathlib.Path(args.spec)
    spec = load_spec(spec_path)
    name = str(spec.get("pipeline_name") or args.name).strip() or args.name
    slug = slugify(name)
    output = pathlib.Path(args.output).expanduser().resolve()

    if output.exists():
        if not args.force:
            raise SystemExit(f"Target exists. Use --force to overwrite: {output}")
        shutil.rmtree(output)
    output.mkdir(parents=True)

    providers = providers_from_spec(spec)
    stages = spec.get("stages") if isinstance(spec.get("stages"), list) else infer_stages(spec)
    export_cfg = spec.get("export", {}) if isinstance(spec.get("export"), dict) else {}
    width = int(export_cfg.get("width", spec.get("width", 1080)))
    height = int(export_cfg.get("height", spec.get("height", 1920)))
    fps = int(export_cfg.get("fps", spec.get("fps", 30)))

    write(output / "SKILL.md", root_skill_text(name, slug))
    write(output / "START_HERE.md", start_here_text(name))
    write(output / "SYSTEM.md", system_text(name))
    write(output / "AGENT_RUNBOOK.md", runbook_text(name, stages))
    write(output / ".env.example", env_example(providers))
    write(
        output / ".gitignore",
        ".env\n.DS_Store\n__pycache__/\n*.pyc\noutput/drafts/*\noutput/approved/*\noutput/published/*\n!output/drafts/.gitkeep\n!output/approved/.gitkeep\n!output/published/.gitkeep\n",
    )

    write_json(
        output / "config" / "project.json",
        {
            "project_name": name,
            "pipeline_slug": slug,
            "primary_audience": spec.get("primary_audience", "Replace with audience"),
            "target_platforms": spec.get("target_platforms", spec.get("platforms", [])),
            "timezone": spec.get("timezone", "UTC"),
        },
    )
    write_json(
        output / "config" / "pipeline.json",
        {
            "pipeline_name": name,
            "pipeline_slug": slug,
            "content_source_mode": normalize_choice(spec, "content_source_mode", "manual_script"),
            "script_mode": normalize_choice(spec, "script_mode", "manual_script"),
            "media_construction_method": normalize_choice(spec, "media_construction_method", normalize_choice(spec, "media_method", "generated_clips")),
            "audio_mode": normalize_choice(spec, "audio_mode", "none"),
            "captions_mode": normalize_choice(spec, "captions_mode", "none"),
            "approval_gates": list_value(spec, "approval_gates"),
            "stages": stages,
        },
    )
    write_json(
        output / "config" / "video.json",
        {
            "width": width,
            "height": height,
            "fps": fps,
            "duration_seconds_target": spec.get("duration_seconds_target", None),
            "aspect_ratio": spec.get("aspect_ratio", f"{width}:{height}"),
            "media_construction_method": normalize_choice(spec, "media_construction_method", normalize_choice(spec, "media_method", "generated_clips")),
            "audio_mode": normalize_choice(spec, "audio_mode", "none"),
            "captions_mode": normalize_choice(spec, "captions_mode", "none"),
            "scale_mode": export_cfg.get("scale_mode", "cover"),
        },
    )
    write_json(output / "config" / "providers.json", {"providers": providers})
    write_json(
        output / "config" / "export.json",
        {
            "container": "mp4",
            "video_codec": "libx264",
            "audio_codec": "aac",
            "pixel_format": "yuv420p",
            "width": width,
            "height": height,
            "fps": fps,
            "scale_mode": export_cfg.get("scale_mode", "cover"),
            "image_duration_seconds": export_cfg.get("image_duration_seconds", 3.0),
            "audio_required": bool(export_cfg.get("audio_required", normalize_choice(spec, "audio_mode", "none") not in {"none", "silent", "no_voice"})),
            "ffmpeg_path": export_cfg.get("ffmpeg_path", "ffmpeg"),
            "ffprobe_path": export_cfg.get("ffprobe_path", "ffprobe"),
            "qa_rules": spec.get("qa_rules", ["final file exists", "final file is .mp4", "ffprobe verifies dimensions and non-zero duration"]),
        },
    )

    central_dir = output / "skills" / slug
    write(central_dir / "SKILL.md", central_skill_text(name, slug, stages))
    for stage in stages:
        write(central_dir / "subskills" / stage["slug"] / "SKILL.md", subskill_text(stage))

    write(output / "scripts" / "setup_check.py", setup_check_script())
    write(output / "scripts" / "export_mp4.py", export_mp4_script())
    write(output / "scripts" / "audit_pipeline.py", audit_pipeline_script())

    for rel in ("output/drafts/.gitkeep", "output/approved/.gitkeep", "output/published/.gitkeep"):
        write(output / rel, "")

    return output


def main() -> int:
    output = scaffold(parse_args())
    print(json.dumps({"status": "success", "pipeline_path": str(output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
