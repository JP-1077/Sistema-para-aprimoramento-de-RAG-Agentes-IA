#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-*/
                                                            # 1. IMPORTAÇÕES DAS BIBLIOTECAS
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-*/
from services.service_ingestao import IngestaoArquivos
from services.parser_service import ParserService
from services.metadados_service import MetadadosService
from services.quality_service import ServiceQualidadeArquivo
from services.structure_service import ServiceEstrutura
from services.analytics_service import AnalyticsService
from services.report_service import ReportService
from services.transformation_service import TransformService
from sql.conexao_db import ConexaoDataBase
from sql.insercao_info_arquivo import InsercaoArquivo
from sql.insercao_log_processo import LogProcesso

from utils.aux_insert_info_arquivos import insert_info_arquivo_bd
from utils.aux_insert_logs_processos import insert_log_processo_bd

from datetime import datetime
import warnings
import logging
import uuid


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                                        # 2. CONFIGURAÇÕES DE LOGS E WARNINGS
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger("aplicacao_qualidade_rag_knowledge")

warnings.filterwarnings("ignore", message="Your application has authenticated using end user credentials", category=UserWarning)

warnings.filterwarnings("ignore", message="Print area cannot be set to Defined name", category=UserWarning)

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                                        # 3. EXECUÇÃO DA APLICAÇÃO
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def execucao_aplicacao():

    logger.info("========== INÍCIO EXECUÇÃO DA APLICAÇÃO PROCESSAMENTO ARQUIVOS RAG ==========")
    inicio_execucao = datetime.now()
    status_processo = "SUCESSO"
    mensagem_sucesso = ("Pipeline executado com sucesso.")
    mensagem_erro = None

    try:
        ingestion = IngestaoArquivos(r"C:\projetos\pipeline-qualidade-knowledge\data\input")

        parser = ParserService()
        service_metadados = (MetadadosService())
        qualidade = (ServiceQualidadeArquivo())
        estrutura = (ServiceEstrutura())
        analytics = (AnalyticsService())
        report = (ReportService())
        transform = (TransformService())
        repository_arquivo = (InsercaoArquivo())

        arquivos = (ingestion.lista_arquivos_validos())
        logger.info(f"{len(arquivos)} arquivo(s) encontrados.")

        for arquivo in arquivos:

            logger.info(f"Processando " f"{arquivo['nome_arquivo']}")
            documento = (parser.parse_document(arquivo))
            logger.info(f"Etapa Parser: iniciando extração e interpretação do conteúdo do documento.")

            metadados = (service_metadados.extracao_metadados(arquivo))
            logger.info(f"Etapa Metadata: extraindo informações complementares do documento (autor, título, datas e propriedades do arquivo).")

            resultado_qualidade = (qualidade.analise_documento(documento))
            logger.info(f"Etapa Análise Qualidade Arquivo: avaliando completude, volume e relevância do conteúdo para utilização em bases de conhecimento de agentes de IA.")

            resultado_estrutura = (estrutura.analisar_estrutura(documento))
            logger.info(f"Etapa Análise Estrutura Arquivo: avaliando organização documental, cabeçalhos, seções, listas e demais elementos estruturais.")

            resultado_analise = (analytics.analise(resultado_qualidade,resultado_estrutura))
            logger.info(f"Etapa Anáise Final e Score: consolidando resultados das análises e calculando score final de classificação do documento.")

            caminho_relatorio = (report.relatorio(documento,resultado_analise))
            logger.info(f"Etapa Report Analitico: gerando relatório de avaliação documental em formato JSON.")

            caminho_saida_arquivo = None

            if resultado_analise["aprovado"]:
                resultado_transformacao = (transform.transformacao_documento(documento,resultado_analise))
                caminho_saida_arquivo = (resultado_transformacao.get("arquivo_md"))
                logger.info("Etapa Transform: documento aprovado e convertido para o formato Markdown padronizado.")            

            info_arquivo = (insert_info_arquivo_bd(arquivo, metadados, resultado_qualidade, resultado_estrutura, resultado_analise, caminho_saida_arquivo))
            repository_arquivo.armazenar_documento(info_arquivo)
            logger.info("Etapa Armazenamento infos banco de dados: Infos sobre os arquivos armazenadas na tabela tb_polaris_IA_processamento_rag.")

    except Exception as erro:
        logger.exception(f"Erro na execução da aplicação: {erro}")
        status_processo = "FALHA"
        mensagem_sucesso = None
        mensagem_erro = str(erro)

    finally:

        fim_execucao = datetime.now()

        log_execucao = (insert_log_processo_bd(inicio_execucao,fim_execucao,status_processo,mensagem_sucesso,mensagem_erro))

        try:

            LogProcesso().insercao_log(
                id_execucao=str(uuid.uuid4()),
                nome_processo="Aplicação Processamento de Arquivos RAG",
                tipo_processo="Automação",
                pipeline_processo= "INGESTAO -> PARSER -> METADADOS -> QUALITY -> STRUCTURE -> ANALYTICS -> REPORT -> TRANSFORM",
                descricao_processo="Aplicação desenvolvida para analisar, padronizar e transformar documentos utilizados como fontes de conhecimento para agentes de Inteligência Artificial..",
                nome_agente_relacionado="Ultracombo - Polaris AI",
                data_inicio_processo=inicio_execucao,
                data_fim_processo=fim_execucao,
                tempo_total_execucao_ms=log_execucao["tempo_execucao_ms"],
                status=log_execucao["status"],
                mensagem_sucesso=log_execucao["mensagem_sucesso"],
                mensagem_erro=log_execucao["mensagem_erro"],
                owner_processo="Joao Pedro Mendes Fonseca - Polaris AI",
                versao="1.0.0"
            )

        except Exception as erro_log:
            logger.exception(f"Erro ao registrar log: {erro_log}")

        logger.info("========== FIM EXECUÇÃO DA APLICAÇÃO PROCESSAMENTO ARQUIVOS RAG ==========")


if __name__ == "__main__":
    execucao_aplicacao()
