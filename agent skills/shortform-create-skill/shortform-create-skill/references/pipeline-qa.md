# Pipeline QA

QA enforces repeatability.

## Pipeline Audit

Check:

- central skill exists
- runbook exists
- config files exist and are valid JSON
- required subskills exist
- optional subskills match selected options
- `.env.example` has placeholders only
- no real API keys or generated media are present
- final export is MP4
- FFmpeg export rules exist

## Run QA

For each production run, verify:

- every required stage produced its output
- paid API calls were approved
- final `.mp4` exists
- `ffprobe` confirms dimensions and duration
- audio exists if required
- captions exist only if selected
- output is in the configured publish folder

## Failure Rule

If a required artifact is missing, stop and report the missing stage. Do not skip ahead and pretend the pipeline completed.
