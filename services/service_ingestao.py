import os
from pathlib import Path


extensoes_validas = [".docx", ".pdf", ".md", ".xlsx"]

class IngestaoArquivos:
    def __init__(self,caminho_input):
        self.caminho_input = Path(caminho_input)

    def validacao_arquivos(self, arquivo: Path) -> bool:
        return arquivo.suffix.lower() in extensoes_validas
    
    def lista_arquivos_validos(self) -> list:
        arquivos_validos = []

        for arquivo in self.caminho_input.iterdir():
            if (arquivo.is_file() and self.validacao_arquivos(arquivo)):

                arquivos_validos.append(
                {
                    "nome_arquivo": arquivo.name,
                    "tipo_arquivo": arquivo.suffix.lower(),
                    "caminho": str(arquivo)
                }
                )

        return arquivos_validos
    
    def contagem_arquivos(self) -> int:

        return len(self.lista_arquivos_validos())