# Provider And Tool Selection

Provider selection follows the user's process. Do not hardcode one provider.

## Provider Adapter Pattern

Each provider subskill or helper must define:

- provider purpose
- required env vars
- input shape
- output artifact
- async polling behavior, if any
- download/persistence behavior
- cost/approval rule
- failure handling

## Example Providers

- video generation: Kling, Runway, Pika, Veo, Luma
- avatar/talking head: HeyGen, Synthesia, D-ID
- voice: user audio, ElevenLabs, OpenAI TTS, PlayHT, local TTS
- transcription: Whisper, HyperFrames transcribe, ElevenLabs Scribe, manual transcript
- images: imagegen, stock search, user files
- animation: HyperFrames, Remotion, HTML/CSS/GSAP
- assembly: FFmpeg

## Secrets

Provider keys never go into skill docs or config files. Use:

- `.env.example` with empty values
- `.env` locally, ignored by git
- config files for non-secret defaults only

If a provider is optional, its env vars are optional in setup checks.
