CREATE TABLE [Data_Adhoc].TB_LOGS_PROCS_AI 
(
	
	id_process INT IDENTITY(1,1) PRIMARY KEY,
	id_execucao UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
	nome_processo NVARCHAR(500) NOT NULL,
	tipo_processo NVARCHAR(500) NOT NULL,
	pipeline_processo NVARCHAR(500) NULL,
	descricao_processo NVARCHAR(MAX) NULL,
	nome_agente_relacionado NVARCHAR(500) NOT NULL,
	data_inicio_processo DATETIME NOT NULL DEFAULT GETDATE(),
	data_fim_processo DATETIME NULL,
	tempo_total_execucao_ms INT NULL,
	status NVARCHAR(50) NOT NULL,
	mensagem_sucesso NVARCHAR(MAX) NULL,
	mensagem_erro NVARCHAR (MAX) NULL,
	owner_processo NVARCHAR(200) NULL,
	versao NVARCHAR (50) NULL,
	data_criacao_log DATETIME NOT NULL DEFAULT GETDATE()
);
