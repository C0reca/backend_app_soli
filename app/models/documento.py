# app/models/documento.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Documento(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True, index=True)
    nome_original = Column(String, nullable=False)
    caminho_ficheiro = Column(String, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)

    processo_id = Column(Integer, ForeignKey("processos.id"))
    processo = relationship("Processo", back_populates="documentos")
    apagado_em = Column(DateTime, nullable=True)
    restaurado_em = Column(DateTime, nullable=True)