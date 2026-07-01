# Caption Spec

Use this file when burning captions into the final video.

## Rendering Method

Use FFmpeg's `subtitles` filter with ASS styling.

Do not rely on raw `drawtext` for long captions.

## Required Font

Use this font by default:

- `{baseDir}/../assets/fonts/JetBrainsMono-Bold.ttf`

Pass the font directory through `fontsdir` so libass can resolve it.

Use the ASS font family name `JetBrains Mono` unless a user explicitly overrides it.

## Transcription Provider

Use `--transcription-provider auto` by default.

- If `ELEVENLABS_API_KEY` is configured, the helper may use ElevenLabs Scribe.
- If ElevenLabs is not configured, the helper falls back to `npx hyperframes@0.6.4 transcribe --json` with the configured Whisper model.
- A user can bypass transcription by passing `--transcript-json`.

## Safe-Zone Rule

Captions must sit in the top-half empty space just above the HyperFrames ticker by default.

That means:

- centered horizontally
- padded from the left edge
- padded from the right edge
- high enough above the ticker to avoid collision
- low enough to feel attached to the ticker/news package
- never cut off
- never allowed to extend beyond the readable width of the frame

## Three-Word Highlight Mode

Default caption mode is `three-word-highlight`.

- show up to 3 words at once
- keep the 3-word phrase anchored in one fixed position
- render inactive words white
- render the currently spoken word in neon cyberpunk red (`#ff003c`)
- advance the active highlight from word to word using word timestamps
- do not move the whole caption block every word; the color shift should be the primary timing cue

## Layout Rule

Caption text must be wrapped into neat line groups before it can overflow the frame.

Use ASS subtitle rendering so the text can stay inside a constrained, centered caption block instead of one oversized line.

Persistent top titles must preserve the full text.

That means:

- never silently truncate a title because it crossed a soft word or character target
- wrap the title into additional lines when necessary
- if the wrapped title is still too large, reduce title styling before dropping words
- an overlong full title is acceptable; a cut-off title is not

## Styling Direction

The technical system should support these ASS style fields:

- `FontName`
- `FontSize`
- `Alignment`
- `MarginL`
- `MarginR`
- `MarginV`
- `Outline`
- `Shadow`
- `PrimaryColour`

The recommended default alignment for lower-third centered captions is bottom-center.

## Animation Direction

Default captions should use no pop, scale, bounce, or fade animation. The 3-word caption group stays visually stable while the active spoken word changes to neon cyberpunk red.

`pop-fade` and `fade` remain available as explicit overrides, but do not use them unless the user asks for animated caption entrances. Do not move captions around the frame per word; keep the caption block anchored so it remains readable.

## FFmpeg Rule

Use:

- `fontsdir` for the custom font directory
- `force_style` for ASS style overrides
- `wrap_unicode=1` when supported by the FFmpeg/libass build

`wrap_unicode` improves line breaking behavior, but the subtitle asset still needs to be authored cleanly.

## QA Rule

Reject the edit if:

- any line runs off-screen
- any line touches the edge too closely
- the subtitle block sits too low or too high
- the captions feel visually uneven across the clip
