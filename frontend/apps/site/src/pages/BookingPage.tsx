import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Card, Input, cn, useToast } from "@barbershop/design-system";
import { ArrowLeft, ArrowRight, Check, User, Scissors, Calendar, Phone, Star } from "lucide-react";

type Step = 1 | 2 | 3 | 4;

interface BookingState {
  professionalId: string | null;
  professionalName: string | null;
  serviceId: string | null;
  serviceName: string | null;
  servicePrice: string | null;
  date: string | null;
  time: string | null;
  customerName: string;
  customerPhone: string;
  notes: string;
}

export function BookingPage() {
  const navigate = useNavigate();
  const { addToast } = useToast();
  const [step, setStep] = useState<Step>(1);
  const [state, setState] = useState<BookingState>({
    professionalId: null,
    professionalName: null,
    serviceId: null,
    serviceName: null,
    servicePrice: null,
    date: null,
    time: null,
    customerName: "",
    customerPhone: "",
    notes: "",
  });

  const update = (patch: Partial<BookingState>) => setState((s) => ({ ...s, ...patch }));

  const handleSubmit = () => {
    // API call would go here
    addToast({ type: "success", title: "Agendamento confirmado! 🎉", description: "20/07 às 14:30 com Marcos" });
    navigate("/confirmacao/demo123");
  };

  const steps = [
    { num: 1, label: "Profissional", icon: User },
    { num: 2, label: "Serviço", icon: Scissors },
    { num: 3, label: "Horário", icon: Calendar },
    { num: 4, label: "Dados", icon: Phone },
  ];

  const professionals = [
    { id: "1", name: "Qualquer profissional", description: "Disponível mais cedo", rating: null, special: true },
    { id: "2", name: "Marcos", description: "Especialista em degradê e tesoura", rating: 4.9 },
    { id: "3", name: "Ricardo", description: "Cortes clássicos e barba tradicional", rating: 4.7 },
    { id: "4", name: "Lucas", description: "Cortes modernos e design", rating: 4.8 },
  ];

  const services = [
    { id: "1", name: "Corte", price: "R$ 45,00", duration: "30 min" },
    { id: "2", name: "Barba", price: "R$ 30,00", duration: "20 min" },
    { id: "3", name: "Corte + Barba", price: "R$ 65,00", duration: "45 min", popular: true },
    { id: "4", name: "Hidratação", price: "R$ 40,00", duration: "25 min" },
  ];

  const morningSlots = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30"];
  const afternoonSlots = ["13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00"];

  return (
    <div className="min-h-screen bg-[#0D0D0D] pt-24 pb-24 px-6">
      <div className="mx-auto max-w-2xl">
      {/* Progress */}
      <div className="flex items-center justify-between mb-8">
        {steps.map((s) => (
          <div key={s.num} className="flex items-center gap-2">
            <div
              className={cn(
                "flex h-8 w-8 items-center justify-center rounded-full text-sm font-bold transition-colors",
                step > s.num
                  ? "bg-success text-white"
                  : step === s.num
                  ? "bg-primary text-white"
                  : "bg-surface-hover text-text-disabled"
              )}
            >
              {step > s.num ? <Check className="h-4 w-4" /> : s.num}
            </div>
            <span className={cn("text-xs font-medium hidden sm:block", step === s.num ? "text-primary" : "text-text-disabled")}>
              {s.label}
            </span>
            {s.num < 4 && <div className="hidden sm:block h-px w-6 bg-border mx-1" />}
          </div>
        ))}
      </div>

      {/* Summary bar */}
      {(state.professionalName || state.serviceName) && (
        <Card className="mb-6 flex items-center gap-4 text-sm">
          {state.professionalName && <span>💇 {state.professionalName}</span>}
          {state.serviceName && <span>✂️ {state.serviceName} — {state.servicePrice}</span>}
          {state.date && state.time && <span>📅 {state.date} às {state.time}</span>}
        </Card>
      )}

      {/* Step 1: Professional */}
      {step === 1 && (
        <div>
          <h2 className="text-xl font-bold mb-1">Escolha seu barbeiro</h2>
          <p className="text-sm text-text-secondary mb-6">Ou selecione "Qualquer profissional" para o primeiro horário disponível.</p>
          <div className="space-y-3">
            {professionals.map((pro) => (
              <Card
                key={pro.id}
                variant={state.professionalId === pro.id ? "selected" : "interactive"}
                onClick={() => update({ professionalId: pro.id, professionalName: pro.name })}
              >
                <div className="flex items-center gap-3">
                  <div className={cn("flex h-10 w-10 items-center justify-center rounded-full text-sm font-bold", pro.special ? "bg-success/10 text-success" : "bg-primary-light text-primary")}>
                    {pro.name[0]}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-medium">{pro.name}</p>
                    <p className="text-sm text-text-secondary">{pro.description}</p>
                    {pro.rating && <p className="text-xs text-warning">⭐ {pro.rating}</p>}
                  </div>
                  {state.professionalId === pro.id && <Check className="h-5 w-5 text-primary shrink-0" />}
                </div>
              </Card>
            ))}
          </div>
          <div className="flex gap-3 mt-6">
            <Button variant="ghost" onClick={() => update({ professionalId: "1", professionalName: "Qualquer profissional" })}>
              Pular etapa
            </Button>
            <div className="flex-1" />
            <Button onClick={() => setStep(2)} rightIcon={<ArrowRight className="h-4 w-4" />} disabled={!state.professionalId}>
              Continuar
            </Button>
          </div>
        </div>
      )}

      {/* Step 2: Service */}
      {step === 2 && (
        <div>
          <h2 className="text-xl font-bold mb-1">Escolha o serviço</h2>
          <p className="text-sm text-text-secondary mb-6">Selecione um ou mais serviços.</p>
          <div className="space-y-3">
            {services.map((svc) => (
              <Card
                key={svc.id}
                variant={state.serviceId === svc.id ? "selected" : "interactive"}
                onClick={() => update({ serviceId: svc.id, serviceName: svc.name, servicePrice: svc.price })}
                className="relative"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">{svc.name}</p>
                    <p className="text-sm text-text-secondary">⏱ {svc.duration}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-lg font-bold text-primary">{svc.price}</p>
                    {svc.popular && (
                      <span className="text-xs text-warning font-medium">Mais popular</span>
                    )}
                  </div>
                </div>
                {state.serviceId === svc.id && <Check className="absolute top-3 right-3 h-5 w-5 text-primary" />}
              </Card>
            ))}
          </div>
          <div className="flex gap-3 mt-6">
            <Button variant="ghost" leftIcon={<ArrowLeft className="h-4 w-4" />} onClick={() => setStep(1)}>
              Voltar
            </Button>
            <div className="flex-1" />
            <Button onClick={() => setStep(3)} rightIcon={<ArrowRight className="h-4 w-4" />} disabled={!state.serviceId}>
              Continuar
            </Button>
          </div>
        </div>
      )}

      {/* Step 3: Date & Time */}
      {step === 3 && (
        <div>
          <h2 className="text-xl font-bold mb-1">Escolha o horário</h2>
          <p className="text-sm text-text-secondary mb-6">Selecione a data e o horário.</p>

          {/* Date selector */}
          <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
            {["Hoje", "Amanhã", "Qua 23", "Qui 24", "Sex 25", "Sáb 26"].map((d, i) => (
              <button
                key={d}
                onClick={() => update({ date: d })}
                className={cn(
                  "shrink-0 px-4 py-2 rounded-md text-sm font-medium border transition-colors",
                  state.date === d
                    ? "border-primary bg-primary text-white"
                    : "border-border hover:border-primary hover:bg-primary/5"
                )}
              >
                {d}
              </button>
            ))}
          </div>

          {state.date && (
            <>
              <h3 className="text-sm font-semibold text-text-secondary mb-3">Manhã ☀️</h3>
              <div className="grid grid-cols-4 gap-2 mb-6">
                {morningSlots.map((slot) => {
                  const occupied = slot === "10:00";
                  return (
                    <button
                      key={slot}
                      disabled={occupied}
                      onClick={() => update({ time: slot })}
                      className={cn(
                        "py-2.5 rounded-md text-sm font-medium border transition-colors",
                        occupied && "bg-surface-hover text-text-disabled border-border cursor-not-allowed line-through",
                        state.time === slot && "border-primary bg-primary text-white",
                        !occupied && state.time !== slot && "border-border hover:border-primary"
                      )}
                    >
                      {slot}
                    </button>
                  );
                })}
              </div>

              <h3 className="text-sm font-semibold text-text-secondary mb-3">Tarde 🌤️</h3>
              <div className="grid grid-cols-4 gap-2 mb-6">
                {afternoonSlots.map((slot) => (
                  <button
                    key={slot}
                    onClick={() => update({ time: slot })}
                    className={cn(
                      "py-2.5 rounded-md text-sm font-medium border transition-colors",
                      state.time === slot
                        ? "border-primary bg-primary text-white"
                        : "border-border hover:border-primary"
                    )}
                  >
                    {slot}
                  </button>
                ))}
              </div>
            </>
          )}

          <div className="flex gap-3 mt-6">
            <Button variant="ghost" leftIcon={<ArrowLeft className="h-4 w-4" />} onClick={() => setStep(2)}>Voltar</Button>
            <div className="flex-1" />
            <Button onClick={() => setStep(4)} rightIcon={<ArrowRight className="h-4 w-4" />} disabled={!state.time}>Continuar</Button>
          </div>
        </div>
      )}

      {/* Step 4: Customer Data */}
      {step === 4 && (
        <div>
          <h2 className="text-xl font-bold mb-1">Seus dados</h2>
          <p className="text-sm text-text-secondary mb-6">Preencha para confirmar o agendamento.</p>

          {/* Summary recap */}
          <Card className="mb-6">
            <div className="space-y-2 text-sm">
              <div className="flex justify-between"><span className="text-text-secondary">Barbeiro:</span> <span className="font-medium">{state.professionalName}</span></div>
              <div className="flex justify-between"><span className="text-text-secondary">Serviço:</span> <span className="font-medium">{state.serviceName} — {state.servicePrice}</span></div>
              <div className="flex justify-between"><span className="text-text-secondary">Data:</span> <span className="font-medium">{state.date}</span></div>
              <div className="flex justify-between"><span className="text-text-secondary">Horário:</span> <span className="font-medium">{state.time}</span></div>
            </div>
          </Card>

          <div className="space-y-4">
            <Input
              label="Nome completo"
              placeholder="Seu nome"
              required
              value={state.customerName}
              onChange={(e) => update({ customerName: e.target.value })}
            />
            <Input
              label="WhatsApp"
              placeholder="(11) 99999-9999"
              required
              helperText="Enviaremos a confirmação e o lembrete por aqui."
              value={state.customerPhone}
              onChange={(e) => update({ customerPhone: e.target.value })}
            />
            <Input
              label="Observação (opcional)"
              placeholder="Ex: prefiro degradê baixo"
              value={state.notes}
              onChange={(e) => update({ notes: e.target.value })}
            />
            <label className="flex items-start gap-2 text-sm">
              <input type="checkbox" className="mt-1 rounded border-border" />
              <span>Li e aceito os termos de uso e política de privacidade.</span>
            </label>
          </div>

          <div className="flex gap-3 mt-6">
            <Button variant="ghost" leftIcon={<ArrowLeft className="h-4 w-4" />} onClick={() => setStep(3)}>Voltar</Button>
            <div className="flex-1" />
            <Button
              size="lg"
              onClick={handleSubmit}
              disabled={!state.customerName || !state.customerPhone}
            >
              Confirmar Agendamento
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
