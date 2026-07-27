// ============================================================
// URBAN Theme — Professionals Section
// Grid de cards com hover reveal e efeito glitch sutil.
// ============================================================

import { motion } from "framer-motion";
import { Star, Instagram, MessageCircle } from "lucide-react";
import type { ProfessionalsProps, Professional } from "../../shared/types";
import { tokens } from "../constants/tokens";

function ProfessionalCard({ pro, index }: { pro: Professional; index: number }) {
  return (
    <motion.article
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-60px" }}
      transition={{ duration: 0.5, delay: index * 0.1, ease: tokens.motion.easing.easeOut }}
      whileHover={{ y: -6 }}
      className="group relative overflow-hidden text-center"
    >
      {/* Avatar */}
      <div className="relative mx-auto mb-6 w-40 h-40 md:w-48 md:h-48 overflow-hidden" style={{ borderRadius: tokens.borderRadius.full }}>
        {pro.avatar ? (
          <img
            src={pro.avatar}
            alt={pro.name}
            className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
            loading="lazy"
          />
        ) : (
          <div
            className="w-full h-full flex items-center justify-center text-5xl font-bold"
            style={{
              backgroundColor: tokens.colors.surfaceHover,
              color: tokens.colors.primary,
              fontFamily: tokens.typography.headingFont,
            }}
          >
            {pro.name[0]}
          </div>
        )}
        {/* Border ring */}
        <div
          className="absolute inset-0 rounded-full border-2 opacity-0 group-hover:opacity-100 transition-all duration-500 scale-90 group-hover:scale-100"
          style={{ borderColor: tokens.colors.primary }}
        />
      </div>

      {/* Info */}
      <h3
        className="mb-1 text-xl transition-colors duration-300 group-hover:text-primary"
        style={{
          fontFamily: tokens.typography.headingFont,
          fontSize: tokens.typography.scale.h4,
          fontWeight: tokens.typography.weight.bold,
          color: tokens.colors.text,
          letterSpacing: tokens.typography.letterSpacing.normal,
        }}
      >
        {pro.name}
      </h3>
      <p className="mb-3 text-sm" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>
        {pro.role}
      </p>

      {/* Rating */}
      <div className="flex items-center justify-center gap-1 mb-4">
        {Array.from({ length: 5 }).map((_, i) => (
          <Star
            key={i}
            className="w-3.5 h-3.5"
            style={{
              fill: i < Math.floor(pro.rating) ? tokens.colors.primary : "none",
              color: i < Math.floor(pro.rating) ? tokens.colors.primary : tokens.colors.textMuted,
            }}
          />
        ))}
        <span className="ml-1 text-xs font-medium" style={{ color: tokens.colors.textSecondary }}>
          {pro.rating}
        </span>
      </div>

      {/* Social Links */}
      {pro.socialLinks && pro.socialLinks.length > 0 && (
        <div className="flex items-center justify-center gap-3">
          {pro.socialLinks.map((link) => (
            <a
              key={link.platform}
              href={link.url}
              target="_blank"
              rel="noopener noreferrer"
              className="w-9 h-9 flex items-center justify-center rounded-full border transition-all duration-300 hover:scale-110"
              style={{ borderColor: tokens.colors.borderLight, color: tokens.colors.textMuted }}
              aria-label={`${pro.name} no ${link.platform}`}
            >
              {link.platform === "instagram" && <Instagram className="w-4 h-4" />}
              {link.platform === "whatsapp" && <MessageCircle className="w-4 h-4" />}
            </a>
          ))}
        </div>
      )}
    </motion.article>
  );
}

export function Professionals({ title, subtitle, team }: ProfessionalsProps) {
  return (
    <section
      style={{ backgroundColor: tokens.colors.surface, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }}
      aria-labelledby="professionals-title"
    >
      <div className="max-w-[1400px] mx-auto px-6 md:px-12">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6 }}
          className="mb-16 text-center"
        >
          <span
            className="inline-block mb-4 text-sm font-semibold tracking-widest uppercase"
            style={{ color: tokens.colors.primary, fontFamily: tokens.typography.bodyFont }}
          >
            Equipe
          </span>
          <h2
            id="professionals-title"
            style={{
              fontFamily: tokens.typography.headingFont,
              fontSize: tokens.typography.scale.h2,
              fontWeight: tokens.typography.weight.bold,
              color: tokens.colors.text,
              letterSpacing: tokens.typography.letterSpacing.normal,
            }}
          >
            {title}
          </h2>
          {subtitle && (
            <p className="mt-4 max-w-xl mx-auto" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>
              {subtitle}
            </p>
          )}
        </motion.div>

        {/* Grid */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8 md:gap-12">
          {team.map((pro, i) => (
            <ProfessionalCard key={pro.id || i} pro={pro} index={i} />
          ))}
        </div>
      </div>
    </section>
  );
}
