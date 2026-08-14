from sql.insercao_info_arquivo import InsercaoArquivo
import pytest

@pytest.fixture
def operacoes_sql():
    return InsercaoArquivo()

def test_instanciacao_operacoes(operacoes_sql):
    assert operacoes_sql is not None

def test_armazenar_documento(operacoes_sql):
    documento = {
        'nome_arquivo': 'teste.txt',
        'caminho_arquivo_input': '/caminho/para/entrada',
        'tipo_arquivo': 'texto',
        'hash_arquivo': 'abc123',
        'tamanho_arquivo': 1024,
        'data_criacao': '2023-01-01',
        'data_processamento': '2023-01-02',
        'status_processamento': 'concluido',
        'area_responsavel': 'TI',
        'projeto': 'Projeto X',
        'score_qualidade': 95,
        'caminho_arquivo_output': '/caminho/para/saida'
    }
    id = operacoes_sql.armazenar_documento(documento)
    assert id is not None

def test_busca_id_documento(operacoes_sql):
    resultado = operacoes_sql.buscar_documento_id(2)
    assert resultado is not None

def test_busca_hash_documento(operacoes_sql):
    resultado = operacoes_sql.busca_documento_hash('abc123')
    assert resultado is not None

def test_atualizacao_documento(operacoes_sql):
    documento = {
        'score_qualidade': 98,
        'data_processamento': '2023-01-03'
    }
    resultado = operacoes_sql.atualizacao_documento(1, documento)
    assert resultado is not None

def test_deletar_documento(operacoes_sql):
    resultado = operacoes_sql.deletar_documento(2)
    assert resultado is not None

def test_deletar_documento_id(operacoes_sql):
    resultado = operacoes_sql.deletar_documento(3)
    assert resultado is not None