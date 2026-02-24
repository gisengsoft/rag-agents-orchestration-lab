import os
from fastapi import FastAPI
from pydantic import BaseModel

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

app = FastAPI(title="RAG Agents Orchestration Lab")

class AskRequest(BaseModel):
    question: str

def get_db_engine() -> Engine:
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    instance_conn = os.environ["INSTANCE_CONNECTION_NAME"]

    # Cloud SQL Postgres via Unix socket no Cloud Run
    socket_dir = f"/cloudsql/{instance_conn}"

    # Observação: sem host/porta TCP; usa socket
    db_url = f"postgresql+psycopg2://{db_user}:{db_pass}@/{db_name}?host={socket_dir}"

    return create_engine(db_url, pool_pre_ping=True)

@app.get("/")
def root():
    return {"status": "ok", "service": "rag-agents-orchestration-lab"}

@app.get("/health")
def health():
    return {"healthy": True}

@app.get("/db/ping")
def db_ping():
    engine = get_db_engine()
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"db": "ok"}

@app.post("/ask")
def ask(req: AskRequest):
    engine = get_db_engine()
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS questions (
                id SERIAL PRIMARY KEY,
                question TEXT NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """))
        conn.execute(
            text("INSERT INTO questions (question) VALUES (:q)"),
            {"q": req.question},
        )
        n = conn.execute(text("SELECT COUNT(*) FROM questions")).scalar_one()

    return {"answer": f"Você perguntou: {req.question}. (DB ok, total perguntas={n})"}