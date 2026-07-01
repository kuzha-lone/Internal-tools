# Optional Captions

Captions are optional. Do not wire captions into the required path unless the user chooses them.

## Caption Modes

- `none`
- `plain_subtitles`
- `burned_in`
- `karaoke_highlight`
- `lower_third_only`
- `platform_native`

## Caption Contract

If captions are selected, define:

- transcript source
- caption style
- font
- placement
- burn-in or sidecar behavior
- whether captions are required for final export

## Technical Default

For burned-in captions, prefer ASS subtitles rendered with FFmpeg's `subtitles` filter. Use `drawtext` only for short fixed overlays or titles.

Do not assume three-word captions, active-word highlighting, or any fixed style unless the user selects it.
