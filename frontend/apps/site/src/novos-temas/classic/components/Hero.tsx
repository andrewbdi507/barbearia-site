// ============================================================
// CLASSIC Theme — Hero
// ============================================================

import { useRef } from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import { ArrowRight } from "lucide-react";
import type { HeroProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function Hero({ title, subtitle, cta, secondaryCta, backgroundImage, overlayOpacity = 0.4 }: HeroProps) {
  const ref = useRef<HTMLElement>(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start start", "end start"] });
  const contentY = useTransform(scrollYProgress, [0, 1], [0, 50]);
  const opacity = useTransform(scrollYProgress, [0, 0.5], [1, 0]);

  return (
    <section ref={ref} className="relative min-h-screen flex items-center justify-center overflow-hidden" style={{ backgroundColor: tokens.colors.background }} aria-label="Hero">
      {backgroundImage && (
        <div className="absolute inset-0 z-0">
          <img src={backgroundImage} alt="" className="w-full h-full object-cover" loading="eager" fetchPriority="high" decoding="async" />
          <div className="absolute inset-0" style={{ background: `linear-gradient(180deg, ${tokens.colors.background} 0%, rgba(251,247,240,${overlayOpacity}) 40%, ${tokens.colors.background} 100%)` }} />
        </div>
      )}
      <div className="absolute top-8 left-8 right-8 bottom-8 border z-[1] pointer-events-none" style={{ borderColor: tokens.colors.primary, opacity: 0.15 }} />
      <div className="absolute top-12 left-12 right-12 bottom-12 border z-[1] pointer-events-none" style={{ borderColor: tokens.colors.primary, opacity: 0.08 }} />
      <motion.div className="relative z-10 w-full max-w-[1280px] mx-auto px-6 md:px-12 text-center" style={{ y: contentY, opacity }}>
        <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.8, delay: 0.2, ease: tokens.motion.easing.easeOut }}>
          <div className="flex items-center justify-center gap-4 mb-8">
            <div className="w-8 h-px" style={{ backgroundColor: tokens.colors.secondary }} />
            <span className="text-xs tracking-[0.3em] uppercase" style={{ color: tokens.colors.secondary, fontFamily: tokens.typography.bodyFont }}>Desde 1985</span>
            <div className="w-8 h-px" style={{ backgroundColor: tokens.colors.secondary }} />
          </div>
          <h1 className="mb-8" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.display, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text, lineHeight: tokens.typography.lineHeight.tight, letterSpacing: tokens.typography.letterSpacing.tight }} dangerouslySetInnerHTML={{ __html: title }} />
          <div className="mx-auto mb-8 w-16 h-px" style={{ backgroundColor: tokens.colors.secondary }} />
          {subtitle && <p className="mb-12 max-w-xl mx-auto text-lg italic" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary, fontWeight: tokens.typography.weight.light, lineHeight: tokens.typography.lineHeight.relaxed }}>{subtitle}</p>}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-5">
            <a href={cta.href} className="group inline-flex items-center gap-2 px-10 py-4 text-sm font-bold tracking-wider uppercase transition-all duration-500" style={{ fontFamily: tokens.typography.bodyFont, backgroundColor: tokens.colors.primary, color: tokens.colors.textInverse, letterSpacing: tokens.typography.letterSpacing.wide, borderRadius: tokens.borderRadius.sm, boxShadow: tokens.shadows.md }}>{cta.label} <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" /></a>
            {secondaryCta && <a href={secondaryCta.href} className="inline-flex items-center gap-2 px-10 py-4 text-sm font-medium tracking-wider uppercase border transition-all duration-500" style={{ fontFamily: tokens.typography.bodyFont, borderColor: tokens.colors.primary, color: tokens.colors.primary, borderRadius: tokens.borderRadius.sm, letterSpacing: tokens.typography.letterSpacing.wide }}>{secondaryCta.label}</a>}
          </div>
        </motion.div>
      </motion.div>
    </section>
  );
}
