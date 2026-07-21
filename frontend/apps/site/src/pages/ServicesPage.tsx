import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { Scissors, Clock, ArrowRight } from "lucide-react";

const allServices = [
  { name: "Corte", price: "R$ 45,00", duration: "30 min", desc: "Tesoura, máquina e finalização com pomada." },
  { name: "Barba", price: "R$ 30,00", duration: "20 min", desc: "Toalha quente, balm e navalhete." },
  { name: "Corte + Barba", price: "R$ 65,00", duration: "45 min", desc: "Combo completo para renovar o visual." },
  { name: "Hidratação", price: "R$ 40,00", duration: "25 min", desc: "Tratamento capilar revitalizante." },
  { name: "Platinado", price: "R$ 120,00", duration: "90 min", desc: "Descoloração completa com matização." },
  { name: "Pezinho", price: "R$ 20,00", duration: "15 min", desc: "Acabamento com navalha." },
];

export function ServicesPage() {
  return (
    <div className="min-h-screen bg-[#0D0D0D] pt-24 pb-24 px-6">
      <div className="mx-auto max-w-5xl">
        <motion.div initial={{ opacity: 0, y: 40 }} animate={{ opacity: 1, y: 0 }} className="mb-16 text-center">
          <p className="mb-3 text-sm font-semibold uppercase tracking-[0.2em] text-[#D72638]">Serviços</p>
          <h1 className="text-display-sm text-[#F5F5F5] mb-4">Nossos Serviços</h1>
          <p className="text-white/40 max-w-md mx-auto">Conheça nossos serviços e preços.</p>
        </motion.div>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {allServices.map((svc, i) => (
            <motion.div key={svc.name} initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.08 }} whileHover={{ y: -2 }}
              className="flex items-center justify-between gap-4 rounded-2xl border border-white/5 bg-white/[0.02] p-6 transition-all duration-300 hover:border-[#D72638]/20">
              <div className="flex items-start gap-4">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#D72638]/10">
                  <Scissors className="h-4 w-4 text-[#D72638]" /></div>
                <div><h3 className="font-bold text-[#F5F5F5]">{svc.name}</h3>
                  <p className="text-sm text-white/40 mt-0.5">{svc.desc}</p>
                  <p className="text-xs text-white/20 mt-1 flex items-center gap-1"><Clock className="h-3 w-3" /> {svc.duration}</p></div></div>
              <span className="text-lg font-bold text-[#D72638] whitespace-nowrap">{svc.price}</span>
            </motion.div>))}
        </div>
        <div className="mt-16 text-center">
          <Link to="/agendar" className="inline-flex items-center gap-2 rounded-full bg-[#D72638] px-8 py-4 text-lg font-bold text-white transition-all duration-300 hover:scale-105">
            Agendar Agora <ArrowRight className="h-5 w-5" /></Link></div></div></div>);}

export function TeamPage() {
  const team = [{ name: "Marcos", role: "Master Barber", rating: 4.9 }, { name: "Ricardo", role: "Senior Barber", rating: 4.7 }, { name: "Lucas", role: "Style Specialist", rating: 4.8 }, { name: "Rafael", role: "Creative Director", rating: 4.9 }];
  return (
    <div className="min-h-screen bg-[#0D0D0D] pt-24 pb-24 px-6">
      <div className="mx-auto max-w-5xl">
        <motion.div initial={{ opacity: 0, y: 40 }} animate={{ opacity: 1, y: 0 }} className="mb-16 text-center">
          <p className="mb-3 text-sm font-semibold uppercase tracking-[0.2em] text-[#D72638]">Equipe</p>
          <h1 className="text-display-sm text-[#F5F5F5] mb-4">Nossa Equipe</h1>
          <p className="text-white/40 max-w-md mx-auto">Conheça os mestres do ofício.</p>
        </motion.div>
        <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {team.map((pro, i) => (
            <motion.div key={pro.name} initial={{ opacity: 0, y: 40 }} animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }} className="text-center group">
              <div className="mx-auto mb-5 flex h-32 w-32 items-center justify-center rounded-full bg-white/[0.03] ring-1 ring-white/5 group-hover:ring-[#D72638]/30 transition-all duration-500">
                <span className="text-4xl font-bold text-white/20 group-hover:text-[#D72638] transition-colors">{pro.name[0]}</span></div>
              <h3 className="text-xl font-bold text-[#F5F5F5]">{pro.name}</h3>
              <p className="text-sm text-white/40">{pro.role}</p>
              <p className="mt-2 text-sm text-[#D72638]">⭐ {pro.rating}</p>
            </motion.div>))}
        </div></div></div>);}

export function GalleryPage() {
  return (
    <div className="min-h-screen bg-[#0D0D0D] pt-24 pb-24 px-6">
      <div className="mx-auto max-w-6xl">
        <motion.div initial={{ opacity: 0, y: 40 }} animate={{ opacity: 1, y: 0 }} className="mb-16 text-center">
          <p className="mb-3 text-sm font-semibold uppercase tracking-[0.2em] text-[#D72638]">Galeria</p>
          <h1 className="text-display-sm text-[#F5F5F5] mb-4">Galeria</h1>
          <p className="text-white/40 max-w-md mx-auto">Nossos melhores trabalhos.</p>
        </motion.div>
        <div className="grid gap-4 grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
          {Array.from({ length: 8 }).map((_, i) => (
            <motion.div key={i} initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: i * 0.05 }} whileHover={{ scale: 1.02 }}
              className="aspect-square rounded-2xl border border-white/5 bg-white/[0.02] flex items-center justify-center text-white/10 text-sm">
              Imagem {i + 1}
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
