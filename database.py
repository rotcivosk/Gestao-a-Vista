import os
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL não configurada!")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print(f"Conectando ao banco com: {DATABASE_URL}")

# Retry de conexão
for i in range(10):
    try:
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        connection = engine.connect()
        print("Conexão bem-sucedida ao banco de dados!")
        connection.close()
        break
    except Exception as e:
        print(f"Tentativa {i+1}: Falha ao conectar. Erro: {e}")
        time.sleep(3)
else:
    raise Exception("Não foi possível conectar ao banco após várias tentativas.")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
