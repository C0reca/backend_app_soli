from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class LogAtividade(Base):
    __tablename__ = "logs_atividade"

    id = Column(Integer, primary_key=True, index=True)
    utilizador = Column(String, nullable=False)
    acao = Column(String, nullable=False)
    entidade = Column(String, nullable=False)
    entidade_id = Column(Integer, nullable=False)
    detalhes = Column(String, nullable=True)
    data_hora = Column(DateTime, default=datetime.utcnow)
