# Pipeline Step Design

A content pipeline is a repeatable production graph, not one giant prompt.

Each stage must define:

- purpose
- inputs
- outputs
- tool or provider
- user approval requirement
- success condition
- failure condition

## Common Stages

Use only the stages needed by the user's formula:

- content input or research
- script, outline, beat cards, or scene cards
- asset gathering or generation
- media construction
- animation
- voice/audio
- captions
- MP4 export
- QA
- publishing handoff

## Stage Order

The central generated `SKILL.md` must freeze stage order. Optional stages are present only if selected.

Example:

```text
manual script -> generated video prompts -> provider clip render -> MP4 export -> QA
```

Different example:

```text
topic research -> approved outline -> image search/generation -> TTS -> slideshow assembly -> optional captions -> MP4 export -> QA
```

## Approval Gates

Use approval gates for expensive, irreversible, or creative-choice-heavy stages:

- live API calls
- final script approval
- provider render submission
- publishing

Do not require approval for every small local file operation unless the user asks for strict manual control.
