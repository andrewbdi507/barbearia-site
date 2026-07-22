import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
// ============================================================
// Card Component
// ============================================================
import * as React from "react";
import { cn } from "../utils/cn";
export const Card = React.forwardRef(({ className, variant = "default", noPadding = false, children, ...props }, ref) => {
    return (_jsx("div", { ref: ref, className: cn("rounded-lg border border-border bg-surface shadow-sm", "transition-all duration-200", !noPadding && "p-4", variant === "interactive" && "cursor-pointer hover:shadow-md hover:-translate-y-0.5", variant === "selected" && "border-primary ring-2 ring-primary/20", variant === "stat" && "text-center", className), ...props, children: children }));
});
Card.displayName = "Card";
// Card sub-components
export const CardHeader = ({ className, ...props }) => (_jsx("div", { className: cn("mb-3", className), ...props }));
CardHeader.displayName = "CardHeader";
export const CardTitle = ({ className, ...props }) => (_jsx("h3", { className: cn("text-lg font-semibold text-text-primary", className), ...props }));
CardTitle.displayName = "CardTitle";
export const CardDescription = ({ className, ...props }) => (_jsx("p", { className: cn("text-sm text-text-secondary", className), ...props }));
CardDescription.displayName = "CardDescription";
export const CardContent = ({ className, ...props }) => (_jsx("div", { className: cn("", className), ...props }));
CardContent.displayName = "CardContent";
export const CardFooter = ({ className, ...props }) => (_jsx("div", { className: cn("mt-4 flex items-center gap-3", className), ...props }));
CardFooter.displayName = "CardFooter";
export const CardStat = ({ label, value, trend }) => (_jsxs("div", { children: [_jsx("p", { className: "text-sm text-text-secondary", children: label }), _jsx("p", { className: "text-2xl font-bold text-text-primary", children: value }), trend && _jsx("p", { className: "text-xs text-text-secondary mt-1", children: trend })] }));
CardStat.displayName = "CardStat";
//# sourceMappingURL=Card.js.map