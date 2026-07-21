import { Card } from "@barbershop/design-system";

export function ProfessionalsPage() {
  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-text-primary">Equipe</h1>
        <p className="text-sm text-text-secondary mt-1">Gerencie seus profissionais, horários e especialidades.</p>
      </div>

      <div className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
        {["Marcos Silva", "Ricardo Santos", "Lucas Oliveira"].map((name) => (
          <Card key={name}>
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10 text-primary font-semibold">
                {name.split(" ").map(n => n[0]).join("")}
              </div>
              <div>
                <p className="font-medium text-text-primary">{name}</p>
                <p className="text-sm text-text-secondary">Barbeiro</p>
              </div>
            </div>
            <div className="mt-3 flex gap-2">
              <span className="rounded-full bg-surface-hover px-2 py-0.5 text-xs text-text-secondary">Barba</span>
              <span className="rounded-full bg-surface-hover px-2 py-0.5 text-xs text-text-secondary">Corte</span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
