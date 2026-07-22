import * as React from "react";
import type { VariantProps } from "class-variance-authority";
declare const badgeVariants: (props?: ({
    variant?: "error" | "outline" | "primary" | "secondary" | "success" | "warning" | "info" | null | undefined;
} & import("class-variance-authority/types").ClassProp) | undefined) => string;
export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement>, VariantProps<typeof badgeVariants> {
    dot?: boolean;
}
export declare function Badge({ className, variant, dot, children, ...props }: BadgeProps): React.JSX.Element;
export interface AvatarProps {
    src?: string;
    alt?: string;
    fallback?: string;
    size?: "sm" | "md" | "lg" | "xl";
    className?: string;
}
export declare function Avatar({ src, alt, fallback, size, className }: AvatarProps): React.JSX.Element;
export interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {
    variant?: "text" | "circular" | "rectangular";
    width?: string | number;
    height?: string | number;
}
export declare function Skeleton({ className, variant, width, height, ...props }: SkeletonProps): React.JSX.Element;
export interface EmptyStateProps {
    icon?: React.ReactNode;
    title: string;
    description?: string;
    action?: React.ReactNode;
    className?: string;
}
export declare function EmptyState({ icon, title, description, action, className }: EmptyStateProps): React.JSX.Element;
export declare function Spinner({ className, size }: {
    className?: string;
    size?: "sm" | "md" | "lg";
}): React.JSX.Element;
export {};
//# sourceMappingURL=Display.d.ts.map