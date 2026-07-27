// ============================================================
// CLASSIC Theme — Services
// ============================================================

import { motion } from "framer-motion";
import { Scissors, Clock } from "lucide-react";
import type { ServicesProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function Services({ title, subtitle, items }: ServicesProps) {
  return (
    <section style={{ backgroundColor: tokens.colors.surfaceAlt, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="classic-services-title">
      <div className="max-w-[1280px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.6 }} className="mb-16 text-center">
          <span className="inline-block mb-4 text-xs tracking-[0.25em] uppercase" style={{ color: tokens.colors.secondary, fontFamily: tokens.typography.bodyFont }}>Serviços</span>
          <h2 id="classic-services-title" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text }}>{title}</h2>
          {subtitle && <p className="mt-4 max-w-lg mx-auto italic" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{subtitle}</p>}
        </motion.div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {items.map((svc, i) => (
            <motion.article key={svc.id || i} initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.5, delay: i * 0.1 }} whileHover={{ y: -4 }} className="group p-8 border text-center transition-all duration-500" style={{ borderColor: tokens.colors.borderLight, backgroundColor: tokens.colors.surface, borderRadius: tokens.borderRadius.lg, boxShadow: tokens.shadows.xs }}>
              <div className="w-14 h-14 mx-auto mb-6 flex items-center justify-center rounded-full" style={{ backgroundColor: tokens.colors.primaryLight, color: tokens.colors.primary }}><Scissors className="w-6 h-6" /></div>
              <h3 className="mb-3 text-xl" style={{ fontFamily: tokens.typography.headingFont, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text }}>{svc.name}</h3>
              <p className="mb-6 text-sm leading-relaxed" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{svc.description}</p>
              <div className="pt-4 border-t flex items-center justify-between" style={{ borderColor: tokens.colors.borderLight }}>
                <span className="text-xl font-bold" style={{ fontFamily: tokens.typography.headingFont, color: tokens.colors.primary }}>R$ {svc.price.toFixed(0)}</span>
                <span className="text-xs flex items-center gap-1" style={{ color: tokens.colors.textMuted }}><Clock className="w-3 h-3" />{svc.duration}min</span>
              </div>
            </motion.article>
          ))}
        </div>
      </div>
    </section>
  );
}
