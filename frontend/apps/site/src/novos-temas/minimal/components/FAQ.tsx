// ============================================================
// MINIMAL Theme — FAQ
// ============================================================

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown } from "lucide-react";
import type { FAQProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function FAQ({ title, subtitle, items }: FAQProps) {
  const [openId, setOpenId] = useState<string | null>(null);
  return (
    <section style={{ backgroundColor: tokens.colors.surface, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="minimal-faq-title">
      <div className="max-w-[720px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.5 }} className="mb-14">
          <span className="inline-block mb-3 text-xs font-medium tracking-wider uppercase" style={{ color: tokens.colors.textMuted, fontFamily: tokens.typography.bodyFont }}>FAQ</span>
          <h2 id="minimal-faq-title" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.semibold, color: tokens.colors.text }}>{title}</h2>
          {subtitle && <p className="mt-3" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{subtitle}</p>}
        </motion.div>
        <div className="divide-y" style={{ borderColor: tokens.colors.borderLight }}>
          {items.map((item, i) => {
            const isOpen = openId === item.id;
            return (
              <div key={item.id || i}>
                <button onClick={() => setOpenId((prev) => (prev === item.id ? null : item.id))} className="w-full flex items-center justify-between gap-4 py-5 text-left" aria-expanded={isOpen}>
                  <span className="text-sm font-medium" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.text }}>{item.question}</span>
                  <motion.span animate={{ rotate: isOpen ? 180 : 0 }} transition={{ duration: 0.2 }}><ChevronDown className="w-4 h-4" style={{ color: tokens.colors.textMuted }} /></motion.span>
                </button>
                <AnimatePresence initial={false}>{isOpen && <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: "auto", opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.25 }} className="overflow-hidden"><p className="pb-5 text-sm leading-relaxed" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{item.answer}</p></motion.div>}</AnimatePresence>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
