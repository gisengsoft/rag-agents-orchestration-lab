
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="RAG Agents Orchestration Lab")

class AskRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "ok", "service": "rag-agents-orchestration-lab"}

@app.get("/health")
def health():
    return {"healthy": True}

@app.post("/ask")
def ask(req: AskRequest):
    return {"answer": f"Você perguntou: {req.question}. (RAG/Agentes serão ativados na próxima etapa)"}