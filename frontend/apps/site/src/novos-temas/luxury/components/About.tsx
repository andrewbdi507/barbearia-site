// ============================================================
// LUXURY Theme — About Section
// Elegante, com tipografia refinada e layout editorial.
// ============================================================

import { motion } from "framer-motion";
import { Crown, Shield, Sparkles } from "lucide-react";
import type { AboutProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

const defaultHighlights = [
  { icon: "Crown", label: "Tradição", value: "20+" },
  { icon: "Shield", label: "Excelência", value: "Premium" },
  { icon: "Sparkles", label: "Clientes VIP", value: "5k+" },
];

const iconMap: Record<string, React.ReactNode> = {
  Crown: <Crown className="w-5 h-5" />,
  Shield: <Shield className="w-5 h-5" />,
  Sparkles: <Sparkles className="w-5 h-5" />,
};

export function About({ title, description, highlights, image, imageAlt = "Sobre" }: AboutProps) {
  const items = highlights?.length ? highlights : defaultHighlights;

  return (
    <section
      style={{ backgroundColor: tokens.colors.background, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }}
      aria-labelledby="luxury-about-title"
    >
      <div className="max-w-[1280px] mx-auto px-6 md:px-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-20 items-center">
          {/* Image Side */}
          <motion.div
            initial={{ opacity: 0, clipPath: "inset(0 100% 0 0)" }}
            whileInView={{ opacity: 1, clipPath: "inset(0 0% 0 0)" }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 1, ease: tokens.motion.easing.easeOut }}
            className="relative"
          >
            <div className="relative overflow-hidden" style={{ borderRadius: tokens.borderRadius.lg }}>
              {image ? (
                <img src={image} alt={imageAlt} className="w-full h-auto object-cover aspect-[4/5]" loading="lazy" />
              ) : (
                <div className="w-full aspect-[4/5] flex items-center justify-center" style={{ backgroundColor: tokens.colors.surface, color: tokens.colors.textMuted }}>
                  <Crown className="w-16 h-16 opacity-20" />
                </div>
              )}
            </div>
            {/* Gold frame accent */}
            <div className="absolute -top-4 -left-4 w-32 h-32 border-t-2 border-l-2" style={{ borderColor: tokens.colors.primary, opacity: 0.3 }} />
            <div className="absolute -bottom-4 -right-4 w-32 h-32 border-b-2 border-r-2" style={{ borderColor: tokens.colors.primary, opacity: 0.3 }} />
          </motion.div>

          {/* Text Side */}
          <motion.div
            initial={{ opacity: 0, x: 40 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.9, delay: 0.3, ease: tokens.motion.easing.easeOut }}
          >
            <span
              className="inline-block mb-6 text-xs font-semibold tracking-[0.3em] uppercase"
              style={{ color: tokens.colors.primary, fontFamily: tokens.typography.bodyFont }}
            >
              Nossa Essência
            </span>

            <h2
              id="luxury-about-title"
              className="mb-8"
              style={{
                fontFamily: tokens.typography.headingFont,
                fontSize: tokens.typography.scale.h2,
                fontWeight: tokens.typography.weight.bold,
                color: tokens.colors.text,
                lineHeight: tokens.typography.lineHeight.tight,
                letterSpacing: tokens.typography.letterSpacing.tight,
              }}
            >
              {title}
            </h2>

            <div className="w-16 h-px mb-8" style={{ backgroundColor: tokens.colors.primary, opacity: 0.4 }} />

            <p
              className="mb-12 text-base leading-relaxed"
              style={{
                fontFamily: tokens.typography.bodyFont,
                color: tokens.colors.textSecondary,
                lineHeight: tokens.typography.lineHeight.relaxed,
                fontWeight: tokens.typography.weight.light,
              }}
            >
              {description}
            </p>

            {/* Highlights */}
            <div className="grid grid-cols-3 gap-8">
              {items.map((item, i) => (
                <motion.div
                  key={item.label}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: 0.5 + i * 0.15, duration: 0.6 }}
                  className="text-center"
                >
                  <div className="inline-flex items-center justify-center w-12 h-12 mb-4 rounded-full" style={{ backgroundColor: tokens.colors.primaryLight, color: tokens.colors.primary }}>
                    {iconMap[item.icon || "Crown"] || <Crown className="w-5 h-5" />}
                  </div>
                  <div className="text-2xl font-bold mb-1" style={{ fontFamily: tokens.typography.headingFont, color: tokens.colors.primary }}>
                    {item.value}
                  </div>
                  <div className="text-xs tracking-wider uppercase" style={{ color: tokens.colors.textMuted, fontFamily: tokens.typography.bodyFont }}>
                    {item.label}
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
