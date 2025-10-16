# app/routers/documentos.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.documento import Documento
from app.models.processo import Processo
from pathlib import Path
import shutil
from fastapi.responses import FileResponse
import os
from datetime import datetime
from app.schemas.documento import DocumentoResponse


router = APIRouter(prefix="/documentos", tags=["Documentos"])

UPLOAD_DIR = Path("documentos_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload/{processo_id}")
def upload_documento(processo_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    processo = db.query(Processo).filter_by(id=processo_id).first()
    if not processo:
        raise HTTPException(status_code=404, detail="Processo não encontrado")

    processo_dir = UPLOAD_DIR / f"processo_{processo_id}"
    processo_dir.mkdir(parents=True, exist_ok=True)

    caminho = processo_dir / file.filename

    with caminho.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    doc = Documento(
        nome_original=file.filename,
        caminho_ficheiro=str(caminho),
        processo_id=processo_id,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return {"msg": "Upload realizado com sucesso", "id": doc.id}

@router.get("/{processo_id}", response_model=list[DocumentoResponse])
def listar_documentos(processo_id: int, db: Session = Depends(get_db)):
    return db.query(Documento).filter_by(processo_id=processo_id).all()

@router.get("/download/{documento_id}")
def download_documento(documento_id: int, db: Session = Depends(get_db)):
    doc = db.query(Documento).filter_by(id=documento_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Documento não encontrado")

    if doc.eliminado_em:
        raise HTTPException(status_code=400, detail="Documento está na lixeira e não pode ser descarregado")

    caminho = Path(doc.caminho_ficheiro)
    if not caminho.exists():
        raise HTTPException(status_code=404, detail="Ficheiro não encontrado no disco")

    return FileResponse(
        path=caminho,
        filename=doc.nome_original,
        media_type='application/octet-stream',
        headers={"Content-Disposition": f'attachment; filename="{doc.nome_original}"'}
    )


@router.delete("/{documento_id}")
def eliminar_documento(documento_id: int, db: Session = Depends(get_db)):
    doc = db.query(Documento).filter_by(id=documento_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Documento não encontrado")

    path_atual = Path(doc.caminho_ficheiro)
    path_lixeira = Path("documentos_uploads") / "lixo" / path_atual.name
    path_lixeira.parent.mkdir(parents=True, exist_ok=True)

    shutil.move(str(path_atual), str(path_lixeira))

    doc.caminho_ficheiro = str(path_lixeira)
    doc.apagado_em = datetime.utcnow()
    doc.restaurado_em = None

    db.commit()
    return {"msg": "Documento movido para a lixeira"}


@router.post("/restaurar/{documento_id}")
def restaurar_documento(documento_id: int, db: Session = Depends(get_db)):
    doc = db.query(Documento).filter_by(id=documento_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Documento não encontrado")

    caminho_atual = Path(doc.caminho_ficheiro)
    if "lixo" not in caminho_atual.parts:
        raise HTTPException(status_code=400, detail="O documento não está na pasta de lixo")

    processo_id = doc.processo_id
    pasta_original = UPLOAD_DIR / f"processo_{processo_id}"
    pasta_original.mkdir(parents=True, exist_ok=True)

    destino = pasta_original / caminho_atual.name
    shutil.move(str(caminho_atual), destino)

    doc.caminho_ficheiro = str(destino)
    db.commit()

    return {"msg": "Documento restaurado com sucesso", "novo_caminho": str(destino)}

@router.get("/lixeira/{processo_id}", response_model=list[DocumentoResponse])
def listar_documentos_na_lixeira(processo_id: int, db: Session = Depends(get_db)):
    documentos = db.query(Documento).filter_by(processo_id=processo_id).all()

    documentos_na_lixeira = [
        doc for doc in documentos if "lixo" in Path(doc.caminho_ficheiro).parts
    ]

    return documentos_na_lixeira
