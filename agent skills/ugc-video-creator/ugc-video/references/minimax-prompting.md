# MiniMax Hailuo 2.3 Video Prompting Guide

## Key Principles

1. **Describe the motion** — What should move and how? Be specific about actions.
2. **Keep it simple** — One clear motion per clip works better than complex sequences
3. **Camera movement** — Describe camera motion explicitly if desired
4. **Duration awareness** — 6-second clips are short, so focus on one key motion

## Camera Motion Commands

MiniMax supports these camera commands (include in brackets in your prompt):
- `[Pan left]` / `[Pan right]` — horizontal camera pan
- `[Tilt up]` / `[Tilt down]` — vertical camera tilt
- `[Dolly in]` / `[Dolly out]` — camera moves toward/away from subject
- `[Zoom in]` / `[Zoom out]` — lens zoom
- `[Truck left]` / `[Truck right]` — lateral camera movement
- `[Crane up]` / `[Crane down]` — vertical crane movement
- `[Static]` — no camera movement (good for subtle subject motion)

## UGC Avatar Motion Prompts

For the intro reaction clip:
- "The woman turns slightly toward camera with a shocked expression, subtle hair movement, natural blink [Static]"
- "She looks up from her phone with an amazed reaction, mouth slightly open, eyes widening [Dolly in]"
- "The girl laughs and covers her mouth in surprise, gentle head shake [Static]"

Keep avatar motions subtle and natural — exaggerated movements look unnatural in AI video.

## Product Demo Motion Prompts

For the product showcase clip:
- "Slow cinematic push in on the product, light shifts across the surface [Dolly in]"
- "Camera slowly orbits around the product, reflections shift [Pan right]"
- "The app interface appears on screen with smooth animations [Static]"

## CTA Motion Prompts

For the benefit/call-to-action clip:
- "The person looks at camera with a satisfied smile, gentle nod [Static]"
- "Slow zoom out revealing the full scene, warm lighting [Zoom out]"
- "Person uses the product naturally, showing the result [Static]"

## Tips

- Shorter prompts often work better than very long ones
- MiniMax has a built-in prompt optimizer (enabled by default) — it will enhance your prompt
- For portrait 9:16 video, vertical subject compositions work best
- Avoid describing text in the video — text is added separately via ffmpeg
