// ============================================================
// ThemeHomePage — Renderiza o tema ativo com dados do tenant
// Usa lazy loading + Suspense para code splitting.
// ============================================================

import { Suspense, memo } from "react";
import { Helmet } from "react-helmet-async";
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

/** Extrai SEO metadata da resposta da API */
function SiteSEO({ siteData }: { siteData: Record<string, unknown> | null }) {
  if (!siteData) return null;

  const tenant = siteData.tenant as Record<string, unknown> | undefined;
  const seo = siteData.seo as Record<string, unknown> | undefined;
  const branding = siteData.branding as Record<string, unknown> | undefined;
  const jsonLd = siteData.json_ld as Record<string, unknown> | undefined;

  const title = (seo?.title as string) || (tenant?.name as string) || "Barbearia";
  const description = (seo?.description as string) || `Agende seu horário na ${tenant?.name || "barbearia"} online.`;
  const ogImage = (seo?.og as Record<string, unknown>)?.image as string
    || (branding?.banner_url as string)
    || (branding?.logo_url as string)
    || "";
  const canonical = (seo?.canonical as string) || window.location.href;
  const robots = (seo?.robots as string) || "index, follow";

  return (
    <Helmet>
      <title>{title}</title>
      <meta name="description" content={description} />
      <meta name="robots" content={robots} />
      <link rel="canonical" href={canonical} />

      {/* Open Graph */}
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:type" content="website" />
      <meta property="og:url" content={canonical} />
      <meta property="og:site_name" content={tenant?.name as string || "Barbearia"} />
      {ogImage && <meta property="og:image" content={ogImage} />}

      {/* Twitter Cards */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      {ogImage && <meta name="twitter:image" content={ogImage} />}

      {/* JSON-LD */}
      {jsonLd && (
        <script type="application/ld+json">
          {JSON.stringify(jsonLd)}
        </script>
      )}

      {/* Analytics */}
      {seo?.analytics && (
        <>
          {(seo.analytics as Record<string, unknown>).google && (
            <>
              <script async src={`https://www.googletagmanager.com/gtag/js?id=${(seo.analytics as Record<string, unknown>).google}`} />
              <script>{`
                window.dataLayer = window.dataLayer || [];
                function gtag(){dataLayer.push(arguments);}
                gtag('js', new Date());
                gtag('config', '${(seo.analytics as Record<string, unknown>).google}');
              `}</script>
            </>
          )}
        </>
      )}
    </Helmet>
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
    <>
      <SiteSEO siteData={siteData as Record<string, unknown> | null} />
      <Suspense fallback={<ThemeSkeleton />}>
        <ThemeComponent tenant={tenant} />
      </Suspense>
    </>
  );
});
