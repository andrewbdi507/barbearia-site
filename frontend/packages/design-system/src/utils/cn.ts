// ============================================================
// Utility: className merger using clsx + tailwind-merge
// Prevents Tailwind class conflicts when composing components.
// ============================================================

import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}
