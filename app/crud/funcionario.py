# app/crud/funcionario.py

from sqlalchemy.orm import Session
from app.models.funcionario import Funcionario
from app.schemas.funcionario import FuncionarioCreate

def create_funcionario(db: Session, funcionario: FuncionarioCreate) -> Funcionario:
    novo = Funcionario(
        nome=funcionario.nome,
        email=funcionario.email,
        cargo=funcionario.cargo,
        departamento=funcionario.departamento,
        telefone=funcionario.telefone,
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

def get_funcionarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Funcionario).offset(skip).limit(limit).all()

def get_funcionario_by_id(db: Session, funcionario_id: int):
    return db.query(Funcionario).filter(Funcionario.id == funcionario_id).first()

def update_funcionario(db: Session, funcionario_id: int, dados: FuncionarioCreate):
    funcionario = get_funcionario_by_id(db, funcionario_id)
    if funcionario:
        funcionario.nome = dados.nome
        funcionario.email = dados.email
        funcionario.cargo = dados.cargo
        funcionario.departamento = dados.departamento
        funcionario.telefone = dados.telefone
        db.commit()
        db.refresh(funcionario)
    return funcionario

def delete_funcionario(db: Session, funcionario_id: int):
    funcionario = get_funcionario_by_id(db, funcionario_id)
    if funcionario:
        db.delete(funcionario)
        db.commit()
    return funcionario
