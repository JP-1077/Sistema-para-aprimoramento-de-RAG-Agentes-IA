import pytest
from sql.conexao_db import ConexaoDataBase


def test_instancia_conexao():
    conexao = ConexaoDataBase()
    assert conexao is not None

def test_cursor_sqlserver():
    conexao = ConexaoDataBase()
    cursor = conexao.get_cursor()
    assert cursor is not None
    conexao.close_conexao()

def test_consulta_sqlserver():
    conexao = ConexaoDataBase()
    cursor = conexao.get_cursor()
    cursor.execute("SELECT 1")
    resultado = cursor.fetchone()
    assert resultado[0] == 1
    conexao.close_conexao()