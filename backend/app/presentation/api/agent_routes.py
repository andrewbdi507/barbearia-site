# ============================================================
# Agent Routes — REST API for Multi-Agent Integration
# ============================================================

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

from app.integrations.agents import get_agent_orchestrator, AgentOrchestrator

agent_router = APIRouter(prefix="/agents", tags=["AI Agents"])


# ---- Request/Response Models ----

class TaskRequest(BaseModel):
    input: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None


class PlanRequest(BaseModel):
    goal: str
    constraints: Optional[Dict[str, Any]] = None


class OptimizeRequest(BaseModel):
    target: str
    metrics: Dict[str, float]


class OrchestrateRequest(BaseModel):
    tasks: List[Dict[str, Any]]
    workflow_name: str = "default"


class MemoryRetrieveRequest(BaseModel):
    user_id: str
    query: Optional[str] = None


class MemoryStoreRequest(BaseModel):
    user_id: str
    memory: Dict[str, Any]
    tags: Optional[List[str]] = None


class WorkflowRequest(BaseModel):
    name: str
    steps: List[Dict[str, Any]]


class AgentHealthResponse(BaseModel):
    agents: Dict[str, Any]
    total: int
    healthy: int


# ---- Endpoints ----

@agent_router.get("/health", response_model=AgentHealthResponse)
async def agents_health(
    orchestrator: AgentOrchestrator = Depends(get_agent_orchestrator),
):
    """Health check for all AI agents."""
    return await orchestrator.check_all_agents()


@agent_router.get("/{agent_id}/status")
async def agent_status(
    agent_id: str,
    orchestrator: AgentOrchestrator = Depends(get_agent_orchestrator),
):
    """Get detailed status from a specific agent."""
    result = await orchestrator.get_agent_status(agent_id)
    if "error" in result:
        raise HTTPException(404, result["error"])
    return result


# ---- AND Agent ----
@agent_router.post("/and/execute")
async def and_execute(
    body: TaskRequest,
    orchestrator: AgentOrchestrator = Depends(get_agent_orchestrator),
):
    """Execute reasoning/analysis with AND agent."""
    result = await orchestrator.execute_with_and(body.input)
    if result.error:
        raise HTTPException(502, f"AND agent error: {result.error}")
    return result.data


# ---- Hermes Agent ----
@agent_router.post("/hermes/plan")
async def hermes_plan(
    body: PlanRequest,
    orchestrator: AgentOrchestrator = Depends(get_agent_orchestrator),
):
    """Plan and optimize with Hermes agent."""
    result = await orchestrator.execute_with_hermes(body.goal, body.constraints)
    if result.error:
        raise HTTPException(502, f"Hermes agent error: {result.error}")
    return result.data


# ---- Evolver Agent ----
@agent_router.post("/evolver/optimize")
async def evolver_optimize(
    body: OptimizeRequest,
    orchestrator: AgentOrchestrator = Depends(get_agent_orchestrator),
):
    """Optimize strategy with Evolver agent."""
    result = await orchestrator.evolve_strategy(body.target, body.metrics)
    if result.error:
        raise HTTPException(502, f"Evolver agent error: {result.error}")
    return result.data


# ---- Generic Agent ----
@agent_router.post("/generic/orchestrate")
async def generic_orchestrate(
    body: OrchestrateRequest,
    orchestrator: AgentOrchestrator = Depends(get_agent_orchestrator),
):
    """Orchestrate tasks with Generic agent."""
    result = await orchestrator.generic_orchestration(body.tasks)
    if result.error:
        raise HTTPException(502, f"Generic agent error: {result.error}")
    return result.data


# ---- Claude-Mem Agent ----
@agent_router.post("/claude-mem/retrieve")
async def claude_mem_retrieve(
    body: MemoryRetrieveRequest,
    orchestrator: AgentOrchestrator = Depends(get_agent_orchestrator),
):
    """Retrieve memories from Claude-Mem agent."""
    result = await orchestrator.memory_retrieval(body.user_id, body.query)
    if result.error:
        raise HTTPException(502, f"Claude-Mem agent error: {result.error}")
    return result.data


@agent_router.post("/claude-mem/store")
async def claude_mem_store(
    body: MemoryStoreRequest,
    orchestrator: AgentOrchestrator = Depends(get_agent_orchestrator),
):
    """Store a memory in Claude-Mem agent."""
    result = await orchestrator.store_memory(body.user_id, body.memory, body.tags)
    if result.error:
        raise HTTPException(502, f"Claude-Mem agent error: {result.error}")
    return result.data


# ---- Multi-Agent Workflow ----
@agent_router.post("/workflow")
async def run_workflow(
    body: WorkflowRequest,
    orchestrator: AgentOrchestrator = Depends(get_agent_orchestrator),
):
    """Execute a multi-agent workflow."""
    return await orchestrator.process_workflow(body.model_dump())
