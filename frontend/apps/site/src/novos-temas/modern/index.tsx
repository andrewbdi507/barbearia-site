// ============================================================
// MODERN Theme — Main Entry Point
// ============================================================

import { memo, type FC } from "react";
import type { ThemePageProps } from "../../shared/types";
import * as S from "./components";

export const ModernTheme: FC<ThemePageProps> = memo(({ tenant, slots }) => {
  const d = tenant;
  if (!d) return <div className="min-h-screen flex items-center justify-center bg-[#0A0A0F] text-[#555568]"><p>Carregando...</p></div>;
  const mk = (k: keyof NonNullable<typeof slots>) => slots?.[k];
  const H = mk("Hero") || S.Hero, A = mk("About") || S.About, Sv = mk("Services") || S.Services, P = mk("Professionals") || S.Professionals, G = mk("Gallery") || S.Gallery, T = mk("Testimonials") || S.Testimonials, FQ = mk("FAQ") || S.FAQ, B = mk("BookingCTA") || S.BookingCTA, C = mk("Contact") || S.Contact, FT = mk("Footer") || S.Footer;
  return (
    <main>
      <H title={d.name} subtitle={d.slogan} cta={{ label: "Agendar Agora", href: "/agendar" }} secondaryCta={{ label: "Explorar Serviços", href: "/servicos" }} backgroundImage={d.heroImage} overlayOpacity={0.5} />
      <A title="Tecnologia e Estilo" description={d.description || "Unimos o melhor da tecnologia com a arte da barbearia. Agendamento inteligente, profissionais qualificados e uma experiência fluida do início ao fim."} image={d.aboutImage} highlights={[{ label: "Clientes", value: "12k+" }, { label: "Avaliação", value: "4.9" }, { label: "NPS", value: "94" }]} />
      <Sv title="Serviços Inteligentes" subtitle="Escolha, agende e aproveite — sem complicação." items={d.services} />
      <P title="Nossa Equipe Tech" subtitle="Barbeiros que dominam técnica e tecnologia." team={d.professionals} />
      <G title="Momentos Capturados" subtitle="Registros do nosso espaço e dos nossos trabalhos." images={d.gallery} />
      <T title="Feedback 5 Estrelas" subtitle="O que nossos clientes dizem sobre a experiência." testimonials={d.testimonials} />
      <B title="Pronto para uma Nova Experiência?" subtitle="Agende em segundos e descubra o futuro da barbearia." cta={{ label: "Agendar Agora", href: "/agendar" }} features={d.features || [{ text: "Agendamento em 30s" }, { text: "IA para recomendação" }, { text: "Lembretes automáticos" }, { text: "Histórico de serviços" }]} />
      <FQ title="Dúvidas Rápidas" subtitle="Respostas diretas para você." items={d.faq} />
      <C title="Nosso Endereço" subtitle="Visite nosso espaço tech." info={d.contact} />
      <FT brandName={d.name} brandLogo={d.logo} description={d.description} links={[{ title: "Navegação", items: [{ label: "Início", href: "/" }, { label: "Serviços", href: "/servicos" }, { label: "Equipe", href: "/equipe" }, { label: "Galeria", href: "/galeria" }] }, { title: "Links", items: [{ label: "Agendar", href: "/agendar" }, { label: "Privacidade", href: "/privacidade" }, { label: "Termos", href: "/termos" }] }]} socialLinks={d.socialLinks} legalLinks={[{ label: "Privacidade", href: "/privacidade" }, { label: "Termos", href: "/termos" }]} />
    </main>
  );
});
export default ModernTheme;
