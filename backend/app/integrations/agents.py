# ============================================================
# Agent Orchestrator — Multi-Agent Integration Layer
# Coordinates 5 AI agents for SaaS business optimization.
# ============================================================

from __future__ import annotations

import httpx
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum

from app.core.config import get_settings


class AgentStatus(str, Enum):
    ONLINE = "healthy"
    OFFLINE = "offline"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"


@dataclass
class AgentConfig:
    name: str
    url: str
    enabled: bool
    timeout: int = 30
    retries: int = 3

    @property
    def base_url(self) -> str:
        return self.url.rstrip("/")


@dataclass
class AgentResult:
    agent: str
    status: str
    data: Dict[str, Any]
    error: Optional[str] = None
    latency_ms: float = 0.0


class AgentOrchestrator:
    """Orchestrates communication with all 5 AI agents.

    Each agent exposes a standard REST API:
      POST /api/v1/process  — Process a task
      POST /api/v1/learn    — Learn from data
      GET  /api/v1/status   — Agent status
      GET  /api/v1/health   — Health check
    """

    def __init__(self):
        settings = get_settings()
        self.agents: Dict[str, AgentConfig] = {
            "and": AgentConfig(
                name="AND",
                url=getattr(settings, "and_agent_url", "http://and-agent:8000"),
                enabled=getattr(settings, "and_agent_enabled", True),
            ),
            "hermes": AgentConfig(
                name="Hermes",
                url=getattr(settings, "hermes_agent_url", "http://hermes-agent:8000"),
                enabled=getattr(settings, "hermes_agent_enabled", True),
            ),
            "evolver": AgentConfig(
                name="Evolver",
                url=getattr(settings, "evolver_url", "http://evolver-agent:8000"),
                enabled=getattr(settings, "evolver_enabled", True),
            ),
            "generic": AgentConfig(
                name="Generic",
                url=getattr(settings, "generic_agent_url", "http://generic-agent:8000"),
                enabled=getattr(settings, "generic_agent_enabled", True),
            ),
            "claude-mem": AgentConfig(
                name="Claude-Mem",
                url=getattr(settings, "claude_mem_url", "http://claude-mem-agent:8000"),
                enabled=getattr(settings, "claude_mem_enabled", True),
            ),
        }
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0),
                limits=httpx.Limits(max_keepalive_connections=10),
            )
        return self._client

    # ---- Health Checks ----

    async def check_all_agents(self) -> Dict[str, Any]:
        """Check health of all configured agents."""
        import time

        results = {}
        for agent_id, config in self.agents.items():
            if not config.enabled:
                results[agent_id] = "disabled"
                continue

            try:
                client = await self._get_client()
                start = time.monotonic()
                resp = await client.get(f"{config.base_url}/api/v1/health")
                latency = (time.monotonic() - start) * 1000

                if resp.status_code == 200:
                    data = resp.json()
                    results[agent_id] = {
                        "status": data.get("status", "healthy"),
                        "agent": data.get("agent", config.name),
                        "latency_ms": round(latency, 1),
                    }
                else:
                    results[agent_id] = {"status": "degraded", "http_status": resp.status_code}
            except Exception as e:
                results[agent_id] = {"status": "offline", "error": str(e)}

        return {
            "agents": results,
            "total": len(results),
            "healthy": sum(1 for v in results.values() if isinstance(v, dict) and v.get("status") == "healthy"),
        }

    async def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Get detailed status from a specific agent."""
        config = self.agents.get(agent_id)
        if not config:
            return {"error": f"Unknown agent: {agent_id}"}
        if not config.enabled:
            return {"status": "disabled", "agent": config.name}

        try:
            client = await self._get_client()
            resp = await client.get(f"{config.base_url}/api/v1/status")
            return resp.json() if resp.status_code == 200 else {"error": f"HTTP {resp.status_code}"}
        except Exception as e:
            return {"status": "offline", "error": str(e)}

    # ---- Task Execution ----

    async def _call_agent(
        self, agent_id: str, endpoint: str, payload: Dict[str, Any]
    ) -> AgentResult:
        """Internal: call an agent endpoint with error handling."""
        import time

        config = self.agents.get(agent_id)
        if not config or not config.enabled:
            return AgentResult(agent=agent_id, status="disabled", data={}, error="Agent disabled")

        try:
            client = await self._get_client()
            start = time.monotonic()
            resp = await client.post(
                f"{config.base_url}{endpoint}",
                json=payload,
                timeout=config.timeout,
            )
            latency = (time.monotonic() - start) * 1000
            resp.raise_for_status()
            return AgentResult(
                agent=agent_id,
                status="success",
                data=resp.json(),
                latency_ms=round(latency, 1),
            )
        except httpx.HTTPStatusError as e:
            return AgentResult(
                agent=agent_id,
                status="error",
                data={},
                error=f"HTTP {e.response.status_code}: {e.response.text[:200]}",
            )
        except Exception as e:
            return AgentResult(agent=agent_id, status="error", data={}, error=str(e))

    # ---- Public API Methods ----

    async def execute_with_and(self, task: Dict[str, Any]) -> AgentResult:
        """Execute reasoning task with AND agent (pattern analysis)."""
        return await self._call_agent("and", "/api/v1/process", {"input": task})

    async def execute_with_hermes(self, goal: str, constraints: Optional[Dict] = None) -> AgentResult:
        """Plan with Hermes agent (scheduling optimization)."""
        payload = {"goal": goal}
        if constraints:
            payload["constraints"] = constraints
        return await self._call_agent("hermes", "/api/v1/process", payload)

    async def evolve_strategy(self, target: str, metrics: Dict[str, float]) -> AgentResult:
        """Optimize strategy with Evolver agent (pricing, resources)."""
        return await self._call_agent(
            "evolver",
            "/api/v1/process",
            {"target": target, "metrics": metrics, "generations": 5},
        )

    async def generic_orchestration(self, tasks: List[Dict]) -> AgentResult:
        """Orchestrate multiple tasks with Generic agent."""
        return await self._call_agent(
            "generic",
            "/api/v1/process",
            {"workflow_name": "saas_workflow", "tasks": tasks},
        )

    async def memory_retrieval(self, user_id: str, query: Optional[str] = None) -> AgentResult:
        """Retrieve memories/preferences with Claude-Mem agent."""
        payload: Dict[str, Any] = {"user_id": user_id, "limit": 10}
        if query:
            payload["query"] = query
        return await self._call_agent("claude-mem", "/api/v1/process", payload)

    async def store_memory(self, user_id: str, memory: Dict, tags: Optional[List[str]] = None) -> AgentResult:
        """Store a memory in Claude-Mem agent."""
        return await self._call_agent(
            "claude-mem",
            "/api/v1/store",
            {"user_id": user_id, "memory": memory, "tags": tags or []},
        )

    # ---- Workflow Orchestration ----

    async def process_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a multi-agent workflow.

        Example workflow:
        {
            "name": "booking_optimization",
            "steps": [
                {"agent": "and", "action": "analyze_patterns"},
                {"agent": "hermes", "action": "optimize_schedule"},
                {"agent": "evolver", "action": "suggest_pricing"},
            ]
        }
        """
        results = []
        for step in workflow.get("steps", []):
            agent = step.get("agent")
            action = step.get("action")
            payload = step.get("payload", {})

            if agent == "and":
                result = await self.execute_with_and(payload)
            elif agent == "hermes":
                result = await self.execute_with_hermes(
                    goal=payload.get("goal", "Optimize schedule"),
                    constraints=payload.get("constraints"),
                )
            elif agent == "evolver":
                result = await self.evolve_strategy(
                    target=payload.get("target", "pricing"),
                    metrics=payload.get("metrics", {}),
                )
            elif agent == "generic":
                result = await self.generic_orchestration(payload.get("tasks", []))
            elif agent == "claude-mem":
                result = await self.memory_retrieval(
                    user_id=payload.get("user_id", "unknown"),
                    query=payload.get("query"),
                )
            else:
                result = AgentResult(agent=agent, status="skipped", data={}, error=f"Unknown agent: {agent}")

            results.append({
                "agent": agent,
                "action": action,
                "status": result.status,
                "data": result.data,
                "latency_ms": result.latency_ms,
                "error": result.error,
            })

        return {
            "workflow": workflow.get("name", "unnamed"),
            "steps_completed": len(results),
            "results": results,
        }

    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None


# ---- Singleton ----
_orchestrator: Optional[AgentOrchestrator] = None


def get_agent_orchestrator() -> AgentOrchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = AgentOrchestrator()
    return _orchestrator
