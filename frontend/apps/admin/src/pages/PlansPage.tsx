import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Check, Zap, Shield, Infinity, Palette, Users, Brain } from "lucide-react";

interface PlanData {
  id: string;
  slug: string;
  name: string;
  tier: string;
  price_monthly: number;
  price_yearly: number;
  limits: { max_bookings: number; max_staff: number };
  features: string[];
  themes: string[];
  ai_tokens: number | null;
  max_concurrent_users: number | null;
}

const planIcons: Record<string, typeof Zap> = {
  starter: Zap,
  pro: Shield,
  premium: Brain,
  enterprise: Infinity,
};

const defaultPlans: PlanData[] = [
  {
    id: "1", slug: "starter", name: "Starter", tier: "starter",
    price_monthly: 4900, price_yearly: 47040,
    limits: { max_bookings: 100, max_staff: 1 },
    features: ["Agendamento", "WhatsApp básico", "E-mail"],
    themes: ["minimal"],
    ai_tokens: 1000, max_concurrent_users: 5,
  },
  {
    id: "2", slug: "pro", name: "Pro", tier: "pro",
    price_monthly: 9900, price_yearly: 95040,
    limits: { max_bookings: 500, max_staff: 5 },
    features: ["Agendamento", "WhatsApp", "E-mail", "Relatórios", "Multi-profissionais"],
    themes: ["classic", "urban", "minimal"],
    ai_tokens: 5000, max_concurrent_users: 20,
  },
  {
    id: "3", slug: "premium", name: "Premium", tier: "premium",
    price_monthly: 19900, price_yearly: 191040,
    limits: { max_bookings: 999999, max_staff: 999999 },
    features: ["Tudo do Pro", "API Access", "White-label", "Suporte prioritário"],
    themes: ["luxury", "modern", "classic", "urban", "minimal"],
    ai_tokens: 20000, max_concurrent_users: 50,
  },
  {
    id: "4", slug: "enterprise", name: "Enterprise", tier: "enterprise",
    price_monthly: 0, price_yearly: 0,
    limits: { max_bookings: 999999, max_staff: 999999 },
    features: ["Tudo do Premium", "UI personalizada", "Treinamento", "Suporte 24/7"],
    themes: ["luxury", "modern", "classic", "urban", "minimal", "custom"],
    ai_tokens: null, max_concurrent_users: null,
  },
];

const featureLabels: Record<string, string> = {
  booking: "Agendamento ilimitado",
  whatsapp: "WhatsApp",
  whatsapp_basic: "WhatsApp básico",
  email: "E-mail",
  reports: "Relatórios",
  multi_staff: "Multi-profissionais",
  api_access: "API Access",
  white_label: "White-label",
  priority_support: "Suporte prioritário",
  all: "Todas funcionalidades",
  custom_ui: "UI personalizada",
  training: "Treinamento",
  support_24_7: "Suporte 24/7",
};

export default function PlansPage() {
  const [billing, setBilling] = useState<"monthly" | "yearly">("monthly");
  const [selected, setSelected] = useState<string | null>(null);

  return (
    <div className="animate-fade-in p-6 max-w-7xl mx-auto">
      <div className="text-center mb-10">
        <h1 className="text-3xl font-bold text-text-primary mb-2">Planos e Preços</h1>
        <p className="text-text-secondary">Escolha o plano ideal para sua barbearia.</p>
        <div className="inline-flex items-center gap-1 mt-6 bg-surface-hover rounded-full p-1">
          {(["monthly", "yearly"] as const).map((b) => (
            <button
              key={b}
              onClick={() => setBilling(b)}
              className={`px-5 py-2 rounded-full text-sm font-medium transition-all ${
                billing === b ? "bg-primary text-white shadow-sm" : "text-text-secondary hover:text-text-primary"
              }`}
            >
              {b === "monthly" ? "Mensal" : "Anual (20% off)"}
            </button>
          ))}
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-4">
        {defaultPlans.map((plan, i) => {
          const Icon = planIcons[plan.slug] || Zap;
          const isCurrent = plan.slug === "premium";
          const price = billing === "monthly" ? plan.price_monthly : plan.price_yearly;
          return (
            <motion.div
              key={plan.slug}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              whileHover={{ y: -4 }}
              className={`relative rounded-2xl border-2 p-6 transition-all ${
                isCurrent ? "border-primary bg-primary/5" : "border-border hover:border-primary/30"
              } ${plan.slug === "enterprise" ? "lg:col-span-1" : ""}`}
            >
              {isCurrent && (
                <span className="absolute -top-3 left-1/2 -translate-x-1/2 bg-primary text-white text-xs font-bold px-3 py-1 rounded-full">
                  ATUAL
                </span>
              )}
              <div className="flex items-center gap-3 mb-4">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10">
                  <Icon className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <h3 className="font-bold text-lg text-text-primary">{plan.name}</h3>
                  <p className="text-xs text-text-secondary capitalize">{plan.tier}</p>
                </div>
              </div>

              <div className="mb-6">
                {price > 0 ? (
                  <p className="text-3xl font-bold text-text-primary">
                    R$ {(price / 100).toFixed(0)}
                    <span className="text-sm font-normal text-text-secondary">/mês</span>
                  </p>
                ) : (
                  <p className="text-xl font-bold text-text-primary">Sob consulta</p>
                )}
              </div>

              <div className="space-y-2.5 mb-6 text-sm">
                <div className="flex items-center gap-2 text-text-secondary">
                  <Palette className="h-4 w-4" /> {plan.themes.length} temas
                </div>
                <div className="flex items-center gap-2 text-text-secondary">
                  <Zap className="h-4 w-4" /> {plan.limits.max_bookings >= 999999 ? "∞" : plan.limits.max_bookings} agendamentos/mês
                </div>
                <div className="flex items-center gap-2 text-text-secondary">
                  <Users className="h-4 w-4" /> {plan.limits.max_staff >= 999999 ? "∞" : plan.limits.max_staff} profissionais
                </div>
                <div className="flex items-center gap-2 text-text-secondary">
                  <Brain className="h-4 w-4" /> {plan.ai_tokens ? `${(plan.ai_tokens / 1000).toFixed(0)}K` : "∞"} tokens IA
                </div>
              </div>

              <button
                className={`w-full py-3 rounded-full font-bold text-sm transition-all ${
                  isCurrent
                    ? "bg-success/10 text-success border border-success/30 cursor-default"
                    : "bg-primary text-white hover:bg-primary-hover"
                }`}
                disabled={isCurrent}
              >
                {isCurrent ? "Plano Atual" : plan.slug === "enterprise" ? "Falar com Vendas" : "Assinar"}
              </button>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
