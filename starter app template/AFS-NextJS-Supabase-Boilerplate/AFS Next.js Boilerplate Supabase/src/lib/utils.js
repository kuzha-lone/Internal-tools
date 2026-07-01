// Utility functions for styling and component management
// This file contains helper functions used by Shadcn UI components

import { clsx } from "clsx"
import { twMerge } from "tailwind-merge"
 
export function cn(...inputs) {
  return twMerge(clsx(inputs))
} 