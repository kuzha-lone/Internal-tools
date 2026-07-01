#!/usr/bin/env python3
"""Generate a video from an image using MiniMax Hailuo 2.3 API with async polling."""

import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error

API_BASE = "https://api.minimax.io/v1"


def api_request(endpoint, api_key, method="GET", data=None, params=None):
    """Make an API request to MiniMax."""
    url = f"{API_BASE}/{endpoint}"
    if params:
        query = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{url}?{query}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    req = urllib.request.Request(url, method=method, headers=headers)
    if data:
        req.data = json.dumps(data).encode("utf-8")

    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    parser = argparse.ArgumentParser(description="Generate video via MiniMax Hailuo 2.3")
    parser.add_argument("--image", required=True, help="Input image file path")
    parser.add_argument("--prompt", required=True, help="Video motion prompt")
    parser.add_argument("--duration", type=int, default=6, choices=[6, 10], help="Video duration in seconds (default: 6)")
    parser.add_argument("--out", required=True, help="Output video file path")
    parser.add_argument("--model", default="MiniMax-Hailuo-2.3-Fast", help="Model name (default: MiniMax-Hailuo-2.3-Fast)")
    parser.add_argument("--resolution", default="1080P", help="Resolution (default: 1080P)")
    args = parser.parse_args()

    api_key = os.environ.get("MINIMAX_API_KEY")
    if not api_key:
        print("Error: MINIMAX_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.image):
        print(f"Error: Input image not found: {args.image}", file=sys.stderr)
        sys.exit(1)

    # Step 1: Read and base64-encode the image
    with open(args.image, "rb") as f:
        image_data = f.read()

    ext = os.path.splitext(args.image)[1].lower()
    mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
    mime_type = mime_map.get(ext, "image/png")

    image_b64 = base64.b64encode(image_data).decode("utf-8")
    data_uri = f"data:{mime_type};base64,{image_b64}"

    size_mb = len(image_data) / (1024 * 1024)
    print(f"Image loaded: {args.image} ({size_mb:.1f} MB, {mime_type})")

    if len(image_data) > 20 * 1024 * 1024:
        print("Error: Image exceeds 20MB limit", file=sys.stderr)
        sys.exit(1)

    # Step 2: Submit video generation task
    print(f"Submitting video generation task (model: {args.model}, duration: {args.duration}s)...")

    payload = {
        "model": args.model,
        "first_frame_image": data_uri,
        "prompt": args.prompt,
        "duration": args.duration,
        "resolution": args.resolution,
        "prompt_optimizer": True,
    }

    try:
        result = api_request("video_generation", api_key, method="POST", data=payload)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"Error submitting task: HTTP {e.code} - {body}", file=sys.stderr)
        sys.exit(1)

    if result.get("base_resp", {}).get("status_code", -1) != 0:
        print(f"Error: {json.dumps(result, indent=2)}", file=sys.stderr)
        sys.exit(1)

    task_id = result["task_id"]
    print(f"Task ID: {task_id}")

    # Step 3: Poll for completion (timeout: 300s)
    timeout = 300
    start = time.time()
    poll_interval = 10

    while time.time() - start < timeout:
        time.sleep(poll_interval)

        try:
            status_result = api_request(
                "query/video_generation", api_key,
                method="GET", params={"task_id": task_id}
            )
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            print(f"Poll error: HTTP {e.code} - {body}", file=sys.stderr)
            continue

        status = status_result.get("status", "Unknown")
        elapsed = int(time.time() - start)
        print(f"Status: {status} ({elapsed}s elapsed)")

        if status == "Success":
            file_id = status_result.get("file_id")
            if not file_id:
                print(f"Error: No file_id in response: {json.dumps(status_result)}", file=sys.stderr)
                sys.exit(1)

            print(f"Video ready (file_id: {file_id}). Retrieving download URL...")

            # Step 4: Get download URL from file_id
            try:
                file_result = api_request(
                    "files/retrieve", api_key,
                    method="GET", params={"file_id": file_id}
                )
            except urllib.error.HTTPError as e:
                body = e.read().decode("utf-8", errors="replace")
                print(f"Error retrieving file: HTTP {e.code} - {body}", file=sys.stderr)
                sys.exit(1)

            download_url = file_result.get("file", {}).get("download_url")
            if not download_url:
                print(f"Error: No download_url in response: {json.dumps(file_result)}", file=sys.stderr)
                sys.exit(1)

            # Step 5: Download the video
            print("Downloading video...")
            dl_req = urllib.request.Request(download_url)
            with urllib.request.urlopen(dl_req, timeout=120) as dl_resp:
                video_data = dl_resp.read()

            out_dir = os.path.dirname(args.out)
            if out_dir:
                os.makedirs(out_dir, exist_ok=True)

            with open(args.out, "wb") as f:
                f.write(video_data)

            print(f"Video saved to {args.out} ({len(video_data)} bytes)")
            return

        elif status == "Fail":
            print(f"Video generation failed: {json.dumps(status_result, indent=2)}", file=sys.stderr)
            sys.exit(1)

    print(f"Timeout: video generation did not complete within {timeout}s", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
