// ============================================================
// IA & Agentes — Admin Page
// Dashboard for managing all 5 AI agents.
// ============================================================

import { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, Badge, Button } from "@barbershop/design-system";
import {
  Brain,
  Bot,
  TrendingUp,
  Workflow,
  Database,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Play,
  RefreshCw,
  Loader2,
} from "lucide-react";
import { agentsAPI } from "../lib/api";

interface AgentStatus {
  name: string;
  icon: typeof Brain;
  description: string;
  useCase: string;
  port: number;
  status: "healthy" | "offline" | "degraded" | "disabled" | "loading";
  latency_ms?: number;
  capabilities: string[];
}

const agentDefinitions: AgentStatus[] = [
  {
    name: "AND",
    icon: Brain,
    description: "Raciocínio avançado e aprendizado contínuo",
    useCase: "IA Agenda — Aprende padrões de agendamento",
    port: 8001,
    status: "loading",
    capabilities: ["pattern_recognition", "reasoning", "learning"],
  },
  {
    name: "Hermes",
    icon: Bot,
    description: "Planejamento e execução autônoma",
    useCase: "IA Agenda — Otimiza horários automaticamente",
    port: 8002,
    status: "loading",
    capabilities: ["planning", "execution", "scheduling"],
  },
  {
    name: "Evolver",
    icon: TrendingUp,
    description: "Evolução e adaptação de estratégias",
    useCase: "IA Preço — Sugere preços dinâmicos",
    port: 8003,
    status: "loading",
    capabilities: ["evolution", "optimization", "pricing"],
  },
  {
    name: "Generic",
    icon: Workflow,
    description: "Orquestração de tarefas",
    useCase: "IA Atendimento — Chatbot para clientes",
    port: 8004,
    status: "loading",
    capabilities: ["orchestration", "chatbot", "automation"],
  },
  {
    name: "Claude-Mem",
    icon: Database,
    description: "Memória de longo prazo e contexto",
    useCase: "IA Memória — Preferências de clientes",
    port: 8005,
    status: "loading",
    capabilities: ["memory", "retrieval", "preferences"],
  },
];

const statusConfig: Record<string, { icon: typeof CheckCircle; color: string; label: string }> = {
  healthy: { icon: CheckCircle, color: "text-success", label: "Online" },
  offline: { icon: XCircle, color: "text-error", label: "Offline" },
  degraded: { icon: AlertTriangle, color: "text-warning", label: "Degradado" },
  disabled: { icon: XCircle, color: "text-text-disabled", label: "Desativado" },
  loading: { icon: Loader2, color: "text-info", label: "Verificando..." },
};

export default function AgentsPage() {
  const [agents, setAgents] = useState<AgentStatus[]>(agentDefinitions);
  const [workflowResult, setWorkflowResult] = useState<string | null>(null);
  const [running, setRunning] = useState(false);

  useEffect(() => {
    checkAgents();
  }, []);

  async function checkAgents() {
    setAgents((prev) => prev.map((a) => ({ ...a, status: "loading" as const })));
    try {
      const res = await agentsAPI.health();
      const statuses = res.agents || {};
      setAgents((prev) =>
        prev.map((agent) => {
          const key = agent.name.toLowerCase().replace("-", "_").replace(" ", "-");
          const status = statuses[agent.name.toLowerCase()] || statuses[key];
          return {
            ...agent,
            status: status?.status || "offline",
            latency_ms: status?.latency_ms,
          };
        })
      );
    } catch {
      setAgents((prev) => prev.map((a) => ({ ...a, status: "offline" as const })));
    }
  }

  async function runWorkflow() {
    setRunning(true);
    setWorkflowResult("Executando workflow multi-agente...");
    try {
      const result = await agentsAPI.runWorkflow({
        name: "booking_optimization",
        steps: [
          { agent: "and", action: "analyze_patterns", payload: { input: { type: "booking_trends" } } },
          { agent: "hermes", action: "optimize_schedule", payload: { goal: "Maximize occupancy" } },
          { agent: "evolver", action: "suggest_pricing", payload: { target: "service_pricing", metrics: { occupancy: 0.65, revenue: 1200 } } },
        ],
      });
      setWorkflowResult(JSON.stringify(result, null, 2));
    } catch (e: any) {
      setWorkflowResult(`Erro: ${e.message}`);
    }
    setRunning(false);
  }

  const healthyCount = agents.filter((a) => a.status === "healthy").length;

  return (
    <div className="animate-fade-in p-6 max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-text-primary">IA & Agentes</h1>
          <p className="text-text-secondary mt-1">
            Gerencie os agentes de inteligência artificial integrados ao ecossistema.
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={checkAgents} leftIcon={<RefreshCw className="h-4 w-4" />}>
            Verificar
          </Button>
          <Button size="sm" onClick={runWorkflow} loading={running} leftIcon={<Play className="h-4 w-4" />}>
            Testar Workflow
          </Button>
        </div>
      </div>

      {/* Status Summary */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mb-6">
        <Card variant="stat">
          <p className="text-2xl font-bold text-primary">{healthyCount}/{agents.length}</p>
          <p className="text-xs text-text-secondary">Online</p>
        </Card>
        {agents.slice(0, 4).map((agent) => (
          <Card key={agent.name} variant="stat">
            <div className="flex items-center justify-center gap-1.5">
              <span className={`h-2 w-2 rounded-full ${
                agent.status === "healthy" ? "bg-success" :
                agent.status === "degraded" ? "bg-warning" :
                agent.status === "loading" ? "bg-info animate-pulse" : "bg-error"
              }`} />
              <p className="text-sm font-semibold">{agent.name}</p>
            </div>
            <p className="text-xs text-text-secondary mt-1">
              {agent.latency_ms ? `${agent.latency_ms}ms` : statusConfig[agent.status]?.label}
            </p>
          </Card>
        ))}
      </div>

      {/* Agent Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {agents.map((agent) => {
          const Icon = agent.icon;
          const status = statusConfig[agent.status] || statusConfig.offline;
          const StatusIcon = status.icon;

          return (
            <Card key={agent.name} variant={agent.status === "healthy" ? "default" : "interactive"}>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                      <Icon className="h-5 w-5 text-primary" />
                    </div>
                    <div>
                      <CardTitle>{agent.name}</CardTitle>
                      <p className="text-xs text-text-secondary">Porta {agent.port}</p>
                    </div>
                  </div>
                  <Badge className={`${status.color} bg-transparent border-current`}>
                    <StatusIcon className="h-3 w-3 mr-1" />
                    {status.label}
                  </Badge>
                </div>
              </CardHeader>

              <p className="text-sm text-text-secondary mb-3">{agent.description}</p>

              <div className="bg-surface-hover rounded-md p-2 mb-3">
                <p className="text-xs font-medium text-primary mb-1">💡 Caso de Uso</p>
                <p className="text-xs text-text-secondary">{agent.useCase}</p>
              </div>

              <div className="flex flex-wrap gap-1">
                {agent.capabilities.map((cap) => (
                  <Badge key={cap} className="bg-primary/5 text-primary text-[10px]">
                    {cap.replace(/_/g, " ")}
                  </Badge>
                ))}
              </div>
            </Card>
          );
        })}
      </div>

      {/* Workflow Result */}
      {workflowResult && (
        <Card className="mt-6">
          <CardHeader>
            <CardTitle>📋 Resultado do Workflow</CardTitle>
          </CardHeader>
          <pre className="bg-surface-hover rounded-md p-4 text-xs text-text-secondary overflow-auto max-h-64">
            {workflowResult}
          </pre>
        </Card>
      )}
    </div>
  );
}
