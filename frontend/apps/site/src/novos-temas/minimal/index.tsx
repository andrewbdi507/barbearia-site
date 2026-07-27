// ============================================================
// MINIMAL Theme — Main Entry Point
// ============================================================

import { memo, type FC } from "react";
import type { ThemePageProps } from "../../shared/types";
import * as S from "./components";

export const MinimalTheme: FC<ThemePageProps> = memo(({ tenant, slots }) => {
  const d = tenant;
  if (!d) return <div className="min-h-screen flex items-center justify-center bg-[#FAFAFA] text-[#AAAAAA]"><p>Carregando...</p></div>;
  const H = slots?.Hero || S.Hero, A = slots?.About || S.About, Sv = slots?.Services || S.Services, P = slots?.Professionals || S.Professionals, G = slots?.Gallery || S.Gallery, T = slots?.Testimonials || S.Testimonials, FQ = slots?.FAQ || S.FAQ, B = slots?.BookingCTA || S.BookingCTA, C = slots?.Contact || S.Contact, FT = slots?.Footer || S.Footer;
  return (
    <main>
      <H title={d.name} subtitle={d.slogan} cta={{ label: "Agendar", href: "/agendar" }} secondaryCta={{ label: "Serviços", href: "/servicos" }} backgroundImage={d.heroImage} overlayOpacity={0.35} />
      <A title="Simplicidade que transforma" description={d.description || "Acreditamos que menos é mais. Nossa barbearia oferece o essencial com excelência: cortes precisos, ambiente clean e atendimento sem frescura."} image={d.aboutImage} highlights={[{ label: "Clientes", value: "5k+" }, { label: "Avaliação", value: "4.9" }, { label: "Anos", value: "8+" }]} />
      <Sv title="O Essencial" subtitle="Serviços diretos, sem complicação." items={d.services} />
      <P title="Nossa Equipe" subtitle="Profissionais que dominam o ofício." team={d.professionals} />
      <G title="Nosso Espaço" subtitle="Ambiente clean e acolhedor." images={d.gallery} />
      <T title="O Que Dizem" subtitle="Feedbacks reais de clientes reais." testimonials={d.testimonials} />
      <B title="Agende Seu Horário" subtitle="Rápido, simples e sem burocracia." cta={{ label: "Agendar Agora", href: "/agendar" }} features={d.features || [{ text: "Agendamento em 30 segundos" }, { text: "Escolha seu barbeiro" }, { text: "Lembretes por WhatsApp" }, { text: "Cancelamento gratuito" }]} />
      <FQ title="Perguntas Frequentes" subtitle="Respostas diretas para suas dúvidas." items={d.faq} />
      <C title="Onde Estamos" subtitle="Venha nos visitar." info={d.contact} />
      <FT brandName={d.name} brandLogo={d.logo} description={d.description} links={[{ title: "Menu", items: [{ label: "Início", href: "/" }, { label: "Serviços", href: "/servicos" }, { label: "Equipe", href: "/equipe" }, { label: "Galeria", href: "/galeria" }] }, { title: "Info", items: [{ label: "Agendar", href: "/agendar" }, { label: "Privacidade", href: "/privacidade" }, { label: "Termos", href: "/termos" }] }]} socialLinks={d.socialLinks} legalLinks={[{ label: "Privacidade", href: "/privacidade" }, { label: "Termos", href: "/termos" }]} />
    </main>
  );
});
export default MinimalTheme;
