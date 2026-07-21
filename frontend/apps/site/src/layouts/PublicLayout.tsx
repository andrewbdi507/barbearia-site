import { Outlet, Link, useLocation } from "react-router-dom";
import { useState } from "react";
import { Button, cn } from "@barbershop/design-system";
import { Menu, X, Phone, MapPin, Clock, Instagram, MessageCircle } from "lucide-react";

const navLinks = [
  { to: "/", label: "Início" },
  { to: "/servicos", label: "Serviços" },
  { to: "/equipe", label: "Equipe" },
  { to: "/galeria", label: "Galeria" },
];

export function PublicLayout() {
  const [menuOpen, setMenuOpen] = useState(false);
  const location = useLocation();

  return (
    <div className="flex flex-col min-h-screen">
      {/* Header */}
      <header className="sticky top-0 z-20 bg-surface/95 backdrop-blur-sm border-b border-border">
        <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-4">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-white font-bold text-sm">
              S
            </div>
            <span className="text-lg font-bold text-text-primary hidden sm:block">
              Studio 27
            </span>
          </Link>

          {/* Desktop Nav */}
          <nav className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => (
              <Link
                key={link.to}
                to={link.to}
                className={cn(
                  "px-3 py-2 text-sm font-medium rounded-md transition-colors",
                  location.pathname === link.to
                    ? "text-primary bg-primary/5"
                    : "text-text-secondary hover:text-text-primary hover:bg-surface-hover"
                )}
              >
                {link.label}
              </Link>
            ))}
          </nav>

          {/* CTA + Mobile menu */}
          <div className="flex items-center gap-2">
            <Link to="/agendar">
              <Button size="sm" className="hidden sm:flex">Agendar</Button>
            </Link>
            <button
              className="md:hidden p-2 rounded-md text-text-secondary hover:bg-surface-hover"
              onClick={() => setMenuOpen(!menuOpen)}
              aria-label="Menu"
            >
              {menuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
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
