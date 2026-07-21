// ============================================================
// Theme Context — Dynamic theme switching for white-label
// Uses CSS custom properties set on :root by applyTheme().
// ============================================================

import React, { createContext, useContext, useEffect, useState, useCallback } from "react";
import { themes, applyTheme, getThemeById, type Theme } from "../themes/themes";

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

const ThemeContext = createContext<ThemeContextValue | null>(null);

export function useTheme(): ThemeContextValue {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error("useTheme must be used within <ThemeProvider>");
  return ctx;
}

export interface ThemeProviderProps {
  /** Initial theme id (default: "urban") */
  defaultTheme?: string;
  /** Initial dark mode (default: false) */
  defaultDark?: boolean;
  children: React.ReactNode;
}

export function ThemeProvider({
  defaultTheme = "urban",
  defaultDark = false,
  children,
}: ThemeProviderProps) {
  const [themeId, setThemeId] = useState(defaultTheme);
  const [isDark, setIsDark] = useState(defaultDark);

  const theme = getThemeById(themeId) ?? themes[0];

  // Apply CSS custom properties whenever theme or dark mode changes
  useEffect(() => {
    applyTheme(theme);
    document.documentElement.classList.toggle("dark", isDark);
  }, [theme, isDark]);

  const setTheme = useCallback((id: string) => {
    const t = getThemeById(id);
    if (t) setThemeId(id);
  }, []);

  const toggleDarkMode = useCallback(() => {
    setIsDark((prev) => !prev);
  }, []);

  return (
    <ThemeContext.Provider
      value={{ theme, themeList: themes, setTheme, toggleDarkMode, isDark }}
    >
      {children}
    </ThemeContext.Provider>
  );
}
