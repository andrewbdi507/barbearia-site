// ============================================================
// MODERN THEME — Vibrante e Contemporâneo
// Inspirado em Booksy, Fresha, Airbnb — tecnologia com IA
// ============================================================
import type { Theme } from "../types";

export const modern: Theme = {
  id: "modern",
  name: "Modern",
  description: "Vibrante e contemporâneo — tecnologia de ponta",
  preview: "linear-gradient(135deg, #0A0A0A 0%, #00D4FF 50%, #FF00FF 100%)",

  colors: {
    background: "#0A0A0A",
    surface: "rgba(255,255,255,0.04)",
    surfaceHover: "rgba(255,255,255,0.08)",
    primary: "#00D4FF",
    primaryHover: "#33DDFF",
    secondary: "#FF00FF",
    text: "#FFFFFF",
    textSecondary: "#A0A0B0",
    textMuted: "#555566",
    accent: "#00D4FF",
    accentHover: "#33DDFF",
    border: "rgba(255,255,255,0.08)",
    borderLight: "rgba(255,255,255,0.04)",
    shadow: "0 4px 24px rgba(0,212,255,0.15)",
    success: "#00FF88",
    error: "#FF4466",
    gradient: "linear-gradient(135deg, #0A0A0A 0%, #0D1B2A 50%, #1A0A2E 100%)",
  },

  typography: {
    headingFont: "'Inter', sans-serif",
    bodyFont: "'DM Sans', sans-serif",
    headingSize: {
      display: "clamp(3.5rem, 8vw, 6.5rem)",
      h1: "clamp(2.5rem, 6vw, 4rem)",
      h2: "clamp(2rem, 4vw, 3rem)",
      h3: "clamp(1.4rem, 3vw, 2rem)",
      h4: "clamp(1.1rem, 2vw, 1.5rem)",
    },
    bodySize: "1rem",
    bodySmall: "0.85rem",
    letterSpacing: "-0.01em",
    lineHeight: "1.6",
    headingWeight: 800,
    bodyWeight: 400,
  },

  spacing: {
    section: "clamp(4rem, 10vw, 8rem)",
    sectionInner: "clamp(2.5rem, 6vw, 5rem)",
    card: "1.5rem",
    gap: "1.25rem",
    padding: "1.5rem",
  },

  borderRadius: { sm: "8px", md: "14px", lg: "20px", xl: "28px", full: "9999px" },

  shadows: {
    sm: "0 2px 8px rgba(0,212,255,0.08)",
    md: "0 4px 16px rgba(0,212,255,0.12)",
    lg: "0 8px 32px rgba(0,212,255,0.18)",
    xl: "0 12px 48px rgba(0,212,255,0.25)",
    glow: "0 0 40px rgba(0,212,255,0.4), 0 0 80px rgba(255,0,255,0.15)",
  },

  animations: {
    duration: { fast: 0.25, normal: 0.4, slow: 0.6 },
    easing: {
      ease: [0.22, 1, 0.36, 1],
      easeIn: [0.4, 0, 1, 1],
      easeOut: [0, 0, 0.2, 1],
      spring: { stiffness: 200, damping: 15 },
    },
    fadeUp: {
      initial: { opacity: 0, y: 30 },
      animate: { opacity: 1, y: 0 },
    },
    fadeIn: {
      initial: { opacity: 0 },
      animate: { opacity: 1 },
    },
    scaleIn: {
      initial: { opacity: 0, scale: 0.9 },
      animate: { opacity: 1, scale: 1 },
    },
    stagger: {
      container: { animate: { transition: { staggerChildren: 0.08, delayChildren: 0.05 } } },
      item: { initial: { opacity: 0, y: 20 }, animate: { opacity: 1, y: 0 } },
    },
  },

  hero: {
    overlayOpacity: 0.5,
    textTransform: "none",
    layoutClass: "centered",
    buttonStyle: "rounded",
    buttonGlow: true,
  },

  cardStyle: {
    glassmorphism: true,
    borderAccent: false,
    hoverEffect: "lift",
    borderRadius: "20px",
  },

  cssVariables: {
    "--font-heading": "'Inter', sans-serif",
    "--font-body": "'DM Sans', sans-serif",
    "--color-primary": "#00D4FF",
    "--color-primary-hover": "#33DDFF",
    "--color-background": "#0A0A0A",
    "--color-surface": "rgba(255,255,255,0.04)",
    "--color-surface-hover": "rgba(255,255,255,0.08)",
    "--color-text": "#FFFFFF",
    "--color-text-secondary": "#A0A0B0",
    "--color-accent": "#00D4FF",
    "--color-border": "rgba(255,255,255,0.08)",
    "--radius": "14px",
    "--shadow": "0 4px 24px rgba(0,212,255,0.15)",
    "--transition": "0.3s cubic-bezier(0.22,1,0.36,1)",
  },
};
