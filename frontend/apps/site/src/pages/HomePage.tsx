import { Link } from "react-router-dom";
import { ArrowRight, Scissors, Star, MapPin, Clock } from "lucide-react";
import { useTheme } from "../themes/ThemeProvider";
import { Hero, Section, SectionHeading, Card, Button, LinkButton, Grid, StaggerContainer, StaggerItem } from "../components";

const services = [
  { name: "Corte", price: "R$ 45", duration: "30 min", desc: "Tesoura, máquina e finalização." },
  { name: "Barba", price: "R$ 30", duration: "20 min", desc: "Toalha quente e navalhete." },
  { name: "Corte + Barba", price: "R$ 65", duration: "45 min", desc: "Combo completo." },
];

const team = [
  { name: "Marcos", role: "Master Barber", rating: 4.9 },
  { name: "Ricardo", role: "Senior Barber", rating: 4.7 },
  { name: "Lucas", role: "Style Specialist", rating: 4.8 },
  { name: "Rafael", role: "Creative Director", rating: 4.9 },
];

export function HomePage() {
  const { theme } = useTheme();

  return (
    <div style={{ backgroundColor: theme.colors.background, color: theme.colors.text }}>
      {/* Hero */}
      <Hero
        title={`ONDE O ESTILO<br/><span style="color:${theme.colors.primary}">ENCONTRA A ARTE</span>`}
        subtitle="Agende seu horário em menos de 2 minutos. Escolha seu barbeiro, serviço e horário."
        cta="Agendar Agora"
        ctaHref="/agendar"
        secondaryCta="Ver Serviços"
        secondaryHref="/servicos"
        bgImage="https://images.unsplash.com/photo-1599351431202-1e0f0137899a?w=1600"
      />

      {/* Services */}
      <Section>
        <SectionHeading title="Excelência em cada detalhe" subtitle="Serviços" />
        <StaggerContainer>
          <Grid cols={3}>
            {services.map((svc) => (
              <StaggerItem key={svc.name}>
                <Card>
                  <div
                    className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl"
                    style={{ backgroundColor: `${theme.colors.primary}15` }}
                  >
                    <Scissors className="h-5 w-5" style={{ color: theme.colors.primary }} />
                  </div>
                  <h3 className="mb-2 text-xl font-bold" style={{ fontFamily: theme.typography.headingFont }}>
                    {svc.name}
                  </h3>
                  <p className="mb-4 text-sm" style={{ color: theme.colors.textSecondary }}>
                    {svc.desc}
                  </p>
                  <div className="flex items-center justify-between">
                    <span className="text-2xl font-bold" style={{ color: theme.colors.primary }}>
                      {svc.price}
                    </span>
                    <span className="flex items-center gap-1 text-sm" style={{ color: theme.colors.textMuted }}>
                      <Clock className="h-3.5 w-3.5" /> {svc.duration}
                    </span>
                  </div>
                </Card>
              </StaggerItem>
            ))}
          </Grid>
        </StaggerContainer>
        <div className="mt-10 text-center">
          <Link
            to="/servicos"
            className="inline-flex items-center gap-2 text-sm font-medium transition-colors"
            style={{ color: theme.colors.textMuted }}
          >
            Ver todos os serviços <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </Section>

      {/* Team */}
      <Section>
        <SectionHeading title="Mestres do ofício" subtitle="Equipe" />
        <StaggerContainer>
          <Grid cols={4}>
            {team.map((pro) => (
              <StaggerItem key={pro.name}>
                <div className="text-center">
                  <div
                    className="mx-auto mb-5 flex h-28 w-28 items-center justify-center rounded-full transition-all duration-500"
                    style={{ backgroundColor: theme.colors.surfaceHover, border: `1px solid ${theme.colors.borderLight}` }}
                  >
                    <span
                      className="text-3xl font-bold transition-colors"
                      style={{ fontFamily: theme.typography.headingFont, color: theme.colors.textMuted }}
                    >
                      {pro.name[0]}
                    </span>
                  </div>
                  <h3 className="text-lg font-bold" style={{ fontFamily: theme.typography.headingFont }}>
                    {pro.name}
                  </h3>
                  <p className="text-sm" style={{ color: theme.colors.textSecondary }}>{pro.role}</p>
                  <div className="mt-2 flex items-center justify-center gap-1">
                    <Star className="h-3.5 w-3.5 fill-current" style={{ color: theme.colors.primary }} />
                    <span className="text-sm font-medium" style={{ color: theme.colors.textSecondary }}>{pro.rating}</span>
                  </div>
                </div>
              </StaggerItem>
            ))}
          </Grid>
        </StaggerContainer>
      </Section>

      {/* Location */}
      <Section>
        <div className="text-center">
          <SectionHeading title="Onde Estamos" subtitle="Localização" />
          <div className="flex items-center justify-center gap-2" style={{ color: theme.colors.textSecondary }}>
            <MapPin className="h-5 w-5" style={{ color: theme.colors.primary }} />
            <span>Rua Augusta, 1234 — Consolação, São Paulo</span>
          </div>
          <div
            className="mt-8 mx-auto max-w-2xl h-64 rounded-2xl flex items-center justify-center"
            style={{ border: `1px solid ${theme.colors.borderLight}`, backgroundColor: theme.colors.surfaceHover, color: theme.colors.textMuted }}
          >
            Google Maps
          </div>
        </div>
      </Section>

      {/* CTA Final */}
      <Section>
        <div className="mx-auto max-w-3xl text-center">
          <Card accent>
            <h2
              className="mb-4"
              style={{ fontFamily: theme.typography.headingFont, fontSize: theme.typography.headingSize.h2, fontWeight: theme.typography.headingWeight }}
            >
              Pronto para renovar seu visual?
            </h2>
            <p className="mb-8" style={{ color: theme.colors.textSecondary }}>
              Agende agora e transforme seu estilo.
            </p>
            <LinkButton href="/agendar" variant="primary" glow>
              Agendar Agora <ArrowRight className="h-5 w-5" />
            </LinkButton>
          </Card>
        </div>
      </Section>
    </div>
  );
}
