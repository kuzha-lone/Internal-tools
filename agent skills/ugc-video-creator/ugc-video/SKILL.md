---
name: ugc-video
description: >-
  Create 18-second UGC-style viral short-form videos (9:16 portrait) with
  AI-generated visuals. Produces a 3-clip video: intro avatar reaction,
  product demo, and call-to-action. Uses Flux 2 Pro for images and MiniMax
  Hailuo 2.3 for video animation. Trigger with requests like "make a UGC
  video", "create a product video", "generate a viral ad", or "short-form
  promo for [product]".
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "os": ["linux"],
        "requires":
          {
            "bins": ["python3", "ffmpeg"],
            "env": ["BFL_API_KEY", "MINIMAX_API_KEY"],
          },
        "primaryEnv": "BFL_API_KEY",
      },
  }
---

# UGC Video Creator (Mode 1)

Create 18-second vertical (1080x1920) UGC-style viral videos from a product description. The video has 3 clips of 6 seconds each.

## Pipeline Overview

```
User describes product
        ↓
[1] Generate clip 1 image (Flux 2 Pro text-to-image) — SHOCKED girl selfie
        ↓
[2] Generate clip 2 image (Flux 2 Pro image-to-image, using clip 1 as reference) — SAME girl, focused expression
        ↓
[3] Generate clip 3 image (Flux 2 Pro image-to-image, using clip 1 as reference) — SAME girl, satisfied expression
        ↓
[4] Animate each image to 6s video (MiniMax Hailuo 2.3) — 9:16 portrait
        ↓
[5] Add text overlays to each clip (ffmpeg)
        ↓
[6] Stitch 3 clips into one 18s video (ffmpeg)
        ↓
Final 1080x1920 portrait video returned to user
```

> **CHARACTER CONSISTENCY**: Clips 2 and 3 use `--image` to pass clip 1's image as a reference. This keeps the same girl (face, hair, features) across all 3 clips while generating completely new scenes and expressions via the prompt. Image generation for clips MUST be sequential — clip 1 first, then clip 2, then clip 3.

## Step-by-Step Workflow

### Step 1: Understand the Request

Parse what the user wants:
- **Product name** and what it does
- **Target audience** (who is the video for?)
- **Reference images** (optional — user may attach product screenshots)
- If the user doesn't specify details, make creative choices yourself.

> **IMPORTANT — Reference images**: If the user provides reference images (product photos, screenshots, etc.), these are ONLY for you to understand what the product looks like. You must NEVER pass reference images directly to `generate-video.py`. You ALWAYS generate brand new images with Flux 2 Pro for every clip.

### Step 2: Create Working Directory

```bash
mkdir -p /home/node/.openclaw/workspace/ugc-video-$(date +%s)/{images,videos,output}
```

Use this directory for ALL files in this pipeline.

### Step 3: Generate 3 Images (Flux 2 Pro) — SEQUENTIAL

Generate each image at **1080x1920** (portrait 9:16). Images MUST be generated sequentially because clips 2 and 3 depend on clip 1's output.

**Clip 1 — Intro Reaction Avatar (SELFIE STYLE, SHOCKED EXPRESSION):**

```bash
python3 {baseDir}/scripts/generate-image.py \
  --prompt "YOUR PROMPT HERE" \
  --width 1080 --height 1920 \
  --out WORKDIR/images/clip1-reaction.png
```

> **CRITICAL RULES FOR CLIP 1:**
> - This MUST be a **close-up selfie-style** photo — as if the girl is holding her phone camera and filming herself
> - **NO phones visible** in the image. The phone IS the camera. First-person POV selfie angle.
> - **Head and upper shoulders ONLY** — slight upward angle, typical of selfie videos
> - She must be **looking directly at the camera**
> - NEVER generate a full-body shot or a photo taken by someone else
> - Her expression MUST be **SHOCKED, BEWILDERED, MIND-BLOWN** — jaw dropped, eyes wide open, eyebrows raised high

Prompt template for Clip 1:
> "close-up selfie-style photo, first-person POV as if taken by the subject holding the camera, of a super realistic beautiful (22-25) year old (choose hair color) (choose race) girl looking directly at camera with a SHOCKED BEWILDERED expression, jaw dropped open, eyes wide with disbelief, eyebrows raised high, mind-blown reaction face; head and upper shoulders only, slight upward selfie angle, at (describe setting), hyper realistic, raw, crystal clear, NO phone visible in frame, NO hands holding phone"

Vary the girl's appearance each time — different races, hair colors, ages (22-25), settings. The SHOCKED expression is mandatory for every clip 1.

**Clip 2 — Product Demo (SAME GIRL via `--image` reference):**

Wait for clip 1 to finish, then use it as a reference image:

```bash
python3 {baseDir}/scripts/generate-image.py \
  --prompt "YOUR PROMPT HERE" \
  --image WORKDIR/images/clip1-reaction.png \
  --width 1080 --height 1920 \
  --out WORKDIR/images/clip2-product.png
```

> **CRITICAL RULES FOR CLIP 2:**
> - You MUST pass `--image WORKDIR/images/clip1-reaction.png` to maintain character consistency (same girl).
> - If the user provided a product reference image, use it ONLY to understand what the product looks like. NEVER use the user's reference image as `--image` input.
> - The generated image must show the **SAME GIRL from clip 1** but with a **DIFFERENT expression**: focused, intrigued, curious, leaning in, examining the product closely, eyes lit up with interest.
> - Place the product in a **lifestyle, aspirational, relatable environment** — NOT on a white/plain background.
> - The prompt MUST describe the girl's new expression AND the product scene. Be very specific about the facial expression and body language.

Prompt template for Clip 2:
> "super realistic photo of the same young woman, now with a focused intrigued expression, eyes lit up with curiosity, leaning slightly forward examining (describe product) closely, holding/interacting with (product) in (describe lifestyle setting — cozy room, modern desk, outdoor café, etc.), warm natural lighting, hyper realistic, crystal clear, portrait orientation"

**Clip 3 — Call-To-Action / Benefit (SAME GIRL via `--image` reference):**

Wait for clip 1 to finish (clip 3 also references clip 1, NOT clip 2):

```bash
python3 {baseDir}/scripts/generate-image.py \
  --prompt "YOUR PROMPT HERE" \
  --image WORKDIR/images/clip1-reaction.png \
  --width 1080 --height 1920 \
  --out WORKDIR/images/clip3-cta.png
```

> **CRITICAL RULES FOR CLIP 3:**
> - You MUST pass `--image WORKDIR/images/clip1-reaction.png` to maintain character consistency (same girl).
> - The generated image must show the **SAME GIRL from clip 1** but with a **DIFFERENT expression**: satisfied, confident, glowing smile, relaxed, content.
> - Prompt should show how the product benefits the user's life, with the girl looking happy and fulfilled.
> - Be very specific about the facial expression and body language — it must be distinctly different from clips 1 and 2.

Prompt template for Clip 3:
> "super realistic photo of the same young woman, now with a satisfied confident expression, glowing relaxed smile, looking directly at camera with a content pleased look, arms crossed or casual relaxed pose, in (describe aspirational setting that shows product benefit), warm golden lighting, hyper realistic, crystal clear, portrait orientation"

### Expression Guide Per Clip

| Clip | Role | Expression | Example descriptors |
|------|------|-----------|-------------------|
| 1 | Intro reaction | **SHOCKED / BEWILDERED** | jaw dropped, eyes wide, eyebrows raised, mind-blown, disbelief, stunned |
| 2 | Product demo | **FOCUSED / INTRIGUED** | curious eyes, leaning in, examining closely, eyes lit up, fascinated, engaged |
| 3 | CTA / benefit | **SATISFIED / CONFIDENT** | glowing smile, relaxed, content, pleased, confident smirk, arms crossed looking proud |

### Step 4: Animate Each Image to Video (MiniMax Hailuo 2.3)

Turn each still image into a 6-second video clip.

```bash
python3 {baseDir}/scripts/generate-video.py \
  --image WORKDIR/images/clip1-reaction.png \
  --prompt "The woman's jaw drops in shock, eyes widen with disbelief, she leans back slightly stunned, subtle hair movement, natural blink, shocked reaction" \
  --duration 6 \
  --out WORKDIR/videos/clip1-raw.mp4

python3 {baseDir}/scripts/generate-video.py \
  --image WORKDIR/images/clip2-product.png \
  --prompt "The woman leans in curiously examining the product, eyes focused and intrigued, gentle hand movement, subtle cinematic lighting shift" \
  --duration 6 \
  --out WORKDIR/videos/clip2-raw.mp4

python3 {baseDir}/scripts/generate-video.py \
  --image WORKDIR/images/clip3-cta.png \
  --prompt "The woman smiles confidently at camera, relaxed satisfied expression, gentle nod, warm golden lighting, subtle hair movement" \
  --duration 6 \
  --out WORKDIR/videos/clip3-raw.mp4
```

Write your own motion prompts — make them detailed and cinematic. The examples above are just starting points.

### Step 5: Add Text Overlays (ffmpeg)

**Clip 1 — Intro Hook (bottom third):**

```bash
python3 {baseDir}/scripts/add-text-overlay.py \
  --input WORKDIR/videos/clip1-raw.mp4 \
  --text "YOUR HOOK TEXT" \
  --position bottom \
  --out WORKDIR/videos/clip1-text.mp4
```

Write a gen-z style, edgy intro hook. Examples:
- "I just quit my OF because THIS makes me more money"
- "POV: your bf thinks you do OF becuz youre bringing home $15,363 a month from home LMAO"
- "I got russian ops chasing me because I found THIS..."
- "POV: your ugly broke ass been looking for a job for 7 months... and NOW YOU FIND THIS"
- "I thought this was another SCAM APP... I was wrong in 3 minutes PROPS"
- "If you're still doing this manually in 2026... ur an IDIOT... and we need to talk"
- "This app replaced 3 hours of my day... and my boss still thinks I'm grinding LOL"

**Clip 2 — Product Text (upper third):**

```bash
python3 {baseDir}/scripts/add-text-overlay.py \
  --input WORKDIR/videos/clip2-raw.mp4 \
  --text "YOUR PRODUCT TEXT" \
  --position top \
  --out WORKDIR/videos/clip2-text.mp4
```

Instantly and emphatically explain how the product helps the user.

**Clip 3 — CTA Text (bottom third):**

```bash
python3 {baseDir}/scripts/add-text-overlay.py \
  --input WORKDIR/videos/clip3-raw.mp4 \
  --text "YOUR CTA TEXT" \
  --position bottom \
  --out WORKDIR/videos/clip3-text.mp4
```

Examples:
- "yes your life will get 100x better...go check it out on my page"
- "you literally don't understand how much this will help you... go look on my page"

### Step 6: Stitch All Clips Together (ffmpeg)

```bash
{baseDir}/scripts/stitch-clips.sh \
  --clip1 WORKDIR/videos/clip1-text.mp4 \
  --clip2 WORKDIR/videos/clip2-text.mp4 \
  --clip3 WORKDIR/videos/clip3-text.mp4 \
  --out WORKDIR/output/final.mp4
```

### Step 7: Speed Up 1.2x (ffmpeg)

Speed up the final stitched video by 1.2x. This is applied AFTER text overlays are burned in so everything (visuals + text) speeds up together.

```bash
ffmpeg -i WORKDIR/output/final.mp4 -vf "setpts=PTS/1.2" -an WORKDIR/output/final-fast.mp4
```

> The `-an` flag drops audio since these clips have no meaningful audio track. The output `final-fast.mp4` is the deliverable.

### Step 8: Return the Video

Send the final video back to the user. The file at `WORKDIR/output/final-fast.mp4` is the completed portrait UGC video.

## Important Notes

- ALL images must be **1080x1920** (portrait 9:16)
- ALL videos are **6 seconds** each, portrait format
- Text overlays use **white text with black stroke outline**
- Be creative with prompts — vary the avatar, settings, and hooks every time
- If a script fails, check stderr for error details and retry with adjusted parameters
- For references on prompt engineering, see `references/flux-prompting.md` and `references/minimax-prompting.md`
