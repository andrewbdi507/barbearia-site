// ============================================================
// MINIMAL Theme — Gallery
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
    <section style={{ backgroundColor: tokens.colors.surface, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }} aria-labelledby="minimal-gallery-title">
      <div className="max-w-[1200px] mx-auto px-6 md:px-12">
        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.5 }} className="mb-14">
          <span className="inline-block mb-3 text-xs font-medium tracking-wider uppercase" style={{ color: tokens.colors.textMuted, fontFamily: tokens.typography.bodyFont }}>Galeria</span>
          <h2 id="minimal-gallery-title" style={{ fontFamily: tokens.typography.headingFont, fontSize: tokens.typography.scale.h2, fontWeight: tokens.typography.weight.semibold, color: tokens.colors.text }}>{title}</h2>
          {subtitle && <p className="mt-3 max-w-lg" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>{subtitle}</p>}
        </motion.div>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-2 md:gap-3">
          {images.map((img, i) => (
            <motion.div key={img.id || i} initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} viewport={{ once: true }} transition={{ duration: 0.3, delay: i * 0.03 }} className="group relative aspect-square overflow-hidden cursor-pointer" onClick={() => setSelectedIdx(i)} style={{ borderRadius: tokens.borderRadius.sm }}>
              <img src={img.src} alt={img.alt} className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-103" loading="lazy" decoding="async" />
              <div className="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-all duration-300 flex items-center justify-center"><Expand className="w-5 h-5 text-white opacity-0 group-hover:opacity-100 transition-all duration-300" /></div>
            </motion.div>
          ))}
        </div>
      </div>
      <AnimatePresence>{selectedIdx !== null && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-white/98" onClick={() => setSelectedIdx(null)}>
          <button onClick={() => setSelectedIdx(null)} className="absolute top-6 right-6 z-10 w-10 h-10 flex items-center justify-center rounded-full" style={{ backgroundColor: tokens.colors.surfaceAlt, color: tokens.colors.text }} aria-label="Fechar"><X className="w-5 h-5" /></button>
          <button onClick={(e) => { e.stopPropagation(); prev(); }} className="absolute left-4 z-10 w-12 h-12 flex items-center justify-center rounded-full" style={{ backgroundColor: tokens.colors.surfaceAlt, color: tokens.colors.text }} aria-label="Anterior"><ChevronLeft className="w-5 h-5" /></button>
          <motion.img key={selectedIdx} initial={{ opacity: 0, scale: 0.98 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0 }} src={images[selectedIdx].src} alt={images[selectedIdx].alt} className="max-w-full max-h-[85vh] object-contain" onClick={(e) => e.stopPropagation()} />
          <button onClick={(e) => { e.stopPropagation(); next(); }} className="absolute right-4 z-10 w-12 h-12 flex items-center justify-center rounded-full" style={{ backgroundColor: tokens.colors.surfaceAlt, color: tokens.colors.text }} aria-label="Próximo"><ChevronRight className="w-5 h-5" /></button>
        </motion.div>
      )}</AnimatePresence>
    </section>
  );
}
