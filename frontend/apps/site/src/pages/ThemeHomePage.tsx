// ============================================================
// ThemeHomePage — Renderiza o tema ativo com dados do tenant
// Usa lazy loading + Suspense para code splitting.
// ============================================================

import { Suspense, memo } from "react";
import { useTheme } from "../themes/ThemeProvider";
import { getThemeComponent } from "../novos-temas";
import { mapApiToThemePageProps } from "../novos-temas/shared/adapters/apiToThemeProps";

// ---- Skeleton de carregamento enquanto o tema carrega ----
function ThemeSkeleton() {
  return (
    <div className="min-h-screen flex items-center justify-center" style={{ background: "var(--color-background, #111)" }}>
      <div className="flex flex-col items-center gap-4">
        <div className="w-10 h-10 border-2 border-t-transparent rounded-full animate-spin" style={{ borderColor: "rgba(255,255,255,0.2)", borderTopColor: "transparent" }} />
        <span className="text-sm text-neutral-500">Carregando...</span>
      </div>
    </div>
  );
}

export default memo(function ThemeHomePage() {
  const { themeId, siteData } = useTheme();
  const ThemeComponent = getThemeComponent(themeId);

  // Sem dados da API → mostra skeleton (white-label: nada de fallback fake)
  if (!siteData) {
    return <ThemeSkeleton />;
  }

  const tenant = mapApiToThemePageProps(siteData as Record<string, unknown>);

  return (
    <Suspense fallback={<ThemeSkeleton />}>
      <ThemeComponent tenant={tenant} />
    </Suspense>
  );
});
