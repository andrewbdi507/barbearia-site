// ============================================================
// URBAN THEME — Ousado e Street
// Streetwear, atitude, cinematográfico
// ============================================================
import type { Theme } from "../types";

export const urban: Theme = {
  id: "urban",
  name: "Urban",
  description: "Ousado e street — atitude urbana",
  preview: "linear-gradient(135deg, #0D0D0D 0%, #D72638 50%, #2A2A2A 100%)",

  colors: {
    background: "#0D0D0D",
    surface: "#1A1A1A",
    surfaceHover: "#262626",
    primary: "#D72638",
    primaryHover: "#E84050",
    secondary: "#2A2A2A",
    text: "#F5F5F5",
    textSecondary: "#999999",
    textMuted: "#555555",
    accent: "#D72638",
    accentHover: "#E84050",
    border: "rgba(215,38,56,0.3)",
    borderLight: "rgba(215,38,56,0.1)",
    shadow: "0 8px 32px rgba(215,38,56,0.2)",
    success: "#22C55E",
    error: "#D72638",
    gradient: "linear-gradient(135deg, #0D0D0D 0%, #1A0A0A 100%)",
  },

  typography: {
    headingFont: "'Bebas Neue', sans-serif",
    bodyFont: "'Montserrat', sans-serif",
    headingSize: {
      display: "clamp(5rem, 12vw, 10rem)",
      h1: "clamp(3.5rem, 8vw, 6rem)",
      h2: "clamp(2.5rem, 5vw, 4rem)",
      h3: "clamp(1.8rem, 3.5vw, 2.6rem)",
      h4: "clamp(1.3rem, 2.5vw, 1.8rem)",
    },
    bodySize: "1rem",
    bodySmall: "0.85rem",
    letterSpacing: "0.04em",
    lineHeight: "1.5",
    headingWeight: 700,
    bodyWeight: 500,
  },

  spacing: {
    section: "clamp(4rem, 10vw, 8rem)",
    sectionInner: "clamp(2.5rem, 6vw, 5rem)",
    card: "1.5rem",
    gap: "1.25rem",
    padding: "1.5rem",
  },

  borderRadius: { sm: "0", md: "0", lg: "4px", xl: "8px", full: "9999px" },

  shadows: {
    sm: "0 4px 0 rgba(215,38,56,0.3)",
    md: "0 6px 0 rgba(215,38,56,0.4)",
    lg: "0 8px 0 rgba(215,38,56,0.5)",
    xl: "0 12px 0 rgba(215,38,56,0.6)",
    glow: "0 0 20px rgba(215,38,56,0.5)",
  },

  animations: {
    duration: { fast: 0.2, normal: 0.35, slow: 0.5 },
    easing: {
      ease: [0.25, 0.46, 0.45, 0.94],
      easeIn: [0.55, 0.085, 0.68, 0.53],
      easeOut: [0.25, 0.46, 0.45, 0.94],
      spring: { stiffness: 300, damping: 12 },
    },
    fadeUp: {
      initial: { opacity: 0, y: 80 },
      animate: { opacity: 1, y: 0 },
    },
    fadeIn: {
      initial: { opacity: 0 },
      animate: { opacity: 1 },
    },
    scaleIn: {
      initial: { opacity: 0, scale: 0.85 },
      animate: { opacity: 1, scale: 1 },
    },
    stagger: {
      container: { animate: { transition: { staggerChildren: 0.06, delayChildren: 0.03 } } },
      item: { initial: { opacity: 0, y: 60 }, animate: { opacity: 1, y: 0 } },
    },
  },

  hero: {
    overlayOpacity: 0.6,
    textTransform: "uppercase",
    layoutClass: "fullscreen-left",
    buttonStyle: "square",
    buttonGlow: true,
  },

  cardStyle: {
    glassmorphism: false,
    borderAccent: true,
    hoverEffect: "lift",
    borderRadius: "0",
  },

  cssVariables: {
    "--font-heading": "'Bebas Neue', sans-serif",
    "--font-body": "'Montserrat', sans-serif",
    "--color-primary": "#D72638",
    "--color-primary-hover": "#E84050",
    "--color-background": "#0D0D0D",
    "--color-surface": "#1A1A1A",
    "--color-surface-hover": "#262626",
    "--color-text": "#F5F5F5",
    "--color-text-secondary": "#999999",
    "--color-accent": "#D72638",
    "--color-border": "rgba(215,38,56,0.3)",
    "--radius": "0",
    "--shadow": "0 6px 0 rgba(215,38,56,0.4)",
    "--transition": "0.3s cubic-bezier(0.25,0.46,0.45,0.94)",
  },
};
