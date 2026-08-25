#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-*/
                                                                # 1. IMPORTAÇÕES DAS BIBLIOTECAS
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-*/
from datetime import datetime
import warnings
import logging
import uuid
import os
from pathlib import Path
import pandas as pd
from docx import Document
import pymupdf
import fitz
from datetime import datetime
from openpyxl import load_workbook
import re
import json
import pyodbc
import uuid


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-*/
                                                            # 2. CONFIGURAÇÕES DE LOGS E WARNINGS
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-*/

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger("aplicacao_qualidade_arquivos_rag_AI")

warnings.filterwarnings("ignore", message="Your application has authenticated using end user credentials", category=UserWarning)

warnings.filterwarnings("ignore", message="Print area cannot be set to Defined name", category=UserWarning)


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                                # 3. CONEXÃO COM BANCO DE DADOS E CONFIGURAÇÕES PARA DADOS USUARIO
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def dados_usuario_aplicacao ():
    """
    Esta função identifica o usuário logado no sistema operacional da máquina (Windows) 
    por meio da variável de ambiente 'USER PROFILE'. Representando o id do usuário da 
    máquina que está executando o processo

    Saida da função:
        string: Matricula do usuario 
    """

    logger.info("ETAPA [CONEXAO]: Identificando usuário do sistema operacional")
    coleta_usuario = os.path.basename(os.environ['USERPROFILE'])
    logger.info(f"Matricula usuario identificada: {coleta_usuario}")
    return coleta_usuario



def conexao_banco_dados():
    """
    Esta função realiza a abertura de conexão com o banco SQL Server (BDS) e retorna 
    conexão e cursor.

    Saida da função:
        Conexão ativa e um cursor associado para exec de comandos SQL no banco BDS

    Obs:
        Necessita a instalação do driver ODBC do SQL Server instalado e configurado na máquina
    """

    logger.info("ETAPA [CONEXAO]: Iniciando conexão com Banco de Dados BDS")

    try:
        dados_conexao_sql = (
            'Driver={SQL Server};'
            'Server=Snepdb56c01;'
            'Database=BDS;'
            'Trusted_Connection=yes;'
        )
        conexao = pyodbc.connect(dados_conexao_sql)
        cursor = conexao.cursor()

        logger.info("ETAPA [CONEXAO]: Conectado com sucesso ao banco BDS")
        return conexao, cursor
    
    except Exception as e:
        logger.exception(f"ETAPA [CONEXAO]: Erro ao conectar ao banco BDS: {e}")
        raise


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                                        # 4. ENTRADA (INGESTÃO ARQUIVOS)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def ingestao_arquivos(caminho_input):
    """
    Esta função possui como objetivo principal realiza a identificação de arquivos 
    válidos disponíveis na pasta de entrada da aplicação

    Saída da função:
        lista:
            Lista contendo os arquivos válidos
            encontrados para processamento.
    """

    logger.info("ETAPA [INPUT]: Iniciando identificação dos arquivos da pasta de entrada.")

    try:
        caminho_input = Path(caminho_input)
        caminho_input.mkdir(parents=True, exist_ok=True)

        extensoes_validas = [".docx", ".pdf", ".md"]

        arquivos_validos = []

        for arquivo in caminho_input.iterdir():

            if not arquivo.is_file():
                continue

            if arquivo.suffix.lower() not in extensoes_validas:
                continue

            arquivos_validos.append(
                {
                    "nome_arquivo": arquivo.name,
                    "tipo_arquivo": arquivo.suffix.lower(),
                    "caminho": str(arquivo)
                }
            )

        logger.info(f"ETAPA [INPUT]: " f"{len(arquivos_validos)} arquivo(s) válido(s) encontrado(s).")

        if arquivos_validos:
            logger.info (f"ETAPA [INPUT]: Os arquivos identificados para processamento são:")
            for indice, arquivo in enumerate(arquivos_validos, start=1):
                logger.info(f"[{indice}]" f"{arquivo['nome_arquivo']}")

        else:
            logger.warning("ETAPA [INPUT]: Nenhum arquivo válido foi encontrado.")
                
        return arquivos_validos
    
    except Exception as e:
        logger.exception(f"ETAPA [INPUT]: Erro na etapa de ingestão arquivos: {e}")


    
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                                            # 5. PROCESSAMENTO ARQUIVOS
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                        # 5.1 SERVICE - PARSER ARQUIVO
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def extracao_conteudo(arquivo_info):
    """
    Esta função realiza a leitura e extração do conteúdo dos arquivos validos 
    pela aplicação.

    Saída da função:
        dicionario:
            -nome_arquivo
            -tipo_arquivo
            -conteudo
    """
    logger.info(f"ETAPA [PARSER]: Iniciando etapa de extração de conteudo do arquivo.")

    try:   
        tipo_arquivo = (arquivo_info["tipo_arquivo"].lower())
        caminho_arquivo = (arquivo_info["caminho"])

        if tipo_arquivo == ".pdf":
            documento_pdf = fitz.open(caminho_arquivo)
            conteudo_documento = ""

            for pagina in documento_pdf:
                conteudo_documento += pagina.get_text()

            resultado_parser = {
                "nome_arquivo": arquivo_info["nome_arquivo"],
                "tipo_arquivo": arquivo_info["tipo_arquivo"],
                "conteudo": conteudo_documento,
                "numero_paginas": len(documento_pdf)
            }

        elif tipo_arquivo == ".docx":
            documento_docx = Document(caminho_arquivo)
            paragrafos = []

            for paragrafo in documento_docx.paragraphs:

                if paragrafo.text.strip():
                    paragrafos.append(paragrafo.text)

            resultado_parser = {
                "nome_arquivo": arquivo_info["nome_arquivo"],
                "tipo_arquivo": arquivo_info["tipo_arquivo"],
                "conteudo": "\n".join(paragrafos),
                "quantidade_paragrafos": len(paragrafos)
            }

        elif tipo_arquivo == ".md":
            with open (caminho_arquivo, mode="r", encoding="utf-8") as arquivo:
                conteudo = arquivo.read()

            resultado_parser = {
                "nome_arquivo": arquivo_info["nome_arquivo"],
                "tipo_arquivo": tipo_arquivo,
                "conteudo": conteudo,
                "quantidade_linhas": len(conteudo.splitlines()),
                "quantidade_caracteres": len(conteudo)
            }

        else:
            raise ValueError(f"Tipo de arquivo não suportado pela aplicação: {tipo_arquivo}")
        
        logger.info(f"ETAPA [PARSER]: Extração de conteúdo concluída com sucesso. A qtd caracteres foi: {len(resultado_parser['conteudo'])}")

        return resultado_parser
    
    except Exception as e:
        logger.exception(f"ETAPA [PARSER]: Erro na etapa de extração de conteudo do arquivo: {e}")


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                        # 5.2 SERVICE - METADADOS ARQUIVO
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def extracao_metadados(arquivo_info):
    """
    Esta função realiza a leitura e extração doS metadados dos arquivos validos 
    pela aplicação.

    Saída da função:
        dicionario: Contendo informações de metadados dos arquivos processados
    """

    logger.info(f"ETAPA [METADADOS]: Iniciando etapa de extração de metadados do arquivo: {arquivo_info['nome_arquivo']}")

    try:
        tipo_arquivo = (arquivo_info["tipo_arquivo"].lower())
        caminho_arquivo = Path(arquivo_info["caminho"])

        metadados = {
            "tamanho_arquivo": caminho_arquivo.stat().st_size,

            "data_criacao": datetime.fromtimestamp(caminho_arquivo.stat().st_ctime),

            "data_modificacao": datetime.fromtimestamp(caminho_arquivo.stat().st_mtime)
        }

        if tipo_arquivo == ".pdf":
            documento_pdf = fitz.open(str(caminho_arquivo))

            propriedades_pdf = (documento_pdf.metadata)

            metadados.update({

                "titulo": propriedades_pdf.get("title"),

                "autor": propriedades_pdf.get("author"),

                "numero_paginas": len(documento_pdf)})

        elif tipo_arquivo == ".docx":
            documento_docx = Document(str(caminho_arquivo))

            propriedades_docx = (documento_docx.core_properties)

            metadados.update({
                "autor": propriedades_docx.author,

                "titulo": propriedades_docx.title,

                "assunto": propriedades_docx.subject,

                "categoria": propriedades_docx.category,

                "ultima_modificacao_por": propriedades_docx.last_modified_by,

                "data_criacao_documento": propriedades_docx.created,

                "data_modificacao_documento": propriedades_docx.modified
            })

        elif tipo_arquivo == ".md":
            with open(caminho_arquivo, mode="r", encoding="utf-8") as arquivo:

                conteudo = (arquivo.read())

            metadados.update({
                "quantidade_linhas": len(conteudo.splitlines()),

                "quantidade_caracteres": len(conteudo),

                "quantidade_cabecalhos": sum(1 for linha in conteudo.splitlines() if linha.strip().startswith("#"))
            })

        else:
            raise ValueError(f"Tipo de arquivo não suportado pela aplicação: {tipo_arquivo}")
        
        logger.info(f"ETAPA [METADADOS]: Extração de metadados do arquivo concluído com sucesso. No arquivo {arquivo_info['nome_arquivo']} ")
        
        return metadados
    
    except Exception as e:
        logger.exception(f"ETAPA [METADADOS]: Erro na etapa de extração de metadados do arquivo: {e}")


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                        # 5.3 SERVICE - ANALYTICS
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                # ANALISE CONTEUDO ARQUIVO
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==
def analise_conteudo_arquivo(documento):
    """
    Esta função é responsável por aplicar uma análise do conteúdo do arquivo referente 
    a sua extensiabilidade e tamanho.  
    
    Saída da função:
        dicionario contendo as sseguintes informações:
            - score_conteudo,
            - classificacao:,
            - warnings,
            - data_analise
    """

    logger.info(f"ETAPA [ANALYTICS]: Iniciando análise de qualidade do conteúdo do arquivo.")

    try:
        conteudo = documento.get("conteudo", "")
        warnings = []
        quantidade_caracteres = len(conteudo.strip())

        if quantidade_caracteres == 0:
            score_conteudo = 0
            classificacao = "REPROVADO"
            warnings.append("Documento sem conteúdo. Não foi possível realizar a avaliação da qualidade do conteúdo.")

        elif quantidade_caracteres <= 100:
            score_conteudo = 20
            classificacao = "REPROVADO"
            warnings.append("Documento possui quantidade insuficiente de informações. Portanto, não recommenda-se aplica-lo como fonte de conhecimento.")

        elif quantidade_caracteres <= 1000:
            score_conteudo = 40
            classificacao = "REPROVADO"
            warnings.append("O conteúdo do documento é invalido para os formatos adequados de fonte de conhecimento para agentes de IA. Apresentando informações insuficientes para o agente.")

        elif quantidade_caracteres <= 5000:
            score_conteudo = 70
            classificacao = "BOM"

        elif quantidade_caracteres <= 15000:
            score_conteudo = 100
            classificacao = "EXCELENTE"

        else:
            score_conteudo = 80
            classificacao = "REPROVADO"
            warnings.append("O conteúdo do documento é muito extenso. Recomenda-se fragmentação do conteúdo para otimizar recuperação de informação pelo agente de IA.")

        logger.info(f"ETAPA [ANALYTICS]: Análise de conteúdo concluída |" f"Score Qualidade do Conteúdo: {score_conteudo} | " f"Classificação: {classificacao}")

        if warnings:
            logger.warning(f"Warnings identificados no arquivo: " f"{warnings}")

        return {
            "score_conteudo": score_conteudo,
            "classificacao": classificacao,
            "warnings": warnings,
            "data_analise": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.exception(f"ETAPA [ANALYTICS]: Erro na etapa de análise de qualidade do conteudo: {e}")


##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
            #  ANALISE ESTRUTURA ARQUIVO
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==

def analise_estrutura_documento(documento):
    """
    Esta função é responsável por aplicar uma análise da estrutura do arquivo referente 
    a sua organização e separação do conteudo.  
    
    Saída da função:
        dicionario contendo as sseguintes informações:
            - score_conteudo,
            - classificacao:,
            - warnings,
            - data_analise
    """

    logger.info(f"ETAPA [ANALYTICS]: Iniciando análise de estrutura do conteúdo do arquivo.")

    try:
        conteudo = documento.get("conteudo", "")
        warnings = []
        score_estrutura_arquivo = 0

        # Avaliação de cabecalhos
        quantidade_cabecalhos = len(re.findall(r"^#{1,6}\s", conteudo, re.MULTILINE))
        logger.info(f"Quantidade de cabeçalhos identificados: " f"{quantidade_cabecalhos}")

        if quantidade_cabecalhos == 0:
            warnings.append("O Documento não possui cabeçalhos.")

        elif quantidade_cabecalhos <= 3:
            score_estrutura_arquivo += 10

        elif quantidade_cabecalhos <= 10:
            score_estrutura_arquivo += 20

        else:
            score_estrutura_arquivo += 30

        # Avaliação de Parágrafos
        quantidade_paragrafos = len([p for p in conteudo.split("\n\n") if p.strip()])
        logger.info(f"Quantidade de paragrafos identificados: " f"{quantidade_paragrafos}")

        if quantidade_paragrafos <= 1:
            warnings.append("O Documento não possui separação de parágrafos.")

        elif quantidade_paragrafos <= 5:
            score_estrutura_arquivo += 10

        else: 
            score_estrutura_arquivo += 20

        # Avaliação de Organização .md
        possui_titulo = "#" in conteudo
        possui_secao = "##" in conteudo
        possui_subsecao = "###" in conteudo

        if (possui_titulo and possui_secao and possui_subsecao):
            score_estrutura_arquivo += 10

        else:
            score_estrutura_arquivo += 5
            warnings.append("Organização estrutural do documento limitada.")

        
        if score_estrutura_arquivo >= 90:
            classificacao = "EXCELENTE"

        elif score_estrutura_arquivo >= 70:
            classificacao = "BOM"

        elif score_estrutura_arquivo >= 50:
            classificacao = "REGULAR"

        else:
            classificacao = "REPROVADO"

        logger.info(f"Análise estrutural concluída | " f"Score Estrutura: {score_estrutura_arquivo} | " f"Classificação: {classificacao}")

        if warnings:
            logger.warning(f"Warnings de analise estrutura identificados no arquivo: " f"{warnings}")

        return {
            "score_estrutura": score_estrutura_arquivo,
            "classificacao": classificacao,
            "warnings": warnings,
            "data_analise": datetime.now().isoformat()
        }

    except Exception as e:
        logger.exception(f"ETAPA [ANALYTICS]: Erro na etapa de análise de estrutura do conteudo: {e}")


##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
            # ANALISE FINAL ARQUIVO (SCORE ARQUIVO)
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==

def analise_final_score_arquivo (resultado_qualidade, resultado_estrutura):
    """
    Esta função é responsável por aplicar a análise final do arquivo criando um score final
    utilizando como base a avaliação de conteudo e estrutura.  
    
    Saída da função:
        dicionario contendo as sseguintes informações:
            - score_final,
            - score_qualidade,
            - score_estrutura,
            - classificacao
            - aprovado
            - warnings
            - data analise
    """

    logger.info(f"ETAPA [ANALYTICS]: Iniciando análise final do arquivo e gerando score.")

    try:
        warnings = []
        warnings.extend(resultado_qualidade.get("warnings",[]))
        warnings.extend(resultado_estrutura.get("warnings",[])) 

        score_qualidade = resultado_qualidade["score_conteudo"]
        score_estrutura = resultado_estrutura["score_estrutura"]
        logger.info(f"Score de qualidade do arquivo: " f"{score_qualidade}")
        logger.info(f"Score de estrutura do arquivo: " f"{score_estrutura}")

        score_final = round((score_qualidade * 0.7 + score_estrutura * 0.3), 2) 

        if score_final >= 90:
            classificacao = "Excelente"
    
        elif score_final >= 70:
            classificacao = "Bom"
    
        elif score_final >= 50:
            classificacao = "Regular"

        else:
            classificacao = "Reprovado"

        aprovacao = score_final >= 70
    
        logger.info(f"Score final concluído: " f"Score final: {score_final} | "  f"Classificação: " f"{classificacao} | " f"Aprovado: " f"{aprovacao}")

        return {
            "score_final": score_final,
            "score_qualidade": score_qualidade,
            "score_estrutura": score_estrutura,
            "classificacao": classificacao,
            "aprovado": aprovacao,
            "warnings":warnings,
            "data_analise": datetime.now().isoformat()
        }

    except Exception as e:
        logger.exception(f"ETAPA [ANALYTICS]: Erro na etapa de análise final e criação do score: {e}")


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                                            # 6. SAÍDAS (REPORT E TRANSFORMAÇÃO)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                        # 6.1 SERVICE - REPORT
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def relatorio_json(documento, resultado_analise):
    """
    Essa função é responsável pela criação do report analitico do arquivo processado
    Na qual contém informações sobre todo o processamento e análise aplicadas no arquivo.

    Saída:
        str: Caminho de saída do arquivo
    """

    logger.info(f"ETAPA [REPORT]: Iniciando criação relatório de avaliação documental em formato JSON.")

    try:
        caminho_entrada_report_json = (r"C:\projetos\pipeline-qualidade-knowledge\data\reports\report_transformacao_arquivo.json")
        
        with open(caminho_entrada_report_json, "r", encoding="utf-8") as arquivo_json:
            estrutura_card = json.load(arquivo_json)

        warnings_documento = (resultado_analise.get("warnings",[]))
        warnings_formatado = ("Nenhum warning identificado.")

        if warnings_documento:
            warnings_formatado = "\n".join(warnings_documento)


        dados_report = {
            "nome_arquivo": documento["nome_arquivo"],

            "tipo_arquivo": documento["tipo_arquivo"],

            "score_qualidade": resultado_analise["score_qualidade"],

            "score_estrutura": resultado_analise["score_estrutura"],

            "score_final": resultado_analise["score_final"],

            "classificacao": resultado_analise["classificacao"],

            "aprovado":("SIM" if resultado_analise["aprovado"] else "NÃO"),

            "warnings": warnings_formatado,

            "data_analise": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }

        estrutura_card_str = json.dumps(estrutura_card)
        for chave, valor in dados_report.items():
            placeholder = "{{" + chave + "}}"
            valor = json.dumps(str(valor), ensure_ascii=False)[1:-1]
            estrutura_card_str = (estrutura_card_str.replace(placeholder, valor))
        estrutura_card = json.loads(estrutura_card_str)

        
        caminho_output = Path(r"C:\projetos\pipeline-qualidade-knowledge\data\reports\output")
        caminho_output.mkdir(parents=True, exist_ok=True)
        nome_arquivo = Path(documento["nome_arquivo"]).stem
        caminho_saida_report = caminho_output / f"{nome_arquivo}_adaptive_card.json"

        with open(caminho_saida_report, "w", encoding="utf-8") as arquivo_json_saida:
            json.dump(estrutura_card, arquivo_json_saida, ensure_ascii=False, indent=4)
        
        logger.info("ETAPA [REPORT] - Criação report analitico do arquivo concluido com sucesso.")

        return str(caminho_saida_report)

    except Exception as e:
        logger.exception(f"Erro ao gerar Adaptive Card: {e}")

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                    # 6.2 SERVICE - TRANSFORMAÇÃO ARQUIVO
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


def transformacao_arquivo (documento, resultado_analise):
    """
    Esta função realiza a transformação dos documentos
    aprovados em arquivos Markdown (.md).

    Saída da função:
        dicionario:
            "transformado": bool,
            "arquivo_md": str
    
    """

    logger.info("ETAPA [TRANSFORMAÇÃO]: Iniciando etapa de transformação arquivo.")

    try:
        if not resultado_analise["aprovado"]:
            logger.warning("Documento não pode ser transformado. Pois, foi reprovado na análise")

            return {"transformado": False, "motivo": "Documento reprovado nas análises."}
    
        caminho_saida_arquivos = Path(r"C:\projetos\pipeline-qualidade-knowledge\data\output")
        caminho_saida_arquivos.mkdir(parents=True, exist_ok=True)
        nome_arquivo = (Path (documento["nome_arquivo"]).stem)
        caminho_arquivo_saida = (caminho_saida_arquivos/f"{nome_arquivo}.md")

        conteudo = documento.get("conteudo", "")
        conteudo = re.sub(r"\n\s*\n", "\n\n", conteudo)
        conteudo = re.sub(r"[ \t]+", " ", conteudo)
        conteudo = conteudo.strip()

        linhas_markdown = []

        for linha in conteudo.splitlines():
            linha = linha.strip()
            if not linha:
                continue

            if re.match(r"^\d+\.\s", linha):
                linha = re.sub(r"^\d+\.\s*", "## ", linha)

            elif re.match(r"^\d+\.\d+\s*", linha):
                linha = re.sub(r"^\d+\.\d+\s*", "### ", linha)

            elif re.match(r"^\d+\.\d+\.\d+\s*", linha):
                linha = re.sub(r"^\d+\.\d+\.\d+\s*", "#### ", linha)

            linhas_markdown.append(linha)

        conteudo_transformado = "\n\n".join(linhas_markdown)

        markdown = f"""
            # Documento .md
            ## Nome do Documento
            {nome_arquivo}
            ## Conteúdo
            {conteudo_transformado}

        """
        with open(caminho_arquivo_saida, mode="w", encoding="utf-8") as arquivo:
            arquivo.write(markdown)

        logger.info("ETAPA [TRANSFORMAÇÃO]: A transformação do arquivo em markdown concluída com sucesso: " f"{caminho_arquivo_saida}")

        return {"transformado": True, "arquivo_md" : str(caminho_arquivo_saida)}
    
    except Exception as e:
        logger.exception(f"ETAPA [TRANSFORMAÇÃO]: Erro durante a transformação do documento: {e}")



#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                        # 7. BANCO DE DADOS: ARMAZENAMENTO INFO ARQUIVOS E INSERÇÃO LOG PROCESSO
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                # 7.1 ARMAZENAMENTO INFORMAÇÕES ARQUIVO DB
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def armazenamento_dados_arquivos_db(cursor, conexao,documento):

    logger.info("ETAPA [DATABASE]: Iniciando etapa de peristência informações no banco.")
    nome_tabela = "[Data_process].tb_polaris_IA_processamento_rag"

    try:
        query_comando_insert = """            
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

            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(
            query_comando_insert,
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
        resultado = cursor.fetchone()
        conexao.commit()
        if resultado is None:
            raise RuntimeError("Não foi possível recuperar o ID do registro inserido.")
        id_registro = resultado[0]
        logger.info("ETAPA [DATABASE]: " f"Persistência dos dados concluída com sucesso. " f"Tabela: {nome_tabela} | " f"ID Registro: {id_registro}")
        return id_registro
    
    except Exception as e:
        conexao.rollback()
        logger.exception(f"ETAPA [DATABASE]: Erro na etapa de persistir dados no banco de dados: {e}")
        raise

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                    # 7.2 INSERÇÃO DE LOG DO PROCESSO
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def insercao_log_db(cursor, conexao, inicio_execucao, fim_execucao, status_processo, mensagem_sucesso_execucao, mensagem_falha_execucao):

    logger.info("ETAPA [DATABASE]: Iniciando etapa de inserção de log da automação.")
    nome_tabela_log = "[Data_Adhoc].TB_LOGS_PROCS_AI"

    try:
        tempo_total_execucao_ms = int((fim_execucao - inicio_execucao).total_seconds() * 1000)
        
        query_insert_log = """
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
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(
            query_insert_log,
            (
                str(uuid.uuid4()),
                "Aplicação Processamento de Arquivos RAG",
                "Automação",
                "INGESTAO -> PARSER -> METADADOS -> QUALITY -> STRUCTURE -> ANALYTICS -> REPORT -> TRANSFORM",
                "Aplicação desenvolvida para analisar, padronizar e transformar documentos utilizados como fontes de conhecimento para agentes de Inteligência Artificial.",
                "Ultracombo - Polaris AI",
                inicio_execucao,
                fim_execucao,
                tempo_total_execucao_ms,
                status_processo,
                mensagem_sucesso_execucao,
                mensagem_falha_execucao,
                "Joao Pedro Mendes Fonseca - Polaris AI",
                "2.0.0",
                datetime.now()
            )
        )
        conexao.commit()
        logger.info(f"ETAPA [DATABASE]: Etapa criação de log do processo concluído com sucesso na tabela {nome_tabela_log}")

    except Exception as e:
         conexao.rollback()
         logger.info(f"ETAPA [DATABASE]: Erro na etapa de criação de log da automação: {e}")


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                                            # 6. EXECUÇÃO DA APLICAÇÃO
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


def execucao_aplicacao():
    """
    Função principal responsável por orquestrar a execução completa
    da aplicação de processamento de arquivos para RAG.

    Saídas:
        0: execução concluída com sucesso
        1: execução concluída com uma ou mais falhas

    """
    logger.info("========== INÍCIO EXECUÇÃO DA APLICAÇÃO PROCESSAMENTO ARQUIVOS RAG ==========")


    inicio_execucao = datetime.now()
    logger.info("Data/Hora Início: %s", inicio_execucao.strftime("%d/%m/%Y %H:%M:%S"))

    status_processo = "SUCESSO"
    mensagem_sucesso = "Automação executada com sucesso"
    mensagem_erro = None

    conexao = None
    cursor = None

    try:
        usuario_execucao = (dados_usuario_aplicacao())

        conexao, cursor = conexao_banco_dados()

        arquivos = ingestao_arquivos( r"C:\projetos\pipeline-qualidade-knowledge\data\input")
        total_arquivos = len(arquivos)
        
        for indice, arquivo in enumerate(arquivos, start=1):

            documento = extracao_conteudo(arquivo)
            metadados = extracao_metadados(arquivo)
            resultado_qualidade = analise_conteudo_arquivo(documento)
            resultado_estrutura = analise_estrutura_documento(documento)
            resultado_analise = analise_final_score_arquivo(resultado_qualidade, resultado_estrutura)
            resultado_transformacao = transformacao_arquivo(documento, resultado_analise)

            caminho_arquivo_saida = None

            if resultado_transformacao["transformado"]:
                caminho_arquivo_saida = (resultado_transformacao["arquivo_md"])
            caminho_relatorio = (relatorio_json(documento, resultado_analise))

            dados_documento = {
                "nome_arquivo": documento["nome_arquivo"],
                "caminho_arquivo_input": arquivo["caminho"],
                "hash_arquivo": None,
                "data_criacao": metadados.get("data_criacao"),
                "data_processamento": datetime.now(),
                "status_processamento": ("APROVADO" if resultado_analise["aprovado"] else "REPROVADO"),
                "score_qualidade": resultado_qualidade["score_conteudo"],
                "caminho_arquivo_output": caminho_arquivo_saida,
                "extensao_arquivo":documento["tipo_arquivo"],
                "score_final":resultado_analise["score_final"],
                "score_estrutura": resultado_analise["score_estrutura"],
                "classificacao":resultado_analise["classificacao"],
                "aprovado":("SIM" if resultado_analise["aprovado"] else "NÃO"),
                "warnings": resultado_analise["warnings"]
            }

            armazenamento_dados_arquivos_db(cursor, conexao, dados_documento)
            logger.info(f"Fim do Processamento Arquivo [{indice}/{total_arquivos}] " f"{arquivo['nome_arquivo']}")

        logger.info("Pipeline executado com sucesso.") 
       
    except Exception as e:
        status_processo = "FALHA"
        mensagem_sucesso = None
        mensagem_erro = str(e)

        logger.exception(f"Erro na execução da aplicação, {e}")

    finally:
        fim_execucao = datetime.now()

        try:
            if conexao and cursor:
                insercao_log_db(cursor, conexao, inicio_execucao, fim_execucao, status_processo, mensagem_sucesso, mensagem_erro)
        except Exception as erro_log:
            logger.exception(f"Erro ao registrar log da aplicação: {erro_log}")

        finally:
            try:
                if cursor:
                    cursor.close()
                if conexao:
                    conexao.close()

            except Exception:
                pass
    
        logger.info(f"Status Final: {status_processo}")
        logger.info(f"Data/Hora Início: {inicio_execucao.strftime('%d/%m/%Y %H:%M:%S')}")
        logger.info(f"Data/Hora Fim: {fim_execucao.strftime('%d/%m/%Y %H:%M:%S')}")
        tempo_total_execucao_ms = int((fim_execucao - inicio_execucao).total_seconds() * 1000)
        logger.info(f"Tempo total execução: {tempo_total_execucao_ms}")
    

    logger.info("========== FIM EXECUÇÃO DA APLICAÇÃO PROCESSAMENTO ARQUIVOS RAG ==========")


if __name__ == "__main__":
    execucao_aplicacao()

    







