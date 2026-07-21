import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { User, Calendar, Clock, ArrowRight } from "lucide-react";

export function ProfilePage() {
  return (
    <div className="min-h-screen bg-[#0D0D0D] pt-24 pb-24 px-6">
      <div className="mx-auto max-w-lg">
        <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-12">
          <div className="mx-auto mb-6 flex h-24 w-24 items-center justify-center rounded-full bg-white/[0.03] ring-1 ring-white/5">
            <User className="h-10 w-10 text-white/30" /></div>
          <h1 className="text-2xl font-bold text-[#F5F5F5]">Meu Perfil</h1>
          <p className="text-white/40 mt-2">Gerencie seus agendamentos.</p>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
          className="rounded-2xl border border-white/5 bg-white/[0.02] p-8 mb-6">
          <h2 className="font-bold text-[#F5F5F5] mb-4 flex items-center gap-2"><Calendar className="h-5 w-5 text-[#D72638]" /> Agendamentos</h2>
          <p className="text-white/40 text-sm mb-6">Você ainda não possui agendamentos.</p>
          <Link to="/agendar" className="inline-flex items-center gap-2 rounded-full bg-[#D72638] px-6 py-3 text-sm font-bold text-white hover:bg-[#B81E2E] transition-colors">
            Agendar Agora <ArrowRight className="h-4 w-4" /></Link>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
          className="rounded-2xl border border-white/5 bg-white/[0.02] p-8">
          <h2 className="font-bold text-[#F5F5F5] mb-4 flex items-center gap-2"><Clock className="h-5 w-5 text-[#D72638]" /> Histórico</h2>
          <p className="text-white/40 text-sm">Nenhum serviço realizado ainda.</p>
        </motion.div>
      </div></div>);}
