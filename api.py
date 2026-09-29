from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import os

from src.graph import run_graph, RAGGraph
from src.config import OLLAMA_MODEL, QDRANT_COLLECTION

app = FastAPI(
    title="DocuMind AI",
    description="Grounded RAG API for the Agentic AI knowledge base",
    version="1.0.0"
)

# Initialize graph runner globally to reuse components like the embedder and vector store
try:
    graph_runner = RAGGraph()
except Exception as e:
    print(f"Failed to initialize RAG pipeline: {e}")
    graph_runner = None

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, strip_whitespace=True)

class RetrievedContext(BaseModel):
    text: str
    source: str
    page: Optional[int]
    chunk_id: str
    score: float

class QueryResponse(BaseModel):
    question: str
    answer: str
    retrieved_context: List[RetrievedContext]
    retrieval_score: Optional[float]
    model: str
    status: str

@app.get("/")
def read_root():
    return {
        "name": "DocuMind AI",
        "description": "Grounded RAG API for the Agentic AI knowledge base",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "DocuMind AI",
        "model": OLLAMA_MODEL,
        "vector_database": "qdrant",
        "collection": QDRANT_COLLECTION
    }

@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    if not graph_runner:
        raise HTTPException(status_code=500, detail="RAG pipeline is not initialized properly.")
        
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
        
    try:
        # Call the existing LangGraph pipeline
        state = graph_runner.run(question)
        
        has_context = state.get("has_context", False)
        answer = state.get("answer", "")
        raw_context = state.get("retrieved_context", [])
        
        formatted_context = []
        retrieval_score = None
        
        if has_context and raw_context:
            for item in raw_context:
                formatted_context.append(RetrievedContext(
                    text=item.get("text", ""),
                    source=item.get("source", ""),
                    page=item.get("page"),
                    chunk_id=item.get("chunk_id", ""),
                    score=item.get("score", 0.0)
                ))
            
            # Find the highest retrieval score
            scores = [item.score for item in formatted_context]
            retrieval_score = max(scores) if scores else None
            status = "success"
        else:
            status = "no_context"
            
        return QueryResponse(
            question=question,
            answer=answer,
            retrieved_context=formatted_context,
            retrieval_score=retrieval_score,
            model=OLLAMA_MODEL,
            status=status
        )
        
    except Exception as e:
        # Do not expose the full stack trace to the API response
        raise HTTPException(status_code=500, detail="An internal server error occurred while processing the request.")
