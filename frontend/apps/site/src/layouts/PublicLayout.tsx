import { Outlet, Link, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Menu, X, Scissors } from "lucide-react";

const navLinks = [
  { to: "/", label: "Início" },
  { to: "/servicos", label: "Serviços" },
  { to: "/equipe", label: "Equipe" },
  { to: "/galeria", label: "Galeria" },
];

// Rotas que renderizam tema completo (já incluem Footer próprio)
const themeRoutes = new Set(["/", "/servicos", "/equipe", "/galeria"]);

export function PublicLayout() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const location = useLocation();

  // Detecta se a rota atual é uma página de tema (já tem Footer)
  const isThemePage = themeRoutes.has(location.pathname);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => { setMenuOpen(false); }, [location]);

  // ---- Estilos temáticos via CSS Variables (definidas pelo ThemeProvider) ----
  const cssVar = (name: string, fallback: string) =>
    `var(${name}, ${fallback})`;

  return (
    <div
      className="min-h-screen antialiased"
      style={{
        backgroundColor: cssVar("--color-background", "#0D0D0D"),
        color: cssVar("--color-text", "#F5F5F5"),
      }}
    >
      {/* Header */}
      <header
        className="fixed top-0 z-50 w-full transition-all duration-500"
        style={{
          backgroundColor: scrolled
            ? `color-mix(in srgb, ${cssVar("--color-background", "#0D0D0D")} 95%, transparent)`
            : "transparent",
          backdropFilter: scrolled ? "blur(20px)" : "none",
          borderBottom: scrolled
            ? `1px solid ${cssVar("--color-border", "rgba(255,255,255,0.05)")}`
            : "1px solid transparent",
        }}
      >
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
          <Link to="/" className="flex items-center gap-2 group">
            <div
              className="flex h-9 w-9 items-center justify-center rounded-full transition-colors"
              style={{ backgroundColor: cssVar("--color-primary", "#D72638") }}
            >
              <Scissors className="h-4 w-4" style={{ color: cssVar("--color-text-inverse", "#FFF") }} />
            </div>
            <span
              className="text-lg font-bold tracking-tight"
              style={{ fontFamily: cssVar("--font-heading", "Inter") }}
            >
              Barbearia
            </span>
          </Link>

          <nav className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => (
              <Link
                key={link.to}
                to={link.to}
                className="px-4 py-2 text-sm font-medium rounded-full transition-all duration-300"
                style={{
                  backgroundColor:
                    location.pathname === link.to
                      ? `color-mix(in srgb, ${cssVar("--color-text", "#FFF")} 10%, transparent)`
                      : "transparent",
                  color:
                    location.pathname === link.to
                      ? cssVar("--color-text", "#FFF")
                      : cssVar("--color-text-secondary", "rgba(255,255,255,0.6)"),
                }}
                onMouseEnter={(e) => {
                  if (location.pathname !== link.to) {
                    e.currentTarget.style.color = cssVar("--color-text", "#FFF");
                    e.currentTarget.style.backgroundColor = `color-mix(in srgb, ${cssVar("--color-text", "#FFF")} 5%, transparent)`;
                  }
                }}
                onMouseLeave={(e) => {
                  if (location.pathname !== link.to) {
                    e.currentTarget.style.color = cssVar("--color-text-secondary", "rgba(255,255,255,0.6)");
                    e.currentTarget.style.backgroundColor = "transparent";
                  }
                }}
              >
                {link.label}
              </Link>
            ))}
          </nav>

          <div className="flex items-center gap-3">
            <Link
              to="/agendar"
              className="hidden sm:inline-flex items-center gap-2 rounded-full px-5 py-2.5 text-sm font-semibold transition-all duration-300 hover:scale-105 active:scale-95"
              style={{
                backgroundColor: cssVar("--color-primary", "#D72638"),
                color: cssVar("--color-text-inverse", "#FFF"),
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = cssVar("--color-primary-hover", "#B81E2E");
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = cssVar("--color-primary", "#D72638");
              }}
            >
              Agendar
            </Link>
            <button
              className="md:hidden p-2 transition-colors"
              style={{ color: cssVar("--color-text-secondary", "rgba(255,255,255,0.6)") }}
              onClick={() => setMenuOpen(!menuOpen)}
              aria-label={menuOpen ? "Fechar menu" : "Abrir menu"}
            >
              {menuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </button>
          </div>
        </div>
      </header>

      {/* Mobile Menu */}
      <AnimatePresence>
        {menuOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="fixed inset-0 z-40 flex flex-col pt-20"
            style={{ backgroundColor: cssVar("--color-background", "#0D0D0D") }}
          >
            <nav className="flex flex-col items-center gap-4 p-8">
              {navLinks.map((link, i) => (
                <motion.div
                  key={link.to}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.05 }}
                >
                  <Link
                    to={link.to}
                    className="text-2xl font-bold transition-colors"
                    style={{
                      color:
                        location.pathname === link.to
                          ? cssVar("--color-primary", "#E63946")
                          : cssVar("--color-text-secondary", "rgba(255,255,255,0.6)"),
                    }}
                  >
                    {link.label}
                  </Link>
                </motion.div>
              ))}
              <Link
                to="/agendar"
                className="mt-4 rounded-full px-8 py-3 text-lg font-bold transition-all hover:scale-105"
                style={{
                  backgroundColor: cssVar("--color-primary", "#D72638"),
                  color: cssVar("--color-text-inverse", "#FFF"),
                }}
              >
                Agendar Agora
              </Link>
            </nav>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Content */}
      <main>
        <Outlet />
      </main>

      {/* Footer — oculto em páginas de tema (já possuem Footer próprio) */}
      {!isThemePage && (
        <footer
          className="px-6 py-16"
          style={{
            borderTop: `1px solid ${cssVar("--color-border", "rgba(255,255,255,0.05)")}`,
            backgroundColor: cssVar("--color-background", "#0D0D0D"),
            color: cssVar("--color-text", "#F5F5F5"),
          }}
        >
          <div className="mx-auto max-w-7xl">
            <div className="grid gap-12 sm:grid-cols-2 lg:grid-cols-4">
              <div>
                <div className="flex items-center gap-2 mb-4">
                  <div
                    className="flex h-8 w-8 items-center justify-center rounded-full"
                    style={{ backgroundColor: cssVar("--color-primary", "#D72638") }}
                  >
                    <Scissors className="h-3.5 w-3.5" style={{ color: cssVar("--color-text-inverse", "#FFF") }} />
                  </div>
                  <span
                    className="font-bold tracking-tight"
                    style={{ fontFamily: cssVar("--font-heading", "Inter") }}
                  >
                    Barbearia
                  </span>
                </div>
                <p style={{ color: cssVar("--color-text-muted", "rgba(255,255,255,0.4)") }} className="text-sm">
                  Tradição e estilo.
                </p>
              </div>
              <div>
                <h4
                  className="font-semibold mb-3 text-sm uppercase tracking-wider"
                  style={{ color: cssVar("--color-text-muted", "rgba(255,255,255,0.4)") }}
                >
                  Links
                </h4>
                <div className="flex flex-col gap-2 text-sm">
                  {navLinks.map((l) => (
                    <Link
                      key={l.to}
                      to={l.to}
                      className="transition-colors hover:underline"
                      style={{ color: cssVar("--color-text-secondary", "rgba(255,255,255,0.6)") }}
                    >
                      {l.label}
                    </Link>
                  ))}
                </div>
              </div>
              <div>
                <h4
                  className="font-semibold mb-3 text-sm uppercase tracking-wider"
                  style={{ color: cssVar("--color-text-muted", "rgba(255,255,255,0.4)") }}
                >
                  Contato
                </h4>
                <div
                  className="text-sm space-y-1"
                  style={{ color: cssVar("--color-text-secondary", "rgba(255,255,255,0.6)") }}
                >
                  <p>(11) 3333-4444</p>
                  <p>Rua Augusta, 1234</p>
                  <p>Seg-Sex 9h-19h · Sáb 9h-14h</p>
                </div>
              </div>
              <div>
                <h4
                  className="font-semibold mb-3 text-sm uppercase tracking-wider"
                  style={{ color: cssVar("--color-text-muted", "rgba(255,255,255,0.4)") }}
                >
                  Redes
                </h4>
                <div className="flex gap-3">
                  <a
                    href="#"
                    className="transition-colors hover:underline"
                    style={{ color: cssVar("--color-text-muted", "rgba(255,255,255,0.4)") }}
                  >
                    Instagram
                  </a>
                  <a
                    href="#"
                    className="transition-colors hover:underline"
                    style={{ color: cssVar("--color-text-muted", "rgba(255,255,255,0.4)") }}
                  >
                    WhatsApp
                  </a>
                </div>
              </div>
            </div>
            <div
              className="mt-12 pt-8 text-center text-xs"
              style={{
                borderTop: `1px solid ${cssVar("--color-border", "rgba(255,255,255,0.05)")}`,
                color: cssVar("--color-text-muted", "rgba(255,255,255,0.3)"),
              }}
            >
              © {new Date().getFullYear()} Barbearia · Todos os direitos reservados
            </div>
          </div>
        </footer>
      )}
    </div>
  );
}
