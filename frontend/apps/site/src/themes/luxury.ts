// ============================================================
// LUXURY THEME — Elegante e Sofisticado
// Inspirado em campanhas de moda, streetwear e barbearias premium
// ============================================================
import type { Theme } from "../types";

export const luxury: Theme = {
  id: "luxury",
  name: "Luxury",
  description: "Elegante e sofisticado — para barbearias premium",
  preview: "linear-gradient(135deg, #0D0D0D 0%, #C9A84C 50%, #1A1A1A 100%)",

  colors: {
    background: "#0D0D0D",
    surface: "#1A1A1A",
    surfaceHover: "#242424",
    primary: "#C9A84C",
    primaryHover: "#D4B86A",
    secondary: "#1A1A2E",
    text: "#F5F5F5",
    textSecondary: "#B8B8B8",
    textMuted: "#6B6B6B",
    accent: "#E8D5A3",
    accentHover: "#F0E4C0",
    border: "rgba(201, 168, 76, 0.25)",
    borderLight: "rgba(201, 168, 76, 0.10)",
    shadow: "0 8px 32px rgba(0,0,0,0.5)",
    success: "#4CAF50",
    error: "#D72638",
    gradient: "linear-gradient(135deg, #0D0D0D 0%, #1A1A2E 100%)",
  },

  typography: {
    headingFont: "'Playfair Display', serif",
    bodyFont: "'Cormorant Garamond', serif",
    headingSize: {
      display: "clamp(4rem, 10vw, 8rem)",
      h1: "clamp(3rem, 7vw, 5rem)",
      h2: "clamp(2.2rem, 5vw, 3.5rem)",
      h3: "clamp(1.6rem, 3.5vw, 2.4rem)",
      h4: "clamp(1.2rem, 2.5vw, 1.8rem)",
    },
    bodySize: "1.125rem",
    bodySmall: "0.9rem",
    letterSpacing: "0.02em",
    lineHeight: "1.8",
    headingWeight: 700,
    bodyWeight: 400,
  },

  spacing: {
    section: "clamp(5rem, 12vw, 10rem)",
    sectionInner: "clamp(3rem, 8vw, 6rem)",
    card: "2rem",
    gap: "2rem",
    padding: "2rem",
  },

  borderRadius: { sm: "4px", md: "8px", lg: "16px", xl: "24px", full: "9999px" },

  shadows: {
    sm: "0 2px 8px rgba(0,0,0,0.3)",
    md: "0 4px 16px rgba(0,0,0,0.4)",
    lg: "0 8px 32px rgba(0,0,0,0.5)",
    xl: "0 16px 64px rgba(0,0,0,0.6)",
    glow: "0 0 30px rgba(201,168,76,0.3)",
  },

  animations: {
    duration: { fast: 0.5, normal: 0.8, slow: 1.2 },
    easing: {
      ease: [0.25, 0.1, 0.25, 1],
      easeIn: [0.4, 0, 1, 1],
      easeOut: [0, 0, 0.2, 1],
      spring: { stiffness: 80, damping: 20 },
    },
    fadeUp: {
      initial: { opacity: 0, y: 60 },
      animate: { opacity: 1, y: 0 },
    },
    fadeIn: {
      initial: { opacity: 0 },
      animate: { opacity: 1 },
    },
    scaleIn: {
      initial: { opacity: 0, scale: 0.92 },
      animate: { opacity: 1, scale: 1 },
    },
    stagger: {
      container: { animate: { transition: { staggerChildren: 0.15, delayChildren: 0.1 } } },
      item: { initial: { opacity: 0, y: 40 }, animate: { opacity: 1, y: 0 } },
    },
  },

  hero: {
    overlayOpacity: 0.7,
    textTransform: "none",
    layoutClass: "asymmetric-left",
    buttonStyle: "pill",
    buttonGlow: true,
  },

  cardStyle: {
    glassmorphism: true,
    borderAccent: true,
    hoverEffect: "glow",
    borderRadius: "16px",
  },

  cssVariables: {
    "--font-heading": "'Playfair Display', serif",
    "--font-body": "'Cormorant Garamond', serif",
    "--color-primary": "#C9A84C",
    "--color-primary-hover": "#D4B86A",
    "--color-background": "#0D0D0D",
    "--color-surface": "#1A1A1A",
    "--color-surface-hover": "#242424",
    "--color-text": "#F5F5F5",
    "--color-text-secondary": "#B8B8B8",
    "--color-accent": "#E8D5A3",
    "--color-border": "rgba(201,168,76,0.25)",
    "--radius": "8px",
    "--shadow": "0 8px 32px rgba(0,0,0,0.5)",
    "--transition": "0.6s cubic-bezier(0,0,0.2,1)",
  },
};
