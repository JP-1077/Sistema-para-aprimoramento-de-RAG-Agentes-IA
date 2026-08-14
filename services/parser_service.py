from pathlib import Path
from docx import Document
import fitz

class ParserService:
    def parse_document(self, arquivo_info):
        tipo_arquivo = arquivo_info["tipo_arquivo"].lower()

        if tipo_arquivo == ".pdf":
            return self.parse_pdf(arquivo_info)
        elif tipo_arquivo == ".docx":
            return self.parse_docx(arquivo_info)
        elif tipo_arquivo == ".md":
            return self.parse_md(arquivo_info)
        else:
            raise ValueError(f"Tipo de arquivo não suportado: {tipo_arquivo}")
    
    def parse_pdf(self, arquivo_info):
        caminho = arquivo_info["caminho"]
        documento = fitz.open(caminho)
        texto = ""

        for pagina in documento:
            texto += pagina.get_text()

        return {
            "nome_arquivo": arquivo_info["nome_arquivo"],
            "tipo_arquivo": arquivo_info["tipo_arquivo"],
            "conteudo": texto,
            "numero_paginas": len(documento)
        }
    
    def parse_docx(self, arquivo_info):
        caminho = arquivo_info["caminho"]
        documento = Document(caminho)
        paragrafos = []

        for paragrafo in documento.paragraphs:
            if paragrafo.text.strip():
                paragrafos.append(paragrafo.text)

        texto = "\n".join(paragrafos)

        return {
            "nome_arquivo": arquivo_info["nome_arquivo"],
            "tipo_arquivo": arquivo_info["tipo_arquivo"],
            "conteudo": texto,
            "qtd_paragrafos": len(paragrafos)
        }
    
    def parse_md(self, arquivo_info):
        caminho = arquivo_info["caminho"]
        with open (caminho, mode="r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()

        qtd_linhas = len(conteudo.splitlines())
        qtd_caracteres = len(conteudo)

        return {
            "nome_arquivo": arquivo_info["nome_arquivo"],
            "tipo_arquivo": arquivo_info["tipo_arquivo"],
            "conteudo": conteudo,
            "quantidade_linhas": qtd_linhas,
            "quantidade_caracteres": qtd_caracteres
        }