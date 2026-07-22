import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
// ============================================================
// Input Component
// With label, helper text, error message, and icon support.
// ============================================================
import * as React from "react";
import { cn } from "../utils/cn";
export const Input = React.forwardRef(({ className, label, helperText, error, leftIcon, rightIcon, containerClassName, id, required, disabled, ...props }, ref) => {
    const inputId = id || React.useId();
    const hasError = Boolean(error);
    return (_jsxs("div", { className: cn("flex flex-col gap-1.5", containerClassName), children: [label && (_jsxs("label", { htmlFor: inputId, className: cn("text-sm font-medium", hasError ? "text-error" : "text-text-primary", disabled && "text-text-disabled"), children: [label, required && _jsx("span", { className: "text-error ml-0.5", children: "*" })] })), _jsxs("div", { className: "relative", children: [leftIcon && (_jsx("span", { className: "absolute left-3 top-1/2 -translate-y-1/2 text-text-secondary", "aria-hidden": "true", children: leftIcon })), _jsx("input", { id: inputId, ref: ref, disabled: disabled, "aria-invalid": hasError, "aria-describedby": hasError ? `${inputId}-error` : helperText ? `${inputId}-helper` : undefined, className: cn("flex h-10 w-full rounded-md border bg-surface px-3 py-2 text-sm", "placeholder:text-text-disabled", "transition-colors duration-200", "focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary", "disabled:cursor-not-allowed disabled:opacity-50", leftIcon && "pl-10", rightIcon && "pr-10", hasError
                            ? "border-error focus:ring-error/20 focus:border-error"
                            : "border-border", className), ...props }), rightIcon && (_jsx("span", { className: "absolute right-3 top-1/2 -translate-y-1/2 text-text-secondary", "aria-hidden": "true", children: rightIcon }))] }), helperText && !hasError && (_jsx("p", { id: `${inputId}-helper`, className: "text-xs text-text-secondary", children: helperText })), hasError && (_jsx("p", { id: `${inputId}-error`, className: "text-xs text-error animate-fade-in", role: "alert", children: error }))] }));
});
Input.displayName = "Input";
//# sourceMappingURL=Input.js.map