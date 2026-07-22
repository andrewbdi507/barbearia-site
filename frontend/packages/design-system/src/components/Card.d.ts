import * as React from "react";
export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
    /** Visual variant */
    variant?: "default" | "interactive" | "selected" | "stat";
    /** Remove padding */
    noPadding?: boolean;
}
export declare const Card: React.ForwardRefExoticComponent<CardProps & React.RefAttributes<HTMLDivElement>>;
export declare const CardHeader: {
    ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>): React.JSX.Element;
    displayName: string;
};
export declare const CardTitle: {
    ({ className, ...props }: React.HTMLAttributes<HTMLHeadingElement>): React.JSX.Element;
    displayName: string;
};
export declare const CardDescription: {
    ({ className, ...props }: React.HTMLAttributes<HTMLParagraphElement>): React.JSX.Element;
    displayName: string;
};
export declare const CardContent: {
    ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>): React.JSX.Element;
    displayName: string;
};
export declare const CardFooter: {
    ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>): React.JSX.Element;
    displayName: string;
};
export declare const CardStat: {
    ({ label, value, trend }: {
        label: string;
        value: string;
        trend?: string;
    }): React.JSX.Element;
    displayName: string;
};
//# sourceMappingURL=Card.d.ts.map