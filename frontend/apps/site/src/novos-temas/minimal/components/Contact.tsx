// ============================================================
// MINIMAL Theme — Contact
// ============================================================

import { motion } from "framer-motion";
import { MapPin, Phone, Mail, MessageCircle } from "lucide-react";
import type { ContactProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function Contact({ title, subtitle, info }: ContactProps) {
  return (
    <section style={{ backgroundColor: tokens.colors.surface, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="minimal-contact-title">
      <div className="max-w-[1200px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.5 }} className="mb-14">
          <span className="inline-block mb-3 text-xs font-medium tracking-wider uppercase" style={{ color: tokens.colors.textMuted, fontFamily: tokens.typography.bodyFont }}>Contato</span>
          <h2 id="minimal-contact-title" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.semibold, color: tokens.colors.text }}>{title}</h2>
          {subtitle && <p className="mt-3 max-w-lg" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{subtitle}</p>}
        </motion.div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div className="space-y-8">
            {info.address && <InfoRow icon={<MapPin className="w-5 h-5" />} label="Endereço" value={info.address} />}
            {info.phone && <InfoRow icon={<Phone className="w-5 h-5" />} label="Telefone" value={info.phone} href={`tel:${info.phone.replace(/\D/g, "")}`} />}
            {info.email && <InfoRow icon={<Mail className="w-5 h-5" />} label="E-mail" value={info.email} href={`mailto:${info.email}`} />}
            {info.whatsapp && <a href={`https://wa.me/${info.whatsapp.replace(/\D/g, "")}`} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 px-6 py-3 text-sm font-medium transition-all duration-300" style={{ fontFamily: tokens.typography.bodyFont, backgroundColor: "#25D366", color: "#FFF", borderRadius: tokens.borderRadius.md }}><MessageCircle className="w-4 h-4" /> WhatsApp</a>}
          </div>
          <div className="min-h-[350px] border overflow-hidden" style={{ borderColor: tokens.colors.borderLight, borderRadius: tokens.borderRadius.lg }}>
            {info.mapEmbedUrl ? <iframe src={info.mapEmbedUrl} width="100%" height="100%" className="border-0" allowFullScreen loading="lazy" title="Mapa" /> : <div className="w-full h-full flex items-center justify-center" style={{ backgroundColor: tokens.colors.surfaceAlt, color: tokens.colors.textMuted }}><MapPin className="w-10 h-10 opacity-20" /></div>}
          </div>
        </div>
      </div>
    </section>
  );
}

function InfoRow({ icon, label, value, href }: { icon: React.ReactNode; label: string; value: string; href?: string }) {
  return <div className="flex items-start gap-4"><div className="w-10 h-10 flex items-center justify-center flex-shrink-0 rounded-full" style={{ backgroundColor: tokens.colors.surfaceAlt, color: tokens.colors.text }}>{icon}</div><div><h4 className="text-xs font-medium mb-1" style={{ color: tokens.colors.textMuted }}>{label}</h4>{href ? <a href={href} className="text-sm transition-colors hover:underline" style={{ color: tokens.colors.textSecondary }}>{value}</a> : <p className="text-sm" style={{ color: tokens.colors.textSecondary }}>{value}</p>}</div></div>;
}
