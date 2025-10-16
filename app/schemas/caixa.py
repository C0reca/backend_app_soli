from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from enum import Enum

class TipoMovimento(str, Enum):
    entrada = "entrada"
    saida = "saida"

class CaixaMovimentoBase(BaseModel):
    descricao: str
    valor: float
    tipo: TipoMovimento
    data: Optional[datetime] = None
    processo_id: Optional[int] = None

class CaixaMovimentoCreate(CaixaMovimentoBase):
    pass

class CaixaMovimento(CaixaMovimentoBase):
    id: int
    class Config:
        from_attributes = True

class CaixaFechoBase(BaseModel):
    data: date
    total_entrada: float
    total_saida: float
    saldo_final: float

class CaixaFecho(CaixaFechoBase):
    id: int
    class Config:
        from_attributes = True

class ResumoCaixa(BaseModel):
    total_entradas: float
    total_saidas: float
    saldo: float


class CaixaFecho(BaseModel):
    id: int
    data: date
    total_entradas: float
    total_saidas: float
    saldo_final: float

    class Config:
        from_attributes = True