import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database.database import Database
from src.database.tables import Tabela

from src.router import router

app = FastAPI(
    title="API Sistema de Doação e Voluntariado",
    description="API para gestão de doações, voluntariado e distribuição de auxílio.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = Database()
tb = Tabela()

tb.criar_tabelas(db)

app.include_router(router)

@app.get("/", tags=["Health Check"])
def health_check():
    return {
        "status": "online",
        "mensagem": "Sistema de Gestão de Doações e Voluntariado a funcionar perfeitamente!"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)