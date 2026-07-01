#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, Sequence

from media_utils import ensure_dir, media_info, read_json, require_command, script_dir, write_json

DEFAULT_FONT_PATH = script_dir().parent / "assets" / "fonts" / "Sddystopiandemo-GO7xa.otf"
DEFAULT_FONT_NAME = "SDDystopianDemo"
DEFAULT_ACTIVE_WORD_COLOR = "#00d9ff"
DEFAULT_INACTIVE_WORD_COLOR = "#ffffff"


def normalize_word(text: str) -> str:
    return re.sub(r"[^\w']+", "", text.lower())


def clean_display_word(text: Any) -> str:
    return str(text or "").strip()


def extract_timed_words(transcript: dict[str, Any]) -> list[dict[str, Any]]:
    words: list[dict[str, Any]] = []

    if isinstance(transcript.get("words"), list):
        iterable = transcript["words"]
        for item in iterable:
            word_text = clean_display_word(item.get("word") or item.get("text"))
            normalized = normalize_word(word_text)
            start = item.get("start")
            end = item.get("end")
            if normalized and start is not None and end is not None:
                words.append(
                    {
                        "display": word_text,
                        "normalized": normalized,
                        "start": float(start),
                        "end": float(end),
                    }
                )

    for segment in transcript.get("segments", []) or []:
        for item in segment.get("words", []) or []:
            word_text = clean_display_word(item.get("word") or item.get("text"))
            normalized = normalize_word(word_text)
            start = item.get("start")
            end = item.get("end")
            if normalized and start is not None and end is not None:
                words.append(
                    {
                        "display": word_text,
                        "normalized": normalized,
                        "start": float(start),
                        "end": float(end),
                    }
                )

    deduped: list[dict[str, Any]] = []
    seen = set()
    for word in sorted(words, key=lambda item: (item["start"], item["end"], item["display"])):
        key = (round(word["start"], 3), round(word["end"], 3), word["normalized"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(word)

    if not deduped:
        raise SystemExit("Transcript does not contain word timestamps.")
    return deduped


def words_for_clip(
    timed_words: list[dict[str, Any]],
    *,
    clip: dict[str, Any],
    duration: float,
) -> list[dict[str, Any]]:
    cut_start = clip.get("cut_start")
    cut_end = clip.get("cut_end")
    if cut_start is None:
        cut_start = clip.get("source_start", 0.0)
    if cut_end is None:
        cut_end = float(cut_start) + duration

    clip_start = float(cut_start)
    clip_end = float(cut_end)
    selected: list[dict[str, Any]] = []
    for word in timed_words:
        absolute_start = float(word["start"])
        absolute_end = float(word["end"])
        if absolute_end <= clip_start or absolute_start >= clip_end:
            continue
        start = max(0.0, absolute_start - clip_start)
        end = min(duration, absolute_end - clip_start)
        if end <= start:
            end = min(duration, start + 0.08)
        if start >= duration:
            continue
        selected.append({**word, "start": start, "end": end})

    if selected:
        return normalize_token_times(selected, duration)

    # If the transcript was generated from the already-cut clip, timestamps may be clip-relative.
    clip_relative = [
        {**word, "start": max(0.0, float(word["start"])), "end": min(duration, float(word["end"]))}
        for word in timed_words
        if float(word["start"]) < duration and float(word["end"]) > 0
    ]
    if clip_relative:
        return normalize_token_times(clip_relative, duration)

    raise SystemExit(f"No transcript words matched clip index {clip.get('index')}.")


def normalize_token_times(tokens: list[dict[str, Any]], duration: float) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    previous_end = 0.0
    for token in sorted(tokens, key=lambda item: (item["start"], item["end"])):
        start = max(0.0, min(duration, float(token["start"])))
        end = max(start + 0.05, min(duration, float(token["end"])))
        if start < previous_end:
            start = previous_end
            end = max(start + 0.05, end)
        if start >= duration:
            continue
        end = min(duration, end)
        normalized.append({**token, "start": start, "end": end})
        previous_end = end
    return normalized


def chunk_three_word_highlight_tokens(
    tokens: list[dict[str, Any]],
    *,
    duration: float,
    max_gap: float,
    hold_sec: float,
) -> list[dict[str, Any]]:
    groups: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    for token in tokens:
        if current:
            gap = float(token["start"]) - float(current[-1]["end"])
            if len(current) >= 3 or gap > max_gap:
                groups.append(current)
                current = []
        current.append(token)
    if current:
        groups.append(current)

    cues: list[dict[str, Any]] = []
    for group_index, group in enumerate(groups):
        words = [token["display"] for token in group]
        next_group_start = (
            float(groups[group_index + 1][0]["start"]) if group_index + 1 < len(groups) else duration
        )
        group_end = min(duration, next_group_start, float(group[-1]["end"]) + hold_sec)
        for active_index, token in enumerate(group):
            next_start = group[active_index + 1]["start"] if active_index + 1 < len(group) else group_end
            start = max(0.0, float(token["start"]))
            end = min(duration, max(start + 0.08, float(next_start)))
            if end <= start:
                continue
            cues.append(
                {
                    "start": start,
                    "end": end,
                    "words": words,
                    "active_index": active_index,
                    "text": " ".join(words),
                }
            )
    return normalize_cue_timing(cues, duration)


def normalize_cue_timing(cues: list[dict[str, Any]], duration: float) -> list[dict[str, Any]]:
    duration_cs = max(0, int(round(duration * 100)))
    previous_end_cs = 0
    normalized: list[dict[str, Any]] = []
    for cue in sorted(cues, key=lambda item: (float(item["start"]), float(item["end"]))):
        start_cs = max(previous_end_cs, int(round(float(cue["start"]) * 100)))
        if start_cs >= duration_cs:
            continue
        end_cs = max(start_cs + 4, int(round(float(cue["end"]) * 100)))
        end_cs = min(duration_cs, end_cs)
        if end_cs <= start_cs:
            continue
        normalized.append({**cue, "start": start_cs / 100.0, "end": end_cs / 100.0})
        previous_end_cs = end_cs
    return normalized


def ass_timestamp(seconds: float) -> str:
    centiseconds = max(0, int(round(seconds * 100)))
    hours = centiseconds // 360000
    minutes = (centiseconds % 360000) // 6000
    secs = (centiseconds % 6000) // 100
    centis = centiseconds % 100
    return f"{hours}:{minutes:02d}:{secs:02d}.{centis:02d}"


def escape_ass_text(text: str) -> str:
    escaped = text.replace("\\", r"\\")
    escaped = escaped.replace("{", "(").replace("}", ")")
    return escaped


def ass_color_from_hex(value: str) -> str:
    cleaned = value.strip().lstrip("#")
    if len(cleaned) != 6 or not re.fullmatch(r"[0-9a-fA-F]{6}", cleaned):
        raise SystemExit(f"Invalid caption color: {value}")
    red = cleaned[0:2]
    green = cleaned[2:4]
    blue = cleaned[4:6]
    return f"&H00{blue}{green}{red}&".upper()


def split_index_for_caption(words: Sequence[str], max_line_chars: int) -> int | None:
    if len(words) <= 1 or len(" ".join(words)) <= max_line_chars:
        return None
    best_index: int | None = None
    best_score: tuple[int, int] | None = None
    for index in range(1, len(words)):
        first = " ".join(words[:index])
        second = " ".join(words[index:])
        score = (max(len(first), len(second)), abs(len(first) - len(second)))
        if best_score is None or score < best_score:
            best_score = score
            best_index = index
    return best_index


def highlighted_caption_text(
    words: Sequence[str],
    *,
    active_index: int,
    active_color: str,
    inactive_color: str,
    max_line_chars: int,
) -> str:
    split_index = split_index_for_caption(words, max_line_chars)
    parts: list[str] = []
    for index, word in enumerate(words):
        if split_index is not None and index == split_index:
            parts.append(r"\N")
        color = active_color if index == active_index else inactive_color
        parts.append(r"{\c" + color + "}" + escape_ass_text(word))
        if index < len(words) - 1:
            parts.append(" ")
    return "".join(parts)


def resolve_font_name(font_path: Path, override: str | None) -> str:
    if override:
        return override
    scanner = shutil.which("fc-scan")
    if scanner:
        result = subprocess.run(
            [scanner, "--format", "%{family}\n", str(font_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        family = result.stdout.strip().splitlines()
        if family and family[0].strip():
            return family[0].strip()
    return DEFAULT_FONT_NAME


def write_ass_subtitles(
    cues: list[dict[str, Any]],
    *,
    ass_path: Path,
    font_name: str,
    font_size: int,
    margin_v: int,
    active_word_color: str,
    inactive_word_color: str,
    max_line_chars: int,
) -> Path:
    ensure_dir(ass_path.parent)
    active_ass_color = ass_color_from_hex(active_word_color)
    inactive_ass_color = ass_color_from_hex(inactive_word_color)
    header = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,"
        "ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding",
        (
            "Style: Default,"
            f"{font_name},{font_size},&H00FFFFFF,&H000000FF,&H00000000,&H78000000,"
            f"1,0,0,0,100,100,0,0,1,5.4,1.2,2,80,80,{margin_v},1"
        ),
        "",
        "[Events]",
        "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text",
    ]
    event_lines = []
    for cue in cues:
        text = highlighted_caption_text(
            cue["words"],
            active_index=int(cue["active_index"]),
            active_color=active_ass_color,
            inactive_color=inactive_ass_color,
            max_line_chars=max_line_chars,
        )
        event_lines.append(
            "Dialogue: 0,"
            f"{ass_timestamp(float(cue['start']))},"
            f"{ass_timestamp(float(cue['end']))},"
            f"Default,,0,0,0,,{text}"
        )

    ass_path.write_text("\n".join(header + event_lines) + "\n", encoding="utf-8")
    return ass_path


def subtitle_filter_arg(ass_path: Path, font_dir: Path) -> str:
    ass_text = str(ass_path.resolve()).replace("\\", r"\\").replace("'", r"\'")
    font_text = str(font_dir.resolve()).replace("\\", r"\\").replace("'", r"\'")
    return f"subtitles=filename='{ass_text}':fontsdir='{font_text}'"


def burn_captions(
    *,
    input_path: Path,
    ass_path: Path,
    font_dir: Path,
    output_path: Path,
    crf: int,
    preset: str,
) -> Path:
    require_command("ffmpeg")
    ensure_dir(output_path.parent)
    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-vf",
        subtitle_filter_arg(ass_path, font_dir),
        "-c:v",
        "libx264",
        "-preset",
        preset,
        "-crf",
        str(crf),
        "-c:a",
        "copy",
        "-movflags",
        "+faststart",
        str(output_path),
    ]
    subprocess.run(command, check=True)
    return output_path


def caption_clip(
    *,
    clip: dict[str, Any],
    timed_words: list[dict[str, Any]],
    output_dir: Path,
    font_path: Path,
    font_name: str,
    font_size: int,
    margin_v: int,
    active_word_color: str,
    inactive_word_color: str,
    max_line_chars: int,
    max_gap: float,
    hold_sec: float,
    crf: int,
    preset: str,
) -> dict[str, Any]:
    index = int(clip["index"])
    input_path = Path(clip["vertical_path"]).expanduser().resolve()
    if not input_path.exists():
        raise SystemExit(f"Vertical clip does not exist for clip {index}: {input_path}")

    info = media_info(input_path)
    duration = float(info.get("duration_sec") or 0.0)
    if duration <= 0:
        raise SystemExit(f"Could not determine duration for clip {index}: {input_path}")

    tokens = words_for_clip(timed_words, clip=clip, duration=duration)
    cues = chunk_three_word_highlight_tokens(tokens, duration=duration, max_gap=max_gap, hold_sec=hold_sec)
    if not cues:
        raise SystemExit(f"No caption cues generated for clip {index}.")

    ass_path = output_dir / f"clip_{index:03d}_captions.ass"
    output_path = output_dir / f"clip_{index:03d}_captioned.mp4"
    clip_manifest_path = output_dir / f"clip_{index:03d}_caption_manifest.json"
    write_ass_subtitles(
        cues,
        ass_path=ass_path,
        font_name=font_name,
        font_size=font_size,
        margin_v=margin_v,
        active_word_color=active_word_color,
        inactive_word_color=inactive_word_color,
        max_line_chars=max_line_chars,
    )
    burn_captions(
        input_path=input_path,
        ass_path=ass_path,
        font_dir=font_path.parent,
        output_path=output_path,
        crf=crf,
        preset=preset,
    )
    output_info = media_info(output_path)
    result = {
        "index": index,
        "source_vertical_path": str(input_path),
        "captioned_path": str(output_path.resolve()),
        "ass_path": str(ass_path.resolve()),
        "caption_manifest_path": str(clip_manifest_path.resolve()),
        "cue_count": len(cues),
        "word_count": len(tokens),
        "style": {
            "mode": "three-word-highlight",
            "position": "lower-third-centered",
            "font_path": str(font_path.resolve()),
            "font_name": font_name,
            "font_size": font_size,
            "margin_v": margin_v,
            "active_word_color": active_word_color,
            "inactive_word_color": inactive_word_color,
            "max_line_chars": max_line_chars,
        },
        "output_media": output_info,
    }
    write_json(clip_manifest_path, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Burn lower-third active-word captions into vertical clips.")
    parser.add_argument("--manifest", required=True, help="Project manifest from make_manifest.py.")
    parser.add_argument("--transcript", help="Transcript JSON. Defaults to manifest transcript_path.")
    parser.add_argument("--out-dir", help="Caption output directory. Defaults to <workdir>/captioned.")
    parser.add_argument("--out", help="Caption outputs JSON. Defaults to <out-dir>/caption_outputs.json.")
    parser.add_argument("--clip-index", type=int, action="append", help="Only caption this clip index. May be repeated.")
    parser.add_argument("--font-file", default=str(DEFAULT_FONT_PATH))
    parser.add_argument("--font-name", help="ASS font family name. Defaults to detected family or SDDystopianDemo.")
    parser.add_argument("--font-size", type=int, default=62)
    parser.add_argument("--margin-v", type=int, default=360, help="ASS bottom margin. 360 centers captions in lower third.")
    parser.add_argument("--active-word-color", default=DEFAULT_ACTIVE_WORD_COLOR)
    parser.add_argument("--inactive-word-color", default=DEFAULT_INACTIVE_WORD_COLOR)
    parser.add_argument("--max-line-chars", type=int, default=24)
    parser.add_argument("--max-gap", type=float, default=0.65)
    parser.add_argument("--hold-sec", type=float, default=0.08)
    parser.add_argument("--crf", type=int, default=18)
    parser.add_argument("--preset", default="medium")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    manifest = read_json(manifest_path)
    workdir = Path(manifest.get("workdir") or manifest_path.parent).expanduser().resolve()
    transcript_path = Path(args.transcript).expanduser().resolve() if args.transcript else Path(
        manifest["transcript_path"]
    ).expanduser().resolve()
    transcript = read_json(transcript_path)
    timed_words = extract_timed_words(transcript)

    output_dir = ensure_dir(Path(args.out_dir).expanduser() if args.out_dir else workdir / "captioned").resolve()
    font_path = Path(args.font_file).expanduser().resolve()
    if not font_path.exists():
        raise SystemExit(f"Caption font file not found: {font_path}")
    font_name = resolve_font_name(font_path, args.font_name)

    selected_indexes = set(args.clip_index or [])
    clips = [
        clip
        for clip in manifest.get("clips", [])
        if clip.get("vertical_path") and (not selected_indexes or int(clip["index"]) in selected_indexes)
    ]
    if not clips:
        raise SystemExit("No captionable vertical clips found in manifest.")

    results = [
        caption_clip(
            clip=clip,
            timed_words=timed_words,
            output_dir=output_dir,
            font_path=font_path,
            font_name=font_name,
            font_size=args.font_size,
            margin_v=args.margin_v,
            active_word_color=args.active_word_color,
            inactive_word_color=args.inactive_word_color,
            max_line_chars=args.max_line_chars,
            max_gap=args.max_gap,
            hold_sec=args.hold_sec,
            crf=args.crf,
            preset=args.preset,
        )
        for clip in clips
    ]

    report = {
        "status": "success",
        "manifest_path": str(manifest_path),
        "transcript_path": str(transcript_path),
        "output_dir": str(output_dir),
        "clip_count": len(results),
        "clips": results,
    }
    out_path = Path(args.out).expanduser() if args.out else output_dir / "caption_outputs.json"
    write_json(out_path, report)
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
