from pathlib import Path
import pandas as pd
from docx import Document
import pymupdf
import fitz
from datetime import datetime
from openpyxl import load_workbook


class MetadadosService:
    def extracao_metadados(self, arquivo_info):

        tipo_arquivo = arquivo_info["tipo_arquivo"].lower()

        if tipo_arquivo == ".pdf":
            return self._metadados_pdf(arquivo_info)
        elif tipo_arquivo == ".docx":
            return self._metadados_docx(arquivo_info)
        elif tipo_arquivo == ".md":
            return self._metadados_md(arquivo_info)
        else:
            raise ValueError(f"Tipo de arquivo não suportado: {tipo_arquivo}")
    
    def _metadados_base(self, caminho):

        return {
            "tamanho_arquivo": Path(caminho).stat().st_size,
            "data_criacao": datetime.fromtimestamp(Path(caminho).stat().st_ctime),
            "data_modificacao": datetime.fromtimestamp(Path(caminho).stat().st_mtime)
        }

    def _metadados_pdf(self, arquivo_info):
        caminho = arquivo_info["caminho"]
        documento = fitz.open(caminho)
        metadata = documento.metadata
        metadados_pdf = self._metadados_base(caminho)

        metadados_pdf.update({
            "titulo": metadata.get("title"),
            "numero_paginas": len(documento)
        })

        return metadados_pdf

    def _metadados_docx(self, arquivo_info):
        caminho = arquivo_info["caminho"]
        documento = Document(caminho)
        propriedades = documento.core_properties
        metadados_docx = self._metadados_base(caminho)

        metadados_docx.update({
            "autor": propriedades.author,
            "titulo": propriedades.title,
            "assunto": propriedades.subject,
            "categoria": propriedades.category,
            "ultima_modificacao_por": propriedades.last_modified_by,
            "data_criacao_documento": propriedades.created,
            "data_modificacao_documento": propriedades.modified
        })

        return metadados_docx
    
    def _metadados_md(self, arquivo_info):
        caminho = arquivo_info["caminho"]
        metadados_md = self._metadados_base(caminho)
        with open (caminho, mode="r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()

        qtd_linhas = len(conteudo.splitlines())
        qtd_caracteres = len(conteudo)
        qtd_cabecalhos = sum(1 for linha in conteudo.splitlines() if linha.strip().startswith("#"))

        metadados_md.update({
            "quantidade_linhas": qtd_linhas,
            "quantidade_caracteres": qtd_caracteres,
            "quantidade_cabecalhos": qtd_cabecalhos
        })

        return metadados_md
        

    