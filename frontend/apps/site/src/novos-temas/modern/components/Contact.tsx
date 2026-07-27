// ============================================================
// MODERN Theme — Contact
// ============================================================

import { motion } from "framer-motion";
import { MapPin, Phone, Mail, MessageCircle } from "lucide-react";
import type { ContactProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function Contact({ title, subtitle, info }: ContactProps) {
  return (
    <section style={{ backgroundColor: tokens.colors.surfaceAlt, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="modern-contact-title">
      <div className="max-w-[1400px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.5 }} className="mb-16 text-center">
          <span className="inline-block mb-4 text-xs font-semibold tracking-widest uppercase" style={{ color: tokens.colors.primary, fontFamily: tokens.typography.bodyFont }}>Contato</span>
          <h2 id="modern-contact-title" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text }}>{title}</h2>
          {subtitle && <p className="mt-4 max-w-lg mx-auto" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{subtitle}</p>}
        </motion.div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div className="space-y-8">
            {info.address && <Ci i={<MapPin className="w-5 h-5" />} l="Endereço" v={info.address} />}
            {info.phone && <Ci i={<Phone className="w-5 h-5" />} l="Telefone" v={info.phone} h={`tel:${info.phone.replace(/\D/g, "")}`} />}
            {info.email && <Ci i={<Mail className="w-5 h-5" />} l="E-mail" v={info.email} h={`mailto:${info.email}`} />}
            {info.whatsapp && <a href={`https://wa.me/${info.whatsapp.replace(/\D/g, "")}`} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 px-6 py-3 text-sm font-semibold transition-all duration-300 rounded-full" style={{ backgroundColor: "#25D366", color: "#FFF", fontFamily: tokens.typography.bodyFont }}><MessageCircle className="w-4 h-4" /> WhatsApp</a>}
          </div>
          <div className="min-h-[350px] border overflow-hidden" style={{ borderColor: tokens.colors.border, borderRadius: tokens.borderRadius.xl }}>{info.mapEmbedUrl ? <iframe src={info.mapEmbedUrl} width="100%" height="100%" className="border-0" allowFullScreen loading="lazy" title="Mapa" /> : <div className="w-full h-full flex items-center justify-center" style={{ backgroundColor: tokens.colors.surface, color: tokens.colors.textMuted }}><MapPin className="w-10 h-10 opacity-20" /></div>}</div>
        </div>
      </div>
    </section>
  );
}

function Ci({ i, l, v, h }: { i: React.ReactNode; l: string; v: string; h?: string }) {
  return <div className="flex items-start gap-4"><div className="w-10 h-10 flex items-center justify-center rounded-2xl flex-shrink-0" style={{ background: `linear-gradient(135deg, ${tokens.colors.primaryLight}, ${tokens.colors.primaryLight})`, color: tokens.colors.primary }}>{i}</div><div><h4 className="text-xs font-semibold mb-1" style={{ color: tokens.colors.textMuted }}>{l}</h4>{h ? <a href={h} className="text-sm hover:underline" style={{ color: tokens.colors.textSecondary }}>{v}</a> : <p className="text-sm" style={{ color: tokens.colors.textSecondary }}>{v}</p>}</div></div>;
}
