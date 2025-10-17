from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date
from typing import List

# Base comum para criação e resposta
class ClienteBase(BaseModel):
    tipo: Optional[str] = None  # 'singular' ou 'coletivo'

    # Dados principais
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None

    # Morada
    morada: Optional[str] = None
    codigo_postal: Optional[str] = None
    localidade: Optional[str] = None
    distrito: Optional[str] = None
    pais: Optional[str] = None

    # Pessoa Singular
    nif: Optional[str] = None
    data_nascimento: Optional[date] = None
    estado_civil: Optional[str] = None
    profissao: Optional[str] = None
    num_cc: Optional[str] = None
    validade_cc: Optional[date] = None
    num_ss: Optional[str] = None
    num_sns: Optional[str] = None
    num_ident_civil: Optional[str] = None
    nacionalidade: Optional[str] = None

    # Pessoa Coletiva
    nome_empresa: Optional[str] = None
    nif_empresa: Optional[str] = None
    forma_juridica: Optional[str] = None
    data_constituicao: Optional[date] = None
    registo_comercial: Optional[str] = None
    cae: Optional[str] = None
    capital_social: Optional[str] = None

    # Representante Legal
    representante_nome: Optional[str] = None
    representante_nif: Optional[str] = None
    representante_email: Optional[EmailStr] = None
    representante_telemovel: Optional[str] = None
    representante_cargo: Optional[str] = None

    # Documentos e outros
    iban: Optional[str] = None
    certidao_permanente: Optional[str] = None
    observacoes: Optional[str] = None

# Schema de criação
class ClienteCreate(ClienteBase):
    pass

# Schema de resposta (inclui ID e datas)
class ClienteResponse(ClienteBase):
    id: int
    criado_em: Optional[datetime] = None   # ← agora pode ser null
    atualizado_em: Optional[datetime] = None
    ativo: Optional[bool] = None           # ← agora pode ser null

    class Config:
        orm_mode = True  # se usares Pydantic v2, substitui por model_config = {"from_attributes": True}