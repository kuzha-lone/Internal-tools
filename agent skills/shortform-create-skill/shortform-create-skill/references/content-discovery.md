# Content Discovery

Use this reference before scaffolding a pipeline.

The agent's job is to turn the user's desired content process into a repeatable production graph. Start by asking how the content begins and what final output they expect.

## Ask For The Formula

Collect:

- content type and niche
- target platform
- target viewer
- desired length
- aspect ratio
- examples or references, if available
- repeatable structure
- what the agent should automate
- what the user wants to approve manually

## Content Source Modes

Common starting modes:

- `manual_script`: user provides the final script
- `manual_topic`: user provides a topic, agent helps produce the script
- `agent_research`: agent researches and proposes topics/scripts
- `research_with_approval`: agent researches, user approves topic/script before production
- `source_media`: user provides long video/audio/screenshots/files
- `recurring_feed`: agent pulls from configured feeds such as Google News, X, Reddit, RSS, CSV, or folders

## Readiness Test

Do not scaffold until the agent can state:

- where ideas/scripts come from
- how a script or beat plan becomes approved
- what assets/media must exist before export
- whether voice/audio exists
- whether captions are required
- what FFmpeg must export

If the user is unsure, propose 2-3 possible formulas and ask them to choose one.
