import { Component, type ErrorInfo, type ReactNode } from "react";
interface Props {
    children: ReactNode;
    fallback?: ReactNode;
    onError?: (error: Error, info: ErrorInfo) => void;
}
interface State {
    hasError: boolean;
    error: Error | null;
}
export declare class ErrorBoundary extends Component<Props, State> {
    constructor(props: Props);
    static getDerivedStateFromError(error: Error): State;
    componentDidCatch(error: Error, info: ErrorInfo): void;
    render(): ReactNode;
}
export {};
//# sourceMappingURL=ErrorBoundary.d.ts.map