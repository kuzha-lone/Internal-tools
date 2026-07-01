#!/usr/bin/env python3
"""Audit a custom short-form video pipeline folder."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from typing import Any


SECRET_RE = re.compile(
    r"(sk_[A-Za-z0-9_-]{12,}|api[_-]?key\s*[:=]\s*['\"][^'\"]{8,}|token\s*[:=]\s*['\"][^'\"]{8,}|secret\s*[:=]\s*['\"][^'\"]{8,})",
    re.IGNORECASE,
)
MEDIA_SUFFIXES = {".mp4", ".mov", ".m4v", ".wav", ".mp3", ".aac", ".aiff"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit a generated short-form pipeline.")
    parser.add_argument("--path", required=True, help="Pipeline folder to audit.")
    return parser.parse_args()


def load_json(path: pathlib.Path) -> Any:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def is_placeholder_env_line(line: str) -> bool:
    if "=" not in line or line.strip().startswith("#"):
        return True
    _key, value = line.split("=", 1)
    stripped = value.strip().strip("\"'")
    return stripped == "" or "insert" in stripped.lower() or "replace" in stripped.lower()


def audit(root: pathlib.Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    required = [
        "SKILL.md",
        "AGENT_RUNBOOK.md",
        "SYSTEM.md",
        "START_HERE.md",
        ".env.example",
        ".gitignore",
        "config/project.json",
        "config/pipeline.json",
        "config/video.json",
        "config/providers.json",
        "config/export.json",
        "scripts/setup_check.py",
        "scripts/export_mp4.py",
        "scripts/audit_pipeline.py",
        "output/drafts/.gitkeep",
        "output/approved/.gitkeep",
        "output/published/.gitkeep",
    ]
    for rel in required:
        if not (root / rel).exists():
            errors.append(f"Missing {rel}")

    pipeline: dict[str, Any] = {}
    export: dict[str, Any] = {}
    providers: dict[str, Any] = {}
    for rel in ("config/project.json", "config/pipeline.json", "config/video.json", "config/providers.json", "config/export.json"):
        path = root / rel
        if not path.exists():
            continue
        try:
            data = load_json(path)
            if rel.endswith("pipeline.json"):
                pipeline = data
            elif rel.endswith("export.json"):
                export = data
            elif rel.endswith("providers.json"):
                providers = data
        except Exception as exc:
            errors.append(f"Invalid JSON in {rel}: {exc}")

    slug = str(pipeline.get("pipeline_slug", "")).strip()
    if not slug:
        errors.append("config/pipeline.json missing pipeline_slug")
    central = root / "skills" / slug / "SKILL.md" if slug else root / "skills" / "MISSING" / "SKILL.md"
    if not central.exists():
        errors.append("Missing nested central skill SKILL.md")

    stages = pipeline.get("stages", [])
    if not isinstance(stages, list) or not stages:
        errors.append("config/pipeline.json must define non-empty stages")
    else:
        stage_slugs = []
        for stage in stages:
            if not isinstance(stage, dict):
                errors.append("Every pipeline stage must be an object")
                continue
            stage_slug = str(stage.get("slug", "")).strip()
            stage_slugs.append(stage_slug)
            for key in ("purpose", "inputs", "outputs", "tool", "success_condition", "failure_condition"):
                if not str(stage.get(key, "")).strip():
                    errors.append(f"Stage {stage_slug or '<missing>'} missing {key}")
            if stage_slug and not (central.parent / "subskills" / stage_slug / "SKILL.md").exists():
                errors.append(f"Missing subskill for stage {stage_slug}")
        if "export-skill" not in stage_slugs:
            errors.append("Pipeline must include export-skill")
        if "qa-skill" not in stage_slugs:
            errors.append("Pipeline must include qa-skill")

    if export.get("container") != "mp4":
        errors.append("config/export.json container must be mp4")
    if export.get("video_codec") not in {"libx264", "h264", "h264_videotoolbox"}:
        warnings.append("Export video codec is unusual; expected libx264/h264.")
    if export.get("pixel_format") != "yuv420p":
        warnings.append("Pixel format should usually be yuv420p for compatibility.")

    env_example = root / ".env.example"
    if env_example.exists():
        for idx, line in enumerate(env_example.read_text(encoding="utf-8").splitlines(), start=1):
            if not is_placeholder_env_line(line):
                errors.append(f".env.example line {idx} appears to contain a real value")

    for provider in providers.get("providers", []) if isinstance(providers, dict) else []:
        if provider.get("required") and not provider.get("env"):
            warnings.append(f"Provider {provider.get('name')} is required but has no env vars listed")

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if path.suffix.lower() in MEDIA_SUFFIXES and path.name != ".gitkeep":
            errors.append(f"Generated media should not be in template: {rel}")
            continue
        if path.suffix.lower() in {".md", ".json", ".txt", ".py", ".example"} or path.name == ".env.example":
            text = path.read_text(encoding="utf-8", errors="ignore")
            if SECRET_RE.search(text):
                errors.append(f"Possible secret in {rel}")

    return {
        "status": "blocked" if errors else "success",
        "errors": errors,
        "warnings": warnings,
        "stage_count": len(stages) if isinstance(stages, list) else 0,
    }


def main() -> int:
    root = pathlib.Path(parse_args().path).expanduser().resolve()
    if not root.exists():
        print(json.dumps({"status": "blocked", "errors": [f"Path not found: {root}"]}, indent=2))
        return 1
    result = audit(root)
    print(json.dumps(result, indent=2))
    return 1 if result["status"] != "success" else 0


if __name__ == "__main__":
    sys.exit(main())
