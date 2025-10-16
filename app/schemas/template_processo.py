from pydantic import BaseModel
from typing import List, Optional

class TarefaTemplateCreate(BaseModel):
    titulo: str
    descricao: Optional[str] = None

class TemplateProcessoCreate(BaseModel):
    nome: str
    tipo: str
    tarefas: List[TarefaTemplateCreate]

class TemplateProcessoResponse(BaseModel):
    id: int
    nome: str
    tipo: str

    class Config:
        from_attributes = True
