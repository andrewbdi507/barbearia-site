// ============================================================
// Badge, Avatar, Skeleton, EmptyState Components
// ============================================================

import * as React from "react";
import { cn } from "../utils/cn";
import { AvatarRoot, AvatarImage, AvatarFallback } from "./primitives";
import type { VariantProps } from "class-variance-authority";
import { cva } from "class-variance-authority";

// ---- Badge ----
const badgeVariants = cva(
  "inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-medium transition-colors",
  {
    variants: {
      variant: {
        success: "bg-success/10 text-success",
        warning: "bg-warning/10 text-warning",
        error: "bg-error/10 text-error",
        info: "bg-info/10 text-info",
        primary: "bg-primary/10 text-primary",
        secondary: "bg-secondary/10 text-secondary",
        outline: "border border-border text-text-secondary",
      },
    },
    defaultVariants: { variant: "primary" },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {
  dot?: boolean;
}

export function Badge({ className, variant, dot = false, children, ...props }: BadgeProps) {
  return (
    <span className={cn(badgeVariants({ variant, className }))} {...props}>
      {dot && <span className="h-1.5 w-1.5 rounded-full bg-current" aria-hidden="true" />}
      {children}
    </span>
  );
}

// ---- Avatar ----
export interface AvatarProps {
  src?: string;
  alt?: string;
  fallback?: string;
  size?: "sm" | "md" | "lg" | "xl";
  className?: string;
}

const avatarSizes = { sm: "h-8 w-8 text-xs", md: "h-10 w-10 text-sm", lg: "h-12 w-12 text-base", xl: "h-16 w-16 text-lg" };

export function Avatar({ src, alt = "", fallback, size = "md", className }: AvatarProps) {
  const initials = fallback
    ?.split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);

  return (
    <AvatarRoot className={cn("relative flex shrink-0 overflow-hidden rounded-full", avatarSizes[size], className)}>
      <AvatarImage src={src} alt={alt} className="h-full w-full object-cover" />
      <AvatarFallback
        className="flex h-full w-full items-center justify-center rounded-full bg-primary-light text-primary font-medium"
        delayMs={600}
      >
        {initials || "?"}
      </AvatarFallback>
    </AvatarRoot>
  );
}

// ---- Skeleton ----
export interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "text" | "circular" | "rectangular";
  width?: string | number;
  height?: string | number;
}

export function Skeleton({ className, variant = "text", width, height, ...props }: SkeletonProps) {
  return (
    <div
      aria-hidden="true"
      className={cn(
        "animate-shimmer bg-gradient-to-r from-surface-hover via-surface to-surface-hover bg-[length:200%_100%]",
        variant === "text" && "h-4 rounded-sm",
        variant === "circular" && "rounded-full",
        variant === "rectangular" && "rounded-md",
        className
      )}
      style={{ width, height }}
      {...props}
    />
  );
}

// ---- Empty State ----
export interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description?: string;
  action?: React.ReactNode;
  className?: string;
}

export function EmptyState({ icon, title, description, action, className }: EmptyStateProps) {
  return (
    <div className={cn("flex flex-col items-center justify-center py-16 text-center", className)} role="status">
      {icon && <div className="mb-4 text-text-disabled">{icon}</div>}
      <h3 className="text-lg font-semibold text-text-primary">{title}</h3>
      {description && <p className="mt-2 text-sm text-text-secondary max-w-sm">{description}</p>}
      {action && <div className="mt-6">{action}</div>}
    </div>
  );
}

// ---- Spinner ----
export function Spinner({ className, size = "md" }: { className?: string; size?: "sm" | "md" | "lg" }) {
  const sizeMap = { sm: "h-4 w-4", md: "h-6 w-6", lg: "h-8 w-8" };
  return (
    <div
      className={cn("animate-spin rounded-full border-2 border-primary border-t-transparent", sizeMap[size], className)}
      role="status"
      aria-label="Carregando"
    />
  );
}
