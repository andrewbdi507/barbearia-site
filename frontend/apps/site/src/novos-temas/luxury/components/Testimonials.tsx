// ============================================================
// LUXURY Theme — Testimonials
// ============================================================

import { motion } from "framer-motion";
import { Star, Quote } from "lucide-react";
import type { TestimonialsProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function Testimonials({ title, subtitle, testimonials }: TestimonialsProps) {
  return (
    <section style={{ backgroundColor: tokens.colors.surface, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="luxury-testimonials-title">
      <div className="max-w-[1280px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.8 }} className="mb-20 text-center">
          <span className="inline-block mb-6 text-xs font-semibold tracking-[0.3em] uppercase" style={{ color: tokens.colors.primary, fontFamily: tokens.typography.bodyFont }}>Depoimentos</span>
          <h2 id="luxury-testimonials-title" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text }}>{title}</h2>
          {subtitle && <p className="mt-6 max-w-lg mx-auto italic" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary, fontWeight: tokens.typography.weight.light }}>{subtitle}</p>}
        </motion.div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {testimonials.map((t, i) => (
            <motion.article key={t.id || i} initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.6, delay: i * 0.1 }} className="relative p-10 border" style={{ borderColor: tokens.colors.borderLight, backgroundColor: tokens.colors.surface, borderRadius: tokens.borderRadius.md }}>
              <Quote className="absolute top-8 right-8 w-8 h-8 opacity-[0.06]" style={{ color: tokens.colors.primary }} />
              <div className="flex items-center gap-1.5 mb-6">
                {Array.from({ length: 5 }).map((_, si) => <Star key={si} className="w-3.5 h-3.5" style={{ fill: si < t.rating ? tokens.colors.primary : "none", color: si < t.rating ? tokens.colors.primary : tokens.colors.textMuted }} />)}
              </div>
              <blockquote className="mb-8 text-base leading-relaxed italic" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary, fontWeight: tokens.typography.weight.light }}>&ldquo;{t.text}&rdquo;</blockquote>
              <div className="flex items-center gap-4 pt-6 border-t" style={{ borderColor: tokens.colors.borderLight }}>
                <div className="w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold overflow-hidden" style={{ backgroundColor: tokens.colors.primaryLight, color: tokens.colors.primary, fontFamily: tokens.typography.headingFont }}>{t.avatar ? <img src={t.avatar} alt={t.name} className="w-full h-full rounded-full object-cover" /> : t.name[0]}</div>
                <div>
                  <div className="text-sm font-semibold" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.text }}>{t.name}</div>
                  {t.service && <div className="text-xs tracking-wider uppercase" style={{ color: tokens.colors.textMuted }}>{t.service}</div>}
                </div>
              </div>
            </motion.article>
          ))}
        </div>
      </div>
    </section>
  );
}
