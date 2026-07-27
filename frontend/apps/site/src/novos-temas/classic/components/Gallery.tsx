// ============================================================
// CLASSIC Theme — Gallery
// ============================================================

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Expand, X, ChevronLeft, ChevronRight } from "lucide-react";
import type { GalleryProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function Gallery({ title, subtitle, images }: GalleryProps) {
  const [sel, setSel] = useState<number | null>(null);
  const n = () => setSel((p) => (p !== null ? (p + 1) % images.length : 0));
  const p = () => setSel((p) => (p !== null ? (p - 1 + images.length) % images.length : 0));
  return (
    <section style={{ backgroundColor: tokens.colors.surfaceAlt, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="classic-gallery-title">
      <div className="max-w-[1280px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.6 }} className="mb-16 text-center">
          <span className="inline-block mb-4 text-xs tracking-[0.25em] uppercase" style={{ color: tokens.colors.secondary, fontFamily: tokens.typography.bodyFont }}>Galeria</span>
          <h2 id="classic-gallery-title" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text }}>{title}</h2>
          {subtitle && <p className="mt-4 max-w-lg mx-auto italic" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{subtitle}</p>}
        </motion.div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
          {images.map((img, i) => (
            <motion.div key={img.id || i} initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} viewport={{ once: true }} transition={{ duration: 0.4, delay: i * 0.04 }} className="group relative aspect-square overflow-hidden cursor-pointer border" style={{ borderColor: tokens.colors.borderLight }} onClick={() => setSel(i)}>
              <img src={img.src} alt={img.alt} className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" loading="lazy" decoding="async" />
              <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-all duration-500 flex items-center justify-center"><Expand className="w-6 h-6 text-white opacity-0 group-hover:opacity-100 transition-all duration-500 scale-50 group-hover:scale-100" /></div>
            </motion.div>
          ))}
        </div>
      </div>
      <AnimatePresence>{sel !== null && <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="fixed inset-0 z-[100] flex items-center justify-center p-4" style={{ backgroundColor: "rgba(251,247,240,0.98)" }} onClick={() => setSel(null)}>
        <button onClick={() => setSel(null)} className="absolute top-6 right-6 z-10 w-12 h-12 flex items-center justify-center rounded-full" style={{ backgroundColor: tokens.colors.surface, color: tokens.colors.text, boxShadow: tokens.shadows.sm }} aria-label="Fechar"><X className="w-5 h-5" /></button>
        <button onClick={(e) => { e.stopPropagation(); p(); }} className="absolute left-4 z-10 w-12 h-12 flex items-center justify-center rounded-full" style={{ backgroundColor: tokens.colors.surface, color: tokens.colors.text, boxShadow: tokens.shadows.sm }} aria-label="Anterior"><ChevronLeft className="w-5 h-5" /></button>
        <motion.img key={sel} initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0 }} src={images[sel].src} alt={images[sel].alt} className="max-w-full max-h-[85vh] object-contain" onClick={(e) => e.stopPropagation()} />
        <button onClick={(e) => { e.stopPropagation(); n(); }} className="absolute right-4 z-10 w-12 h-12 flex items-center justify-center rounded-full" style={{ backgroundColor: tokens.colors.surface, color: tokens.colors.text, boxShadow: tokens.shadows.sm }} aria-label="Próximo"><ChevronRight className="w-5 h-5" /></button>
      </motion.div>}</AnimatePresence>
    </section>
  );
}
