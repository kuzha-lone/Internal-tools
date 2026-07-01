#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from media_utils import media_info, read_json, write_json


def collect_paths(manifest_path: Path | None, input_dir: Path | None) -> list[Path]:
    paths: list[Path] = []
    if manifest_path:
        manifest = read_json(manifest_path)
        for clip in manifest.get("clips", []):
            if clip.get("vertical_path"):
                paths.append(Path(clip["vertical_path"]))
            if clip.get("captioned_path"):
                paths.append(Path(clip["captioned_path"]))
    if input_dir:
        paths.extend(sorted(input_dir.glob("*.mp4")))
    deduped: list[Path] = []
    seen = set()
    for path in paths:
        resolved = str(path.expanduser().resolve())
        if resolved not in seen:
            seen.add(resolved)
            deduped.append(Path(resolved))
    return deduped


def main() -> int:
    parser = argparse.ArgumentParser(description="Run lightweight ffprobe QA on generated vertical videos.")
    parser.add_argument("--manifest", help="Project manifest path.")
    parser.add_argument("--input-dir", help="Directory of vertical MP4 outputs.")
    parser.add_argument("--out", required=True, help="QA report JSON path.")
    parser.add_argument("--expected-ratio", default="9:16", help="Expected W:H ratio. Default: 9:16.")
    parser.add_argument("--tolerance", type=float, default=0.02, help="Aspect ratio tolerance.")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser() if args.manifest else None
    input_dir = Path(args.input_dir).expanduser() if args.input_dir else None
    paths = collect_paths(manifest_path, input_dir)
    expected_w, expected_h = [float(part) for part in args.expected_ratio.split(":", 1)]
    expected_ratio = expected_w / expected_h

    checks = []
    for path in paths:
        info = media_info(path)
        video = info.get("video", {})
        width = video.get("width") or 0
        height = video.get("height") or 0
        ratio = (width / height) if height else 0
        ratio_ok = abs(ratio - expected_ratio) <= args.tolerance
        duration_ok = bool(info.get("duration_sec") and info["duration_sec"] > 0)
        checks.append(
            {
                "path": str(path),
                "width": width,
                "height": height,
                "duration_sec": info.get("duration_sec"),
                "has_audio": info.get("audio", {}).get("has_audio"),
                "ratio": ratio,
                "ratio_ok": ratio_ok,
                "duration_ok": duration_ok,
                "status": "ok" if ratio_ok and duration_ok else "warn",
            }
        )

    report = {
        "expected_ratio": args.expected_ratio,
        "clip_count": len(checks),
        "ok_count": sum(1 for check in checks if check["status"] == "ok"),
        "checks": checks,
    }
    write_json(args.out, report)
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
