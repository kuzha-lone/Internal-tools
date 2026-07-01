import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'
import { glassTokens, glassVariants, type GlassVariant, type GlassIntensity } from './glassTokens'

/**
 * Utility function for merging Tailwind classes
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Generate glass effect classes
 *
 * @param variant - The glass variant to use
 * @param intensity - The intensity of the glass effect
 * @param options - Additional styling options
 * @returns Combined class string for glass effect
 *
 * @example
 * const classes = glass('card', 'medium', { border: true, shadow: true })
 * // Returns: 'backdrop-blur-lg bg-white/10 rounded-xl border border-white/10 shadow-lg shadow-black/5'
 */
export function glass(
  variant: GlassVariant = 'default',
  intensity: GlassIntensity = 'medium',
  options: {
    border?: boolean | 'subtle' | 'default' | 'prominent'
    shadow?: boolean | 'soft' | 'default' | 'prominent'
    className?: string
  } = {}
): string {
  const baseClass = glassVariants[variant][intensity]

  const borderClass = options.border
    ? typeof options.border === 'string'
      ? glassTokens.border[options.border]
      : glassTokens.border.default
    : ''

  const shadowClass = options.shadow
    ? typeof options.shadow === 'string'
      ? glassTokens.shadow[options.shadow]
      : glassTokens.shadow.default
    : ''

  return cn(baseClass, borderClass, shadowClass, options.className)
}

/**
 * Generate custom glass effect with specific blur and opacity
 *
 * @param blur - Blur size: 'sm' | 'md' | 'lg' | 'xl'
 * @param opacity - Opacity level: 'light' | 'medium' | 'heavy'
 * @param options - Additional styling options
 * @returns Combined class string
 *
 * @example
 * const classes = customGlass('lg', 'medium', { border: true })
 * // Returns: 'backdrop-blur-lg bg-white/10 border border-white/10'
 */
export function customGlass(
  blur: keyof typeof glassTokens.blur,
  opacity: keyof typeof glassTokens.opacity,
  options: {
    border?: boolean | 'subtle' | 'default' | 'prominent'
    shadow?: boolean | 'soft' | 'default' | 'prominent'
    rounded?: string
    className?: string
  } = {}
): string {
  const baseClass = `${glassTokens.blur[blur]} ${glassTokens.opacity[opacity]}`

  const borderClass = options.border
    ? typeof options.border === 'string'
      ? glassTokens.border[options.border]
      : glassTokens.border.default
    : ''

  const shadowClass = options.shadow
    ? typeof options.shadow === 'string'
      ? glassTokens.shadow[options.shadow]
      : glassTokens.shadow.default
    : ''

  const roundedClass = options.rounded || ''

  return cn(baseClass, borderClass, shadowClass, roundedClass, options.className)
}
