import React from "react";
import { type Theme } from "../themes/themes";
interface ThemeContextValue {
    /** Current active theme */
    theme: Theme;
    /** All available themes */
    themeList: Theme[];
    /** Switch to a theme by id */
    setTheme: (themeId: string) => void;
    /** Toggle dark mode */
    toggleDarkMode: () => void;
    /** Whether dark mode is active */
    isDark: boolean;
}
export declare function useTheme(): ThemeContextValue;
export interface ThemeProviderProps {
    /** Initial theme id (default: "urban") */
    defaultTheme?: string;
    /** Initial dark mode (default: false) */
    defaultDark?: boolean;
    children: React.ReactNode;
}
export declare function ThemeProvider({ defaultTheme, defaultDark, children, }: ThemeProviderProps): React.JSX.Element;
export {};
//# sourceMappingURL=ThemeProvider.d.ts.map