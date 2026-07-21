// ============================================================
// Card Component
// ============================================================

import * as React from "react";
import { cn } from "../utils/cn";

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Visual variant */
  variant?: "default" | "interactive" | "selected" | "stat";
  /** Remove padding */
  noPadding?: boolean;
}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant = "default", noPadding = false, children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          "rounded-lg border border-border bg-surface shadow-sm",
          "transition-all duration-200",
          !noPadding && "p-4",
          variant === "interactive" && "cursor-pointer hover:shadow-md hover:-translate-y-0.5",
          variant === "selected" && "border-primary ring-2 ring-primary/20",
          variant === "stat" && "text-center",
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
  }
);

Card.displayName = "Card";

// Card sub-components
export const CardHeader = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("mb-3", className)} {...props} />
);
CardHeader.displayName = "CardHeader";

export const CardTitle = ({ className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) => (
  <h3 className={cn("text-lg font-semibold text-text-primary", className)} {...props} />
);
CardTitle.displayName = "CardTitle";

export const CardDescription = ({ className, ...props }: React.HTMLAttributes<HTMLParagraphElement>) => (
  <p className={cn("text-sm text-text-secondary", className)} {...props} />
);
CardDescription.displayName = "CardDescription";

export const CardContent = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("", className)} {...props} />
);
CardContent.displayName = "CardContent";

export const CardFooter = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("mt-4 flex items-center gap-3", className)} {...props} />
);
CardFooter.displayName = "CardFooter";

export const CardStat = ({ label, value, trend }: { label: string; value: string; trend?: string }) => (
  <div>
    <p className="text-sm text-text-secondary">{label}</p>
    <p className="text-2xl font-bold text-text-primary">{value}</p>
    {trend && <p className="text-xs text-text-secondary mt-1">{trend}</p>}
  </div>
);
CardStat.displayName = "CardStat";
