from sqlalchemy import Column, Integer, String, Float,Boolean , Enum, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from datetime import datetime
from datetime import date

class TipoMovimentoEnum(str, enum.Enum):
    entrada = "entrada"
    saida = "saida"

class CaixaMovimento(Base):
    __tablename__ = "caixa_movimentos"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)  # "entrada" ou "saida"
    valor = Column(Float, nullable=False)
    descricao = Column(String)
    data = Column(DateTime, default=datetime.today)
    associado_a_processo = Column(Boolean, default=False)
    processo_id = Column(Integer, ForeignKey("processos.id"), nullable=True)

    processo = relationship("Processo", back_populates="movimentos_caixa")

    processo = relationship("Processo", back_populates="movimentos_caixa")

class CaixaFecho(Base):
    __tablename__ = "caixa_fechos"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(Date, unique=True, nullable=False)
    total_entrada = Column(Float, nullable=False)
    total_saida = Column(Float, nullable=False)
    saldo_final = Column(Float, nullable=False)



