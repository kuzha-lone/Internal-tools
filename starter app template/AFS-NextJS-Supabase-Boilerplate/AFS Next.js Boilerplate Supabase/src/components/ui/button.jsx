import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva } from "class-variance-authority"

import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-xl text-sm font-semibold ring-offset-background transition-all duration-200 ease-out focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 active:scale-[0.98]",
  {
    variants: {
      variant: {
        default: "bg-black/80 backdrop-blur-sm text-white hover:bg-black/90 shadow-lg hover:-translate-y-0.5 border border-black/20",
        destructive:
          "bg-red-500/80 backdrop-blur-sm text-white hover:bg-red-600/90 shadow-lg border border-red-400/20",
        outline:
          "border border-white/30 bg-white/15 backdrop-blur-md hover:bg-white/25 text-gray-700 shadow-[0_4px_16px_rgba(0,0,0,0.1)]",
        secondary:
          "bg-white/20 backdrop-blur-md text-gray-900 hover:bg-white/30 border border-white/25",
        ghost: "hover:bg-white/20 backdrop-blur-sm text-gray-600 hover:text-gray-900",
        link: "text-gray-900 underline-offset-4 hover:underline",
        glass: "bg-white/15 backdrop-blur-md border border-white/30 text-gray-700 hover:bg-white/25 shadow-[0_4px_16px_rgba(0,0,0,0.1),inset_0_1px_0_rgba(255,255,255,0.3)] hover:shadow-[0_8px_24px_rgba(0,0,0,0.15)]",
        "glass-dark": "bg-black/20 backdrop-blur-md border border-white/15 text-white hover:bg-black/30 shadow-[0_4px_16px_rgba(0,0,0,0.2)]",
      },
      size: {
        default: "h-10 px-5 py-2.5",
        sm: "h-9 rounded-lg px-4 text-sm",
        lg: "h-12 rounded-xl px-8 text-base",
        xl: "h-14 rounded-xl px-10 text-lg",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

const Button = React.forwardRef(({ className, variant, size, asChild = false, ...props }, ref) => {
  const Comp = asChild ? Slot : "button"
  return (
    <Comp
      className={cn(buttonVariants({ variant, size, className }))}
      ref={ref}
      {...props}
    />
  )
})
Button.displayName = "Button"

export { Button, buttonVariants }
