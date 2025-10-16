# app/crud/historico_processo.py

from sqlalchemy.orm import Session
from app.models.historico_processo import HistoricoProcesso
from app.schemas.historico_processo import HistoricoCreate

def registar_acao(db: Session, historico: HistoricoCreate):
    registo = HistoricoProcesso(**historico.model_dump())
    db.add(registo)
    db.commit()
    db.refresh(registo)
    return registo

def listar_historico_do_processo(db: Session, processo_id: int):
    return db.query(HistoricoProcesso).filter(HistoricoProcesso.processo_id == processo_id).order_by(HistoricoProcesso.data.desc()).all()
