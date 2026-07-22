// ============================================================
// CLASSIC THEME — Tradicional e Atemporal
// Barbearia raiz, madeira, couro, tradição
// ============================================================
import type { Theme } from "../types";

export const classic: Theme = {
  id: "classic",
  name: "Classic",
  description: "Tradicional e atemporal — barbearia raiz",
  preview: "linear-gradient(135deg, #5C3D2E 0%, #D4A574 50%, #F5F0E8 100%)",

  colors: {
    background: "#F5F0E8",
    surface: "#FFFFFF",
    surfaceHover: "#FDF8F0",
    primary: "#8B4513",
    primaryHover: "#6B3410",
    secondary: "#D4A574",
    text: "#2C1810",
    textSecondary: "#6B5A4E",
    textMuted: "#9B8A7E",
    accent: "#C9A84C",
    accentHover: "#D4B86A",
    border: "rgba(139,69,19,0.2)",
    borderLight: "rgba(139,69,19,0.08)",
    shadow: "0 4px 20px rgba(44,24,16,0.12)",
    success: "#4A7C59",
    error: "#B85450",
    gradient: "linear-gradient(135deg, #F5F0E8 0%, #EDE0D0 100%)",
  },

  typography: {
    headingFont: "'Merriweather', serif",
    bodyFont: "'Lora', serif",
    headingSize: {
      display: "clamp(3rem, 8vw, 6rem)",
      h1: "clamp(2.5rem, 6vw, 4rem)",
      h2: "clamp(2rem, 4vw, 3rem)",
      h3: "clamp(1.5rem, 3vw, 2.2rem)",
      h4: "clamp(1.1rem, 2vw, 1.6rem)",
    },
    bodySize: "1.05rem",
    bodySmall: "0.9rem",
    letterSpacing: "0.01em",
    lineHeight: "1.75",
    headingWeight: 700,
    bodyWeight: 400,
  },

  spacing: {
    section: "clamp(4rem, 10vw, 8rem)",
    sectionInner: "clamp(2.5rem, 6vw, 5rem)",
    card: "1.75rem",
    gap: "1.5rem",
    padding: "1.75rem",
  },

  borderRadius: { sm: "4px", md: "6px", lg: "10px", xl: "16px", full: "9999px" },

  shadows: {
    sm: "0 2px 6px rgba(44,24,16,0.06)",
    md: "0 4px 12px rgba(44,24,16,0.1)",
    lg: "0 6px 20px rgba(44,24,16,0.14)",
    xl: "0 10px 40px rgba(44,24,16,0.18)",
    glow: "0 0 20px rgba(201,168,76,0.2)",
  },

  animations: {
    duration: { fast: 0.3, normal: 0.5, slow: 0.8 },
    easing: {
      ease: [0.4, 0, 0.2, 1],
      easeIn: [0.4, 0, 1, 1],
      easeOut: [0, 0, 0.2, 1],
      spring: { stiffness: 100, damping: 18 },
    },
    fadeUp: {
      initial: { opacity: 0, y: 40 },
      animate: { opacity: 1, y: 0 },
    },
    fadeIn: {
      initial: { opacity: 0 },
      animate: { opacity: 1 },
    },
    scaleIn: {
      initial: { opacity: 0, scale: 0.96 },
      animate: { opacity: 1, scale: 1 },
    },
    stagger: {
      container: { animate: { transition: { staggerChildren: 0.12, delayChildren: 0.08 } } },
      item: { initial: { opacity: 0, y: 30 }, animate: { opacity: 1, y: 0 } },
    },
  },

  hero: {
    overlayOpacity: 0.3,
    textTransform: "none",
    layoutClass: "centered",
    buttonStyle: "square",
    buttonGlow: false,
  },

  cardStyle: {
    glassmorphism: false,
    borderAccent: true,
    hoverEffect: "scale",
    borderRadius: "10px",
  },

  cssVariables: {
    "--font-heading": "'Merriweather', serif",
    "--font-body": "'Lora', serif",
    "--color-primary": "#8B4513",
    "--color-primary-hover": "#6B3410",
    "--color-background": "#F5F0E8",
    "--color-surface": "#FFFFFF",
    "--color-surface-hover": "#FDF8F0",
    "--color-text": "#2C1810",
    "--color-text-secondary": "#6B5A4E",
    "--color-accent": "#C9A84C",
    "--color-border": "rgba(139,69,19,0.2)",
    "--radius": "6px",
    "--shadow": "0 4px 20px rgba(44,24,16,0.12)",
    "--transition": "0.4s cubic-bezier(0.4,0,0.2,1)",
  },
};
