// ============================================================
// Theme System — Shared Types
// Contrato técnico universal para TODOS os temas.
// NUNCA alterar estas interfaces.
// ============================================================

import type { FC, ReactNode } from "react";

// ---- Core Theme Identity ----
export interface ThemeMeta {
  id: string;
  name: string;
  version: string;
  author: string;
  description: string;
  category: "urban" | "luxury" | "minimal" | "classic" | "modern" | "custom";
  tags: string[];
  preview: string; // gradient CSS
}

// ---- Design Tokens ----
export interface ThemeTokens {
  colors: {
    background: string;
    surface: string;
    surfaceAlt: string;
    surfaceHover: string;
    primary: string;
    primaryHover: string;
    primaryLight: string;
    secondary: string;
    secondaryHover: string;
    text: string;
    textSecondary: string;
    textMuted: string;
    textInverse: string;
    accent: string;
    accentHover: string;
    border: string;
    borderLight: string;
    success: string;
    error: string;
    warning: string;
    info: string;
    gradientHero: string;
    gradientSection: string;
    gradientCard: string;
  };
  typography: {
    headingFont: string;
    bodyFont: string;
    monoFont: string;
    scale: {
      display: string;   // hero title
      h1: string;
      h2: string;
      h3: string;
      h4: string;
      h5: string;
      body: string;
      small: string;
      caption: string;
    };
    weight: {
      light: number;
      regular: number;
      medium: number;
      semibold: number;
      bold: number;
      extrabold: number;
    };
    letterSpacing: {
      tight: string;
      normal: string;
      wide: string;
    };
    lineHeight: {
      tight: number;
      normal: number;
      relaxed: number;
    };
  };
  spacing: {
    section: string;
    sectionInner: string;
    element: string;
    card: string;
    gap: string;
    gapSmall: string;
    padding: string;
    container: string;
  };
  borderRadius: {
    none: string;
    sm: string;
    md: string;
    lg: string;
    xl: string;
    "2xl": string;
    full: string;
  };
  shadows: {
    none: string;
    xs: string;
    sm: string;
    md: string;
    lg: string;
    xl: string;
    "2xl": string;
    glow: string;
    glowStrong: string;
    inner: string;
  };
  motion: {
    duration: {
      instant: number;
      fast: number;
      normal: number;
      slow: number;
      slower: number;
    };
    easing: {
      easeOut: [number, number, number, number];
      easeIn: [number, number, number, number];
      easeInOut: [number, number, number, number];
      spring: { stiffness: number; damping: number; mass?: number };
      bounce: { stiffness: number; damping: number };
    };
    stagger: number; // seconds between children
  };
  glassmorphism: {
    enabled: boolean;
    blur: string;
    opacity: number;
    borderOpacity: number;
  };
}

// ---- Component Props (CONTRATO IMBUTÍVEL) ----
// NUNCA alterar estas interfaces. Todos os temas DEVEM segui-las.

export interface HeroProps {
  title: string;
  subtitle?: string;
  cta: { label: string; href: string };
  secondaryCta?: { label: string; href: string };
  backgroundImage?: string;
  backgroundVideo?: string;
  overlayOpacity?: number;
  className?: string;
}

export interface AboutProps {
  title: string;
  description: string;
  highlights?: { icon?: string; label: string; value: string }[];
  image?: string;
  imageAlt?: string;
  className?: string;
}

export interface ServiceItem {
  id: string;
  name: string;
  description: string;
  price: number;
  duration: number; // minutes
  icon?: string;
  image?: string;
  featured?: boolean;
}

export interface ServicesProps {
  title: string;
  subtitle?: string;
  items: ServiceItem[];
  className?: string;
}

export interface Professional {
  id: string;
  name: string;
  role: string;
  bio?: string;
  avatar?: string;
  rating: number;
  reviewCount?: number;
  specialties?: string[];
  socialLinks?: { platform: string; url: string }[];
}

export interface ProfessionalsProps {
  title: string;
  subtitle?: string;
  team: Professional[];
  className?: string;
}

export interface GalleryImage {
  id: string;
  src: string;
  alt: string;
  width?: number;
  height?: number;
  category?: string;
}

export interface GalleryProps {
  title: string;
  subtitle?: string;
  images: GalleryImage[];
  className?: string;
}

export interface Testimonial {
  id: string;
  name: string;
  avatar?: string;
  rating: number;
  text: string;
  date?: string;
  service?: string;
}

export interface TestimonialsProps {
  title: string;
  subtitle?: string;
  testimonials: Testimonial[];
  className?: string;
}

export interface FAQItem {
  id: string;
  question: string;
  answer: string;
}

export interface FAQProps {
  title: string;
  subtitle?: string;
  items: FAQItem[];
  className?: string;
}

export interface BookingCTAProps {
  title: string;
  subtitle?: string;
  cta: { label: string; href: string };
  features?: { icon?: string; text: string }[];
  className?: string;
}

export interface ContactInfo {
  address?: string;
  phone?: string;
  email?: string;
  whatsapp?: string;
  workingHours?: { day: string; hours: string }[];
  mapEmbedUrl?: string;
}

export interface ContactProps {
  title: string;
  subtitle?: string;
  info: ContactInfo;
  className?: string;
}

export interface FooterProps {
  brandName: string;
  brandLogo?: string;
  description?: string;
  links: { title: string; items: { label: string; href: string }[] }[];
  socialLinks?: { platform: string; url: string; icon?: string }[];
  legalLinks?: { label: string; href: string }[];
  className?: string;
}

// ---- THEME COMPONENT CONTRACT ----
// Cada tema DEVE exportar um componente com exatamente estas props.
export interface ThemePageProps {
  /** Dados do tenant vindos da API */
  tenant?: {
    name: string;
    slogan?: string;
    description?: string;
    logo?: string;
    heroImage?: string;
    heroVideo?: string;
    aboutImage?: string;
    services: ServiceItem[];
    professionals: Professional[];
    gallery: GalleryImage[];
    testimonials: Testimonial[];
    faq: FAQItem[];
    contact: ContactInfo;
    socialLinks?: FooterProps["socialLinks"];
    features?: BookingCTAProps["features"];
  };
  /** Override de componentes individuais (para customização extrema) */
  slots?: Partial<{
    Hero: FC<HeroProps>;
    About: FC<AboutProps>;
    Services: FC<ServicesProps>;
    Professionals: FC<ProfessionalsProps>;
    Gallery: FC<GalleryProps>;
    Testimonials: FC<TestimonialsProps>;
    FAQ: FC<FAQProps>;
    BookingCTA: FC<BookingCTAProps>;
    Contact: FC<ContactProps>;
    Footer: FC<FooterProps>;
  }>;
}

// ---- Re-export React types used across themes ----
export type { FC, ReactNode };
