import { Card, Button } from "@barbershop/design-system";
import { Calendar, DollarSign, TrendingUp, Clock, Star, ArrowUp, ArrowDown } from "lucide-react";
import { useEffect, useState } from "react";
import { adminAPI, type DashboardKPI, type TimelineItem } from "../lib/api";
import { Link } from "react-router-dom";

export function DashboardPage() {
  const [kpis, setKpis] = useState<DashboardKPI | null>(null);
  const [timeline, setTimeline] = useState<TimelineItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    adminAPI.getDashboard()
      .then(data => { setKpis(data.kpis); setTimeline(data.today_timeline); })
      .catch(() => { /* fallback to static */ })
      .finally(() => setLoading(false));
  }, []);

  const formatBRL = (cents: number) => `R$ ${(cents / 100).toFixed(2).replace(".", ",")}`;

  const Skeleton = ({ className }: { className?: string }) => (
    <span className={`inline-block animate-pulse rounded bg-surface-hover ${className || "h-4 w-16"}`} />
  );

  const stats = kpis ? [
    { label: "Faturamento Hoje", value: formatBRL(kpis.revenue_today), trend: `${kpis.bookings_completed} atendimentos`, icon: DollarSign, up: true },
    { label: "Agendamentos", value: String(kpis.bookings_confirmed), trend: `${kpis.bookings_cancelled} cancelamentos`, icon: Calendar, up: kpis.bookings_confirmed > kpis.bookings_cancelled },
    { label: "Ocupação", value: `${kpis.occupancy_pct}%`, trend: `${kpis.active_staff} profissionais ativos`, icon: TrendingUp, up: kpis.occupancy_pct >= 50 },
    { label: "Avaliação", value: `${kpis.avg_rating} ⭐`, trend: `${kpis.total_reviews} avaliações`, icon: Star, up: kpis.avg_rating >= 4.5 },
  ] : [];

  const fallbackTimeline = [
    { time: "09:00", customer: "João S.", service: "Corte", status: "confirmed" },
    { time: "09:30", customer: "Pedro L.", service: "Barba", status: "in_progress" },
    { time: "10:00", customer: "Livre", service: "", status: "" },
    { time: "10:30", customer: "Ana C.", service: "Combo", status: "confirmed" },
  ];

  const displayTimeline = timeline.length > 0 ? timeline : fallbackTimeline;

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-text-primary">Dashboard</h1>
          <p className="text-sm text-text-secondary mt-1">Bem-vindo de volta! Veja como está sua barbearia hoje.</p>
        </div>
        <div className="flex gap-2">
          <Link to="/agenda"><Button variant="outline" size="sm"><Calendar className="h-4 w-4 mr-2" />Ver Agenda</Button></Link>
          <Link to="/services"><Button size="sm"><TrendingUp className="h-4 w-4 mr-2" />Novo Atendimento</Button></Link>
        </div>
      </div>

      <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
        {loading ? [1,2,3,4].map(i => (
          <Card key={i} variant="stat">
            <Skeleton className="h-4 w-24 mb-2" />
            <Skeleton className="h-7 w-20 mb-1" />
            <Skeleton className="h-3 w-28" />
          </Card>
        )) : stats.map((stat) => (
          <Card key={stat.label} variant="stat">
            <div className="flex items-center gap-2 text-sm text-text-secondary mb-2">
              <stat.icon className="h-4 w-4" />{stat.label}
            </div>
            <div className="text-2xl font-bold text-text-primary">{stat.value}</div>
            <div className={`flex items-center gap-1 text-xs mt-1 ${stat.up ? "text-success" : "text-error"}`}>
              {stat.up ? <ArrowUp className="h-3 w-3" /> : <ArrowDown className="h-3 w-3" />}{stat.trend}
            </div>
          </Card>
        ))}
      </div>

      <div className="grid gap-6 grid-cols-1 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <h3 className="text-lg font-semibold mb-4">Faturamento — Últimos 7 dias</h3>
          <div className="h-48 flex items-center justify-center text-text-secondary text-sm border border-dashed border-border rounded-md bg-bg/50">
            📊 Gráfico de faturamento (Recharts)
          </div>
        </Card>

        <Card>
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2"><Clock className="h-5 w-5" />Hoje</h3>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {displayTimeline.map((item, i) => (
              <div key={i} className="flex items-center gap-3 text-sm">
                <span className="text-text-secondary font-mono w-12 shrink-0">{item.time}</span>
                <div className={`h-2 w-2 rounded-full shrink-0 ${
                  item.status === "in_progress" ? "bg-warning animate-pulse" :
                  item.status === "confirmed" ? "bg-success" : item.status === "completed" ? "bg-primary" :
                  !item.status ? "bg-border" : "bg-error"}`} />
                <span className={!item.status ? "text-text-secondary italic" : "text-text-primary"}>{item.customer}</span>
                {item.service && <span className="text-text-secondary ml-auto text-xs">{item.service}</span>}
              </div>
            ))}
          </div>
        </Card>
      </div>

      <Card>
        <h3 className="text-lg font-semibold mb-4">Desempenho dos Profissionais</h3>
        <div className="space-y-3">
          {[{ name: "Marcos", bookings: 8, revenue: "R$ 360", rating: "4.9 ⭐", occupancy: 80 },
            { name: "Ricardo", bookings: 4, revenue: "R$ 180", rating: "4.7 ⭐", occupancy: 40 },
            { name: "Lucas", bookings: 6, revenue: "R$ 270", rating: "4.8 ⭐", occupancy: 60 },
          ].map((pro) => (
            <div key={pro.name} className="flex items-center justify-between border-b border-border pb-3 last:border-0 last:pb-0">
              <div className="flex items-center gap-3">
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/10 text-primary font-semibold text-sm">{pro.name[0]}</div>
                <div><p className="text-sm font-medium text-text-primary">{pro.name}</p><p className="text-xs text-text-secondary">{pro.bookings} agend. · {pro.revenue}</p></div>
              </div>
              <div className="text-right">
                <p className="text-sm font-semibold text-text-primary">{pro.rating}</p>
                <div className="mt-1 h-1.5 w-24 rounded-full bg-surface-hover">
                  <div className="h-full rounded-full bg-primary transition-all" style={{ width: `${pro.occupancy}%` }} />
                </div>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
