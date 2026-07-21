import { Card, Button } from "@barbershop/design-system";
import { Settings, Globe, Bell, Shield, Users, CreditCard } from "lucide-react";
import { Link } from "react-router-dom";

const settingSections = [
  { icon: Globe, label: "Empresa", desc: "Nome, endereço, contato", to: "/settings/company" },
  { icon: Users, label: "Usuários", desc: "Acessos e permissões", to: "/settings/users" },
  { icon: Bell, label: "Notificações", desc: "Preferências de envio", to: "/settings/notifications" },
  { icon: Shield, label: "Segurança", desc: "Senha, 2FA, logs", to: "/settings/security" },
  { icon: CreditCard, label: "Plano", desc: "Assinatura e faturamento", to: "/settings/plan" },
];

export function SettingsPage() {
  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-text-primary">Configurações</h1>
        <p className="text-sm text-text-secondary mt-1">Gerencie sua empresa e preferências.</p>
      </div>

      <div className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
        {settingSections.map((s) => (
          <Link key={s.label} to={s.to}>
            <Card className="hover:border-primary/30 transition-colors cursor-pointer h-full">
              <div className="flex items-start gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                  <s.icon className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <p className="font-medium text-text-primary">{s.label}</p>
                  <p className="text-sm text-text-secondary mt-0.5">{s.desc}</p>
                </div>
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
