#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def ensure_dir(path: str | Path) -> Path:
    target = Path(path)
    target.mkdir(parents=True, exist_ok=True)
    return target


def read_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: str | Path, data: Any) -> Path:
    target = Path(path)
    ensure_dir(target.parent)
    with target.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return target


def run_command(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, check=check)


def require_command(name: str) -> None:
    if shutil.which(name) is None:
        candidate_dirs = [
            Path(sys.executable).parent,
            Path(os.environ["VIRTUAL_ENV"]) / "bin" if os.environ.get("VIRTUAL_ENV") else None,
            script_dir().parent / ".venv" / "bin",
        ]
        for executable_dir in [item for item in candidate_dirs if item is not None]:
            local_command = executable_dir / name
            if local_command.exists() and os.access(local_command, os.X_OK):
                os.environ["PATH"] = f"{executable_dir}{os.pathsep}{os.environ.get('PATH', '')}"
                return
        raise SystemExit(f"Required command not found in PATH: {name}")


def sanitize_filename(value: str, fallback: str = "source") -> str:
    safe = re.sub(r'[<>:"/\\|?*\x00-\x1f#]+', "", value).strip()
    safe = re.sub(r"\s+", "_", safe)
    return (safe or fallback)[:120]


def parse_fps(value: str | None) -> float | None:
    if not value:
        return None
    if "/" in value:
        num, den = value.split("/", 1)
        try:
            denominator = float(den)
            if denominator == 0:
                return None
            return float(num) / denominator
        except ValueError:
            return None
    try:
        return float(value)
    except ValueError:
        return None


def ffprobe_json(path: str | Path) -> dict[str, Any]:
    require_command("ffprobe")
    result = run_command(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_format",
            "-show_streams",
            "-of",
            "json",
            str(path),
        ]
    )
    return json.loads(result.stdout)


def media_info(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    data = ffprobe_json(source)
    fmt = data.get("format", {})
    video_stream = None
    audio_stream = None

    for stream in data.get("streams", []):
        if stream.get("codec_type") == "video" and video_stream is None:
            video_stream = stream
        elif stream.get("codec_type") == "audio" and audio_stream is None:
            audio_stream = stream

    duration = None
    for candidate in (
        fmt.get("duration"),
        (video_stream or {}).get("duration"),
        (audio_stream or {}).get("duration"),
    ):
        if candidate not in (None, "N/A"):
            try:
                duration = float(candidate)
                break
            except ValueError:
                pass

    size_bytes = None
    if fmt.get("size"):
        try:
            size_bytes = int(fmt["size"])
        except ValueError:
            pass
    if size_bytes is None and source.exists():
        size_bytes = source.stat().st_size

    fps = parse_fps((video_stream or {}).get("avg_frame_rate")) or parse_fps(
        (video_stream or {}).get("r_frame_rate")
    )
    real_fps = parse_fps((video_stream or {}).get("r_frame_rate"))
    is_variable_frame_rate = False
    if fps and real_fps:
        is_variable_frame_rate = abs(real_fps - fps) > 0.5

    return {
        "path": str(source.resolve()),
        "exists": source.exists(),
        "size_bytes": size_bytes,
        "duration_sec": duration,
        "video": {
            "codec": (video_stream or {}).get("codec_name"),
            "width": (video_stream or {}).get("width"),
            "height": (video_stream or {}).get("height"),
            "fps": fps,
            "r_frame_rate": (video_stream or {}).get("r_frame_rate"),
            "avg_frame_rate": (video_stream or {}).get("avg_frame_rate"),
            "pix_fmt": (video_stream or {}).get("pix_fmt"),
            "start_time": (video_stream or {}).get("start_time"),
            "nb_frames": (video_stream or {}).get("nb_frames"),
            "is_variable_frame_rate": is_variable_frame_rate,
        },
        "audio": {
            "has_audio": audio_stream is not None,
            "codec": (audio_stream or {}).get("codec_name"),
            "sample_rate": (audio_stream or {}).get("sample_rate"),
            "channels": (audio_stream or {}).get("channels"),
            "start_time": (audio_stream or {}).get("start_time"),
        },
    }


def script_dir() -> Path:
    return Path(__file__).resolve().parent
