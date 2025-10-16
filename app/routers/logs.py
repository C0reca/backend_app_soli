from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.log_atividade import LogAtividade
from app.schemas.log_atividade import LogAtividadeResponse

router = APIRouter(prefix="/logs", tags=["Logs"])

@router.get("/", response_model=list[LogAtividadeResponse])
def listar_logs(db: Session = Depends(get_db)):
    return db.query(LogAtividade).order_by(LogAtividade.data_hora.desc()).all()
