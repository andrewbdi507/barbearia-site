// ============================================================
// URBAN Theme — Footer Section
// Footer escuro com grid de links, branding e copyright.
// ============================================================

import { motion } from "framer-motion";
import { Scissors, Instagram, Facebook, Youtube, Twitter, ArrowUpRight } from "lucide-react";
import type { FooterProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

const socialIcons: Record<string, React.ReactNode> = {
  instagram: <Instagram className="w-5 h-5" />,
  facebook: <Facebook className="w-5 h-5" />,
  youtube: <Youtube className="w-5 h-5" />,
  twitter: <Twitter className="w-5 h-5" />,
};

export function Footer({ brandName, brandLogo, description, links, socialLinks, legalLinks }: FooterProps) {
  const currentYear = new Date().getFullYear();

  return (
    <footer
      className="relative overflow-hidden"
      style={{ backgroundColor: tokens.colors.background, paddingTop: tokens.spacing.section, paddingBottom: "2rem" }}
    >
      {/* Top accent line */}
      <div className="absolute top-0 left-0 right-0 h-px" style={{ backgroundColor: tokens.colors.border }} />

      <div className="max-w-[1400px] mx-auto px-6 md:px-12">
        {/* Main Footer Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10 pb-16 border-b" style={{ borderColor: tokens.colors.borderLight }}>
          {/* Brand Column */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="lg:col-span-1"
          >
            <div className="flex items-center gap-3 mb-4">
              {brandLogo ? (
                <img src={brandLogo} alt={brandName} className="h-10 w-auto" />
              ) : (
                <div
                  className="w-10 h-10 flex items-center justify-center"
                  style={{ backgroundColor: tokens.colors.primary, color: tokens.colors.textInverse }}
                >
                  <Scissors className="w-5 h-5" />
                </div>
              )}
              <span
                className="text-xl font-bold tracking-wider"
                style={{ fontFamily: tokens.typography.headingFont, color: tokens.colors.text }}
              >
                {brandName}
              </span>
            </div>
            {description && (
              <p className="text-sm leading-relaxed mb-6" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textMuted }}>
                {description}
              </p>
            )}
            {/* Social Links */}
            {socialLinks && socialLinks.length > 0 && (
              <div className="flex items-center gap-3">
                {socialLinks.map((link) => (
                  <a
                    key={link.platform}
                    href={link.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-10 h-10 flex items-center justify-center rounded-full border transition-all duration-300 hover:scale-110 hover:-translate-y-0.5"
                    style={{ borderColor: tokens.colors.border, color: tokens.colors.textMuted }}
                    aria-label={link.platform}
                  >
                    {socialIcons[link.platform] || <ArrowUpRight className="w-4 h-4" />}
                  </a>
                ))}
              </div>
            )}
          </motion.div>

          {/* Link Columns */}
          {links.map((group, gi) => (
            <motion.div
              key={group.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: gi * 0.1 }}
            >
              <h4
                className="text-sm font-bold tracking-widest uppercase mb-5"
                style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.text }}
              >
                {group.title}
              </h4>
              <ul className="space-y-3">
                {group.items.map((item) => (
                  <li key={item.label}>
                    <a
                      href={item.href}
                      className="text-sm transition-colors duration-200 hover:translate-x-1 inline-block"
                      style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textMuted }}
                    >
                      {item.label}
                    </a>
                  </li>
                ))}
              </ul>
            </motion.div>
          ))}
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textMuted }}>
            &copy; {currentYear} {brandName}. Todos os direitos reservados.
          </p>
          {legalLinks && legalLinks.length > 0 && (
            <div className="flex items-center gap-6">
              {legalLinks.map((link) => (
                <a
                  key={link.label}
                  href={link.href}
                  className="text-xs transition-colors hover:underline"
                  style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textMuted }}
                >
                  {link.label}
                </a>
              ))}
            </div>
          )}
        </div>
      </div>
    </footer>
  );
}
