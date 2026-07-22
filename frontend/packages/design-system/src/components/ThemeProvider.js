import { jsx as _jsx } from "react/jsx-runtime";
// ============================================================
// Theme Context — Dynamic theme switching for white-label
// Uses CSS custom properties set on :root by applyTheme().
// ============================================================
import { createContext, useContext, useEffect, useState, useCallback } from "react";
import { themes, applyTheme, getThemeById } from "../themes/themes";
const ThemeContext = createContext(null);
export function useTheme() {
    const ctx = useContext(ThemeContext);
    if (!ctx)
        throw new Error("useTheme must be used within <ThemeProvider>");
    return ctx;
}
export function ThemeProvider({ defaultTheme = "urban", defaultDark = false, children, }) {
    const [themeId, setThemeId] = useState(defaultTheme);
    const [isDark, setIsDark] = useState(defaultDark);
    const theme = getThemeById(themeId) ?? themes[0];
    // Apply CSS custom properties whenever theme or dark mode changes
    useEffect(() => {
        applyTheme(theme);
        document.documentElement.classList.toggle("dark", isDark);
    }, [theme, isDark]);
    const setTheme = useCallback((id) => {
        const t = getThemeById(id);
        if (t)
            setThemeId(id);
    }, []);
    const toggleDarkMode = useCallback(() => {
        setIsDark((prev) => !prev);
    }, []);
    return (_jsx(ThemeContext.Provider, { value: { theme, themeList: themes, setTheme, toggleDarkMode, isDark }, children: children }));
}
//# sourceMappingURL=ThemeProvider.js.map