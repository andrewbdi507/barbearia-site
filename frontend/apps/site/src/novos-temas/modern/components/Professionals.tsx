// ============================================================
// MODERN Theme — Professionals
// ============================================================

import { motion } from "framer-motion";
import { Star } from "lucide-react";
import type { ProfessionalsProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function Professionals({ title, subtitle, team }: ProfessionalsProps) {
  return (
    <section style={{ backgroundColor: tokens.colors.surfaceAlt, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="modern-pros-title">
      <div className="max-w-[1400px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.5 }} className="mb-16 text-center">
          <span className="inline-block mb-4 text-xs font-semibold tracking-widest uppercase" style={{ color: tokens.colors.primary, fontFamily: tokens.typography.bodyFont }}>Equipe</span>
          <h2 id="modern-pros-title" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text }}>{title}</h2>
          {subtitle && <p className="mt-4 max-w-lg mx-auto" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{subtitle}</p>}
        </motion.div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
          {team.map((pro, i) => (
            <motion.article key={pro.id || i} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.4, delay: i * 0.06 }} whileHover={{ y: -4 }} className="group text-center p-6 border backdrop-blur-xl" style={{ borderColor: tokens.colors.border, backgroundColor: tokens.colors.surface, borderRadius: tokens.borderRadius.xl }}>
              <div className="mx-auto mb-5 w-36 h-36 rounded-full overflow-hidden ring-2 ring-offset-4 ring-offset-[#131318]" style={{ borderColor: tokens.colors.primary }}>
                {pro.avatar ? <img src={pro.avatar} alt={pro.name} className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" loading="lazy" /> : <div className="w-full h-full flex items-center justify-center text-3xl font-bold" style={{ backgroundColor: tokens.colors.surfaceHover, color: tokens.colors.primary }}>{pro.name[0]}</div>}
              </div>
              <h3 className="text-base font-bold mb-1" style={{ fontFamily: tokens.typography.headingFont, color: tokens.colors.text }}>{pro.name}</h3>
              <p className="text-xs mb-2" style={{ color: tokens.colors.textMuted }}>{pro.role}</p>
              <div className="flex items-center justify-center gap-0.5">{Array.from({ length: 5 }).map((_, si) => <Star key={si} className="w-3.5 h-3.5" style={{ fill: si < Math.floor(pro.rating) ? tokens.colors.primary : "none", color: si < Math.floor(pro.rating) ? tokens.colors.primary : tokens.colors.border }} />)}</div>
            </motion.article>
          ))}
        </div>
      </div>
    </section>
  );
}
