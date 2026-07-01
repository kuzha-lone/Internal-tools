#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
import re
from pathlib import Path
from typing import Any

from media_utils import read_json, write_json


HOOK_PATTERNS = [
    r"\bwhy\b",
    r"\bhow\b",
    r"\bmistake\b",
    r"\bsecret\b",
    r"\btruth\b",
    r"\bproblem\b",
    r"\bimportant\b",
    r"\bmost people\b",
    r"\bno one\b",
    r"\bthe reason\b",
    r"\bhere'?s\b",
    r"\byou need\b",
    r"\byou should\b",
    r"\bstop\b",
    r"\bnever\b",
    r"\balways\b",
    r"\bfirst\b",
    r"\bsecond\b",
    r"\bthird\b",
    r"\bframework\b",
    r"\bworkflow\b",
    r"\bexample\b",
]

INTRO_OUTRO_PATTERNS = [
    r"\bwelcome back\b",
    r"\blike and subscribe\b",
    r"\bsponsor\b",
    r"\bad break\b",
    r"\bthanks for watching\b",
]

BAD_START = {"and", "but", "so", "because", "then", "also", "like"}


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def flatten_units(transcript: dict[str, Any]) -> list[dict[str, Any]]:
    units: list[dict[str, Any]] = []
    for segment in transcript.get("segments", []):
        text = normalize_text(segment.get("text", ""))
        if not text:
            continue
        units.append(
            {
                "start": float(segment.get("start", 0)),
                "end": float(segment.get("end", 0)),
                "text": text,
            }
        )
    return units


def window_text(units: list[dict[str, Any]], start_index: int, end_index: int) -> str:
    return normalize_text(" ".join(unit["text"] for unit in units[start_index:end_index]))


def score_window(text: str, duration: float, starts_at: float, target_duration: float) -> tuple[float, list[str]]:
    lower = text.lower()
    reasons: list[str] = []
    score = 0.0

    for pattern in HOOK_PATTERNS:
        matches = re.findall(pattern, lower)
        if matches:
            score += min(len(matches), 3) * 1.6
            label = pattern.replace("\\b", "").replace("\\", "")
            reasons.append(f"hook language: {label}")

    if "?" in text:
        score += 2.0
        reasons.append("question creates a hook")
    if "!" in text:
        score += 0.8
        reasons.append("emphatic delivery")

    for pattern in INTRO_OUTRO_PATTERNS:
        if re.search(pattern, lower):
            score -= 4.0
            reasons.append("intro/outro or sponsor language")

    words = re.findall(r"\w+", lower)
    if words:
        first_word = words[0]
        if first_word in BAD_START:
            score -= 1.5
            reasons.append("starts mid-thought")
        unique_ratio = len(set(words)) / max(1, len(words))
        score += unique_ratio * 2.0

    duration_penalty = abs(duration - target_duration) / max(target_duration, 1)
    score -= duration_penalty

    word_count = len(words)
    if word_count < 45:
        score -= 2.0
        reasons.append("likely too little context")
    elif word_count > 190:
        score -= 1.0
        reasons.append("dense segment")

    if starts_at < 20:
        score -= 0.8
        reasons.append("near source intro")

    if not reasons:
        reasons.append("coherent transcript window")

    return score, reasons[:4]


def build_candidates(
    transcript: dict[str, Any],
    count: int,
    min_duration: float,
    max_duration: float,
    target_duration: float,
    stride_segments: int,
) -> list[dict[str, Any]]:
    units = flatten_units(transcript)
    if not units:
        return []

    windows: list[dict[str, Any]] = []
    for start_index in range(0, len(units), max(1, stride_segments)):
        end_index = start_index + 1
        while end_index <= len(units):
            start = units[start_index]["start"]
            end = units[end_index - 1]["end"]
            duration = end - start
            if duration >= min_duration:
                text = window_text(units, start_index, end_index)
                score, reasons = score_window(text, duration, start, target_duration)
                windows.append(
                    {
                        "start": round(start, 3),
                        "end": round(end, 3),
                        "duration": round(duration, 3),
                        "score": round(score, 3),
                        "text": text,
                        "title": make_title(text),
                        "hook_text": make_hook(text),
                        "reason": "; ".join(reasons),
                    }
                )
            if duration >= max_duration:
                break
            end_index += 1

    windows.sort(key=lambda item: item["score"], reverse=True)
    selected: list[dict[str, Any]] = []
    for candidate in windows:
        if overlaps_existing(candidate, selected):
            continue
        selected.append(candidate)
        if len(selected) >= count:
            break

    for index, candidate in enumerate(selected, start=1):
        candidate["index"] = index
    selected.sort(key=lambda item: item["index"])
    return selected


def overlaps_existing(candidate: dict[str, Any], selected: list[dict[str, Any]]) -> bool:
    for item in selected:
        overlap = max(0.0, min(candidate["end"], item["end"]) - max(candidate["start"], item["start"]))
        if overlap / max(1.0, candidate["duration"]) > 0.35:
            return True
    return False


def make_title(text: str) -> str:
    words = re.findall(r"[A-Za-z0-9']+", text)
    if not words:
        return "Short clip"
    title = " ".join(words[:10])
    return title[:80].rstrip()


def make_hook(text: str) -> str:
    cleaned = normalize_text(re.sub(r"[^\w\s']", " ", text))
    words = cleaned.split()
    if not words:
        return "Watch this"
    hook = " ".join(words[:7])
    if len(hook) > 48:
        hook = hook[:48].rsplit(" ", 1)[0]
    return hook


def main() -> int:
    parser = argparse.ArgumentParser(description="Find short-form clip candidates from a transcript JSON.")
    parser.add_argument("--transcript", required=True, help="Transcript JSON from transcribe_source.py.")
    parser.add_argument("--out", required=True, help="Path to write clip candidate JSON.")
    parser.add_argument("--count", type=int, default=5, help="Number of candidates to keep.")
    parser.add_argument("--min-duration", type=float, default=18.0, help="Minimum clip duration in seconds.")
    parser.add_argument("--max-duration", type=float, default=60.0, help="Maximum clip duration in seconds.")
    parser.add_argument("--target-duration", type=float, default=38.0, help="Preferred clip duration.")
    parser.add_argument("--stride-segments", type=int, default=1, help="Segment stride for candidate windows.")
    args = parser.parse_args()

    transcript = read_json(args.transcript)
    clips = build_candidates(
        transcript,
        count=args.count,
        min_duration=args.min_duration,
        max_duration=args.max_duration,
        target_duration=args.target_duration,
        stride_segments=args.stride_segments,
    )
    output = {
        "source_transcript": str(Path(args.transcript).resolve()),
        "selection_method": "local_transcript_heuristic",
        "clips": clips,
    }
    write_json(args.out, output)
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
