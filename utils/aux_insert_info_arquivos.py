from datetime import datetime


def insert_info_arquivo_bd(arquivo, metadados, resultado_qualidade, resultado_estrutura, resultado_analise, caminho_saida_arquivo):

    return {
        "nome_arquivo": arquivo["nome_arquivo"],
        "caminho_arquivo_input": arquivo["caminho"],
        "hash_arquivo": None,
        "data_criacao": metadados.get("data_criacao"),
        "data_processamento": datetime.now(),
        "status_processamento":("APROVADO" if resultado_analise["aprovado"] else "REPROVADO"),
        "score_qualidade":resultado_qualidade["score_conteudo"],
        "caminho_arquivo_output":caminho_saida_arquivo,
        "extensao_arquivo":arquivo["tipo_arquivo"],
        "score_final":resultado_analise["score_final"],
        "score_estrutura":resultado_estrutura["score_estrutura"],
        "classificacao":resultado_analise["classificacao"],
        "aprovado":str(resultado_analise["aprovado"]),
        "warnings":resultado_analise["warnings"]
    }