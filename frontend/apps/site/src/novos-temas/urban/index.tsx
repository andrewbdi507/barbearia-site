// ============================================================
// URBAN Theme — Main Entry Point
// Compõe todas as seções do tema Urban.
// Uso: <UrbanTheme tenant={data} />
// ============================================================

import { memo, type FC } from "react";
import type { ThemePageProps } from "../../shared/types";
import * as Sections from "./components";

export const UrbanTheme: FC<ThemePageProps> = memo(({ tenant, slots }) => {
  const data = tenant;

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#0A0A0A] text-[#A0A0A8]">
        <p>Carregando...</p>
      </div>
    );
  }

  const HeroComp = slots?.Hero || Sections.Hero;
  const AboutComp = slots?.About || Sections.About;
  const ServicesComp = slots?.Services || Sections.Services;
  const ProfessionalsComp = slots?.Professionals || Sections.Professionals;
  const GalleryComp = slots?.Gallery || Sections.Gallery;
  const TestimonialsComp = slots?.Testimonials || Sections.Testimonials;
  const FAQComp = slots?.FAQ || Sections.FAQ;
  const BookingCTAComp = slots?.BookingCTA || Sections.BookingCTA;
  const ContactComp = slots?.Contact || Sections.Contact;
  const FooterComp = slots?.Footer || Sections.Footer;

  return (
    <main>
      <HeroComp
        title={data.name}
        subtitle={data.slogan}
        cta={{ label: "Agendar Agora", href: "/agendar" }}
        secondaryCta={{ label: "Ver Serviços", href: "/servicos" }}
        backgroundImage={data.heroImage}
        overlayOpacity={0.65}
      />

      <AboutComp
        title="Onde o Estilo Encontra a Atitude"
        description={data.description || "Somos mais que uma barbearia — somos um ponto de encontro para quem vive o estilo urbano. Nossa equipe de barbeiros é treinada nas técnicas mais avançadas, combinando tradição e inovação em cada corte."}
        image={data.aboutImage}
      />

      <ServicesComp
        title="Serviços de Elite"
        subtitle="Do clássico ao contemporâneo, cada serviço é uma experiência."
        items={data.services}
      />

      <ProfessionalsComp
        title="Os Mestres da Navalha"
        subtitle="Profissionais que respiram arte e estilo."
        team={data.professionals}
      />

      <GalleryComp
        title="Registros de Estilo"
        subtitle="Momentos capturados no templo do corte."
        images={data.gallery}
      />

      <TestimonialsComp
        title="Quem Vive, Recomenda"
        subtitle="A opinião de quem faz parte da nossa história."
        testimonials={data.testimonials}
      />

      <BookingCTAComp
        title="Seu Visual, Sua Identidade"
        subtitle="Reserve seu horário em menos de 60 segundos e venha viver a experiência."
        cta={{ label: "Agendar Agora", href: "/agendar" }}
        features={data.features || [
          { text: "Agendamento instantâneo, sem burocracia" },
          { text: "Escolha seu barbeiro favorito" },
          { text: "Confirmação via WhatsApp" },
          { text: "Remarcação gratuita até 2h antes" },
        ]}
      />

      <FAQComp
        title="Tire suas Dúvidas"
        subtitle="Tudo que você precisa saber antes de nos visitar."
        items={data.faq}
      />

      <ContactComp
        title="Venha nos Conhecer"
        subtitle="Estamos no coração da cidade, pronto para te receber."
        info={data.contact}
      />

      <FooterComp
        brandName={data.name}
        brandLogo={data.logo}
        description={data.description}
        links={[
          {
            title: "Navegação",
            items: [
              { label: "Início", href: "/" },
              { label: "Serviços", href: "/servicos" },
              { label: "Equipe", href: "/equipe" },
              { label: "Galeria", href: "/galeria" },
            ],
          },
          {
            title: "Serviços",
            items: [
              { label: "Corte Masculino", href: "/servicos" },
              { label: "Barba Completa", href: "/servicos" },
              { label: "Combo Premium", href: "/servicos" },
              { label: "Relaxamento", href: "/servicos" },
            ],
          },
          {
            title: "Links Úteis",
            items: [
              { label: "Agendar Horário", href: "/agendar" },
              { label: "Política de Privacidade", href: "/privacidade" },
              { label: "Termos de Uso", href: "/termos" },
              { label: "Trabalhe Conosco", href: "/carreiras" },
            ],
          },
        ]}
        socialLinks={data.socialLinks || [
          { platform: "instagram", url: "#", icon: "instagram" },
          { platform: "facebook", url: "#", icon: "facebook" },
          { platform: "youtube", url: "#", icon: "youtube" },
        ]}
        legalLinks={[
          { label: "Privacidade", href: "/privacidade" },
          { label: "Termos", href: "/termos" },
        ]}
      />
    </main>
  );
});

export default UrbanTheme;
