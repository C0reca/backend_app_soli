from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime, Text
from datetime import datetime
from app.database import Base
from sqlalchemy.dialects.postgresql import ARRAY

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)

    # Tipo de cliente: 'singular' ou 'coletivo'
    tipo = Column(String, nullable=True)

    # Dados comuns
    nome = Column(String, nullable=True)
    email = Column(String, nullable=True)
    telefone = Column(String, nullable=True)
    morada = Column(String, nullable=True)
    codigo_postal = Column(String, nullable=True)
    localidade = Column(String, nullable=True)
    distrito = Column(String, nullable=True)
    pais = Column(String, nullable=True)

    # Pessoa Singular
    nif = Column(String, nullable=True)
    data_nascimento = Column(Date, nullable=True)
    estado_civil = Column(String, nullable=True)
    profissao = Column(String, nullable=True)
    num_cc = Column(String, nullable=True)
    validade_cc = Column(Date, nullable=True)
    num_ss = Column(String, nullable=True)
    num_sns = Column(String, nullable=True)
    num_ident_civil = Column(String, nullable=True)
    nacionalidade = Column(String, nullable=True)

    # Pessoa Coletiva
    nome_empresa = Column(String, nullable=True)
    nif_empresa = Column(String, nullable=True)
    forma_juridica = Column(String, nullable=True)
    data_constituicao = Column(Date, nullable=True)
    registo_comercial = Column(String, nullable=True)
    cae = Column(String, nullable=True)
    capital_social = Column(String, nullable=True)

    # Representante legal (para empresas ou menores)
    representante_nome = Column(String, nullable=True)
    representante_nif = Column(String, nullable=True)
    representante_email = Column(String, nullable=True)
    representante_telemovel = Column(String, nullable=True)
    representante_cargo = Column(String, nullable=True)

    # Documentos e info adicional
    iban = Column(String, nullable=True)
    certidao_permanente = Column(String, nullable=True)
    observacoes = Column(Text, nullable=True)

    # Meta
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ativo = Column(Boolean, default=True)