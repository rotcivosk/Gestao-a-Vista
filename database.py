from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 🚩 Pegando a URL do banco nas variáveis de ambiente do Railway
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
	raise ValueError("DATABASE_URL environment variable is not set.")

# 🚀 Conexão com PostgreSQL
engine = create_engine(DATABASE_URL)

# 🗄️ Sessão do banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🏛️ Base das models
Base = declarative_base()
