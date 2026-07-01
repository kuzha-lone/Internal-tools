import * as React from "react"

import { cn } from "@/lib/utils"

const Input = React.forwardRef(({ className, type, ...props }, ref) => {
  return (
    <input
      type={type}
      className={cn(
        "flex h-11 w-full rounded-xl border border-white/30 bg-white/20 backdrop-blur-md px-4 py-2.5 text-sm text-gray-900 ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-gray-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/50 focus-visible:ring-offset-0 focus-visible:border-white/50 focus-visible:bg-white/30 disabled:cursor-not-allowed disabled:opacity-50 transition-all duration-200 shadow-[inset_0_2px_4px_rgba(0,0,0,0.05)]",
        className
      )}
      ref={ref}
      {...props}
    />
  )
})
Input.displayName = "Input"

export { Input }
