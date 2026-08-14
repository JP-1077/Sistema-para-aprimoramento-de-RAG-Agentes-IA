import pytest

from services.structure_service import (
    ServiceEstrutura
)


def test_instancia_service():

    service = ServiceEstrutura()

    assert service is not None


def test_documento_sem_estrutura():

    service = ServiceEstrutura()

    resultado = service.analisar_estrutura(
        {
            "conteudo": "Texto simples"
        }
    )

    assert resultado["score_estrutura"] < 50

    assert resultado["classificacao"] == "REPROVADO"

    assert len(resultado["warnings"]) > 0


def test_avaliacao_cabecalhos_basica():

    service = ServiceEstrutura()

    conteudo = """
# Título

## Seção

### Subseção
"""

    warnings = []

    score = service._avaliar_cabecalhos(
        conteudo,
        warnings
    )

    assert score == 10

    assert warnings == []


def test_avaliacao_cabecalhos_com_muitos_itens():

    service = ServiceEstrutura()

    conteudo = "\n".join(
        [f"# Cabeçalho {i}" for i in range(12)]
    )

    score = service._avaliar_cabecalhos(
        conteudo,
        []
    )

    assert score == 30


def test_avaliacao_cabecalhos_sem_cabecalho():

    service = ServiceEstrutura()

    warnings = []

    score = service._avaliar_cabecalhos(
        "texto simples",
        warnings
    )

    assert score == 0

    assert (
        "O documento não possui cabeçalhos."
        in warnings
    )


def test_avaliacao_paragrafos():

    service = ServiceEstrutura()

    conteudo = """

Parágrafo 1.

Parágrafo 2.

Parágrafo 3.

Parágrafo 4.

Parágrafo 5.

Parágrafo 6.

"""

    score = service._avaliar_paragrafos(
        conteudo,
        []
    )

    assert score == 20


def test_avaliacao_paragrafo_unico():

    service = ServiceEstrutura()

    warnings = []

    score = service._avaliar_paragrafos(
        "Texto único sem separação",
        warnings
    )

    assert score == 0

    assert (
        "Documento não possui separação de parágrafos."
        in warnings
    )


def test_avaliacao_listas():

    service = ServiceEstrutura()

    conteudo = """
- item 1
- item 2
- item 3
- item 4
- item 5
- item 6
"""

    score = service._avaliar_listas(
        conteudo,
        []
    )

    assert score == 20


def test_avaliacao_sem_listas():

    service = ServiceEstrutura()

    warnings = []

    score = service._avaliar_listas(
        "Texto comum",
        warnings
    )

    assert score == 0

    assert (
        "Documento sem listas."
        in warnings
    )


def test_avaliacao_tabelas():

    service = ServiceEstrutura()

    conteudo = """
| Nome | Idade |
|------|-------|
| João | 30 |
| Maria | 25 |
"""

    score = service._avaliar_tabelas(
        conteudo,
        []
    )

    assert score == 10


def test_avaliacao_sem_tabelas():

    service = ServiceEstrutura()

    warnings = []

    score = service._avaliar_tabelas(
        "Texto sem tabela",
        warnings
    )

    assert score == 0

    assert (
        "Documento sem tabelas."
        in warnings
    )


def test_avaliacao_organizacao_completa():

    service = ServiceEstrutura()

    conteudo = """
# Título

## Seção

### Subseção
"""

    score = service._avaliar_organizacao(
        conteudo,
        []
    )

    assert score == 10


def test_avaliacao_organizacao_limitada():

    service = ServiceEstrutura()

    warnings = []

    score = service._avaliar_organizacao(
        "# Apenas título",
        warnings
    )

    assert score == 5

    assert (
        "Organização do arquivo limitada."
        in warnings
    )


def test_classificacao_reprovado():

    service = ServiceEstrutura()

    assert (
        service._classificacao_final_estrutura(20)
        == "REPROVADO"
    )


def test_classificacao_regular():

    service = ServiceEstrutura()

    assert (
        service._classificacao_final_estrutura(50)
        == "REGULAR"
    )


def test_classificacao_bom():

    service = ServiceEstrutura()

    assert (
        service._classificacao_final_estrutura(70)
        == "BOM"
    )


def test_classificacao_excelente():

    service = ServiceEstrutura()

    assert (
        service._classificacao_final_estrutura(95)
        == "EXCELENTE"
    )