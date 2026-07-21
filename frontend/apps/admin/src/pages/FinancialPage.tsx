import { Card } from "@barbershop/design-system";
import { DollarSign, TrendingUp, CreditCard, ArrowUpRight } from "lucide-react";

export function FinancialPage() {
  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-text-primary">Financeiro</h1>
        <p className="text-sm text-text-secondary mt-1">Acompanhe receitas, pagamentos e assinatura.</p>
      </div>

      <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
        <Card variant="stat">
          <div className="flex items-center gap-2 text-sm text-text-secondary mb-1">
            <DollarSign className="h-4 w-4" /> Receita Total
          </div>
          <div className="text-2xl font-bold text-text-primary">R$ 4.580</div>
          <div className="text-xs text-success mt-1">↑ 18% vs. mês anterior</div>
        </Card>
        <Card variant="stat">
          <div className="flex items-center gap-2 text-sm text-text-secondary mb-1">
            <CreditCard className="h-4 w-4" /> Pagamentos
          </div>
          <div className="text-2xl font-bold text-text-primary">127</div>
          <div className="text-xs text-text-secondary mt-1">Este mês</div>
        </Card>
        <Card variant="stat">
          <div className="flex items-center gap-2 text-sm text-text-secondary mb-1">
            <TrendingUp className="h-4 w-4" /> Ticket Médio
          </div>
          <div className="text-2xl font-bold text-text-primary">R$ 36</div>
          <div className="text-xs text-text-secondary mt-1">por atendimento</div>
        </Card>
        <Card variant="stat">
          <div className="flex items-center gap-2 text-sm text-text-secondary mb-1">
            <ArrowUpRight className="h-4 w-4" /> Plano
          </div>
          <div className="text-2xl font-bold text-text-primary">Pro</div>
          <div className="text-xs text-text-secondary mt-1">R$ 197/mês</div>
        </Card>
      </div>

      <Card>
        <h3 className="text-lg font-semibold mb-4">Últimos Pagamentos</h3>
        <div className="space-y-3">
          {[
            { customer: "João Silva", amount: "R$ 45", method: "PIX", date: "20/07/2026", status: "Pago" },
            { customer: "Ana Costa", amount: "R$ 60", method: "Cartão", date: "20/07/2026", status: "Pago" },
            { customer: "Pedro Lima", amount: "R$ 35", method: "PIX", date: "19/07/2026", status: "Pago" },
          ].map((p, i) => (
            <div key={i} className="flex items-center justify-between border-b border-border pb-3 last:border-0 last:pb-0">
              <div>
                <p className="text-sm font-medium text-text-primary">{p.customer}</p>
                <p className="text-xs text-text-secondary">{p.method} · {p.date}</p>
              </div>
              <div className="text-right">
                <p className="text-sm font-semibold text-text-primary">{p.amount}</p>
                <span className="text-xs text-success">{p.status}</span>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
