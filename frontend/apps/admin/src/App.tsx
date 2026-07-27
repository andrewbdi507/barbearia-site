import { Routes, Route, Navigate } from "react-router-dom";
import { Suspense, lazy } from "react";
import { AdminLayout } from "./layouts/AdminLayout";
import { LoginPage } from "./pages/LoginPage";

const DashboardPage = lazy(() => import("./pages/DashboardPage"));
const AgendaPage = lazy(() => import("./pages/AgendaPage"));
const ClientsPage = lazy(() => import("./pages/ClientsPage"));
const ProfessionalsPage = lazy(() => import("./pages/ProfessionalsPage"));
const ServicesPage = lazy(() => import("./pages/ServicesPage"));
const FinancialPage = lazy(() => import("./pages/FinancialPage"));
const ReportsPage = lazy(() => import("./pages/ReportsPage"));
const SettingsPage = lazy(() => import("./pages/SettingsPage"));
const ThemeConfigPage = lazy(() => import("./pages/ThemeConfigPage"));
const AgentsPage = lazy(() => import("./pages/AgentsPage"));
const PlansPage = lazy(() => import("./pages/PlansPage"));
const SettingsPlanPage = lazy(() => import("./pages/SettingsPlanPage"));

function PageLoader() {
  return (
    <div className="flex items-center justify-center h-64">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
    </div>
  );
}

function RequireAuth({ children }: { children: React.ReactNode }) {
  const token = sessionStorage.getItem("access_token");
  if (!token) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        element={
          <RequireAuth>
            <AdminLayout />
          </RequireAuth>
        }
      >
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Suspense fallback={<PageLoader />}><DashboardPage /></Suspense>} />
        <Route path="/agenda" element={<Suspense fallback={<PageLoader />}><AgendaPage /></Suspense>} />
        <Route path="/clients" element={<Suspense fallback={<PageLoader />}><ClientsPage /></Suspense>} />
        <Route path="/professionals" element={<Suspense fallback={<PageLoader />}><ProfessionalsPage /></Suspense>} />
        <Route path="/services" element={<Suspense fallback={<PageLoader />}><ServicesPage /></Suspense>} />
        <Route path="/financial" element={<Suspense fallback={<PageLoader />}><FinancialPage /></Suspense>} />
        <Route path="/reports" element={<Suspense fallback={<PageLoader />}><ReportsPage /></Suspense>} />
        <Route path="/settings" element={<Suspense fallback={<PageLoader />}><SettingsPage /></Suspense>} />
        <Route path="/settings/theme" element={<Suspense fallback={<PageLoader />}><ThemeConfigPage /></Suspense>} />
        <Route path="/settings/plan" element={<Suspense fallback={<PageLoader />}><SettingsPlanPage /></Suspense>} />
        <Route path="/agents" element={<Suspense fallback={<PageLoader />}><AgentsPage /></Suspense>} />
        <Route path="/plans" element={<Suspense fallback={<PageLoader />}><PlansPage /></Suspense>} />
      </Route>
    </Routes>
  );
}
