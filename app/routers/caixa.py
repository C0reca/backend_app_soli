from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import schemas, models, database
from datetime import datetime, date
from app.schemas import caixa as schemas
from app.models import caixa as models
from datetime import date
from typing import Optional
router = APIRouter(prefix="/caixa", tags=["Caixa"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/movimento", response_model=schemas.CaixaMovimento)
def criar_movimento(mov: schemas.CaixaMovimentoCreate, db: Session = Depends(get_db)):
    novo = models.CaixaMovimento(**mov.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.get("/movimentos", response_model=list[schemas.CaixaMovimento])
def listar_movimentos(
    data: Optional[date] = Query(default=None),
    db: Session = Depends(get_db)
):
    if data is None:
        data = date.today()

    inicio = datetime.combine(data, datetime.min.time())
    fim = datetime.combine(data, datetime.max.time())

    return db.query(models.CaixaMovimento).filter(
        models.CaixaMovimento.data.between(inicio, fim)
    ).all()

@router.post("/fecho", response_model=schemas.CaixaFecho)
def fechar_caixa(data: date, db: Session = Depends(get_db)):
    movimentos = listar_movimentos(data, db)
    total_entrada = sum(m.valor for m in movimentos if m.tipo == "entrada")
    total_saida = sum(m.valor for m in movimentos if m.tipo == "saida")
    saldo_final = total_entrada - total_saida

    if db.query(models.CaixaFecho).filter(models.CaixaFecho.data == data).first():
        raise HTTPException(status_code=400, detail="Fecho já existe para esta data")

    fecho = models.CaixaFecho(
        data=data,
        total_entrada=total_entrada,
        total_saida=total_saida,
        saldo_final=saldo_final
    )
    db.add(fecho)
    db.commit()
    db.refresh(fecho)
    return fecho

@router.get("/saldo")
def saldo_atual(db: Session = Depends(get_db)):
    ultimo = db.query(models.CaixaFecho).order_by(models.CaixaFecho.data.desc()).first()
    return {"saldo": ultimo.saldo_final if ultimo else 0.0}

@router.get("/resumo/{data}", response_model=schemas.ResumoCaixa)
def resumo_caixa(data: date, db: Session = Depends(get_db)):
    inicio = datetime.combine(data, datetime.min.time())
    fim = datetime.combine(data, datetime.max.time())

    entradas = db.query(func.sum(models.CaixaMovimento.valor))\
        .filter(models.CaixaMovimento.data.between(inicio, fim))\
        .filter(models.CaixaMovimento.tipo == "entrada")\
        .scalar() or 0

    saidas = db.query(func.sum(models.CaixaMovimento.valor))\
        .filter(models.CaixaMovimento.data.between(inicio, fim))\
        .filter(models.CaixaMovimento.tipo == "saida")\
        .scalar() or 0

    return schemas.ResumoCaixa(
        data=data,
        total_entradas=entradas,
        total_saidas=saidas,
        saldo=entradas - saidas
    )


@router.get("/fechos", response_model=list[schemas.CaixaFecho])
def listar_fechos(db: Session = Depends(get_db)):
    return db.query(models.CaixaFecho).order_by(models.CaixaFecho.data.desc()).all()