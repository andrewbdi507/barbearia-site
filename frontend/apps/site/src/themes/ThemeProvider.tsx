// ============================================================
// ThemeProvider — Unificado Admin + Site
// Usa applyTheme do @barbershop/design-system para CSS variables.
// Ambos apps compartilham as mesmas :root vars.
// ============================================================
import {
  createContext, useContext, useState, useEffect, useMemo, useCallback,
  type ReactNode,
} from "react";
import { applyTheme as applyDSTheme, themes as dsThemes, getThemeById } from "@barbershop/design-system";
import { getTheme, themes as allThemes } from "./index";
import type { Theme } from "./types";

interface ThemeContextValue {
  theme: Theme;
  themeId: string;
  setTheme: (id: string) => void;
  themes: Theme[];
  isLoading: boolean;
  /** Dados completos do site retornados pela API (/api/v1/site).
   *  null = API não respondeu ainda ou falhou (usa fallback). */
  siteData: Record<string, unknown> | null;
}

const ThemeContext = createContext<ThemeContextValue | null>(null);
const DEFAULT_ID = "urban";

function applyFullTheme(themeId: string): void {
  const siteTheme = getTheme(themeId);
  // Apply Site-specific extras
  if (siteTheme) {
    document.body.style.backgroundColor = siteTheme.colors.background;
    document.body.style.color = siteTheme.colors.text;
    document.body.className = `theme-${siteTheme.id}`;
    // Apply Site CSS variables (finer-grained)
    Object.entries(siteTheme.cssVariables).forEach(([key, val]) => {
      document.documentElement.style.setProperty(key, val);
    });
  }
  // Apply design-system CSS variables (used by both Admin + Site Tailwind)
  const dsTheme = getThemeById(themeId);
  if (dsTheme) {
    applyDSTheme(dsTheme);
  }
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [themeId, setThemeId] = useState<string>(() => {
    return localStorage.getItem("barbershop_site_theme") || DEFAULT_ID;
  });
  const [isLoading, setIsLoading] = useState(true);
  const [siteData, setSiteData] = useState<Record<string, unknown> | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const host = window.location.hostname;
        const parts = host.split(".");
        const subdomain = parts.length > 2 ? parts[0] : null;
        const apiBase = (import.meta as Record<string, unknown>).env
          ? (import.meta as unknown as { env: Record<string, string> }).env.VITE_API_URL || ""
          : "";

        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), 4000);

        const resp = await fetch(
          `${apiBase}/api/v1/site?subdomain=${subdomain || "demo"}`,
          { signal: controller.signal, headers: { "Content-Type": "application/json" } }
        );
        clearTimeout(timer);

        if (resp.ok) {
          const data = await resp.json();
          const branding = data.branding || {};
          const apiTheme = branding.theme;

          if (!cancelled) {
            setSiteData(data); // armazena resposta completa
          }

          if (apiTheme && allThemes[apiTheme] && !cancelled) {
            setThemeId(apiTheme);
            localStorage.setItem("barbershop_site_theme", apiTheme);
            applyFullTheme(apiTheme);
            setIsLoading(false);
            return;
          }
        }
      } catch {
        // CORS / timeout / offline → siteData permanece null (fallback)
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
      applyFullTheme(themeId);
    }
  }, [currentTheme, isLoading]);

  const setTheme = useCallback((id: string) => {
    if (allThemes[id]) {
      setThemeId(id);
      localStorage.setItem("barbershop_site_theme", id);
      applyFullTheme(id);
    }
  }, []);

  const value = useMemo<ThemeContextValue>(() => ({
    theme: currentTheme,
    themeId,
    setTheme,
    themes: Object.values(allThemes),
    isLoading,
    siteData,
  }), [currentTheme, themeId, setTheme, isLoading, siteData]);

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