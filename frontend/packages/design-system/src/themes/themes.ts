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
  textPrimary: string;
  textSecondary: string;
  headingFont: string;
  bodyFont: string;
  borderRadius: string;
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
      primary: "#1a1a2e",
      primaryHover: "#16213e",
      secondary: "#e94560",
      secondaryHover: "#d63851",
      background: "#fafafa",
      surface: "#ffffff",
      textPrimary: "#1a1a2e",
      textSecondary: "#666680",
      headingFont: "Inter",
      bodyFont: "Inter",
      borderRadius: "8px",
    },
  },
  {
    id: "luxury",
    name: "Luxury",
    description: "Elegante e sofisticado — para barbearias premium",
    preview: "linear-gradient(135deg, #1a1a1a 0%, #c9a96e 100%)",
    colors: {
      primary: "#1a1a1a",
      primaryHover: "#333333",
      secondary: "#c9a96e",
      secondaryHover: "#b8944f",
      background: "#fdfbf7",
      surface: "#ffffff",
      textPrimary: "#1a1a1a",
      textSecondary: "#6b6b6b",
      headingFont: "Playfair Display",
      bodyFont: "Lato",
      borderRadius: "4px",
    },
  },
  {
    id: "minimal",
    name: "Minimal",
    description: "Limpo e direto — foco no essencial",
    preview: "linear-gradient(135deg, #ffffff 0%, #e0e0e0 100%)",
    colors: {
      primary: "#2d2d2d",
      primaryHover: "#1a1a1a",
      secondary: "#666666",
      secondaryHover: "#555555",
      background: "#ffffff",
      surface: "#fafafa",
      textPrimary: "#2d2d2d",
      textSecondary: "#888888",
      headingFont: "Inter",
      bodyFont: "Inter",
      borderRadius: "0px",
    },
  },
  {
    id: "classic",
    name: "Classic",
    description: "Tradicional e atemporal — barbearia raiz",
    preview: "linear-gradient(135deg, #5c3d2e 0%, #b8956a 100%)",
    colors: {
      primary: "#5c3d2e",
      primaryHover: "#4a3024",
      secondary: "#b8956a",
      secondaryHover: "#a07d52",
      background: "#fdf8f0",
      surface: "#ffffff",
      textPrimary: "#3d2b1f",
      textSecondary: "#7a6652",
      headingFont: "Merriweather",
      bodyFont: "Source Sans 3",
      borderRadius: "6px",
    },
  },
  {
    id: "modern",
    name: "Modern",
    description: "Vibrante e contemporâneo — atrai clientes jovens",
    preview: "linear-gradient(135deg, #6366f1 0%, #ec4899 100%)",
    colors: {
      primary: "#6366f1",
      primaryHover: "#5558e8",
      secondary: "#ec4899",
      secondaryHover: "#db2780",
      background: "#f8fafc",
      surface: "#ffffff",
      textPrimary: "#1e293b",
      textSecondary: "#64748b",
      headingFont: "Inter",
      bodyFont: "Inter",
      borderRadius: "12px",
    },
  },
];

export function applyTheme(theme: Theme): void {
  const root = document.documentElement;
  root.style.setProperty("--color-primary", theme.colors.primary);
  root.style.setProperty("--color-primary-hover", theme.colors.primaryHover);
  root.style.setProperty("--color-secondary", theme.colors.secondary);
  root.style.setProperty("--color-secondary-hover", theme.colors.secondaryHover);
  root.style.setProperty("--color-bg", theme.colors.background);
  root.style.setProperty("--color-surface", theme.colors.surface);
  root.style.setProperty("--color-text-primary", theme.colors.textPrimary);
  root.style.setProperty("--color-text-secondary", theme.colors.textSecondary);
  root.style.setProperty("--font-heading", theme.colors.headingFont);
  root.style.setProperty("--font-body", theme.colors.bodyFont);
  root.style.setProperty("--radius", theme.colors.borderRadius);
}

export function getThemeById(id: string): Theme | undefined {
  return themes.find((t) => t.id === id);
}
