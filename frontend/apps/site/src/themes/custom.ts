// ============================================================
// CUSTOM THEME — White-Label Base
// Neutro, preparado para receber branding do cliente
// ============================================================
import type { Theme } from "./types";

export const custom: Theme = {
  id: "custom",
  name: "Custom",
  description: "Neutro e personalizável — base para white-label",
  preview: "linear-gradient(135deg, #FFFFFF 0%, #4A5568 100%)",

  colors: {
    background: "#FFFFFF",
    surface: "#F8F9FA",
    surfaceHover: "#E9ECEF",
    primary: "#4A5568",
    primaryHover: "#2D3748",
    secondary: "#718096",
    text: "#111820",
    textSecondary: "#3A4555",
    textMuted: "#6B7A8D",
    accent: "#4A5568",
    accentHover: "#2D3748",
    border: "rgba(0,0,0,0.10)",
    borderLight: "rgba(0,0,0,0.05)",
    shadow: "0 4px 12px rgba(0,0,0,0.08)",
    success: "#38A169",
    error: "#E53E3E",
    gradient: undefined,
  },

  typography: {
    headingFont: "'Inter', sans-serif",
    bodyFont: "'Inter', sans-serif",
    headingSize: {
      display: "clamp(2.8rem, 7vw, 5rem)",
      h1: "clamp(2.2rem, 5vw, 3.5rem)",
      h2: "clamp(1.6rem, 3.5vw, 2.5rem)",
      h3: "clamp(1.2rem, 2.5vw, 1.8rem)",
      h4: "clamp(1rem, 1.5vw, 1.3rem)",
    },
    bodySize: "0.95rem",
    bodySmall: "0.85rem",
    letterSpacing: "-0.015em",
    lineHeight: "1.6",
    headingWeight: 700,
    bodyWeight: 400,
  },

  spacing: {
    section: "clamp(4rem, 10vw, 8rem)",
    sectionInner: "clamp(2.5rem, 6vw, 5rem)",
    card: "1.5rem",
    gap: "1.25rem",
    padding: "1.25rem",
  },

  borderRadius: { sm: "6px", md: "8px", lg: "12px", xl: "16px", full: "9999px" },

  shadows: {
    sm: "0 1px 3px rgba(0,0,0,0.06)",
    md: "0 4px 12px rgba(0,0,0,0.08)",
    lg: "0 8px 24px rgba(0,0,0,0.10)",
    xl: "0 12px 36px rgba(0,0,0,0.12)",
    glow: "0 0 20px rgba(74,85,104,0.2)",
  },

  animations: {
    duration: { fast: 0.18, normal: 0.3, slow: 0.45 },
    easing: {
      ease: [0.4, 0, 0.2, 1],
      easeIn: [0.4, 0, 1, 1],
      easeOut: [0, 0, 0.2, 1],
      spring: { stiffness: 180, damping: 18 },
    },
    fadeUp: {
      initial: { opacity: 0, y: 20 },
      animate: { opacity: 1, y: 0 },
    },
    fadeIn: {
      initial: { opacity: 0 },
      animate: { opacity: 1 },
    },
    scaleIn: {
      initial: { opacity: 0, scale: 0.97 },
      animate: { opacity: 1, scale: 1 },
    },
    stagger: {
      container: { animate: { transition: { staggerChildren: 0.06, delayChildren: 0.03 } } },
      item: { initial: { opacity: 0, y: 16 }, animate: { opacity: 1, y: 0 } },
    },
  },

  hero: {
    overlayOpacity: 0.3,
    textTransform: "none",
    layoutClass: "centered",
    buttonStyle: "rounded",
    buttonGlow: false,
  },

  cardStyle: {
    glassmorphism: false,
    borderAccent: false,
    hoverEffect: "lift",
    borderRadius: "8px",
  },

  cssVariables: {
    "--font-heading": "'Inter', sans-serif",
    "--font-body": "'Inter', sans-serif",
    "--color-primary": "#4A5568",
    "--color-primary-hover": "#2D3748",
    "--color-background": "#FFFFFF",
    "--color-surface": "#F8F9FA",
    "--color-surface-hover": "#E9ECEF",
    "--color-text": "#111820",
    "--color-text-secondary": "#3A4555",
    "--color-accent": "#4A5568",
    "--color-border": "rgba(0,0,0,0.10)",
    "--radius": "8px",
    "--shadow": "0 4px 12px rgba(0,0,0,0.08)",
    "--transition": "0.25s cubic-bezier(0.4,0,0.2,1)",
  },
};
