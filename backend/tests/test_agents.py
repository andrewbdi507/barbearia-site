# ============================================================
# Agent Integration Tests
# ============================================================

import pytest
from unittest.mock import AsyncMock, patch
from app.integrations.agents import AgentOrchestrator, AgentResult


@pytest.fixture
def orchestrator():
    return AgentOrchestrator()


class TestAgentHealth:
    """Test agent health checks."""

    @pytest.mark.asyncio
    async def test_check_all_agents_disabled(self, orchestrator):
        """Agents should report disabled when all are disabled."""
        for agent in orchestrator.agents.values():
            agent.enabled = False
        result = await orchestrator.check_all_agents()
        assert result["total"] == 5
        assert result["healthy"] == 0

    @pytest.mark.asyncio
    async def test_get_agent_status_unknown(self, orchestrator):
        """Unknown agent should return error."""
        result = await orchestrator.get_agent_status("nonexistent")
        assert "error" in result


class TestHERMESPlanning:
    """Test Hermes agent planning capabilities."""

    @pytest.mark.asyncio
    async def test_hermes_plan_generation(self, orchestrator):
        """Hermes should generate a plan from a goal."""
        result = await orchestrator.execute_with_hermes(
            goal="Maximize barbershop occupancy",
            constraints={"max_hours": 8, "staff_count": 3},
        )
        assert result.agent == "hermes"

    @pytest.mark.asyncio
    async def test_hermes_empty_goal(self, orchestrator):
        """Hermes should handle empty goal gracefully."""
        result = await orchestrator.execute_with_hermes(goal="")
        assert result.agent == "hermes"


class TestEvolverOptimization:
    """Test Evolver agent strategy optimization."""

    @pytest.mark.asyncio
    async def test_evolver_pricing(self, orchestrator):
        """Evolver should optimize pricing based on metrics."""
        result = await orchestrator.evolve_strategy(
            target="service_pricing",
            metrics={"occupancy": 0.65, "revenue": 1200.0, "cost": 400.0},
        )
        assert result.agent == "evolver"


class TestANDReasoning:
    """Test AND agent reasoning capabilities."""

    @pytest.mark.asyncio
    async def test_and_pattern_analysis(self, orchestrator):
        """AND should analyze patterns from booking data."""
        result = await orchestrator.execute_with_and(
            task={"type": "booking_trends", "period": "weekly", "data_points": 150}
        )
        assert result.agent == "and"


class TestClaudeMemMemory:
    """Test Claude-Mem agent memory management."""

    @pytest.mark.asyncio
    async def test_store_and_retrieve(self, orchestrator):
        """Should store and retrieve customer preferences."""
        # Store
        stored = await orchestrator.store_memory(
            user_id="cust_123",
            memory={"preferred_barber": "Marcos", "last_service": "Corte + Barba"},
            tags=["preference", "booking"],
        )
        assert stored.agent == "claude-mem"

        # Retrieve
        retrieved = await orchestrator.memory_retrieval(
            user_id="cust_123",
            query="barber",
        )
        assert retrieved.agent == "claude-mem"


class TestWorkflowOrchestration:
    """Test multi-agent workflow execution."""

    @pytest.mark.asyncio
    async def test_booking_optimization_workflow(self, orchestrator):
        """Full workflow: AND → Hermes → Evolver."""
        workflow = {
            "name": "booking_optimization",
            "steps": [
                {"agent": "and", "action": "analyze_patterns", "payload": {"input": {"type": "trends"}}},
                {"agent": "hermes", "action": "optimize_schedule", "payload": {"goal": "Maximize slots"}},
                {"agent": "evolver", "action": "suggest_pricing", "payload": {"target": "pricing", "metrics": {"occ": 0.7}}},
            ],
        }
        result = await orchestrator.process_workflow(workflow)
        assert result["workflow"] == "booking_optimization"
        assert result["steps_completed"] == 3
