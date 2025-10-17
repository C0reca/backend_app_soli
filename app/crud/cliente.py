from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate

def create_cliente(db: Session, cliente: ClienteCreate) -> Cliente:
    novo_cliente = Cliente(
        tipo=cliente.tipo,

        # Dados comuns
        nome=cliente.nome,
        email=cliente.email,
        telefone=cliente.telefone,
        morada=cliente.morada,
        codigo_postal=cliente.codigo_postal,
        localidade=cliente.localidade,
        distrito=cliente.distrito,
        pais=cliente.pais,

        # Pessoa Singular
        nif=cliente.nif,
        data_nascimento=cliente.data_nascimento,
        estado_civil=cliente.estado_civil,
        profissao=cliente.profissao,
        num_cc=cliente.num_cc,
        validade_cc=cliente.validade_cc,
        num_ss=cliente.num_ss,
        num_sns=cliente.num_sns,
        num_ident_civil=cliente.num_ident_civil,
        nacionalidade=cliente.nacionalidade,

        # Pessoa Coletiva
        nome_empresa=cliente.nome_empresa,
        nif_empresa=cliente.nif_empresa,
        forma_juridica=cliente.forma_juridica,
        data_constituicao=cliente.data_constituicao,
        registo_comercial=cliente.registo_comercial,
        cae=cliente.cae,
        capital_social=cliente.capital_social,

        # Representante
        representante_nome=cliente.representante_nome,
        representante_nif=cliente.representante_nif,
        representante_email=cliente.representante_email,
        representante_telemovel=cliente.representante_telemovel,
        representante_cargo=cliente.representante_cargo,

        # Outros
        iban=cliente.iban,
        certidao_permanente=cliente.certidao_permanente,
        observacoes=cliente.observacoes,
    )
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    return novo_cliente


def get_clientes(db: Session, skip: int = 0, limit: int = 99999):
    return db.query(Cliente).offset(skip).limit(limit).all()


def get_cliente_by_id(db: Session, cliente_id: int):
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()


def get_cliente_by_email(db: Session, email: str):
    return db.query(Cliente).filter(Cliente.email == email).first()

def get_cliente_by_nif(db: Session, nif: str):
    print(nif)
    return db.query(Cliente).filter(Cliente.nif == nif).first()


def delete_cliente(db: Session, cliente_id: int):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if cliente:
        db.delete(cliente)
        db.commit()
    return cliente


def update_cliente(db: Session, cliente_id: int, dados: ClienteCreate):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if cliente:
        for campo, valor in dados.dict(exclude_unset=True).items():
            setattr(cliente, campo, valor)
        db.commit()
        db.refresh(cliente)
    return cliente