# ============================================================
# GENERIC Agent — Task orchestration base framework
# Exposes standard agent interface on port 8004.
# ============================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import uuid
import asyncio

app = FastAPI(title="Generic Agent", version="0.1.0")

workflows: Dict[str, Dict] = {}
tasks: Dict[str, Dict] = {}


class OrchestrateRequest(BaseModel):
    workflow_name: str
    tasks: List[Dict[str, Any]]
    dependencies: Optional[Dict[str, List[str]]] = None
    parallel: bool = False

class TaskExecuteRequest(BaseModel):
    task_spec: Dict[str, Any]

class LearnRequest(BaseModel):
    data: List[Dict[str, Any]]


class GenericAgent:
    """Base agent framework for task orchestration."""

    async def orchestrate(self, request: OrchestrateRequest) -> Dict:
        workflow_id = str(uuid.uuid4())
        results = []

        if request.parallel:
            coros = [self._execute_task(t) for t in request.tasks]
            results = await asyncio.gather(*coros)
        else:
            for task_spec in request.tasks:
                result = await self._execute_task(task_spec)
                results.append(result)

        workflow = {
            "workflow_id": workflow_id,
            "workflow_name": request.workflow_name,
            "tasks": results,
            "completed_at": datetime.now(timezone.utc).isoformat(),
        }
        workflows[workflow_id] = workflow

        return {
            "workflow_id": workflow_id,
            "status": "completed",
            "tasks_completed": len(results),
            "results": results,
        }

    async def process_single(self, task_spec: Dict) -> Dict:
        """Process a single task."""
        task_id = str(uuid.uuid4())
        await asyncio.sleep(0.06)

        result = {
            "task_id": task_id,
            "type": task_spec.get("type", "generic"),
            "action": task_spec.get("action", "process"),
            "status": "completed",
            "output": f"Processed: {task_spec.get('action', 'unknown')}",
        }
        tasks[task_id] = result
        return result

    async def _execute_task(self, task_spec: Dict) -> Dict:
        return await self.process_single(task_spec)

    async def learn(self, data: List[Dict]) -> Dict:
        return {"status": "learned", "tasks_registered": len(data)}


agent = GenericAgent()


@app.post("/api/v1/process")
async def process_task(request: OrchestrateRequest):
    return await agent.orchestrate(request)


@app.post("/api/v1/execute")
async def execute_single(request: TaskExecuteRequest):
    return await agent.process_single(request.task_spec)


@app.post("/api/v1/learn")
async def learn(request: LearnRequest):
    return await agent.learn(request.data)


@app.get("/api/v1/status")
async def status():
    return {
        "agent": "Generic",
        "version": "0.1.0",
        "active_workflows": len(workflows),
        "tasks_processed": len(tasks),
        "capabilities": ["orchestration", "task_execution", "chatbot", "automation"],
    }


@app.get("/api/v1/health")
async def health():
    return {"status": "healthy", "agent": "Generic"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
