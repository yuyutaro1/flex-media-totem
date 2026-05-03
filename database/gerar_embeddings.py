import psycopg2
from psycopg2.extras import RealDictCursor
from google import genai

client = genai.Client(api_key="AIzaSyADytMW5KVDvNr1R9tUF2l-qlnKm6u_sOQ")

conn = psycopg2.connect(
    host="flex-media-db.clgcuigukvtv.us-east-1.rds.amazonaws.com",
    port="5432",
    dbname="flexmedia",
    user="postgres",
    password="Eunchae123"
)

cur = conn.cursor(cursor_factory=RealDictCursor)
cur.execute("SELECT id, titulo, conteudo FROM base_conhecimento WHERE embedding IS NULL")
docs = cur.fetchall()

print(f"Gerando embeddings para {len(docs)} documentos...")

for doc in docs:
    texto = f"{doc['titulo']}\n{doc['conteudo']}"
    result = client.models.embed_content(
        model="models/gemini-embedding-001",
        contents=texto
    )
    embedding = result.embeddings[0].values
    vector_str = "[" + ",".join(str(x) for x in embedding) + "]"
    cur.execute("UPDATE base_conhecimento SET embedding = %s::vector WHERE id = %s", (vector_str, doc["id"]))
    conn.commit()
    print(f"ok: {doc['titulo']}")

conn.close()
print("Pronto!")
