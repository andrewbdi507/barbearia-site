import { Card } from "@barbershop/design-system";
import { Users } from "lucide-react";

export function TeamPage() {
  return (
    <div className="animate-fade-in">
      <section className="mx-auto max-w-6xl px-4 py-16">
        <div className="text-center mb-12">
          <Users className="mx-auto mb-4 h-12 w-12 text-primary" />
          <h1 className="text-3xl md:text-4xl font-bold mb-4">Nossa Equipe</h1>
          <p className="text-lg text-muted-foreground max-w-lg mx-auto">
            Conheça os profissionais que fazem a diferença no seu visual.
          </p>
        </div>

        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <Card key={i} variant="interactive" className="text-center p-6">
              <div className="mx-auto mb-4 h-24 w-24 rounded-full bg-muted flex items-center justify-center">
                <Users className="h-10 w-10 text-muted-foreground" />
              </div>
              <h3 className="font-semibold text-lg">Barbeiro {i}</h3>
              <p className="text-sm text-muted-foreground mt-1">Especialista em cortes modernos</p>
            </Card>
          ))}
        </div>
      </section>
    </div>
  );
}
