# app/schemas/documento.py
from pydantic import BaseModel
from datetime import datetime

class DocumentoResponse(BaseModel):
    id: int
    nome_original: str
    caminho_ficheiro: str
    criado_em: datetime

    class Config:
        from_attributes = True
