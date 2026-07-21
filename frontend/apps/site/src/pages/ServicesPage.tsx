import { Card } from "@barbershop/design-system";

export function ServicesPage() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-12 animate-fade-in">
      <h1 className="text-2xl font-bold mb-2">Serviços</h1>
      <p className="text-text-secondary mb-8">Conheça nossos serviços e preços.</p>
      <div className="grid gap-4">
        {[
          { name: "Corte", price: "R$ 45,00", duration: "30 min", desc: "Tesoura, máquina e finalização com pomada." },
          { name: "Barba", price: "R$ 30,00", duration: "20 min", desc: "Toalha quente, balm e navalhete." },
          { name: "Corte + Barba", price: "R$ 65,00", duration: "45 min", desc: "Combo completo para renovar o visual." },
          { name: "Hidratação", price: "R$ 40,00", duration: "25 min", desc: "Tratamento capilar revitalizante." },
        ].map((svc) => (
          <Card key={svc.name} className="flex items-center justify-between flex-wrap gap-3">
            <div>
              <h3 className="font-semibold">{svc.name}</h3>
              <p className="text-sm text-text-secondary">{svc.desc}</p>
              <p className="text-sm text-text-secondary mt-1">⏱ {svc.duration}</p>
            </div>
            <span className="text-xl font-bold text-primary">{svc.price}</span>
          </Card>
        ))}
      </div>
    </div>
  );
}

export function TeamPage() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-12 animate-fade-in">
      <h1 className="text-2xl font-bold mb-2">Equipe</h1>
      <p className="text-text-secondary mb-8">Conheça os profissionais que vão cuidar de você.</p>
      <div className="grid gap-4 grid-cols-1 sm:grid-cols-2">
        {["Marcos", "Ricardo", "Lucas", "Rafael"].map((name) => (
          <Card key={name}>
            <div className="flex items-center gap-4">
              <div className="h-16 w-16 rounded-full bg-primary-light flex items-center justify-center text-primary font-bold text-xl">
                {name[0]}
              </div>
              <div>
                <h3 className="font-semibold">{name}</h3>
                <p className="text-sm text-text-secondary">Barbeiro</p>
                <p className="text-sm text-text-secondary">⭐ 4.8 (120 avaliações)</p>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

export function GalleryPage() {
  return (
    <div className="mx-auto max-w-6xl px-4 py-12 animate-fade-in">
      <h1 className="text-2xl font-bold mb-2">Galeria</h1>
      <p className="text-text-secondary mb-8">Nossos melhores trabalhos.</p>
      <div className="grid gap-4 grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
        {Array.from({ length: 8 }).map((_, i) => (
          <div key={i} className="aspect-square rounded-lg bg-surface-hover border border-border flex items-center justify-center text-text-disabled">
            📸 Foto {i + 1}
          </div>
        ))}
      </div>
    </div>
  );
}

export function ProfilePage() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-12 animate-fade-in">
      <h1 className="text-2xl font-bold mb-2">Meu Perfil</h1>
      <p className="text-text-secondary">Gerencie seus dados e veja seu histórico.</p>
    </div>
  );
}
