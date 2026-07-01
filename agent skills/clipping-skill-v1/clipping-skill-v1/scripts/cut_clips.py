#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from media_utils import ensure_dir, media_info, read_json, require_command, write_json


def cut_clip(source: Path, output_path: Path, start: float, end: float, crf: int, preset: str) -> None:
    require_command("ffmpeg")
    ensure_dir(output_path.parent)
    command = [
        "ffmpeg",
        "-y",
        "-ss",
        f"{start:.3f}",
        "-to",
        f"{end:.3f}",
        "-i",
        str(source),
        "-map",
        "0",
        "-c:v",
        "libx264",
        "-crf",
        str(crf),
        "-preset",
        preset,
        "-c:a",
        "aac",
        "-movflags",
        "+faststart",
        str(output_path),
    ]
    subprocess.run(command, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Cut candidate clips from a long source before vertical reframing.")
    parser.add_argument("--input", required=True, help="Source video path.")
    parser.add_argument("--candidates", required=True, help="Clip candidates JSON.")
    parser.add_argument("--out-dir", required=True, help="Directory for horizontal cut clips.")
    parser.add_argument("--out", help="Path to write cuts JSON. Defaults to <out-dir>/cuts.json.")
    parser.add_argument("--pre-roll", type=float, default=0.2, help="Seconds to include before candidate start.")
    parser.add_argument("--post-roll", type=float, default=0.2, help="Seconds to include after candidate end.")
    parser.add_argument("--crf", type=int, default=18)
    parser.add_argument("--preset", default="fast")
    args = parser.parse_args()

    source = Path(args.input).expanduser().resolve()
    candidates = read_json(args.candidates).get("clips", [])
    out_dir = ensure_dir(args.out_dir)
    report_clips = []

    for fallback_index, candidate in enumerate(candidates, start=1):
        index = int(candidate.get("index") or fallback_index)
        start = max(0.0, float(candidate["start"]) - args.pre_roll)
        end = max(start + 1.0, float(candidate["end"]) + args.post_roll)
        output_path = out_dir / f"clip_{index:03d}_horizontal.mp4"
        cut_clip(source, output_path, start, end, args.crf, args.preset)
        item = dict(candidate)
        item.update(
            {
                "index": index,
                "cut_start": round(start, 3),
                "cut_end": round(end, 3),
                "horizontal_path": str(output_path.resolve()),
                "horizontal_media": media_info(output_path),
            }
        )
        report_clips.append(item)

    report = {
        "source_path": str(source),
        "candidate_path": str(Path(args.candidates).resolve()),
        "clips": report_clips,
    }
    out_path = Path(args.out) if args.out else out_dir / "cuts.json"
    write_json(out_path, report)
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
