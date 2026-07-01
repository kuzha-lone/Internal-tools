#!/usr/bin/env python3
"""Template FFmpeg MP4 exporter. Use scaffold_shortform_pipeline.py for a filled version."""

from __future__ import annotations

import argparse


def main() -> int:
    parser = argparse.ArgumentParser(description="Export final MP4 with FFmpeg.")
    parser.add_argument("--help-template", action="store_true")
    parser.parse_args()
    print("Use the scaffolded pipeline's scripts/export_mp4.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
