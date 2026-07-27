// ============================================================
// URBAN Theme — Services Section
// Grid de cards com efeito glassmorphism e hover lift.
// ============================================================

import { motion } from "framer-motion";
import { Clock, ArrowRight } from "lucide-react";
import type { ServicesProps, ServiceItem } from "../../shared/types";
import { tokens } from "../constants/tokens";

function ServiceCard({ service, index }: { service: ServiceItem; index: number }) {
  return (
    <motion.article
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-60px" }}
      transition={{ duration: 0.5, delay: index * 0.08, ease: tokens.motion.easing.easeOut }}
      whileHover={{ y: -8, transition: { duration: 0.3 } }}
      className="group relative overflow-hidden p-8 border cursor-pointer transition-all duration-300"
      style={{
        backgroundColor: tokens.colors.surface,
        borderColor: tokens.colors.borderLight,
        ...(tokens.glassmorphism.enabled
          ? {
              backdropFilter: `blur(${tokens.glassmorphism.blur})`,
              background: `rgba(20,20,20,${tokens.glassmorphism.opacity + 0.02})`,
            }
          : {}),
      }}
    >
      {/* Hover gradient reveal */}
      <div
        className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500"
        style={{ background: tokens.colors.gradientCard }}
      />

      {/* Top accent line */}
      <div
        className="absolute top-0 left-6 right-6 h-px opacity-0 group-hover:opacity-100 transition-opacity duration-300"
        style={{ backgroundColor: tokens.colors.primary }}
      />

      <div className="relative z-10">
        {/* Icon */}
        <div
          className="w-14 h-14 mb-6 flex items-center justify-center text-xl transition-all duration-300 group-hover:scale-110"
          style={{ backgroundColor: tokens.colors.primaryLight, color: tokens.colors.primary }}
        >
          {service.icon ? (
            <span dangerouslySetInnerHTML={{ __html: service.icon }} />
          ) : (
            <span style={{ fontFamily: tokens.typography.headingFont, fontWeight: tokens.typography.weight.bold }}>
              {(index + 1).toString().padStart(2, "0")}
            </span>
          )}
        </div>

        {/* Name */}
        <h3
          className="mb-3 transition-colors duration-300"
          style={{
            fontFamily: tokens.typography.headingFont,
            fontSize: tokens.typography.scale.h4,
            fontWeight: tokens.typography.weight.bold,
            color: tokens.colors.text,
            letterSpacing: tokens.typography.letterSpacing.normal,
          }}
        >
          {service.name}
        </h3>

        {/* Description */}
        <p
          className="mb-6 text-sm leading-relaxed"
          style={{
            fontFamily: tokens.typography.bodyFont,
            color: tokens.colors.textSecondary,
            lineHeight: tokens.typography.lineHeight.normal,
          }}
        >
          {service.description}
        </p>

        {/* Footer */}
        <div className="flex items-end justify-between pt-4 border-t" style={{ borderColor: tokens.colors.borderLight }}>
          <div>
            <span
              className="text-2xl font-bold"
              style={{ fontFamily: tokens.typography.headingFont, color: tokens.colors.primary }}
            >
              R$ {service.price.toFixed(0)}
            </span>
          </div>
          <div className="flex items-center gap-1.5 text-xs" style={{ color: tokens.colors.textMuted }}>
            <Clock className="w-3.5 h-3.5" />
            {service.duration} min
          </div>
        </div>
      </div>
    </motion.article>
  );
}

export function Services({ title, subtitle, items }: ServicesProps) {
  return (
    <section
      style={{ backgroundColor: tokens.colors.background, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }}
      aria-labelledby="services-title"
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
            Serviços
          </span>
          <h2
            id="services-title"
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
            <p
              className="mt-4 max-w-xl mx-auto"
              style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}
            >
              {subtitle}
            </p>
          )}
        </motion.div>

        {/* Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {items.map((service, i) => (
            <ServiceCard key={service.id || i} service={service} index={i} />
          ))}
        </div>

        {/* View All Link */}
        {items.length > 3 && (
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="mt-12 text-center"
          >
            <a
              href="/servicos"
              className="group inline-flex items-center gap-2 text-sm font-semibold tracking-wider uppercase transition-colors"
              style={{ color: tokens.colors.primary, fontFamily: tokens.typography.bodyFont }}
            >
              Ver Todos os Serviços
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </a>
          </motion.div>
        )}
      </div>
    </section>
  );
}
