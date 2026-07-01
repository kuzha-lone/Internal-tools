# Agent Runbook

This file is written for the user's AI agent.

## Your Job

Use this folder to run the configured character short-form content workflow.

The goal is to:
1. find one top narrative for the current run
2. write a short script in the configured voice
3. render a HeyGen talking-head clip first from the approved script
4. break the same approved script into 3 or 4 mini prompts for HyperFrames
5. generate HyperFrames visuals for those mini prompts
6. assemble the final vertical video with FFmpeg and add the lower-third title
7. burn timed JetBrains Mono captions onto the assembled master
8. speed up the fully assembled and captioned final video to 1.5x
9. return the final master and production artifacts

## Research Rules

Start with relevant sources for top narratives.

Then search X with the configured rules:
- keywords: use the configured topic keyword set
- last 6 to 8 hours only
- original posts only
- no retweets
- no replies
- do not read comments
- max 100 posts per run
- stay under the configured X budget cap
- use likes as the fallback ranking signal

Choose one top narrative per run.
Do not choose three at once.
Freshness matters more.

## Consequence Rule

After choosing the narrative:
- check whether it has a real audience impact or useful practical consequence
- if yes, include that in the content
- if no, skip it

## Video Rules

The final master must be:
- 1080x1920
- 9:16 vertical
- 15 to 30 seconds
- top half = HyperFrames visuals
- bottom half = HeyGen avatar clip

### HeyGen
- use the configured avatar
- use the configured HeyGen voice ID
- reuse the same configured HeyGen voice ID across all 3 daily avatar looks unless the user explicitly changes that rule
- create the talking-head video first for the bottom half
- do not speed up the talking-head clip by itself
- use the configured daily avatar rotation
- run slot 1 = look 1, run slot 2 = look 2, run slot 3 = look 3

### HyperFrames
- actually use the HyperFrames skill and real HyperFrames composition flow
- break the approved script into 3 or 4 mini prompts
- each mini prompt must match the part of the script being spoken during that time window
- the top half should look like premium informational motion design: explainer slides, maps, stat cards, dashboards, infographics, and polished visual hierarchy
- every HyperFrames top half must include a contextual moving ticker/news tape as part of the package: it should use story-specific short labels, move continuously during scenes, reinforce the editorial genre, remain secondary to the main safe-zone content, and be glued to the bottom edge of the HyperFrames top-half viewport directly above the avatar split
- designed on-screen text is allowed when it is part of the explainer design: headlines, labels, annotations, source lines, stat figures
- subtitle-style overlays are not allowed
- do not render prompt text, debug text, scene labels, or transcript text into the top half
- do not use placeholder graphics, rough sketches, fake charts, simple SVG stand-ins, or homemade hero assets under any circumstances
- no manual placeholder lines or generic rings pretending to be real information design
- output HyperFrames in 1:1 so it can fit cleanly at the top of the final video
- the primary HyperFrames layout truth is the final visible top-half viewport of 1080x960 in the assembled 1080x1920 master; do not treat the full 1080x1080 source square as the composition truth
- inside that 1080x960 top-half viewport, the mandatory primary animation safe zone for HyperFrames assets and infographics is 960x890 at x=60..1020 and y=35..925
- when authoring a 1080x1080 square HyperFrames source, the CSS safe-zone equivalent is `left:60px; top:95px; width:960px; height:890px`
- all major HyperFrames assets and infographics must fit inside that centered 960x890 primary animation safe zone. 
- also treat the final visible top-half crop in the assembled 1080x1920 master as a hard seam boundary; no primary HyperFrames element may sit so low that it risks touching the split with the avatar
- do not force every HyperFrames scene into a permanent split with a small bottom box and a separate top box
- the safe zone is one unified 960x890 primary animation area inside the 1080x960 top-half viewport
- use the full safe zone when needed; only use separate upper/lower regions when that genuinely helps the scene
- primary scene content must be center-weighted and dense inside the safe zone; fill the middle with a real board, chart, map, photo, screenshot, stat cluster, or comparison layout
- do not leave a hollow middle, pin the whole beat to the top, or use giant empty panels that do not carry information
- if you use a lower message region, make it large enough for all text/cards/components to fit with no clipping, no running off, and no cut-off words or elements
- work inside the centered 960x890 primary animation safe zone first; the ticker sits at y=925..960 and captions are added after assembly without changing the HyperFrames safe zone
- do not design HyperFrames scenes from the top first; if the key message, key stat, or key visual is pushed too high because the upper visual stole too much room, the scene is wrong
- preserve a seam-safe buffer, but do not waste the upper region on weak filler graphics or leave the lower region too small to hold the important content
- no overlap, no clipping, no running off frame, and no cut-off components are allowed anywhere in the safe zone
- avoid generic modular show-package boards that feel like reusable scaffolds: do not default to a pill label + oversized headline + inset explainer card + separator-strip stack unless the scene genuinely demands it
- each scene should read like one unified bespoke composition built for that beat, not multiple prebuilt segment types stacked together
- preserve a seam-safe buffer, but do not waste the upper region on weak filler graphics, oversized padding, or disconnected modules while starving the lower region of meaningful content
- do not crop, cut off, mask, stylize, or add decorative effects over the screenshot/photo hook unless the user explicitly asks for that treatment
- if a layout does not fit cleanly, simplify the scene; never force it into a rigid split
- the bottom-half talking avatar must be fitted to the 1080x960 bottom half by proportional zoom-to-fit crop only; never stretch or compress it
- only background texture, glows, and non-essential decorative elements may live outside the safe zone
- ticker/tape edges may extend outside the primary animation safe zone, but the tape must stay attached to the bottom of the HyperFrames layer and ticker text must not collide with major content, captions, source cards, or the final top/bottom seam
- do not render until each mini prompt has required assets, layout direction, motion direction, a named layout blueprint, and verification checks
- do not improvise around the workflow, skip layout steps, replace the established spacing system with a manual shortcut, or cut corners at any point even if it seems faster
- do not proceed to the next stage until the current stage's required artifact exists and has been checked against the workflow rules
- every new run must invent a fresh creative direction inside the same clean layout system; do not reuse the exact prior style, arrangement, scene order, animation structure, asset pack, or old scaffold from any previous video with only text swaps
- you are not allowed to use old scaffolds from old videos
- every run must create brand-new HyperFrames scenes, assets, and motion treatment for that script; reusing the same scene architecture from the previous video is a workflow violation
- variation should come from palette, typography, grid split, panel structure, annotation treatment, map/chart treatment, motion language, beat structure, and asset selection
- prefer native HTML/CSS/SVG information-design graphics over reliance on external assets
- generate new clips from a branded template system only; do not reuse or patch old rendered output templates from prior runs
- primary scene layout must come from reusable brand-frame components and blueprint primitives, not freeform absolute-positioned major content blocks
- if a scene is too dense for the safe zone, automatically simplify the scene and render anyway; do not abort the run
- once a run starts, you are not allowed to abort it because you want to review, rethink, improve, or reclassify the plan
- once a run starts, freeze the plan, finish the render, and deliver the output first
- no mid-run replanning, no mid-run skill edits, and no mid-run restarts unless there is a hard technical failure that makes the render literally impossible to complete

### Assembly
- use the user's installed `ffmpeg`/`ffprobe` from PATH to assemble the final master; the optional `config/video.json` paths, `FFMPEG_PATH`, `FFPROBE_PATH`, `--ffmpeg`, and `--ffprobe` may override this for unusual installs
- after the top/bottom video is assembled, add a short viral edgy title as a lower-third over the HeyGen talking-head section, under the speaker's face
- title style must use `Helvetica75 Bold/Helvetica75 Bold.ttf`, white text, a solid black rectangular background, and no rounded corners
- title text must wrap or resize so it never runs off screen; keep clear horizontal padding and readable line spacing inside the black band, and never export a title that is clipped, cut off, or too close to the frame edges
- after the lower-third title is burned into the assembled master, burn timed captions using `heygen_video.py caption-final`
- captions must use `JetBrainsMono-Bold.ttf` / `JetBrains Mono`, stable 3-word cue groups, active-word neon cyberpunk red highlighting (`#ff003c`), and default animation `none` so the text does not pop, scale, or bounce
- caption transcription provider should be `auto`: use ElevenLabs if configured, otherwise use HyperFrames/Whisper
- captions must sit in the top-half empty space just above the HyperFrames ticker; they must not collide with the speaker's face, the title band, the HyperFrames main content, or the ticker
- after the captioned master exists, speed up the final video to 1.5x with the same FFmpeg binary
- do not speed up only one part; speed up the finished assembled and captioned video

## Output Contract

Return:
- selected topic
- short reason it won
- final script
- raw HeyGen render path
- HyperFrames planning package path
- HyperFrames asset/output path
- final assembled master path
- any blocked reason or provider error

## API Cost Rule

- do not run multiple live provider tests in one run
- maximum one live provider test per run
- do not use paid API keys unless the user explicitly approved that run
- if approval is missing, stop before the live provider call

## Daily Avatar Rotation Rule

- the system has 3 avatar look ids configured
- each daily run must use a different look
- run 1 uses look 1
- run 2 uses look 2
- run 3 uses look 3
- pass the run slot into the video render step so the correct look is selected
