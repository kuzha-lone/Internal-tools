# Script System Design

Script creation is optional. Some pipelines start from user media, existing footage, or visual-only concepts. If a script exists, define exactly how it is created.

## Script Modes

- `manual_script`: user provides final copy
- `agent_script`: agent writes from user topic
- `research_to_script`: agent researches, then writes
- `outline_then_script`: agent creates outline before final script
- `scene_cards`: agent produces beat/scene cards instead of prose
- `source_clip_notes`: agent extracts moments from source audio/video

## Required Contract

The generated pipeline must define:

- script input source
- output format: text, markdown, JSON scene cards, CSV, or transcript markers
- length target
- tone/style rules
- forbidden content rules
- approval gate
- validation rule

## Script Validation

Use deterministic validation when consistency matters:

- word/character length
- number of beats/scenes
- required hook/CTA/close
- claims/source requirements
- banned terms or style rules

Use a script helper only when validation is repeatable. Keep creative examples in references.
