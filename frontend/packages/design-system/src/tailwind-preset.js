// ============================================================
// Shared Tailwind Preset — Design System
// Single source of truth for Tailwind config.
// Both apps (admin + site) extend this preset.
// ALL colors use CSS variables → theme changes affect both apps instantly.
// ============================================================

/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "var(--color-primary, #D72638)",
          hover: "var(--color-primary-hover, #E84050)",
          light: "var(--color-primary-light, rgba(215,38,56,0.15))",
        },
        secondary: {
          DEFAULT: "var(--color-secondary, #2A2A2A)",
          hover: "var(--color-secondary-hover, #3A3A3A)",
        },
        accent: {
          DEFAULT: "var(--color-accent, #D72638)",
          hover: "var(--color-accent-hover, #E84050)",
        },
        success: "var(--color-success, #27ae60)",
        warning: "var(--color-warning, #f39c12)",
        error: "var(--color-error, #e74c3c)",
        info: "var(--color-info, #3498db)",
        surface: {
          DEFAULT: "var(--color-surface, #1A1A1A)",
          hover: "var(--color-surface-hover, #262626)",
        },
        background: "var(--color-background, #0D0D0D)",
        "bg-dark": "var(--color-background, #0D0D0D)",
        "surface-dark": "var(--color-surface, #1A1A1A)",
        "surface-hover-dark": "var(--color-surface-hover, #262626)",
        "border-dark": "var(--color-border, rgba(215,38,56,0.3))",
        border: {
          DEFAULT: "var(--color-border, rgba(215,38,56,0.3))",
          light: "var(--color-border-light, rgba(215,38,56,0.1))",
        },
        "text-primary": "var(--color-text, #F5F5F5)",
        "text-secondary": "var(--color-text-secondary, #999999)",
        "text-disabled": "var(--color-text-muted, #555555)",
        "text-inverse": "var(--color-text-inverse, #0D0D0D)",
        "text-primary-dark": "var(--color-text, #F5F5F5)",
        "text-secondary-dark": "var(--color-text-secondary, #999999)",
        "text-disabled-dark": "var(--color-text-muted, #555555)",
      },
      fontFamily: {
        heading: ["var(--font-heading, 'Bebas Neue')", "system-ui", "sans-serif"],
        body: ["var(--font-body, 'Montserrat')", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      borderRadius: {
        sm: "var(--radius-sm, 0px)",
        md: "var(--radius-md, 0px)",
        lg: "var(--radius-lg, 4px)",
        xl: "var(--radius-xl, 8px)",
        full: "9999px",
      },
      boxShadow: {
        sm: "var(--shadow-sm, 0 4px 0 rgba(215,38,56,0.3))",
        md: "var(--shadow-md, 0 6px 0 rgba(215,38,56,0.4))",
        lg: "var(--shadow-lg, 0 8px 32px rgba(215,38,56,0.2))",
        xl: "var(--shadow-xl, 0 12px 48px rgba(0,0,0,0.6))",
        glow: "var(--shadow-glow, 0 0 20px rgba(215,38,56,0.5))",
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
