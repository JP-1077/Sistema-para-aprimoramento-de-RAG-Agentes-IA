# Documentação da Tabela de Metadados de Arquivos

## Visão Geral

Esta tabela é responsável por armazenar os metadados dos arquivos processados pelo sistema, incluindo informações de origem, rastreabilidade, controle de versão, status de processamento e localização dos artefatos transformados.

---

## Estrutura da Tabela

| Campo | Tipo de Informação | Descrição |
|---------|---------|---------|
| **nome_arquivo** | Texto | Nome original do arquivo enviado para processamento. |
| **caminho_arquivo** | Texto | Caminho completo do arquivo em sua localização de origem. |
| **tipo_arquivo** | Texto | Tipo ou extensão do arquivo, como PDF, DOCX ou XLSX. |
| **hash_arquivo** | Texto | Hash SHA-256 utilizado para garantir integridade e identificação única do arquivo. |
| **tamanho_arquivo** | Número | Tamanho do arquivo em bytes. |
| **data_criacao** | Data/Hora | Data e hora de criação do arquivo. |
| **data_processamento** | Data/Hora | Data e hora em que o arquivo foi processado pelo sistema. |
| **status_processamento** | Texto | Situação atual do processamento do arquivo. Exemplos: `Processado`, `Reprovado`. |
| **area responsavel** | Texto | Autor ou responsável pela criação do documento original. |
| **projeto** | Texto | Projeto, sistema ou contexto de origem do documento. |
| **score_qualidade** | Texto | Nota geral do score do arquivo |
| **caminho_markdown** | Texto | Caminho do arquivo convertido para formato Markdown (.md). |
| **caminho_json** | Texto | Caminho do arquivo convertido para formato JSON (.json). |
| **caminho_docx** | Texto | Caminho do arquivo convertido ou gerado em formato DOCX (.docx). |

---

## Descrição dos Status de Processamento

| Status | Descrição |
|----------|----------|
| **Processado** | O arquivo foi processado com sucesso e seus artefatos foram gerados. |
| **Reprovado** | O processamento falhou devido a erros de validação, leitura ou transformação do arquivo. |

---

## Objetivos da Tabela

A tabela tem como principais finalidades:

- Garantir rastreabilidade dos documentos processados.
- Controlar o ciclo de vida dos arquivos dentro da plataforma.
- Armazenar informações de auditoria e governança.
- Facilitar consultas por projeto, autor, idioma ou versão.
- Referenciar os artefatos gerados durante a etapa de transformação documental.

---

