import * as React from "react";
import { type VariantProps } from "class-variance-authority";
declare const buttonVariants: (props?: ({
    variant?: "link" | "outline" | "primary" | "secondary" | "ghost" | "danger" | "success" | null | undefined;
    size?: "sm" | "md" | "lg" | "xl" | "icon" | null | undefined;
    fullWidth?: boolean | null | undefined;
} & import("class-variance-authority/types").ClassProp) | undefined) => string;
export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>, VariantProps<typeof buttonVariants> {
    /** Render as a child component (e.g., Next.js Link) */
    asChild?: boolean;
    /** Show loading spinner and disable */
    loading?: boolean;
    /** Icon to display before the text */
    leftIcon?: React.ReactNode;
    /** Icon to display after the text */
    rightIcon?: React.ReactNode;
}
export declare const Button: React.ForwardRefExoticComponent<ButtonProps & React.RefAttributes<HTMLButtonElement>>;
export {};
//# sourceMappingURL=Button.d.ts.map