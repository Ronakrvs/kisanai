from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.rag import answer
from app.schemas import ChatRequest, ChatResponse

app = FastAPI(title="Farmer Chatbot Service", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["POST", "GET"], allow_headers=["*"])


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    resp = await answer(req.message, req.language)
    return ChatResponse(answer=resp, language=req.language)
