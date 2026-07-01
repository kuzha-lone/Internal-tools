# Dependency Checks

Generated pipelines should include a setup check.

## Required For Video Export

- `ffmpeg`
- `ffprobe`
- Python 3

## Optional Dependencies

Only check these when selected:

- HyperFrames CLI for HyperFrames animation
- Node/npm for HyperFrames or web animation tooling
- provider API keys for selected live providers
- transcription tools for captions
- browser tooling for web capture/screenshot pipelines

## Setup Check Behavior

The setup script should return JSON:

```json
{
  "status": "success",
  "errors": []
}
```

or:

```json
{
  "status": "blocked",
  "errors": ["missing ffmpeg"]
}
```

Optional provider keys should not fail setup unless that provider is selected as required.
