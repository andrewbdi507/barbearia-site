// ============================================================
// CUSTOM Theme — Services
// ============================================================

import { motion } from "framer-motion";
import { Scissors, Clock } from "lucide-react";
import type { ServicesProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function Services({ title, subtitle, items }: ServicesProps) {
  return (
    <section style={{ backgroundColor: tokens.colors.background, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="custom-services-title">
      <div className="max-w-[1200px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.4 }} className="mb-14 text-center">
          <h2 id="custom-services-title" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text }}>{title}</h2>
          {subtitle && <p className="mt-3 max-w-lg mx-auto" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{subtitle}</p>}
        </motion.div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {items.map((svc, i) => (
            <motion.article key={svc.id || i} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.3, delay: i * 0.05 }} whileHover={{ y: -3 }} className="p-7 border transition-all duration-300" style={{ borderColor: tokens.colors.borderLight, backgroundColor: tokens.colors.surface, borderRadius: tokens.borderRadius.lg, boxShadow: tokens.shadows.xs }}>
              <div className="w-11 h-11 mb-4 flex items-center justify-center rounded-lg" style={{ backgroundColor: tokens.colors.primaryLight }}><Scissors className="w-5 h-5" style={{ color: tokens.colors.primary }} /></div>
              <h3 className="mb-2 text-lg font-bold" style={{ fontFamily: tokens.typography.headingFont, color: tokens.colors.text }}>{svc.name}</h3>
              <p className="mb-5 text-sm" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{svc.description}</p>
              <div className="flex items-center justify-between pt-4 border-t" style={{ borderColor: tokens.colors.borderLight }}>
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
