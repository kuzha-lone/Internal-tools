# Troubleshooting

Use this file when the applied effect looks wrong or the component breaks after wrapping.

## Component Turns Black

Cause:

- `liquid-glass-react` renders black helper layers.
- Existing component backgrounds were left behind.

Fix:

- Hide package black siblings with selectors like `[&>div.bg-black]:!hidden`.
- Remove old `bg-black`, `bg-slate-*`, or opaque background classes from the converted surface.
- Use transparent tint values, not opaque fills.

## Component Has Ugly Lines

Cause:

- Hard borders, ring shadows, inset shadows, or duplicate overlay layers.

Fix:

- Avoid flat `border-white/*` as the main edge style.
- Use a masked gradient rim.
- Keep inset glow soft and blurred.
- Do not add multiple edge layers unless each one has a clear purpose.

## Component Has No Visible Edge

Cause:

- Tint and glow are working, but there is no rim or shadow separation.

Fix:

- Increase `edgeWidth`.
- Increase opacity in `edgeGradient`.
- Increase colored outer shadow alpha.
- Use `overflow-visible` so shadows are not clipped.

## Component Looks Too Blurry

Cause:

- `blurAmount` is too high.
- Extra CSS `backdrop-blur-*` was added.
- Warp tint/fill is too strong.

Fix:

- Lower `blurAmount`.
- Remove extra `backdrop-blur-*` classes unless intentionally used.
- Lower `glass__warp` tint opacity.

## Component Looks Like A Magnifying Glass

Cause:

- `displacementScale` is too high for the component size.
- `mode` is too dramatic.
- Large component sits over a detailed fixed background.

Fix:

- Lower `displacementScale`.
- Use `mode: "standard"`.
- Keep `elasticity: 0`.
- Reduce `aberrationIntensity`.

## Hover Stretch Feels Bad

Cause:

- `elasticity` is above `0`.

Fix:

- Use `elasticity: 0` for rigid dashboard surfaces.
- Only use elasticity for playful buttons or small controls when requested.

## Glow Is Clipped

Cause:

- Parent wrapper or grid cell has `overflow-hidden`.

Fix:

- Use `overflow-visible` on the glass wrapper when possible.
- Check parent containers for clipping.

## Content Is Misaligned

Cause:

- The wrapper changed size.
- Padding moved from the old component to the wrong layer.
- Old layout classes were lost.

Fix:

- Put padding, grid, flex, min-height, and alignment in `contentClassName`.
- Preserve original dimensions when converting existing components.
- Inspect icons, labels, values, actions, and footers after wrapping.

If the conversion is still messy, rebuild the component interior from scratch using the original component as a visual/content reference.

## Next.js Hydration Or Server Error

Cause:

- `liquid-glass-react` is imported in a server component.

Fix:

- Add `"use client"`.
- Use `next/dynamic` with `ssr: false`.

## Safari Or Firefox Looks Different

Cause:

- The package README notes Safari and Firefox only partially support displacement.

Fix:

- Keep fallback tint, rim, and glow readable.
- Do not rely only on displacement for the component’s visual identity.
