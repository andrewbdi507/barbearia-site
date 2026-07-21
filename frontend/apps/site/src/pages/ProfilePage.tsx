import { Card, Button } from "@barbershop/design-system";
import { User, Calendar, Clock } from "lucide-react";
import { Link } from "react-router-dom";

export function ProfilePage() {
  return (
    <div className="animate-fade-in">
      <section className="mx-auto max-w-2xl px-4 py-16">
        <div className="text-center mb-8">
          <div className="mx-auto mb-4 h-20 w-20 rounded-full bg-primary flex items-center justify-center">
            <User className="h-10 w-10 text-white" />
          </div>
          <h1 className="text-2xl font-bold">Meu Perfil</h1>
          <p className="text-muted-foreground mt-1">Gerencie seus agendamentos e dados</p>
        </div>

        <Card className="p-6 mb-6">
          <h2 className="font-semibold text-lg mb-4 flex items-center gap-2">
            <Calendar className="h-5 w-5" /> Seus Agendamentos
          </h2>
          <p className="text-muted-foreground text-sm mb-4">
            Você ainda não possui agendamentos.
          </p>
          <Link to="/agendar">
            <Button>Agendar Agora</Button>
          </Link>
        </Card>

        <Card className="p-6">
          <h2 className="font-semibold text-lg mb-4 flex items-center gap-2">
            <Clock className="h-5 w-5" /> Histórico
          </h2>
          <p className="text-muted-foreground text-sm">
            Nenhum serviço realizado ainda.
          </p>
        </Card>
      </section>
    </div>
  );
}
