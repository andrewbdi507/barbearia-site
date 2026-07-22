import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
// ============================================================
// Toast Component (Radix-based notification system)
// ============================================================
import * as React from "react";
import { CheckCircle, XCircle, AlertTriangle, Info, X } from "lucide-react";
import { cn } from "../utils/cn";
const ToastContext = React.createContext(null);
export function useToast() {
    const ctx = React.useContext(ToastContext);
    if (!ctx)
        throw new Error("useToast must be used within ToastProvider");
    return ctx;
}
const iconMap = {
    success: CheckCircle,
    error: XCircle,
    warning: AlertTriangle,
    info: Info,
};
const colorMap = {
    success: "border-l-success text-success",
    error: "border-l-error text-error",
    warning: "border-l-warning text-warning",
    info: "border-l-info text-info",
};
export function ToastProvider({ children }) {
    const [toasts, setToasts] = React.useState([]);
    const addToast = React.useCallback((toast) => {
        const id = crypto.randomUUID();
        setToasts((prev) => [...prev, { ...toast, id }]);
        const duration = toast.duration ?? 5000;
        setTimeout(() => {
            setToasts((prev) => prev.filter((t) => t.id !== id));
        }, duration);
    }, []);
    const removeToast = React.useCallback((id) => {
        setToasts((prev) => prev.filter((t) => t.id !== id));
    }, []);
    return (_jsxs(ToastContext.Provider, { value: { toasts, addToast, removeToast }, children: [children, _jsx("div", { "aria-live": "polite", "aria-label": "Notifications", className: "fixed bottom-4 right-4 z-50 flex flex-col gap-2 max-w-sm w-full pointer-events-none", children: toasts.map((toast) => {
                    const Icon = iconMap[toast.type];
                    return (_jsxs("div", { role: "status", className: cn("pointer-events-auto flex items-start gap-3 rounded-md border bg-surface p-4 shadow-lg", "animate-slide-up border-l-4", colorMap[toast.type]), children: [_jsx(Icon, { className: "h-5 w-5 shrink-0 mt-0.5", "aria-hidden": "true" }), _jsxs("div", { className: "flex-1 min-w-0", children: [_jsx("p", { className: "text-sm font-medium text-text-primary", children: toast.title }), toast.description && (_jsx("p", { className: "text-xs text-text-secondary mt-0.5", children: toast.description }))] }), _jsx("button", { onClick: () => removeToast(toast.id), className: "shrink-0 rounded p-0.5 text-text-secondary hover:text-text-primary transition-colors", "aria-label": "Fechar notifica\u00E7\u00E3o", children: _jsx(X, { className: "h-4 w-4" }) }), _jsx("div", { className: "absolute bottom-0 left-0 h-1 bg-current opacity-20 rounded-b-md animate-[shrink_5s_linear]" })] }, toast.id));
                }) })] }));
}
//# sourceMappingURL=Toast.js.map