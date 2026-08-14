from datetime import datetime
from sql.conexao_db import ConexaoDataBase

class LogProcesso:

    def __init__(self):
        self.conexao = ConexaoDataBase()
        self.cursor = self.conexao.get_cursor()

    def insercao_log(
        self,
        id_execucao,
        nome_processo,
        tipo_processo,
        pipeline_processo,
        descricao_processo,
        nome_agente_relacionado,
        data_inicio_processo,
        data_fim_processo,
        tempo_total_execucao_ms,
        status,
        mensagem_sucesso,
        mensagem_erro,
        owner_processo,
        versao
    ):

        query = """
            INSERT INTO [Data_Adhoc].[TB_LOGS_PROCS_AI]
            (
                id_execucao,
                nome_processo,
                tipo_processo,
                pipeline_processo,
                descricao_processo,
                nome_agente_relacionado,
                data_inicio_processo,
                data_fim_processo,
                tempo_total_execucao_ms,
                status,
                mensagem_sucesso,
                mensagem_erro,
                owner_processo,
                versao,
                data_criacao_log
            )
            VALUES
            (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        """

        self.cursor.execute(
            query,
            (
                id_execucao,
                nome_processo,
                tipo_processo,
                pipeline_processo,
                descricao_processo,
                nome_agente_relacionado,
                data_inicio_processo,
                data_fim_processo,
                tempo_total_execucao_ms,
                status,
                mensagem_sucesso,
                mensagem_erro,
                owner_processo,
                versao,
                datetime.now()
            )
        )
        self.conexao.connection.commit()
        return True

    def fechar_conexao(self):
        self.cursor.close()
        self.conexao.connection.close()