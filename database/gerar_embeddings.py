import psycopg2
from psycopg2.extras import RealDictCursor
from google import genai

client = genai.Client(api_key="AIzaSyAjPSlnWjiBnXZJuNbwap0Da3SpDHrA-Io")

conn = psycopg2.connect(
    host="sprint4-db.c7rd3jqs5wvx.us-east-1.rds.amazonaws.com",
    port="5432",
    dbname="flexmedia",
    user="postgres",
    password="jennie12"
)

cur = conn.cursor(cursor_factory=RealDictCursor)
cur.execute("SELECT id, titulo, conteudo FROM base_conhecimento WHERE embedding IS NULL")
docs = cur.fetchall()

print(f"Gerando embeddings para {len(docs)} documentos...")

for doc in docs:
    texto = f"{doc['titulo']}\n{doc['conteudo']}"
    result = client.models.embed_content(model="models/gemini-embedding-001", contents=texto)
    embedding = result.embeddings[0].values
    vector_str = "[" + ",".join(str(x) for x in embedding) + "]"
    cur.execute("UPDATE base_conhecimento SET embedding = %s::vector WHERE id = %s", (vector_str, doc["id"]))
    conn.commit()
    print(f"OK: {doc['titulo']}")

conn.close()
print("Pronto!")
