from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from collections import defaultdict
from sqlalchemy import func
from app.database import get_db
from app.models.tarefa import Tarefa
from app.models.processo import Processo
from app.schemas.tarefa import TarefaCreate, TarefaResponse, TarefaUpdate
from datetime import datetime, timezone

router = APIRouter(prefix="/tarefas", tags=["Tarefas"])


@router.post("/", response_model=TarefaResponse)
def criar_tarefa(tarefa: TarefaCreate, db: Session = Depends(get_db)):
    if tarefa.data_fim and tarefa.data_fim.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail="A data de fim não pode ser anterior à data atual."
        )

    nova_tarefa = Tarefa(**tarefa.dict())
    nova_tarefa.prioridade = nova_tarefa.prioridade.value
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    return nova_tarefa

@router.put("/{tarefa_id}", response_model=TarefaResponse)
def atualizar_tarefa(tarefa_id: int, dados: TarefaCreate, db: Session = Depends(get_db)):
    tarefa = db.query(Tarefa).filter_by(id=tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    if dados.data_fim and dados.data_fim < datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="A data de fim não pode ser anterior à data atual."
        )

    for campo, valor in dados.dict().items():
        setattr(tarefa, campo, valor)

    db.commit()
    db.refresh(tarefa)
    return tarefa

@router.get("/", response_model=List[TarefaResponse])
def listar_tarefas(db: Session = Depends(get_db)):
    return db.query(Tarefa).order_by(Tarefa.data_fim).all()

@router.get("/processo/{processo_id}", response_model=List[TarefaResponse])
def listar_tarefas_do_processo(processo_id: int, db: Session = Depends(get_db)):
    return db.query(Tarefa).filter_by(processo_id=processo_id).order_by(Tarefa.data_fim).all()


@router.get("/{tarefa_id}", response_model=TarefaResponse)
def obter_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(Tarefa).filter_by(id=tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa


@router.put("/{tarefa_id}", response_model=TarefaResponse)
def atualizar_tarefa(tarefa_id: int, dados: TarefaUpdate, db: Session = Depends(get_db)):
    tarefa = db.query(Tarefa).filter_by(id=tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    for key, value in dados.dict(exclude_unset=True).items():
        setattr(tarefa, key, value)

    db.commit()
    db.refresh(tarefa)
    return tarefa


@router.delete("/{tarefa_id}")
def eliminar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(Tarefa).filter_by(id=tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    db.delete(tarefa)
    db.commit()
    return {"msg": "Tarefa eliminada com sucesso"}

@router.patch("/concluir/{tarefa_id}")
def concluir_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(Tarefa).filter_by(id=tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    if tarefa.estado == "concluida":
        return {"msg": "Tarefa já está concluída."}

    tarefa.estado = "concluida"
    tarefa.concluida_em = datetime.utcnow()

    db.commit()
    db.refresh(tarefa)
    return {"msg": "Tarefa marcada como concluída com sucesso", "id": tarefa.id, "concluida_em": tarefa.concluida_em}

@router.get("/por-status/{processo_id}")
def listar_tarefas_por_status(processo_id: int, db: Session = Depends(get_db)):
    pendentes = db.query(Tarefa).filter_by(processo_id=processo_id, concluida=False).all()
    concluidas = db.query(Tarefa).filter_by(processo_id=processo_id, concluida=True).all()

    return {
        "pendentes": pendentes,
        "concluidas": concluidas
    }


@router.get("/por-semana/{processo_id}")
def tarefas_por_semana(processo_id: int, db: Session = Depends(get_db)):
    tarefas = db.query(Tarefa).filter_by(processo_id=processo_id).all()

    agrupadas = defaultdict(list)
    for tarefa in tarefas:
        if tarefa.data_fim:
            semana = tarefa.data_fim.isocalendar().week
            agrupadas[f"Semana {semana}"].append(tarefa)

    return agrupadas

@router.get("/por-mes/{processo_id}")
def tarefas_por_mes(processo_id: int, db: Session = Depends(get_db)):
    tarefas = db.query(Tarefa).filter_by(processo_id=processo_id).all()

    agrupadas = defaultdict(list)
    for tarefa in tarefas:
        if tarefa.data_fim:
            mes = tarefa.data_fim.strftime("%Y-%m")
            agrupadas[mes].append(tarefa)

    return agrupadas

@router.get("/tarefas/dashboard")
def tarefas_kpis(db: Session = Depends(get_db)):
    total = db.query(Tarefa).count()
    pendentes = db.query(Tarefa).filter_by(concluida=False).count()
    concluidas = db.query(Tarefa).filter_by(concluida=True).count()

    por_prioridade = db.query(
        Tarefa.prioridade, func.count(Tarefa.id)
    ).group_by(Tarefa.prioridade).all()

    por_processo = db.query(
        Tarefa.processo_id, func.count(Tarefa.id)
    ).group_by(Tarefa.processo_id).all()

    return {
        "total": total,
        "pendentes": pendentes,
        "concluidas": concluidas,
        "por_prioridade": {p.name: c for p, c in por_prioridade},
        "por_processo": {pid: c for pid, c in por_processo}
    }
