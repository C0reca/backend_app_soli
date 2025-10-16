# app/schemas/historico_processo.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class HistoricoCreate(BaseModel):
    processo_id: int
    funcionario_id: Optional[int] = None
    acao: str
    detalhes: Optional[str] = None

class HistoricoResponse(HistoricoCreate):
    id: int
    data: datetime

    class Config:
        from_attributes = True
