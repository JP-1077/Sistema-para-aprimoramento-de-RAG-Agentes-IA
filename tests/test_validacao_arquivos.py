from pathlib import Path
from services.service_ingestao import IngestaoArquivos
import pytest
import pytest_cov

@pytest.fixture
def ingestao():
    return IngestaoArquivos()

@pytest.fixture
def arquivos_pasta(tmp_path):
    (tmp_path / "arquivo1.pdf").write_text("pdf")
    (tmp_path / "arquivo2.docx").write_text("docx")
    (tmp_path / "arquivo3.exe").write_text("exe")
    (tmp_path / "arquivo4.xlsx").write_text("xlsx")
    return tmp_path

@pytest.mark.parametrize(
    "arquivo,esperado",
    [
        ("documento.pdf", True),
        ("documento.docx", True),
        ("documento.xlsx", True),
        ("documento.md", True),
        ("imagem.jpg", False),
        ("arquivo.exe", False),
        ("arquivo.zip", False),
    ]
)
def test_validacao_arquivos(ingestao, arquivo, esperado):
    assert ingestao.validacao_arquivos(Path(arquivo)) == esperado

def test_validacao_arquivo_extensao_maiscula(ingestao):
    assert ingestao.validacao_arquivos(Path("ARQUIVO.PDF"))

def test_validacao_arquivo_sem_extensao(ingestao):
    assert not ingestao.validacao_arquivos(Path("arquivo"))

def test_lista_arquivos_validos(ingestao,arquivos_pasta):
    ingestao.caminho_pasta_input_arquivos = (arquivos_pasta)
    arquivos = ingestao.lista_arquivos_validos()

    assert arquivos == [
        "arquivo1.pdf",
        "arquivo2.docx",
        "arquivo4.xlsx",
    ]

def test_contagem_arquivos_validos(ingestao, arquivos_pasta):
    ingestao.caminho_pasta_input_arquivos = (arquivos_pasta)
    assert ingestao.contagem_arquivos() == 3

def test_contagem_arquivos_pasta_vazia(ingestao, tmp_path):
    ingestao.caminho_pasta_input_arquivos = tmp_path
    assert ingestao.contagem_arquivos() == 0

