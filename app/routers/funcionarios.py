# app/routers/funcionarios.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.funcionario import FuncionarioCreate, FuncionarioResponse
from app.crud import funcionario as crud_funcionario
from app.database import get_db

router = APIRouter(
    prefix="/funcionarios",
    tags=["Funcionários"]
)

@router.post("/", response_model=FuncionarioResponse, status_code=status.HTTP_201_CREATED)
def criar_funcionario(funcionario: FuncionarioCreate, db: Session = Depends(get_db)):
    return crud_funcionario.create_funcionario(db, funcionario)

@router.get("/", response_model=List[FuncionarioResponse])
def listar_funcionarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_funcionario.get_funcionarios(db, skip=skip, limit=limit)

@router.get("/{funcionario_id}", response_model=FuncionarioResponse)
def obter_funcionario(funcionario_id: int, db: Session = Depends(get_db)):
    funcionario = crud_funcionario.get_funcionario_by_id(db, funcionario_id)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado.")
    return funcionario

@router.put("/{funcionario_id}", response_model=FuncionarioResponse)
def atualizar_funcionario(funcionario_id: int, dados: FuncionarioCreate, db: Session = Depends(get_db)):
    funcionario = crud_funcionario.update_funcionario(db, funcionario_id, dados)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado para atualização.")
    return funcionario

@router.delete("/{funcionario_id}", status_code=status.HTTP_204_NO_CONTENT)
def apagar_funcionario(funcionario_id: int, db: Session = Depends(get_db)):
    funcionario = crud_funcionario.delete_funcionario(db, funcionario_id)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado para eliminação.")
