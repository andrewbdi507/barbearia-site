// ============================================================
// URBAN Theme — Contact Section
// Layout split: info à esquerda + mini mapa à direita.
// ============================================================

import { motion } from "framer-motion";
import { MapPin, Phone, Mail, MessageCircle, Clock } from "lucide-react";
import type { ContactProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function Contact({ title, subtitle, info }: ContactProps) {
  return (
    <section
      style={{ backgroundColor: tokens.colors.surface, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }}
      aria-labelledby="contact-title"
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
            Contato
          </span>
          <h2
            id="contact-title"
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
            <p className="mt-4" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>
              {subtitle}
            </p>
          )}
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Left — Info */}
          <motion.div
            initial={{ opacity: 0, x: -40 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, ease: tokens.motion.easing.easeOut }}
            className="space-y-8"
          >
            {info.address && (
              <div className="flex items-start gap-4">
                <div
                  className="w-12 h-12 flex items-center justify-center flex-shrink-0 rounded-full"
                  style={{ backgroundColor: tokens.colors.primaryLight, color: tokens.colors.primary }}
                >
                  <MapPin className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-semibold mb-1" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.text }}>
                    Endereço
                  </h4>
                  <p style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary, lineHeight: tokens.typography.lineHeight.normal }}>
                    {info.address}
                  </p>
                </div>
              </div>
            )}

            {info.phone && (
              <div className="flex items-start gap-4">
                <div
                  className="w-12 h-12 flex items-center justify-center flex-shrink-0 rounded-full"
                  style={{ backgroundColor: tokens.colors.primaryLight, color: tokens.colors.primary }}
                >
                  <Phone className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-semibold mb-1" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.text }}>
                    Telefone
                  </h4>
                  <a
                    href={`tel:${info.phone.replace(/\D/g, "")}`}
                    className="transition-colors hover:underline"
                    style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}
                  >
                    {info.phone}
                  </a>
                </div>
              </div>
            )}

            {info.email && (
              <div className="flex items-start gap-4">
                <div
                  className="w-12 h-12 flex items-center justify-center flex-shrink-0 rounded-full"
                  style={{ backgroundColor: tokens.colors.primaryLight, color: tokens.colors.primary }}
                >
                  <Mail className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-semibold mb-1" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.text }}>
                    E-mail
                  </h4>
                  <a
                    href={`mailto:${info.email}`}
                    className="transition-colors hover:underline"
                    style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}
                  >
                    {info.email}
                  </a>
                </div>
              </div>
            )}

            {info.whatsapp && (
              <a
                href={`https://wa.me/${info.whatsapp.replace(/\D/g, "")}`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-3 px-8 py-4 font-bold transition-all duration-300"
                style={{
                  fontFamily: tokens.typography.bodyFont,
                  backgroundColor: "#25D366",
                  color: "#FFFFFF",
                  letterSpacing: tokens.typography.letterSpacing.normal,
                  boxShadow: tokens.shadows.md,
                }}
              >
                <MessageCircle className="w-5 h-5" />
                Falar no WhatsApp
              </a>
            )}

            {/* Working Hours */}
            {info.workingHours && info.workingHours.length > 0 && (
              <div className="flex items-start gap-4">
                <div
                  className="w-12 h-12 flex items-center justify-center flex-shrink-0 rounded-full"
                  style={{ backgroundColor: tokens.colors.primaryLight, color: tokens.colors.primary }}
                >
                  <Clock className="w-5 h-5" />
                </div>
                <div className="space-y-1">
                  <h4 className="text-sm font-semibold mb-2" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.text }}>
                    Horários
                  </h4>
                  {info.workingHours.map((wh, i) => (
                    <div key={i} className="flex gap-4 text-sm" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>
                      <span className="w-20 font-medium" style={{ color: tokens.colors.text }}>{wh.day}</span>
                      <span>{wh.hours}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </motion.div>

          {/* Right — Map */}
          <motion.div
            initial={{ opacity: 0, x: 40 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2, ease: tokens.motion.easing.easeOut }}
            className="relative overflow-hidden border min-h-[400px]"
            style={{ borderColor: tokens.colors.border, borderRadius: tokens.borderRadius.lg }}
          >
            {info.mapEmbedUrl ? (
              <iframe
                src={info.mapEmbedUrl}
                width="100%"
                height="100%"
                className="absolute inset-0"
                style={{ border: "none" }}
                allowFullScreen
                loading="lazy"
                referrerPolicy="no-referrer-when-downgrade"
                title="Localização"
              />
            ) : (
              <div
                className="absolute inset-0 flex items-center justify-center"
                style={{ backgroundColor: tokens.colors.surfaceHover, color: tokens.colors.textMuted }}
              >
                <div className="text-center">
                  <MapPin className="w-12 h-12 mx-auto mb-3 opacity-30" />
                  <span className="text-sm">Mapa indisponível</span>
                </div>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </section>
  );
}
