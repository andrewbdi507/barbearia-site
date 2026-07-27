// ============================================================
// Shared Animation Utilities
// Utilitários de animação comuns a todos os temas.
// ============================================================

import type { Variants, Transition } from "framer-motion";

// ---- Scroll-triggered reveal ----
export function fadeUpVariant(distance = 40, delay = 0): Variants {
  return {
    hidden: { opacity: 0, y: distance },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.7, delay, ease: [0.25, 0.46, 0.45, 0.94] },
    },
  };
}

export function fadeInVariant(delay = 0): Variants {
  return {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { duration: 0.6, delay, ease: "easeOut" },
    },
  };
}

export function scaleInVariant(delay = 0): Variants {
  return {
    hidden: { opacity: 0, scale: 0.92 },
    visible: {
      opacity: 1,
      scale: 1,
      transition: { duration: 0.5, delay, ease: [0.34, 1.56, 0.64, 1] },
    },
  };
}

export function slideInLeftVariant(distance = 60, delay = 0): Variants {
  return {
    hidden: { opacity: 0, x: -distance },
    visible: {
      opacity: 1,
      x: 0,
      transition: { duration: 0.7, delay, ease: [0.25, 0.46, 0.45, 0.94] },
    },
  };
}

export function slideInRightVariant(distance = 60, delay = 0): Variants {
  return {
    hidden: { opacity: 0, x: distance },
    visible: {
      opacity: 1,
      x: 0,
      transition: { duration: 0.7, delay, ease: [0.25, 0.46, 0.45, 0.94] },
    },
  };
}

// ---- Stagger container ----
export function staggerContainer(staggerChildren = 0.08, delayChildren = 0.04): Variants {
  return {
    hidden: {},
    visible: {
      transition: { staggerChildren, delayChildren },
    },
  };
}

export const staggerItem: Variants = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: [0.25, 0.46, 0.45, 0.94] },
  },
};

// ---- Viewport settings ----
export const viewportOnce = {
  once: true,
  margin: "-80px",
} as const;

export const viewportOnceEarly = {
  once: true,
  margin: "-120px",
} as const;

// ---- Hover effects ----
export const hoverScale = { scale: 1.03 };
export const hoverLift = { y: -6 };
export const tapScale = { scale: 0.97 };

// ---- Page transition ----
export const pageTransition: Variants = {
  initial: { opacity: 0, y: 20 },
  animate: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: [0.25, 0.46, 0.45, 0.94] },
  },
  exit: {
    opacity: 0,
    y: -20,
    transition: { duration: 0.3, ease: "easeIn" },
  },
};

// ---- Parallax helpers ----
export function parallaxY(scrollY: number, factor = 0.5): number {
  return scrollY * factor;
}

// ---- Floating animation ----
export const floatAnimation = (duration = 6, y = 10): Variants => ({
  animate: {
    y: [0, -y, 0],
    transition: { duration, repeat: Infinity, ease: "easeInOut" },
  },
});

// ---- Pulse glow ----
export const pulseGlow = (color: string): Variants => ({
  animate: {
    boxShadow: [
      `0 0 10px ${color}20`,
      `0 0 30px ${color}40`,
      `0 0 10px ${color}20`,
    ],
    transition: { duration: 3, repeat: Infinity, ease: "easeInOut" },
  },
});

// ---- Counter animation ----
export function counterAnimation(duration = 2): Record<string, unknown> {
  return {
    initial: { opacity: 0, scale: 0.5 },
    animate: { opacity: 1, scale: 1 },
    transition: { duration, ease: [0.34, 1.56, 0.64, 1] },
  };
}
