// ============================================================
// Theme-Aware Components — Site Público
// Cada componente se adapta automaticamente ao tema ativo.
// ============================================================
import { type ReactNode, type ButtonHTMLAttributes, type AnchorHTMLAttributes } from "react";
import { motion, type HTMLMotionProps } from "framer-motion";
import { useTheme } from "../themes/ThemeProvider";

// ============================================================
// Hero Section
// ============================================================
interface HeroProps {
  title: string;
  subtitle?: string;
  cta?: string;
  ctaHref?: string;
  secondaryCta?: string;
  secondaryHref?: string;
  bgImage?: string;
}

export function Hero({ title, subtitle, cta, ctaHref, secondaryCta, secondaryHref, bgImage }: HeroProps) {
  const { theme } = useTheme();
  const { hero: heroStyle, colors, typography } = theme;

  return (
    <section className="relative min-h-screen flex items-center overflow-hidden">
      {/* Background */}
      {bgImage && (
        <>
          <motion.div
            className="absolute inset-0 z-0"
            initial={{ scale: 1.1 }}
            animate={{ scale: 1 }}
            transition={{ duration: 1.5, ease: [0, 0, 0.2, 1] }}
          >
            <img src={bgImage} alt="" className="w-full h-full object-cover" />
          </motion.div>
          <div
            className="absolute inset-0 z-[1]"
            style={{ background: `rgba(0,0,0,${heroStyle.overlayOpacity})` }}
          />
        </>
      )}

      {/* Content */}
      <div className={`relative z-10 w-full px-4 ${heroStyle.layoutClass === "fullscreen-left" ? "text-left" : heroStyle.layoutClass === "centered" ? "text-center" : "text-left"}`}>
        <div className="mx-auto max-w-7xl">
          <div className={heroStyle.layoutClass === "centered" ? "max-w-3xl mx-auto" : "max-w-3xl"}>
            <motion.h1
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: theme.animations.duration.slow / 1000, delay: 0.2, ease: theme.animations.easing.easeOut }}
              className="leading-[0.9] mb-6"
              style={{
                fontFamily: typography.headingFont,
                fontSize: typography.headingSize.display,
                fontWeight: typography.headingWeight,
                color: colors.text,
                textTransform: heroStyle.textTransform,
                letterSpacing: typography.letterSpacing,
              }}
              dangerouslySetInnerHTML={{ __html: title }}
            />
            {subtitle && (
              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: theme.animations.duration.normal / 1000, delay: 0.4, ease: theme.animations.easing.easeOut }}
                className="text-xl md:text-2xl max-w-xl opacity-80"
                style={{ fontFamily: typography.bodyFont, color: colors.textSecondary, lineHeight: typography.lineHeight }}
              >
                {subtitle}
              </motion.p>
            )}
            {(cta || secondaryCta) && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: theme.animations.duration.normal / 1000, delay: 0.6, ease: theme.animations.easing.easeOut }}
                className="flex flex-wrap gap-4 mt-8"
              >
                {cta && (
                  <a
                    href={ctaHref || "#"}
                    className="inline-flex items-center gap-2 px-8 py-3.5 font-bold transition-all duration-300 text-sm tracking-wide"
                    style={{
                      fontFamily: typography.bodyFont,
                      backgroundColor: colors.primary,
                      color: colors.background,
                      borderRadius: heroStyle.buttonStyle === "pill" ? "9999px" : heroStyle.buttonStyle === "square" ? "0" : "8px",
                      boxShadow: heroStyle.buttonGlow ? `0 0 24px ${colors.primary}40` : "none",
                    }}
                  >
                    {cta}
                  </a>
                )}
                {secondaryCta && (
                  <a
                    href={secondaryHref || "#"}
                    className="inline-flex items-center gap-2 px-8 py-3.5 font-bold border-2 transition-all duration-300 text-sm tracking-wide"
                    style={{
                      fontFamily: typography.bodyFont,
                      borderColor: colors.primary,
                      color: colors.text,
                      borderRadius: heroStyle.buttonStyle === "pill" ? "9999px" : heroStyle.buttonStyle === "square" ? "0" : "8px",
                    }}
                  >
                    {secondaryCta}
                  </a>
                )}
              </motion.div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}

// ============================================================
// Section Wrapper
// ============================================================
export function Section({ children, className = "", id }: { children: ReactNode; className?: string; id?: string }) {
  const { theme } = useTheme();
  return (
    <section
      id={id}
      className={`${className}`}
      style={{
        paddingTop: theme.spacing.section,
        paddingBottom: theme.spacing.section,
        backgroundColor: theme.colors.background,
      }}
    >
      <div className="mx-auto max-w-7xl px-4" style={{ paddingLeft: theme.spacing.padding, paddingRight: theme.spacing.padding }}>
        {children}
      </div>
    </section>
  );
}

// ============================================================
// Section Heading
// ============================================================
export function SectionHeading({ title, subtitle }: { title: string; subtitle?: string }) {
  const { theme } = useTheme();
  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: theme.animations.duration.normal / 1000, ease: theme.animations.easing.easeOut }}
      className="mb-12 text-center"
    >
      <h2
        style={{
          fontFamily: theme.typography.headingFont,
          fontSize: theme.typography.headingSize.h2,
          fontWeight: theme.typography.headingWeight,
          color: theme.colors.text,
          letterSpacing: theme.typography.letterSpacing,
        }}
      >
        {title}
      </h2>
      {subtitle && (
        <p
          className="mt-3 max-w-lg mx-auto"
          style={{
            fontFamily: theme.typography.bodyFont,
            fontSize: theme.typography.bodySize,
            color: theme.colors.textSecondary,
            lineHeight: theme.typography.lineHeight,
          }}
        >
          {subtitle}
        </p>
      )}
    </motion.div>
  );
}

// ============================================================
// Card
// ============================================================
export function Card({ children, className = "", accent = false }: { children: ReactNode; className?: string; accent?: boolean }) {
  const { theme } = useTheme();
  const cs = theme.cardStyle;

  return (
    <motion.div
      initial="initial"
      whileInView="animate"
      viewport={{ once: true, margin: "-40px" }}
      variants={{
        initial: { opacity: 0, y: 30 },
        animate: { opacity: 1, y: 0, transition: { duration: theme.animations.duration.normal / 1000, ease: theme.animations.easing.easeOut } },
      }}
      whileHover={cs.hoverEffect !== "none" ? { y: cs.hoverEffect === "lift" ? -6 : 0, scale: cs.hoverEffect === "scale" ? 1.02 : 1 } : undefined}
      className={`${className}`}
      style={{
        backgroundColor: cs.glassmorphism ? theme.colors.surface : theme.colors.surface,
        backdropFilter: cs.glassmorphism ? "blur(20px)" : "none",
        borderRadius: cs.borderRadius,
        border: `1px solid ${accent || cs.borderAccent ? theme.colors.border : theme.colors.borderLight}`,
        boxShadow: theme.shadows.md,
        padding: theme.spacing.card,
        transition: `all ${theme.animations.duration.fast}ms ${theme.animations.easing.easeOut.join(",") ? "ease-out" : "ease-out"}`,
      }}
    >
      {children}
    </motion.div>
  );
}

// ============================================================
// Button
// ============================================================
interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline";
  glow?: boolean;
}

export function Button({ children, variant = "primary", glow, className = "", ...props }: ButtonProps) {
  const { theme } = useTheme();
  const styles: Record<string, React.CSSProperties> = {
    primary: {
      backgroundColor: theme.colors.primary,
      color: theme.colors.background,
      border: "none",
      boxShadow: glow ? theme.shadows.glow : theme.shadows.sm,
    },
    secondary: {
      backgroundColor: theme.colors.surfaceHover,
      color: theme.colors.text,
      border: `1px solid ${theme.colors.border}`,
    },
    outline: {
      backgroundColor: "transparent",
      color: theme.colors.text,
      border: `2px solid ${theme.colors.primary}`,
    },
  };

  return (
    <motion.button
      whileHover={{ scale: 1.03 }}
      whileTap={{ scale: 0.97 }}
      className={`inline-flex items-center gap-2 px-6 py-3 font-semibold transition-all duration-200 ${className}`}
      style={{
        fontFamily: theme.typography.bodyFont,
        borderRadius: theme.borderRadius.md,
        ...styles[variant],
      }}
      {...(props as HTMLMotionProps<"button">)}
    >
      {children}
    </motion.button>
  );
}

// ============================================================
// Link Button (as anchor)
// ============================================================
export function LinkButton({ children, href, variant = "primary", glow, className = "" }: { children: ReactNode; href: string; variant?: "primary" | "outline"; glow?: boolean; className?: string }) {
  const { theme } = useTheme();
  const isPrimary = variant === "primary";

  return (
    <motion.a
      whileHover={{ scale: 1.03 }}
      whileTap={{ scale: 0.97 }}
      href={href}
      className={`inline-flex items-center gap-2 px-6 py-3 font-semibold transition-all duration-200 ${className}`}
      style={{
        fontFamily: theme.typography.bodyFont,
        borderRadius: theme.borderRadius.md,
        backgroundColor: isPrimary ? theme.colors.primary : "transparent",
        color: isPrimary ? theme.colors.background : theme.colors.text,
        border: isPrimary ? "none" : `2px solid ${theme.colors.primary}`,
        boxShadow: isPrimary && glow ? theme.shadows.glow : "none",
      }}
    >
      {children}
    </motion.a>
  );
}

// ============================================================
// Grid Layout
// ============================================================
export function Grid({ children, cols = 3, className = "" }: { children: ReactNode; cols?: 2 | 3 | 4; className?: string }) {
  const { theme } = useTheme();
  const gridCols = cols === 4 ? "lg:grid-cols-4" : cols === 3 ? "lg:grid-cols-3" : "lg:grid-cols-2";
  return (
    <div
      className={`grid grid-cols-1 md:grid-cols-2 ${gridCols} ${className}`}
      style={{ gap: theme.spacing.gap }}
    >
      {children}
    </div>
  );
}

// ============================================================
// Stagger Container (animates children sequentially)
// ============================================================
export function StaggerContainer({ children, className = "" }: { children: ReactNode; className?: string }) {
  const { theme } = useTheme();
  return (
    <motion.div
      initial="initial"
      whileInView="animate"
      viewport={{ once: true, margin: "-40px" }}
      variants={theme.animations.stagger.container as Record<string, unknown>}
      className={className}
    >
      {children}
    </motion.div>
  );
}

export function StaggerItem({ children, className = "" }: { children: ReactNode; className?: string }) {
  const { theme } = useTheme();
  return (
    <motion.div variants={theme.animations.stagger.item as Record<string, unknown>} className={className}>
      {children}
    </motion.div>
  );
}
