import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Scissors, Star, MapPin, Clock, ArrowRight } from "lucide-react";

const fadeUp = {
  hidden: { opacity: 0, y: 60 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.15, duration: 0.8, ease: [0.16, 1, 0.3, 1] },
  }),
};

const services = [
  { name: "Corte", price: "R$ 45", duration: "30 min", desc: "Tesoura, máquina e finalização." },
  { name: "Barba", price: "R$ 30", duration: "20 min", desc: "Toalha quente e navalhete." },
  { name: "Corte + Barba", price: "R$ 65", duration: "45 min", desc: "Combo completo." },
];

const team = [
  { name: "Marcos", role: "Master Barber", rating: 4.9 },
  { name: "Ricardo", role: "Senior Barber", rating: 4.7 },
  { name: "Lucas", role: "Style Specialist", rating: 4.8 },
  { name: "Rafael", role: "Creative Director", rating: 4.9 },
];

export function HomePage() {
  return (
    <div className="bg-[#0D0D0D]">
      {/* Hero */}
      <section className="relative flex min-h-screen items-center justify-center overflow-hidden px-6">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-[#0D0D0D]/50 to-[#0D0D0D]" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(215,38,56,0.15),transparent_70%)]" />
        
        <div className="relative z-10 mx-auto max-w-4xl text-center">
          <motion.div custom={0} initial="hidden" animate="visible" variants={fadeUp}>
            <p className="mb-4 text-sm font-semibold uppercase tracking-[0.3em] text-[#D72638]">
              São Paulo · Brasil
            </p>
          </motion.div>
          <motion.h1
            custom={1}
            initial="hidden"
            animate="visible"
            variants={fadeUp}
            className="text-display mb-6 text-[#F5F5F5]"
          >
            ONDE O ESTILO<br />
            <span className="text-[#D72638]">ENCONTRA A ARTE</span>
          </motion.h1>
          <motion.p
            custom={2}
            initial="hidden"
            animate="visible"
            variants={fadeUp}
            className="mx-auto mb-10 max-w-lg text-lg text-white/50"
          >
            Agende seu horário em menos de 2 minutos. Escolha seu barbeiro, serviço e horário.
          </motion.p>
          <motion.div custom={3} initial="hidden" animate="visible" variants={fadeUp} className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              to="/agendar"
              className="group inline-flex items-center gap-2 rounded-full bg-[#D72638] px-8 py-4 text-lg font-bold text-white transition-all duration-300 hover:scale-105 hover:bg-[#B81E2E] active:scale-95"
            >
              Agendar Agora
              <ArrowRight className="h-5 w-5 transition-transform group-hover:translate-x-1" />
            </Link>
            <Link
              to="/servicos"
              className="inline-flex items-center gap-2 rounded-full border border-white/10 px-8 py-4 text-lg font-medium text-white/60 transition-all duration-300 hover:border-white/30 hover:text-white"
            >
              Ver Serviços
            </Link>
          </motion.div>
        </div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.5, duration: 1 }}
          className="absolute bottom-8 left-1/2 -translate-x-1/2"
        >
          <div className="h-10 w-6 rounded-full border-2 border-white/20 flex justify-center">
            <motion.div
              animate={{ y: [0, 12, 0] }}
              transition={{ repeat: Infinity, duration: 1.5 }}
              className="mt-2 h-1.5 w-1.5 rounded-full bg-white/40"
            />
          </div>
        </motion.div>
      </section>

      {/* Services */}
      <section className="px-6 py-24">
        <div className="mx-auto max-w-6xl">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-16 text-center"
          >
            <p className="mb-3 text-sm font-semibold uppercase tracking-[0.2em] text-[#D72638]">Serviços</p>
            <h2 className="text-display-sm text-[#F5F5F5]">Excelência em cada detalhe</h2>
          </motion.div>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {services.map((svc, i) => (
              <motion.div
                key={svc.name}
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                whileHover={{ y: -4 }}
                className="group cursor-pointer rounded-2xl border border-white/5 bg-white/[0.02] p-8 transition-all duration-500 hover:border-[#D72638]/30 hover:bg-white/[0.04]"
              >
                <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-[#D72638]/10">
                  <Scissors className="h-5 w-5 text-[#D72638]" />
                </div>
                <h3 className="mb-2 text-xl font-bold text-[#F5F5F5]">{svc.name}</h3>
                <p className="mb-4 text-sm text-white/40">{svc.desc}</p>
                <div className="flex items-center justify-between">
                  <span className="text-2xl font-bold text-[#D72638]">{svc.price}</span>
                  <span className="flex items-center gap-1 text-sm text-white/30">
                    <Clock className="h-3.5 w-3.5" /> {svc.duration}
                  </span>
                </div>
              </motion.div>
            ))}
          </div>
          <div className="mt-10 text-center">
            <Link to="/servicos" className="inline-flex items-center gap-2 text-sm font-medium text-white/40 transition-colors hover:text-white">
              Ver todos os serviços <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* Team */}
      <section className="border-t border-white/5 px-6 py-24">
        <div className="mx-auto max-w-6xl">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-16 text-center"
          >
            <p className="mb-3 text-sm font-semibold uppercase tracking-[0.2em] text-[#D72638]">Equipe</p>
            <h2 className="text-display-sm text-[#F5F5F5]">Mestres do ofício</h2>
          </motion.div>
          <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
            {team.map((pro, i) => (
              <motion.div
                key={pro.name}
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="text-center group"
              >
                <div className="mx-auto mb-5 flex h-28 w-28 items-center justify-center rounded-full bg-white/[0.03] ring-1 ring-white/5 group-hover:ring-[#D72638]/30 transition-all duration-500">
                  <span className="text-3xl font-bold text-white/20 group-hover:text-[#D72638] transition-colors">
                    {pro.name[0]}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-[#F5F5F5]">{pro.name}</h3>
                <p className="text-sm text-white/40">{pro.role}</p>
                <div className="mt-2 flex items-center justify-center gap-1">
                  <Star className="h-3.5 w-3.5 fill-[#D72638] text-[#D72638]" />
                  <span className="text-sm font-medium text-white/60">{pro.rating}</span>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Location */}
      <section className="border-t border-white/5 px-6 py-24">
        <div className="mx-auto max-w-6xl text-center">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <p className="mb-3 text-sm font-semibold uppercase tracking-[0.2em] text-[#D72638]">Localização</p>
            <h2 className="text-display-sm mb-6 text-[#F5F5F5]">Onde Estamos</h2>
            <div className="flex items-center justify-center gap-2 text-white/50">
              <MapPin className="h-5 w-5 text-[#D72638]" />
              <span>Rua Augusta, 1234 — Consolação, São Paulo</span>
            </div>
            <div className="mt-8 mx-auto max-w-2xl h-64 rounded-2xl border border-white/5 bg-white/[0.02] flex items-center justify-center text-white/20">
              Google Maps
            </div>
          </motion.div>
        </div>
      </section>

      {/* CTA Final */}
      <section className="px-6 py-24">
        <div className="mx-auto max-w-3xl text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="rounded-3xl border border-white/5 bg-white/[0.02] p-16"
          >
            <h2 className="text-display-sm mb-4 text-[#F5F5F5]">Pronto para renovar seu visual?</h2>
            <p className="mb-8 text-white/40">Agende agora e transforme seu estilo.</p>
            <Link
              to="/agendar"
              className="inline-flex items-center gap-2 rounded-full bg-[#D72638] px-10 py-5 text-lg font-bold text-white transition-all duration-300 hover:scale-105 hover:bg-[#B81E2E]"
            >
              Agendar Agora <ArrowRight className="h-5 w-5" />
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
