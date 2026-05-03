from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Pergunta(BaseModel):
    pergunta: str

@app.get("/")
def root():
    return {"status": "online", "servico": "Totem Flex Media"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/perguntar")
def perguntar(body: Pergunta):
    return {
        "resposta": "Em breve responderei com base no conhecimento interno.",
        "fontes": [],
        "status": "ok"
    }