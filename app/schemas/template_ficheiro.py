from pydantic import BaseModel

class FicheiroTemplateResponse(BaseModel):
    id: int
    nome_original: str
    caminho_ficheiro: str

    class Config:
        from_attributes = True