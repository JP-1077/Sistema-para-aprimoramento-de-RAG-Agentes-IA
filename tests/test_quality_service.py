import pytest
from services.quality_service import ServiceQualidadeArquivo


def test_instancia_service():
    service = ServiceQualidadeArquivo()
    assert service is not None


def test_documento_vazio():

    service = ServiceQualidadeArquivo()
    resultado = service.analise_documento(
        {
            "conteudo": ""
        }
    )
    assert resultado["score_conteudo"] == 0
    assert resultado["classificacao"] == "REPROVADO"
    assert (
        "Documento não possui conteúdo."
        in resultado["warnings"]
    )


def test_documento_muito_pequeno():

    service = ServiceQualidadeArquivo()

    resultado = service.analise_documento(
        {
            "conteudo": "A" * 50
        }
    )

    assert resultado["score_conteudo"] == 20

    assert resultado["classificacao"] == "REPROVADO"

    assert (
        "Conteúdo muito pequeno."
        in resultado["warnings"]
    )


def test_documento_pequeno():

    service = ServiceQualidadeArquivo()

    resultado = service.analise_documento(
        {
            "conteudo": "A" * 500
        }
    )

    assert resultado["score_conteudo"] == 40

    assert resultado["classificacao"] == "REPROVADO"


def test_documento_bom():

    service = ServiceQualidadeArquivo()

    resultado = service.analise_documento(
        {
            "conteudo": "A" * 3000
        }
    )

    assert resultado["score_conteudo"] == 70

    assert resultado["classificacao"] == "BOM"


def test_documento_excelente():

    service = ServiceQualidadeArquivo()

    resultado = service.analise_documento(
        {
            "conteudo": "A" * 10000
        }
    )

    assert resultado["score_conteudo"] == 100

    assert resultado["classificacao"] == "EXCELENTE"


def test_documento_muito_extenso():

    service = ServiceQualidadeArquivo()

    resultado = service.analise_documento(
        {
            "conteudo": "A" * 20000
        }
    )

    assert resultado["score_conteudo"] == 80

    assert resultado["classificacao"] == "BOM"

    assert (
        "Documento muito extenso, Recomenda-se fragmentação para RAG."
        in resultado["warnings"]
    )


def test_classificacao_reprovado():

    service = ServiceQualidadeArquivo()

    assert (
        service._classificacao_final(10)
        == "REPROVADO"
    )


def test_classificacao_regular():

    service = ServiceQualidadeArquivo()

    assert (
        service._classificacao_final(50)
        == "REGULAR"
    )


def test_classificacao_bom():

    service = ServiceQualidadeArquivo()

    assert (
        service._classificacao_final(70)
        == "BOM"
    )


def test_classificacao_excelente():

    service = ServiceQualidadeArquivo()

    assert (
        service._classificacao_final(95)
        == "EXCELENTE"
    )