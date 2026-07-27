// ============================================================
// MODERN Theme — Services
// ============================================================

import { motion } from "framer-motion";
import { Scissors, Clock } from "lucide-react";
import type { ServicesProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function Services({ title, subtitle, items }: ServicesProps) {
  return (
    <section style={{ backgroundColor: tokens.colors.background, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="modern-services-title">
      <div className="max-w-[1400px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.5 }} className="mb-16 text-center">
          <span className="inline-block mb-4 text-xs font-semibold tracking-widest uppercase" style={{ color: tokens.colors.primary, fontFamily: tokens.typography.bodyFont }}>Serviços</span>
          <h2 id="modern-services-title" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text }}>{title}</h2>
          {subtitle && <p className="mt-4 max-w-lg mx-auto" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{subtitle}</p>}
        </motion.div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {items.map((svc, i) => (
            <motion.article key={svc.id || i} initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.4, delay: i * 0.06 }} whileHover={{ y: -4 }} className="group p-8 border backdrop-blur-xl transition-all duration-300" style={{ borderColor: tokens.colors.border, backgroundColor: tokens.colors.surface, borderRadius: tokens.borderRadius.xl }}>
              <div className="w-12 h-12 mb-5 flex items-center justify-center rounded-2xl" style={{ background: `linear-gradient(135deg, ${tokens.colors.primaryLight}, ${tokens.colors.primaryLight})` }}><Scissors className="w-5 h-5" style={{ color: tokens.colors.primary }} /></div>
              <h3 className="mb-3 text-lg font-bold" style={{ fontFamily: tokens.typography.headingFont, color: tokens.colors.text }}>{svc.name}</h3>
              <p className="mb-6 text-sm leading-relaxed" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{svc.description}</p>
              <div className="flex items-center justify-between pt-4 border-t" style={{ borderColor: tokens.colors.border }}>
                <span className="text-2xl font-bold" style={{ fontFamily: tokens.typography.headingFont, background: `linear-gradient(135deg, ${tokens.colors.primary}, ${tokens.colors.secondary})`, WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>R$ {svc.price.toFixed(0)}</span>
                <span className="flex items-center gap-1 text-xs" style={{ color: tokens.colors.textMuted }}><Clock className="w-3 h-3" />{svc.duration}min</span>
              </div>
            </motion.article>
          ))}
        </div>
      </div>
    </section>
  );
}
