// ============================================================
// Modal / Dialog Component
// ============================================================

import * as React from "react";
import { X } from "lucide-react";
import { cn } from "../utils/cn";
import {
  DialogRoot,
  DialogPortal,
  DialogOverlay,
  DialogContent,
  DialogTitle,
  DialogDescription,
} from "./primitives";

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

export function Modal({
  open,
  onOpenChange,
  title,
  description,
  size = "md",
  children,
  footer,
  className,
}: ModalProps) {
  const sizeClasses = {
    sm: "max-w-sm",
    md: "max-w-md",
    lg: "max-w-lg",
    xl: "max-w-xl",
    full: "max-w-[90vw] max-h-[90vh]",
  };

  return (
    <DialogRoot open={open} onOpenChange={onOpenChange}>
      <DialogPortal>
        <DialogOverlay className="fixed inset-0 z-30 bg-black/50 data-[state=open]:animate-fade-in" />
        <DialogContent
          className={cn(
            "fixed left-1/2 top-1/2 z-40 -translate-x-1/2 -translate-y-1/2",
            "w-[calc(100%-2rem)] rounded-lg bg-surface shadow-xl",
            "data-[state=open]:animate-scale-in",
            "max-h-[85vh] flex flex-col",
            sizeClasses[size],
            className
          )}
        >
          {/* Header */}
          {(title || onOpenChange) && (
            <div className="flex items-start justify-between p-6 pb-2">
              <div>
                {title && <DialogTitle className="text-lg font-semibold">{title}</DialogTitle>}
                {description && (
                  <DialogDescription className="text-sm text-text-secondary mt-1">
                    {description}
                  </DialogDescription>
                )}
              </div>
              <button
                onClick={() => onOpenChange(false)}
                className="rounded-md p-1.5 text-text-secondary hover:bg-surface-hover hover:text-text-primary transition-colors"
                aria-label="Fechar"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
          )}

          {/* Body */}
          <div className="overflow-y-auto px-6 py-2 flex-1">{children}</div>

          {/* Footer */}
          {footer && (
            <div className="flex items-center justify-end gap-3 p-6 pt-4 border-t border-border">
              {footer}
            </div>
          )}
        </DialogContent>
      </DialogPortal>
    </DialogRoot>
  );
}
