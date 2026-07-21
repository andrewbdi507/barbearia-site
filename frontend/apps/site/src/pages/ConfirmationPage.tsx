import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { Button, Card } from "@barbershop/design-system";
import { CheckCircle, CalendarPlus, MapPin, Clock } from "lucide-react";

export function ConfirmationPage() {
  return (
    <div className="min-h-screen bg-[#0D0D0D] pt-24 pb-24 px-6 flex items-center justify-center">
      <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }}
        className="max-w-lg w-full text-center">
      {/* Success Icon */}
      <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-success/10">
        <CheckCircle className="h-10 w-10 text-success" />
      </div>

      <h1 className="text-2xl font-bold mb-2">Agendamento Confirmado!</h1>
      <p className="text-text-secondary mb-8">Você receberá a confirmação no WhatsApp em instantes.</p>

      {/* Details Card */}
      <Card className="mb-6 text-left">
        <div className="space-y-3">
          <div className="flex justify-between text-sm">
            <span className="text-text-secondary">Barbearia</span>
            <span className="font-medium">Studio 27</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-text-secondary">Barbeiro</span>
            <span className="font-medium">Marcos</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-text-secondary">Serviço</span>
            <span className="font-medium">Corte — R$ 45,00</span>
          </div>
          <hr className="border-border" />
          <div className="flex justify-between text-sm">
            <span className="text-text-secondary flex items-center gap-1"><CalendarPlus className="h-4 w-4" /> Data</span>
            <span className="font-medium">20 de Julho de 2026 (Segunda)</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-text-secondary flex items-center gap-1"><Clock className="h-4 w-4" /> Horário</span>
            <span className="font-medium">14:30 (30 min)</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-text-secondary flex items-center gap-1"><MapPin className="h-4 w-4" /> Endereço</span>
            <span className="font-medium">Rua Augusta, 1234</span>
          </div>
        </div>
      </Card>

      {/* Actions */}
      <div className="space-y-3">
        <Button fullWidth variant="outline" leftIcon={<CalendarPlus className="h-4 w-4" />}>
          Adicionar ao Google Calendar
        </Button>
        <Button fullWidth variant="outline" leftIcon={<CalendarPlus className="h-4 w-4" />}>
          Adicionar ao Apple Calendar
        </Button>
        <Link to="/">
          <Button fullWidth variant="ghost">Voltar ao site</Button>
        </Link>
      </div>
    </div>
  );
}
