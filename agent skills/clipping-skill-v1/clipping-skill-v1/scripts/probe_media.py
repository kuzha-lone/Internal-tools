#!/usr/bin/env python3
from __future__ import annotations

import argparse

from media_utils import media_info, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe a media file with ffprobe and write normalized JSON metadata.")
    parser.add_argument("--input", required=True, help="Path to the media file.")
    parser.add_argument("--out", required=True, help="Path to write metadata JSON.")
    args = parser.parse_args()

    info = media_info(args.input)
    write_json(args.out, info)
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

