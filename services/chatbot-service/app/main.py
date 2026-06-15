from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.rag import RAGPipeline
from app.schemas import ChatRequest, ChatResponse
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.rag = RAGPipeline(
        db_url=os.getenv("DATABASE_URL"),
        llm_model=os.getenv("LLM_MODEL", "llama3"),
        embed_model=os.getenv("EMBED_MODEL", "BAAI/bge-small-en-v1.5"),
    )
    app.state.rag.init()
    yield


app = FastAPI(title="Farmer Chatbot Service", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["POST", "GET"], allow_headers=["*"])


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    rag: RAGPipeline = app.state.rag
    answer = rag.answer(req.message, req.language)
    return ChatResponse(answer=answer, language=req.language)
