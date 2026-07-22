import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Zap, Shield, Infinity as InfinityIcon, Brain, Palette, Users,
  Check, ChevronDown, ChevronUp, RefreshCw, AlertTriangle, Sparkles,
  ArrowRight, Calendar,
} from "lucide-react";
import { planAPI, tenantAPI, type PlanDTO, type PlanUsageDTO } from "../lib/api";

// ---- Icon mapping ----
const planIcons: Record<string, React.ComponentType<{ className?: string }>> = {
  starter: Zap,
  pro: Shield,
  premium: Brain,
  enterprise: InfinityIcon,
};

// ---- Helpers ----
function fmtPrice(cents: number): string {
  if (cents === 0) return "Sob consulta";
  return `R$ ${(cents / 100).toFixed(0)}`;
}

function fmtTokens(n: number | null): string {
  if (n === null) return "∞";
  if (n >= 1000) return `${(n / 1000).toFixed(0)}K`;
  return String(n);
}

function planBenefits(slug: string): string[] {
  const map: Record<string, string[]> = {
    starter: ["Até 100 agendamentos/mês", "1 profissional", "1 tema (Minimal)", "1K tokens IA", "Suporte por e-mail"],
    pro: ["Até 500 agendamentos/mês", "5 profissionais", "3 temas", "5K tokens IA", "Relatórios", "WhatsApp", "Suporte prioritário"],
    premium: ["Agendamentos ilimitados", "Profissionais ilimitados", "5 temas", "20K tokens IA", "API Access", "White-label", "Suporte prioritário"],
    enterprise: ["Tudo do Premium", "Tema customizado", "Tokens IA ilimitados", "Treinamento", "Suporte 24/7", "SLA garantido"],
  };
  return map[slug] || [];
}

// ---- Component ----

export function PlanSelector() {
  const [plans, setPlans] = useState<PlanDTO[]>([]);
  const [currentPlanId, setCurrentPlanId] = useState<string | null>(null);
  const [_usage, setUsage] = useState<PlanUsageDTO | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [upgrading, setUpgrading] = useState<string | null>(null);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  // ---- Fetch data ----
  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const [plansRes, tenantRes] = await Promise.allSettled([
        planAPI.listAll(),
        tenantAPI.me(),
      ]);

      if (plansRes.status === "fulfilled") {
        setPlans(plansRes.value.plans);
      } else {
        setError("Erro ao carregar planos.");
      }

      if (tenantRes.status === "fulfilled") {
        const tid = tenantRes.value.plan_id;
        setCurrentPlanId(tid);
        if (tid) {
          try {
            const u = await planAPI.getUsage(tid);
            setUsage(u);
          } catch {
            // usage not critical
          }
        }
      }
    } catch {
      setError("Erro de conexão.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // ---- Upgrade handler ----
  const handleUpgrade = async (planId: string) => {
    setUpgrading(planId);
    try {
      // TODO: connect to real payment gateway
      await new Promise((r) => setTimeout(r, 800)); // simula API call
      setSuccessMsg("Plano atualizado com sucesso!");
      setCurrentPlanId(planId);
      setTimeout(() => setSuccessMsg(null), 4000);
    } catch {
      setError("Falha ao atualizar plano.");
    } finally {
      setUpgrading(null);
    }
  };

  // ---- Loading skeleton ----
  if (loading) {
    return (
      <div className="space-y-4 animate-pulse">
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-48 rounded-2xl bg-surface-hover" />
        ))}
      </div>
    );
  }

  // ---- Render ----
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <h2 className="text-xl font-bold text-text-primary">Seu Plano</h2>
          <p className="text-sm text-text-secondary mt-0.5">
            Gerencie sua assinatura e faça upgrade quando precisar.
          </p>
        </div>
        <button
          onClick={fetchData}
          className="flex items-center gap-1.5 text-sm text-text-secondary hover:text-text-primary transition-colors"
        >
          <RefreshCw className="h-3.5 w-3.5" />
          Atualizar
        </button>
      </div>

      {/* Error banner */}
      {error && (
        <div className="flex items-center gap-2 px-4 py-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-sm">
          <AlertTriangle className="h-4 w-4 shrink-0" />
          {error}
        </div>
      )}

      {/* Success toast */}
      <AnimatePresence>
        {successMsg && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="flex items-center gap-2 px-4 py-3 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-sm"
          >
            <Sparkles className="h-4 w-4 shrink-0" />
            {successMsg}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Plan cards */}
      <div className="grid gap-4">
        {plans.map((plan, i) => {
          const Icon = planIcons[plan.slug] || Zap;
          const isCurrent = plan.id === currentPlanId;
          const canDowngrade = plan.tier === "enterprise";
          const benefits = planBenefits(plan.slug);

          return (
            <motion.div
              key={plan.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.08 }}
              className={`relative rounded-2xl border transition-all overflow-hidden ${
                isCurrent
                  ? "border-primary/50 bg-primary/[0.03] shadow-[0_0_20px_-6px_rgba(var(--color-primary-rgb,215,38,56),0.15)]"
                  : "border-border bg-surface hover:border-primary/20"
              }`}
            >
              {/* Current plan badge */}
              {isCurrent && (
                <div className="absolute top-0 right-0">
                  <div className="bg-primary text-white text-xs font-bold px-4 py-1.5 rounded-bl-xl flex items-center gap-1">
                    <Check className="h-3 w-3" /> PLANO ATUAL
                  </div>
                </div>
              )}

              <div className="p-5">
                <div className="flex items-start justify-between gap-4">
                  {/* Left: icon + name + price */}
                  <div className="flex items-start gap-3 flex-1">
                    <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl ${isCurrent ? "bg-primary/10" : "bg-surface-hover"}`}>
                      <Icon className={`h-5 w-5 ${isCurrent ? "text-primary" : "text-text-secondary"}`} />
                    </div>
                    <div className="min-w-0">
                      <div className="flex items-center gap-2 flex-wrap">
                        <h3 className="font-bold text-text-primary">{plan.name}</h3>
                        <span className="text-xs px-2 py-0.5 rounded-full bg-surface-hover text-text-secondary capitalize">
                          {plan.tier}
                        </span>
                      </div>
                      <p className="text-2xl font-bold text-text-primary mt-1">
                        {fmtPrice(plan.price_monthly)}
                        {plan.price_monthly > 0 && (
                          <span className="text-sm font-normal text-text-secondary">/mês</span>
                        )}
                      </p>
                    </div>
                  </div>

                  {/* Right: action button */}
                  <div className="shrink-0">
                    {isCurrent ? (
                      <span className="inline-flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                        <Check className="h-4 w-4" /> Assinado
                      </span>
                    ) : (
                      <button
                        onClick={() => handleUpgrade(plan.id)}
                        disabled={upgrading === plan.id}
                        className={`inline-flex items-center gap-1.5 px-5 py-2 rounded-full text-sm font-bold transition-all ${
                          canDowngrade
                            ? "bg-surface-hover text-text-primary border border-border hover:bg-surface-hover/80"
                            : "bg-primary text-white hover:bg-primary-hover shadow-sm"
                        } disabled:opacity-50`}
                      >
                        {upgrading === plan.id ? (
                          <RefreshCw className="h-4 w-4 animate-spin" />
                        ) : plan.price_monthly === 0 ? (
                          <>Falar com Vendas <ArrowRight className="h-3.5 w-3.5" /></>
                        ) : isCurrent ? (
                          "Atual"
                        ) : (
                          <>Assinar <ArrowRight className="h-3.5 w-3.5" /></>
                        )}
                      </button>
                    )}
                  </div>
                </div>

                {/* Stats row */}
                <div className="flex flex-wrap gap-4 mt-4 pt-4 border-t border-border/50">
                  <div className="flex items-center gap-1.5 text-xs text-text-secondary">
                    <Calendar className="h-3.5 w-3.5" />
                    {(() => {
                      const limits = plan.limits as Record<string, number> | undefined;
                      if (!limits) return "—";
                      const max = limits.max_bookings_per_month;
                      if (!max) return "—";
                      return max >= 999999 ? "∞ agendamentos" : `${max} agendamentos/mês`;
                    })()}
                  </div>
                  <div className="flex items-center gap-1.5 text-xs text-text-secondary">
                    <Palette className="h-3.5 w-3.5" />
                    {plan.themes?.length || 0} temas
                  </div>
                  <div className="flex items-center gap-1.5 text-xs text-text-secondary">
                    <Brain className="h-3.5 w-3.5" />
                    {fmtTokens(plan.ai_tokens)} tokens IA
                  </div>
                  <div className="flex items-center gap-1.5 text-xs text-text-secondary">
                    <Users className="h-3.5 w-3.5" />
                    {plan.max_concurrent_users ?? "∞"} usuários
                  </div>
                </div>

                {/* Expandable benefits */}
                <button
                  onClick={() => setExpandedId(expandedId === plan.id ? null : plan.id)}
                  className="flex items-center gap-1 mt-3 text-xs text-text-secondary hover:text-text-primary transition-colors"
                >
                  {expandedId === plan.id ? (
                    <ChevronUp className="h-3.5 w-3.5" />
                  ) : (
                    <ChevronDown className="h-3.5 w-3.5" />
                  )}
                  {expandedId === plan.id ? "Recolher" : "Ver benefícios"}
                </button>

                <AnimatePresence>
                  {expandedId === plan.id && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      className="overflow-hidden"
                    >
                      <ul className="mt-3 space-y-1.5">
                        {benefits.map((b, j) => (
                          <li key={j} className="flex items-center gap-2 text-sm text-text-secondary">
                            <Check className="h-3.5 w-3.5 text-emerald-400 shrink-0" />
                            {b}
                          </li>
                        ))}
                      </ul>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}

export default PlanSelector;
