import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Component } from "react";
export class ErrorBoundary extends Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
    }
    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }
    componentDidCatch(error, info) {
        console.error("[ErrorBoundary]", error.message, info.componentStack);
        this.props.onError?.(error, info);
    }
    render() {
        if (this.state.hasError) {
            return (this.props.fallback ?? (_jsxs("div", { className: "flex flex-col items-center justify-center min-h-[300px] p-8 text-center", children: [_jsx("div", { className: "text-4xl mb-4", children: "\u26A0\uFE0F" }), _jsx("h2", { className: "text-lg font-semibold text-gray-700 mb-2", children: "Algo deu errado" }), _jsx("p", { className: "text-sm text-gray-500 mb-4 max-w-md", children: this.state.error?.message ?? "Erro inesperado ao carregar esta seção." }), _jsx("button", { onClick: () => this.setState({ hasError: false, error: null }), className: "px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors", children: "Tentar novamente" })] })));
        }
        return this.props.children;
    }
}
//# sourceMappingURL=ErrorBoundary.js.map