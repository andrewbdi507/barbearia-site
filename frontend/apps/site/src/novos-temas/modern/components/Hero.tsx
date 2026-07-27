// ============================================================
// MODERN Theme — Hero
// Apple-like, ciano/magenta, glassmorphism, bordas arredondadas.
// ============================================================

import { useRef } from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import { ArrowRight, Zap } from "lucide-react";
import type { HeroProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function Hero({ title, subtitle, cta, secondaryCta, backgroundImage, overlayOpacity = 0.5 }: HeroProps) {
  const ref = useRef<HTMLElement>(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start start", "end start"] });
  const bgY = useTransform(scrollYProgress, [0, 1], [0, -80]);
  const contentY = useTransform(scrollYProgress, [0, 1], [0, 60]);
  const opacity = useTransform(scrollYProgress, [0, 0.4], [1, 0]);

  return (
    <section ref={ref} className="relative min-h-screen flex items-center justify-center overflow-hidden" style={{ backgroundColor: tokens.colors.background }} aria-label="Hero">
      {backgroundImage && (
        <motion.div className="absolute inset-0 z-0" style={{ y: bgY }}>
          <img src={backgroundImage} alt="" className="w-full h-full object-cover" loading="eager" fetchPriority="high" decoding="async" />
          <div className="absolute inset-0" style={{ background: `linear-gradient(180deg, ${tokens.colors.background} 0%, rgba(10,10,15,${overlayOpacity}) 50%, ${tokens.colors.background} 100%)` }} />
        </motion.div>
      )}
      <motion.div className="absolute top-1/4 -left-20 w-[500px] h-[500px] rounded-full blur-[150px] z-[1]" style={{ backgroundColor: tokens.colors.primary }} animate={{ opacity: [0.06, 0.14, 0.06], scale: [1, 1.1, 1] }} transition={{ duration: 5, repeat: Infinity }} />
      <motion.div className="absolute bottom-1/4 -right-20 w-[500px] h-[500px] rounded-full blur-[150px] z-[1]" style={{ backgroundColor: tokens.colors.secondary }} animate={{ opacity: [0.05, 0.12, 0.05], scale: [1, 1.15, 1] }} transition={{ duration: 6, repeat: Infinity, delay: 1 }} />
      <motion.div className="relative z-10 w-full max-w-[1400px] mx-auto px-6 md:px-12 text-center" style={{ y: contentY, opacity }}>
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.1 }} className="inline-flex items-center gap-2 mb-8 px-4 py-2 rounded-full border text-xs font-medium backdrop-blur-xl" style={{ borderColor: tokens.colors.border, backgroundColor: tokens.colors.surface, color: tokens.colors.primary, fontFamily: tokens.typography.bodyFont }}>
          <Zap className="w-3.5 h-3.5" /> Agendamento inteligente
        </motion.div>
        <motion.h1 initial={{ opacity: 0, y: 40 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7, delay: 0.2, ease: tokens.motion.easing.easeOut }} className="mb-6" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.display, fontWeight: tokens.typography.weight.extrabold, color: tokens.colors.text, lineHeight: tokens.typography.lineHeight.tight, letterSpacing: tokens.typography.letterSpacing.tight }}>
          <span dangerouslySetInnerHTML={{ __html: title }} />
        </motion.h1>
        {subtitle && <motion.p initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.4 }} className="mb-10 max-w-xl mx-auto text-lg" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary, fontWeight: tokens.typography.weight.regular }}>{subtitle}</motion.p>}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.6 }} className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <a href={cta.href} className="group relative inline-flex items-center gap-2 px-8 py-3.5 text-sm font-semibold transition-all duration-300 overflow-hidden" style={{ fontFamily: tokens.typography.bodyFont, background: `linear-gradient(135deg, ${tokens.colors.primary}, ${tokens.colors.secondary})`, color: tokens.colors.textInverse, borderRadius: tokens.borderRadius.full, boxShadow: tokens.shadows.glow }}>
            <span className="relative z-10 flex items-center gap-2">{cta.label} <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" /></span>
          </a>
          {secondaryCta && <a href={secondaryCta.href} className="inline-flex items-center gap-2 px-8 py-3.5 text-sm font-medium border transition-all duration-300" style={{ fontFamily: tokens.typography.bodyFont, borderColor: tokens.colors.border, color: tokens.colors.text, borderRadius: tokens.borderRadius.full, backdropFilter: `blur(${tokens.glassmorphism.blur})`, backgroundColor: tokens.colors.surface }}>{secondaryCta.label}</a>}
        </motion.div>
      </motion.div>
    </section>
  );
}
