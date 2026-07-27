// ============================================================
// LUXURY Theme — Main Entry Point
// Uso: <LuxuryTheme tenant={data} />
// ============================================================

import { memo, type FC } from "react";
import type { ThemePageProps } from "../../shared/types";
import * as Sections from "./components";

export const LuxuryTheme: FC<ThemePageProps> = memo(({ tenant, slots }) => {
  const data = tenant;
  if (!data) return <div className="min-h-screen flex items-center justify-center bg-[#080808] text-[#B8B4A8]"><p>Carregando...</p></div>;

  const H = slots?.Hero || Sections.Hero;
  const A = slots?.About || Sections.About;
  const S = slots?.Services || Sections.Services;
  const P = slots?.Professionals || Sections.Professionals;
  const G = slots?.Gallery || Sections.Gallery;
  const T = slots?.Testimonials || Sections.Testimonials;
  const FQ = slots?.FAQ || Sections.FAQ;
  const B = slots?.BookingCTA || Sections.BookingCTA;
  const C = slots?.Contact || Sections.Contact;
  const FT = slots?.Footer || Sections.Footer;

  return (
    <main>
      <H title={data.name} subtitle={data.slogan} cta={{ label: "Agendar Visita", href: "/agendar" }} secondaryCta={{ label: "Nossos Serviços", href: "/servicos" }} backgroundImage={data.heroImage} overlayOpacity={0.7} />
      <A title="Excelência e Sofisticação" description={data.description || "Cada detalhe foi pensado para oferecer uma experiência única. Do ambiente climatizado ao atendimento personalizado, nossa barbearia redefine o conceito de cuidado masculino."} image={data.aboutImage} />
      <S title="Serviços Exclusivos" subtitle="Experiências pensadas para o homem que valoriza o requinte." items={data.services} />
      <P title="Mestres Barbeiros" subtitle="Profissionais selecionados entre os melhores do país." team={data.professionals} />
      <G title="Registro da Excelência" subtitle="Momentos de sofisticação capturados em nosso espaço." images={data.gallery} />
      <T title="A Opinião de Nossos Clientes" subtitle="Depoimentos de quem experimenta o padrão premium." testimonials={data.testimonials} />
      <B title="Sua Experiência Começa Aqui" subtitle="Reserve seu horário e descubra o significado de atendimento de excelência." cta={{ label: "Agendar Agora", href: "/agendar" }} features={data.features || [{ text: "Atendimento personalizado e exclusivo" }, { text: "Ambiente climatizado e confortável" }, { text: "Bebidas premium cortesia" }, { text: "Estacionamento privativo" }]} />
      <FQ title="Dúvidas Frequentes" subtitle="Informações para sua total tranquilidade." items={data.faq} />
      <C title="Visite-nos" subtitle="Estamos localizados na região mais nobre da cidade." info={data.contact} />
      <FT brandName={data.name} brandLogo={data.logo} description={data.description} links={[{ title: "Navegação", items: [{ label: "Início", href: "/" }, { label: "Serviços", href: "/servicos" }, { label: "Equipe", href: "/equipe" }, { label: "Galeria", href: "/galeria" }] }, { title: "Serviços", items: [{ label: "Corte Premium", href: "/servicos" }, { label: "Barba Clássica", href: "/servicos" }, { label: "Experiência VIP", href: "/servicos" }] }, { title: "Links", items: [{ label: "Agendar", href: "/agendar" }, { label: "Privacidade", href: "/privacidade" }, { label: "Termos", href: "/termos" }] }]} socialLinks={data.socialLinks || [{ platform: "instagram", url: "#" }, { platform: "facebook", url: "#" }]} legalLinks={[{ label: "Privacidade", href: "/privacidade" }, { label: "Termos", href: "/termos" }]} />
    </main>
  );
});

export default LuxuryTheme;
