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

export function PublicLayout() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => { setMenuOpen(false); }, [location]);

  return (
    <div className="min-h-screen bg-[#0D0D0D] text-[#F5F5F5]">
      {/* Header */}
      <header
        className={`fixed top-0 z-50 w-full transition-all duration-500 ${
          scrolled ? "bg-[#0D0D0D]/95 backdrop-blur-xl border-b border-white/5" : "bg-transparent"
        }`}
      >
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
          <Link to="/" className="flex items-center gap-2 group">
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-[#D72638]">
              <Scissors className="h-4 w-4 text-white" />
            </div>
            <span className="text-lg font-bold tracking-tight">STUDIO 27</span>
          </Link>

          <nav className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => (
              <Link
                key={link.to}
                to={link.to}
                className={`px-4 py-2 text-sm font-medium rounded-full transition-all duration-300 ${
                  location.pathname === link.to
                    ? "bg-white/10 text-white"
                    : "text-white/60 hover:text-white hover:bg-white/5"
                }`}
              >
                {link.label}
              </Link>
            ))}
          </nav>

          <div className="flex items-center gap-3">
            <Link
              to="/agendar"
              className="hidden sm:inline-flex items-center gap-2 rounded-full bg-[#D72638] px-5 py-2.5 text-sm font-semibold text-white transition-all duration-300 hover:bg-[#B81E2E] hover:scale-105 active:scale-95"
            >
              Agendar
            </Link>
            <button
              className="md:hidden p-2 text-white/60 hover:text-white"
              onClick={() => setMenuOpen(!menuOpen)}
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
            className="fixed inset-0 z-40 flex flex-col bg-[#0D0D0D] pt-20"
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
                    className={`text-2xl font-bold ${
                      location.pathname === link.to ? "text-[#D72638]" : "text-white/60"
                    }`}
                  >
                    {link.label}
                  </Link>
                </motion.div>
              ))}
              <Link
                to="/agendar"
                className="mt-4 rounded-full bg-[#D72638] px-8 py-3 text-lg font-bold text-white"
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

      {/* Footer */}
      <footer className="border-t border-white/5 bg-[#0D0D0D] px-6 py-16">
        <div className="mx-auto max-w-7xl">
          <div className="grid gap-12 sm:grid-cols-2 lg:grid-cols-4">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-[#D72638]">
                  <Scissors className="h-3.5 w-3.5 text-white" />
                </div>
                <span className="font-bold tracking-tight">STUDIO 27</span>
              </div>
              <p className="text-sm text-white/40">Tradição e estilo desde 2018.</p>
            </div>
            <div>
              <h4 className="font-semibold mb-3 text-sm uppercase tracking-wider text-white/40">Links</h4>
              <div className="flex flex-col gap-2 text-sm text-white/60">
                {navLinks.map(l => <Link key={l.to} to={l.to} className="hover:text-white transition-colors">{l.label}</Link>)}
              </div>
            </div>
            <div>
              <h4 className="font-semibold mb-3 text-sm uppercase tracking-wider text-white/40">Contato</h4>
              <div className="text-sm text-white/60 space-y-1">
                <p>(11) 3333-4444</p>
                <p>Rua Augusta, 1234</p>
                <p>Seg-Sex 9h-19h · Sáb 9h-14h</p>
              </div>
            </div>
            <div>
              <h4 className="font-semibold mb-3 text-sm uppercase tracking-wider text-white/40">Redes</h4>
              <div className="flex gap-3">
                <a href="#" className="text-white/40 hover:text-white transition-colors">Instagram</a>
                <a href="#" className="text-white/40 hover:text-white transition-colors">WhatsApp</a>
              </div>
            </div>
          </div>
          <div className="mt-12 pt-8 border-t border-white/5 text-center text-xs text-white/30">
            © 2026 Studio 27 Barbearia · Todos os direitos reservados
          </div>
        </div>
      </footer>
    </div>
  );
}
            </button>
          </div>
        </div>

        {/* Mobile Nav */}
        {menuOpen && (
          <nav className="md:hidden border-t border-border bg-surface px-4 py-3 animate-slide-down">
            {navLinks.map((link) => (
              <Link
                key={link.to}
                to={link.to}
                onClick={() => setMenuOpen(false)}
                className="block px-3 py-2.5 text-sm font-medium rounded-md text-text-secondary hover:bg-surface-hover"
              >
                {link.label}
              </Link>
            ))}
            <Link to="/agendar" onClick={() => setMenuOpen(false)} className="block mt-2">
              <Button fullWidth>Agendar Agora</Button>
            </Link>
          </nav>
        )}
      </header>

      {/* Page Content */}
      <main className="flex-1">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-primary text-white mt-auto">
        <div className="mx-auto max-w-6xl px-4 py-10 grid gap-8 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
          <div>
            <h4 className="font-bold text-lg mb-3">Studio 27</h4>
            <p className="text-sm text-white/70">Tradição e estilo desde 2018.</p>
          </div>
          <div>
            <h4 className="font-bold mb-3">Links</h4>
            <div className="flex flex-col gap-2 text-sm text-white/70">
              {navLinks.map((l) => (
                <Link key={l.to} to={l.to} className="hover:text-white transition-colors">{l.label}</Link>
              ))}
            </div>
          </div>
          <div>
            <h4 className="font-bold mb-3">Contato</h4>
            <div className="space-y-2 text-sm text-white/70">
              <div className="flex items-center gap-2"><Phone className="h-4 w-4" /> (11) 3333-4444</div>
              <div className="flex items-center gap-2"><MapPin className="h-4 w-4" /> Rua Augusta, 1234</div>
              <div className="flex items-center gap-2"><Clock className="h-4 w-4" /> Seg-Sex 9h-19h · Sáb 9h-14h</div>
            </div>
          </div>
          <div>
            <h4 className="font-bold mb-3">Redes Sociais</h4>
            <div className="flex gap-3">
              <a href="#" className="text-white/70 hover:text-white transition-colors" aria-label="Instagram"><Instagram className="h-5 w-5" /></a>
              <a href="#" className="text-white/70 hover:text-white transition-colors" aria-label="WhatsApp"><MessageCircle className="h-5 w-5" /></a>
            </div>
          </div>
        </div>
        <div className="border-t border-white/10 py-4 text-center text-sm text-white/50">
          © {new Date().getFullYear()} Studio 27 Barbearia · Todos os direitos reservados
        </div>
      </footer>

      {/* Mobile CTA sticky */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 z-20 bg-surface border-t border-border p-3 safe-bottom">
        <Link to="/agendar">
          <Button fullWidth size="lg">Agendar Agora</Button>
        </Link>
      </div>

      {/* WhatsApp floating button */}
      <a
        href="https://wa.me/5511999999999"
        target="_blank"
        rel="noopener noreferrer"
        className="fixed bottom-24 right-4 z-20 md:bottom-6 flex h-14 w-14 items-center justify-center rounded-full bg-success text-white shadow-lg hover:scale-105 transition-transform animate-pulse"
        aria-label="Fale conosco no WhatsApp"
      >
        <MessageCircle className="h-6 w-6" />
      </a>
    </div>
  );
}
