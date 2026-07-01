#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from media_utils import write_json


def transcribe_with_faster_whisper(
    input_path: str,
    model_name: str,
    device: str,
    compute_type: str,
) -> dict[str, Any]:
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise SystemExit(
            "faster-whisper is not installed. Install it or provide an existing transcript JSON."
        ) from exc

    model = WhisperModel(model_name, device=device, compute_type=compute_type)
    segments_iter, info = model.transcribe(input_path, word_timestamps=True)

    segments: list[dict[str, Any]] = []
    full_text_parts: list[str] = []
    for index, segment in enumerate(segments_iter):
        words = []
        for word in segment.words or []:
            words.append(
                {
                    "word": word.word,
                    "start": float(word.start),
                    "end": float(word.end),
                    "probability": float(word.probability) if word.probability is not None else None,
                }
            )
        segments.append(
            {
                "id": index,
                "start": float(segment.start),
                "end": float(segment.end),
                "text": segment.text.strip(),
                "words": words,
            }
        )
        full_text_parts.append(segment.text.strip())

    return {
        "source_path": str(Path(input_path).resolve()),
        "engine": "faster-whisper",
        "model": model_name,
        "language": getattr(info, "language", None),
        "language_probability": getattr(info, "language_probability", None),
        "duration_sec": getattr(info, "duration", None),
        "text": " ".join(part for part in full_text_parts if part),
        "segments": segments,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Transcribe a source video/audio file with local faster-whisper.")
    parser.add_argument("--input", required=True, help="Path to source media.")
    parser.add_argument("--out", required=True, help="Path to transcript JSON.")
    parser.add_argument("--model", default="base", help="faster-whisper model name. Default: base.")
    parser.add_argument("--device", default="cpu", help="faster-whisper device. Default: cpu.")
    parser.add_argument("--compute-type", default="int8", help="faster-whisper compute type. Default: int8.")
    args = parser.parse_args()

    transcript = transcribe_with_faster_whisper(args.input, args.model, args.device, args.compute_type)
    write_json(args.out, transcript)
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

