---
name: sina-liquid-glass
description: Apply Apple's liquid glass effect in React using the Sina Liquid Glass visual system built on rdev/liquid-glass-react. Use when a user asks any agent to install or apply Apple's liquid glass effect in React, liquid glass, glass refraction, translucent frosted cards, colored glass tint, displacement, blur, chromatic aberration, glow, gradient rims, or the Richr/Sina glass style to an existing component or to create a new glass component.
---

# Sina Liquid Glass

Use this skill to apply **sina-liquid-glass**, a reusable preset for **Apple's liquid glass effect in React** built on top of [`liquid-glass-react`](https://github.com/rdev/liquid-glass-react).

`liquid-glass-react` is the rendering engine for Apple's liquid glass effect in React. `sina-liquid-glass` is the styled preset system: transparent tint, controlled blur, refraction, colored outer glow, soft inset glow, gradient rim, and layout-preserving component composition.

## Source Links

- GitHub engine repo: https://github.com/rdev/liquid-glass-react
- npm package: https://www.npmjs.com/package/liquid-glass-react
- Engine demo: https://liquid-glass.maxrovensky.com

The agent should install the npm package and use the engine README/API, but should apply the **Sina defaults** from this skill unless the user asks to tune them.

## Skill Files

Before implementing, read:

- [implementation-guide.md](references/implementation-guide.md) for setup and workflows.
- [settings-reference.md](references/settings-reference.md) when tuning blur, displacement, tint, glow, or borders.
- [troubleshooting.md](references/troubleshooting.md) if the glass looks black, blurry, stretched, misaligned, clipped, or too much like a magnifier.

Use [SinaLiquidGlassSurface.tsx](assets/SinaLiquidGlassSurface.tsx) as the default wrapper template.

## Agent Pipeline

Follow this pipeline exactly.

1. Identify the project type:
   - React SPA
   - Next.js App Router
   - Next.js Pages Router
   - Other React framework

2. Install the engine:

   ```bash
   npm install liquid-glass-react
   ```

   Use the project package manager if it is clearly different:

   ```bash
   pnpm add liquid-glass-react
   yarn add liquid-glass-react
   bun add liquid-glass-react
   ```

3. Add the wrapper:
   - Copy or adapt [SinaLiquidGlassSurface.tsx](assets/SinaLiquidGlassSurface.tsx).
   - Put it somewhere like `src/components/glass/SinaLiquidGlassSurface.tsx`.
   - For Next.js, keep `"use client"` and use dynamic import with `ssr: false`.

4. Select the implementation mode:
   - Convert Existing Component
   - Create New Component

5. Apply the default Sina settings first.
   - Do not invent new defaults.
   - Tune only if the user requests a different look.

6. Rebuild the component structure if necessary.
   - If the original component breaks after wrapping, rebuild the internal layout inside the glass surface.
   - Preserve intent, spacing, content hierarchy, dimensions, icons, and actions.

7. Remove conflicting old styles:
   - Remove old opaque backgrounds.
   - Remove duplicate borders.
   - Remove stale shadows.
   - Remove extra `backdrop-blur` layers unless intentionally used.

8. Verify visually in context when possible.
   - The component should still be aligned.
   - Text should be readable.
   - The glass should have one clean surface.
   - The edge should be visible through the gradient rim and glow, not hard white lines.

## Default Preset

Use these as the default values unless the user requests changes:

```ts
hero: {
  displacementScale: 58,
  blurAmount: 0.05,
  saturation: 116,
  aberrationIntensity: 1.05,
  elasticity: 0,
  mode: "standard",
}

metric: {
  displacementScale: 40,
  blurAmount: 0.05,
  saturation: 112,
  aberrationIntensity: 0.82,
  elasticity: 0,
  mode: "standard",
}

panel: {
  displacementScale: 34,
  blurAmount: 0.05,
  saturation: 110,
  aberrationIntensity: 0.68,
  elasticity: 0,
  mode: "standard",
}
```

The default material includes:

- Medium internal transparent tint.
- Softer warp tint.
- Colored outer drop shadow.
- Soft inset glow.
- Masked gradient rim border.
- `overflow-visible` so glow is not clipped.
- `elasticity: 0` so components do not stretch or wobble unless requested.

## How The Effect Is Applied

The visual stack is:

```txt
page background or surrounding UI
↓
liquid-glass-react refraction/filter layer
↓
sina-liquid-glass transparent tint + warp tint
↓
sina-liquid-glass colored outer glow + soft inset glow
↓
sina-liquid-glass masked gradient rim
↓
component content
```

The agent should not put a duplicated background image inside every component. Prefer one real background or rich UI layer behind the glass surfaces.

## Two Modes

### Convert Existing Component

Use this when the user wants to apply glass to an existing card, button, nav, tile, modal, chart panel, dashboard section, or toolbar.

Do not just wrap JSX and assume the component still works. Preserve or rebuild the component layout carefully.

Workflow:

1. Inspect the original component dimensions, padding, radius, gap, alignment, typography, icon placement, actions, and responsive behavior.
2. Identify existing backgrounds, borders, shadows, and backdrop classes that will conflict with the glass material.
3. Replace the visual surface with `SinaLiquidGlassSurface`.
4. Move the component content into the glass content layer.
5. Preserve the original size and alignment unless the user requests a redesign.
6. Rebuild the inside if the wrapper changes spacing or alignment.
7. Remove old opaque backgrounds, duplicate borders, stale shadows, and leftover wrappers.
8. Confirm the component has one clean glass surface and the content is composed intentionally.

### Create New Component

Use this when the user wants a new glass card, metric tile, panel, nav item, button, toolbar, modal, dashboard section, or other UI surface.

Build a complete component, not an empty glass rectangle.

Workflow:

1. Understand the component purpose and expected content.
2. Choose `variant`: `hero`, `metric`, or `panel`.
3. Choose `tone`: `violet`, `cyan`, `green`, `amber`, `red`, or `white`.
4. Define dimensions, padding, radius, and responsive behavior.
5. Compose label/title, primary content, supporting copy, icons, actions, badges, and footer/status rows.
6. Apply `SinaLiquidGlassSurface`.
7. Keep typography, spacing, and alignment deliberate.

New components must be complete UI pieces. Do not create an empty decorative glass rectangle.

## Layout Rules

- Preserve component sizing when converting an existing component.
- Do not create oversized wrappers that stretch or misalign content.
- Do not leave the old component background underneath the glass.
- Do not add opaque black backgrounds.
- Do not add hard white borders unless the user explicitly requests them.
- Do not put cards inside cards.
- Do not let icons, text, badges, or buttons float randomly.
- Do not apply the effect to the whole app at once unless the user explicitly asks; start with one component when the design is being tuned.
- Use visual assets or real page backgrounds behind glass; glass needs something to refract.

## User-Tunable Controls

Always tell the user these settings can be changed:

- `displacementScale`: liquid/refraction strength.
- `blurAmount`: frosted blur.
- `saturation`: color intensity.
- `aberrationIntensity`: prism/color splitting.
- `elasticity`: hover stretch/wobble.
- `mode`: refraction style.
- `cornerRadius`: shape radius.
- `edgeWidth`: gradient rim thickness.
- `toneClass`: internal tint, warp tint, outer glow, inset glow.
- `edgeGradient`: rim color and shine.
- `contentClassName`: spacing and layout inside the glass.

## Browser Notes

The package README notes Safari and Firefox only partially support the displacement effect. Chrome and Edge usually show the strongest result. Provide a readable translucent fallback for unsupported browsers.
