export declare const tokens: {
    readonly colors: {
        readonly primary: {
            readonly DEFAULT: "#1a1a2e";
            readonly hover: "#16213e";
            readonly light: "#e8e8f0";
        };
        readonly secondary: {
            readonly DEFAULT: "#e94560";
            readonly hover: "#d63851";
        };
        readonly success: "#27ae60";
        readonly warning: "#f39c12";
        readonly error: "#e74c3c";
        readonly info: "#3498db";
        readonly surface: {
            readonly DEFAULT: "#ffffff";
            readonly hover: "#f5f5f5";
        };
        readonly background: "#fafafa";
        readonly border: "#e0e0e0";
        readonly text: {
            readonly primary: "#1a1a2e";
            readonly secondary: "#666680";
            readonly disabled: "#9e9eb0";
            readonly inverse: "#ffffff";
        };
    };
    readonly typography: {
        readonly fonts: {
            readonly heading: readonly ["Inter", "system-ui", "sans-serif"];
            readonly body: readonly ["Inter", "system-ui", "sans-serif"];
            readonly mono: readonly ["JetBrains Mono", "monospace"];
        };
        readonly sizes: {
            readonly xs: "12px";
            readonly sm: "14px";
            readonly base: "16px";
            readonly lg: "18px";
            readonly xl: "20px";
            readonly "2xl": "24px";
            readonly "3xl": "32px";
            readonly "4xl": "40px";
        };
        readonly weights: {
            readonly normal: "400";
            readonly medium: "500";
            readonly semibold: "600";
            readonly bold: "700";
            readonly extrabold: "800";
        };
    };
    readonly spacing: {
        readonly unit: 4;
        readonly scale: {
            readonly 0: "0";
            readonly 1: "4px";
            readonly 2: "8px";
            readonly 3: "12px";
            readonly 4: "16px";
            readonly 5: "20px";
            readonly 6: "24px";
            readonly 8: "32px";
            readonly 10: "40px";
            readonly 12: "48px";
            readonly 16: "64px";
        };
    };
    readonly borderRadius: {
        readonly sm: "4px";
        readonly md: "8px";
        readonly lg: "12px";
        readonly xl: "16px";
        readonly full: "9999px";
    };
    readonly shadows: {
        readonly sm: "0 1px 2px rgba(0,0,0,0.05)";
        readonly md: "0 4px 12px rgba(0,0,0,0.08)";
        readonly lg: "0 8px 24px rgba(0,0,0,0.12)";
        readonly xl: "0 12px 48px rgba(0,0,0,0.15)";
    };
    readonly breakpoints: {
        readonly xs: 0;
        readonly sm: 640;
        readonly md: 768;
        readonly lg: 1024;
        readonly xl: 1280;
        readonly "2xl": 1536;
    };
    readonly motion: {
        readonly durations: {
            readonly instant: 100;
            readonly fast: 200;
            readonly normal: 300;
            readonly slow: 500;
        };
        readonly easings: {
            readonly default: readonly [0.4, 0, 0.2, 1];
            readonly in: readonly [0.4, 0, 1, 1];
            readonly out: readonly [0, 0, 0.2, 1];
            readonly bounce: readonly [0.34, 1.56, 0.64, 1];
        };
    };
    readonly zIndex: {
        readonly base: 0;
        readonly dropdown: 10;
        readonly sticky: 20;
        readonly overlay: 30;
        readonly modal: 40;
        readonly toast: 50;
        readonly tooltip: 60;
    };
};
export type DesignTokens = typeof tokens;
//# sourceMappingURL=tokens.d.ts.map