import json
from pathlib import Path
from datetime import datetime

class ReportService:

    def __init__(self):
        self.report_path = Path(r"C:\projetos\pipeline-qualidade-knowledge\data\reports")

        self.report_path.mkdir(parents=True, exist_ok=True)

    
    def relatorio(self, documento, resultado_analise):

        nome_arquivo = Path(documento["nome_arquivo"]).stem

        caminho_relatorio = self.report_path / f"{nome_arquivo}_report.json" 
        relatorio = {
            "nome_arquivo": documento["nome_arquivo"],

            "tipo_arquivo": documento["tipo_arquivo"],

            "score_final": resultado_analise["score_final"],

            "score_qualidade": resultado_analise["score_qualidade"],

            "score_estrutura": resultado_analise["score_estrutura"],

            "classificacao": resultado_analise["classificacao"],

            "aprovado": resultado_analise["aprovado"],

            "warnings": resultado_analise["warnings"],

            "data_analise": datetime.now().isoformat()
        }

        with open(caminho_relatorio, "w", encoding="utf-8") as arquivo:
            json.dump(relatorio, arquivo, indent=4, ensure_ascii=False)

        return str(caminho_relatorio)
