// ============================================================
// ThemeProvider — Contexto global de tema com CSS Variables
// Sincroniza com a API do backend via subdominio.
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
const DEFAULT_ID = "urban";

function applyCSSVariables(theme: Theme): void {
  const root = document.documentElement;
  Object.entries(theme.cssVariables).forEach(([key, val]) => {
    root.style.setProperty(key, val);
  });
  document.body.style.backgroundColor = theme.colors.background;
  document.body.style.color = theme.colors.text;
  document.body.className = `theme-${theme.id}`;
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [themeId, setThemeId] = useState<string>(() => {
    return localStorage.getItem("barbershop_site_theme") || DEFAULT_ID;
  });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        // Extract subdomain from hostname
        const host = window.location.hostname;
        const parts = host.split(".");
        const subdomain = parts.length > 2 ? parts[0] : null;

        // Try API first: GET /api/v1/site?subdomain={subdomain}
        const apiBase = (import.meta as Record<string, unknown>).env
          ? (import.meta as unknown as { env: Record<string, string> }).env.VITE_API_URL || ""
          : "";
        const resp = await fetch(
          `${apiBase}/api/v1/site?subdomain=${subdomain || "demo"}`,
          { headers: { "Content-Type": "application/json" } }
        );

        if (resp.ok) {
          const data = await resp.json();
          const branding = data.branding || {};
          const apiTheme = branding.theme;

          if (apiTheme && allThemes[apiTheme] && !cancelled) {
            setThemeId(apiTheme);
            localStorage.setItem("barbershop_site_theme", apiTheme);
            applyCSSVariables(allThemes[apiTheme]);
            setIsLoading(false);
            return;
          }
        }
      } catch {
        // API offline — fallback to localStorage
      }

      // Fallback: localStorage
      const saved = localStorage.getItem("barbershop_site_theme");
      if (saved && allThemes[saved] && !cancelled) {
        setThemeId(saved);
      }
      setIsLoading(false);
    }

    load();
    return () => { cancelled = true; };
  }, []);

  const currentTheme = useMemo(() => getTheme(themeId), [themeId]);

  useEffect(() => {
    if (!isLoading) {
      applyCSSVariables(currentTheme);
    }
  }, [currentTheme, isLoading]);

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

  if (isLoading) {
    return (
      <div
        className="flex items-center justify-center min-h-screen"
        style={{ backgroundColor: "#0D0D0D", color: "#F5F5F5" }}
      >
        <div className="animate-pulse text-sm tracking-widest uppercase">Carregando...</div>
      </div>
    );
  }

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme(): ThemeContextValue {
  const ctx = useContext(ThemeContext);
  if (!ctx) {
    throw new Error("useTheme must be used inside <ThemeProvider>");
  }
  return ctx;
}