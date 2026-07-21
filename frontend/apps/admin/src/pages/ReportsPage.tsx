import { Card } from "@barbershop/design-system";
import { BarChart3, TrendingUp, Download, Filter } from "lucide-react";

export function ReportsPage() {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-text-primary">Relatórios</h1>
          <p className="text-sm text-text-secondary mt-1">Análise de desempenho e métricas.</p>
        </div>
        <div className="flex gap-2">
          <button className="flex items-center gap-2 rounded-md border border-border px-3 py-1.5 text-sm text-text-secondary hover:bg-surface-hover">
            <Filter className="h-4 w-4" /> Filtros
          </button>
          <button className="flex items-center gap-2 rounded-md bg-primary px-3 py-1.5 text-sm text-white hover:bg-primary-hover">
            <Download className="h-4 w-4" /> Exportar
          </button>
        </div>
      </div>

      <div className="grid gap-6 grid-cols-1 lg:grid-cols-2">
        <Card>
          <h3 className="text-lg font-semibold mb-4">Faturamento Mensal</h3>
          <div className="h-48 flex items-center justify-center text-text-secondary text-sm border border-dashed border-border rounded-md">
            <BarChart3 className="h-6 w-6 mr-2" /> Gráfico (Recharts)
          </div>
        </Card>
        <Card>
          <h3 className="text-lg font-semibold mb-4">Agendamentos por Serviço</h3>
          <div className="h-48 flex items-center justify-center text-text-secondary text-sm border border-dashed border-border rounded-md">
            <BarChart3 className="h-6 w-6 mr-2" /> Gráfico (Recharts)
          </div>
        </Card>
        <Card>
          <h3 className="text-lg font-semibold mb-4">Clientes Recorrentes</h3>
          <div className="h-48 flex items-center justify-center text-text-secondary text-sm border border-dashed border-border rounded-md">
            <TrendingUp className="h-6 w-6 mr-2" /> Gráfico (Recharts)
          </div>
        </Card>
        <Card>
          <h3 className="text-lg font-semibold mb-4">Taxa de Ocupação</h3>
          <div className="h-48 flex items-center justify-center text-text-secondary text-sm border border-dashed border-border rounded-md">
            <TrendingUp className="h-6 w-6 mr-2" /> Gráfico (Recharts)
          </div>
        </Card>
      </div>
    </div>
  );
}
