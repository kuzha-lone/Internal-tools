#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlparse

from media_utils import ensure_dir, media_info, require_command, sanitize_filename, write_json

DEFAULT_YOUTUBE_EXTRACTOR_ARGS = None
DEFAULT_FORMAT = (
    "bv*[height>=720][height<=1080][vcodec^=avc1]+ba[ext=m4a]/"
    "bv*[height>=720][height<=1080]+ba/"
    "b[height>=720]"
)


def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def is_youtube_url(value: str) -> bool:
    parsed = urlparse(value)
    host = parsed.netloc.lower().removeprefix("www.")
    return host in {"youtube.com", "youtu.be", "music.youtube.com", "youtube-nocookie.com"} or host.endswith(
        ".youtube.com"
    )


def copy_file(source: str, output_path: Path) -> Path:
    source_path = Path(source).expanduser().resolve()
    if not source_path.exists():
        raise SystemExit(f"Input file does not exist: {source}")
    ensure_dir(output_path.parent)
    if source_path != output_path.resolve():
        shutil.copy2(source_path, output_path)
    return output_path


def download_url(
    url: str,
    output_dir: Path,
    *,
    cookies_from_browser: str | None = None,
    cookies: str | None = None,
    download_format: str = DEFAULT_FORMAT,
    extractor_args: str | None = DEFAULT_YOUTUBE_EXTRACTOR_ARGS,
    js_runtimes: str | None = None,
    remote_components: str | None = None,
) -> Path:
    ensure_dir(output_dir)
    require_command("yt-dlp")
    for stale_source in output_dir.glob("source.*"):
        if stale_source.is_file():
            stale_source.unlink()
    output_template = str(output_dir / "source.%(ext)s")
    command = [
        "yt-dlp",
        "--no-playlist",
        "--merge-output-format",
        "mp4",
        "--remux-video",
        "mp4",
        "-f",
        download_format,
        "-o",
        output_template,
    ]
    if extractor_args:
        command.extend(["--extractor-args", extractor_args])
    if js_runtimes is None and is_youtube_url(url) and shutil.which("node"):
        js_runtimes = "node"
    if js_runtimes:
        command.extend(["--js-runtimes", js_runtimes])
        if remote_components is None and is_youtube_url(url):
            remote_components = "ejs:github"
    if remote_components:
        command.extend(["--remote-components", remote_components])
    if cookies_from_browser:
        command.extend(["--cookies-from-browser", cookies_from_browser])
    if cookies:
        command.extend(["--cookies", cookies])
    command.append(url)
    subprocess.run(command, check=True)

    candidates = sorted(output_dir.glob("source.*"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not candidates:
        raise SystemExit("yt-dlp completed but no source file was found.")

    downloaded = candidates[0]
    final_path = output_dir / "source.mp4"
    if downloaded != final_path:
        if final_path.exists():
            final_path.unlink()
        downloaded.rename(final_path)
    return final_path


def enforce_source_quality(info: dict, min_short_edge: int, allow_low_res: bool) -> None:
    if allow_low_res or min_short_edge <= 0:
        return
    video = info.get("video", {})
    width = int(video.get("width") or 0)
    height = int(video.get("height") or 0)
    short_edge = min(width, height) if width and height else 0
    if short_edge >= min_short_edge:
        return
    raise SystemExit(
        f"Source is too low resolution ({width}x{height}). "
        f"This skill requires HD source by default: short edge >= {min_short_edge}px. "
        "For YouTube, rerun with --cookies-from-browser chrome/safari/firefox so yt-dlp can access HD streams, "
        "or provide the original HD file with --file. Use --allow-low-res only for debugging."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest a local video file or URL into a stable work directory.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", help="Local video file path.")
    group.add_argument("--url", help="Video URL. User-provided URLs are treated as intentionally supplied sources.")
    parser.add_argument("--workdir", default="clipping_work", help="Working directory for source and metadata.")
    parser.add_argument("--out", help="Final source path. Defaults to <workdir>/source.mp4.")
    parser.add_argument("--keep-original-name", action="store_true", help="Preserve local source basename when copying.")
    parser.add_argument(
        "--cookies-from-browser",
        help="Browser cookie source for yt-dlp, e.g. chrome, safari, firefox, or 'chrome:Profile 1'.",
    )
    parser.add_argument("--cookies", help="Netscape-format cookies.txt file for yt-dlp.")
    parser.add_argument("--download-format", default=DEFAULT_FORMAT, help="yt-dlp format selector for URL ingestion.")
    parser.add_argument("--extractor-args", default=DEFAULT_YOUTUBE_EXTRACTOR_ARGS, help="yt-dlp extractor args.")
    parser.add_argument("--js-runtimes", help="yt-dlp JS runtime setting. Defaults to node for YouTube when available.")
    parser.add_argument("--remote-components", help="yt-dlp remote component setting, e.g. ejs:github.")
    parser.add_argument("--min-source-short-edge", type=int, default=720, help="Minimum source short edge in pixels.")
    parser.add_argument("--allow-low-res", action="store_true", help="Allow sources below HD. Intended only for debugging.")
    args = parser.parse_args()

    workdir = ensure_dir(args.workdir)
    if args.out:
        output_path = Path(args.out).expanduser().resolve()
    elif args.keep_original_name and args.file:
        output_path = workdir / f"{sanitize_filename(Path(args.file).stem)}{Path(args.file).suffix or '.mp4'}"
    else:
        output_path = workdir / "source.mp4"

    if args.url:
        if not is_url(args.url):
            raise SystemExit(f"Invalid URL: {args.url}")
        source_path = download_url(
            args.url,
            output_path.parent,
            cookies_from_browser=args.cookies_from_browser,
            cookies=args.cookies,
            download_format=args.download_format,
            extractor_args=args.extractor_args,
            js_runtimes=args.js_runtimes,
            remote_components=args.remote_components,
        )
        if source_path != output_path:
            if output_path.exists():
                output_path.unlink()
            source_path.rename(output_path)
        source_type = "url"
        source_value = args.url
    else:
        source_path = copy_file(args.file, output_path)
        source_type = "file"
        source_value = str(Path(args.file).expanduser().resolve())

    info = media_info(source_path)
    enforce_source_quality(info, args.min_source_short_edge, args.allow_low_res)
    ingest = {
        "source_type": source_type,
        "source": source_value,
        "path": str(source_path.resolve()),
        "media": info,
    }
    write_json(workdir / "source_info.json", ingest)
    print(source_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
