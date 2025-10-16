from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.registo_predial import RegistoPredial as RegistoModel
from app.schemas.registo_predial import RegistoPredialCreate, RegistoPredialUpdate, RegistoPredial

router = APIRouter(prefix="/registos", tags=["Registos Prediais"])

@router.post("/", response_model=RegistoPredial, status_code=201)
def criar_registo(registo: RegistoPredialCreate, db: Session = Depends(get_db)):
    db_registo = RegistoModel(**registo.dict())
    db.add(db_registo)
    db.commit()
    db.refresh(db_registo)
    return db_registo

@router.get("/", response_model=List[RegistoPredial])
def listar_registos(db: Session = Depends(get_db)):
    return db.query(RegistoModel).all()

@router.get("/{registo_id}", response_model=RegistoPredial)
def obter_registo(registo_id: int, db: Session = Depends(get_db)):
    registo = db.query(RegistoModel).filter(RegistoModel.id == registo_id).first()
    if not registo:
        raise HTTPException(status_code=404, detail="Registo não encontrado")
    return registo

@router.put("/{registo_id}", response_model=RegistoPredial)
def atualizar_registo(registo_id: int, dados: RegistoPredialUpdate, db: Session = Depends(get_db)):
    registo = db.query(RegistoModel).filter(RegistoModel.id == registo_id).first()
    if not registo:
        raise HTTPException(status_code=404, detail="Registo não encontrado")
    for key, value in dados.dict().items():
        setattr(registo, key, value)
    db.commit()
    db.refresh(registo)
    return registo

@router.delete("/{registo_id}", status_code=204)
def apagar_registo(registo_id: int, db: Session = Depends(get_db)):
    registo = db.query(RegistoModel).filter(RegistoModel.id == registo_id).first()
    if not registo:
        raise HTTPException(status_code=404, detail="Registo não encontrado")
    db.delete(registo)
    db.commit()
    return