// ============================================================
// MINIMAL Theme — About
// ============================================================

import { motion } from "framer-motion";
import { Scissors } from "lucide-react";
import type { AboutProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function About({ title, description, highlights, image, imageAlt = "Sobre" }: AboutProps) {
  return (
    <section style={{ backgroundColor: tokens.colors.background, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="minimal-about-title">
      <div className="max-w-[1200px] mx-auto px-6 md:px-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <motion.div initial={{ opacity: 0, x: -30 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} transition={{ duration: 0.6 }} className="relative">
            <div className="overflow-hidden" style={{ borderRadius: tokens.borderRadius.lg }}>
              {image ? <img src={image} alt={imageAlt} className="w-full aspect-[4/5] object-cover" loading="lazy" /> : <div className="w-full aspect-[4/5] flex items-center justify-center" style={{ backgroundColor: tokens.colors.surfaceAlt, color: tokens.colors.textMuted }}><Scissors className="w-12 h-12 opacity-20" /></div>}
            </div>
          </motion.div>
          <motion.div initial={{ opacity: 0, x: 30 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} transition={{ duration: 0.6, delay: 0.2 }}>
            <span className="inline-block mb-3 text-xs font-medium tracking-wider uppercase" style={{ color: tokens.colors.textMuted, fontFamily: tokens.typography.bodyFont }}>Sobre</span>
            <h2 id="minimal-about-title" className="mb-6" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.semibold, color: tokens.colors.text, letterSpacing: tokens.typography.letterSpacing.tight }}>{title}</h2>
            <p className="text-base leading-relaxed" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary, lineHeight: tokens.typography.lineHeight.relaxed }}>{description}</p>
            {highlights && highlights.length > 0 && (
              <div className="grid grid-cols-3 gap-6 mt-10 pt-10 border-t" style={{ borderColor: tokens.colors.borderLight }}>
                {highlights.map((h, i) => <div key={i} className="text-center"><div className="text-2xl font-bold mb-1" style={{ fontFamily: tokens.typography.headingFont, color: tokens.colors.text }}>{h.value}</div><div className="text-xs" style={{ color: tokens.colors.textMuted }}>{h.label}</div></div>)}
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </section>
  );
}
