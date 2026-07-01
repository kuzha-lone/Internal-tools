#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

from media_utils import ensure_dir, read_json, script_dir, write_json


def run_step(command: list[str]) -> None:
    print(" ".join(command), flush=True)
    subprocess.run(command, check=True)


def py_script(name: str) -> str:
    return str(script_dir() / name)


def is_youtube_url(value: str | None) -> bool:
    if not value:
        return False
    parsed = urlparse(value)
    host = parsed.netloc.lower().removeprefix("www.")
    return host in {"youtube.com", "youtu.be", "music.youtube.com", "youtube-nocookie.com"} or host.endswith(
        ".youtube.com"
    )


def default_youtube_auth_dir() -> Path:
    return Path.home() / ".cache" / "clipping-skill" / "youtube"


def run_youtube_auth(args: argparse.Namespace, auth_dir: Path) -> Path:
    cookies_path = auth_dir / "youtube.cookies.txt"
    command = [
        sys.executable,
        py_script("youtube_auth.py"),
        "--profile-dir",
        str(auth_dir / "profile"),
        "--cookies-out",
        str(cookies_path),
        "--timeout",
        str(args.youtube_auth_timeout),
    ]
    if args.youtube_auth_browser_channel:
        command.extend(["--browser-channel", args.youtube_auth_browser_channel])
    run_step(command)
    return cookies_path


def build_ingest_cmd(
    args: argparse.Namespace,
    workdir: Path,
    *,
    managed_cookies: Path | None = None,
) -> list[str]:
    ingest_cmd = [sys.executable, py_script("ingest_source.py"), "--workdir", str(workdir)]
    if args.file:
        ingest_cmd.extend(["--file", args.file])
    else:
        ingest_cmd.extend(["--url", args.url])
        if args.cookies:
            ingest_cmd.extend(["--cookies", args.cookies])
        elif managed_cookies:
            ingest_cmd.extend(["--cookies", str(managed_cookies)])
        elif args.cookies_from_browser:
            ingest_cmd.extend(["--cookies-from-browser", args.cookies_from_browser])
        if args.download_format:
            ingest_cmd.extend(["--download-format", args.download_format])
        if args.extractor_args:
            ingest_cmd.extend(["--extractor-args", args.extractor_args])
        if args.js_runtimes:
            ingest_cmd.extend(["--js-runtimes", args.js_runtimes])
        if args.remote_components:
            ingest_cmd.extend(["--remote-components", args.remote_components])
    ingest_cmd.extend(["--min-source-short-edge", str(args.min_source_short_edge)])
    if args.allow_low_res:
        ingest_cmd.append("--allow-low-res")
    return ingest_cmd


def run_ingest(args: argparse.Namespace, workdir: Path) -> None:
    managed_cookies: Path | None = None
    should_use_youtube_auth = bool(args.url and args.youtube_auth and is_youtube_url(args.url) and not args.cookies)
    if should_use_youtube_auth:
        auth_dir = ensure_dir(Path(args.youtube_auth_dir).expanduser()) if args.youtube_auth_dir else ensure_dir(
            default_youtube_auth_dir()
        )
        existing_cookies = auth_dir / "youtube.cookies.txt"
        if existing_cookies.exists():
            managed_cookies = existing_cookies

    try:
        run_step(build_ingest_cmd(args, workdir, managed_cookies=managed_cookies))
        return
    except subprocess.CalledProcessError:
        if not should_use_youtube_auth:
            raise

    print("YouTube HD ingest failed. Opening managed YouTube auth browser and retrying.", flush=True)
    managed_cookies = run_youtube_auth(args, auth_dir)
    run_step(build_ingest_cmd(args, workdir, managed_cookies=managed_cookies))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the complete URL/file to vertical short-form clip pipeline.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", help="Local source video path.")
    source.add_argument("--url", help="User-provided video URL.")
    parser.add_argument("--workdir", default="clipping_work", help="Working directory.")
    parser.add_argument("--clips", type=int, default=5, help="Number of candidate clips to generate.")
    parser.add_argument("--min-duration", type=float, default=18.0)
    parser.add_argument("--max-duration", type=float, default=60.0)
    parser.add_argument("--target-duration", type=float, default=38.0)
    parser.add_argument("--transcript", help="Existing transcript JSON to use instead of transcribing.")
    parser.add_argument("--transcribe-model", default="base")
    parser.add_argument("--transcribe-device", default="cpu")
    parser.add_argument("--transcribe-compute-type", default="int8")
    parser.add_argument("--height", type=int, default=1920)
    parser.add_argument("--native-height", action="store_true")
    parser.add_argument("--wide-mode", choices=["blur", "letterbox"], default="blur")
    parser.add_argument("--yolo-model", help="YOLO model weights path. Defaults to assets/models/yolov8n.pt.")
    parser.add_argument("--no-captions", action="store_true", help="Skip lower-third caption burn-in.")
    parser.add_argument("--caption-font-file", help="Caption font file. Defaults to assets/fonts/Sddystopiandemo-GO7xa.otf.")
    parser.add_argument("--caption-font-name", help="ASS caption font family name override.")
    parser.add_argument("--caption-font-size", type=int, default=62)
    parser.add_argument("--caption-margin-v", type=int, default=360, help="ASS bottom margin for lower-third captions.")
    parser.add_argument("--caption-active-word-color", default="#00d9ff")
    parser.add_argument("--caption-inactive-word-color", default="#ffffff")
    parser.add_argument("--caption-max-line-chars", type=int, default=24)
    parser.add_argument("--keep-source", action="store_true", help="Keep workdir/source.mp4 after pipeline completes.")
    parser.add_argument(
        "--cookies-from-browser",
        help="Pass browser cookies to yt-dlp for HD YouTube formats, e.g. chrome, safari, firefox.",
    )
    parser.add_argument("--cookies", help="Pass a Netscape-format cookies.txt file to yt-dlp.")
    parser.add_argument("--download-format", help="Override yt-dlp format selector for URL ingestion.")
    parser.add_argument("--extractor-args", help="Override yt-dlp extractor args for URL ingestion.")
    parser.add_argument("--js-runtimes", help="Override yt-dlp JS runtime setting for URL ingestion.")
    parser.add_argument("--remote-components", help="Override yt-dlp remote component setting for URL ingestion.")
    parser.add_argument("--min-source-short-edge", type=int, default=720, help="Minimum source short edge in pixels.")
    parser.add_argument("--allow-low-res", action="store_true", help="Allow sources below HD. Intended only for debugging.")
    parser.add_argument(
        "--youtube-auth",
        action="store_true",
        help="For YouTube URLs, use a skill-owned login browser and cookies file when HD ingest is blocked.",
    )
    parser.add_argument(
        "--youtube-auth-dir",
        help="Directory for the managed YouTube profile and cookies. Defaults to ~/.cache/clipping-skill/youtube.",
    )
    parser.add_argument(
        "--youtube-auth-timeout",
        type=int,
        default=900,
        help="Seconds to wait for YouTube sign-in during managed auth.",
    )
    parser.add_argument(
        "--youtube-auth-browser-channel",
        help="Optional Playwright browser channel for managed auth, e.g. chrome or msedge.",
    )
    args = parser.parse_args()

    workdir = ensure_dir(args.workdir).resolve()
    clips_dir = ensure_dir(workdir / "clips")
    vertical_dir = ensure_dir(workdir / "vertical")

    run_ingest(args, workdir)

    source_path = workdir / "source.mp4"
    source_info = read_json(workdir / "source_info.json")
    if source_info.get("path"):
        source_path = Path(source_info["path"])

    run_step(
        [
            sys.executable,
            py_script("probe_media.py"),
            "--input",
            str(source_path),
            "--out",
            str(workdir / "source_metadata.json"),
        ]
    )

    transcript_path = workdir / "transcript.json"
    if args.transcript:
        transcript_path.write_text(Path(args.transcript).expanduser().read_text(encoding="utf-8"), encoding="utf-8")
    else:
        run_step(
            [
                sys.executable,
                py_script("transcribe_source.py"),
                "--input",
                str(source_path),
                "--out",
                str(transcript_path),
                "--model",
                args.transcribe_model,
                "--device",
                args.transcribe_device,
                "--compute-type",
                args.transcribe_compute_type,
            ]
        )

    run_step(
        [
            sys.executable,
            py_script("find_clip_candidates.py"),
            "--transcript",
            str(transcript_path),
            "--out",
            str(workdir / "clip_candidates.json"),
            "--count",
            str(args.clips),
            "--min-duration",
            str(args.min_duration),
            "--max-duration",
            str(args.max_duration),
            "--target-duration",
            str(args.target_duration),
        ]
    )

    run_step(
        [
            sys.executable,
            py_script("cut_clips.py"),
            "--input",
            str(source_path),
            "--candidates",
            str(workdir / "clip_candidates.json"),
            "--out-dir",
            str(clips_dir),
        ]
    )

    cuts = read_json(clips_dir / "cuts.json")
    vertical_clips = []
    for clip in cuts.get("clips", []):
        index = int(clip["index"])
        horizontal_path = clip["horizontal_path"]
        vertical_path = vertical_dir / f"clip_{index:03d}_vertical.mp4"
        report_path = vertical_dir / f"clip_{index:03d}_vertical.json"
        command = [
            sys.executable,
            py_script("autocrop_vertical.py"),
            "--input",
            horizontal_path,
            "--output",
            str(vertical_path),
            "--report",
            str(report_path),
            "--height",
            str(args.height),
            "--wide-mode",
            args.wide_mode,
        ]
        if args.yolo_model:
            command.extend(["--yolo-model", args.yolo_model])
        if args.native_height:
            command.append("--native-height")
        run_step(command)
        vertical_clips.append(
            {
                "index": index,
                "horizontal_path": horizontal_path,
                "vertical_path": str(vertical_path.resolve()),
                "report_path": str(report_path.resolve()),
            }
        )

    write_json(vertical_dir / "vertical_outputs.json", {"clips": vertical_clips})

    manifest_path = workdir / "project_manifest.json"
    run_step(
        [
            sys.executable,
            py_script("make_manifest.py"),
            "--workdir",
            str(workdir),
            "--out",
            str(manifest_path),
        ]
    )

    if not args.no_captions:
        caption_cmd = [
            sys.executable,
            py_script("caption_clips.py"),
            "--manifest",
            str(manifest_path),
            "--font-size",
            str(args.caption_font_size),
            "--margin-v",
            str(args.caption_margin_v),
            "--active-word-color",
            args.caption_active_word_color,
            "--inactive-word-color",
            args.caption_inactive_word_color,
            "--max-line-chars",
            str(args.caption_max_line_chars),
        ]
        if args.caption_font_file:
            caption_cmd.extend(["--font-file", args.caption_font_file])
        if args.caption_font_name:
            caption_cmd.extend(["--font-name", args.caption_font_name])
        run_step(caption_cmd)
        run_step(
            [
                sys.executable,
                py_script("make_manifest.py"),
                "--workdir",
                str(workdir),
                "--out",
                str(manifest_path),
            ]
        )

    run_step(
        [
            sys.executable,
            py_script("qa_outputs.py"),
            "--manifest",
            str(manifest_path),
            "--out",
            str(workdir / "qa_report.json"),
        ]
    )
    run_step(
        [
            sys.executable,
            py_script("make_manifest.py"),
            "--workdir",
            str(workdir),
            "--out",
            str(manifest_path),
        ]
    )

    if not args.keep_source and args.url and source_path.exists():
        source_path.unlink()

    print(manifest_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
