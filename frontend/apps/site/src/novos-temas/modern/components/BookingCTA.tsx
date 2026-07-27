// ============================================================
// MODERN Theme — BookingCTA
// ============================================================

import { motion } from "framer-motion";
import { ArrowRight, CheckCircle2 } from "lucide-react";
import type { BookingCTAProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function BookingCTA({ title, subtitle, cta, features }: BookingCTAProps) {
  return (
    <section className="relative overflow-hidden" style={{ backgroundColor: tokens.colors.background, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-label="Agendamento">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full blur-[200px] -z-10" style={{ background: `linear-gradient(135deg, ${tokens.colors.primary}30, ${tokens.colors.secondary}20)` }} />
      <div className="max-w-[1400px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.6 }} className="text-center p-12 md:p-20 border backdrop-blur-xl" style={{ borderColor: tokens.colors.border, backgroundColor: tokens.colors.surface, borderRadius: tokens.borderRadius["2xl"] }}>
          <h2 className="mb-4" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text }}>{title}</h2>
          {subtitle && <p className="mb-10 max-w-lg mx-auto" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{subtitle}</p>}
          <a href={cta.href} className="group inline-flex items-center gap-2 px-10 py-4 text-sm font-semibold transition-all duration-300" style={{ fontFamily: tokens.typography.bodyFont, background: `linear-gradient(135deg, ${tokens.colors.primary}, ${tokens.colors.secondary})`, color: tokens.colors.textInverse, borderRadius: tokens.borderRadius.full, boxShadow: tokens.shadows.glow }}>{cta.label} <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" /></a>
          {features && features.length > 0 && <div className="mt-14 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">{features.map((f, i) => <div key={i} className="flex items-start gap-3 text-left"><CheckCircle2 className="w-5 h-5 flex-shrink-0 mt-0.5" style={{ color: tokens.colors.success }} /><span className="text-sm" style={{ color: tokens.colors.textSecondary }}>{f.text}</span></div>)}</div>}
        </motion.div>
      </div>
    </section>
  );
}
