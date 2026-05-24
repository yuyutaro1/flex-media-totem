import json
import time
import random
import datetime
import psycopg2

conn = psycopg2.connect(
    host="sprint4-db.c7rd3jqs5wvx.us-east-1.rds.amazonaws.com",
    port="5432",
    dbname="flexmedia",
    user="postgres",
    password="jennie12"
)

contador = 0
print("Simulador ESP32 iniciado! Enviando dados...")

while True:
    distancia = random.uniform(30, 200)
    movimento = distancia < 100
    
    if movimento:
        contador += 1
    
    dado = {
        "device_id": "totem-flex-01",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "distancia_cm": round(distancia, 2),
        "movimento_detectado": movimento,
        "contador_passagens": contador
    }
    
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO leituras_iot (device_id, distancia_cm, movimento_detectado, contador_passagens)
            VALUES (%s, %s, %s, %s)
        """, (dado["device_id"], dado["distancia_cm"], dado["movimento_detectado"], dado["contador_passagens"]))
    conn.commit()
    
    print(f"Enviado: dist={dado['distancia_cm']}cm | movimento={dado['movimento_detectado']} | contador={contador}")
    time.sleep(3)
