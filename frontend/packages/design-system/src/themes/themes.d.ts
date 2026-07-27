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
export declare const themes: Theme[];
export declare function applyTheme(theme: Theme): void;
export declare function getThemeById(id: string): Theme | undefined;
//# sourceMappingURL=themes.d.ts.map