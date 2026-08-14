import pytest
import fitz
from docx import Document
from services.metadados_service import MetadadosService

def test_instancia_metadados_service():
    service = MetadadosService()
    assert service is not None

def test_metadados_md(tmp_path):
    caminho_arquivo = tmp_path / "teste.md"
    caminho_arquivo.write_text(
        """
        # Título

        ## Seção

        Conteúdo de teste.
        """,
        encoding="utf-8"
    )

    service = MetadadosService()
    resultado = service._metadados_md(
        {
            "nome_arquivo": "teste.md",
            "tipo_arquivo": ".md",
            "caminho": str(caminho_arquivo)
        }
    )
    assert resultado is not None
    assert (resultado["quantidade_linhas"] > 0)
    assert (resultado["quantidade_caracteres"]> 0)
    assert (resultado["quantidade_cabecalhos"] == 2)


def test_metadados_docx(tmp_path):
    caminho_arquivo = tmp_path / "teste.docx"

    documento = Document()
    documento.core_properties.author = ("Joao Pedro")
    documento.core_properties.title = ("Documento Teste")
    documento.add_paragraph("Conteúdo de exemplo")
    documento.save(caminho_arquivo)

    service = MetadadosService()

    resultado = service._metadados_docx(
        {
            "nome_arquivo": "teste.docx",
            "tipo_arquivo": ".docx",
            "caminho": str(caminho_arquivo)
        }
    )

    assert resultado is not None
    assert resultado["autor"] == ("Joao Pedro")
    assert resultado["titulo"] == ("Documento Teste")


def test_metadados_pdf(tmp_path):

    caminho_arquivo = tmp_path / "teste.pdf"

    pdf = fitz.open()
    pagina = pdf.new_page()
    pagina.insert_text((72, 72), "PDF de teste")
    pdf.set_metadata({"title": "Documento PDF Teste"})
    pdf.save(str(caminho_arquivo))
    pdf.close()

    service = MetadadosService()

    resultado = service._metadados_pdf(
        {
            "nome_arquivo": "teste.pdf",
            "tipo_arquivo": ".pdf",
            "caminho": str(caminho_arquivo)
        }
    )

    assert resultado is not None
    assert (resultado["titulo"]== "Documento PDF Teste")
    assert (resultado["numero_paginas"]== 1)


def test_extracao_metadados_md(tmp_path):

    caminho_arquivo = tmp_path / "teste.md"

    caminho_arquivo.write_text("# Título", encoding="utf-8")

    service = MetadadosService()

    resultado = service.extracao_metadados(
        {
            "nome_arquivo": "teste.md",
            "tipo_arquivo": ".md",
            "caminho": str(caminho_arquivo)
        }
    )

    assert resultado is not None


def test_tipo_arquivo_invalido():
    service = MetadadosService()

    with pytest.raises(ValueError):

        service.extracao_metadados(
            {
                "nome_arquivo": "teste.txt",
                "tipo_arquivo": ".txt",
                "caminho": "teste.txt"
            }
        )