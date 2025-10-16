from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from sqlalchemy import Enum
import enum
from app.models.funcionario import Funcionario  # Certifica-te que está importado
from sqlalchemy import Enum as PgEnum

class PrioridadeEnum(enum.Enum):
    baixa = "baixa"
    media = "media"
    alta = "alta"

class Tarefa(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    data_fim = Column(DateTime, nullable=True)
    concluida = Column(Boolean, default=False)
    criado_em = Column(DateTime, default=datetime.utcnow)

    processo_id = Column(Integer, ForeignKey("processos.id"), nullable=False)
    processo = relationship("Processo", back_populates="tarefas")

    responsavel_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=True)
    responsavel = relationship("Funcionario")

    prioridade = Column(PgEnum(PrioridadeEnum, name="prioridadeenum2"), nullable=True)

