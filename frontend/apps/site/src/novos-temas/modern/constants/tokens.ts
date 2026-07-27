// ============================================================
// MODERN Theme — Design Tokens
// ============================================================

import type { ThemeTokens } from "../../shared/types";

export const tokens: ThemeTokens = {
  colors: {
    background: "#0A0A0F", surface: "rgba(255,255,255,0.04)", surfaceAlt: "#131318", surfaceHover: "rgba(255,255,255,0.08)",
    primary: "#00D4FF", primaryHover: "#33DDFF", primaryLight: "rgba(0,212,255,0.12)",
    secondary: "#B44DFF", secondaryHover: "#C770FF",
    text: "#FFFFFF", textSecondary: "#B0B0C0", textMuted: "#6A6A7A", textInverse: "#0A0A0F",
    accent: "#00D4FF", accentHover: "#33DDFF",
    border: "rgba(255,255,255,0.08)", borderLight: "rgba(255,255,255,0.04)",
    success: "#00FF88", error: "#FF4466", warning: "#FFB444", info: "#44AAFF",
    gradientHero: "linear-gradient(180deg, #0A0A0F 0%, rgba(10,10,15,0.3) 50%, #0A0A0F 100%)",
    gradientSection: "linear-gradient(135deg, #0A0A0F 0%, #0D1520 50%, #100A20 100%)",
    gradientCard: "linear-gradient(135deg, rgba(0,212,255,0.06) 0%, rgba(180,77,255,0.06) 100%)",
  },
  typography: {
    headingFont: "'Inter', 'SF Pro Display', sans-serif", bodyFont: "'Inter', 'DM Sans', sans-serif", monoFont: "'JetBrains Mono', monospace",
    scale: { display: "clamp(3.5rem, 8vw, 6.5rem)", h1: "clamp(2.5rem, 6vw, 4rem)", h2: "clamp(2rem, 4vw, 3rem)", h3: "clamp(1.4rem, 2.5vw, 2rem)", h4: "clamp(1.1rem, 1.8vw, 1.5rem)", h5: "1rem", body: "1rem", small: "0.85rem", caption: "0.75rem" },
    weight: { light: 300, regular: 400, medium: 500, semibold: 600, bold: 700, extrabold: 800 },
    letterSpacing: { tight: "-0.025em", normal: "-0.01em", wide: "0.04em" },
    lineHeight: { tight: 1.05, normal: 1.6, relaxed: 1.75 },
  },
  spacing: { section: "clamp(5rem, 12vw, 9rem)", sectionInner: "clamp(3rem, 8vw, 5rem)", element: "clamp(1.5rem, 4vw, 2.5rem)", card: "1.75rem", gap: "1.5rem", gapSmall: "0.75rem", padding: "1.5rem", container: "1400px" },
  borderRadius: { none: "0", sm: "8px", md: "14px", lg: "20px", xl: "28px", "2xl": "32px", full: "9999px" },
  shadows: { none: "none", xs: "0 2px 6px rgba(0,212,255,0.06)", sm: "0 4px 12px rgba(0,212,255,0.10)", md: "0 8px 24px rgba(0,212,255,0.14)", lg: "0 12px 36px rgba(0,212,255,0.20)", xl: "0 16px 48px rgba(0,212,255,0.25)", "2xl": "0 24px 64px rgba(0,212,255,0.30)", glow: "0 0 30px rgba(0,212,255,0.3), 0 0 60px rgba(180,77,255,0.15)", glowStrong: "0 0 50px rgba(0,212,255,0.5), 0 0 100px rgba(180,77,255,0.25)", inner: "inset 0 1px 2px rgba(255,255,255,0.05)" },
  motion: { duration: { instant: 100, fast: 200, normal: 350, slow: 500, slower: 800 }, easing: { easeOut: [0.22, 1, 0.36, 1], easeIn: [0.4, 0, 1, 1], easeInOut: [0.45, 0, 0.55, 1], spring: { stiffness: 250, damping: 15, mass: 1 }, bounce: { stiffness: 350, damping: 8 } }, stagger: 0.07 },
  glassmorphism: { enabled: true, blur: "24px", opacity: 0.04, borderOpacity: 0.10 },
};
