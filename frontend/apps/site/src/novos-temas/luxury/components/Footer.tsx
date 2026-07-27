// ============================================================
// LUXURY Theme — Footer
// ============================================================

import { motion } from "framer-motion";
import { Scissors, Instagram, Facebook, Youtube, Twitter, ArrowUpRight } from "lucide-react";
import type { FooterProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

const socialIcons: Record<string, React.ReactNode> = { instagram: <Instagram className="w-4 h-4" />, facebook: <Facebook className="w-4 h-4" />, youtube: <Youtube className="w-4 h-4" />, twitter: <Twitter className="w-4 h-4" /> };

export function Footer({ brandName, brandLogo, description, links, socialLinks, legalLinks }: FooterProps) {
  const currentYear = new Date().getFullYear();
  return (
    <footer style={{ backgroundColor: tokens.colors.background, paddingTop: tokens.spacing.section, paddingBottom: "2.5rem" }}>
      <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: "1px", background: `linear-gradient(90deg, transparent, ${tokens.colors.primary}40, transparent)` }} />
      <div className="max-w-[1280px] mx-auto px-6 md:px-12" style={{ position: "relative" }}>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 pb-16" style={{ borderBottom: `1px solid`, borderColor: tokens.colors.borderLight }}>
          <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.6 }} className="lg:col-span-1">
            <div className="flex items-center gap-3 mb-6">
              {brandLogo ? <img src={brandLogo} alt={brandName} className="h-10 w-auto" /> : <div className="w-10 h-10 flex items-center justify-center" style={{ backgroundColor: tokens.colors.primary, color: tokens.colors.textInverse, borderRadius: tokens.borderRadius.sm }}><Scissors className="w-5 h-5" /></div>}
              <span className="text-xl font-bold tracking-wider" style={{ fontFamily: tokens.typography.headingFont, color: tokens.colors.text }}>{brandName}</span>
            </div>
            {description && <p className="text-sm leading-relaxed mb-8" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textMuted, fontWeight: tokens.typography.weight.light }}>{description}</p>}
            {socialLinks && socialLinks.length > 0 && <div className="flex items-center gap-3">{socialLinks.map((link) => <a key={link.platform} href={link.url} target="_blank" rel="noopener noreferrer" className="w-10 h-10 flex items-center justify-center rounded-full border transition-all duration-500 hover:-translate-y-0.5" style={{ borderColor: tokens.colors.border, color: tokens.colors.textMuted }} aria-label={link.platform}>{socialIcons[link.platform] || <ArrowUpRight className="w-4 h-4" />}</a>)}</div>}
          </motion.div>
          {links.map((group, gi) => (
            <motion.div key={group.title} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.6, delay: gi * 0.1 }}>
              <h4 className="text-xs font-bold tracking-[0.2em] uppercase mb-6" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.text }}>{group.title}</h4>
              <ul className="space-y-4">{group.items.map((item) => <li key={item.label}><a href={item.href} className="text-sm transition-colors duration-300" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textMuted, fontWeight: tokens.typography.weight.light }}>{item.label}</a></li>)}</ul>
            </motion.div>
          ))}
        </div>
        <div className="pt-10 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textMuted }}>&copy; {currentYear} {brandName}.</p>
          {legalLinks && legalLinks.length > 0 && <div className="flex items-center gap-8">{legalLinks.map((link) => <a key={link.label} href={link.href} className="text-xs transition-colors" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textMuted }}>{link.label}</a>)}</div>}
        </div>
      </div>
    </footer>
  );
}
