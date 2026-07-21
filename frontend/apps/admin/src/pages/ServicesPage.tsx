import { useState, useEffect } from "react";
import { Card, Button, Badge, Spinner, EmptyState } from "@barbershop/design-system";
import { Plus, Pencil, Trash2, Clock } from "lucide-react";
import { servicesAPI, type ServiceDTO } from "../lib/api";

export function ServicesPage() {
  const [services, setServices] = useState<ServiceDTO[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = async () => {
    try { setLoading(true); setError(""); const data = await servicesAPI.list(); setServices(data); }
    catch (e) { setError(e instanceof Error ? e.message : "Erro ao carregar"); }
    finally { setLoading(false); }
  };
  useEffect(() => { load(); }, []);

  const handleDelete = async (id: string) => {
    if (!confirm("Excluir este serviço?")) return;
    try { await servicesAPI.delete(id); load(); } catch (e) { setError(e instanceof Error ? e.message : "Erro"); }
  };

  if (loading) return <div className="p-8 flex justify-center"><Spinner /></div>;

  return (
    <div className="space-y-6 animate-fade-in p-6">
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <h1 className="text-2xl font-bold text-text-primary">Serviços</h1>
          <p className="text-sm text-text-secondary mt-1">{services.length} serviços — API real</p>
        </div>
      </div>
      {error && <div className="text-sm text-red-500 bg-red-50 p-3 rounded">{error}</div>}
      {services.length === 0 ? <EmptyState title="Nenhum serviço" description="Cadastre via API" /> : (
        <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
          {services.map((svc) => (
            <Card key={svc.id}>
              <div className="flex items-start justify-between mb-3">
                <h3 className="font-semibold text-text-primary">{svc.name}</h3>
                <Badge variant={svc.is_active ? "success" : "error"} dot>{svc.is_active ? "Ativo" : "Inativo"}</Badge>
              </div>
              <div className="flex items-center gap-4 text-sm text-text-secondary mb-3">
                <span className="text-lg font-bold text-primary">R$ {(svc.price_cents / 100).toFixed(2)}</span>
                <span className="flex items-center gap-1"><Clock className="h-3.5 w-3.5" />{svc.duration_minutes}min</span>
              </div>
              <div className="flex gap-2 pt-3 border-t border-border">
                <Button variant="ghost" size="sm" leftIcon={<Trash2 className="h-3.5 w-3.5" />} className="text-error" onClick={() => handleDelete(svc.id)}>Excluir</Button>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}

// Placeholder pages for remaining admin routes
export function ProfessionalsPage() {
  return (
    <div className="animate-fade-in">
      <h1 className="text-2xl font-bold text-text-primary">Profissionais</h1>
      <p className="text-sm text-text-secondary mt-1">Gerencie a equipe da barbearia.</p>
    </div>
  );
}

export function FinancialPage() {
  return (
    <div className="animate-fade-in">
      <h1 className="text-2xl font-bold text-text-primary">Financeiro</h1>
      <p className="text-sm text-text-secondary mt-1">Acompanhe receitas, despesas e comissões.</p>
    </div>
  );
}

export function ReportsPage() {
  return (
    <div className="animate-fade-in">
      <h1 className="text-2xl font-bold text-text-primary">Relatórios</h1>
      <p className="text-sm text-text-secondary mt-1">Relatórios de desempenho e faturamento.</p>
    </div>
  );
}

export function SettingsPage() {
  return (
    <div className="animate-fade-in">
      <h1 className="text-2xl font-bold text-text-primary">Configurações</h1>
      <p className="text-sm text-text-secondary mt-1">Gerencie as configurações da barbearia.</p>
    </div>
  );
}
