// ============================================================
// LUXURY Theme — Hero Section
// Elegante, centralizado, dourado, animações suaves.
// ============================================================

import { useRef } from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import { ArrowRight, Sparkles } from "lucide-react";
import type { HeroProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function Hero({
  title,
  subtitle,
  cta,
  secondaryCta,
  backgroundImage,
  overlayOpacity = 0.7,
}: HeroProps) {
  const ref = useRef<HTMLElement>(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start start", "end start"] });
  const bgScale = useTransform(scrollYProgress, [0, 1], [1, 1.08]);
  const contentY = useTransform(scrollYProgress, [0, 1], [0, 60]);
  const opacity = useTransform(scrollYProgress, [0, 0.4], [1, 0]);

  return (
    <section
      ref={ref}
      className="relative min-h-screen flex items-center justify-center overflow-hidden"
      style={{ backgroundColor: tokens.colors.background }}
      aria-label="Hero"
    >
      {/* Background Image */}
      {backgroundImage && (
        <motion.div className="absolute inset-0 z-0" style={{ scale: bgScale }}>
          <img src={backgroundImage} alt="" className="w-full h-full object-cover" loading="eager" fetchPriority="high" decoding="async" />
          <div className="absolute inset-0" style={{ background: `linear-gradient(180deg, ${tokens.colors.background} 0%, rgba(8,8,8,${overlayOpacity}) 30%, rgba(8,8,8,${overlayOpacity}) 70%, ${tokens.colors.background} 100%)` }} />
        </motion.div>
      )}

      {/* Gold ambient glow */}
      <motion.div
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] rounded-full blur-[200px] z-[1]"
        style={{ backgroundColor: tokens.colors.primary }}
        animate={{ opacity: [0.04, 0.10, 0.04] }}
        transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
      />

      {/* Ornamental lines */}
      <div className="absolute top-0 left-0 right-0 z-[1] flex justify-center pt-12">
        <div className="flex items-center gap-6">
          <div className="w-16 h-px" style={{ backgroundColor: tokens.colors.primary, opacity: 0.4 }} />
          <div className="w-1.5 h-1.5 rotate-45" style={{ backgroundColor: tokens.colors.primary, opacity: 0.6 }} />
          <div className="w-16 h-px" style={{ backgroundColor: tokens.colors.primary, opacity: 0.4 }} />
        </div>
      </div>

      {/* Content */}
      <motion.div
        className="relative z-10 w-full max-w-[1000px] mx-auto px-6 md:px-12 text-center"
        style={{ y: contentY, opacity }}
      >
        {/* Ornament */}
        <motion.div
          initial={{ opacity: 0, scale: 0 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.2, ease: [0.34, 1.56, 0.64, 1] }}
          className="mb-10 inline-flex items-center gap-4"
        >
          <div className="w-12 h-px" style={{ backgroundColor: tokens.colors.primary, opacity: 0.6 }} />
          <Sparkles className="w-5 h-5" style={{ color: tokens.colors.primary }} />
          <div className="w-12 h-px" style={{ backgroundColor: tokens.colors.primary, opacity: 0.6 }} />
        </motion.div>

        {/* Title */}
        <motion.h1
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 0.4, ease: [0.25, 0.1, 0.25, 1] }}
          className="mb-8"
          style={{
            fontFamily: tokens.typography.headingFont,
            fontSize: tokens.typography.scale.display,
            fontWeight: tokens.typography.weight.bold,
            color: tokens.colors.text,
            lineHeight: tokens.typography.lineHeight.tight,
            letterSpacing: tokens.typography.letterSpacing.tight,
            textShadow: `0 0 60px ${tokens.colors.primary}15`,
          }}
          dangerouslySetInnerHTML={{ __html: title }}
        />

        {/* Divider */}
        <motion.div
          initial={{ scaleX: 0 }}
          animate={{ scaleX: 1 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="mx-auto mb-8 w-24 h-px"
          style={{ backgroundColor: tokens.colors.primary, opacity: 0.5 }}
        />

        {/* Subtitle */}
        {subtitle && (
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.7 }}
            className="mb-12 max-w-xl mx-auto text-lg md:text-xl italic"
            style={{
              fontFamily: tokens.typography.bodyFont,
              color: tokens.colors.textSecondary,
              lineHeight: tokens.typography.lineHeight.relaxed,
              fontWeight: tokens.typography.weight.light,
            }}
          >
            {subtitle}
          </motion.p>
        )}

        {/* CTAs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.9 }}
          className="flex flex-col sm:flex-row items-center justify-center gap-5"
        >
          <a
            href={cta.href}
            className="group relative inline-flex items-center gap-3 px-12 py-4 text-base font-semibold tracking-wider uppercase overflow-hidden transition-all duration-500"
            style={{
              fontFamily: tokens.typography.bodyFont,
              backgroundColor: tokens.colors.primary,
              color: tokens.colors.textInverse,
              letterSpacing: tokens.typography.letterSpacing.wide,
              boxShadow: tokens.shadows.glow,
            }}
          >
            <span className="relative z-10 flex items-center gap-2">
              {cta.label}
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </span>
          </a>
          {secondaryCta && (
            <a
              href={secondaryCta.href}
              className="inline-flex items-center gap-2 px-10 py-4 text-base tracking-wider uppercase border transition-all duration-500 hover:-translate-y-0.5"
              style={{
                fontFamily: tokens.typography.bodyFont,
                borderColor: tokens.colors.border,
                color: tokens.colors.text,
                letterSpacing: tokens.typography.letterSpacing.wide,
              }}
            >
              {secondaryCta.label}
            </a>
          )}
        </motion.div>
      </motion.div>

      {/* Bottom ornament */}
      <div className="absolute bottom-16 left-1/2 -translate-x-1/2 z-10">
        <motion.div
          animate={{ y: [0, 8, 0] }}
          transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
          className="text-xs tracking-[0.3em] uppercase"
          style={{ color: tokens.colors.textMuted, fontFamily: tokens.typography.bodyFont }}
        >
          Deslize para descobrir
        </motion.div>
      </div>
    </section>
  );
}
