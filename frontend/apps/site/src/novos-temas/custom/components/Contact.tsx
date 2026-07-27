// ============================================================
// CUSTOM Theme — Contact
// ============================================================

import { motion } from "framer-motion";
import { MapPin, Phone, Mail, MessageCircle } from "lucide-react";
import type { ContactProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function Contact({ title, subtitle, info }: ContactProps) {
  return (
    <section style={{ backgroundColor: tokens.colors.background, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="custom-contact-title">
      <div className="max-w-[1200px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.4 }} className="mb-14 text-center">
          <h2 id="custom-contact-title" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text }}>{title}</h2>
          {subtitle && <p className="mt-3 max-w-lg mx-auto" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{subtitle}</p>}
        </motion.div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
          <div className="space-y-7">
            {info.address && <div className="flex items-start gap-3"><MapPin className="w-5 h-5 flex-shrink-0 mt-0.5" style={{ color: tokens.colors.primary }} /><div><h4 className="text-xs font-semibold mb-1" style={{ color: tokens.colors.textMuted }}>Endereço</h4><p className="text-sm" style={{ color: tokens.colors.textSecondary }}>{info.address}</p></div></div>}
            {info.phone && <div className="flex items-start gap-3"><Phone className="w-5 h-5 flex-shrink-0 mt-0.5" style={{ color: tokens.colors.primary }} /><div><h4 className="text-xs font-semibold mb-1" style={{ color: tokens.colors.textMuted }}>Telefone</h4><a href={`tel:${info.phone.replace(/\D/g, "")}`} className="text-sm" style={{ color: tokens.colors.textSecondary }}>{info.phone}</a></div></div>}
            {info.email && <div className="flex items-start gap-3"><Mail className="w-5 h-5 flex-shrink-0 mt-0.5" style={{ color: tokens.colors.primary }} /><div><h4 className="text-xs font-semibold mb-1" style={{ color: tokens.colors.textMuted }}>E-mail</h4><a href={`mailto:${info.email}`} className="text-sm" style={{ color: tokens.colors.textSecondary }}>{info.email}</a></div></div>}
            {info.whatsapp && <a href={`https://wa.me/${info.whatsapp.replace(/\D/g, "")}`} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 px-6 py-3 text-sm font-medium rounded-lg transition-all" style={{ backgroundColor: "#25D366", color: "#FFF" }}><MessageCircle className="w-4 h-4" /> WhatsApp</a>}
          </div>
          <div className="min-h-[350px] border rounded-xl overflow-hidden" style={{ borderColor: tokens.colors.border }}>{info.mapEmbedUrl ? <iframe src={info.mapEmbedUrl} width="100%" height="100%" className="border-0" allowFullScreen loading="lazy" title="Mapa" /> : <div className="w-full h-full flex items-center justify-center" style={{ backgroundColor: tokens.colors.surfaceAlt, color: tokens.colors.textMuted }}><MapPin className="w-10 h-10 opacity-20" /></div>}</div>
        </div>
      </div>
    </section>
  );
}
