import { Routes, Route } from "react-router-dom";
import { PublicLayout } from "./layouts/PublicLayout";
import { HomePage } from "./pages/HomePage";
import { ServicesPage } from "./pages/ServicesPage";
import { TeamPage } from "./pages/TeamPage";
import { GalleryPage } from "./pages/GalleryPage";
import { BookingPage } from "./pages/BookingPage";
import { ConfirmationPage } from "./pages/ConfirmationPage";
import { ProfilePage } from "./pages/ProfilePage";

export default function App() {
  return (
    <Routes>
      <Route element={<PublicLayout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/servicos" element={<ServicesPage />} />
        <Route path="/equipe" element={<TeamPage />} />
        <Route path="/galeria" element={<GalleryPage />} />
        <Route path="/agendar" element={<BookingPage />} />
        <Route path="/confirmacao/:bookingId" element={<ConfirmationPage />} />
        <Route path="/perfil" element={<ProfilePage />} />
      </Route>
    </Routes>
  );
}
