#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from media_utils import ensure_dir, media_info, require_command, script_dir, write_json


DEFAULT_YOLO_MODEL_PATH = script_dir().parent / "assets" / "models" / "yolov8n.pt"


@dataclass
class ScenePlan:
    index: int
    start_frame: int
    end_frame: int
    start_sec: float
    end_sec: float
    strategy: str
    target_box: list[int] | None
    people_count: int


def lazy_imports():
    try:
        import cv2
        import numpy as np
    except ImportError as exc:
        raise SystemExit("opencv-python and numpy are required for vertical reframing.") from exc
    return cv2, np


def get_video_properties(video_path: str) -> tuple[int, int, float, int]:
    cv2, _ = lazy_imports()
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise SystemExit(f"Could not open video: {video_path}")
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = float(cap.get(cv2.CAP_PROP_FPS) or 30.0)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return width, height, fps, frame_count


def detect_scenes(video_path: str, fps: float, frame_count: int, threshold: float) -> list[tuple[int, int, float, float]]:
    try:
        from scenedetect import open_video, SceneManager
        from scenedetect.detectors import ContentDetector

        video = open_video(video_path)
        manager = SceneManager()
        manager.add_detector(ContentDetector(threshold=threshold))
        manager.detect_scenes(video=video)
        scene_list = manager.get_scene_list()
        scenes = []
        for start, end in scene_list:
            scenes.append(
                (
                    int(start.get_frames()),
                    int(end.get_frames()),
                    float(start.get_seconds()),
                    float(end.get_seconds()),
                )
            )
        if scenes:
            return scenes
    except Exception as exc:
        print(f"Scene detection unavailable, using one scene: {exc}", file=sys.stderr)

    duration = frame_count / fps if fps else 0.0
    return [(0, frame_count, 0.0, duration)]


def load_yolo(model_path: Path):
    try:
        from ultralytics import YOLO
    except ImportError:
        return None
    try:
        ensure_dir(model_path.parent)
        return YOLO(str(model_path))
    except Exception as exc:
        print(f"YOLO model unavailable, using face detection only: {exc}", file=sys.stderr)
        return None


def load_face_cascade():
    cv2, _ = lazy_imports()
    try:
        cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        if cascade.empty():
            return None
        return cascade
    except Exception:
        return None


def sample_frame(video_path: str, frame_number: int):
    cv2, _ = lazy_imports()
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, frame_number))
    ok, frame = cap.read()
    cap.release()
    if not ok:
        return None
    return frame


def detect_people(frame, yolo_model, face_cascade) -> list[dict[str, Any]]:
    cv2, _ = lazy_imports()
    detections: list[dict[str, Any]] = []

    if yolo_model is not None:
        try:
            results = yolo_model(frame, verbose=False, classes=[0])
            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = [int(value) for value in box.xyxy[0]]
                    person_box = [x1, y1, x2, y2]
                    face_box = None
                    if face_cascade is not None:
                        roi = frame[max(0, y1) : max(0, y2), max(0, x1) : max(0, x2)]
                        if roi.size:
                            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                            faces = face_cascade.detectMultiScale(
                                gray, scaleFactor=1.1, minNeighbors=5, minSize=(28, 28)
                            )
                            if len(faces) > 0:
                                fx, fy, fw, fh = faces[0]
                                face_box = [x1 + fx, y1 + fy, x1 + fx + fw, y1 + fy + fh]
                    detections.append({"person_box": person_box, "face_box": face_box})
        except Exception as exc:
            print(f"YOLO detection failed on a scene sample: {exc}", file=sys.stderr)

    if detections or face_cascade is None:
        return detections

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(28, 28))
    for x, y, w, h in faces:
        detections.append({"person_box": [x, y, x + w, y + h], "face_box": [x, y, x + w, y + h]})
    return detections


def enclosing_box(boxes: list[list[int]]) -> list[int] | None:
    if not boxes:
        return None
    return [
        min(box[0] for box in boxes),
        min(box[1] for box in boxes),
        max(box[2] for box in boxes),
        max(box[3] for box in boxes),
    ]


def choose_strategy(
    detections: list[dict[str, Any]],
    frame_width: int,
    frame_height: int,
    aspect_ratio: float,
) -> tuple[str, list[int] | None]:
    crop_width = int(frame_height * aspect_ratio)
    if not detections:
        return "WIDE", None

    if len(detections) == 1:
        target = detections[0].get("face_box") or detections[0].get("person_box")
        return "TRACK", target

    boxes = [item["person_box"] for item in detections if item.get("person_box")]
    group = enclosing_box(boxes)
    if not group:
        return "WIDE", None

    group_width = group[2] - group[0]
    if group_width <= crop_width:
        return "TRACK", group
    return "WIDE", None


def build_scene_plan(
    video_path: str,
    scenes: list[tuple[int, int, float, float]],
    frame_width: int,
    frame_height: int,
    aspect_ratio: float,
    sample_count: int,
    yolo_model_path: Path,
) -> list[ScenePlan]:
    yolo_model = load_yolo(yolo_model_path)
    face_cascade = load_face_cascade()
    plans: list[ScenePlan] = []

    for index, (start_frame, end_frame, start_sec, end_sec) in enumerate(scenes, start=1):
        frame_span = max(1, end_frame - start_frame)
        sample_frames = {
            start_frame + int(frame_span * fraction)
            for fraction in ([0.5] if sample_count <= 1 else [0.25, 0.5, 0.75])
        }
        detections: list[dict[str, Any]] = []
        for frame_number in sorted(sample_frames):
            frame = sample_frame(video_path, frame_number)
            if frame is None:
                continue
            detections.extend(detect_people(frame, yolo_model, face_cascade))

        strategy, target_box = choose_strategy(detections, frame_width, frame_height, aspect_ratio)
        plans.append(
            ScenePlan(
                index=index,
                start_frame=start_frame,
                end_frame=end_frame,
                start_sec=start_sec,
                end_sec=end_sec,
                strategy=strategy,
                target_box=target_box,
                people_count=len(detections),
            )
        )
    return plans


def crop_box_for_target(target_box: list[int], frame_width: int, frame_height: int, aspect_ratio: float) -> list[int]:
    crop_height = frame_height
    crop_width = min(frame_width, int(crop_height * aspect_ratio))
    center_x = (target_box[0] + target_box[2]) / 2
    x1 = int(center_x - crop_width / 2)
    x1 = max(0, min(x1, frame_width - crop_width))
    return [x1, 0, x1 + crop_width, crop_height]


def make_wide_frame(frame, output_width: int, output_height: int, wide_mode: str):
    cv2, np = lazy_imports()
    frame_height, frame_width = frame.shape[:2]

    if wide_mode == "letterbox":
        scale = min(output_width / frame_width, output_height / frame_height)
        scaled_width = max(2, int(frame_width * scale))
        scaled_height = max(2, int(frame_height * scale))
        resized = cv2.resize(frame, (scaled_width, scaled_height))
        output = np.zeros((output_height, output_width, 3), dtype=np.uint8)
        x_offset = (output_width - scaled_width) // 2
        y_offset = (output_height - scaled_height) // 2
        output[y_offset : y_offset + scaled_height, x_offset : x_offset + scaled_width] = resized
        return output

    scale = max(output_width / frame_width, output_height / frame_height)
    bg_width = max(output_width, int(frame_width * scale))
    bg_height = max(output_height, int(frame_height * scale))
    background = cv2.resize(frame, (bg_width, bg_height))
    x = (bg_width - output_width) // 2
    y = (bg_height - output_height) // 2
    background = background[y : y + output_height, x : x + output_width]
    background = cv2.GaussianBlur(background, (51, 51), 0)

    fg_scale = min(output_width / frame_width, output_height / frame_height)
    fg_width = max(2, int(frame_width * fg_scale))
    fg_height = max(2, int(frame_height * fg_scale))
    foreground = cv2.resize(frame, (fg_width, fg_height))
    x_offset = (output_width - fg_width) // 2
    y_offset = (output_height - fg_height) // 2
    background[y_offset : y_offset + fg_height, x_offset : x_offset + fg_width] = foreground
    return background


def process_video(
    input_path: str,
    output_path: str,
    plans: list[ScenePlan],
    output_width: int,
    output_height: int,
    aspect_ratio: float,
    fps: float,
    crf: int,
    preset: str,
    wide_mode: str,
) -> None:
    cv2, _ = lazy_imports()
    require_command("ffmpeg")
    ensure_dir(Path(output_path).parent)

    command = [
        "ffmpeg",
        "-y",
        "-f",
        "rawvideo",
        "-vcodec",
        "rawvideo",
        "-pix_fmt",
        "bgr24",
        "-s",
        f"{output_width}x{output_height}",
        "-r",
        f"{fps:.6f}",
        "-i",
        "-",
        "-i",
        input_path,
        "-map",
        "0:v:0",
        "-map",
        "1:a?",
        "-c:v",
        "libx264",
        "-crf",
        str(crf),
        "-preset",
        preset,
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-shortest",
        "-movflags",
        "+faststart",
        output_path,
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    cap = cv2.VideoCapture(input_path)
    frame_number = 0
    scene_index = 0
    last_output = None

    try:
        while cap.isOpened():
            ok, frame = cap.read()
            if not ok:
                break

            while scene_index < len(plans) - 1 and frame_number >= plans[scene_index + 1].start_frame:
                scene_index += 1
            plan = plans[scene_index]

            try:
                if plan.strategy == "TRACK" and plan.target_box:
                    x1, y1, x2, y2 = crop_box_for_target(
                        plan.target_box, frame.shape[1], frame.shape[0], aspect_ratio
                    )
                    cropped = frame[y1:y2, x1:x2]
                    output = cv2.resize(cropped, (output_width, output_height))
                else:
                    output = make_wide_frame(frame, output_width, output_height, wide_mode)
                last_output = output
            except Exception:
                output = last_output
                if output is None:
                    output = make_wide_frame(frame, output_width, output_height, wide_mode)

            assert process.stdin is not None
            process.stdin.write(output.tobytes())
            frame_number += 1
    finally:
        cap.release()
        if process.stdin:
            process.stdin.close()

    stderr = process.stderr.read().decode("utf-8", errors="replace") if process.stderr else ""
    return_code = process.wait()
    if return_code != 0:
        raise SystemExit(f"ffmpeg failed while writing vertical video:\n{stderr}")


def plan_to_json(plans: list[ScenePlan]) -> list[dict[str, Any]]:
    return [
        {
            "index": plan.index,
            "start_frame": plan.start_frame,
            "end_frame": plan.end_frame,
            "start_sec": round(plan.start_sec, 3),
            "end_sec": round(plan.end_sec, 3),
            "strategy": plan.strategy,
            "target_box": plan.target_box,
            "people_count": plan.people_count,
        }
        for plan in plans
    ]


def parse_ratio(value: str) -> float:
    try:
        width, height = value.split(":", 1)
        return float(width) / float(height)
    except Exception as exc:
        raise SystemExit(f"Invalid ratio '{value}'. Use W:H, for example 9:16.") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert a video clip into vertical format with scene-aware reframing.")
    parser.add_argument("--input", required=True, help="Input clip path.")
    parser.add_argument("--output", required=True, help="Vertical output path.")
    parser.add_argument("--report", help="Report JSON path. Defaults to <output>.json.")
    parser.add_argument("--ratio", default="9:16", help="Output ratio as W:H. Default: 9:16.")
    parser.add_argument("--height", type=int, default=1920, help="Output height in pixels. Default: 1920.")
    parser.add_argument("--native-height", action="store_true", help="Use source height instead of --height.")
    parser.add_argument("--wide-mode", choices=["blur", "letterbox"], default="blur")
    parser.add_argument(
        "--yolo-model",
        default=str(DEFAULT_YOLO_MODEL_PATH),
        help="YOLO model weights path. Defaults to assets/models/yolov8n.pt.",
    )
    parser.add_argument("--scene-threshold", type=float, default=27.0)
    parser.add_argument("--scene-samples", type=int, default=3, choices=[1, 3])
    parser.add_argument("--crf", type=int, default=23)
    parser.add_argument("--preset", default="fast")
    args = parser.parse_args()

    input_path = str(Path(args.input).expanduser().resolve())
    output_path = str(Path(args.output).expanduser().resolve())
    yolo_model_path = Path(args.yolo_model).expanduser().resolve()
    aspect_ratio = parse_ratio(args.ratio)

    frame_width, frame_height, fps, frame_count = get_video_properties(input_path)
    output_height = frame_height if args.native_height else args.height
    if output_height % 2:
        output_height += 1
    output_width = int(output_height * aspect_ratio)
    if output_width % 2:
        output_width += 1

    scenes = detect_scenes(input_path, fps, frame_count, args.scene_threshold)
    plans = build_scene_plan(
        input_path,
        scenes,
        frame_width,
        frame_height,
        aspect_ratio,
        sample_count=args.scene_samples,
        yolo_model_path=yolo_model_path,
    )
    process_video(
        input_path=input_path,
        output_path=output_path,
        plans=plans,
        output_width=output_width,
        output_height=output_height,
        aspect_ratio=aspect_ratio,
        fps=fps,
        crf=args.crf,
        preset=args.preset,
        wide_mode=args.wide_mode,
    )

    report = {
        "input_path": input_path,
        "output_path": output_path,
        "ratio": args.ratio,
        "output_width": output_width,
        "output_height": output_height,
        "wide_mode": args.wide_mode,
        "yolo_model_path": str(yolo_model_path),
        "scene_plan": plan_to_json(plans),
        "output_media": media_info(output_path),
    }
    report_path = Path(args.report) if args.report else Path(output_path).with_suffix(".json")
    write_json(report_path, report)
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
