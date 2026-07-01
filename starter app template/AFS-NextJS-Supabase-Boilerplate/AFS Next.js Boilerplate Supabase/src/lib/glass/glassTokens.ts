/**
 * Glassmorphism Design Tokens
 *
 * Centralized system for glass effects across the application.
 * All blur, transparency, and glass styling should use these tokens.
 */

export const glassTokens = {
  // Backdrop blur values
  blur: {
    sm: 'backdrop-blur-sm',    // 4px blur
    md: 'backdrop-blur-md',    // 12px blur
    lg: 'backdrop-blur-lg',    // 16px blur
    xl: 'backdrop-blur-xl',    // 24px blur
  },

  // Background opacity values
  opacity: {
    light: 'bg-white/5',
    medium: 'bg-white/10',
    heavy: 'bg-white/20',
  },

  // Border styles for glass surfaces
  border: {
    subtle: 'border border-white/5',
    default: 'border border-white/10',
    prominent: 'border border-white/20',
  },

  // Shadow styles for depth
  shadow: {
    soft: 'shadow-sm shadow-black/5',
    default: 'shadow-lg shadow-black/5',
    prominent: 'shadow-xl shadow-black/10',
  },
} as const

// Pre-composed variants for common use cases
export const glassVariants = {
  default: {
    light: 'backdrop-blur-sm bg-white/5',
    medium: 'backdrop-blur-md bg-white/10',
    heavy: 'backdrop-blur-lg bg-white/20',
  },
  card: {
    light: 'backdrop-blur-md bg-white/5 rounded-xl',
    medium: 'backdrop-blur-lg bg-white/10 rounded-xl',
    heavy: 'backdrop-blur-xl bg-white/20 rounded-xl',
  },
  nav: {
    light: 'backdrop-blur-sm bg-white/5',
    medium: 'backdrop-blur-md bg-white/10',
    heavy: 'backdrop-blur-lg bg-white/15',
  },
  modal: {
    light: 'backdrop-blur-md bg-white/10 rounded-2xl',
    medium: 'backdrop-blur-lg bg-white/15 rounded-2xl',
    heavy: 'backdrop-blur-xl bg-white/25 rounded-2xl',
  },
  sidebar: {
    light: 'backdrop-blur-sm bg-white/5',
    medium: 'backdrop-blur-md bg-white/8',
    heavy: 'backdrop-blur-lg bg-white/12',
  },
} as const

export type GlassVariant = keyof typeof glassVariants
export type GlassIntensity = 'light' | 'medium' | 'heavy'
