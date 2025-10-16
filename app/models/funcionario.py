# app/models/funcionario.py

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class Funcionario(Base):
    __tablename__ = "funcionarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    cargo = Column(String, nullable=True)
    departamento = Column(String, nullable=True)
    telefone = Column(String, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
