// ============================================================
// CLASSIC Theme — FAQ
// ============================================================

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown } from "lucide-react";
import type { FAQProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function FAQ({ title, subtitle, items }: FAQProps) {
  const [open, setOpen] = useState<string | null>(null);
  return (
    <section style={{ backgroundColor: tokens.colors.surfaceAlt, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="classic-faq-title">
      <div className="max-w-[800px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.6 }} className="mb-16 text-center">
          <span className="inline-block mb-4 text-xs tracking-[0.25em] uppercase" style={{ color: tokens.colors.secondary, fontFamily: tokens.typography.bodyFont }}>FAQ</span>
          <h2 id="classic-faq-title" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text }}>{title}</h2>
          {subtitle && <p className="mt-4 italic" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{subtitle}</p>}
        </motion.div>
        <div className="space-y-3">
          {items.map((item, i) => {
            const isO = open === item.id;
            return (
              <motion.div key={item.id || i} initial={{ opacity: 0, y: 15 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: i * 0.04 }} className="border overflow-hidden" style={{ borderColor: isO ? tokens.colors.primary : tokens.colors.borderLight, backgroundColor: tokens.colors.surface, borderRadius: tokens.borderRadius.md }}>
                <button onClick={() => setOpen((pv) => (pv === item.id ? null : item.id))} className="w-full flex items-center justify-between gap-4 px-6 py-5 text-left" aria-expanded={isO}>
                  <span className="text-sm font-medium" style={{ fontFamily: tokens.typography.bodyFont, color: isO ? tokens.colors.primary : tokens.colors.text }}>{item.question}</span>
                  <motion.span animate={{ rotate: isO ? 180 : 0 }} transition={{ duration: 0.3 }}><ChevronDown className="w-4 h-4" style={{ color: tokens.colors.secondary }} /></motion.span>
                </button>
                <AnimatePresence initial={false}>{isO && <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: "auto", opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.35 }} className="overflow-hidden"><p className="px-6 pb-5 text-sm leading-relaxed" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{item.answer}</p></motion.div>}</AnimatePresence>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
