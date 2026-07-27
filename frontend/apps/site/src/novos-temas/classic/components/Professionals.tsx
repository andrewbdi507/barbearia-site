// ============================================================
// CLASSIC Theme — Professionals
// ============================================================

import { motion } from "framer-motion";
import { Star } from "lucide-react";
import type { ProfessionalsProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function Professionals({ title, subtitle, team }: ProfessionalsProps) {
  return (
    <section style={{ backgroundColor: tokens.colors.background, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="classic-pros-title">
      <div className="max-w-[1280px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.6 }} className="mb-16 text-center">
          <span className="inline-block mb-4 text-xs tracking-[0.25em] uppercase" style={{ color: tokens.colors.secondary, fontFamily: tokens.typography.bodyFont }}>Equipe</span>
          <h2 id="classic-pros-title" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text }}>{title}</h2>
          {subtitle && <p className="mt-4 max-w-lg mx-auto italic" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{subtitle}</p>}
        </motion.div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-10">
          {team.map((pro, i) => (
            <motion.article key={pro.id || i} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.5, delay: i * 0.1 }} className="text-center group">
              <div className="mx-auto mb-5 w-40 h-40 rounded-full overflow-hidden border-2" style={{ borderColor: tokens.colors.borderLight }}>
                {pro.avatar ? <img src={pro.avatar} alt={pro.name} className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" loading="lazy" /> : <div className="w-full h-full flex items-center justify-center text-4xl font-bold" style={{ backgroundColor: tokens.colors.surfaceAlt, color: tokens.colors.primary, fontFamily: tokens.typography.headingFont }}>{pro.name[0]}</div>}
              </div>
              <h3 className="text-lg font-bold mb-1" style={{ fontFamily: tokens.typography.headingFont, color: tokens.colors.text }}>{pro.name}</h3>
              <p className="text-xs tracking-wider uppercase mb-2" style={{ color: tokens.colors.textMuted }}>{pro.role}</p>
              <div className="flex items-center justify-center gap-0.5">{Array.from({ length: 5 }).map((_, si) => <Star key={si} className="w-3.5 h-3.5" style={{ fill: si < Math.floor(pro.rating) ? tokens.colors.secondary : "none", color: si < Math.floor(pro.rating) ? tokens.colors.secondary : tokens.colors.border }} />)}</div>
            </motion.article>
          ))}
        </div>
      </div>
    </section>
  );
}
