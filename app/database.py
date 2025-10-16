# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import DATABASE_URL

# Criação do engine com a URL da base de dados
engine = create_engine(DATABASE_URL)

# Criação da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

# Dependência que pode ser usada nos endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
