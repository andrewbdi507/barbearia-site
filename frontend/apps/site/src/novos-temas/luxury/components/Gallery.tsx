// ============================================================
// LUXURY Theme — Gallery Section
// Grid elegante 4-colunas com hover reveal.
// ============================================================

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Expand, X, ChevronLeft, ChevronRight } from "lucide-react";
import type { GalleryProps } from "../../shared/types";
import { tokens } from "../constants/tokens";

export function Gallery({ title, subtitle, images }: GalleryProps) {
  const [selectedIdx, setSelectedIdx] = useState<number | null>(null);
  const next = () => setSelectedIdx((prev) => (prev !== null ? (prev + 1) % images.length : 0));
  const prev = () => setSelectedIdx((prev) => (prev !== null ? (prev - 1 + images.length) % images.length : 0));

  return (
    <section style={{ backgroundColor: tokens.colors.background, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="luxury-gallery-title">
      <div className="max-w-[1280px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.8 }} className="mb-20 text-center">
          <span className="inline-block mb-6 text-xs font-semibold tracking-[0.3em] uppercase" style={{ color: tokens.colors.primary, fontFamily: tokens.typography.bodyFont }}>Galeria</span>
          <h2 id="luxury-gallery-title" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.bold, color: tokens.colors.text }}>{title}</h2>
          {subtitle && <p className="mt-6 max-w-lg mx-auto italic" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary, fontWeight: tokens.typography.weight.light }}>{subtitle}</p>}
        </motion.div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
          {images.map((img, i) => (
            <motion.div key={img.id || i} initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} viewport={{ once: true }} transition={{ duration: 0.5, delay: i * 0.05 }} className="group relative aspect-square overflow-hidden cursor-pointer" onClick={() => setSelectedIdx(i)}>
              <img src={img.src} alt={img.alt} className="w-full h-full object-cover transition-transform duration-1000 group-hover:scale-110" loading="lazy" decoding="async" />
              <div className="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition-all duration-500 flex items-center justify-center">
                <Expand className="w-6 h-6 text-white opacity-0 group-hover:opacity-100 transition-all duration-500 scale-50 group-hover:scale-100" />
              </div>
            </motion.div>
          ))}
        </div>
      </div>
      <AnimatePresence>
        {selectedIdx !== null && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/95" onClick={() => setSelectedIdx(null)}>
            <button onClick={() => setSelectedIdx(null)} className="absolute top-6 right-6 z-10 w-12 h-12 flex items-center justify-center rounded-full border" style={{ borderColor: tokens.colors.border, color: tokens.colors.text }} aria-label="Fechar"><X className="w-6 h-6" /></button>
            <button onClick={(e) => { e.stopPropagation(); prev(); }} className="absolute left-4 md:left-10 z-10 w-14 h-14 flex items-center justify-center rounded-full" style={{ backgroundColor: tokens.colors.surface, color: tokens.colors.text }} aria-label="Anterior"><ChevronLeft className="w-6 h-6" /></button>
            <motion.img key={selectedIdx} initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.95 }} src={images[selectedIdx].src} alt={images[selectedIdx].alt} className="max-w-full max-h-[85vh] object-contain" onClick={(e) => e.stopPropagation()} />
            <button onClick={(e) => { e.stopPropagation(); next(); }} className="absolute right-4 md:right-10 z-10 w-14 h-14 flex items-center justify-center rounded-full" style={{ backgroundColor: tokens.colors.surface, color: tokens.colors.text }} aria-label="Próximo"><ChevronRight className="w-6 h-6" /></button>
          </motion.div>
        )}
      </AnimatePresence>
    </section>
  );
}
