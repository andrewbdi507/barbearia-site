// ============================================================
// MODERN Theme — Footer
// ============================================================

import { Scissors, Instagram, Facebook, Youtube, ArrowUpRight } from "lucide-react";
import type { FooterProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

const si: Record<string, React.ReactNode> = { instagram: <Instagram className="w-4 h-4" />, facebook: <Facebook className="w-4 h-4" />, youtube: <Youtube className="w-4 h-4" /> };

export function Footer({ brandName, brandLogo, description, links, socialLinks, legalLinks }: FooterProps) {
  const y = new Date().getFullYear();
  return (
    <footer style={{ backgroundColor: tokens.colors.background, paddingTop: tokens.spacing.section, paddingBottom: "2rem", borderTop: `1px solid ${tokens.colors.border}` }}>
      <div className="max-w-[1400px] mx-auto px-6 md:px-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10 pb-12 border-b" style={{ borderColor: tokens.colors.border }}>
          <div><div className="flex items-center gap-2 mb-4">{brandLogo ? <img src={brandLogo} alt={brandName} className="h-8 w-auto" /> : <Scissors className="w-5 h-5" style={{ color: tokens.colors.primary }} />}<span className="text-lg font-bold" style={{ fontFamily: tokens.typography.headingFont, color: tokens.colors.text }}>{brandName}</span></div>
            {description && <p className="text-xs leading-relaxed mb-4" style={{ color: tokens.colors.textMuted, fontFamily: tokens.typography.bodyFont }}>{description}</p>}
            {socialLinks && <div className="flex gap-3">{socialLinks.map((l) => <a key={l.platform} href={l.url} target="_blank" rel="noopener noreferrer" className="w-8 h-8 flex items-center justify-center rounded-full border transition-colors" style={{ borderColor: tokens.colors.border, color: tokens.colors.textMuted }} aria-label={l.platform}>{si[l.platform] || <ArrowUpRight className="w-3.5 h-3.5" />}</a>)}</div>}
          </div>
          {links.map((g, gi) => <div key={g.title}><h4 className="text-xs font-semibold tracking-wider uppercase mb-4" style={{ color: tokens.colors.text }}>{g.title}</h4><ul className="space-y-2.5">{g.items.map((item) => <li key={item.label}><a href={item.href} className="text-xs transition-colors" style={{ color: tokens.colors.textMuted }}>{item.label}</a></li>)}</ul></div>)}
        </div>
        <div className="pt-8 flex flex-col sm:flex-row items-center justify-between gap-4"><p className="text-xs" style={{ color: tokens.colors.textMuted }}>&copy; {y} {brandName}</p>{legalLinks && <div className="flex gap-6">{legalLinks.map((l) => <a key={l.label} href={l.href} className="text-xs" style={{ color: tokens.colors.textMuted }}>{l.label}</a>)}</div>}</div>
      </div>
    </footer>
  );
}
