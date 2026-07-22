// ============================================================
// ThemeProvider — Contexto global de tema com CSS Variables
// ============================================================
import {
  createContext, useContext, useState, useEffect, useMemo, useCallback,
  type ReactNode,
} from "react";
import { getTheme, themes as allThemes } from "./index";
import type { Theme } from "./types";

interface ThemeContextValue {
  theme: Theme;
  themeId: string;
  setTheme: (id: string) => void;
  themes: Theme[];
  isLoading: boolean;
}

const ThemeContext = createContext<ThemeContextValue | null>(null);

// ---- Default (fallback) ----
const DEFAULT_ID = "urban";

function applyCSSVariables(theme: Theme): void {
  const root = document.documentElement;
  Object.entries(theme.cssVariables).forEach(([key, val]) => {
    root.style.setProperty(key, val);
  });
  // Extra: apply font
  root.style.setProperty("font-family", theme.typography.bodyFont);
  document.body.style.backgroundColor = theme.colors.background;
  document.body.style.color = theme.colors.text;
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [themeId, setThemeId] = useState<string>(() => {
    return localStorage.getItem("barbershop_site_theme") || DEFAULT_ID;
  });
  const [isLoading, setIsLoading] = useState(true);

  // ---- Load theme from API on mount ----
  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        // Try localStorage first
        const saved = localStorage.getItem("barbershop_site_theme");
        if (saved && allThemes[saved]) {
          if (!cancelled) setThemeId(saved);
        }

        // Then try public API
        const resp = await fetch("/api/v1/site/settings", {
          headers: { "Content-Type": "application/json" },
        });
        if (resp.ok) {
          const data = await resp.json();
          if (data.theme && allThemes[data.theme] && !cancelled) {
            setThemeId(data.theme);
            localStorage.setItem("barbershop_site_theme", data.theme);
          }
        }
      } catch {
        // API offline — use localStorage fallback
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    }

    load();
    return () => { cancelled = true; };
  }, []);

  // ---- Apply CSS variables whenever theme changes ----
  const currentTheme = useMemo(() => getTheme(themeId), [themeId]);

  useEffect(() => {
    if (!isLoading) {
      applyCSSVariables(currentTheme);
    }
  }, [currentTheme, isLoading]);

  // ---- setTheme ----
  const setTheme = useCallback((id: string) => {
    if (allThemes[id]) {
      setThemeId(id);
      localStorage.setItem("barbershop_site_theme", id);
      applyCSSVariables(allThemes[id]);
    }
  }, []);

  const value = useMemo<ThemeContextValue>(() => ({
    theme: currentTheme,
    themeId,
    setTheme,
    themes: Object.values(allThemes),
    isLoading,
  }), [currentTheme, themeId, setTheme, isLoading]);

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

// ---- Hook ----
export function useTheme(): ThemeContextValue {
  const ctx = useContext(ThemeContext);
  if (!ctx) {
    throw new Error("useTheme must be used inside <ThemeProvider>");
  }
  return ctx;
}
