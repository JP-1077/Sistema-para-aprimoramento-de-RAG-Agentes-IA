from datetime import datetime

class AnalyticsService:

    APROVACAO = 70

    def analise (self, resultado_qualidade, resultado_estrutura):

        score_qualidade = (resultado_qualidade ["score_conteudo"])

        score_estrutura = (resultado_estrutura ["score_estrutura"])

        nota_final = round((score_qualidade * 0.7 + score_estrutura * 0.3), 2)
        
        classificacao = (self._classificacao_final(nota_final))
        
        aprovado = (nota_final >= self.APROVACAO)

        warnings = []

        warnings.extend(resultado_qualidade.get("warnings", []))

        warnings.extend(resultado_estrutura.get("warnings", []))
        
        return {
            "score_final": nota_final,

            "score_qualidade": score_qualidade,

            "score_estrutura": score_estrutura,

            "classificacao": classificacao,

            "aprovado": aprovado,

            "warnings":warnings,

            "data_analise": datetime.now().isoformat()
        }
        
    def _classificacao_final(self, score):

        if score >= 90:
            return "Excelente"
        if score >= 70:
            return "Bom"
        if score >= 50:
            return "Regular"
        
        return "Reprovado"