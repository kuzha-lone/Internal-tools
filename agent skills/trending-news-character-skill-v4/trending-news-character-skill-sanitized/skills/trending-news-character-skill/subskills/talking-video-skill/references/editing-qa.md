# Editing QA

Run this QA pass on every final video.

## Pass Conditions

- the file is 1080x1920
- the file is 9:16 vertical
- the top half contains the Hyperframes visual
- the bottom half contains the HeyGen avatar render
- the Hyperframes top half stays visually contained in the top section
- the HeyGen avatar stays visually contained in the bottom section
- the final master has timed JetBrains Mono 3-word highlighted captions in neon cyberpunk red above the HyperFrames ticker
- captions do not collide with the ticker, face, title band, or HyperFrames main content
- the final master preserves the talking-head audio

## Fail Conditions

Reject the edit if:

- the top visual bleeds into the bottom half
- the avatar bleeds into the top half
- the stacked halves are misaligned or stretched badly
- captions are missing, clipped, off-screen, too close to the ticker, or covering main HyperFrames content
- the final file is only a raw HeyGen render with no top-half composition
