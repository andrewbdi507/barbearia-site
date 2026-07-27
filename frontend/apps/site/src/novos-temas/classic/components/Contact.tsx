// ============================================================
// CLASSIC Theme — Contact
// ============================================================

import { motion } from "framer-motion";
import { MapPin, Phone, Mail, MessageCircle } from "lucide-react";
import type { ContactProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function Contact({ title, subtitle, info }: ContactProps) {
  return (
    <section style={{ backgroundColor: tokens.colors.surfaceAlt, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="classic-contact-title">
      <div className="max-w-[1280px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.6 }} className="mb-16 text-center">
          <span className="inline-block mb-4 text-xs tracking-[0.25em] uppercase" style={{ color: tokens.colors.secondary, fontFamily: tokens.typography.bodyFont }}>Contato</span>
          <h2 id="classic-contact-title" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text }}>{title}</h2>
          {subtitle && <p className="mt-4 max-w-lg mx-auto italic" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{subtitle}</p>}
        </motion.div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div className="space-y-8">
            {info.address && <CItem i={<MapPin className="w-5 h-5" />} l="Endereço" v={info.address} />}
            {info.phone && <CItem i={<Phone className="w-5 h-5" />} l="Telefone" v={info.phone} h={`tel:${info.phone.replace(/\D/g, "")}`} />}
            {info.email && <CItem i={<Mail className="w-5 h-5" />} l="E-mail" v={info.email} h={`mailto:${info.email}`} />}
            {info.whatsapp && <a href={`https://wa.me/${info.whatsapp.replace(/\D/g, "")}`} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 px-6 py-3 text-sm font-medium transition-all duration-300" style={{ backgroundColor: "#25D366", color: "#FFF", borderRadius: tokens.borderRadius.md, fontFamily: tokens.typography.bodyFont }}><MessageCircle className="w-4 h-4" /> WhatsApp</a>}
          </div>
          <div className="min-h-[350px] border overflow-hidden" style={{ borderColor: tokens.colors.border, borderRadius: tokens.borderRadius.lg }}>{info.mapEmbedUrl ? <iframe src={info.mapEmbedUrl} width="100%" height="100%" className="border-0" allowFullScreen loading="lazy" title="Mapa" /> : <div className="w-full h-full flex items-center justify-center" style={{ backgroundColor: tokens.colors.surface, color: tokens.colors.textMuted }}><MapPin className="w-10 h-10 opacity-20" /></div>}</div>
        </div>
      </div>
    </section>
  );
}

function CItem({ i, l, v, h }: { i: React.ReactNode; l: string; v: string; h?: string }) {
  return <div className="flex items-start gap-4"><div className="w-10 h-10 flex items-center justify-center rounded-full flex-shrink-0" style={{ backgroundColor: tokens.colors.primaryLight, color: tokens.colors.primary }}>{i}</div><div><h4 className="text-xs font-semibold tracking-wider uppercase mb-1" style={{ color: tokens.colors.text }}>{l}</h4>{h ? <a href={h} className="text-sm hover:underline" style={{ color: tokens.colors.textSecondary }}>{v}</a> : <p className="text-sm" style={{ color: tokens.colors.textSecondary }}>{v}</p>}</div></div>;
}
