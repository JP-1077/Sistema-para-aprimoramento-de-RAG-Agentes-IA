import pyodbc
import logging
import os
from dotenv import load_dotenv

load_dotenv()

class ConexaoDataBase:
    def __init__(self):
        servidor_db = os.getenv("SERVIDOR_DB")
        banco_dados = os.getenv("DATABASE")
        trusted_connection = os.getenv("TRUSTED_CONNECTION")
        driver = os.getenv("DRIVER")

        self.string_conexao = (
            f"Driver={driver};"
            f"Server={servidor_db};"
            f"Database={banco_dados};"
            f"Trusted_Connection={trusted_connection};"
        )

        self.connection = None

    def conexao(self):
        if self.connection is None:
            self.connection = pyodbc.connect(
                self.string_conexao
            )
        return self.connection

    def get_cursor(self):
        conexao = self.conexao()
        return conexao.cursor()

    def close_conexao(self):
        if self.connection:
            self.connection.close()
            self.connection = None