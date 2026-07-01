# Implementation Guide

This guide is for any coding agent using the `sina-liquid-glass` skill to apply Apple's liquid glass effect in React. It is not tied to one repo. The agent should inspect the user's project, install the upstream engine, add the wrapper, and apply or create a component using the Sina defaults.

## Install

Install the engine:

```bash
npm install liquid-glass-react
```

For React 19/Next.js projects, use the client-only wrapper in `assets/SinaLiquidGlassSurface.tsx`.

## Engine vs Preset

`liquid-glass-react` provides the SVG/filter refraction engine for Apple's liquid glass effect in React.

`sina-liquid-glass` adds the design system:

- Preset variants: `hero`, `metric`, `panel`.
- Preset tones: `violet`, `cyan`, `green`, `amber`, `red`, `white`.
- Transparent internal tint.
- Warp tint.
- Colored outer glow.
- Soft inset glow.
- Masked gradient rim.
- Layout-preserving wrapper.

## Next.js Setup

Use a client component and dynamic import:

```tsx
"use client";

import dynamic from "next/dynamic";

const LiquidGlass = dynamic(() => import("liquid-glass-react"), {
  ssr: false,
  loading: () => null,
});
```

Then copy or adapt `assets/SinaLiquidGlassSurface.tsx`.

## Exact Agent Workflow

1. Inspect the user’s project structure and package manager.
2. Install `liquid-glass-react` from npm.
3. Add `SinaLiquidGlassSurface.tsx` to the project.
4. Import it in the target component.
5. Choose `variant` and `tone`.
6. Move content into `contentClassName`.
7. Remove conflicting surface styles from the old component.
8. Rebuild spacing and alignment if the wrapper changes the composition.
9. Explain which settings the user can tune.

Do not hardcode repo-specific paths. Adapt to the user’s project.

## Basic Usage

```tsx
import SinaLiquidGlassSurface from "@/components/glass/SinaLiquidGlassSurface";

export function RevenueTile() {
  return (
    <SinaLiquidGlassSurface
      variant="metric"
      tone="green"
      radius={10}
      contentClassName="grid min-h-[150px] gap-3 p-5"
    >
      <div className="flex items-center justify-between gap-3">
        <p className="font-mono text-xs uppercase text-emerald-100/80">Revenue</p>
        <span className="text-emerald-100">↗</span>
      </div>

      <div className="text-4xl font-black text-white">$18.4k</div>

      <div className="flex items-center justify-between text-sm text-white/75">
        <span>Month to date</span>
        <span className="font-mono text-emerald-100">+12.6%</span>
      </div>
    </SinaLiquidGlassSurface>
  );
}
```

## Convert Existing Component

Before editing, inspect the original component:

- Height, width, min-height, max-width.
- Padding.
- Radius.
- Flex/grid layout.
- Text sizes.
- Icon placement.
- Badge/action placement.
- Responsive classes.
- Existing background, border, shadow, and backdrop classes.

The conversion is not finished until the component still looks properly assembled.

When converting:

```tsx
// Before
<div className="rounded-[10px] border border-white/10 bg-slate-950/60 p-5 shadow-xl">
  <CardContent />
</div>

// After
<SinaLiquidGlassSurface
  variant="panel"
  tone="violet"
  radius={10}
  contentClassName="p-5"
>
  <CardContent />
</SinaLiquidGlassSurface>
```

Remove the old `bg-*`, `border-*`, `shadow-*`, and `backdrop-blur-*` classes from the replaced surface unless they are deliberately still needed.

If the component becomes misaligned, rebuild the component content inside the glass surface. Keep the same visual intent, but correct spacing, rows, columns, alignment, and responsive behavior.

## Create New Component

When creating a new component, design the internal composition first:

- Header row: label/title plus icon/action.
- Primary content: value, chart, form fields, table, or body copy.
- Secondary content: detail text, trend, status, helper copy.
- Footer row if needed.

Then wrap the finished composition in `SinaLiquidGlassSurface`.

Use stable dimensions:

```tsx
contentClassName="grid min-h-[160px] gap-4 p-5"
```

Avoid relying on the glass effect to make an empty component look good.

## Background Requirement

Liquid glass needs something behind it to refract. Use a real page background, image, gradient, video, canvas, or rich interface layer behind the component.

Do not put the same background image inside every glass component unless the user explicitly requests that. Prefer one page-level background behind all glass surfaces.

## Package API Source

Use the upstream package docs for engine props:

- https://github.com/rdev/liquid-glass-react
- https://www.npmjs.com/package/liquid-glass-react

The Sina defaults override the package defaults.
