# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import clientes, funcionarios, processos, documentos, tarefas, dashboard, templates, emails, registo_predial, caixa
from app.database import Base, engine

# Inicializa as tabelas na base de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gestão Empresarial API",
    description="API para gestão de clientes, funcionários, processos e automação de ficheiros.",
    version="1.0.0"
)

# Middleware CORS (para comunicação com frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção deves restringir isto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registo dos routers
app.include_router(clientes.router)
app.include_router(funcionarios.router)
app.include_router(processos.router)
app.include_router(documentos.router)
app.include_router(tarefas.router)
app.include_router(dashboard.router)
app.include_router(templates.router)
app.include_router(emails.router)
app.include_router(registo_predial.router)
app.include_router(caixa.router)