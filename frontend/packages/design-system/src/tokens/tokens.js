// ============================================================
// Barbershop Design System — Design Tokens
// Single source of truth for all visual properties.
// Tenant-customizable tokens use CSS custom properties.
// ============================================================
export const tokens = {
    colors: {
        primary: {
            DEFAULT: "#1a1a2e",
            hover: "#16213e",
            light: "#e8e8f0",
        },
        secondary: {
            DEFAULT: "#e94560",
            hover: "#d63851",
        },
        success: "#27ae60",
        warning: "#f39c12",
        error: "#e74c3c",
        info: "#3498db",
        surface: {
            DEFAULT: "#ffffff",
            hover: "#f5f5f5",
        },
        background: "#fafafa",
        border: "#e0e0e0",
        text: {
            primary: "#1a1a2e",
            secondary: "#666680",
            disabled: "#9e9eb0",
            inverse: "#ffffff",
        },
    },
    typography: {
        fonts: {
            heading: ["Inter", "system-ui", "sans-serif"],
            body: ["Inter", "system-ui", "sans-serif"],
            mono: ["JetBrains Mono", "monospace"],
        },
        sizes: {
            xs: "12px",
            sm: "14px",
            base: "16px",
            lg: "18px",
            xl: "20px",
            "2xl": "24px",
            "3xl": "32px",
            "4xl": "40px",
        },
        weights: {
            normal: "400",
            medium: "500",
            semibold: "600",
            bold: "700",
            extrabold: "800",
        },
    },
    spacing: {
        unit: 4,
        scale: {
            0: "0",
            1: "4px",
            2: "8px",
            3: "12px",
            4: "16px",
            5: "20px",
            6: "24px",
            8: "32px",
            10: "40px",
            12: "48px",
            16: "64px",
        },
    },
    borderRadius: {
        sm: "4px",
        md: "8px",
        lg: "12px",
        xl: "16px",
        full: "9999px",
    },
    shadows: {
        sm: "0 1px 2px rgba(0,0,0,0.05)",
        md: "0 4px 12px rgba(0,0,0,0.08)",
        lg: "0 8px 24px rgba(0,0,0,0.12)",
        xl: "0 12px 48px rgba(0,0,0,0.15)",
    },
    breakpoints: {
        xs: 0,
        sm: 640,
        md: 768,
        lg: 1024,
        xl: 1280,
        "2xl": 1536,
    },
    motion: {
        durations: {
            instant: 100,
            fast: 200,
            normal: 300,
            slow: 500,
        },
        easings: {
            default: [0.4, 0, 0.2, 1],
            in: [0.4, 0, 1, 1],
            out: [0, 0, 0.2, 1],
            bounce: [0.34, 1.56, 0.64, 1],
        },
    },
    zIndex: {
        base: 0,
        dropdown: 10,
        sticky: 20,
        overlay: 30,
        modal: 40,
        toast: 50,
        tooltip: 60,
    },
};
//# sourceMappingURL=tokens.js.map