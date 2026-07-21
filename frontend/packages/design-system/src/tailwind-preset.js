// ============================================================
// Shared Tailwind Preset — Design System
// Single source of truth for Tailwind config.
// Both apps (admin + site) extend this preset.
// ============================================================

/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  theme: {
    extend: {
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
        "bg-dark": "#0f0f1a",
        "surface-dark": "#1a1a2e",
        "surface-hover-dark": "#252540",
        "border-dark": "#2a2a40",
        border: "#e0e0e0",
        "text-primary": "#1a1a2e",
        "text-secondary": "#666680",
        "text-disabled": "#9e9eb0",
        "text-inverse": "#ffffff",
        "text-primary-dark": "#f0f0f5",
        "text-secondary-dark": "#9999aa",
        "text-disabled-dark": "#555566",
      },
      fontFamily: {
        heading: ["Inter", "system-ui", "sans-serif"],
        body: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      borderRadius: {
        sm: "4px",
        md: "8px",
        lg: "12px",
        xl: "16px",
      },
      boxShadow: {
        sm: "0 1px 2px rgba(0,0,0,0.05)",
        md: "0 4px 12px rgba(0,0,0,0.08)",
        lg: "0 8px 24px rgba(0,0,0,0.12)",
        xl: "0 12px 48px rgba(0,0,0,0.15)",
      },
      keyframes: {
        "fade-in": {
          "0%": { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        "slide-up": {
          "0%": { opacity: "0", transform: "translateY(16px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        "scale-in": {
          "0%": { opacity: "0", transform: "scale(0.95)" },
          "100%": { opacity: "1", transform: "scale(1)" },
        },
        shimmer: {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
      },
      animation: {
        "fade-in": "fade-in 0.4s ease-out",
        "slide-up": "slide-up 0.5s ease-out",
        "scale-in": "scale-in 0.3s ease-out",
        shimmer: "shimmer 2s infinite linear",
      },
    },
  },
  plugins: [],
};
