# app/routers/clientes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.cliente import ClienteCreate, ClienteResponse
from app.crud import cliente as crud_cliente
from app.database import get_db

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)

@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    print(cliente)
    existente = crud_cliente.get_cliente_by_nif(db, cliente.nif)
    if existente:
        raise HTTPException(status_code=400, detail="Cliente já existe.")
    return crud_cliente.create_cliente(db, cliente)

@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_cliente.get_clientes(db, skip=skip, limit=limit)

@router.get("/{cliente_id}", response_model=ClienteResponse)
def obter_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = crud_cliente.get_cliente_by_id(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return cliente

@router.put("/{cliente_id}", response_model=ClienteResponse)
def atualizar_cliente(cliente_id: int, dados: ClienteCreate, db: Session = Depends(get_db)):
    cliente = crud_cliente.update_cliente(db, cliente_id, dados)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado para atualização.")
    return cliente

@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def apagar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = crud_cliente.delete_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado para eliminação.")
