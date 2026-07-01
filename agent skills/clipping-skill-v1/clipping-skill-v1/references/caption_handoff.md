# Caption Handoff

This skill does not need a caption AI API key. It creates `transcript.json` with word timestamps and can burn captions directly into each vertical clip with `scripts/caption_clips.py`.

Recommended caption workflow:

1. Read `project_manifest.json`.
2. For each clip, use `cut_start` and `cut_end` to select words from `transcript.json`.
3. Shift word timestamps so the clip starts at `0.0`.
4. Group words into stable 3-word chunks.
5. Emit one ASS event per active word, keeping the same 3-word phrase in place while only the active word color changes.
6. Burn the ASS file into the vertical MP4 with FFmpeg's `subtitles` filter.

Default outputs:

```text
workdir/captioned/clip_001_captioned.mp4
workdir/captioned/clip_001_captions.ass
workdir/captioned/clip_001_caption_manifest.json
workdir/captioned/caption_outputs.json
```

Default style:

- centered lower third
- SDDystopianDemo
- active word color `#00d9ff`
- inactive words `#ffffff`
- no pop/bounce animation

Change style with:

```bash
python3 scripts/caption_clips.py \
  --manifest work/project_manifest.json \
  --active-word-color "#00d9ff" \
  --font-file /path/to/font.ttf \
  --font-name "Font Family Name"
```

Do not call an external caption service unless the user explicitly asks for one.
