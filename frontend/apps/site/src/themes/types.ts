// ============================================================
// Theme System — Types
// ============================================================
import type { ComponentType, ElementType } from "react";

export interface ThemeColors {
  background: string;
  surface: string;
  surfaceHover: string;
  primary: string;
  primaryHover: string;
  secondary: string;
  text: string;
  textSecondary: string;
  textMuted: string;
  accent: string;
  accentHover: string;
  border: string;
  borderLight: string;
  shadow: string;
  success: string;
  error: string;
  gradient?: string;
}

export interface ThemeTypography {
  headingFont: string;
  bodyFont: string;
  headingSize: {
    display: string; // hero
    h1: string;
    h2: string;
    h3: string;
    h4: string;
  };
  bodySize: string;
  bodySmall: string;
  letterSpacing: string;
  lineHeight: string;
  headingWeight: number;
  bodyWeight: number;
}

export interface ThemeSpacing {
  section: string;
  sectionInner: string;
  card: string;
  gap: string;
  padding: string;
}

export interface ThemeBorderRadius {
  sm: string;
  md: string;
  lg: string;
  xl: string;
  full: string;
}

export interface ThemeShadows {
  sm: string;
  md: string;
  lg: string;
  xl: string;
  glow: string;
}

export interface ThemeAnimations {
  duration: {
    fast: number;
    normal: number;
    slow: number;
  };
  easing: {
    ease: [number, number, number, number];
    easeIn: [number, number, number, number];
    easeOut: [number, number, number, number];
    spring: { stiffness: number; damping: number };
  };
  fadeUp: {
    initial: Record<string, unknown>;
    animate: Record<string, unknown>;
  };
  fadeIn: {
    initial: Record<string, unknown>;
    animate: Record<string, unknown>;
  };
  scaleIn: {
    initial: Record<string, unknown>;
    animate: Record<string, unknown>;
  };
  stagger: {
    container: Record<string, unknown>;
    item: Record<string, unknown>;
  };
}

export interface Theme {
  id: string;
  name: string;
  description: string;
  preview: string;
  colors: ThemeColors;
  typography: ThemeTypography;
  spacing: ThemeSpacing;
  borderRadius: ThemeBorderRadius;
  shadows: ThemeShadows;
  animations: ThemeAnimations;
  cssVariables: Record<string, string>;
  // Visual style hints for components
  hero: {
    overlayOpacity: number;
    textTransform: "none" | "uppercase" | "capitalize";
    layoutClass: string;
    buttonStyle: "rounded" | "square" | "pill";
    buttonGlow: boolean;
  };
  cardStyle: {
    glassmorphism: boolean;
    borderAccent: boolean;
    hoverEffect: "scale" | "glow" | "lift" | "none";
    borderRadius: string;
  };
}
