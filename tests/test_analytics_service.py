import pytest

from services.analytics_service import (
    AnalyticsService
)


def test_instancia_service():

    service = AnalyticsService()

    assert service is not None


def test_documento_aprovado():

    service = AnalyticsService()

    resultado = service.analise(
        {
            "score_conteudo": 90,
            "warnings": []
        },
        {
            "score_estrutura": 80,
            "warnings": []
        }
    )

    assert resultado["score_final"] == 87.0

    assert resultado["aprovado"] is True

    assert resultado["classificacao"] == "Bom"


def test_documento_reprovado():

    service = AnalyticsService()

    resultado = service.analise(
        {
            "score_conteudo": 20,
            "warnings": []
        },
        {
            "score_estrutura": 20,
            "warnings": []
        }
    )

    assert resultado["score_final"] == 20.0

    assert resultado["aprovado"] is False

    assert resultado["classificacao"] == "Reprovado"


def test_documento_regular():

    service = AnalyticsService()

    resultado = service.analise(
        {
            "score_conteudo": 60,
            "warnings": []
        },
        {
            "score_estrutura": 40,
            "warnings": []
        }
    )

    assert resultado["score_final"] == 54.0

    assert resultado["aprovado"] is False

    assert resultado["classificacao"] == "Regular"


def test_documento_excelente():

    service = AnalyticsService()

    resultado = service.analise(
        {
            "score_conteudo": 100,
            "warnings": []
        },
        {
            "score_estrutura": 100,
            "warnings": []
        }
    )

    assert resultado["score_final"] == 100.0

    assert resultado["aprovado"] is True

    assert resultado["classificacao"] == "Excelente"


def test_consolidacao_warnings():

    service = AnalyticsService()

    resultado = service.analise(
        {
            "score_conteudo": 90,
            "warnings": [
                "Documento muito extenso."
            ]
        },
        {
            "score_estrutura": 80,
            "warnings": [
                "Documento sem tabelas."
            ]
        }
    )

    assert len(resultado["warnings"]) == 2

    assert (
        "Documento muito extenso."
        in resultado["warnings"]
    )

    assert (
        "Documento sem tabelas."
        in resultado["warnings"]
    )


def test_classificacao_reprovado():

    service = AnalyticsService()

    assert (
        service._classificacao_final(10)
        == "Reprovado"
    )


def test_classificacao_regular():

    service = AnalyticsService()

    assert (
        service._classificacao_final(50)
        == "Regular"
    )


def test_classificacao_bom():

    service = AnalyticsService()

    assert (
        service._classificacao_final(70)
        == "Bom"
    )


def test_classificacao_excelente():

    service = AnalyticsService()

    assert (
        service._classificacao_final(95)
        == "Excelente"
    )


def test_limite_aprovacao():

    service = AnalyticsService()

    resultado = service.analise(
        {
            "score_conteudo": 70,
            "warnings": []
        },
        {
            "score_estrutura": 70,
            "warnings": []
        }
    )

    assert resultado["score_final"] == 70.0

    assert resultado["aprovado"] is True