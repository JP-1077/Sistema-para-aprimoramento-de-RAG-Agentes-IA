from datetime import datetime


def insert_log_processo_bd(inicio_execucao,fim_execucao,status_processo, mensagem_sucesso,mensagem_erro):

    tempo_execucao_ms = int((fim_execucao -inicio_execucao).total_seconds() * 1000)

    return {
        "tempo_execucao_ms":tempo_execucao_ms,

        "status": status_processo,

        "mensagem_sucesso": mensagem_sucesso,

        "mensagem_erro": mensagem_erro
    }