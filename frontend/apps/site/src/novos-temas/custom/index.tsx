// ============================================================
// CUSTOM Theme — Main Entry Point (White-Label Base)
// ============================================================

import { memo, type FC } from "react";
import type { ThemePageProps } from "../../shared/types";
import * as S from "./components";

export const CustomTheme: FC<ThemePageProps> = memo(({ tenant, slots }) => {
  const d = tenant;
  if (!d) return <div className="min-h-screen flex items-center justify-center bg-white text-gray-400"><p>Carregando...</p></div>;
  const mk = (k: keyof NonNullable<typeof slots>) => slots?.[k];
  const H = mk("Hero") || S.Hero, A = mk("About") || S.About, Sv = mk("Services") || S.Services, P = mk("Professionals") || S.Professionals, G = mk("Gallery") || S.Gallery, T = mk("Testimonials") || S.Testimonials, FQ = mk("FAQ") || S.FAQ, B = mk("BookingCTA") || S.BookingCTA, C = mk("Contact") || S.Contact, FT = mk("Footer") || S.Footer;
  return (
    <main>
      <H title={d.name} subtitle={d.slogan} cta={{ label: "Agendar", href: "/agendar" }} secondaryCta={{ label: "Serviços", href: "/servicos" }} backgroundImage={d.heroImage} />
      <A title="Quem Somos" description={d.description || "Somos uma barbearia dedicada a oferecer o melhor em cuidados masculinos. Nossa equipe está pronta para proporcionar uma experiência única."} image={d.aboutImage} highlights={[{ label: "Clientes", value: "5k+" }, { label: "Avaliação", value: "4.8" }, { label: "Experiência", value: "10+" }]} />
      <Sv title="Nossos Serviços" subtitle="Conheça tudo que podemos fazer por você." items={d.services} />
      <P title="Nossa Equipe" subtitle="Profissionais preparados para melhor atender." team={d.professionals} />
      <G title="Galeria" subtitle="Conheça nosso espaço." images={d.gallery} />
      <T title="Depoimentos" subtitle="Veja o que nossos clientes dizem." testimonials={d.testimonials} />
      <B title="Agende seu Horário" subtitle="Reserve agora mesmo." cta={{ label: "Agendar", href: "/agendar" }} features={d.features || [{ text: "Agendamento rápido" }, { text: "Escolha seu profissional" }, { text: "Confirmação instantânea" }, { text: "Reagendamento fácil" }]} />
      <FQ title="Dúvidas Frequentes" subtitle="Respostas para as principais perguntas." items={d.faq} />
      <C title="Fale Conosco" subtitle="Entre em contato ou nos visite." info={d.contact} />
      <FT brandName={d.name} brandLogo={d.logo} description={d.description} links={[{ title: "Navegação", items: [{ label: "Início", href: "/" }, { label: "Serviços", href: "/servicos" }, { label: "Equipe", href: "/equipe" }, { label: "Galeria", href: "/galeria" }] }, { title: "Links", items: [{ label: "Agendar", href: "/agendar" }, { label: "Privacidade", href: "/privacidade" }, { label: "Termos", href: "/termos" }] }]} socialLinks={d.socialLinks} legalLinks={[{ label: "Privacidade", href: "/privacidade" }, { label: "Termos", href: "/termos" }]} />
    </main>
  );
});
export default CustomTheme;
