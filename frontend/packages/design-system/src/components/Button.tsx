// ============================================================
// Button Component
// Variants: primary, secondary, ghost, danger, success, outline
// Sizes: sm, md, lg, xl, icon
// States: default, hover, active, focus, loading, disabled
// ============================================================

import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { Slot } from "@radix-ui/react-slot";
import { Loader2 } from "lucide-react";
import { cn } from "../utils/cn";

const buttonVariants = cva(
  [
    "inline-flex items-center justify-center gap-2",
    "font-medium whitespace-nowrap",
    "rounded-md transition-all duration-200",
    "ring-offset-background",
    "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2",
    "disabled:pointer-events-none disabled:opacity-50",
    "select-none",
  ],
  {
    variants: {
      variant: {
        primary:
          "bg-primary text-white hover:bg-primary-hover active:scale-[0.98] shadow-sm",
        secondary:
          "border border-primary text-primary hover:bg-primary/5 active:scale-[0.98]",
        ghost: "text-text-secondary hover:bg-surface-hover hover:text-text-primary",
        danger:
          "bg-error text-white hover:bg-error/90 active:scale-[0.98] shadow-sm",
        success:
          "bg-success text-white hover:bg-success/90 active:scale-[0.98] shadow-sm",
        outline:
          "border border-border text-text-primary hover:bg-surface-hover active:scale-[0.98]",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        sm: "h-8 px-3 text-xs rounded-sm",
        md: "h-10 px-4 text-sm",
        lg: "h-12 px-6 text-base rounded-lg",
        xl: "h-14 px-8 text-lg rounded-lg",
        icon: "h-10 w-10 p-0",
      },
      fullWidth: {
        true: "w-full",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  /** Render as a child component (e.g., Next.js Link) */
  asChild?: boolean;
  /** Show loading spinner and disable */
  loading?: boolean;
  /** Icon to display before the text */
  leftIcon?: React.ReactNode;
  /** Icon to display after the text */
  rightIcon?: React.ReactNode;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant,
      size,
      fullWidth,
      asChild = false,
      loading = false,
      leftIcon,
      rightIcon,
      children,
      disabled,
      ...props
    },
    ref
  ) => {
    const Comp = asChild ? Slot : "button";
    const isDisabled = disabled || loading;

    return (
      <Comp
        className={cn(buttonVariants({ variant, size, fullWidth, className }))}
        ref={ref}
        disabled={isDisabled}
        {...props}
      >
        {loading ? (
          <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
        ) : leftIcon ? (
          <span className="shrink-0" aria-hidden="true">{leftIcon}</span>
        ) : null}
        {children && <span>{children}</span>}
        {!loading && rightIcon && (
          <span className="shrink-0" aria-hidden="true">{rightIcon}</span>
        )}
      </Comp>
    );
  }
);

Button.displayName = "Button";
