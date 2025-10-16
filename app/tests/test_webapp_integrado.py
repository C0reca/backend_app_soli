import pytest
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from app.main import app
from datetime import datetime, timedelta
from datetime import timezone

pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio
async def test_criar_processo_e_tarefa():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            # Criar processo

            cliente_data = {"nome": "Cliente Teste", "email": "cliente@teste.com"}
            cliente_resp = await ac.post("/clientes/", json=cliente_data)
            assert cliente_resp.status_code == 201
            cliente_id = cliente_resp.json()["id"]

            # Criar processo
            processo_data = {
                "titulo": "Processo Teste",
                "descricao": "Criado para testes",
                "tipo": "Financeiro",
                "cliente_id": cliente_id
            }
            response = await ac.post("/processos/", json=processo_data)
            assert response.status_code == 201
            processo = response.json()
            processo_id = processo["id"]

            # Criar tarefa ligada ao processo
            tarefa_data = {
                "titulo": "Tarefa 1",
                "descricao": "Teste",
                "data_fim": (datetime.now(timezone.utc) + timedelta(days=2)).isoformat(),
                "processo_id": processo_id
            }
            response = await ac.post("/tarefas/", json=tarefa_data)
            assert response.status_code == 201
            tarefa = response.json()
            tarefa_id = tarefa["id"]

            # Concluir tarefa via endpoint rápido
            response = await ac.post(f"/tarefas/concluir/{tarefa_id}")
            assert response.status_code == 200
            assert response.json()["concluida"] is True

            # Verificar agrupamento de tarefas
            response = await ac.get("/tarefas/agrupadas")
            assert response.status_code == 200
            data = response.json()
            assert "pendentes" in data
            assert "concluidas" in data

            # Verificar dashboard de KPIs
            response = await ac.get("/dashboard/processos")
            assert response.status_code == 200
            kpis = response.json()
            assert isinstance(kpis["ativos"], int)


@pytest.mark.asyncio
async def test_template_de_processo_e_logs():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            # Criar novo template
            template_data = {
                "nome": "Template Legal",
                "tipo": "Legal",
                "tarefas": [
                    {"titulo": "Análise jurídica", "descricao": "Etapa 1"},
                    {"titulo": "Revisão de cláusulas", "descricao": "Etapa 2"}
                ]
            }
            response = await ac.post("/templates/", json=template_data)
            assert response.status_code == 201
            template = response.json()
            template_id = template["id"]

            # Criar processo a partir do template
            response = await ac.post("/processos/usar-template", json={
                "nome": "Contrato X",
                "tipo": "Legal",
                "template_id": template_id
            })
            assert response.status_code == 201
            processo_criado = response.json()
            assert processo_criado["nome"] == "Contrato X"

            # Verificar logs
            response = await ac.get("/logs/")
            assert response.status_code == 200
            logs = response.json()
            assert any("Contrato X" in log["descricao"] for log in logs)


@pytest.mark.asyncio
async def test_envio_emails_mock(monkeypatch):
    async def fake_enviar_email(dest, assunto, conteudo):
        assert "@" in dest
        return True

    from app.utils import email
    monkeypatch.setattr(email, "enviar_email", fake_enviar_email)

    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/emails/enviar-lembretes")
            assert response.status_code == 200
