from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.database import get_db
from app.models.tarefa import Tarefa
from app.models.funcionario import Funcionario
from app.utils.email import enviar_email

router = APIRouter(prefix="/emails", tags=["Emails"])

@router.post("/enviar-lembretes")
async def enviar_lembretes(db: Session = Depends(get_db)):
    hoje = date.today()
    amanha = hoje + timedelta(days=1)

    tarefas = db.query(Tarefa).filter(
        Tarefa.concluida == False,
        Tarefa.data_fim != None,
        Tarefa.data_fim.between(hoje, amanha),
        Tarefa.responsavel_id != None
    ).all()

    enviados = 0
    for tarefa in tarefas:
        funcionario: Funcionario = db.query(Funcionario).filter_by(id=tarefa.responsavel_id).first()
        if funcionario and funcionario.email:
            assunto = f"[Lembrete] Tarefa para {tarefa.data_fim.date()}: {tarefa.titulo}"
            conteudo = f"""
Olá {funcionario.nome},

Tem uma tarefa pendente:
- Título: {tarefa.titulo}
- Descrição: {tarefa.descricao or "Sem descrição"}
- Data limite: {tarefa.data_fim.strftime('%Y-%m-%d %H:%M')}

Por favor verifique a plataforma para mais detalhes.

Obrigado.
"""
            await enviar_email(funcionario.email, assunto, conteudo)
            enviados += 1

    return {"msg": f"{enviados} lembretes enviados"}
