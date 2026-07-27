// ============================================================
// URBAN Theme — Testimonials Section
// Carrossel horizontal com cards de depoimentos e glassmorphism.
// ============================================================

import { motion } from "framer-motion";
import { Star, Quote } from "lucide-react";
import type { TestimonialsProps, Testimonial } from "../../shared/types";
import { tokens } from "../constants/tokens";

function TestimonialCard({ testimonial, index }: { testimonial: Testimonial; index: number }) {
  return (
    <motion.article
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-50px" }}
      transition={{ duration: 0.5, delay: index * 0.08, ease: tokens.motion.easing.easeOut }}
      className="relative p-8 border flex flex-col"
      style={{
        backgroundColor: tokens.colors.surface,
        borderColor: tokens.colors.borderLight,
        ...(tokens.glassmorphism.enabled
          ? { backdropFilter: `blur(${tokens.glassmorphism.blur})` }
          : {}),
      }}
    >
      {/* Quote Icon */}
      <Quote className="absolute top-6 right-6 w-10 h-10 opacity-10" style={{ color: tokens.colors.primary }} />

      {/* Rating */}
      <div className="flex items-center gap-1 mb-4">
        {Array.from({ length: 5 }).map((_, i) => (
          <Star
            key={i}
            className="w-4 h-4"
            style={{
              fill: i < testimonial.rating ? tokens.colors.primary : "none",
              color: i < testimonial.rating ? tokens.colors.primary : tokens.colors.textMuted,
            }}
          />
        ))}
      </div>

      {/* Text */}
      <blockquote
        className="mb-6 flex-1 text-base leading-relaxed italic"
        style={{
          fontFamily: tokens.typography.bodyFont,
          color: tokens.colors.textSecondary,
          lineHeight: tokens.typography.lineHeight.relaxed,
        }}
      >
        &ldquo;{testimonial.text}&rdquo;
      </blockquote>

      {/* Author */}
      <div className="flex items-center gap-3 pt-4 border-t" style={{ borderColor: tokens.colors.borderLight }}>
        <div
          className="w-11 h-11 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0"
          style={{
            backgroundColor: tokens.colors.primaryLight,
            color: tokens.colors.primary,
            fontFamily: tokens.typography.headingFont,
          }}
        >
          {testimonial.avatar ? (
            <img src={testimonial.avatar} alt={testimonial.name} className="w-full h-full rounded-full object-cover" />
          ) : (
            testimonial.name[0]
          )}
        </div>
        <div>
          <div className="text-sm font-semibold" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.text }}>
            {testimonial.name}
          </div>
          {testimonial.service && (
            <div className="text-xs" style={{ color: tokens.colors.textMuted }}>
              {testimonial.service}
            </div>
          )}
        </div>
      </div>
    </motion.article>
  );
}

export function Testimonials({ title, subtitle, testimonials }: TestimonialsProps) {
  return (
    <section
      style={{ backgroundColor: tokens.colors.background, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }}
      aria-labelledby="testimonials-title"
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
            Depoimentos
          </span>
          <h2
            id="testimonials-title"
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
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {testimonials.map((t, i) => (
            <TestimonialCard key={t.id || i} testimonial={t} index={i} />
          ))}
        </div>

        {/* Average Rating Summary */}
        {testimonials.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="mt-12 text-center"
          >
            <div className="inline-flex items-center gap-6 px-8 py-4 border" style={{ borderColor: tokens.colors.borderLight }}>
              <div className="text-center">
                <div className="text-3xl font-bold" style={{ fontFamily: tokens.typography.headingFont, color: tokens.colors.text }}>
                  {(testimonials.reduce((acc, t) => acc + t.rating, 0) / testimonials.length).toFixed(1)}
                </div>
                <div className="text-xs" style={{ color: tokens.colors.textMuted }}>Média</div>
              </div>
              <div className="w-px h-10" style={{ backgroundColor: tokens.colors.border }} />
              <div className="text-center">
                <div className="text-3xl font-bold" style={{ fontFamily: tokens.typography.headingFont, color: tokens.colors.text }}>
                  {testimonials.length}+
                </div>
                <div className="text-xs" style={{ color: tokens.colors.textMuted }}>Avaliações</div>
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </section>
  );
}
