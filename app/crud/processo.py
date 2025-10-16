# app/crud/processo.py
from http.client import HTTPException

from sqlalchemy.orm import Session
from app.models.processo import Processo
from app.schemas.processo import ProcessoCreate, ProcessoCreateFromTemplate
from app.schemas.historico_processo import HistoricoCreate
from app.crud.historico_processo import registar_acao



def create_processo(db: Session, dados: ProcessoCreate):
    processo = Processo(**dados.model_dump())
    db.add(processo)
    db.commit()
    db.refresh(processo)
    registar_acao(db, HistoricoCreate(
        processo_id=processo.id,
        funcionario_id=processo.funcionario_id,
        acao="criação",
        detalhes=f"Processo '{processo.titulo}' criado."
    ))
    return processo

def get_processos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Processo).offset(skip).limit(limit).all()

def get_processo_by_id(db: Session, processo_id: int):
    return db.query(Processo).filter(Processo.id == processo_id).first()

def update_processo(db: Session, processo_id: int, dados: ProcessoCreate):
    processo = get_processo_by_id(db, processo_id)
    if processo:
        for key, value in dados.model_dump().items():
            setattr(processo, key, value)
        db.commit()
        db.refresh(processo)
    registar_acao(db, HistoricoCreate(
        processo_id=processo.id,
        funcionario_id=processo.funcionario_id,
        acao="edição",
        detalhes=f"Processo '{processo.titulo}' criado."
    ))
    return processo

def delete_processo(db: Session, processo_id: int):
    processo = get_processo_by_id(db, processo_id)
    if processo:
        db.delete(processo)
        db.commit()
    return processo

def criar_processo_com_template(dados: ProcessoCreateFromTemplate, db: Session):
    template = db.query(Template).filter(Template.id == dados.template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template não encontrado")

    novo_processo = Processo(
        nome=dados.nome,
        tipo=dados.tipo or template.tipo,
        cliente_id=dados.cliente_id
    )
    db.add(novo_processo)
    db.commit()
    db.refresh(novo_processo)

    for tarefa in template.tarefas:
        nova_tarefa = Tarefa(
            titulo=tarefa.titulo,
            descricao=tarefa.descricao,
            processo_id=novo_processo.id
        )
        db.add(nova_tarefa)

    db.commit()
    return novo_processo
