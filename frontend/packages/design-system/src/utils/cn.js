// ============================================================
// Utility: className merger using clsx + tailwind-merge
// Prevents Tailwind class conflicts when composing components.
// ============================================================
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";
export function cn(...inputs) {
    return twMerge(clsx(inputs));
}
//# sourceMappingURL=cn.js.map