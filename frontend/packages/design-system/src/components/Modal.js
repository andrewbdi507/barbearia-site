import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { X } from "lucide-react";
import { cn } from "../utils/cn";
import { DialogRoot, DialogPortal, DialogOverlay, DialogContent, DialogTitle, DialogDescription, } from "./primitives";
export function Modal({ open, onOpenChange, title, description, size = "md", children, footer, className, }) {
    const sizeClasses = {
        sm: "max-w-sm",
        md: "max-w-md",
        lg: "max-w-lg",
        xl: "max-w-xl",
        full: "max-w-[90vw] max-h-[90vh]",
    };
    return (_jsx(DialogRoot, { open: open, onOpenChange: onOpenChange, children: _jsxs(DialogPortal, { children: [_jsx(DialogOverlay, { className: "fixed inset-0 z-30 bg-black/50 data-[state=open]:animate-fade-in" }), _jsxs(DialogContent, { className: cn("fixed left-1/2 top-1/2 z-40 -translate-x-1/2 -translate-y-1/2", "w-[calc(100%-2rem)] rounded-lg bg-surface shadow-xl", "data-[state=open]:animate-scale-in", "max-h-[85vh] flex flex-col", sizeClasses[size], className), children: [(title || onOpenChange) && (_jsxs("div", { className: "flex items-start justify-between p-6 pb-2", children: [_jsxs("div", { children: [title && _jsx(DialogTitle, { className: "text-lg font-semibold", children: title }), description && (_jsx(DialogDescription, { className: "text-sm text-text-secondary mt-1", children: description }))] }), _jsx("button", { onClick: () => onOpenChange(false), className: "rounded-md p-1.5 text-text-secondary hover:bg-surface-hover hover:text-text-primary transition-colors", "aria-label": "Fechar", children: _jsx(X, { className: "h-5 w-5" }) })] })), _jsx("div", { className: "overflow-y-auto px-6 py-2 flex-1", children: children }), footer && (_jsx("div", { className: "flex items-center justify-end gap-3 p-6 pt-4 border-t border-border", children: footer }))] })] }) }));
}
//# sourceMappingURL=Modal.js.map