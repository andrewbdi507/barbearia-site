// ============================================================
// CUSTOM Theme — Professionals
// ============================================================

import { motion } from "framer-motion";
import { Star } from "lucide-react";
import type { ProfessionalsProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function Professionals({ title, subtitle, team }: ProfessionalsProps) {
  return (
    <section style={{ backgroundColor: tokens.colors.surface, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="custom-pros-title">
      <div className="max-w-[1200px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.4 }} className="mb-14 text-center">
          <h2 id="custom-pros-title" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text }}>{title}</h2>
          {subtitle && <p className="mt-3 max-w-lg mx-auto" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{subtitle}</p>}
        </motion.div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
          {team.map((pro, i) => (
            <motion.article key={pro.id || i} initial={{ opacity: 0, y: 15 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.3, delay: i * 0.05 }} className="text-center">
              <div className="mx-auto mb-4 w-32 h-32 rounded-full overflow-hidden" style={{ backgroundColor: tokens.colors.surfaceAlt }}>
                {pro.avatar ? <img src={pro.avatar} alt={pro.name} className="w-full h-full object-cover" loading="lazy" /> : <div className="w-full h-full flex items-center justify-center text-2xl font-bold" style={{ color: tokens.colors.textMuted }}>{pro.name[0]}</div>}
              </div>
              <h3 className="text-base font-bold mb-1" style={{ fontFamily: tokens.typography.headingFont, color: tokens.colors.text }}>{pro.name}</h3>
              <p className="text-xs mb-2" style={{ color: tokens.colors.textMuted }}>{pro.role}</p>
              <div className="flex items-center justify-center gap-0.5">{Array.from({ length: 5 }).map((_, si) => <Star key={si} className="w-3 h-3" style={{ fill: si < Math.floor(pro.rating) ? tokens.colors.primary : "none", color: si < Math.floor(pro.rating) ? tokens.colors.primary : tokens.colors.border }} />)}</div>
            </motion.article>
          ))}
        </div>
      </div>
    </section>
  );
}
