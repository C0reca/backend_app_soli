from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LogAtividadeCreate(BaseModel):
    utilizador: str
    acao: str
    entidade: str
    entidade_id: int
    detalhes: Optional[str] = None

class LogAtividadeResponse(LogAtividadeCreate):
    id: int
    data_hora: datetime

    class Config:
        from_attributes = True
