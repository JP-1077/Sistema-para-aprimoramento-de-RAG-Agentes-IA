import json

from pathlib import Path

from services.report_service import (
    ReportService
)


def test_instancia_report_service():

    service = ReportService()

    assert service is not None


def test_gerar_relatorio(tmp_path):

    service = ReportService()

    service.report_path = tmp_path

    documento = {

        "nome_arquivo": "teste.md",

        "tipo_arquivo": ".md"
    }

    resultado_analise = {

        "score_final": 85.5,

        "score_qualidade": 90,

        "score_estrutura": 75,

        "classificacao": "BOM",

        "aprovado": True,

        "warnings": []
    }

    caminho_relatorio = service.relatorio(
        documento,
        resultado_analise
    )

    assert caminho_relatorio is not None

    assert Path(
        caminho_relatorio
    ).exists()


def test_conteudo_relatorio(tmp_path):

    service = ReportService()

    service.report_path = tmp_path

    documento = {

        "nome_arquivo": "documento_teste.md",

        "tipo_arquivo": ".md"
    }

    resultado_analise = {

        "score_final": 92,

        "score_qualidade": 100,

        "score_estrutura": 80,

        "classificacao": "EXCELENTE",

        "aprovado": True,

        "warnings": [
            "Documento muito extenso."
        ]
    }

    caminho_relatorio = service.relatorio(
        documento,
        resultado_analise
    )

    with open(
        caminho_relatorio,
        "r",
        encoding="utf-8"
    ) as arquivo:

        conteudo = json.load(
            arquivo
        )

    assert (
        conteudo["nome_arquivo"]
        == "documento_teste.md"
    )

    assert (
        conteudo["tipo_arquivo"]
        == ".md"
    )

    assert (
        conteudo["score_final"]
        == 92
    )

    assert (
        conteudo["score_qualidade"]
        == 100
    )

    assert (
        conteudo["score_estrutura"]
        == 80
    )

    assert (
        conteudo["classificacao"]
        == "EXCELENTE"
    )

    assert (
        conteudo["aprovado"]
        is True
    )

    assert len(
        conteudo["warnings"]
    ) == 1


def test_relatorio_com_warnings(tmp_path):

    service = ReportService()

    service.report_path = tmp_path

    documento = {

        "nome_arquivo": "warning.md",

        "tipo_arquivo": ".md"
    }

    resultado_analise = {

        "score_final": 55,

        "score_qualidade": 60,

        "score_estrutura": 45,

        "classificacao": "REGULAR",

        "aprovado": False,

        "warnings": [
            "Documento sem tabelas.",
            "Documento sem listas."
        ]
    }

    caminho_relatorio = service.relatorio(
        documento,
        resultado_analise
    )

    with open(
        caminho_relatorio,
        "r",
        encoding="utf-8"
    ) as arquivo:

        conteudo = json.load(
            arquivo
        )

    assert (
        len(
            conteudo["warnings"]
        ) == 2
    )


def test_nome_arquivo_relatorio(tmp_path):

    service = ReportService()

    service.report_path = tmp_path

    documento = {

        "nome_arquivo": "glossario.md",

        "tipo_arquivo": ".md"
    }

    resultado_analise = {

        "score_final": 80,

        "score_qualidade": 80,

        "score_estrutura": 80,

        "classificacao": "BOM",

        "aprovado": True,

        "warnings": []
    }

    caminho_relatorio = service.relatorio(
        documento,
        resultado_analise
    )

    assert (
        Path(
            caminho_relatorio
        ).suffix
        == ".json"
    )