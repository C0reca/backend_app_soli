# app/schemas/funcionario.py

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class FuncionarioCreate(BaseModel):
    nome: str
    email: EmailStr
    cargo: Optional[str] = None
    departamento: Optional[str] = None
    telefone: Optional[str] = None

class FuncionarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    cargo: Optional[str]
    departamento: Optional[str]
    telefone: Optional[str]
    criado_em: datetime

    class Config:
        from_attributes = True  # pydantic v2
