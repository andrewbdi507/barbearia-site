// ============================================================
// MINIMAL THEME — Limpo e Essencial
// Design minimalista, funcional, mobile-first
// ============================================================
import type { Theme } from "../types";

export const minimal: Theme = {
  id: "minimal",
  name: "Minimal",
  description: "Limpo e essencial — foco no que importa",
  preview: "linear-gradient(135deg, #FFFFFF 0%, #F5F5F5 50%, #E0E0E0 100%)",

  colors: {
    background: "#FFFFFF",
    surface: "#FAFAFA",
    surfaceHover: "#F0F0F0",
    primary: "#1A1A1A",
    primaryHover: "#333333",
    secondary: "#666666",
    text: "#1A1A1A",
    textSecondary: "#666666",
    textMuted: "#999999",
    accent: "#1A1A1A",
    accentHover: "#333333",
    border: "rgba(0,0,0,0.08)",
    borderLight: "rgba(0,0,0,0.04)",
    shadow: "0 1px 3px rgba(0,0,0,0.06)",
    success: "#22C55E",
    error: "#EF4444",
    gradient: undefined,
  },

  typography: {
    headingFont: "'Inter', sans-serif",
    bodyFont: "'Inter', sans-serif",
    headingSize: {
      display: "clamp(2.5rem, 6vw, 4.5rem)",
      h1: "clamp(2rem, 4.5vw, 3.5rem)",
      h2: "clamp(1.5rem, 3vw, 2.5rem)",
      h3: "clamp(1.2rem, 2.5vw, 1.8rem)",
      h4: "clamp(1rem, 1.5vw, 1.3rem)",
    },
    bodySize: "0.95rem",
    bodySmall: "0.8rem",
    letterSpacing: "-0.01em",
    lineHeight: "1.55",
    headingWeight: 600,
    bodyWeight: 400,
  },

  spacing: {
    section: "clamp(3rem, 8vw, 6rem)",
    sectionInner: "clamp(2rem, 5vw, 4rem)",
    card: "1.25rem",
    gap: "1rem",
    padding: "1.25rem",
  },

  borderRadius: { sm: "4px", md: "6px", lg: "10px", xl: "14px", full: "9999px" },

  shadows: {
    sm: "0 1px 2px rgba(0,0,0,0.04)",
    md: "0 2px 4px rgba(0,0,0,0.06)",
    lg: "0 4px 8px rgba(0,0,0,0.08)",
    xl: "0 8px 16px rgba(0,0,0,0.1)",
    glow: "none",
  },

  animations: {
    duration: { fast: 0.15, normal: 0.25, slow: 0.35 },
    easing: {
      ease: [0.4, 0, 0.2, 1],
      easeIn: [0.4, 0, 1, 1],
      easeOut: [0, 0, 0.2, 1],
      spring: { stiffness: 150, damping: 20 },
    },
    fadeUp: {
      initial: { opacity: 0, y: 16 },
      animate: { opacity: 1, y: 0 },
    },
    fadeIn: {
      initial: { opacity: 0 },
      animate: { opacity: 1 },
    },
    scaleIn: {
      initial: { opacity: 0, scale: 0.98 },
      animate: { opacity: 1, scale: 1 },
    },
    stagger: {
      container: { animate: { transition: { staggerChildren: 0.04, delayChildren: 0.02 } } },
      item: { initial: { opacity: 0, y: 12 }, animate: { opacity: 1, y: 0 } },
    },
  },

  hero: {
    overlayOpacity: 0,
    textTransform: "none",
    layoutClass: "centered-clean",
    buttonStyle: "square",
    buttonGlow: false,
  },

  cardStyle: {
    glassmorphism: false,
    borderAccent: false,
    hoverEffect: "none",
    borderRadius: "6px",
  },

  cssVariables: {
    "--font-heading": "'Inter', sans-serif",
    "--font-body": "'Inter', sans-serif",
    "--color-primary": "#1A1A1A",
    "--color-primary-hover": "#333333",
    "--color-background": "#FFFFFF",
    "--color-surface": "#FAFAFA",
    "--color-surface-hover": "#F0F0F0",
    "--color-text": "#1A1A1A",
    "--color-text-secondary": "#666666",
    "--color-accent": "#1A1A1A",
    "--color-border": "rgba(0,0,0,0.08)",
    "--radius": "6px",
    "--shadow": "0 1px 3px rgba(0,0,0,0.06)",
    "--transition": "0.2s cubic-bezier(0.4,0,0.2,1)",
  },
};
