# app/models/historico_processo.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class HistoricoProcesso(Base):
    __tablename__ = "historico_processos"

    id = Column(Integer, primary_key=True, index=True)
    processo_id = Column(Integer, ForeignKey("processos.id"), nullable=False)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=True)
    acao = Column(String, nullable=False)
    detalhes = Column(String, nullable=True)
    data = Column(DateTime, default=datetime.utcnow)

    processo = relationship("Processo")
    funcionario = relationship("Funcionario")
