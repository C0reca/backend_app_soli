from sqlalchemy import Column, Integer, String, Date, Enum as SQLEnum, Text
from app.database import Base
import enum

class RegistoPredial(Base):
    __tablename__ = "registos_prediais"

    id = Column(Integer, primary_key=True, index=True)
    numero_processo = Column(String, nullable=True)
    cliente_id = Column(String, nullable=True)
    predio = Column(String, nullable=True)
    freguesia = Column(String, nullable=True)
    registo = Column(String, nullable=True)
    conservatoria = Column(String, nullable=True)
    requisicao = Column(String, nullable=True)
    apresentacao = Column(String, nullable=True)
    data = Column(Date, nullable=True)
    apresentacao_complementar = Column(String,nullable=True)
    data_criacao = Column(Date,nullable=True)
    outras_observacoes = Column(Text)
    estado = Column(String, nullable=True)