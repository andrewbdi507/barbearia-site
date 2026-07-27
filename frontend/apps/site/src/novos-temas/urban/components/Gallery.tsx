// ============================================================
// URBAN Theme — Gallery Section
// Masonry-style grid com hover reveal e lightbox trigger.
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
    <section
      style={{ backgroundColor: tokens.colors.background, paddingTop: tokens.spacing.section, paddingBottom: tokens.spacing.section }}
      aria-labelledby="gallery-title"
    >
      <div className="max-w-[1400px] mx-auto px-6 md:px-12">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mb-16 text-center"
        >
          <span
            className="inline-block mb-4 text-sm font-semibold tracking-widest uppercase"
            style={{ color: tokens.colors.primary, fontFamily: tokens.typography.bodyFont }}
          >
            Galeria
          </span>
          <h2
            id="gallery-title"
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
            <p className="mt-4 max-w-xl mx-auto" style={{ fontFamily: tokens.typography.bodyFont, color: tokens.colors.textSecondary }}>
              {subtitle}
            </p>
          )}
        </motion.div>

        {/* Masonry Grid */}
        <div className="columns-1 sm:columns-2 lg:columns-3 gap-4 space-y-4">
          {images.map((img, i) => (
            <motion.div
              key={img.id || i}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-40px" }}
              transition={{ duration: 0.5, delay: i * 0.06 }}
              className="group relative break-inside-avoid overflow-hidden cursor-pointer"
              onClick={() => setSelectedIdx(i)}
            >
              <img
                src={img.src}
                alt={img.alt}
                className="w-full h-auto object-cover transition-transform duration-700 group-hover:scale-105"
                loading="lazy" decoding="async"
              />
              {/* Overlay */}
              <div className="absolute inset-0 bg-black/0 group-hover:bg-black/50 transition-all duration-300 flex items-center justify-center">
                <Expand className="w-8 h-8 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-300 scale-50 group-hover:scale-100" />
              </div>
              {/* Accent border on hover */}
              <div
                className="absolute inset-0 border-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
                style={{ borderColor: tokens.colors.primary }}
              />
            </motion.div>
          ))}
        </div>

        {/* Lightbox */}
        <AnimatePresence>
          {selectedIdx !== null && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 z-[100] flex items-center justify-center p-4"
              style={{ backgroundColor: "rgba(0,0,0,0.95)" }}
              onClick={() => setSelectedIdx(null)}
            >
              <button
                onClick={() => setSelectedIdx(null)}
                className="absolute top-6 right-6 z-10 w-12 h-12 flex items-center justify-center rounded-full border transition-colors"
                style={{ borderColor: tokens.colors.border, color: tokens.colors.text }}
                aria-label="Fechar"
              >
                <X className="w-6 h-6" />
              </button>

              <button
                onClick={(e) => { e.stopPropagation(); prev(); }}
                className="absolute left-4 md:left-10 z-10 w-14 h-14 flex items-center justify-center rounded-full transition-colors"
                style={{ backgroundColor: tokens.colors.surface, color: tokens.colors.text }}
                aria-label="Anterior"
              >
                <ChevronLeft className="w-6 h-6" />
              </button>

              <motion.img
                key={selectedIdx}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                transition={{ duration: 0.3 }}
                src={images[selectedIdx].src}
                alt={images[selectedIdx].alt}
                className="max-w-full max-h-[85vh] object-contain"
                onClick={(e) => e.stopPropagation()}
              />

              <button
                onClick={(e) => { e.stopPropagation(); next(); }}
                className="absolute right-4 md:right-10 z-10 w-14 h-14 flex items-center justify-center rounded-full transition-colors"
                style={{ backgroundColor: tokens.colors.surface, color: tokens.colors.text }}
                aria-label="Próximo"
              >
                <ChevronRight className="w-6 h-6" />
              </button>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </section>
  );
}
