
from datetime import datetime

class ServiceQualidadeArquivo:

    def analise_documento(self, documento):
        conteudo = documento.get("conteudo", "")
        warnings = []

        score_conteudo = self._avaliacao_documento(conteudo, warnings)

        retorno_classificacao_arquivo = self._classificacao_final(score_conteudo)

        return {
            "score_conteudo": score_conteudo,
            "classificacao": retorno_classificacao_arquivo,
            "warnings": warnings,
            "data_analise": datetime.now().isoformat()
        }
    
    def _avaliacao_documento (self, conteudo, warnings):

        quantidade_caracteres = len(conteudo.strip())

        if quantidade_caracteres == 0:
            warnings.append("Documento não possui conteúdo.")
            return 0
        
        if quantidade_caracteres <= 100:
            warnings.append("Conteúdo muito pequeno.")
            return 20
        
        if quantidade_caracteres <= 1000:
            return 40
        
        if quantidade_caracteres <= 5000:
            return 70   
        
        if quantidade_caracteres <= 15000:
            return 100
        warnings.append("Documento muito extenso, Recomenda-se fragmentação para RAG.")
        
        return 80
    
    def _classificacao_final(self, score):
        if score >= 90:

            return "EXCELENTE"

        if score >= 70:

            return "BOM"

        if score >= 50:

            return "REGULAR"

        return "REPROVADO"
