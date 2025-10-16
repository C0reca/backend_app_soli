from app.models import Documento

def aplicar_template_a_processo(template: TemplateProcesso, processo: Processo, db: Session):
    # Copiar ficheiros
    for f in template.ficheiros:
        origem = Path(f.caminho_ficheiro)
        destino_dir = Path("documentos") / str(processo.id)
        destino_dir.mkdir(parents=True, exist_ok=True)
        destino = destino_dir / origem.name
        shutil.copy2(origem, destino)

        db.add(Documento(
            nome_original=f.nome_original,
            caminho_ficheiro=str(destino),
            processo_id=processo.id
        ))

    db.commit()