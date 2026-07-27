// ============================================================
// LUXURY Theme — Contact Section
// ============================================================

import { motion } from "framer-motion";
import { MapPin, Phone, Mail, MessageCircle } from "lucide-react";
import type { ContactProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function Contact({ title, subtitle, info }: ContactProps) {
  return (
    <section style={{ backgroundColor: tokens.colors.surface, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="luxury-contact-title">
      <div className="max-w-[1280px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.8 }} className="mb-20 text-center">
          <span className="inline-block mb-6 text-xs font-semibold tracking-[0.3em] uppercase" style={{ color: tokens.colors.primary, fontFamily: tokens.typography.bodyFont }}>Contato</span>
          <h2 id="luxury-contact-title" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text }}>{title}</h2>
          {subtitle && <p className="mt-6 max-w-lg mx-auto italic" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary, fontWeight: tokens.typography.weight.light }}>{subtitle}</p>}
        </motion.div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16">
          <motion.div initial={{ opacity: 0, x: -40 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} transition={{ duration: 0.8 }} className="space-y-10">
            {info.address && <InfoItem icon={<MapPin className="w-5 h-5" />} label="Endereço" value={info.address} />}
            {info.phone && <InfoItem icon={<Phone className="w-5 h-5" />} label="Telefone" value={info.phone} href={`tel:${info.phone.replace(/\D/g, "")}`} />}
            {info.email && <InfoItem icon={<Mail className="w-5 h-5" />} label="E-mail" value={info.email} href={`mailto:${info.email}`} />}
            {info.whatsapp && (
              <a href={`https://wa.me/${info.whatsapp.replace(/\D/g, "")}`} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-3 px-8 py-4 font-semibold tracking-wider uppercase transition-all duration-500" style={{ fontFamily: tokens.typography.bodyFont, backgroundColor: "#25D366", color: "#FFF", letterSpacing: tokens.typography.letterSpacing.wide }}>
                <MessageCircle className="w-5 h-5" /> WhatsApp
              </a>
            )}
          </motion.div>
          <motion.div initial={{ opacity: 0, x: 40 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} transition={{ duration: 0.8, delay: 0.2 }} className="relative min-h-[400px] border overflow-hidden" style={{ borderColor: tokens.colors.border, borderRadius: tokens.borderRadius.lg }}>
            {info.mapEmbedUrl ? <iframe src={info.mapEmbedUrl} width="100%" height="100%" className="absolute inset-0" style={{ border: "none" }} allowFullScreen loading="lazy" title="Localização" /> : <div className="absolute inset-0 flex items-center justify-center" style={{ backgroundColor: tokens.colors.surfaceHover, color: tokens.colors.textMuted }}><MapPin className="w-12 h-12 mx-auto mb-3 opacity-20" /></div>}
          </motion.div>
        </div>
      </div>
    </section>
  );
}

function InfoItem({ icon, label, value, href }: { icon: React.ReactNode; label: string; value: string; href?: string }) {
  return (
    <div className="flex items-start gap-5">
      <div className="w-12 h-12 flex items-center justify-center flex-shrink-0 rounded-full" style={{ backgroundColor: tokens.colors.primaryLight, color: tokens.colors.primary }}>{icon}</div>
      <div>
        <h4 className="text-xs font-semibold tracking-[0.2em] uppercase mb-2" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.text }}>{label}</h4>
        {href ? <a href={href} className="text-base transition-colors hover:underline" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary, fontWeight: tokens.typography.weight.light }}>{value}</a> : <p className="text-base" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary, fontWeight: tokens.typography.weight.light }}>{value}</p>}
      </div>
    </div>
  );
}
