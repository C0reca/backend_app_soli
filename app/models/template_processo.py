from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class TemplateProcesso(Base):
    __tablename__ = "templates_processo"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    tipo = Column(String, nullable=False)

    tarefas = relationship("TarefaTemplate", back_populates="template", cascade="all, delete-orphan")
    ficheiros = relationship("FicheiroTemplate", back_populates="template", cascade="all, delete-orphan")
