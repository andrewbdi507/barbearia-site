// ============================================================
// MODERN Theme — Gallery
// ============================================================

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Expand, X, ChevronLeft, ChevronRight } from "lucide-react";
import type { GalleryProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function Gallery({ title, subtitle, images }: GalleryProps) {
  const [sel, setSel] = useState<number | null>(null);
  return (
    <section style={{ backgroundColor: tokens.colors.background, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="modern-gallery-title">
      <div className="max-w-[1400px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.5 }} className="mb-16 text-center">
          <span className="inline-block mb-4 text-xs font-semibold tracking-widest uppercase" style={{ color: tokens.colors.primary, fontFamily: tokens.typography.bodyFont }}>Galeria</span>
          <h2 id="modern-gallery-title" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text }}>{title}</h2>
          {subtitle && <p className="mt-4 max-w-lg mx-auto" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{subtitle}</p>}
        </motion.div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
          {images.map((img, i) => (
            <motion.div key={img.id || i} initial={{ opacity: 0, scale: 0.95 }} whileInView={{ opacity: 1, scale: 1 }} viewport={{ once: true }} transition={{ duration: 0.3, delay: i * 0.03 }} className="group relative aspect-square overflow-hidden cursor-pointer" style={{ borderRadius: tokens.borderRadius.lg }} onClick={() => setSel(i)}>
              <img src={img.src} alt={img.alt} className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" loading="lazy" decoding="async" />
              <div className="absolute inset-0 bg-black/0 group-hover:bg-black/30 transition-all duration-300 flex items-center justify-center"><Expand className="w-6 h-6 text-white opacity-0 group-hover:opacity-100 transition-all duration-300 scale-50 group-hover:scale-100" /></div>
            </motion.div>
          ))}
        </div>
      </div>
      <AnimatePresence>{sel !== null && <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/95 backdrop-blur-xl" onClick={() => setSel(null)}>
        <button onClick={() => setSel(null)} className="absolute top-6 right-6 z-10 w-10 h-10 flex items-center justify-center rounded-full border" style={{ borderColor: tokens.colors.border, color: tokens.colors.text }} aria-label="Fechar"><X className="w-5 h-5" /></button>
        <button onClick={(e) => { e.stopPropagation(); setSel((p) => (p !== null ? (p - 1 + images.length) % images.length : 0)); }} className="absolute left-4 z-10 w-12 h-12 flex items-center justify-center rounded-full border" style={{ borderColor: tokens.colors.border, color: tokens.colors.text }} aria-label="Anterior"><ChevronLeft className="w-5 h-5" /></button>
        <motion.img key={sel} initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0 }} src={images[sel].src} alt={images[sel].alt} className="max-w-full max-h-[85vh] object-contain rounded-2xl" onClick={(e) => e.stopPropagation()} />
        <button onClick={(e) => { e.stopPropagation(); setSel((p) => (p !== null ? (p + 1) % images.length : 0)); }} className="absolute right-4 z-10 w-12 h-12 flex items-center justify-center rounded-full border" style={{ borderColor: tokens.colors.border, color: tokens.colors.text }} aria-label="Próximo"><ChevronRight className="w-5 h-5" /></button>
      </motion.div>}</AnimatePresence>
    </section>
  );
}
