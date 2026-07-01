# Media Construction Options

Ask how the video is visually built. Do not assume a format.

## Common Methods

- `hyperframes_animation`: HTML/CSS/GSAP motion graphics or explainers
- `slideshow`: images plus timing and transitions
- `generated_clips`: video clips from Kling/Runway/Pika/Veo/etc.
- `screen_recording`: product/tutorial capture
- `source_footage`: user-provided clips
- `podcast_clip`: long-form audio/video repurposed into short clips
- `avatar_video`: talking-head/avatar provider
- `montage`: multiple clips, memes, images, overlays, and sound
- `mixed`: more than one method

## Media Stage Contract

For each media stage, define:

- input artifact
- output artifact
- file format
- duration behavior
- timing source
- required provider or local dependency
- fallback behavior

## Asset Strategy

The user must choose how assets are acquired:

- user-provided files
- generated images
- generated video
- web-fetched photos/screenshots
- stock assets
- screen recording
- no external assets

If assets are web-fetched, the generated pipeline should preserve source URLs when relevant.
