// ============================================================
// CLASSIC Theme — About
// ============================================================

import { motion } from "framer-motion";
import { Scissors } from "lucide-react";
import type { AboutProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function About({ title, description, highlights, image, imageAlt = "Sobre" }: AboutProps) {
  return (
    <section style={{ backgroundColor: tokens.colors.background, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="classic-about-title">
      <div className="max-w-[1280px] mx-auto px-6 md:px-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <motion.div initial={{ opacity: 0, x: -40 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} transition={{ duration: 0.7 }}>
            <div className="relative">
              <div className="overflow-hidden border-4" style={{ borderColor: tokens.colors.primary, borderRadius: tokens.borderRadius.lg }}>
                {image ? <img src={image} alt={imageAlt} className="w-full aspect-[4/5] object-cover" loading="lazy" /> : <div className="w-full aspect-[4/5] flex items-center justify-center" style={{ backgroundColor: tokens.colors.surfaceAlt }}><Scissors className="w-16 h-16 opacity-20" style={{ color: tokens.colors.primary }} /></div>}
              </div>
              <div className="absolute -bottom-4 -right-4 w-full h-full border-2 -z-10" style={{ borderColor: tokens.colors.secondary, borderRadius: tokens.borderRadius.lg }} />
            </div>
          </motion.div>
          <motion.div initial={{ opacity: 0, x: 40 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} transition={{ duration: 0.7, delay: 0.2 }}>
            <span className="inline-block mb-4 text-xs tracking-[0.25em] uppercase" style={{ color: tokens.colors.secondary, fontFamily: tokens.typography.bodyFont }}>Nossa Tradição</span>
            <h2 id="classic-about-title" className="mb-6" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text, lineHeight: tokens.typography.lineHeight.tight }}>{title}</h2>
            <div className="w-12 h-px mb-6" style={{ backgroundColor: tokens.colors.secondary }} />
            <p className="mb-10 text-base leading-relaxed" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary, lineHeight: tokens.typography.lineHeight.relaxed }}>{description}</p>
            {highlights && highlights.length > 0 && <div className="grid grid-cols-3 gap-6">{highlights.map((h, i) => <div key={i} className="text-center p-4 border" style={{ borderColor: tokens.colors.borderLight, backgroundColor: tokens.colors.surface }}><div className="text-2xl font-bold mb-1" style={{ fontFamily: tokens.typography.headingFont, color: tokens.colors.primary }}>{h.value}</div><div className="text-xs tracking-wider uppercase" style={{ color: tokens.colors.textMuted }}>{h.label}</div></div>)}</div>}
          </motion.div>
        </div>
      </div>
    </section>
  );
}
