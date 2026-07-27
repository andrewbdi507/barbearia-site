// ============================================================
// MINIMAL Theme — Hero
// ============================================================

import { useRef } from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import { ArrowRight, ArrowDown } from "lucide-react";
import type { HeroProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function Hero({ title, subtitle, cta, secondaryCta, backgroundImage, overlayOpacity = 0.35 }: HeroProps) {
  const ref = useRef<HTMLElement>(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start start", "end start"] });
  const contentY = useTransform(scrollYProgress, [0, 1], [0, 40]);
  const opacity = useTransform(scrollYProgress, [0, 0.4], [1, 0]);

  return (
    <section ref={ref} className="relative min-h-screen flex items-center overflow-hidden" style={{ backgroundColor: tokens.colors.background }} aria-label="Hero">
      {backgroundImage && (
        <div className="absolute inset-0 z-0">
          <img src={backgroundImage} alt="" className="w-full h-full object-cover" loading="eager" fetchPriority="high" decoding="async" />
          <div className="absolute inset-0" style={{ background: `rgba(250,250,250,${overlayOpacity})` }} />
        </div>
      )}
      <motion.div className="relative z-10 w-full max-w-[1200px] mx-auto px-6 md:px-12" style={{ y: contentY, opacity }}>
        <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6, delay: 0.2, ease: tokens.motion.easing.easeOut }} className="max-w-2xl">
          <h1 className="mb-6" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.display, fontWeight: tokens.typography.weight.semibold, color: tokens.colors.text, lineHeight: tokens.typography.lineHeight.tight, letterSpacing: tokens.typography.letterSpacing.tight }} dangerouslySetInnerHTML={{ __html: title }} />
          {subtitle && <motion.p initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.4 }} className="mb-10 text-lg leading-relaxed max-w-lg" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary, fontWeight: tokens.typography.weight.regular }}>{subtitle}</motion.p>}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.6 }} className="flex flex-col sm:flex-row gap-4">
            <a href={cta.href} className="group inline-flex items-center gap-2 px-8 py-3.5 text-sm font-semibold transition-all duration-300" style={{ fontFamily: tokens.typography.bodyFont, backgroundColor: tokens.colors.primary, color: tokens.colors.textInverse, borderRadius: tokens.borderRadius.md }}>{cta.label} <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" /></a>
            {secondaryCta && <a href={secondaryCta.href} className="inline-flex items-center gap-2 px-8 py-3.5 text-sm font-medium border transition-all duration-300" style={{ fontFamily: tokens.typography.bodyFont, borderColor: tokens.colors.border, color: tokens.colors.text, borderRadius: tokens.borderRadius.md }}>{secondaryCta.label}</a>}
          </motion.div>
        </motion.div>
      </motion.div>
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1 }} className="absolute bottom-10 left-6 md:left-12 flex items-center gap-2 text-xs" style={{ color: tokens.colors.textMuted }}>
        <ArrowDown className="w-3.5 h-3.5 animate-bounce" /> Scroll
      </motion.div>
    </section>
  );
}
