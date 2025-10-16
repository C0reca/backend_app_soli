from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum

class RegistoPredialBase(BaseModel):
    numero_processo: str
    cliente_id: str
    predio: str
    freguesia: str
    registo: str
    conservatoria: str
    requisicao: str
    apresentacao: str
    data: date
    apresentacao_complementar: Optional[str] = None
    data_criacao: Optional[date] = None
    outras_observacoes: Optional[str] = None
    estado: str

class RegistoPredialCreate(RegistoPredialBase):
    pass

class RegistoPredialUpdate(RegistoPredialBase):
    pass

class RegistoPredial(RegistoPredialBase):
    id: int

    class Config:
        from_attributes = True