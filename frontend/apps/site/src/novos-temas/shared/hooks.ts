// ============================================================
// Shared Hooks
// Hooks comuns reutilizáveis entre temas.
// ============================================================

import { useState, useEffect, useCallback, useRef } from "react";

// ---- Scroll Position ----
export function useScrollPosition(): number {
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    let ticking = false;
    const onScroll = () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          setScrollY(window.scrollY);
          ticking = false;
        });
        ticking = true;
      }
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return scrollY;
}

// ---- Scroll Direction ----
export function useScrollDirection(): "up" | "down" {
  const [dir, setDir] = useState<"up" | "down">("up");
  const lastY = useRef(0);

  useEffect(() => {
    const onScroll = () => {
      const y = window.scrollY;
      if (Math.abs(y - lastY.current) > 10) {
        setDir(y > lastY.current ? "down" : "up");
      }
      lastY.current = y;
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return dir;
}

// ---- Element in Viewport ----
export function useInView(threshold = 0.2): [boolean, React.RefObject<HTMLElement | null>] {
  const [inView, setInView] = useState(false);
  const ref = useRef<HTMLElement | null>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setInView(true);
          observer.unobserve(el);
        }
      },
      { threshold }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, [threshold]);

  return [inView, ref];
}

// ---- Media Query ----
export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const mq = window.matchMedia(query);
    setMatches(mq.matches);
    const onChange = (e: MediaQueryListEvent) => setMatches(e.matches);
    mq.addEventListener("change", onChange);
    return () => mq.removeEventListener("change", onChange);
  }, [query]);

  return matches;
}

// ---- Reduced Motion ----
export function useReducedMotion(): boolean {
  return useMediaQuery("(prefers-reduced-motion: reduce)");
}

// ---- Lazy Load (for Intersection Observer based rendering) ----
export function useLazyLoad(rootMargin = "200px"): [boolean, (node: HTMLElement | null) => void] {
  const [visible, setVisible] = useState(false);
  const observerRef = useRef<IntersectionObserver | null>(null);

  const refCallback = useCallback(
    (node: HTMLElement | null) => {
      if (observerRef.current) observerRef.current.disconnect();
      if (!node) return;
      observerRef.current = new IntersectionObserver(
        ([entry]) => {
          if (entry.isIntersecting) {
            setVisible(true);
            observerRef.current?.disconnect();
          }
        },
        { rootMargin }
      );
      observerRef.current.observe(node);
    },
    [rootMargin]
  );

  return [visible, refCallback];
}

// ---- Smooth Scroll To ----
export function useSmoothScroll() {
  return useCallback((selector: string) => {
    const el = document.querySelector(selector);
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, []);
}

// ---- Toggle ----
export function useToggle(initial = false): [boolean, () => void, (v: boolean) => void] {
  const [value, setValue] = useState(initial);
  const toggle = useCallback(() => setValue((v) => !v), []);
  return [value, toggle, setValue];
}
