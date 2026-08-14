import json

from sql.conexao_db import ConexaoDataBase


class InsercaoArquivo:

    def __init__(self):
        self.conexao = ConexaoDataBase()
        self.cursor = self.conexao.get_cursor()

    def armazenar_documento(self, documento):
        query = """
            INSERT INTO [Data_process].[tb_polaris_IA_processamento_rag]
            (
                nome_arquivo,
                caminho_arquivo_input,
                hash_arquivo,
                data_criacao,
                data_processamento,
                status_processamento,
                score_qualidade,
                caminho_arquivo_output,
                extensao_arquivo,
                score_final,
                score_estrutura,
                classificacao,
                aprovado,
                warnings
            )

            OUTPUT INSERTED.id

            VALUES
            (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        """
        self.cursor.execute(
            query,
            (
                documento["nome_arquivo"],
                documento["caminho_arquivo_input"],
                documento["hash_arquivo"],
                documento["data_criacao"],
                documento["data_processamento"],
                documento["status_processamento"],
                documento["score_qualidade"],
                documento["caminho_arquivo_output"],
                documento["extensao_arquivo"],
                documento["score_final"],
                documento["score_estrutura"],
                documento["classificacao"],
                documento["aprovado"],
                json.dumps(documento.get("warnings", []), ensure_ascii=False)
            )
        )
        resultado = self.cursor.fetchone()
        self.conexao.connection.commit()
        return resultado[0]

    def fechar_conexao(self):
        self.cursor.close()
        self.conexao.connection.close()