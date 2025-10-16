from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.template_processo import TemplateProcesso
from app.models.tarefa_template import TarefaTemplate
from app.schemas.template_processo import TemplateProcessoCreate, TemplateProcessoResponse
from fastapi import UploadFile, File
from app.models.template_ficheiro import FicheiroTemplate


router = APIRouter(prefix="/templates", tags=["Templates de Processos"])

@router.post("/", response_model=TemplateProcessoResponse, status_code=201)
def criar_template(template_data: TemplateProcessoCreate, db: Session = Depends(get_db)):
    novo_template = TemplateProcesso(nome=template_data.nome, tipo=template_data.tipo)
    db.add(novo_template)
    db.flush()  # Para obter o ID antes de adicionar tarefas

    for tarefa in template_data.tarefas:
        nova_tarefa = TarefaTemplate(
            titulo=tarefa.titulo,
            descricao=tarefa.descricao,
            template_id=novo_template.id
        )
        db.add(nova_tarefa)

    db.commit()
    db.refresh(novo_template)
    return novo_template

@router.get("/", response_model=list[TemplateProcessoResponse])
def listar_templates(db: Session = Depends(get_db)):
    return db.query(TemplateProcesso).all()

@router.post("/{template_id}/ficheiros")
def upload_ficheiro_template(template_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    template = db.query(TemplateProcesso).filter_by(id=template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template não encontrado")

    folder = Path("documentos_templates") / f"template_{template_id}"
    folder.mkdir(parents=True, exist_ok=True)
    caminho = folder / file.filename

    with caminho.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    doc = FicheiroTemplate(
        nome_original=file.filename,
        caminho_ficheiro=str(caminho),
        template_id=template_id
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return {"msg": "Upload realizado", "id": doc.id}