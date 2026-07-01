---
name: trending-news-character-skill
description: Run a configurable trending-news character workflow from topic selection through verified short script and final assembled 9:16 video with HyperFrames on top and HeyGen on bottom.
---

# Trending News Character Skill

Use this skill when a creator wants a reusable workflow for a trending-news character.

## Inputs

Read:

- `{baseDir}/../../../SYSTEM.md`
- `{baseDir}/../../../AGENT_RUNBOOK.md`
- `{baseDir}/../../../config/project.json`
- `{baseDir}/../../../config/research.json`
- `{baseDir}/../../../config/video.json`
- `{baseDir}/../../../config/platforms.json`

Then choose the right subskill path:

- topic discovery from X:
  `{baseDir}/subskills/viral-research-skill/SKILL.md`
- script validation:
  `{baseDir}/subskills/viral-script-skill/SKILL.md`
- HyperFrames visual generation:
  `{baseDir}/subskills/hyperframes-video-skill/SKILL.md`
- video production:
  `{baseDir}/subskills/talking-video-skill/SKILL.md`

## Contract

The workflow must:

1. respect the configured research mode
2. verify claims before scripting
3. preserve the approved script during render
4. create the talking-head clip first from the approved script and wait until the provider returns a completed raw video file
5. extract the completed avatar render's exact duration and word-timed transcript before planning HyperFrames
6. generate the HyperFrames top-half clip from the same approved script using the completed avatar duration/transcript as the timing source
6. after both parts are generated and assembled, burn timed JetBrains Mono captions into the assembled master before the speed pass
7. speed up the fully assembled and captioned final video to 1.5x
8. break the approved script into 3 or 4 mini prompts for the HyperFrames top half only after the avatar render exists
9. make each mini prompt correspond directly to the part of the script being spoken in that real avatar time window
10. use HyperFrames for clean editorial top-half scenes with strong text hierarchy, maps, data cards, dashboards, infographics, and explainer layouts when useful
11. include a contextual moving news ticker or market tape in every HyperFrames top-half run; it must use story-specific labels, move continuously, stay secondary to the main beat, and be glued to the bottom edge of the HyperFrames top-half viewport directly above the avatar split
12. never use homemade placeholder assets, sketch graphics, fake charts, or abstract filler as top-half hero visuals
13. after assembling the top HyperFrames layer and bottom talking-head layer, add a short viral edgy title as a lower-third overlay over the bottom talking-head section, under the speaker's face, using `Helvetica75 Bold/Helvetica75 Bold.ttf`, white text, a black rectangular background, and no rounded corners; title text must wrap or resize so it never runs off screen and must keep clear padding from the black band edges
14. after the lower-third title is in place, burn timed captions onto the assembled master using `JetBrainsMono-Bold.ttf`, centered just above the HyperFrames ticker; captions must use stable 3-word cue groups with the active spoken word highlighted in neon cyberpunk red (`#ff003c`), no default popping/scaling animation, and must not collide with the title, avatar face, HyperFrames main content, or ticker
15. return a final assembled 1080x1920 master
16. never truncate a persistent title
17. never run more than one live provider test in a single run
18. never use paid API keys unless the user explicitly approved that run
19. if avatar rotation is enabled, rotate the 3 configured avatar looks across the 3 daily runs in order; if a single `HEYGEN_AVATAR_LOOK_ID` is configured, use that one and do not touch unrelated avatar/photo IDs
20. once a render run starts, do not abort, replan, or restart the run because you want to review or improve the plan; finish the run and deliver the output first
21. never bypass the established no-overlap layout workflow or substitute a manual shortcut for the spacing system
22. the primary HyperFrames layout truth is the final visible top-half viewport of 1080x960 in the assembled 1080x1920 master, not the full 1080x1080 square source
23. inside that top-half viewport, the mandatory primary animation safe zone for HyperFrames assets and infographics is the centered 960x890 frame at x=60..1020 and y=35..925
24. do not cut corners or skip steps at any stage of the workflow: research, scripting, talking-head render, HyperFrames planning, HyperFrames rendering, assembly, captions, speed pass, and final verification are all mandatory
25. do not move to the next stage until the current stage's required artifact exists and has been checked against the workflow rules
25a. never run HyperFrames planning, asset selection, layout, inspect, or render in parallel with HeyGen generation; the top-half animation must wait for the completed avatar render so its scenes can be timed to the actual spoken video
26. every new HyperFrames run must use new scene architecture, new motion treatment, and new asset selection for that script; reusing the previous run's animation/layout structure is forbidden
27. you are not allowed to use old scaffolds from old videos; all HyperFrames clips must be brand new and have new assets and animations for that run
28. HyperFrames top-half composition must work inside one unified centered 960x890 primary animation safe zone in the 1080x960 top-half viewport; do not force every scene into a rigid two-box split, and if separate upper/lower regions are used they must remain flexible, center-weighted, dense, and never clip, overlap, run off, or cut off any content
29. major scene content must use the center of the safe zone: build dense centered boards, dashboards, maps, charts, stat clusters, or photo/screenshot treatments that fill the beat; do not leave a hollow middle, do not pin the whole scene to the top edge, and do not create giant empty panels
30. screenshot/photo hook scenes must show the screenshot/photo plainly inside the full 960x890 primary animation safe zone with no decorative effects, masking, or cut-off treatment unless the user explicitly asks for it
31. the bottom-half talking avatar must be zoomed proportionally to fit the 1080x960 bottom half; never stretch or compress it
