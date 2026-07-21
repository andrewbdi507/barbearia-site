import { Card } from "@barbershop/design-system";

export function AgendaPage() {
  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-text-primary">Agenda</h1>
        <p className="text-sm text-text-secondary mt-1">Gerencie os agendamentos da barbearia.</p>
      </div>

      {/* Toolbar */}
      <div className="flex flex-wrap items-center gap-3">
        <div className="flex rounded-md border border-border overflow-hidden">
          {["Hoje", "Semana", "Mês"].map((tab) => (
            <button key={tab} className="px-4 py-2 text-sm font-medium hover:bg-surface-hover transition-colors border-r border-border last:border-r-0">
              {tab}
            </button>
          ))}
        </div>
        <div className="flex-1" />
      </div>

      {/* Calendar Grid Placeholder */}
      <Card>
        <div className="h-96 flex items-center justify-center text-text-secondary">
          📅 Grid de agenda multi-profissional (em breve)
        </div>
      </Card>
    </div>
  );
}
