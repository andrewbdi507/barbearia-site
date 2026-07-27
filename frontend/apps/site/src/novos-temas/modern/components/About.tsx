// ============================================================
// MODERN Theme — About
// ============================================================

import { motion } from "framer-motion";
import { Scissors } from "lucide-react";
import type { AboutProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function About({ title, description, highlights, image, imageAlt = "Sobre" }: AboutProps) {
  return (
    <section style={{ backgroundColor: tokens.colors.background, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="modern-about-title">
      <div className="max-w-[1400px] mx-auto px-6 md:px-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <motion.div initial={{ opacity: 0, x: -40 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} transition={{ duration: 0.6, ease: tokens.motion.easing.easeOut }}>
            <div className="relative overflow-hidden" style={{ borderRadius: tokens.borderRadius.xl }}>
              {image ? <img src={image} alt={imageAlt} className="w-full aspect-[4/5] object-cover" loading="lazy" /> : <div className="w-full aspect-[4/5] flex items-center justify-center" style={{ backgroundColor: tokens.colors.surfaceHover }}><Scissors className="w-16 h-16 opacity-20" style={{ color: tokens.colors.primary }} /></div>}
            </div>
          </motion.div>
          <motion.div initial={{ opacity: 0, x: 40 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} transition={{ duration: 0.6, delay: 0.2, ease: tokens.motion.easing.easeOut }}>
            <span className="inline-block mb-4 text-xs font-semibold tracking-widest uppercase" style={{ color: tokens.colors.primary, fontFamily: tokens.typography.bodyFont }}>Sobre Nós</span>
            <h2 id="modern-about-title" className="mb-6" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text, letterSpacing: tokens.typography.letterSpacing.tight }}>{title}</h2>
            <p className="mb-8 text-base leading-relaxed" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary, lineHeight: tokens.typography.lineHeight.relaxed }}>{description}</p>
            {highlights && highlights.length > 0 && <div className="grid grid-cols-3 gap-4">{highlights.map((h, i) => <div key={i} className="text-center p-5 rounded-2xl border" style={{ borderColor: tokens.colors.borderLight, backgroundColor: tokens.colors.surface }}><div className="text-2xl font-bold mb-1" style={{ fontFamily: tokens.typography.headingFont, background: `linear-gradient(135deg, ${tokens.colors.primary}, ${tokens.colors.secondary})`, WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>{h.value}</div><div className="text-xs" style={{ color: tokens.colors.textMuted }}>{h.label}</div></div>)}</div>}
          </motion.div>
        </div>
      </div>
    </section>
  );
}
