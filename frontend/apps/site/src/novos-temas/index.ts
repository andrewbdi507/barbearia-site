// ============================================================
// Theme Library — Index
// Exporta todos os temas com lazy loading para code splitting.
//
// Uso:
//   import { getThemeComponent } from "./novos-temas";
//
//   // Envolva em <Suspense> para fallback durante carregamento:
//   <Suspense fallback={<ThemeSkeleton />}>
//     <ThemeRenderer />
//   </Suspense>
//
//   function ThemeRenderer({ tenant }: { tenant: TenantData }) {
//     const Theme = getThemeComponent(tenant.theme);
//     return <Theme tenant={tenant} />;
//   }
// ============================================================

import { lazy } from "react";

// ---- Lazy-loaded themes (code splitting — cada tema em chunk separado) ----
const UrbanTheme = lazy(() => import("./urban"));
const LuxuryTheme = lazy(() => import("./luxury"));
const MinimalTheme = lazy(() => import("./minimal"));
const ClassicTheme = lazy(() => import("./classic"));
const ModernTheme = lazy(() => import("./modern"));
const CustomTheme = lazy(() => import("./custom"));

// ---- Named exports (para uso direto com switch manual) ----
export { UrbanTheme, LuxuryTheme, MinimalTheme, ClassicTheme, ModernTheme, CustomTheme };

// ---- Shared Types ----
export type {
  ThemeMeta,
  ThemeTokens,
  ThemePageProps,
  HeroProps,
  AboutProps,
  ServiceItem,
  ServicesProps,
  Professional,
  ProfessionalsProps,
  GalleryImage,
  GalleryProps,
  Testimonial,
  TestimonialsProps,
  FAQItem,
  FAQProps,
  BookingCTAProps,
  ContactInfo,
  ContactProps,
  FooterProps,
} from "./shared/types";

// ---- Theme Registry (resolução dinâmica) ----
export const themeRegistry = {
  urban: UrbanTheme,
  luxury: LuxuryTheme,
  minimal: MinimalTheme,
  classic: ClassicTheme,
  modern: ModernTheme,
  custom: CustomTheme,
} as const;

export function getThemeComponent(themeId: string) {
  const key = themeId as keyof typeof themeRegistry;
  return themeRegistry[key] || CustomTheme;
}

