import { Routes, Route, Navigate } from "react-router-dom";
import { AdminLayout } from "./layouts/AdminLayout";
import { LoginPage } from "./pages/LoginPage";
import { DashboardPage } from "./pages/DashboardPage";
import { AgendaPage } from "./pages/AgendaPage";
import { ClientsPage } from "./pages/ClientsPage";
import { ProfessionalsPage } from "./pages/ProfessionalsPage";
import { ServicesPage } from "./pages/ServicesPage";
import { FinancialPage } from "./pages/FinancialPage";
import { ReportsPage } from "./pages/ReportsPage";
import { SettingsPage } from "./pages/SettingsPage";
import { ThemeConfigPage } from "./pages/ThemeConfigPage";
import AgentsPage from "./pages/AgentsPage";
import PlansPage from "./pages/PlansPage";

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
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/agenda" element={<AgendaPage />} />
        <Route path="/clients" element={<ClientsPage />} />
        <Route path="/professionals" element={<ProfessionalsPage />} />
        <Route path="/services" element={<ServicesPage />} />
        <Route path="/financial" element={<FinancialPage />} />
        <Route path="/reports" element={<ReportsPage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="/settings/theme" element={<ThemeConfigPage />} />
        <Route path="/agents" element={<AgentsPage />} />
        <Route path="/plans" element={<PlansPage />} />
      </Route>
    </Routes>
  );
}
