from sqlalchemy.orm import Session
from app.models.log_atividade import LogAtividade
from app.schemas.log_atividade import LogAtividadeCreate

def registar_log(db: Session, log_data: LogAtividadeCreate):
    log = LogAtividade(**log_data.dict())
    db.add(log)
    db.commit()
