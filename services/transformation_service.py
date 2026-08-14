import re
from pathlib import Path
from docx import Document

class TransformService:
    
    APROVACAO = 70

    def __init__(self):
        self.output_path = Path(r"C:\projetos\pipeline-qualidade-knowledge\data\output")

        self.output_path.mkdir(parents=True, exist_ok=True)

    def transformacao_documento(self, documento, resultado_analise):

        if not resultado_analise["aprovado"]:
            return {"transformado": False, "motivo": "Documento reprovado na análise."}

        padronizacao_conteudo_documento = (self.padronizacao_documento(documento["conteudo"]))

        conteudo_estruturado = (self.estruturacao_markdown(padronizacao_conteudo_documento))

        transformacao_md = self._gera_markdown(documento, conteudo_estruturado)

        return {"transformado": True, "arquivo_md" : transformacao_md}
    
    def padronizacao_documento(self, conteudo):
        conteudo = re.sub(r"\n\s*\n", "\n\n", conteudo)
        conteudo = re.sub(r"[ \t]+", " ", conteudo)
        return conteudo.strip()
    
    def estruturacao_markdown(self, conteudo):
        linhas = []

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

            linhas.append(linha)
        return "\n\n".join(linhas)
    
    def _gera_markdown(self, documento, conteudo):
        nome_arquivo = (Path (documento["nome_arquivo"]).stem)
        caminho_md = (self.output_path/f"{nome_arquivo}.md")
        markdown = f"""
        # Documento .md
        ## Nome do Documento
        {nome_arquivo}
        ## Conteúdo
        {conteudo}

        """
        with open(caminho_md, "w", encoding="utf-8") as arquivo:
            arquivo.write(markdown)

        return str(caminho_md)

