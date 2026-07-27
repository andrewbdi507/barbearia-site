// ============================================================
// LUXURY Theme — FAQ Section
// ============================================================

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown } from "lucide-react";
import type { FAQProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function FAQ({ title, subtitle, items }: FAQProps) {
  const [openId, setOpenId] = useState<string | null>(null);
  return (
    <section style={{ backgroundColor: tokens.colors.background, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="luxury-faq-title">
      <div className="max-w-[800px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.8 }} className="mb-16 text-center">
          <span className="inline-block mb-6 text-xs font-semibold tracking-[0.3em] uppercase" style={{ color: tokens.colors.primary, fontFamily: tokens.typography.bodyFont }}>FAQ</span>
          <h2 id="luxury-faq-title" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text }}>{title}</h2>
          {subtitle && <p className="mt-6 italic" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary, fontWeight: tokens.typography.weight.light }}>{subtitle}</p>}
        </motion.div>
        <div className="space-y-3">
          {items.map((item, i) => {
            const isOpen = openId === item.id;
            return (
              <motion.div key={item.id || i} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: i * 0.05 }} className="border overflow-hidden transition-all duration-500" style={{ borderColor: isOpen ? tokens.colors.primary : tokens.colors.borderLight, backgroundColor: tokens.colors.surface }}>
                <button onClick={() => setOpenId((prev) => (prev === item.id ? null : item.id))} className="w-full flex items-center justify-between gap-4 px-8 py-6 text-left" aria-expanded={isOpen}>
                  <span className="text-base" style={{ fontFamily: tokens.typography.bodyFont, fontWeight: tokens.typography.weight.medium, color: isOpen ? tokens.colors.primary : tokens.colors.text }}>{item.question}</span>
                  <motion.span animate={{ rotate: isOpen ? 180 : 0 }} transition={{ duration: 0.4 }} style={{ color: tokens.colors.primary }}><ChevronDown className="w-5 h-5" /></motion.span>
                </button>
                <AnimatePresence initial={false}>
                  {isOpen && (
                    <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: "auto", opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.5, ease: [0.25, 0.1, 0.25, 1] }} className="overflow-hidden">
                      <div className="px-8 pb-6 text-base leading-relaxed" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary, fontWeight: tokens.typography.weight.light, lineHeight: tokens.typography.lineHeight.relaxed }}>{item.answer}</div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
