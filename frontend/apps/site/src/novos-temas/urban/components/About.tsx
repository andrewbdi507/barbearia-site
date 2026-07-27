// ============================================================
// URBAN Theme — About Section
// Layout split com imagem estilo editorial e texto impactante.
// ============================================================

import { motion } from "framer-motion";
import { Scissors, Clock, Award } from "lucide-react";
import type { AboutProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

const defaultHighlights = [
  { icon: "Scissors", label: "Anos de Experiência", value: "15+" },
  { icon: "Clock", label: "Clientes Atendidos", value: "10k+" },
  { icon: "Award", label: "Avaliação Média", value: "4.9" },
];

const iconMap: Record<string, React.ReactNode> = {
  Scissors: <Scissors className="w-6 h-6" />,
  Clock: <Clock className="w-6 h-6" />,
  Award: <Award className="w-6 h-6" />,
};

export function About({ title, description, highlights, image, imageAlt = "Sobre nós" }: AboutProps) {
  const items = highlights?.length ? highlights : defaultHighlights;

  return (
    <section
      className="relative overflow-hidden"
      style={{ backgroundColor: tokens.colors.background, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }}
      aria-labelledby="about-title"
    >
      <div className="max-w-[1400px] mx-auto px-6 md:px-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 lg:gap-24 items-center">
          {/* Image Side */}
          <motion.div
            initial={{ opacity: 0, x: -60 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.8, ease: tokens.motion.easing.easeOut }}
            className="relative"
          >
            <div className="relative overflow-hidden" style={{ borderRadius: tokens.borderRadius.lg }}>
              {image ? (
                <img
                  src={image}
                  alt={imageAlt}
                  className="w-full h-auto object-cover aspect-[4/5]"
                  loading="lazy"
                />
              ) : (
                <div
                  className="w-full aspect-[4/5] flex items-center justify-center"
                  style={{ backgroundColor: tokens.colors.surface, color: tokens.colors.textMuted }}
                >
                  <Scissors className="w-16 h-16 opacity-20" />
                </div>
              )}
              {/* Border Accent */}
              <div
                className="absolute -bottom-3 -right-3 w-full h-full -z-10"
                style={{ border: `2px solid ${tokens.colors.primary}`, borderRadius: tokens.borderRadius.lg }}
              />
            </div>
            {/* Neon highlight */}
            <div
              className="absolute -top-6 -left-6 w-32 h-32 rounded-full blur-[60px] -z-10"
              style={{ backgroundColor: tokens.colors.primary, opacity: 0.15 }}
            />
          </motion.div>

          {/* Text Side */}
          <motion.div
            initial={{ opacity: 0, x: 60 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.8, ease: tokens.motion.easing.easeOut, delay: 0.2 }}
          >
            {/* Label */}
            <span
              className="inline-block mb-4 text-sm font-semibold tracking-widest uppercase"
              style={{ color: tokens.colors.primary, fontFamily: tokens.typography.bodyFont }}
            >
              Nossa História
            </span>

            <h2
              id="about-title"
              className="mb-6"
              style={{
                fontFamily: tokens.typography.headingFont,
                fontSize: tokens.typography.scale.h2,
                fontWeight: tokens.typography.weight.bold,
                color: tokens.colors.text,
                lineHeight: tokens.typography.lineHeight.tight,
                letterSpacing: tokens.typography.letterSpacing.normal,
              }}
            >
              {title}
            </h2>

            <p
              className="mb-10 text-lg leading-relaxed"
              style={{
                fontFamily: tokens.typography.bodyFont,
                color: tokens.colors.textSecondary,
                lineHeight: tokens.typography.lineHeight.relaxed,
              }}
            >
              {description}
            </p>

            {/* Highlights Grid */}
            <div className="grid grid-cols-3 gap-6">
              {items.map((item, i) => (
                <motion.div
                  key={item.label}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: 0.3 + i * 0.1, duration: 0.5 }}
                  className="text-center p-4 border"
                  style={{
                    borderColor: tokens.colors.borderLight,
                    backgroundColor: tokens.colors.surface,
                  }}
                >
                  <div
                    className="inline-flex items-center justify-center w-12 h-12 mb-3 rounded-full"
                    style={{ backgroundColor: tokens.colors.primaryLight, color: tokens.colors.primary }}
                  >
                    {iconMap[item.icon || "Scissors"] || <Scissors className="w-5 h-5" />}
                  </div>
                  <div
                    className="text-2xl font-bold mb-1"
                    style={{ fontFamily: tokens.typography.headingFont, color: tokens.colors.text }}
                  >
                    {item.value}
                  </div>
                  <div className="text-xs uppercase tracking-wider" style={{ color: tokens.colors.textMuted, fontFamily: tokens.typography.bodyFont }}>
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
