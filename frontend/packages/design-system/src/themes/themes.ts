// ============================================================
// Theme System — 5 curated themes for tenant white-label
// Each theme overrides CSS custom properties dynamically.
// ============================================================

export interface ThemeColors {
  primary: string;
  primaryHover: string;
  secondary: string;
  secondaryHover: string;
  background: string;
  surface: string;
  surfaceHover: string;
  textPrimary: string;
  textSecondary: string;
  textMuted: string;
  accent: string;
  accentHover: string;
  border: string;
  borderLight: string;
  shadow: string;
  shadowGlow: string;
  success: string;
  error: string;
  headingFont: string;
  bodyFont: string;
  borderRadius: string;
  radiusSm: string;
  radiusMd: string;
  radiusLg: string;
  radiusXl: string;
}

export interface Theme {
  id: string;
  name: string;
  description: string;
  preview: string;
  colors: ThemeColors;
}

export const themes: Theme[] = [
  {
    id: "urban",
    name: "Urban",
    description: "Moderno e ousado — perfeito para barbearias urbanas",
    preview: "linear-gradient(135deg, #1a1a2e 0%, #e94560 100%)",
    colors: {
      primary: "#D72638",
      primaryHover: "#E84050",
      secondary: "#2A2A2A",
      secondaryHover: "#3A3A3A",
      background: "#0D0D0D",
      surface: "#1A1A1A",
      surfaceHover: "#262626",
      textPrimary: "#F5F5F5",
      textSecondary: "#999999",
      textMuted: "#555555",
      accent: "#D72638",
      accentHover: "#E84050",
      border: "rgba(215,38,56,0.3)",
      borderLight: "rgba(215,38,56,0.1)",
      shadow: "0 6px 0 rgba(215,38,56,0.4)",
      shadowGlow: "0 0 20px rgba(215,38,56,0.5)",
      success: "#22C55E",
      error: "#D72638",
      headingFont: "Bebas Neue",
      bodyFont: "Montserrat",
      borderRadius: "0px",
      radiusSm: "0px",
      radiusMd: "0px",
      radiusLg: "4px",
      radiusXl: "8px",
    },
  },
  {
    id: "luxury",
    name: "Luxury",
    description: "Elegante e sofisticado — para barbearias premium",
    preview: "linear-gradient(135deg, #0D0D0D 0%, #C9A84C 50%, #1A1A1A 100%)",
    colors: {
      primary: "#C9A84C",
      primaryHover: "#D4B86A",
      secondary: "#1A1A2E",
      secondaryHover: "#252540",
      background: "#0D0D0D",
      surface: "#1A1A1A",
      surfaceHover: "#242424",
      textPrimary: "#F5F5F5",
      textSecondary: "#B8B8B8",
      textMuted: "#6B6B6B",
      accent: "#E8D5A3",
      accentHover: "#F0E4C0",
      border: "rgba(201,168,76,0.25)",
      borderLight: "rgba(201,168,76,0.1)",
      shadow: "0 8px 32px rgba(0,0,0,0.5)",
      shadowGlow: "0 0 30px rgba(201,168,76,0.3)",
      success: "#4CAF50",
      error: "#D72638",
      headingFont: "Playfair Display",
      bodyFont: "Cormorant Garamond",
      borderRadius: "8px",
      radiusSm: "4px",
      radiusMd: "8px",
      radiusLg: "16px",
      radiusXl: "24px",
    },
  },
  {
    id: "minimal",
    name: "Minimal",
    description: "Limpo e direto — foco no essencial",
    preview: "linear-gradient(135deg, #FFFFFF 0%, #F5F5F5 50%, #E0E0E0 100%)",
    colors: {
      primary: "#1A1A1A",
      primaryHover: "#333333",
      secondary: "#666666",
      secondaryHover: "#777777",
      background: "#FFFFFF",
      surface: "#FAFAFA",
      surfaceHover: "#F0F0F0",
      textPrimary: "#1A1A1A",
      textSecondary: "#666666",
      textMuted: "#999999",
      accent: "#1A1A1A",
      accentHover: "#333333",
      border: "rgba(0,0,0,0.08)",
      borderLight: "rgba(0,0,0,0.04)",
      shadow: "0 1px 3px rgba(0,0,0,0.06)",
      shadowGlow: "none",
      success: "#22C55E",
      error: "#EF4444",
      headingFont: "Inter",
      bodyFont: "Inter",
      borderRadius: "6px",
      radiusSm: "4px",
      radiusMd: "6px",
      radiusLg: "10px",
      radiusXl: "14px",
    },
  },
  {
    id: "classic",
    name: "Classic",
    description: "Tradicional e atemporal — barbearia raiz",
    preview: "linear-gradient(135deg, #5C3D2E 0%, #D4A574 50%, #F5F0E8 100%)",
    colors: {
      primary: "#8B4513",
      primaryHover: "#6B3410",
      secondary: "#D4A574",
      secondaryHover: "#C49564",
      background: "#F5F0E8",
      surface: "#FFFFFF",
      surfaceHover: "#FDF8F0",
      textPrimary: "#2C1810",
      textSecondary: "#6B5A4E",
      textMuted: "#9B8A7E",
      accent: "#C9A84C",
      accentHover: "#D4B86A",
      border: "rgba(139,69,19,0.2)",
      borderLight: "rgba(139,69,19,0.08)",
      shadow: "0 4px 20px rgba(44,24,16,0.12)",
      shadowGlow: "0 0 20px rgba(201,168,76,0.2)",
      success: "#4A7C59",
      error: "#B85450",
      headingFont: "Merriweather",
      bodyFont: "Lora",
      borderRadius: "6px",
      radiusSm: "4px",
      radiusMd: "6px",
      radiusLg: "10px",
      radiusXl: "16px",
    },
  },
  {
    id: "modern",
    name: "Modern",
    description: "Vibrante e contemporâneo — atrai clientes jovens",
    preview: "linear-gradient(135deg, #0A0A0A 0%, #00D4FF 50%, #FF00FF 100%)",
    colors: {
      primary: "#00D4FF",
      primaryHover: "#33DDFF",
      secondary: "#FF00FF",
      secondaryHover: "#FF33FF",
      background: "#0A0A0A",
      surface: "rgba(255,255,255,0.04)",
      surfaceHover: "rgba(255,255,255,0.08)",
      textPrimary: "#FFFFFF",
      textSecondary: "#A0A0B0",
      textMuted: "#555566",
      accent: "#00D4FF",
      accentHover: "#33DDFF",
      border: "rgba(255,255,255,0.08)",
      borderLight: "rgba(255,255,255,0.04)",
      shadow: "0 4px 24px rgba(0,212,255,0.15)",
      shadowGlow: "0 0 40px rgba(0,212,255,0.4), 0 0 80px rgba(255,0,255,0.15)",
      success: "#00FF88",
      error: "#FF4466",
      headingFont: "Inter",
      bodyFont: "DM Sans",
      borderRadius: "14px",
      radiusSm: "8px",
      radiusMd: "14px",
      radiusLg: "20px",
      radiusXl: "28px",
    },
  },
];

export function applyTheme(theme: Theme): void {
  const root = document.documentElement;
  const c = theme.colors;

  // Colors
  root.style.setProperty("--color-primary", c.primary);
  root.style.setProperty("--color-primary-hover", c.primaryHover);
  root.style.setProperty("--color-primary-light", c.primary + "26"); // 15% opacity
  root.style.setProperty("--color-secondary", c.secondary);
  root.style.setProperty("--color-secondary-hover", c.secondaryHover);
  root.style.setProperty("--color-accent", c.accent);
  root.style.setProperty("--color-accent-hover", c.accentHover);
  root.style.setProperty("--color-background", c.background);
  root.style.setProperty("--color-surface", c.surface);
  root.style.setProperty("--color-surface-hover", c.surfaceHover);
  root.style.setProperty("--color-text", c.textPrimary);
  root.style.setProperty("--color-text-secondary", c.textSecondary);
  root.style.setProperty("--color-text-muted", c.textMuted);
  root.style.setProperty("--color-text-inverse", c.background); // inverse of bg
  root.style.setProperty("--color-border", c.border);
  root.style.setProperty("--color-border-light", c.borderLight);
  root.style.setProperty("--color-success", c.success);
  root.style.setProperty("--color-error", c.error);

  // Shadows
  root.style.setProperty("--shadow-sm", c.shadow);
  root.style.setProperty("--shadow-md", c.shadow);
  root.style.setProperty("--shadow-lg", c.shadow);
  root.style.setProperty("--shadow-xl", c.shadow);
  root.style.setProperty("--shadow-glow", c.shadowGlow);

  // Typography
  root.style.setProperty("--font-heading", c.headingFont);
  root.style.setProperty("--font-body", c.bodyFont);

  // Radii
  root.style.setProperty("--radius-sm", c.radiusSm);
  root.style.setProperty("--radius-md", c.radiusMd);
  root.style.setProperty("--radius-lg", c.radiusLg);
  root.style.setProperty("--radius-xl", c.radiusXl);

  // Body class
  document.body.className = `theme-${theme.id}`;
  document.body.style.backgroundColor = c.background;
  document.body.style.color = c.textPrimary;
}

export function getThemeById(id: string): Theme | undefined {
  return themes.find((t) => t.id === id);
}
