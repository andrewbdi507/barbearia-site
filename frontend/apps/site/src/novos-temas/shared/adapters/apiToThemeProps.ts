// ============================================================
// API → ThemePageProps Adapter
// Funções puras — sem hooks, sem fetch, sem efeitos colaterais.
// Transforma a resposta de /api/v1/site no formato ThemePageProps.
// ============================================================

import type { ThemePageProps } from "../types";

// ---- Tipagem mínima da resposta da API (sem dependência do backend) ----
interface ApiTenant {
  id?: string;
  name?: string;
  subdomain?: string;
  status?: string;
  address?: string;
  phone?: string;
  email?: string;
  whatsapp?: string;
  map_embed_url?: string;
}

interface ApiBranding {
  theme?: string;
  logo_url?: string;
  logo_dark_url?: string;
  favicon_url?: string;
  banner_url?: string;
  primary_color?: string;
  heading_font?: string;
  body_font?: string;
}

interface ApiContent {
  hero_title?: string;
  hero_subtitle?: string;
  hero_cta_text?: string;
  hero_banner_url?: string;
  hero_video_url?: string;
  about_title?: string;
  about_text?: string;
  about_image_url?: string;
  highlights?: string[];
  show_services?: boolean;
  show_team?: boolean;
  show_reviews?: boolean;
  show_gallery?: boolean;
}

interface ApiService {
  id?: string;
  name?: string;
  description?: string;
  base_price?: number;
  effective_price?: number;
  duration_minutes?: number;
  color_tag?: string;
}

interface ApiStaffMember {
  id?: string;
  professional_name?: string;
  photo_url?: string;
  bio?: string;
  specialties?: string[];
  experience_years?: number;
}

interface ApiReview {
  id?: string;
  rating?: number;
  comment?: string;
  tags?: string[];
  created_at?: string;
}

interface ApiBusinessHour {
  day_of_week?: number;
  is_closed?: boolean;
  open_time?: string;
  close_time?: string;
}

interface ApiSocialMedia {
  platform?: string;
  url?: string;
  is_visible?: boolean;
}

interface ApiFAQItem {
  id?: string;
  question?: string;
  answer?: string;
  sort_order?: number;
}

interface ApiGalleryItem {
  id?: string;
  url?: string;
  thumbnail_url?: string;
  alt_text?: string;
  title?: string;
  width?: number;
  height?: number;
  media_type?: string;
}

export interface ApiSiteResponse {
  tenant?: ApiTenant;
  branding?: ApiBranding;
  content?: ApiContent;
  services?: ApiService[];
  team?: ApiStaffMember[];
  reviews?: ApiReview[];
  business_hours?: ApiBusinessHour[];
  social_media?: ApiSocialMedia[];
  faq?: ApiFAQItem[];
  gallery?: ApiGalleryItem[];
}

// ---- Helpers ----

const DAY_LABELS: Record<number, string> = {
  0: "Domingo",
  1: "Segunda",
  2: "Terça",
  3: "Quarta",
  4: "Quinta",
  5: "Sexta",
  6: "Sábado",
};

function formatDayRange(days: number[]): string {
  if (days.length === 0) return "";
  if (days.length === 1) return DAY_LABELS[days[0]] || "";
  // Agrupa dias consecutivos
  const sorted = [...days].sort((a, b) => a - b);
  const first = DAY_LABELS[sorted[0]] || "";
  const last = DAY_LABELS[sorted[sorted.length - 1]] || "";
  return `${first} — ${last}`;
}

function formatTime(raw: string | undefined): string {
  if (!raw) return "";
  // Converte "09:00:00" → "09:00"
  return raw.substring(0, 5);
}

// ---- Mappers ----

function mapServices(apiServices?: ApiService[]): ThemePageProps["tenant"] extends infer T
  ? T extends { services: infer S } ? S : never
  : never {
  if (!apiServices) return [] as never;
  return apiServices.map((s) => ({
    id: s.id || "",
    name: s.name || "",
    description: s.description || "",
    price: s.effective_price ?? s.base_price ?? 0,
    duration: s.duration_minutes || 30,
    featured: false,
  })) as never;
}

function mapProfessionals(apiTeam?: ApiStaffMember[]): ThemePageProps["tenant"] extends infer T
  ? T extends { professionals: infer P } ? P : never
  : never {
  if (!apiTeam) return [] as never;
  return apiTeam.map((p) => ({
    id: p.id || "",
    name: p.professional_name || "",
    role: undefined as unknown as string,
    avatar: p.photo_url,
    bio: p.bio,
    rating: 0,
    reviewCount: 0,
    specialties: p.specialties,
    socialLinks: undefined,
  })) as never;
}

function mapTestimonials(apiReviews?: ApiReview[]): ThemePageProps["tenant"] extends infer T
  ? T extends { testimonials: infer TM } ? TM : never
  : never {
  if (!apiReviews) return [] as never;
  return apiReviews.map((r) => ({
    id: r.id || "",
    name: undefined as unknown as string,
    avatar: undefined,
    rating: r.rating || 5,
    text: r.comment || "",
    date: r.created_at,
    service: undefined,
  })) as never;
}

function mapWorkingHours(apiHours?: ApiBusinessHour[]): { day: string; hours: string }[] {
  if (!apiHours || apiHours.length === 0) return [];

  // Agrupa dias com mesmo horário
  const grouped = new Map<string, number[]>();
  for (const bh of apiHours) {
    if (bh.day_of_week === undefined) continue;
    const key = bh.is_closed
      ? "Fechado"
      : `${formatTime(bh.open_time)} — ${formatTime(bh.close_time)}`;
    const list = grouped.get(key) || [];
    list.push(bh.day_of_week);
    grouped.set(key, list);
  }

  const result: { day: string; hours: string }[] = [];
  for (const [hours, days] of grouped) {
    result.push({ day: formatDayRange(days), hours });
  }
  return result;
}

function mapSocialLinks(apiSocial?: ApiSocialMedia[]): { platform: string; url: string }[] {
  if (!apiSocial) return [];
  return apiSocial
    .filter((s) => s.is_visible !== false)
    .map((s) => ({
      platform: s.platform || "",
      url: s.url || "#",
    }));
}

function mapFeatures(highlights?: string[]): { text: string }[] {
  if (!highlights) return [];
  return highlights.map((text) => ({ text }));
}

// ---- Main Adapter ----

/**
 * Converte a resposta bruta da API no formato esperado por ThemePageProps.
 * Campos indisponíveis no backend são deixados como undefined/[].
 */
export function mapApiToThemePageProps(
  api: ApiSiteResponse
): ThemePageProps["tenant"] {
  return {
    name: api.tenant?.name || "Barbearia",
    slogan: api.content?.hero_subtitle,
    description: api.content?.about_text,
    logo: api.branding?.logo_url,
    heroImage: api.content?.hero_banner_url || api.branding?.banner_url,
    heroVideo: api.content?.hero_video_url,
    aboutImage: api.content?.about_image_url,
    services: mapServices(api.services),
    professionals: mapProfessionals(api.team),
    gallery: (api.gallery || []).map((g) => ({
      id: g.id || "",
      src: g.url || "",
      alt: g.alt_text || g.title || "",
      width: g.width,
      height: g.height,
    })),
    testimonials: mapTestimonials(api.reviews),
    faq: (api.faq || []).map((f) => ({
      id: f.id || "",
      question: f.question || "",
      answer: f.answer || "",
    })),
    contact: {
      address: api.tenant?.address,
      phone: api.tenant?.phone,
      email: api.tenant?.email,
      whatsapp: api.tenant?.whatsapp,
      workingHours: mapWorkingHours(api.business_hours),
      mapEmbedUrl: api.tenant?.map_embed_url,
    },
    socialLinks: mapSocialLinks(api.social_media),
    features: mapFeatures(api.content?.highlights),
  };
}
