// ============================================================
// ThemeConfigPage — Editor visual completo de tema
// Seções: Tema, Cores, Tipografia, Bordas, Identidade
// Preview em tempo real via CSS Variables.
// ============================================================

import { useState, useEffect, useCallback } from "react";
import { motion } from "framer-motion";
import { themes, applyTheme } from "@barbershop/design-system";
import { tenantAPI } from "../lib/api";
import { ColorPicker, FontSelector, RadiusSlider } from "../components/settings/theme-editor";
import { MediaUploader } from "../components/media";
import { Check, Palette, Type, Frame, Globe, RefreshCw, Sparkles, Link } from "lucide-react";

// ---- Tipos locais para o estado do editor ----
interface EditorState {
  // Aparência
  theme: string;
  primaryColor: string;
  secondaryColor: string;
  backgroundColor: string;
  surfaceColor: string;
  textColor: string;
  textLightColor: string;
  // Tipografia
  headingFont: string;
  bodyFont: string;
  baseFontSize: string;
  // Bordas
  borderRadius: string;
  // Identidade
  logoUrl: string;
  bannerUrl: string;
  faviconUrl: string;
  bannerTitle: string;
  bannerSubtitle: string;
  ctaText: string;
}

const DEFAULT_STATE: EditorState = {
  theme: "urban",
  primaryColor: "#1a1a2e",
  secondaryColor: "#e94560",
  backgroundColor: "#f5f5f5",
  surfaceColor: "#ffffff",
  textColor: "#333333",
  textLightColor: "#666666",
  headingFont: "Inter",
  bodyFont: "Inter",
  baseFontSize: "16px",
  borderRadius: "8px",
  logoUrl: "",
  bannerUrl: "",
  faviconUrl: "",
  bannerTitle: "",
  bannerSubtitle: "",
  ctaText: "Agende Agora",
};

// ---- Mapeia um campo do editor para CSS variable ----
function brandingToCSSVar(field: string): string | null {
  const map: Record<string, string> = {
    primaryColor: "--color-primary",
    secondaryColor: "--color-secondary",
    backgroundColor: "--color-background",
    surfaceColor: "--color-surface",
    textColor: "--color-text",
    textLightColor: "--color-text-secondary",
    headingFont: "--font-heading",
    bodyFont: "--font-body",
  };
  return map[field] || null;
}

export function ThemeConfigPage() {
  const [editor, setEditor] = useState<EditorState>(DEFAULT_STATE);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  // ---- Carregar branding atual do tenant ----
  const loadBranding = useCallback(async () => {
    try {
      setLoading(true);
      const tenant = await tenantAPI.me();
      const branding = tenant.branding as Record<string, unknown> | null;
      if (branding) {
        setEditor((prev) => ({
          ...prev,
          theme: (branding.theme as string) || prev.theme,
          primaryColor: (branding.primary_color as string) || prev.primaryColor,
          secondaryColor: (branding.secondary_color as string) || prev.secondaryColor,
          backgroundColor: (branding.background_color as string) || prev.backgroundColor,
          surfaceColor: (branding.surface_color as string) || prev.surfaceColor,
          textColor: (branding.text_color as string) || prev.textColor,
          textLightColor: (branding.text_light_color as string) || prev.textLightColor,
          headingFont: (branding.heading_font as string) || prev.headingFont,
          bodyFont: (branding.body_font as string) || prev.bodyFont,
          baseFontSize: (branding.base_font_size as string) || prev.baseFontSize,
          borderRadius: (branding.border_radius as string) || prev.borderRadius,
          logoUrl: (branding.logo_url as string) || "",
          bannerUrl: (branding.banner_url as string) || "",
          faviconUrl: (branding.favicon_url as string) || "",
          bannerTitle: (branding.banner_title as string) || "",
          bannerSubtitle: (branding.banner_subtitle as string) || "",
          ctaText: (branding.banner_cta_text as string) || prev.ctaText,
        }));
      }
    } catch {
      // usa defaults
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { loadBranding(); }, [loadBranding]);

  // ---- Aplicar preview em tempo real ----
  const updateField = useCallback((field: keyof EditorState, value: string) => {
    setEditor((prev) => ({ ...prev, [field]: value }));
    setSaved(false);

    // Preview imediato via CSS variable
    const cssVar = brandingToCSSVar(field);
    if (cssVar) {
      document.documentElement.style.setProperty(cssVar, value);
    }
  }, []);

  // ---- Selecionar tema ----
  const selectTheme = useCallback((themeId: string) => {
    updateField("theme", themeId);
    const theme = themes.find((t) => t.id === themeId);
    if (theme) {
      applyTheme(theme);
      // Sincroniza cores do tema com o editor
      setEditor((prev) => ({
        ...prev,
        theme: themeId,
        primaryColor: theme.colors.primary,
        secondaryColor: theme.colors.secondary,
        backgroundColor: theme.colors.background,
        surfaceColor: theme.colors.surface,
        textColor: theme.colors.textPrimary,
        textLightColor: theme.colors.textSecondary,
        headingFont: theme.colors.headingFont,
        bodyFont: theme.colors.bodyFont,
        borderRadius: theme.colors.borderRadius,
      }));
    }
  }, [updateField]);

  // ---- Salvar ----
  const handleSave = useCallback(async () => {
    setSaving(true);
    try {
      await tenantAPI.updateMe({
        branding: {
          theme: editor.theme,
          primary_color: editor.primaryColor,
          secondary_color: editor.secondaryColor,
          background_color: editor.backgroundColor,
          surface_color: editor.surfaceColor,
          text_color: editor.textColor,
          text_light_color: editor.textLightColor,
          heading_font: editor.headingFont,
          body_font: editor.bodyFont,
          base_font_size: editor.baseFontSize,
          border_radius: editor.borderRadius,
          logo_url: editor.logoUrl || null,
          banner_url: editor.bannerUrl || null,
          favicon_url: editor.faviconUrl || null,
          banner_title: editor.bannerTitle || null,
          banner_subtitle: editor.bannerSubtitle || null,
          banner_cta_text: editor.ctaText,
        },
      });
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch {
      // silencioso
    } finally {
      setSaving(false);
    }
  }, [editor]);

  // ---- Loading ----
  if (loading) {
    return (
      <div className="animate-fade-in space-y-4">
        <div className="h-8 w-48 rounded-md bg-surface-hover animate-pulse" />
        <div className="grid gap-4 grid-cols-1 md:grid-cols-2">
          {[1, 2, 3, 4].map((i) => <div key={i} className="h-32 rounded-xl bg-surface-hover animate-pulse" />)}
        </div>
      </div>
    );
  }

  // ---- Render ----
  return (
    <motion.div className="animate-fade-in space-y-6 pb-8" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      {/* Cabeçalho */}
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <h1 className="text-2xl font-bold text-text-primary">Personalizar Tema</h1>
          <p className="text-sm text-text-secondary mt-1">
            Configure a aparência do site da sua barbearia. Alterações são aplicadas em tempo real.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={loadBranding}
            className="flex items-center gap-1.5 text-sm text-text-secondary hover:text-text-primary transition-colors px-3 py-1.5 rounded-lg border border-border"
          >
            <RefreshCw className="h-3.5 w-3.5" />
            Recarregar
          </button>
          <button
            onClick={handleSave}
            disabled={saving}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-primary text-white text-sm font-semibold hover:bg-primary-hover transition-all disabled:opacity-50"
          >
            {saving ? (
              <RefreshCw className="h-4 w-4 animate-spin" />
            ) : saved ? (
              <>
                <Check className="h-4 w-4" /> Salvo
              </>
            ) : (
              <>
                <Sparkles className="h-4 w-4" /> Salvar Alterações
              </>
            )}
          </button>
        </div>
      </div>

      <div className="grid gap-6 grid-cols-1 lg:grid-cols-2">
        {/* ============ SEÇÃO 1: TEMA ============ */}
        <motion.section
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.05 }}
          className="lg:col-span-2 rounded-2xl border border-border bg-surface/50 p-6"
        >
          <div className="flex items-center gap-2 mb-4">
            <Palette className="h-5 w-5 text-primary" />
            <h2 className="text-lg font-bold text-text-primary">Tema</h2>
          </div>
          <div className="grid gap-3 grid-cols-2 sm:grid-cols-3 lg:grid-cols-6">
            {themes.map((theme) => {
              const isSelected = editor.theme === theme.id;
              return (
                <button
                  key={theme.id}
                  onClick={() => selectTheme(theme.id)}
                  className={`relative rounded-xl border-2 overflow-hidden transition-all text-left ${
                    isSelected
                      ? "border-primary shadow-[0_0_16px_-4px_var(--color-primary)]"
                      : "border-border hover:border-border/80"
                  }`}
                >
                  <div className="h-16 flex items-end p-2" style={{ background: theme.preview }}>
                    <span className="text-white text-xs font-semibold drop-shadow-md">{theme.name}</span>
                  </div>
                  <div className="p-2.5">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-medium text-text-primary">{theme.name}</span>
                      {isSelected && <Check className="h-3 w-3 text-primary" />}
                    </div>
                  </div>
                </button>
              );
            })}
          </div>
        </motion.section>

        {/* ============ SEÇÃO 2: CORES ============ */}
        <motion.section
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="rounded-2xl border border-border bg-surface/50 p-6"
        >
          <div className="flex items-center gap-2 mb-4">
            <Palette className="h-5 w-5 text-primary" />
            <h2 className="text-lg font-bold text-text-primary">Cores</h2>
          </div>
          <div className="space-y-4">
            <ColorPicker label="Cor Primária" value={editor.primaryColor} onChange={(v) => updateField("primaryColor", v)} />
            <ColorPicker label="Cor Secundária" value={editor.secondaryColor} onChange={(v) => updateField("secondaryColor", v)} />
            <ColorPicker label="Cor de Fundo" value={editor.backgroundColor} onChange={(v) => updateField("backgroundColor", v)} />
            <ColorPicker label="Cor da Superfície" value={editor.surfaceColor} onChange={(v) => updateField("surfaceColor", v)} />
            <ColorPicker label="Cor do Texto" value={editor.textColor} onChange={(v) => updateField("textColor", v)} />
            <ColorPicker label="Cor do Texto Secundário" value={editor.textLightColor} onChange={(v) => updateField("textLightColor", v)} />
          </div>
        </motion.section>

        {/* ============ SEÇÃO 3: TIPOGRAFIA ============ */}
        <motion.section
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15 }}
          className="rounded-2xl border border-border bg-surface/50 p-6"
        >
          <div className="flex items-center gap-2 mb-4">
            <Type className="h-5 w-5 text-primary" />
            <h2 className="text-lg font-bold text-text-primary">Tipografia</h2>
          </div>
          <div className="space-y-4">
            <FontSelector label="Fonte dos Títulos" value={editor.headingFont} onChange={(v) => updateField("headingFont", v)} />
            <FontSelector label="Fonte do Corpo" value={editor.bodyFont} onChange={(v) => updateField("bodyFont", v)} />
            <div>
              <label className="text-xs font-medium text-text-secondary block mb-1.5">Tamanho Base</label>
              <select
                value={editor.baseFontSize}
                onChange={(e) => updateField("baseFontSize", e.target.value)}
                className="w-full bg-surface rounded-md border border-border px-3 py-2 text-sm text-text-primary focus:outline-none focus:border-primary/50"
              >
                {["14px", "15px", "16px", "17px", "18px", "20px"].map((s) => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>
          </div>
        </motion.section>

        {/* ============ SEÇÃO 4: BORDAS ============ */}
        <motion.section
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="rounded-2xl border border-border bg-surface/50 p-6"
        >
          <div className="flex items-center gap-2 mb-4">
            <Frame className="h-5 w-5 text-primary" />
            <h2 className="text-lg font-bold text-text-primary">Bordas</h2>
          </div>
          <RadiusSlider label="Border Radius" value={editor.borderRadius} onChange={(v) => updateField("borderRadius", v)} />
        </motion.section>

        {/* ============ SEÇÃO 5: IDENTIDADE ============ */}
        <motion.section
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.25 }}
          className="lg:col-span-2 rounded-2xl border border-border bg-surface/50 p-6"
        >
          <div className="flex items-center gap-2 mb-4">
            <Globe className="h-5 w-5 text-primary" />
            <h2 className="text-lg font-bold text-text-primary">Identidade Visual</h2>
          </div>

          {/* ---- Upload: Logo + Banner ---- */}
          <div className="grid gap-4 grid-cols-1 md:grid-cols-2 mb-6">
            <div>
              <label className="text-xs font-medium text-text-secondary block mb-2">Logo</label>
              <MediaUploader
                mediaType="logo"
                accept=".png,.jpg,.jpeg,.webp,.svg"
                maxSize={2 * 1024 * 1024}
                label="Upload do Logo"
                description="PNG ou SVG com fundo transparente recomendado."
                initialPreview={editor.logoUrl || undefined}
                onUploaded={(r) => updateField("logoUrl", r.url)}
                onRemoved={() => updateField("logoUrl", "")}
              />
              <div className="mt-2 flex items-center gap-1.5">
                <Link className="h-3 w-3 text-text-disabled flex-shrink-0" />
                <input
                  type="text"
                  value={editor.logoUrl}
                  onChange={(e) => updateField("logoUrl", e.target.value)}
                  className="flex-1 bg-transparent text-xs text-text-disabled focus:outline-none focus:text-text-secondary transition-colors"
                  placeholder="ou cole uma URL..."
                />
              </div>
            </div>
            <div>
              <label className="text-xs font-medium text-text-secondary block mb-2">Banner / Hero</label>
              <MediaUploader
                mediaType="banner"
                accept="image/*"
                maxSize={5 * 1024 * 1024}
                label="Upload do Banner"
                description="Imagem grande para o topo do site (1920×800 recomendado)."
                initialPreview={editor.bannerUrl || undefined}
                onUploaded={(r) => updateField("bannerUrl", r.url)}
                onRemoved={() => updateField("bannerUrl", "")}
              />
              <div className="mt-2 flex items-center gap-1.5">
                <Link className="h-3 w-3 text-text-disabled flex-shrink-0" />
                <input
                  type="text"
                  value={editor.bannerUrl}
                  onChange={(e) => updateField("bannerUrl", e.target.value)}
                  className="flex-1 bg-transparent text-xs text-text-disabled focus:outline-none focus:text-text-secondary transition-colors"
                  placeholder="ou cole uma URL..."
                />
              </div>
            </div>
          </div>

          {/* ---- Demais campos ---- */}
          <div className="grid gap-4 grid-cols-1 md:grid-cols-2">
            <div>
              <label className="text-xs font-medium text-text-secondary block mb-1.5">Favicon URL</label>
              <div className="flex items-center gap-2">
                <input type="text" value={editor.faviconUrl} onChange={(e) => updateField("faviconUrl", e.target.value)}
                  className="flex-1 bg-surface rounded-md border border-border px-3 py-2 text-sm text-text-primary focus:outline-none focus:border-primary/50" placeholder="https://..." />
                {editor.faviconUrl && <img src={editor.faviconUrl} alt="Favicon preview" className="h-8 w-8 object-contain rounded flex-shrink-0" onError={(e) => { (e.target as HTMLImageElement).style.display = "none"; }} />}
              </div>
            </div>
            <div>
              <label className="text-xs font-medium text-text-secondary block mb-1.5">Título do Banner</label>
              <input type="text" value={editor.bannerTitle} onChange={(e) => updateField("bannerTitle", e.target.value)}
                className="w-full bg-surface rounded-md border border-border px-3 py-2 text-sm text-text-primary focus:outline-none focus:border-primary/50" placeholder="Título principal do site" />
            </div>
            <div>
              <label className="text-xs font-medium text-text-secondary block mb-1.5">Subtítulo do Banner</label>
              <input type="text" value={editor.bannerSubtitle} onChange={(e) => updateField("bannerSubtitle", e.target.value)}
                className="w-full bg-surface rounded-md border border-border px-3 py-2 text-sm text-text-primary focus:outline-none focus:border-primary/50" placeholder="Subtítulo descritivo" />
            </div>
            <div>
              <label className="text-xs font-medium text-text-secondary block mb-1.5">Texto do Botão (CTA)</label>
              <input type="text" value={editor.ctaText} onChange={(e) => updateField("ctaText", e.target.value)}
                className="w-full bg-surface rounded-md border border-border px-3 py-2 text-sm text-text-primary focus:outline-none focus:border-primary/50" placeholder="Ex: Agende Agora" />
            </div>
          </div>
        </motion.section>
      </div>
    </motion.div>
  );
}
