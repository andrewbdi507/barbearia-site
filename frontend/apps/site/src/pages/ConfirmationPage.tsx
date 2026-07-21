import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { CheckCircle, CalendarPlus, MapPin, Clock, ArrowLeft } from "lucide-react";

export function ConfirmationPage() {
  return (
    <div className="min-h-screen bg-[#0D0D0D] pt-24 pb-24 px-6 flex items-center justify-center">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="max-w-md w-full text-center"
      >
        <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-[#D72638]/10">
          <CheckCircle className="h-10 w-10 text-[#D72638]" />
        </div>

        <h1 className="text-2xl font-bold text-[#F5F5F5] mb-2">Agendamento Confirmado!</h1>
        <p className="text-white/40 mb-8">Você receberá a confirmação em instantes.</p>

        <div className="rounded-2xl border border-white/5 bg-white/[0.02] p-6 mb-8 text-left">
          <div className="space-y-3 text-sm">
            <div className="flex justify-between">
              <span className="text-white/40">Barbearia</span>
              <span className="text-[#F5F5F5] font-medium">Studio 27</span>
            </div>
            <div className="flex justify-between">
              <span className="text-white/40">Barbeiro</span>
              <span className="text-[#F5F5F5] font-medium">Marcos</span>
            </div>
            <div className="flex justify-between">
              <span className="text-white/40">Serviço</span>
              <span className="text-[#F5F5F5] font-medium">Corte — R$ 45,00</span>
            </div>
            <hr className="border-white/5" />
            <div className="flex justify-between">
              <span className="text-white/40 flex items-center gap-1"><CalendarPlus className="h-4 w-4" /> Data</span>
              <span className="text-[#F5F5F5] font-medium">20 de Julho, 2026</span>
            </div>
            <div className="flex justify-between">
              <span className="text-white/40 flex items-center gap-1"><Clock className="h-4 w-4" /> Horário</span>
              <span className="text-[#F5F5F5] font-medium">14:30 (30 min)</span>
            </div>
            <div className="flex justify-between">
              <span className="text-white/40 flex items-center gap-1"><MapPin className="h-4 w-4" /> Endereço</span>
              <span className="text-[#F5F5F5] font-medium">Rua Augusta, 1234</span>
            </div>
          </div>
        </div>

        <div className="space-y-3">
          <button className="w-full rounded-full border border-white/10 py-3 text-sm font-medium text-white/60 hover:border-white/30 hover:text-white transition-all">
            Adicionar ao Google Calendar
          </button>
          <Link to="/" className="inline-flex items-center gap-2 text-sm text-white/30 hover:text-white/60 transition-colors">
            <ArrowLeft className="h-4 w-4" /> Voltar ao início
          </Link>
        </div>
      </motion.div>
    </div>
  );
}
