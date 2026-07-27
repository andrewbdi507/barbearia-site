// ============================================================
// CLASSIC Theme — Main Entry Point
// ============================================================

import { memo, type FC } from "react";
import type { ThemePageProps } from "../../shared/types";
import * as S from "./components";

export const ClassicTheme: FC<ThemePageProps> = memo(({ tenant, slots }) => {
  const d = tenant;
  if (!d) return <div className="min-h-screen flex items-center justify-center bg-[#FBF7F0] text-[#9B8A7E]"><p>Carregando...</p></div>;
  const mk = (k: keyof NonNullable<typeof slots>) => slots?.[k];
  const H = mk("Hero") || S.Hero, A = mk("About") || S.About, Sv = mk("Services") || S.Services, P = mk("Professionals") || S.Professionals, G = mk("Gallery") || S.Gallery, T = mk("Testimonials") || S.Testimonials, FQ = mk("FAQ") || S.FAQ, B = mk("BookingCTA") || S.BookingCTA, C = mk("Contact") || S.Contact, FT = mk("Footer") || S.Footer;
  return (
    <main>
      <H title={d.name} subtitle={d.slogan} cta={{ label: "Agendar Horário", href: "/agendar" }} secondaryCta={{ label: "Conheça a Casa", href: "/servicos" }} backgroundImage={d.heroImage} overlayOpacity={0.4} />
      <A title="Tradição que se Renova" description={d.description || "Desde 1985, mantemos viva a arte da barbearia clássica. Navalha, toalha quente e o cuidado artesanal que só uma barbearia de verdade oferece."} image={d.aboutImage} highlights={[{ label: "Anos", value: "38+" }, { label: "Tradição", value: "Premium" }, { label: "Clientes", value: "15k+" }]} />
      <Sv title="Nossos Ofícios" subtitle="Serviços executados com maestria artesanal." items={d.services} />
      <P title="Mestres Barbeiros" subtitle="Profissionais que honram a tradição." team={d.professionals} />
      <G title="Nossa Casa" subtitle="Um ambiente que respira história e estilo." images={d.gallery} />
      <T title="Palavra de Cliente" subtitle="Quem conhece, confia e recomenda." testimonials={d.testimonials} />
      <B title="Seu Horário Reservado" subtitle="Agende com a praticidade de hoje e o cuidado de sempre." cta={{ label: "Reservar Agora", href: "/agendar" }} features={d.features || [{ text: "Toalha quente em todo atendimento" }, { text: "Navalhete esterilizado" }, { text: "Ambiente climatizado" }, { text: "Bebida cortesia" }]} />
      <FQ title="Dúvidas Frequentes" subtitle="Tudo que você precisa saber." items={d.faq} />
      <C title="Venha nos Visitar" subtitle="Estamos de portas abertas para recebê-lo." info={d.contact} />
      <FT brandName={d.name} brandLogo={d.logo} description={d.description} links={[{ title: "Menu", items: [{ label: "Início", href: "/" }, { label: "Serviços", href: "/servicos" }, { label: "Equipe", href: "/equipe" }, { label: "Galeria", href: "/galeria" }] }, { title: "Info", items: [{ label: "Agendar", href: "/agendar" }, { label: "Privacidade", href: "/privacidade" }, { label: "Termos", href: "/termos" }] }]} socialLinks={d.socialLinks} legalLinks={[{ label: "Privacidade", href: "/privacidade" }, { label: "Termos", href: "/termos" }]} />
    </main>
  );
});
export default ClassicTheme;
