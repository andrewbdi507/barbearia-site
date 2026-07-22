import * as React from "react";
export interface Toast {
    id: string;
    type: "success" | "error" | "warning" | "info";
    title: string;
    description?: string;
    duration?: number;
}
interface ToastContextValue {
    toasts: Toast[];
    addToast: (toast: Omit<Toast, "id">) => void;
    removeToast: (id: string) => void;
}
export declare function useToast(): ToastContextValue;
export declare function ToastProvider({ children }: {
    children: React.ReactNode;
}): React.JSX.Element;
export {};
//# sourceMappingURL=Toast.d.ts.map