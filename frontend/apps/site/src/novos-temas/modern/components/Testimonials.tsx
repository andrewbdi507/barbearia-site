// ============================================================
// MODERN Theme — Testimonials
// ============================================================

import { motion } from "framer-motion";
import { Star, Quote } from "lucide-react";
import type { TestimonialsProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function Testimonials({ title, subtitle, testimonials }: TestimonialsProps) {
  return (
    <section style={{ backgroundColor: tokens.colors.surfaceAlt, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="modern-testimonials-title">
      <div className="max-w-[1400px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.5 }} className="mb-16 text-center">
          <span className="inline-block mb-4 text-xs font-semibold tracking-widest uppercase" style={{ color: tokens.colors.primary, fontFamily: tokens.typography.bodyFont }}>Depoimentos</span>
          <h2 id="modern-testimonials-title" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text }}>{title}</h2>
          {subtitle && <p className="mt-4 max-w-lg mx-auto" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{subtitle}</p>}
        </motion.div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {testimonials.map((t, i) => (
            <motion.article key={t.id || i} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.4, delay: i * 0.06 }} className="p-8 border backdrop-blur-xl" style={{ borderColor: tokens.colors.border, backgroundColor: tokens.colors.surface, borderRadius: tokens.borderRadius.xl }}>
              <Quote className="w-8 h-8 mb-4" style={{ color: tokens.colors.primary, opacity: 0.3 }} />
              <div className="flex items-center gap-1 mb-4">{Array.from({ length: 5 }).map((_, si) => <Star key={si} className="w-3.5 h-3.5" style={{ fill: si < t.rating ? tokens.colors.primary : "none", color: si < t.rating ? tokens.colors.primary : tokens.colors.border }} />)}</div>
              <blockquote className="mb-6 text-sm leading-relaxed" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>&ldquo;{t.text}&rdquo;</blockquote>
              <div className="flex items-center gap-3 pt-4 border-t" style={{ borderColor: tokens.colors.border }}><div className="w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold overflow-hidden" style={{ backgroundColor: tokens.colors.primaryLight, color: tokens.colors.primary }}>{t.avatar ? <img src={t.avatar} alt={t.name} className="w-full h-full object-cover" /> : t.name[0]}</div><div><div className="text-sm font-medium" style={{ color: tokens.colors.text }}>{t.name}</div>{t.service && <div className="text-xs" style={{ color: tokens.colors.textMuted }}>{t.service}</div>}</div></div>
            </motion.article>
          ))}
        </div>
      </div>
    </section>
  );
}
