#!/usr/bin/env python3
"""Add TikTok-style text overlay to a video clip.

Renders text with Pillow onto a transparent PNG, then composites it onto the
video with ffmpeg's overlay filter. This avoids ffmpeg drawtext bugs with
newline rendering (box glyphs) in certain static builds.

Usage:
  python3 add-text-overlay.py --input clip.mp4 --text "hook text" --position bottom --out output.mp4
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import textwrap

from PIL import Image, ImageDraw, ImageFont


def find_font():
    """Find the best available font file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)
    candidates = [
        os.path.join(skill_dir, "assets", "fonts", "TikTokSans-Bold.ttf"),
        "/app/skills/ugc-video/assets/fonts/TikTokSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for f in candidates:
        if os.path.isfile(f):
            return f
    return None


def get_video_dimensions(input_path):
    """Get video width and height using ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_streams", "-select_streams", "v:0", input_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return 1080, 1920  # fallback to TikTok portrait
    try:
        info = json.loads(result.stdout)
        stream = info["streams"][0]
        return int(stream["width"]), int(stream["height"])
    except (json.JSONDecodeError, KeyError, IndexError):
        return 1080, 1920


def render_text_overlay(text, font_path, fontsize, position, width, height, max_chars):
    """Render text onto a transparent RGBA image using Pillow."""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if font_path:
        font = ImageFont.truetype(font_path, fontsize)
    else:
        font = ImageFont.load_default()

    wrapped = textwrap.fill(text, width=max_chars)
    print(f"Wrapped text:\n{wrapped}")

    # Compute Y anchor position based on --position
    if position == "top":
        y = int(height * 0.10)
        anchor = "ma"  # middle-horizontal, ascender
    elif position == "center":
        y = height // 2
        anchor = "mm"  # middle-horizontal, middle-vertical
    else:  # bottom
        y = int(height * 0.75)
        anchor = "mm"  # middle-horizontal, middle-vertical

    x = width // 2

    # Draw text with stroke (black outline, white fill)
    draw.text(
        (x, y),
        wrapped,
        font=font,
        fill="white",
        stroke_width=4,
        stroke_fill="black",
        anchor=anchor,
        align="center",
    )

    return img


def main():
    parser = argparse.ArgumentParser(description="Add text overlay to video")
    parser.add_argument("--input", required=True, help="Input video file")
    parser.add_argument("--text", required=True, help="Text to overlay")
    parser.add_argument("--position", default="bottom", choices=["top", "center", "bottom"])
    parser.add_argument("--out", required=True, help="Output video file")
    parser.add_argument("--fontsize", default=54, type=int)
    parser.add_argument("--max-chars", default=28, type=int, help="Max chars per line")
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Find font
    font_path = find_font()
    if font_path:
        print(f"Using font: {font_path}")
    else:
        print("Warning: No font found, using Pillow default", file=sys.stderr)

    # Get video dimensions so overlay matches exactly
    vid_w, vid_h = get_video_dimensions(args.input)
    print(f"Video dimensions: {vid_w}x{vid_h}")

    # Render text to transparent PNG
    overlay_img = render_text_overlay(
        args.text, font_path, args.fontsize,
        args.position, vid_w, vid_h, args.max_chars,
    )

    # Ensure output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)

    # Write overlay PNG to a temp file, composite with ffmpeg
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        overlay_path = tmp.name
        overlay_img.save(overlay_path, "PNG")

    try:
        print(f"Adding text overlay at {args.position}")
        print(f"Input: {args.input}")
        print(f"Output: {args.out}")

        cmd = [
            "ffmpeg", "-y",
            "-i", args.input,
            "-i", overlay_path,
            "-filter_complex", "overlay=0:0",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-c:a", "copy",
            args.out,
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)

        if result.returncode != 0:
            print(f"Error: ffmpeg exited with code {result.returncode}", file=sys.stderr)
            sys.exit(result.returncode)

        print(f"Text overlay complete: {args.out}")
    finally:
        os.unlink(overlay_path)


if __name__ == "__main__":
    main()
