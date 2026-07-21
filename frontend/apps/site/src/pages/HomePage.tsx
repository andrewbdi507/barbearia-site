import { Link } from "react-router-dom";
import { Button, Card } from "@barbershop/design-system";
import { Star, MapPin } from "lucide-react";

export function HomePage() {
  return (
    <div className="animate-fade-in">
      {/* Hero Section */}
      <section className="relative bg-primary text-white">
        <div className="mx-auto max-w-6xl px-4 py-16 md:py-28 flex flex-col items-center text-center">
          <h1 className="text-3xl md:text-5xl font-extrabold leading-tight mb-4">
            Seu estilo, <span className="text-secondary">nossa arte</span>
          </h1>
          <p className="text-lg md:text-xl text-white/80 max-w-lg mb-8">
            Agende seu horário em menos de 2 minutos. Escolha seu barbeiro, serviço e horário.
          </p>
          <Link to="/agendar">
            <Button size="xl" className="bg-secondary hover:bg-secondary-hover border-0 text-white">
              Agendar Agora
            </Button>
          </Link>
        </div>
      </section>

      {/* Services Preview */}
      <section className="mx-auto max-w-6xl px-4 py-16">
        <h2 className="text-2xl font-bold text-center mb-8">Nossos Serviços</h2>
        <div className="grid gap-4 grid-cols-1 sm:grid-cols-3">
          {[
            { name: "Corte", price: "R$ 45", duration: "30 min" },
            { name: "Barba", price: "R$ 30", duration: "20 min" },
            { name: "Corte + Barba", price: "R$ 65", duration: "45 min" },
          ].map((svc) => (
            <Card key={svc.name} className="text-center">
              <h3 className="font-semibold text-lg">{svc.name}</h3>
              <p className="text-2xl font-bold text-primary my-2">{svc.price}</p>
              <p className="text-sm text-text-secondary">⏱ {svc.duration}</p>
            </Card>
          ))}
        </div>
        <div className="text-center mt-6">
          <Link to="/servicos" className="text-sm text-primary hover:underline font-medium">Ver todos os serviços →</Link>
        </div>
      </section>

      {/* Team Preview */}
      <section className="bg-surface border-y border-border">
        <div className="mx-auto max-w-6xl px-4 py-16">
          <h2 className="text-2xl font-bold text-center mb-8">Nossa Equipe</h2>
          <div className="grid gap-6 grid-cols-2 md:grid-cols-4">
            {[
              { name: "Marcos", role: "Barbeiro", rating: 4.9 },
              { name: "Ricardo", role: "Barbeiro", rating: 4.7 },
              { name: "Lucas", role: "Barbeiro", rating: 4.8 },
              { name: "Rafael", role: "Barbeiro", rating: 4.9 },
            ].map((pro) => (
              <div key={pro.name} className="text-center">
                <div className="mx-auto h-24 w-24 rounded-full bg-primary-light flex items-center justify-center text-primary font-bold text-2xl mb-3">
                  {pro.name[0]}
                </div>
                <h3 className="font-semibold">{pro.name}</h3>
                <p className="text-sm text-text-secondary">{pro.role}</p>
                <div className="flex items-center justify-center gap-1 mt-1 text-sm text-warning">
                  <Star className="h-3.5 w-3.5 fill-current" /> {pro.rating}
                </div>
              </div>
            ))}
          </div>
          <div className="text-center mt-6">
            <Link to="/equipe" className="text-sm text-primary hover:underline font-medium">Ver toda a equipe →</Link>
          </div>
        </div>
      </section>

      {/* Location */}
      <section className="mx-auto max-w-6xl px-4 py-16">
        <h2 className="text-2xl font-bold text-center mb-4">Onde Estamos</h2>
        <p className="text-center text-text-secondary mb-6 flex items-center justify-center gap-1.5">
          <MapPin className="h-4 w-4" /> Rua Augusta, 1234 — Consolação, São Paulo
        </p>
        <div className="h-64 bg-surface-hover rounded-lg flex items-center justify-center text-text-secondary border border-border">
          🗺️ Google Maps (embed)
        </div>
      </section>
    </div>
  );
}
