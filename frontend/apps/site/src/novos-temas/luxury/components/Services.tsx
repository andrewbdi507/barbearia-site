// ============================================================
// LUXURY Theme — Services
// Cards refinados com bordas douradas sutis e espaçamento generoso.
// ============================================================

import { motion } from "framer-motion";
import { Clock, ArrowRight } from "lucide-react";
import type { ServicesProps, ServiceItem } from "../../shared/types";
import { tokens } from "../constants/tokens";

function ServiceCard({ service, index }: { service: ServiceItem; index: number }) {
  return (
    <motion.article
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-60px" }}
      transition={{ duration: 0.7, delay: index * 0.12, ease: tokens.motion.easing.easeOut }}
      whileHover={{ y: -4, transition: { duration: 0.4 } }}
      className="group relative p-10 text-center border transition-all duration-500"
      style={{ borderColor: tokens.colors.borderLight, backgroundColor: tokens.colors.surface, borderRadius: tokens.borderRadius.md }}
    >
      {/* Gold accent top */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-12 h-px opacity-0 group-hover:opacity-100 transition-all duration-500 group-hover:w-24" style={{ backgroundColor: tokens.colors.primary }} />

      <div className="relative z-10">
        {/* Number */}
        <div className="mb-6 text-7xl font-bold italic opacity-[0.06]" style={{ fontFamily: tokens.typography.headingFont, color: tokens.colors.primary }}>
          {(index + 1).toString().padStart(2, "0")}
        </div>

        <h3 className="mb-4 text-2xl" style={{ fontFamily: tokens.typography.headingFont, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text, letterSpacing: tokens.typography.letterSpacing.tight }}>
          {service.name}
        </h3>

        <p className="mb-8 text-sm leading-relaxed" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary, fontWeight: tokens.typography.weight.light }}>
          {service.description}
        </p>

        <div className="pt-6 border-t" style={{ borderColor: tokens.colors.borderLight }}>
          <div className="text-2xl font-bold mb-2" style={{ fontFamily: tokens.typography.headingFont, color: tokens.colors.primary }}>
            R$ {service.price.toFixed(0)}
          </div>
          <div className="flex items-center justify-center gap-1.5 text-xs" style={{ color: tokens.colors.textMuted }}>
            <Clock className="w-3 h-3" /> {service.duration} min
          </div>
        </div>
      </div>
    </motion.article>
  );
}

export function Services({ title, subtitle, items }: ServicesProps) {
  return (
    <section style={{ backgroundColor: tokens.colors.background, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="luxury-services-title">
      <div className="max-w-[1280px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.8 }} className="mb-20 text-center">
          <span className="inline-block mb-6 text-xs font-semibold tracking-[0.3em] uppercase" style={{ color: tokens.colors.primary, fontFamily: tokens.typography.bodyFont }}>Serviços</span>
          <h2 id="luxury-services-title" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text, letterSpacing: tokens.typography.letterSpacing.tight }}>{title}</h2>
          {subtitle && <p className="mt-6 max-w-lg mx-auto italic" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary, fontWeight: tokens.typography.weight.light }}>{subtitle}</p>}
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {items.map((service, i) => <ServiceCard key={service.id || i} service={service} index={i} />)}
        </div>

        {items.length > 3 && (
          <motion.div initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} viewport={{ once: true }} className="mt-16 text-center">
            <a href="/servicos" className="group inline-flex items-center gap-3 text-xs font-semibold tracking-[0.3em] uppercase transition-colors" style={{ color: tokens.colors.primary, fontFamily: tokens.typography.bodyFont }}>
              Todos os Serviços <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </a>
          </motion.div>
        )}
      </div>
    </section>
  );
}
