# Settings Reference

These settings are the default `sina-liquid-glass` preset for Apple's liquid glass effect in React. Use them first, then tune by user request.

## Default Variant Settings

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

## Engine Knobs

- `displacementScale`: Refraction strength. Higher values feel more liquid but can create a magnifying-glass effect on large components.
- `blurAmount`: Frosting/blur level. Higher values make the background less readable.
- `saturation`: Color intensity of the refracted backdrop.
- `aberrationIntensity`: Prism/color-splitting strength. Use lightly on dashboards.
- `elasticity`: Mouse stretch/wobble. `0` is rigid and stable; higher values feel more playful.
- `mode`: Refraction mode. Prefer `"standard"` for stable dashboard components. `"prominent"` is more dramatic. `"shader"` may be less stable.
- `cornerRadius`: Shape radius in pixels.
- `padding`: Prefer `"0px"` in the wrapper and control spacing with `contentClassName`.

The upstream package documents these props here:

- https://github.com/rdev/liquid-glass-react
- https://www.npmjs.com/package/liquid-glass-react

## Sina Material Knobs

### Internal Tint

In `toneClass`:

```txt
[&_.glass]:!bg-violet-50/[0.06]
```

Higher opacity means stronger colored glass fill. Lower opacity means clearer glass.

### Warp Tint

In `toneClass`:

```txt
[&_.glass__warp]:!bg-violet-50/[0.03]
```

This is the color inside the refraction/blur layer. Increase carefully because it can make the glass cloudy.

### Colored Outer Glow

In `toneClass`:

```txt
0_10px_36px_rgba(221,214,254,0.30)
```

Increase the alpha for stronger colored aura. Increase blur radius for softer glow.

### Soft Inset Glow

In `toneClass`:

```txt
inset_0_0_36px_rgba(221,214,254,0.11)
```

Use this for an internal luminous glass feel. Keep it soft; avoid hard inset lines.

### Gradient Rim

In `edgeGradient`:

```ts
violet: "linear-gradient(135deg, rgba(245,243,255,0.76) 0%, rgba(196,181,253,0.2) 28%, rgba(255,255,255,0.09) 52%, rgba(167,139,250,0.28) 100%)"
```

This paints only the component rim through a CSS mask. It is not a normal filled overlay.

### Edge Width

```ts
const edgeWidth = variant === "hero" ? 1.35 : 1.15;
```

Increase to make the rim more visible. Keep it subtle for dashboard cards.

## Recommended Tuning Ranges

For clean dashboard glass:

```txt
displacementScale: 20-60
blurAmount: 0.02-0.08
saturation: 105-125
aberrationIntensity: 0.3-1.2
elasticity: 0
```

For buttons or playful controls:

```txt
displacementScale: 50-80
blurAmount: 0.05-0.12
saturation: 120-140
aberrationIntensity: 1-2
elasticity: 0.15-0.35
```

For large hero surfaces, keep displacement controlled. Large surfaces magnify backdrop movement more than small buttons.

## Layout Knob

Use `contentClassName` to control internal layout:

```tsx
contentClassName="grid min-h-[160px] gap-4 p-5"
```

Do not use the LiquidGlass `padding` prop for layout in the Sina wrapper. The wrapper uses `padding="0px"` so component sizing is predictable.
