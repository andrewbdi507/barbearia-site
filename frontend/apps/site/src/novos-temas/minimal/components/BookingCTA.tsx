// ============================================================
// MINIMAL Theme — BookingCTA
// ============================================================

import { motion } from "framer-motion";
import { ArrowRight, CheckCircle2 } from "lucide-react";
import type { BookingCTAProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function BookingCTA({ title, subtitle, cta, features }: BookingCTAProps) {
  return (
    <section style={{ backgroundColor: tokens.colors.background, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-label="Agendamento">
      <div className="max-w-[1200px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.5 }} className="p-10 md:p-16 text-center border" style={{ borderColor: tokens.colors.borderLight, backgroundColor: tokens.colors.surface, borderRadius: tokens.borderRadius.xl }}>
          <h2 className="mb-4" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.semibold, color: tokens.colors.text }}>{title}</h2>
          {subtitle && <p className="mb-8 max-w-md mx-auto" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{subtitle}</p>}
          <a href={cta.href} className="group inline-flex items-center gap-2 px-8 py-3.5 text-sm font-semibold transition-all duration-300" style={{ fontFamily: tokens.typography.bodyFont, backgroundColor: tokens.colors.primary, color: tokens.colors.textInverse, borderRadius: tokens.borderRadius.md }}>{cta.label} <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" /></a>
          {features && features.length > 0 && (
            <div className="mt-12 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 text-left">
              {features.map((f, i) => <div key={i} className="flex items-start gap-3"><CheckCircle2 className="w-5 h-5 flex-shrink-0 mt-0.5" style={{ color: tokens.colors.success }} /><span className="text-sm" style={{ color: tokens.colors.textSecondary }}>{f.text}</span></div>)}
            </div>
          )}
        </motion.div>
      </div>
    </section>
  );
}
