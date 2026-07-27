import { Routes, Route } from "react-router-dom";
import { PublicLayout } from "./layouts/PublicLayout";
import ThemeHomePage from "./pages/ThemeHomePage";
import { BookingPage } from "./pages/BookingPage";
import { ConfirmationPage } from "./pages/ConfirmationPage";
import { ProfilePage } from "./pages/ProfilePage";

export default function App() {
  return (
    <Routes>
      <Route element={<PublicLayout />}>
        <Route path="/" element={<ThemeHomePage />} />
        <Route path="/servicos" element={<ThemeHomePage />} />
        <Route path="/equipe" element={<ThemeHomePage />} />
        <Route path="/galeria" element={<ThemeHomePage />} />
        <Route path="/agendar" element={<BookingPage />} />
        <Route path="/confirmacao/:bookingId" element={<ConfirmationPage />} />
        <Route path="/perfil" element={<ProfilePage />} />
      </Route>
    </Routes>
  );
}
