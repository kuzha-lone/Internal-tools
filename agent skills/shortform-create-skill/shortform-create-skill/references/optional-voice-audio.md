# Optional Voice And Audio

Voice is optional. Ask before wiring voice into the pipeline.

## Audio Modes

- `none`: silent or music-only video
- `user_recorded`: user provides voice/audio
- `tts`: provider creates narration
- `avatar_provider`: voice is part of avatar render
- `source_audio`: podcast/interview/source video audio is reused
- `music_only`: no spoken narration

## Timing Sources

The generated pipeline must define one timing source:

- manual durations
- script word-count estimate
- generated voice duration
- transcript word timestamps
- source media clip timestamps

## Audio QA

If audio exists, export QA should verify:

- audio stream exists
- duration is close to visual duration
- audio codec is valid for MP4
- no unwanted audio is dropped
