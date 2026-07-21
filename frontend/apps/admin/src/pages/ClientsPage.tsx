import { Card, Button, Input, Badge, EmptyState } from "@barbershop/design-system";
import { Search, Plus, Users } from "lucide-react";

export function ClientsPage() {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <h1 className="text-2xl font-bold text-text-primary">Clientes</h1>
          <p className="text-sm text-text-secondary mt-1">145 clientes cadastrados</p>
        </div>
        <Button leftIcon={<Plus className="h-4 w-4" />}>Novo Cliente</Button>
      </div>

      {/* Search */}
      <div className="relative max-w-sm">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-text-secondary" />
        <Input placeholder="Buscar por nome ou telefone..." className="pl-10" />
      </div>

      {/* Client List */}
      <Card noPadding>
        <div className="divide-y divide-border">
          {[
            { name: "João Silva", phone: "(11) 99999-9999", visits: 12, lastVisit: "20/07/2026", status: "Frequente" as const },
            { name: "Pedro Lima", phone: "(11) 98888-8888", visits: 5, lastVisit: "19/07/2026", status: "Regular" as const },
            { name: "Ana Costa", phone: "(11) 97777-7777", visits: 1, lastVisit: "20/07/2026", status: "Novo" as const },
          ].map((client) => (
            <div key={client.name} className="flex items-center gap-4 p-4 hover:bg-surface-hover transition-colors cursor-pointer">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary-light text-primary font-semibold text-sm">
                {client.name.split(" ").map(n => n[0]).join("")}
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-medium text-text-primary">{client.name}</p>
                <p className="text-sm text-text-secondary">{client.phone}</p>
              </div>
              <div className="hidden sm:block text-sm text-text-secondary">{client.visits} visitas</div>
              <div className="hidden md:block text-sm text-text-secondary">{client.lastVisit}</div>
              <Badge variant={client.status === "Frequente" ? "success" : client.status === "Novo" ? "info" : "outline"}>
                {client.status}
              </Badge>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
