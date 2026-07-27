// ============================================================
// LUXURY Theme — Booking CTA
// ============================================================

import { motion } from "framer-motion";
import { ArrowRight, CheckCircle2 } from "lucide-react";
import type { BookingCTAProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function BookingCTA({ title, subtitle, cta, features }: BookingCTAProps) {
  return (
    <section className="relative overflow-hidden" style={{ backgroundColor: tokens.colors.background, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-label="Agendamento">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[700px] rounded-full blur-[200px] -z-10" style={{ backgroundColor: tokens.colors.primary, opacity: 0.05 }} />
      <div className="max-w-[1280px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 40 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.9, ease: tokens.motion.easing.easeOut }} className="relative border p-12 md:p-20 text-center" style={{ borderColor: tokens.colors.border, backgroundColor: tokens.colors.surface, borderRadius: tokens.borderRadius.lg }}>
          <div className="absolute top-0 left-0 right-0 h-px" style={{ background: `linear-gradient(90deg, transparent, ${tokens.colors.primary}80, transparent)` }} />
          <div className="absolute bottom-0 left-0 right-0 h-px" style={{ background: `linear-gradient(90deg, transparent, ${tokens.colors.primary}80, transparent)` }} />
          <span className="inline-block mb-6 text-xs font-semibold tracking-[0.3em] uppercase" style={{ color: tokens.colors.primary, fontFamily: tokens.typography.bodyFont }}>Reserve sua Experiência</span>
          <h2 className="mb-6" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text, lineHeight: tokens.typography.lineHeight.tight }}>{title}</h2>
          {subtitle && <p className="mb-10 max-w-lg mx-auto italic" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary, fontWeight: tokens.typography.weight.light }}>{subtitle}</p>}
          <a href={cta.href} className="group inline-flex items-center gap-3 px-12 py-4 text-base font-semibold tracking-[0.2em] uppercase transition-all duration-500" style={{ fontFamily: tokens.typography.bodyFont, backgroundColor: tokens.colors.primary, color: tokens.colors.textInverse, boxShadow: tokens.shadows.glow }}>
            {cta.label} <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </a>
          {features && features.length > 0 && (
            <div className="mt-14 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {features.map((f, i) => (
                <motion.div key={i} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0.4 + i * 0.1 }} className="flex items-start gap-3 text-left">
                  <CheckCircle2 className="w-5 h-5 flex-shrink-0 mt-0.5" style={{ color: tokens.colors.primary }} />
                  <span className="text-sm" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary, fontWeight: tokens.typography.weight.light }}>{f.text}</span>
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>
      </div>
    </section>
  );
}
