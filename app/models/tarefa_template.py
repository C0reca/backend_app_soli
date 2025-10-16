from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class TarefaTemplate(Base):
    __tablename__ = "tarefas_template"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=True)

    template_id = Column(Integer, ForeignKey("templates_processo.id"))
    template = relationship("TemplateProcesso", back_populates="tarefas")
