from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class ProcessamentoDocumentos(BaseModel):

    id: int = None,
    nome_arquivo: str = "",
    caminho_arquivo: str = "",
    tipo_arquivo: str = "",
    hash_arquivo: str = "",
    tamanho_arquivo: str = "",
    data_criacao: datetime = None,
    data_processamento: datetime = None,
    status_processamento: str = "",
    area_responsavel: str = "",
    projeto: str = "",
    score_qualidade: str = "",
    caminho_arquivo_output: str = ""


