#!/usr/bin/env python3
"""Generate an image using BFL Flux 2 Pro API with async polling."""

import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error


def main():
    parser = argparse.ArgumentParser(description="Generate image via Flux 2 Pro")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--width", type=int, default=1080, help="Image width (default: 1080)")
    parser.add_argument("--height", type=int, default=1920, help="Image height (default: 1920)")
    parser.add_argument("--image", help="Reference image path for character consistency (image-to-image)")
    parser.add_argument("--out", required=True, help="Output file path")
    args = parser.parse_args()

    api_key = os.environ.get("BFL_API_KEY")
    if not api_key:
        print("Error: BFL_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    # Step 1: Submit generation request
    payload = {
        "prompt": args.prompt,
        "width": args.width,
        "height": args.height,
    }
    if args.image:
        print(f"Using reference image: {args.image}")
        with open(args.image, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        payload["input_image"] = f"data:image/png;base64,{b64}"

    print(f"Submitting image generation request ({args.width}x{args.height})...")
    req_data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        "https://api.bfl.ai/v1/flux-2-pro",
        method="POST",
        headers={
            "accept": "application/json",
            "x-key": api_key,
            "Content-Type": "application/json",
        },
        data=req_data,
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"Error submitting request: HTTP {e.code} - {body}", file=sys.stderr)
        sys.exit(1)

    request_id = result["id"]
    polling_url = result.get("polling_url", f"https://api.bfl.ai/v1/get_result?id={request_id}")
    print(f"Request ID: {request_id}")
    print(f"Polling URL: {polling_url}")

    # Step 2: Poll until ready (timeout: 120s)
    timeout = 120
    start = time.time()
    poll_interval = 3

    while time.time() - start < timeout:
        time.sleep(poll_interval)

        poll_req = urllib.request.Request(
            f"{polling_url}?id={request_id}" if "?" not in polling_url else polling_url,
            method="GET",
            headers={
                "accept": "application/json",
                "x-key": api_key,
            },
        )

        try:
            with urllib.request.urlopen(poll_req, timeout=15) as resp:
                poll_result = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            print(f"Poll error: HTTP {e.code} - {body}", file=sys.stderr)
            continue

        status = poll_result.get("status", "Unknown")
        print(f"Status: {status} ({int(time.time() - start)}s elapsed)")

        if status == "Ready":
            image_url = poll_result["result"]["sample"]
            print(f"Image ready. Downloading...")

            # Step 3: Download the image (URL valid for 10 minutes)
            dl_req = urllib.request.Request(image_url)
            with urllib.request.urlopen(dl_req, timeout=60) as dl_resp:
                image_data = dl_resp.read()

            # Ensure output directory exists
            out_dir = os.path.dirname(args.out)
            if out_dir:
                os.makedirs(out_dir, exist_ok=True)

            with open(args.out, "wb") as f:
                f.write(image_data)

            print(f"Image saved to {args.out} ({len(image_data)} bytes)")
            return

        elif status in ("Error", "Failed"):
            print(f"Generation failed: {json.dumps(poll_result, indent=2)}", file=sys.stderr)
            sys.exit(1)

    print(f"Timeout: generation did not complete within {timeout}s", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
