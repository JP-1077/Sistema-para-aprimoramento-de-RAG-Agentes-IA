from datetime import datetime
import re

class ServiceEstrutura:

    def analisar_estrutura(self, documento):
        conteudo = documento.get("conteudo", "")
        warnings = []

        score_estrutura = 0
        score_estrutura += self._avaliar_cabecalhos(conteudo, warnings)
        score_estrutura += self._avaliar_paragrafos(conteudo, warnings)
        score_estrutura += self._avaliar_listas(conteudo, warnings)
        score_estrutura += self._avaliar_tabelas(conteudo, warnings)
        score_estrutura += self._avaliar_organizacao(conteudo, warnings)

        retorno_classificacao_estrutura_arquivo = self._classificacao_final_estrutura(score_estrutura)

        return {
            "score_estrutura": score_estrutura,
            "classificacao": retorno_classificacao_estrutura_arquivo,
            "warnings": warnings,
            "data_analise": datetime.now().isoformat()
        }
    
    def _avaliar_cabecalhos(self, conteudo, warnings):
        cabecalhos = re.findall(r"^#{1,6}\s", conteudo, re.MULTILINE)

        quantidade = len(cabecalhos)

        if quantidade == 0 :
            warnings.append("O documento não possui cabeçalhos.")
            return 0
        
        if quantidade <= 3:
            return 10
        if quantidade <= 10:
            return 20
        
        return 30
    
    def _avaliar_paragrafos (self, conteudo, warnings):
        paragrafos = [p for p in conteudo.split("\n\n") if p.strip()]
        quantidade = len(paragrafos)

        if quantidade <= 1:
            warnings.append("Documento não possui separação de parágrafos.")
            return 0
        
        if quantidade <=5:
            return 10
        
        return 20
    
    def _avaliar_listas(self, conteudo, warnings):
        listas = re.findall(r"^(\-|\*|\d+\.)", conteudo, re.MULTILINE)
        quantidade = len(listas)

        if quantidade == 0:
            warnings.append("Documento sem listas.")
            return 0

        if quantidade <= 5:
            return 10
        return 20
    
    def _avaliar_tabelas(self, conteudo, warnings):
        linhas_tabela = re.findall(r"\|.*\|", conteudo)
        quantidade = len(linhas_tabela)

        if quantidade == 0:
            warnings.append("Documento sem tabelas.")
            return 0

        if quantidade <= 5:
            return 10
        return 20
    
    def _avaliar_organizacao(self, conteudo, warnings):
        titulo = "#" in conteudo
        secao = "##" in conteudo
        subsecao = "###" in conteudo

        if (titulo and secao and subsecao):
            return 10
        
        warnings.append("Organização do arquivo limitada.")
        return 5
    
    def _classificacao_final_estrutura(self, score):
        if score >= 90:
            return "EXCELENTE"

        if score >= 70:
            return "BOM"

        if score >= 50:
            return "REGULAR"

        return "REPROVADO"
