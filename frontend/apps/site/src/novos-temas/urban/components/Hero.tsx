// ============================================================
// URBAN Theme — Hero Section
// Fullscreen, cinematográfico, tipografia bold com neon.
// ============================================================

import { useRef } from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import { ArrowRight, Play, Zap } from "lucide-react";
import type { HeroProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function Hero({
  title,
  subtitle,
  cta,
  secondaryCta,
  backgroundImage,
  overlayOpacity = 0.65,
}: HeroProps) {
  const ref = useRef<HTMLElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start start", "end start"],
  });

  const bgScale = useTransform(scrollYProgress, [0, 1], [1, 1.15]);
  const contentY = useTransform(scrollYProgress, [0, 1], [0, 100]);
  const opacity = useTransform(scrollYProgress, [0, 0.5], [1, 0]);

  return (
    <section
      ref={ref}
      className="relative min-h-screen flex items-center justify-center overflow-hidden"
      style={{ backgroundColor: tokens.colors.background }}
      aria-label="Hero"
    >
      {/* Background Image with Parallax */}
      {backgroundImage && (
        <motion.div className="absolute inset-0 z-0" style={{ scale: bgScale }}>
          <img
            src={backgroundImage}
            alt=""
            className="w-full h-full object-cover"
            loading="eager"
            decoding="async"
            fetchPriority="high"
          />
          {/* Gradient Overlay */}
          <div
            className="absolute inset-0"
            style={{
              background: `linear-gradient(180deg, 
                ${tokens.colors.background} 0%, 
                rgba(10,10,10,${overlayOpacity}) 30%, 
                rgba(10,10,10,${overlayOpacity}) 70%, 
                ${tokens.colors.background} 100%)`,
            }}
          />
          {/* Grain Texture */}
          <div
            className="absolute inset-0 opacity-[0.03]"
            style={{
              backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")`,
            }}
          />
        </motion.div>
      )}

      {/* Neon Accent Lines */}
      <div className="absolute left-0 top-1/4 bottom-1/4 w-px z-[1]" style={{ background: `linear-gradient(180deg, transparent, ${tokens.colors.primary}40, transparent)` }} />
      <div className="absolute right-0 top-1/3 bottom-1/3 w-px z-[1]" style={{ background: `linear-gradient(180deg, transparent, ${tokens.colors.primary}30, transparent)` }} />

      {/* Floating Neon Orbs */}
      <motion.div
        className="absolute top-1/4 left-[15%] w-64 h-64 rounded-full blur-[120px] z-[1]"
        style={{ backgroundColor: tokens.colors.primary }}
        animate={{ opacity: [0.08, 0.15, 0.08], scale: [1, 1.1, 1] }}
        transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
      />
      <motion.div
        className="absolute bottom-1/4 right-[10%] w-96 h-96 rounded-full blur-[150px] z-[1]"
        style={{ backgroundColor: tokens.colors.primary }}
        animate={{ opacity: [0.05, 0.12, 0.05], scale: [1, 1.15, 1] }}
        transition={{ duration: 5, repeat: Infinity, ease: "easeInOut", delay: 1 }}
      />

      {/* Content */}
      <motion.div
        className="relative z-10 w-full max-w-[1400px] mx-auto px-6 md:px-12 text-center"
        style={{ y: contentY, opacity }}
      >
        {/* Badge */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="inline-flex items-center gap-2 mb-8 px-5 py-2 rounded-full border text-sm font-medium"
          style={{
            borderColor: tokens.colors.border,
            backgroundColor: tokens.colors.primaryLight,
            color: tokens.colors.primary,
            fontFamily: tokens.typography.bodyFont,
          }}
        >
          <Zap className="w-4 h-4" />
          AGENDA OS — BARBEARIA PREMIUM
        </motion.div>

        {/* Title */}
        <motion.h1
          initial={{ opacity: 0, y: 60 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2, ease: [0.25, 0.46, 0.45, 0.94] }}
          className="mb-6 tracking-wide"
          style={{
            fontFamily: tokens.typography.headingFont,
            fontSize: tokens.typography.scale.display,
            fontWeight: tokens.typography.weight.extrabold,
            color: tokens.colors.text,
            lineHeight: tokens.typography.lineHeight.tight,
            letterSpacing: tokens.typography.letterSpacing.normal,
            textShadow: `0 0 80px ${tokens.colors.primary}30`,
          }}
          dangerouslySetInnerHTML={{ __html: title }}
        />

        {/* Subtitle */}
        {subtitle && (
          <motion.p
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="mb-10 max-w-2xl mx-auto text-lg md:text-xl"
            style={{
              fontFamily: tokens.typography.bodyFont,
              color: tokens.colors.textSecondary,
              lineHeight: tokens.typography.lineHeight.relaxed,
              fontWeight: tokens.typography.weight.regular,
            }}
          >
            {subtitle}
          </motion.p>
        )}

        {/* CTAs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="flex flex-col sm:flex-row items-center justify-center gap-4"
        >
          <a
            href={cta.href}
            className="group relative inline-flex items-center gap-3 px-10 py-4 text-lg font-bold overflow-hidden transition-all duration-300"
            style={{
              fontFamily: tokens.typography.bodyFont,
              backgroundColor: tokens.colors.primary,
              color: tokens.colors.textInverse,
              letterSpacing: tokens.typography.letterSpacing.normal,
              boxShadow: tokens.shadows.glow,
            }}
          >
            <span className="relative z-10 flex items-center gap-2">
              {cta.label}
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </span>
            <motion.span
              className="absolute inset-0 z-0"
              style={{ backgroundColor: tokens.colors.primaryHover }}
              initial={{ x: "-100%" }}
              whileHover={{ x: 0 }}
              transition={{ duration: 0.3 }}
            />
          </a>
          {secondaryCta && (
            <a
              href={secondaryCta.href}
              className="group inline-flex items-center gap-3 px-10 py-4 text-lg font-bold border-2 transition-all duration-300"
              style={{
                fontFamily: tokens.typography.bodyFont,
                borderColor: tokens.colors.primary,
                color: tokens.colors.text,
                letterSpacing: tokens.typography.letterSpacing.normal,
              }}
            >
              <Play className="w-5 h-5" />
              {secondaryCta.label}
            </a>
          )}
        </motion.div>

        {/* Scroll Indicator */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.5 }}
          className="absolute bottom-10 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2"
        >
          <span className="text-xs tracking-widest uppercase" style={{ color: tokens.colors.textMuted }}>
            Scroll
          </span>
          <motion.div
            className="w-6 h-10 rounded-full border flex items-start justify-center p-1"
            style={{ borderColor: tokens.colors.border }}
          >
            <motion.div
              className="w-1.5 h-3 rounded-full"
              style={{ backgroundColor: tokens.colors.primary }}
              animate={{ y: [0, 12, 0] }}
              transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
            />
          </motion.div>
        </motion.div>
      </motion.div>
    </section>
  );
}
