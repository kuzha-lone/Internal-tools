# Editing Handoff

The pipeline stops at clean vertical base clips. Later editing should use `project_manifest.json`.

Each manifest clip includes:

- source timestamps
- horizontal cut path
- vertical base path
- title candidate
- hook text candidate
- reason for selection
- caption handoff instruction

Recommended next editing steps:

1. Generate captions from `transcript.json`.
2. Add hook text using `hook_text`.
3. Add punch-in zooms, B-roll, music, or branded overlays.
4. Export final platform-ready videos.

Keep base vertical clips unchanged and write edited outputs to a separate `final/` folder.

