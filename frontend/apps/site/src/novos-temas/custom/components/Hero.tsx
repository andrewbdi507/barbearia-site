// ============================================================
// CUSTOM Theme — Hero
// Neutro, white-label, pronto para branding.
// ============================================================

import { useRef } from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import { ArrowRight } from "lucide-react";
import type { HeroProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function Hero({ title, subtitle, cta, secondaryCta, backgroundImage }: HeroProps) {
  const ref = useRef<HTMLElement>(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start start", "end start"] });
  const contentY = useTransform(scrollYProgress, [0, 1], [0, 40]);
  return (
    <section ref={ref} className="relative min-h-[90vh] flex items-center" style={{ backgroundColor: tokens.colors.background }} aria-label="Hero">
      {backgroundImage && <div className="absolute inset-0 z-0"><img src={backgroundImage} alt="" className="w-full h-full object-cover" loading="eager" fetchPriority="high" decoding="async" /><div className="absolute inset-0 bg-white/60" /></div>}
      <motion.div className="relative z-10 w-full max-w-[1200px] mx-auto px-6 md:px-12" style={{ y: contentY }}>
        <div className="max-w-2xl">
          <motion.h1 initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.2 }} className="mb-6" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.display, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text, lineHeight: tokens.typography.lineHeight.tight }} dangerouslySetInnerHTML={{ __html: title }} />
          {subtitle && <motion.p initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.35 }} className="mb-8 text-lg max-w-lg" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{subtitle}</motion.p>}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.5 }} className="flex flex-col sm:flex-row gap-4">
            <a href={cta.href} className="group inline-flex items-center gap-2 px-8 py-3.5 text-sm font-semibold transition-all duration-300" style={{ fontFamily: tokens.typography.bodyFont, backgroundColor: tokens.colors.primary, color: tokens.colors.textInverse, borderRadius: tokens.borderRadius.md }}>{cta.label} <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" /></a>
            {secondaryCta && <a href={secondaryCta.href} className="inline-flex items-center gap-2 px-8 py-3.5 text-sm font-medium border transition-all duration-300" style={{ fontFamily: tokens.typography.bodyFont, borderColor: tokens.colors.border, color: tokens.colors.text, borderRadius: tokens.borderRadius.md }}>{secondaryCta.label}</a>}
          </motion.div>
        </div>
      </motion.div>
    </section>
  );
}
