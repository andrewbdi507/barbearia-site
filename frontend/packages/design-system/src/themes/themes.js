// ============================================================
// Theme System — 5 curated themes for tenant white-label
// Each theme overrides CSS custom properties dynamically.
// ============================================================
export const themes = [
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
            textSecondary: "#B0B0B8",
            textMuted: "#707078",
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
            textPrimary: "#F5F0E8",
            textSecondary: "#C0BCB0",
            textMuted: "#7A7668",
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
            primary: "#111111",
            primaryHover: "#333333",
            secondary: "#444444",
            secondaryHover: "#555555",
            background: "#FAFAFA",
            surface: "#FFFFFF",
            surfaceHover: "#EEEEEE",
            textPrimary: "#111111",
            textSecondary: "#444444",
            textMuted: "#666666",
            accent: "#111111",
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
            primary: "#6B3A2A",
            primaryHover: "#8B4A3A",
            secondary: "#C4A265",
            secondaryHover: "#D4B87A",
            background: "#FBF7F0",
            surface: "#FFFFFF",
            surfaceHover: "#EDE0D0",
            textPrimary: "#1A0D08",
            textSecondary: "#5A4A3E",
            textMuted: "#7A6A5E",
            accent: "#C4A265",
            accentHover: "#D4B87A",
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
            textSecondary: "#B0B0C0",
            textMuted: "#6A6A7A",
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
    {
        id: "custom",
        name: "Custom",
        description: "Neutro e personalizável — base para white-label",
        preview: "linear-gradient(135deg, #FFFFFF 0%, #4A5568 100%)",
        colors: {
            primary: "#4A5568",
            primaryHover: "#2D3748",
            secondary: "#718096",
            secondaryHover: "#4A5568",
            background: "#FFFFFF",
            surface: "#F8F9FA",
            surfaceHover: "#E9ECEF",
            textPrimary: "#111820",
            textSecondary: "#3A4555",
            textMuted: "#6B7A8D",
            accent: "#4A5568",
            accentHover: "#2D3748",
            border: "rgba(0,0,0,0.10)",
            borderLight: "rgba(0,0,0,0.05)",
            shadow: "0 4px 12px rgba(0,0,0,0.08)",
            shadowGlow: "0 0 20px rgba(74,85,104,0.2)",
            success: "#38A169",
            error: "#E53E3E",
            headingFont: "Inter",
            bodyFont: "Inter",
            borderRadius: "8px",
            radiusSm: "6px",
            radiusMd: "8px",
            radiusLg: "12px",
            radiusXl: "16px",
        },
    },
];
export function applyTheme(theme) {
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
export function getThemeById(id) {
    return themes.find((t) => t.id === id);
}
//# sourceMappingURL=themes.js.map