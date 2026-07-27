// ============================================================
// CLASSIC Theme — Design Tokens
// ============================================================

import type { ThemeTokens } from "../../shared/types";

export const tokens: ThemeTokens = {
  colors: {
    background: "#FBF7F0", surface: "#FFFFFF", surfaceAlt: "#F5EDE0", surfaceHover: "#EDE0D0",
    primary: "#6B3A2A", primaryHover: "#8B4A3A", primaryLight: "rgba(107,58,42,0.10)",
    secondary: "#C4A265", secondaryHover: "#D4B87A",
    text: "#1A0D08", textSecondary: "#5A4A3E", textMuted: "#7A6A5E", textInverse: "#FFFFFF",
    accent: "#C4A265", accentHover: "#D4B87A",
    border: "rgba(107,58,42,0.20)", borderLight: "rgba(107,58,42,0.08)",
    success: "#4A7C59", error: "#B85450", warning: "#C4A265", info: "#6B8A9E",
    gradientHero: "linear-gradient(180deg, rgba(251,247,240,0.2) 0%, #FBF7F0 100%)",
    gradientSection: "linear-gradient(180deg, #FBF7F0 0%, #F5EDE0 100%)",
    gradientCard: "linear-gradient(135deg, rgba(107,58,42,0.04) 0%, rgba(196,162,101,0.04) 100%)",
  },
  typography: {
    headingFont: "'Playfair Display', 'Merriweather', serif", bodyFont: "'Lora', 'Cormorant Garamond', serif", monoFont: "'JetBrains Mono', monospace",
    scale: { display: "clamp(3rem, 7vw, 5.5rem)", h1: "clamp(2.5rem, 5.5vw, 4rem)", h2: "clamp(1.8rem, 3.5vw, 2.8rem)", h3: "clamp(1.3rem, 2.5vw, 2rem)", h4: "clamp(1.1rem, 1.8vw, 1.5rem)", h5: "clamp(1rem, 1.3vw, 1.2rem)", body: "1.05rem", small: "0.9rem", caption: "0.8rem" },
    weight: { light: 300, regular: 400, medium: 500, semibold: 600, bold: 700, extrabold: 900 },
    letterSpacing: { tight: "-0.01em", normal: "0.01em", wide: "0.10em" },
    lineHeight: { tight: 1.15, normal: 1.7, relaxed: 1.9 },
  },
  spacing: { section: "clamp(5rem, 12vw, 9rem)", sectionInner: "clamp(3rem, 8vw, 6rem)", element: "clamp(1.5rem, 4vw, 2.5rem)", card: "2rem", gap: "1.75rem", gapSmall: "1rem", padding: "1.75rem", container: "1280px" },
  borderRadius: { none: "0", sm: "3px", md: "5px", lg: "8px", xl: "12px", "2xl": "20px", full: "9999px" },
  shadows: { none: "none", xs: "0 1px 3px rgba(44,24,16,0.04)", sm: "0 3px 8px rgba(44,24,16,0.06)", md: "0 6px 20px rgba(44,24,16,0.10)", lg: "0 8px 30px rgba(44,24,16,0.14)", xl: "0 12px 48px rgba(44,24,16,0.18)", "2xl": "0 16px 64px rgba(44,24,16,0.20)", glow: "0 0 20px rgba(196,162,101,0.25)", glowStrong: "0 0 40px rgba(196,162,101,0.35)", inner: "inset 0 1px 3px rgba(44,24,16,0.06)" },
  motion: { duration: { instant: 100, fast: 250, normal: 450, slow: 700, slower: 1000 }, easing: { easeOut: [0.33, 1, 0.68, 1], easeIn: [0.4, 0, 1, 1], easeInOut: [0.65, 0, 0.35, 1], spring: { stiffness: 100, damping: 18, mass: 1.1 }, bounce: { stiffness: 200, damping: 14 } }, stagger: 0.12 },
  glassmorphism: { enabled: false, blur: "0px", opacity: 0, borderOpacity: 0 },
};
