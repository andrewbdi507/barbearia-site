// ============================================================
// URBAN Theme — Booking CTA Section
// CTA impactante com split layout: texto + lista de features.
// ============================================================

import { motion } from "framer-motion";
import { ArrowRight, CheckCircle2 } from "lucide-react";
import type { BookingCTAProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function BookingCTA({ title, subtitle, cta, features }: BookingCTAProps) {
  return (
    <section
      className="relative overflow-hidden"
      style={{ backgroundColor: tokens.colors.background, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }}
      aria-label="Agendamento"
    >
      {/* Background glow */}
      <div
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full blur-[180px] -z-10"
        style={{ backgroundColor: tokens.colors.primary, opacity: 0.08 }}
      />

      <div className="max-w-[1400px] mx-auto px-6 md:px-12">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.7, ease: tokens.motion.easing.easeOut }}
          className="relative border overflow-hidden"
          style={{
            borderColor: tokens.colors.border,
            backgroundColor: tokens.colors.surface,
            borderRadius: tokens.borderRadius.lg,
          }}
        >
          {/* Decorative top line */}
          <div className="absolute top-0 left-0 right-0 h-1" style={{ backgroundColor: tokens.colors.primary }} />

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 p-10 md:p-16">
            {/* Left — Text */}
            <div className="flex flex-col justify-center">
              <span
                className="inline-block mb-4 text-sm font-semibold tracking-widest uppercase"
                style={{ color: tokens.colors.primary, fontFamily: tokens.typography.bodyFont }}
              >
                Pronto para transformar seu visual?
              </span>
              <h2
                className="mb-4"
                style={{
                  fontFamily: tokens.typography.headingFont,
                  fontSize: tokens.typography.scale.h2,
                  fontWeight: tokens.typography.weight.bold,
                  color: tokens.colors.text,
                  lineHeight: tokens.typography.lineHeight.tight,
                  letterSpacing: tokens.typography.letterSpacing.normal,
                }}
              >
                {title}
              </h2>
              {subtitle && (
                <p
                  className="mb-8 text-lg"
                  style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}
                >
                  {subtitle}
                </p>
              )}
              <a
                href={cta.href}
                className="group inline-flex items-center gap-3 px-10 py-4 text-lg font-bold transition-all duration-300 self-start"
                style={{
                  fontFamily: tokens.typography.bodyFont,
                  backgroundColor: tokens.colors.primary,
                  color: tokens.colors.textInverse,
                  letterSpacing: tokens.typography.letterSpacing.normal,
                  boxShadow: tokens.shadows.glow,
                }}
              >
                {cta.label}
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </a>
            </div>

            {/* Right — Features */}
            {features && features.length > 0 && (
              <div className="flex flex-col justify-center space-y-5">
                {features.map((f, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, x: 20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: 0.3 + i * 0.1, duration: 0.4 }}
                    className="flex items-start gap-4"
                  >
                    <CheckCircle2 className="w-6 h-6 flex-shrink-0 mt-0.5" style={{ color: tokens.colors.success }} />
                    <span style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary, lineHeight: tokens.typography.lineHeight.normal }}>
                      {f.text}
                    </span>
                  </motion.div>
                ))}
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
