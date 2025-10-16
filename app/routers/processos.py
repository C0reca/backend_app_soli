# app/routers/processos.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.processo import ProcessoCreate, ProcessoResponse
from app.crud import processo as crud_processo
from app.database import get_db
from app.crud import historico_processo
from app.schemas.historico_processo import HistoricoResponse
from fastapi.responses import FileResponse
from app.utils.ficheiros import gerar_documento_processo
from app.crud.processo import get_processo_by_id, criar_processo_com_template
from fastapi import UploadFile, File
import shutil
from app.schemas import ProcessoCreateFromTemplate


router = APIRouter(
    prefix="/processos",
    tags=["Processos"]
)

@router.post("/", response_model=ProcessoResponse, status_code=status.HTTP_201_CREATED)
def criar_processo(dados: ProcessoCreate, db: Session = Depends(get_db)):
    return crud_processo.create_processo(db, dados)

@router.get("/", response_model=List[ProcessoResponse])
def listar_processos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_processo.get_processos(db, skip, limit)

@router.get("/{processo_id}", response_model=ProcessoResponse)
def obter_processo(processo_id: int, db: Session = Depends(get_db)):
    processo = crud_processo.get_processo_by_id(db, processo_id)
    if not processo:
        raise HTTPException(status_code=404, detail="Processo não encontrado.")
    return processo

@router.put("/{processo_id}", response_model=ProcessoResponse)
def atualizar_processo(processo_id: int, dados: ProcessoCreate, db: Session = Depends(get_db)):
    processo = crud_processo.update_processo(db, processo_id, dados)
    if not processo:
        raise HTTPException(status_code=404, detail="Processo não encontrado.")
    return processo

@router.delete("/{processo_id}", status_code=status.HTTP_204_NO_CONTENT)
def apagar_processo(processo_id: int, db: Session = Depends(get_db)):
    processo = crud_processo.delete_processo(db, processo_id)
    if not processo:
        raise HTTPException(status_code=404, detail="Processo não encontrado.")

@router.get("/{processo_id}/historico", response_model=List[HistoricoResponse])
def ver_historico(processo_id: int, db: Session = Depends(get_db)):
    return historico_processo.listar_historico_do_processo(db, processo_id)

@router.get("/{processo_id}/gerar-doc")
def gerar_doc_processo(processo_id: int, db: Session = Depends(get_db)):
    processo = get_processo_by_id(db, processo_id)
    if not processo:
        raise HTTPException(status_code=404, detail="Processo não encontrado.")

    data = {
        "cliente_nome": processo.cliente.nome,
        "processo_id": processo.id,
        "processo_tipo": processo.tipo,
        "processo_estado": processo.estado.value,
    }

    output_path = gerar_documento_processo(data)  # ← só 1 argumento

    return FileResponse(path=output_path, filename=f"processo_{processo.id}.docx")

@router.post("/{processo_id}/upload")
def upload_arquivo_processo(processo_id: int, ficheiro: UploadFile = File(...)):
    upload_dir = f"documentos/processo_{processo_id}"
    Path(upload_dir).mkdir(parents=True, exist_ok=True)

    file_path = f"{upload_dir}/{ficheiro.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(ficheiro.file, buffer)

    return {"status": "ficheiro guardado", "path": file_path}

@router.post("/usar-template", status_code=201, response_model=None)
def usar_template() -> dict:
    return {"mensagem": "Teste simples"}