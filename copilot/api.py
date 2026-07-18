from __future__ import annotations

import sys
from pathlib import Path

# Bring project root into scope path context
sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from copilot.graph import CopilotWorkflowGraph

app = FastAPI(title="SentinelIQ RAG Copilot Service API", version="1.0.0")

# Register CORS middleware natively (This completely manages preflights out-of-the-box)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

workflow_instance = CopilotWorkflowGraph().compile_graph()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    answer: str
    routing: str

@app.post("/api/v1/query", response_model=QueryResponse)
async def process_query(payload: QueryRequest):
    """Processes incoming prompt statements through the LangGraph engine workflow."""
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query prompt cannot be empty.")
    
    try:
        state = workflow_instance.invoke({"query": payload.query})
        return QueryResponse(
            query=state["query"],
            answer=state["generation_output"],
            routing=state["routing_decision"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal graph error: {str(e)}")

@app.get("/health")
async def health_check():
    """System health monitoring node point."""
    return {"status": "healthy", "service": "sentineliq-copilot"}