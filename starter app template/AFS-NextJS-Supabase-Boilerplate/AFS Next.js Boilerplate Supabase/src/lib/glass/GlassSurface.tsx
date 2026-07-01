import { cn } from '@/lib/utils'
import { forwardRef, HTMLAttributes } from 'react'
import { glassVariants, type GlassVariant } from './glassTokens'

export interface GlassSurfaceProps extends HTMLAttributes<HTMLDivElement> {
  variant?: GlassVariant
  intensity?: 'light' | 'medium' | 'heavy'
  border?: boolean
  shadow?: boolean
}

/**
 * GlassSurface - Centralized glassmorphism component
 *
 * Usage:
 * <GlassSurface variant="card" intensity="medium">
 *   Your content here
 * </GlassSurface>
 */
export const GlassSurface = forwardRef<HTMLDivElement, GlassSurfaceProps>(
  ({
    variant = 'default',
    intensity = 'medium',
    border = true,
    shadow = true,
    className,
    children,
    ...props
  }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          glassVariants[variant][intensity],
          border && 'border border-white/10',
          shadow && 'shadow-lg shadow-black/5',
          className
        )}
        {...props}
      >
        {children}
      </div>
    )
  }
)

GlassSurface.displayName = 'GlassSurface'
