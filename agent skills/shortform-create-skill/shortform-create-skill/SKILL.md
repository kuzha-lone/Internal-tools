---
name: shortform-create-skill
description: Guide an AI agent through designing and scaffolding a repeatable short-form video pipeline for any user-defined content formula, with optional research, scripting, media generation, voice, captions, animation, providers, and a required high-quality FFmpeg MP4 export.
---

# Shortform Create Skill

Use this skill when a user wants to create a reusable agent-followable short-form video pipeline.

This skill does not create one fixed content style. It teaches the agent how to listen to the user's process, ask for missing decisions, break the process into repeatable stages, select tools, scaffold a custom skill folder, and enforce the same production steps every run.

The only universal output requirement for video pipelines is a final `.mp4` export.

## First Rule

Do not assume the user wants:

- captions
- voiceover
- avatars
- HeyGen
- HyperFrames
- research
- split screen
- news content
- slideshow content
- any specific niche or format

Ask, discover, then scaffold.

## Discovery Sequence

Before scaffolding, collect enough information to state the pipeline from input through MP4 export.

Read these references as needed:

- `references/content-discovery.md` when asking the user what they want to create
- `references/pipeline-step-design.md` when converting their process into stages
- `references/script-system-design.md` when script creation is unclear
- `references/media-construction-options.md` when choosing how the video is visually built
- `references/provider-and-tool-selection.md` when choosing APIs/tools
- `references/optional-hyperframes-animation.md` when the user wants custom animations
- `references/optional-voice-audio.md` when the user wants voice, music, or real audio timing
- `references/optional-captions.md` only if the user wants captions
- `references/ffmpeg-mp4-export.md` for export rules
- `references/dependency-checks.md` for required local tools
- `references/pipeline-qa.md` for validation and repeatability checks

## Required Questions

Guide the user through these decisions:

1. **Content source**
   - manual script or idea
   - agent research
   - both research and user approval
   - recurring sources such as web search, Google News, X, Reddit, RSS, CSV, notes, uploaded files, or long-form media

2. **Script system**
   - full manual script
   - agent-written script
   - outline first
   - beat cards or scene cards
   - script approval required or not
   - validation rules for length, tone, structure, and claims

3. **Media construction**
   - HyperFrames animations
   - slideshow from generated or sourced images
   - generated video clips from Kling/Runway/Pika/Veo/etc.
   - screen recordings
   - product demo capture
   - user footage
   - meme/montage edits
   - podcast clipping
   - avatar/talking-head video
   - mixed layout

4. **Audio**
   - no voice
   - user-recorded voice
   - TTS
   - avatar-provider voice
   - extracted podcast/source audio
   - music only
   - timing source: manual timing, script estimate, real audio duration, transcript, or clip timestamps

5. **Captions**
   - no captions
   - plain subtitles
   - burned-in captions
   - karaoke/highlight captions
   - lower-third text only
   - platform-native captions only

6. **Export**
   - final dimensions
   - FPS
   - duration target
   - aspect ratio
   - audio handling
   - scaling/cropping rules
   - QA checks

## Pipeline Contract

After discovery, write a pipeline spec and scaffold a custom pipeline folder. Each stage must have:

- purpose
- inputs
- outputs
- tool/provider
- required user approval, if any
- success condition
- failure condition

The custom pipeline must include:

- central `SKILL.md`
- `AGENT_RUNBOOK.md`
- `SYSTEM.md`
- `START_HERE.md`
- `.env.example`
- `config/*.json`
- subskills matching the chosen process
- FFmpeg MP4 export script
- setup/audit scripts
- empty output folders with `.gitkeep`

Optional modules are only included when chosen. Do not wire captions, voice, animation, or provider APIs into the required path unless the user selected them.

## Scaffolding

Once the pipeline spec is complete, use:

```bash
python3 scripts/scaffold_shortform_pipeline.py --name <pipeline-name> --output <target-folder> --spec <pipeline-spec.json>
```

The spec must include:

- content source mode
- script creation mode
- media construction method
- voice/audio choice
- caption choice
- tools/providers
- MP4 export settings
- approval gates
- QA rules

## Auditing

After scaffolding, use:

```bash
python3 scripts/audit_shortform_pipeline.py --path <pipeline-folder>
```

Fix failures before giving the user the pipeline.

## Non-Negotiables

- Final video export is `.mp4`.
- FFmpeg/ffprobe are the default export/probe tools.
- API keys live only in `.env`.
- `.env.example` must contain placeholders only.
- No generated media belongs in a reusable template.
- No optional step runs unless selected in the user's process.
- The generated agent workflow must be repeatable: same inputs and same config should follow the same stage order every run.
