from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from app.models.processo import EstadoProcesso  # Importa o Enum do modelo


class ProcessoCreate(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    tipo: Optional[str] = None
    estado: Optional[EstadoProcesso] = EstadoProcesso.pendente
    cliente_id: int
    funcionario_id: Optional[int] = None


class ProcessoResponse(ProcessoCreate):
    id: int
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)  # Para Pydantic v2

class ProcessoCreateFromTemplate(BaseModel):
    nome: str
    tipo: Optional[str] = None
    template_id: int
    cliente_id: int  # Se precisares associar ao cliente

    model_config = ConfigDict(from_attributes=True)
