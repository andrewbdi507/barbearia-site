import { useState, useEffect, useCallback } from "react";
import { motion } from "framer-motion";
import { themes, applyTheme, type Theme } from "@barbershop/design-system";
import { Check, Lock, Palette, RefreshCw, AlertTriangle, Sparkles } from "lucide-react";
import { tenantAPI, planAPI } from "../lib/api";

// ---- Theme slug mapping (design-system id → PlanModel themes array slug) ----
const THEME_SLUG_MAP: Record<string, string> = {
  urban: "urban",
  luxury: "luxury",
  minimal: "minimal",
  classic: "classic",
  modern: "modern",
};

// ---- Component ----

export function ThemeSelector() {
  const [selectedId, setSelectedId] = useState<string>(() => {
    return localStorage.getItem("barbershop_selected_theme") || "urban";
  });
  const [allowedThemes, setAllowedThemes] = useState<string[]>(["minimal"]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  // ---- Fetch plan's allowed themes ----
  const fetchAllowedThemes = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const tenant = await tenantAPI.me();
      const planId = tenant.plan_id;

      if (!planId) {
        setAllowedThemes(["minimal"]);
        return;
      }

      const plan = await planAPI.get(planId);
      setAllowedThemes(plan.themes?.length ? plan.themes : ["minimal"]);
    } catch {
      setError("Erro ao carregar temas disponíveis.");
      setAllowedThemes(["minimal"]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAllowedThemes();
  }, [fetchAllowedThemes]);

  // ---- Handle theme selection ----
  const handleSelect = async (theme: Theme) => {
    const slug = THEME_SLUG_MAP[theme.id] || theme.id;

    if (!allowedThemes.includes(slug)) {
      setError(`Tema "${theme.name}" não está incluso no seu plano. Faça upgrade para acessar.`);
      setTimeout(() => setError(null), 4000);
      return;
    }

    setSelectedId(theme.id);
    applyTheme(theme);
    localStorage.setItem("barbershop_selected_theme", theme.id);
    setSaving(true);

    // Simulate save to backend
    try {
      // TODO: PATCH /api/v1/tenants/me/branding with theme
      await new Promise((r) => setTimeout(r, 400));
      setSuccessMsg(`Tema "${theme.name}" aplicado com sucesso!`);
      setTimeout(() => setSuccessMsg(null), 3000);
    } catch {
      setError("Erro ao salvar tema.");
    } finally {
      setSaving(false);
    }
  };

  // ---- Loading skeleton ----
  if (loading) {
    return (
      <div className="space-y-4 animate-pulse">
        <div className="h-8 w-48 rounded-md bg-surface-hover" />
        <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-56 rounded-2xl bg-surface-hover" />
          ))}
        </div>
      </div>
    );
  }

  // ---- Render ----
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <h2 className="text-xl font-bold text-text-primary">Aparência do Site</h2>
          <p className="text-sm text-text-secondary mt-0.5">
            Escolha um tema para o site público da sua barbearia.
            {allowedThemes.length <= 1 && (
              <span className="text-amber-400 ml-1">
                — Faça upgrade para desbloquear mais temas.
              </span>
            )}
          </p>
        </div>
        <button
          onClick={fetchAllowedThemes}
          className="flex items-center gap-1.5 text-sm text-text-secondary hover:text-text-primary transition-colors"
        >
          <RefreshCw className="h-3.5 w-3.5" />
          Atualizar
        </button>
      </div>

      {/* Error banner */}
      {error && (
        <motion.div
          initial={{ opacity: 0, y: -6 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center gap-2 px-4 py-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-sm"
        >
          <AlertTriangle className="h-4 w-4 shrink-0" />
          {error}
        </motion.div>
      )}

      {/* Success toast */}
      {successMsg && (
        <motion.div
          initial={{ opacity: 0, y: -6 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center gap-2 px-4 py-3 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-sm"
        >
          <Sparkles className="h-4 w-4 shrink-0" />
          {successMsg}
        </motion.div>
      )}

      {/* Saving indicator */}
      {saving && (
        <div className="flex items-center gap-2 text-sm text-text-secondary">
          <RefreshCw className="h-3.5 w-3.5 animate-spin" />
          Salvando tema...
        </div>
      )}

      {/* Theme grid */}
      <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
        {themes.map((theme, i) => {
          const slug = THEME_SLUG_MAP[theme.id] || theme.id;
          const isAllowed = allowedThemes.includes(slug);
          const isSelected = selectedId === theme.id;

          return (
            <motion.div
              key={theme.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.06 }}
              onClick={() => handleSelect(theme)}
              className={`relative rounded-2xl border-2 overflow-hidden transition-all cursor-pointer ${
                isAllowed
                  ? "border-border hover:border-primary/40 hover:shadow-lg"
                  : "border-border/50 opacity-60"
              } ${isSelected ? "border-primary shadow-[0_0_20px_-6px_rgba(var(--color-primary-rgb,215,38,56),0.2)]" : ""}`}
            >
              {/* Lock overlay for unavailable themes */}
              {!isAllowed && (
                <div className="absolute inset-0 z-10 flex flex-col items-center justify-center bg-black/30 backdrop-blur-[1px]">
                  <Lock className="h-6 w-6 text-white/80 mb-1" />
                  <span className="text-xs text-white/80 font-medium">Upgrade necessário</span>
                </div>
              )}

              {/* Preview gradient */}
              <div
                className="h-28 flex items-end p-3"
                style={{ background: theme.preview }}
              >
                <span className="text-white text-sm font-semibold drop-shadow-md">
                  {theme.name}
                </span>
              </div>

              {/* Info */}
              <div className="p-4">
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold text-text-primary text-sm">{theme.name}</h3>
                  {isSelected && (
                    <span className="flex items-center gap-1 text-xs font-medium text-primary">
                      <Check className="h-3.5 w-3.5" /> Ativo
                    </span>
                  )}
                </div>
                <p className="text-xs text-text-secondary mt-1 line-clamp-2">
                  {theme.description}
                </p>

                {/* Color swatches */}
                <div className="flex gap-1.5 mt-3">
                  {[theme.colors.primary, theme.colors.secondary, theme.colors.background].map((color, j) => (
                    <div
                      key={j}
                      className="h-4 w-4 rounded-full border border-border/50"
                      style={{ backgroundColor: color }}
                      title={["Principal", "Destaque", "Fundo"][j]}
                    />
                  ))}
                </div>
              </div>

              {/* Selected indicator border glow */}
              {isSelected && (
                <div className="absolute inset-0 rounded-2xl pointer-events-none ring-2 ring-primary/30" />
              )}
            </motion.div>
          );
        })}
      </div>

      {/* Plan theme info */}
      <div className="flex items-center gap-3 px-4 py-3 rounded-xl bg-surface-hover/50 border border-border/50 text-sm text-text-secondary">
        <Palette className="h-4 w-4 shrink-0 text-text-secondary" />
        <span>
          Temas disponíveis no seu plano:{" "}
          <strong className="text-text-primary">{allowedThemes.length}</strong>
          {allowedThemes.length <= 1 && " — considere fazer upgrade para acessar temas premium."}
        </span>
      </div>
    </div>
  );
}

export default ThemeSelector;
