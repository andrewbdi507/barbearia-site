import * as React from "react";
export interface ModalProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    title?: string;
    description?: string;
    size?: "sm" | "md" | "lg" | "xl" | "full";
    children: React.ReactNode;
    footer?: React.ReactNode;
    className?: string;
}
export declare function Modal({ open, onOpenChange, title, description, size, children, footer, className, }: ModalProps): React.JSX.Element;
//# sourceMappingURL=Modal.d.ts.map