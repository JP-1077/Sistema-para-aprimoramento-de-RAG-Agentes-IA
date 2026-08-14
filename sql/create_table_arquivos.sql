CREATE TABLE [Data_process].tb_polaris_IA_processamento_rag
(
    id BIGINT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    nome_arquivo         NVARCHAR(500) NULL,
    caminho_arquivo_input     NVARCHAR(500) NULL,
    tipo_arquivo         NVARCHAR(500) NULL,
    hash_arquivo         NVARCHAR(500) NULL,
    tamanho_arquivo      NVARCHAR(500) NULL,
    data_criacao         DATETIME NULL,
    data_processamento   DATETIME NULL,
    status_processamento NVARCHAR(500) NULL,
    area_responsavel     NVARCHAR(500) NULL,
    projeto              NVARCHAR(500) NULL,
    score_qualidade      NVARCHAR(500) NULL,
	caminho_arquivo_output NVARCHAR(500) NULL
);



SELECT * FROM [Data_process].tb_polaris_IA_processamento_rag