import { Outlet, useLocation, Link, useNavigate } from "react-router-dom";
import { useState, useEffect, useCallback } from "react";
import { cn, Button, Input } from "@barbershop/design-system";
import {
  LayoutDashboard, Calendar, Users, Scissors, UserRound,
  DollarSign, BarChart3, Settings, Palette, LogOut,
  Menu, X, Bell, Sun, Moon, ChevronDown, Search,
  Command, Home, Image, Star, MessageSquare, Globe, HelpCircle,
  ChevronRight, Brain, Zap,
} from "lucide-react";

const navItems = [
  { to: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
  { to: "/agenda", icon: Calendar, label: "Agenda" },
  { to: "/clients", icon: Users, label: "Clientes" },
  { to: "/professionals", icon: UserRound, label: "Equipe" },
  { to: "/services", icon: Scissors, label: "Serviços" },
  { to: "/financial", icon: DollarSign, label: "Financeiro" },
  { to: "/reports", icon: BarChart3, label: "Relatórios" },
  { to: "/gallery", icon: Image, label: "Galeria" },
  { to: "/reviews", icon: Star, label: "Avaliações" },
  { to: "/site", icon: Globe, label: "Site" },
  { to: "/notifications", icon: MessageSquare, label: "Notificações" },
  { to: "/agents", icon: Brain, label: "IA & Agentes" },
  { to: "/plans", icon: Zap, label: "Planos" },
];

const bottomNavItems = [
  { to: "/settings", icon: Settings, label: "Configurações" },
  { to: "/settings/theme", icon: Palette, label: "Aparência" },
  { to: "/help", icon: HelpCircle, label: "Ajuda" },
];

// Breadcrumb resolver
function getBreadcrumbs(pathname: string): { label: string; to?: string }[] {
  const parts = pathname.split("/").filter(Boolean);
  const crumbs: { label: string; to?: string }[] = [{ label: "Home", to: "/dashboard" }];

  const labelMap: Record<string, string> = {
    dashboard: "Dashboard", agenda: "Agenda", clients: "Clientes",
    professionals: "Equipe", services: "Serviços", financial: "Financeiro",
    reports: "Relatórios", settings: "Configurações", theme: "Aparência",
    gallery: "Galeria", reviews: "Avaliações", site: "Site",
    notifications: "Notificações", help: "Ajuda",
  };

  let current = "";
  for (const part of parts) {
    current += `/${part}`;
    const label = labelMap[part] || part;
    crumbs.push({ label, to: current });
  }
  return crumbs;
}

export function AdminLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [dark, setDark] = useState(() => document.documentElement.classList.contains("dark"));
  const [searchOpen, setSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const location = useLocation();
  const navigate = useNavigate();
  const breadcrumbs = getBreadcrumbs(location.pathname);

  const toggleDark = () => {
    setDark(!dark);
    document.documentElement.classList.toggle("dark");
  };

  // ⌘K global search
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setSearchOpen(true);
      }
      if (e.key === "Escape") setSearchOpen(false);
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  const handleSearch = useCallback((q: string) => {
    if (q.length >= 2) {
      navigate(`/dashboard?search=${encodeURIComponent(q)}`);
      setSearchOpen(false);
      setSearchQuery("");
    }
  }, [navigate]);

  return (
    <div className="flex h-screen overflow-hidden bg-bg">
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-20 bg-black/50 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-30 w-64 bg-surface border-r border-border",
          "flex flex-col transition-transform duration-300 lg:relative lg:translate-x-0",
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        )}
      >
        {/* Logo */}
        <div className="flex h-14 items-center gap-3 border-b border-border px-4">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-white font-bold text-sm">
            B
          </div>
          <span className="text-lg font-semibold text-text-primary">Barbershop</span>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto py-4 px-3">
          <div className="space-y-1">
            {navItems.map((item) => (
              <Link
                key={item.to}
                to={item.to}
                onClick={() => setSidebarOpen(false)}
                className={cn(
                  "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                  location.pathname === item.to
                    ? "bg-primary/10 text-primary"
                    : "text-text-secondary hover:bg-surface-hover hover:text-text-primary"
                )}
              >
                <item.icon className="h-5 w-5 shrink-0" />
                {item.label}
              </Link>
            ))}
          </div>

          <div className="mt-6 pt-6 border-t border-border space-y-1">
            {bottomNavItems.map((item) => (
              <Link
                key={item.to}
                to={item.to}
                onClick={() => setSidebarOpen(false)}
                className={cn(
                  "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                  location.pathname.startsWith(item.to)
                    ? "bg-primary/10 text-primary"
                    : "text-text-secondary hover:bg-surface-hover hover:text-text-primary"
                )}
              >
                <item.icon className="h-5 w-5 shrink-0" />
                {item.label}
              </Link>
            ))}
          </div>
        </nav>

        {/* User */}
        <div className="border-t border-border p-4">
          <div className="flex items-center gap-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary-light text-primary text-sm font-semibold">
              CO
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-text-primary truncate">Carlos Oliveira</p>
              <p className="text-xs text-text-secondary">Admin</p>
            </div>
            <Button variant="ghost" size="icon" aria-label="Sair">
              <LogOut className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex flex-1 flex-col overflow-hidden">
        {/* Header */}
        <header className="flex h-14 items-center gap-4 border-b border-border bg-surface px-4 lg:px-6">
          <Button
            variant="ghost"
            size="icon"
            className="lg:hidden"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            aria-label="Menu"
          >
            {sidebarOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </Button>

          {/* Breadcrumb */}
          <nav className="hidden md:flex items-center gap-1 text-sm text-text-secondary" aria-label="Breadcrumb">
            {breadcrumbs.map((crumb, i) => (
              <span key={i} className="flex items-center gap-1">
                {i > 0 && <ChevronRight className="h-3.5 w-3.5" />}
                {crumb.to && i < breadcrumbs.length - 1 ? (
                  <Link to={crumb.to} className="hover:text-text-primary transition-colors">
                    {crumb.label}
                  </Link>
                ) : (
                  <span className="text-text-primary font-medium">{crumb.label}</span>
                )}
              </span>
            ))}
          </nav>

          <div className="flex-1" />

          {/* Global Search trigger */}
          <button
            onClick={() => setSearchOpen(true)}
            className="hidden md:flex items-center gap-2 rounded-md border border-border bg-bg px-3 py-1.5 text-sm text-text-secondary hover:border-primary/30 transition-colors"
          >
            <Search className="h-4 w-4" />
            <span>Buscar...</span>
            <kbd className="ml-4 rounded border border-border bg-surface px-1.5 py-0.5 text-[10px] font-mono text-text-secondary">
              <Command className="h-3 w-3 inline" />K
            </kbd>
          </button>

          <Button variant="ghost" size="icon" onClick={toggleDark} aria-label="Alternar tema">
            {dark ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </Button>

          <Button variant="ghost" size="icon" aria-label="Notificações" className="relative">
            <Bell className="h-5 w-5" />
            <span className="absolute -top-0.5 -right-0.5 flex h-4 w-4 items-center justify-center rounded-full bg-secondary text-[10px] font-bold text-white">
              3
            </span>
          </Button>

          <button className="flex items-center gap-2 rounded-md p-1.5 text-sm hover:bg-surface-hover transition-colors">
            <div className="flex h-7 w-7 items-center justify-center rounded-full bg-primary text-white text-xs font-semibold">
              CO
            </div>
            <span className="hidden md:inline text-text-primary">Carlos</span>
            <ChevronDown className="h-3.5 w-3.5 text-text-secondary hidden md:block" />
          </button>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto p-4 lg:p-6">
          <Outlet />
        </main>
      </div>

      {/* Command Palette Modal */}
      {searchOpen && (
        <div className="fixed inset-0 z-50">
          <div className="fixed inset-0 bg-black/50" onClick={() => setSearchOpen(false)} />
          <div className="fixed inset-x-0 top-[15%] mx-auto max-w-lg">
            <div className="bg-surface rounded-xl shadow-2xl border border-border overflow-hidden">
              <div className="flex items-center gap-3 px-4 py-3 border-b border-border">
                <Search className="h-5 w-5 text-text-secondary" />
                <Input
                  autoFocus
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyDown={(e) => { if (e.key === "Enter") handleSearch(searchQuery); }}
                  placeholder="Buscar clientes, serviços, profissionais..."
                  className="border-0 bg-transparent flex-1 text-sm focus-visible:ring-0 p-0"
                />
                <kbd className="rounded border border-border bg-bg px-1.5 py-0.5 text-[10px] font-mono text-text-secondary">ESC</kbd>
              </div>
              <div className="p-2 max-h-64 overflow-y-auto">
                <p className="px-3 py-2 text-xs text-text-secondary">Comece a digitar para buscar em todo o sistema</p>
                <div className="px-3 py-2 text-xs text-text-secondary flex items-center gap-2">
                  <Command className="h-3 w-3" />
                  Atalhos: ⌘K — Busca global · ⌘S — Salvar · ⌘N — Novo
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
