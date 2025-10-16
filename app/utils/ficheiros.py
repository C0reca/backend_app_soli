# app/utils/ficheiros.py

from docxtpl import DocxTemplate
from pathlib import Path

def gerar_documento_processo(processo_data: dict, template: str = "test.docx") -> str:
    template_path = Path("templates") / template
    output_path = Path("documentos") / f"processo_{processo_data['processo_id']}.docx"

    doc = DocxTemplate(template_path)
    doc.render(processo_data)
    doc.save(output_path)

    return str(output_path)