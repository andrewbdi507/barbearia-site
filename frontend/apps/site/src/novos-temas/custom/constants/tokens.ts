// ============================================================
// CUSTOM Theme — Design Tokens
// ============================================================

import type { ThemeTokens } from "../../shared/types";

export const tokens: ThemeTokens = {
  colors: {
    background: "#FFFFFF", surface: "#F8F9FA", surfaceAlt: "#F1F3F5", surfaceHover: "#E9ECEF",
    primary: "#4A5568", primaryHover: "#2D3748", primaryLight: "rgba(74,85,104,0.08)",
    secondary: "#718096", secondaryHover: "#4A5568",
    text: "#111820", textSecondary: "#3A4555", textMuted: "#6B7A8D", textInverse: "#FFFFFF",
    accent: "#4A5568", accentHover: "#2D3748",
    border: "rgba(0,0,0,0.10)", borderLight: "rgba(0,0,0,0.05)",
    success: "#38A169", error: "#E53E3E", warning: "#D69E2E", info: "#3182CE",
    gradientHero: "linear-gradient(180deg, #FFFFFF 0%, #F8F9FA 100%)",
    gradientSection: "none", gradientCard: "none",
  },
  typography: {
    headingFont: "'Inter', system-ui, sans-serif", bodyFont: "'Inter', system-ui, sans-serif", monoFont: "'JetBrains Mono', monospace",
    scale: { display: "clamp(2.8rem, 7vw, 5rem)", h1: "clamp(2.2rem, 5vw, 3.5rem)", h2: "clamp(1.6rem, 3.5vw, 2.5rem)", h3: "clamp(1.2rem, 2.5vw, 1.8rem)", h4: "clamp(1rem, 1.5vw, 1.3rem)", h5: "0.95rem", body: "0.95rem", small: "0.85rem", caption: "0.75rem" },
    weight: { light: 300, regular: 400, medium: 500, semibold: 600, bold: 700, extrabold: 800 },
    letterSpacing: { tight: "-0.015em", normal: "0", wide: "0.04em" },
    lineHeight: { tight: 1.2, normal: 1.6, relaxed: 1.75 },
  },
  spacing: { section: "clamp(4rem, 10vw, 8rem)", sectionInner: "clamp(2.5rem, 6vw, 5rem)", element: "clamp(1.5rem, 4vw, 2rem)", card: "1.5rem", gap: "1.25rem", gapSmall: "0.75rem", padding: "1.25rem", container: "1200px" },
  borderRadius: { none: "0", sm: "6px", md: "8px", lg: "12px", xl: "16px", "2xl": "24px", full: "9999px" },
  shadows: { none: "none", xs: "0 1px 2px rgba(0,0,0,0.04)", sm: "0 1px 3px rgba(0,0,0,0.06)", md: "0 4px 12px rgba(0,0,0,0.08)", lg: "0 8px 24px rgba(0,0,0,0.10)", xl: "0 12px 36px rgba(0,0,0,0.12)", "2xl": "0 16px 48px rgba(0,0,0,0.14)", glow: "0 0 20px rgba(74,85,104,0.2)", glowStrong: "0 0 40px rgba(74,85,104,0.3)", inner: "inset 0 1px 3px rgba(0,0,0,0.06)" },
  motion: { duration: { instant: 100, fast: 180, normal: 300, slow: 450, slower: 700 }, easing: { easeOut: [0.4, 0, 0.2, 1], easeIn: [0.4, 0, 1, 1], easeInOut: [0.4, 0, 0.2, 1], spring: { stiffness: 180, damping: 18, mass: 1 }, bounce: { stiffness: 280, damping: 12 } }, stagger: 0.06 },
  glassmorphism: { enabled: false, blur: "0px", opacity: 0, borderOpacity: 0 },
};
