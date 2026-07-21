# ============================================================
# CLAUDE-MEM Agent — Long-term memory & context
# Exposes standard agent interface on port 8005.
# ============================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import uuid
import asyncio

app = FastAPI(title="Claude-Mem Agent", version="0.1.0")

memories: Dict[str, List[Dict]] = {}
contexts: Dict[str, Dict] = {}


class StoreRequest(BaseModel):
    user_id: str
    memory: Dict[str, Any]
    tags: Optional[List[str]] = None
    importance: float = 0.5

class RetrieveRequest(BaseModel):
    user_id: str
    query: Optional[str] = None
    tags: Optional[List[str]] = None
    limit: int = 10

class LearnRequest(BaseModel):
    data: List[Dict[str, Any]]

class RetrieveResponse(BaseModel):
    user_id: str
    memories: List[Dict[str, Any]]
    total_found: int
    context_summary: Optional[str] = None


class ClaudeMemAgent:
    """Long-term memory agent with semantic retrieval."""

    async def store(self, request: StoreRequest) -> Dict:
        if request.user_id not in memories:
            memories[request.user_id] = []

        memory_entry = {
            "id": str(uuid.uuid4()),
            "content": request.memory,
            "tags": request.tags or [],
            "importance": request.importance,
            "stored_at": datetime.now(timezone.utc).isoformat(),
        }
        memories[request.user_id].append(memory_entry)

        # Update context
        contexts[request.user_id] = self._build_context(request.user_id)

        return {"status": "stored", "memory_id": memory_entry["id"], "total_memories": len(memories[request.user_id])}

    async def retrieve(self, request: RetrieveRequest) -> RetrieveResponse:
        await asyncio.sleep(0.08)

        user_memories = memories.get(request.user_id, [])
        results = user_memories

        if request.tags:
            results = [m for m in results if any(t in m.get("tags", []) for t in request.tags)]
        if request.query:
            results = [m for m in results if request.query.lower() in str(m["content"]).lower()]

        results = sorted(results, key=lambda m: m.get("importance", 0), reverse=True)[:request.limit]

        return RetrieveResponse(
            user_id=request.user_id,
            memories=results,
            total_found=len(results),
            context_summary=contexts.get(request.user_id, {}).get("summary"),
        )

    async def learn(self, data: List[Dict]) -> Dict:
        for item in data:
            uid = item.get("user_id", "global")
            if uid not in memories:
                memories[uid] = []
            memories[uid].append({
                "id": str(uuid.uuid4()),
                "content": item,
                "tags": item.get("tags", []),
                "importance": item.get("importance", 0.5),
                "stored_at": datetime.now(timezone.utc).isoformat(),
            })
        return {"status": "batch_stored", "items_processed": len(data)}

    def _build_context(self, user_id: str) -> Dict:
        user_memories = memories.get(user_id, [])
        if not user_memories:
            return {"summary": "No memories yet", "count": 0}

        high_value = [m for m in user_memories if m["importance"] >= 0.7]
        return {
            "summary": f"User has {len(user_memories)} memories ({len(high_value)} high-importance)",
            "count": len(user_memories),
            "last_updated": user_memories[-1]["stored_at"] if user_memories else None,
            "top_tags": self._extract_top_tags(user_memories),
        }

    def _extract_top_tags(self, mems: List[Dict]) -> List[str]:
        tag_counts: Dict[str, int] = {}
        for m in mems:
            for tag in m.get("tags", []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        return sorted(tag_counts, key=tag_counts.get, reverse=True)[:5]


agent = ClaudeMemAgent()


@app.post("/api/v1/store")
async def store_memory(request: StoreRequest):
    return await agent.store(request)


@app.post("/api/v1/process", response_model=RetrieveResponse)
async def retrieve_memory(request: RetrieveRequest):
    return await agent.retrieve(request)


@app.post("/api/v1/learn")
async def learn(request: LearnRequest):
    return await agent.learn(request.data)


@app.get("/api/v1/status")
async def status():
    total = sum(len(m) for m in memories.values())
    return {
        "agent": "Claude-Mem",
        "version": "0.1.0",
        "total_memories": total,
        "active_users": len(memories),
        "capabilities": ["memory_storage", "semantic_retrieval", "context_building", "preference_learning"],
    }


@app.get("/api/v1/health")
async def health():
    return {"status": "healthy", "agent": "Claude-Mem"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
