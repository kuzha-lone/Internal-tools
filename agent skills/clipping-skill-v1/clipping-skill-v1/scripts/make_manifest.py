#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from media_utils import read_json, write_json


def read_optional(path: Path) -> Any:
    if path.exists():
        return read_json(path)
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an editing handoff manifest for generated short-form clips.")
    parser.add_argument("--workdir", required=True, help="Pipeline working directory.")
    parser.add_argument("--out", help="Manifest output path. Defaults to <workdir>/project_manifest.json.")
    args = parser.parse_args()

    workdir = Path(args.workdir).expanduser().resolve()
    source_info = read_optional(workdir / "source_info.json")
    source_probe = read_optional(workdir / "source_metadata.json")
    transcript = read_optional(workdir / "transcript.json")
    candidates = read_optional(workdir / "clip_candidates.json")
    cuts = read_optional(workdir / "clips" / "cuts.json")
    vertical_outputs = read_optional(workdir / "vertical" / "vertical_outputs.json")
    caption_outputs = read_optional(workdir / "captioned" / "caption_outputs.json")
    qa = read_optional(workdir / "qa_report.json")

    vertical_by_index = {}
    for item in (vertical_outputs or {}).get("clips", []):
        vertical_by_index[int(item["index"])] = item

    caption_by_index = {}
    for item in (caption_outputs or {}).get("clips", []):
        caption_by_index[int(item["index"])] = item

    clips = []
    for item in (cuts or {}).get("clips", []):
        index = int(item["index"])
        vertical = vertical_by_index.get(index, {})
        caption = caption_by_index.get(index, {})
        clips.append(
            {
                "index": index,
                "source_start": item.get("start"),
                "source_end": item.get("end"),
                "cut_start": item.get("cut_start"),
                "cut_end": item.get("cut_end"),
                "duration": item.get("duration"),
                "title": item.get("title"),
                "hook_text": item.get("hook_text"),
                "reason": item.get("reason"),
                "horizontal_path": item.get("horizontal_path"),
                "vertical_path": vertical.get("vertical_path"),
                "vertical_report": vertical.get("report_path"),
                "captioned_path": caption.get("captioned_path"),
                "caption_ass_path": caption.get("ass_path"),
                "caption_report": caption.get("caption_manifest_path"),
                "status": (
                    "ready_for_agent_edit_captioned"
                    if caption.get("captioned_path")
                    else "ready_for_agent_edit"
                    if vertical.get("vertical_path")
                    else "cut_only"
                ),
                "caption_handoff": {
                    "source": "transcript_words",
                    "instruction": "Captions use transcript word timestamps rebased to each cut; no separate caption API key is required.",
                },
            }
        )

    manifest = {
        "skill": "clipping-skill",
        "workflow": "url_or_file_to_short_form_vertical_clips",
        "workdir": str(workdir),
        "source": source_info,
        "source_probe": source_probe,
        "transcript_path": str((workdir / "transcript.json").resolve()) if transcript else None,
        "candidate_path": str((workdir / "clip_candidates.json").resolve()) if candidates else None,
        "cuts_path": str((workdir / "clips" / "cuts.json").resolve()) if cuts else None,
        "vertical_outputs_path": str((workdir / "vertical" / "vertical_outputs.json").resolve())
        if vertical_outputs
        else None,
        "caption_outputs_path": str((workdir / "captioned" / "caption_outputs.json").resolve())
        if caption_outputs
        else None,
        "qa_path": str((workdir / "qa_report.json").resolve()) if qa else None,
        "clips": clips,
        "next_editing_steps": [
            "review chosen moments",
            "review lower-third active-word captions",
            "add hook text overlays",
            "add b-roll, music, zooms, or branded styling",
            "export final platform-ready files",
        ],
    }
    out_path = Path(args.out) if args.out else workdir / "project_manifest.json"
    write_json(out_path, manifest)
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
