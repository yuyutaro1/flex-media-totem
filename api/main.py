from fastapi import FastAPI
from pydantic import BaseModel
import os, psycopg2
from psycopg2.extras import RealDictCursor
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key="AIzaSyC2yPn-tTViuEe7662QK2m1pMbKifK-YA4")
app = FastAPI()

class Pergunta(BaseModel):
    pergunta: str

def get_db():
    return psycopg2.connect(host="flex-media-db.clgcuigukvtv.us-east-1.rds.amazonaws.com",port="5432",dbname="flexmedia",user="postgres",password="Eunchae123",cursor_factory=RealDictCursor)

def gerar_embedding(texto):
    result = client.models.embed_content(model="models/gemini-embedding-001",contents=texto)
    return result.embeddings[0].values

def buscar_documentos(embedding):
    vector_str = "[" + ",".join(str(x) for x in embedding) + "]"
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT titulo, conteudo FROM base_conhecimento ORDER BY embedding <=> %s::vector LIMIT 3",(vector_str,))
        docs = cur.fetchall()
    conn.close()
    return docs

def gerar_resposta(pergunta, docs):
    conteudos = [d["conteudo"] for d in docs]
    return " ".join(conteudos[:2])

@app.get("/")
def root():
    return {"status": "online", "servico": "Totem Flex Media"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/perguntar")
def perguntar(body: Pergunta):
    try:
        embedding = gerar_embedding(body.pergunta)
        docs = buscar_documentos(embedding)
        if not docs:
            return {"resposta": "Nao encontrei informacoes.", "fontes": [], "status": "sem_resultados"}
        resposta = gerar_resposta(body.pergunta, docs)
        fontes = list({d["titulo"] for d in docs})
        return {"resposta": resposta, "fontes": fontes, "status": "ok"}
    except Exception as e:
        return {"resposta": f"Erro: {str(e)}", "fontes": [], "status": "erro"}