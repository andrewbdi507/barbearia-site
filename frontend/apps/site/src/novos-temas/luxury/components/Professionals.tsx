// ============================================================
// LUXURY Theme — Professionals
// ============================================================

import { motion } from "framer-motion";
import { Star, Instagram, MessageCircle } from "lucide-react";
import type { ProfessionalsProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function Professionals({ title, subtitle, team }: ProfessionalsProps) {
  return (
    <section style={{ backgroundColor: tokens.colors.surface, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="luxury-pros-title">
      <div className="max-w-[1280px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.8 }} className="mb-20 text-center">
          <span className="inline-block mb-6 text-xs font-semibold tracking-[0.3em] uppercase" style={{ color: tokens.colors.primary, fontFamily: tokens.typography.bodyFont }}>Equipe</span>
          <h2 id="luxury-pros-title" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text }}>{title}</h2>
          {subtitle && <p className="mt-6 max-w-lg mx-auto italic" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary, fontWeight: tokens.typography.weight.light }}>{subtitle}</p>}
        </motion.div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-12">
          {team.map((pro, i) => (
            <motion.article key={pro.id || i} initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.6, delay: i * 0.1 }} whileHover={{ y: -4 }} className="group text-center">
              <div className="relative mx-auto mb-6 w-40 h-40 md:w-48 md:h-48 overflow-hidden rounded-full">
                {pro.avatar ? <img src={pro.avatar} alt={pro.name} className="w-full h-full object-cover transition-transform duration-1000 group-hover:scale-105" loading="lazy" /> : <div className="w-full h-full flex items-center justify-center text-4xl font-bold" style={{ backgroundColor: tokens.colors.surfaceHover, color: tokens.colors.primary, fontFamily: tokens.typography.headingFont }}>{pro.name[0]}</div>}
                <div className="absolute inset-0 rounded-full border opacity-0 group-hover:opacity-100 transition-all duration-700" style={{ borderColor: tokens.colors.primary, borderWidth: "1px" }} />
              </div>
              <h3 className="mb-1 text-lg" style={{ fontFamily: tokens.typography.headingFont, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text }}>{pro.name}</h3>
              <p className="mb-3 text-xs tracking-wider uppercase" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textMuted }}>{pro.role}</p>
              <div className="flex items-center justify-center gap-1">
                {Array.from({ length: 5 }).map((_, si) => <Star key={si} className="w-3 h-3" style={{ fill: si < Math.floor(pro.rating) ? tokens.colors.primary : "none", color: si < Math.floor(pro.rating) ? tokens.colors.primary : tokens.colors.textMuted }} />)}
              </div>
              {pro.socialLinks && pro.socialLinks.length > 0 && (
                <div className="flex items-center justify-center gap-3 mt-4">
                  {pro.socialLinks.map((link) => (
                    <a key={link.platform} href={link.url} target="_blank" rel="noopener noreferrer" className="w-9 h-9 flex items-center justify-center rounded-full border transition-all duration-300 hover:scale-110" style={{ borderColor: tokens.colors.borderLight, color: tokens.colors.textMuted }} aria-label={`${pro.name} no ${link.platform}`}>
                      {link.platform === "instagram" && <Instagram className="w-4 h-4" />}
                      {link.platform === "whatsapp" && <MessageCircle className="w-4 h-4" />}
                    </a>
                  ))}
                </div>
              )}
            </motion.article>
          ))}
        </div>
      </div>
    </section>
  );
}
