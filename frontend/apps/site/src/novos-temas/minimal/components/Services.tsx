// ============================================================
// MINIMAL Theme — Services
// ============================================================

import { motion } from "framer-motion";
import { Clock } from "lucide-react";
import type { ServicesProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function Services({ title, subtitle, items }: ServicesProps) {
  return (
    <section style={{ backgroundColor: tokens.colors.surface, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="minimal-services-title">
      <div className="max-w-[1200px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.5 }} className="mb-14">
          <span className="inline-block mb-3 text-xs font-medium tracking-wider uppercase" style={{ color: tokens.colors.textMuted, fontFamily: tokens.typography.bodyFont }}>Serviços</span>
          <h2 id="minimal-services-title" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.semibold, color: tokens.colors.text }}>{title}</h2>
          {subtitle && <p className="mt-3 max-w-lg" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{subtitle}</p>}
        </motion.div>
        <div className="divide-y" style={{ borderColor: tokens.colors.borderLight }}>
          {items.map((svc, i) => (
            <motion.div key={svc.id || i} initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} viewport={{ once: true }} transition={{ delay: i * 0.05 }} className="group flex flex-col sm:flex-row sm:items-center justify-between gap-4 py-6 transition-colors duration-300" style={{ borderColor: tokens.colors.borderLight }}>
              <div>
                <h3 className="text-lg font-semibold mb-1" style={{ fontFamily: tokens.typography.headingFont, color: tokens.colors.text }}>{svc.name}</h3>
                <p className="text-sm" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{svc.description}</p>
              </div>
              <div className="flex items-center gap-6 text-right">
                <span className="text-sm" style={{ color: tokens.colors.textMuted }}><Clock className="w-3.5 h-3.5 inline mr-1" />{svc.duration}min</span>
                <span className="text-xl font-bold" style={{ fontFamily: tokens.typography.headingFont, color: tokens.colors.text }}>R$ {svc.price.toFixed(0)}</span>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
