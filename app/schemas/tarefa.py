from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum as PyEnum, Enum


class PrioridadeEnum(str, Enum):
    baixa = "baixa"
    media = "media"
    alta = "alta"

class TarefaBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    data_fim: Optional[datetime] = None
    prioridade: Optional[PrioridadeEnum] = PrioridadeEnum.media

class TarefaCreate(TarefaBase):
    processo_id: int
    responsavel_id: Optional[int] = None

class TarefaUpdate(TarefaBase):
    concluida: Optional[bool] = None
    responsavel_id: Optional[int] = None

class TarefaResponse(TarefaBase):
    id: int
    concluida: bool
    criado_em: datetime
    responsavel_id: Optional[int] = None

    class Config:
        from_attributes = True
