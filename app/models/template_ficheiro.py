from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class FicheiroTemplate(Base):
    __tablename__ = "ficheiros_template"

    id = Column(Integer, primary_key=True, index=True)
    nome_original = Column(String, nullable=False)
    caminho_ficheiro = Column(String, nullable=False)
    template_id = Column(Integer, ForeignKey("templates_processo.id"), nullable=False)
    template = relationship("TemplateProcesso", back_populates="ficheiros")