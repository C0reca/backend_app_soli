# app/models/processo.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from app.database import Base

class EstadoProcesso(PyEnum):
    pendente = "pendente"
    em_curso = "em_curso"
    concluido = "concluido"

class Processo(Base):
    __tablename__ = "processos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    tipo = Column(String, nullable=True)
    estado = Column(Enum(EstadoProcesso), default=EstadoProcesso.pendente)
    criado_em = Column(DateTime, default=datetime.utcnow)

    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=True)

    cliente = relationship("Cliente")
    funcionario = relationship("Funcionario")

    documentos = relationship("Documento", back_populates="processo", cascade="all, delete")
    tarefas = relationship("Tarefa", back_populates="processo", cascade="all, delete-orphan")
    movimentos_caixa = relationship("CaixaMovimento", back_populates="processo")