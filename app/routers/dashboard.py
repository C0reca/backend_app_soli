from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.database import get_db
from app.models.processo import Processo
from app.models.funcionario import Funcionario

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/kpis")
@router.get("/kpis")
def dashboard_kpis(db: Session = Depends(get_db)):
    total = db.query(Processo).count()
    ativos = db.query(Processo).filter(Processo.estado.in_(["pendente", "em_curso"])).count()
    concluidos = db.query(Processo).filter_by(estado="concluido").count()

    # Por tipo
    tipos = db.query(Processo.tipo, func.count(Processo.id)).group_by(Processo.tipo).all()
    por_tipo = {tipo or "indefinido": count for tipo, count in tipos}

    # Por estado
    estados = db.query(Processo.estado, func.count(Processo.id)).group_by(Processo.estado).all()
    por_estado = {estado: count for estado, count in estados}

    # Por funcionário
    funcionarios = (
        db.query(Funcionario.nome, func.count(Processo.id))
        .join(Processo, Processo.funcionario_id == Funcionario.id)
        .group_by(Funcionario.nome)
        .all()
    )
    por_funcionario = {nome: count for nome, count in funcionarios}

    # Por mês (últimos 12 meses)
    processos_por_mes = (
        db.query(
            extract("year", Processo.criado_em).label("ano"),
            extract("month", Processo.criado_em).label("mes"),
            func.count(Processo.id)
        )
        .group_by("ano", "mes")
        .order_by("ano", "mes")
        .all()
    )

    por_mes = [
        {
            "ano": int(ano),
            "mes": int(mes),
            "total": count,
            "label": f"{datetime(int(ano), int(mes), 1).strftime('%b/%Y')}"
        }
        for ano, mes, count in processos_por_mes
    ]

    return {
        "total_processos": total,
        "ativos": ativos,
        "concluidos": concluidos,
        "por_tipo": por_tipo,
        "por_estado": por_estado,
        "por_funcionario": por_funcionario,
        "evolucao_mensal": por_mes
    }