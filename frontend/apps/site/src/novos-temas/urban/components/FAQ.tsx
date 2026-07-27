// ============================================================
// URBAN Theme — FAQ Section
// Accordion com animação de altura e borda neon no item ativo.
// ============================================================

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown } from "lucide-react";
import type { FAQProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function FAQ({ title, subtitle, items }: FAQProps) {
  const [openId, setOpenId] = useState<string | null>(null);

  const toggle = (id: string) => setOpenId((prev) => (prev === id ? null : id));

  return (
    <section
      style={{ backgroundColor: tokens.colors.surface, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }}
      aria-labelledby="faq-title"
    >
      <div className="max-w-[800px] mx-auto px-6 md:px-12">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6 }}
          className="mb-14 text-center"
        >
          <span
            className="inline-block mb-4 text-sm font-semibold tracking-widest uppercase"
            style={{ color: tokens.colors.primary, fontFamily: tokens.typography.bodyFont }}
          >
            FAQ
          </span>
          <h2
            id="faq-title"
            style={{
              fontFamily: tokens.typography.headingFont,
              fontSize: tokens.typography.scale.h2,
              fontWeight: tokens.typography.weight.bold,
              color: tokens.colors.text,
              letterSpacing: tokens.typography.letterSpacing.normal,
            }}
          >
            {title}
          </h2>
          {subtitle && (
            <p className="mt-4" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>
              {subtitle}
            </p>
          )}
        </motion.div>

        {/* Accordion */}
        <div className="space-y-3">
          {items.map((item, i) => {
            const isOpen = openId === item.id;
            return (
              <motion.div
                key={item.id || i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.05, duration: 0.4 }}
                className="border overflow-hidden transition-all duration-300"
                style={{
                  borderColor: isOpen ? tokens.colors.primary : tokens.colors.borderLight,
                  backgroundColor: isOpen ? tokens.colors.surfaceHover : tokens.colors.surface,
                }}
              >
                <button
                  onClick={() => toggle(item.id)}
                  className="w-full flex items-center justify-between gap-4 px-6 py-5 text-left"
                  aria-expanded={isOpen}
                  aria-controls={`faq-answer-${item.id}`}
                >
                  <span
                    className="font-semibold text-base"
                    style={{
                      fontFamily: tokens.typography.bodyFont,
                      color: isOpen ? tokens.colors.primary : tokens.colors.text,
                      transition: "color 0.3s",
                    }}
                  >
                    {item.question}
                  </span>
                  <motion.span
                    animate={{ rotate: isOpen ? 180 : 0 }}
                    transition={{ duration: 0.3 }}
                    style={{ color: isOpen ? tokens.colors.primary : tokens.colors.textMuted }}
                  >
                    <ChevronDown className="w-5 h-5" />
                  </motion.span>
                </button>

                <AnimatePresence initial={false}>
                  {isOpen && (
                    <motion.div
                      id={`faq-answer-${item.id}`}
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.35, ease: [0.25, 0.46, 0.45, 0.94] }}
                      className="overflow-hidden"
                    >
                      <div
                        className="px-6 pb-5 text-base leading-relaxed"
                        style={{
                          fontFamily: tokens.typography.bodyFont,
                          color: tokens.colors.textSecondary,
                          lineHeight: tokens.typography.lineHeight.relaxed,
                        }}
                      >
                        {item.answer}
                      </div>
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
