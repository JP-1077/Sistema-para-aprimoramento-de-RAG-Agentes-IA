# ROADMAP DE DESENVOLVIMENTO
## Knowledge Quality Pipeline

---

# FASE 1 — Estruturação do Projeto

## Objetivo

Criar a fundação da aplicação, definir arquitetura, estrutura de pastas e ambiente de desenvolvimento.

## Entregas

### Estrutura do Projeto

```text
knowledge-quality-pipeline/

├── main.py

├── config/
│   └── settings.py

├── domain/
│   ├── document.py
│   └── quality_result.py

├── services/
│   ├── ingestion_service.py
│   ├── parser_service.py
│   ├── metadata_service.py
│   ├── quality_service.py
│   ├── duplicate_service.py
│   ├── transform_service.py
│   └── report_service.py

├── database/
│   ├── conexao_db.py
│   └── repository.py

├── storage/
│   ├── input/
│   ├── output/
│   ├── processed/
│   └── reports/

├── tests/

├── docs/

├── requirements.txt

└── README.md
```

### Configuração

Instalar dependências:

```bash
pip install pyodbc
pip install pandas
pip install pymupdf
pip install python-docx
pip install openpyxl
pip install python-dotenv
pip install pytest
pip install loguru
```

## Resultado

Projeto pronto para desenvolvimento.

---

# FASE 2 — Persistência e Banco de Dados

## Objetivo

Implementar comunicação com SQL Server.

## Entregas

### Classe de Conexão

```text
database/conexao_db.py
```

Responsabilidades:

- Ler variáveis de ambiente
- Abrir conexão SQL Server
- Retornar cursor
- Encerrar conexão

### Testes Automatizados

```text
tests/test_conexao_database.py
```

Validações:

- Instância da classe
- Abertura da conexão
- Criação do cursor
- Execução de SELECT 1

## Resultado

Conexão com banco validada.

---

# FASE 3 — Camada de Repositório

## Objetivo

Centralizar todas operações SQL.

## Entregas

### Repository

```text
database/repository.py
```

Métodos:

```python
save_document()

find_by_id()

find_by_hash()

update_document()
```

### Testes Automatizados

```text
tests/test_repository.py
```

Validações:

- Inserção
- Busca por ID
- Busca por Hash
- Atualização

## Resultado

Aplicação consegue persistir documentos.

---

# FASE 4 — Ingestão de Arquivos

## Objetivo

Identificar documentos para processamento.

## Entregas

### Ingestion Service

```text
services/ingestion_service.py
```

Responsabilidades:

- Ler pasta input
- Identificar arquivos válidos
- Ignorar arquivos inválidos

### Extensões Suportadas

```text
.pdf
.docx
.xlsx
```

## Fluxo

```text
storage/input
        ↓
ingestion_service
        ↓
Lista de documentos
```

## Resultado

Sistema localiza documentos automaticamente.

---

# FASE 5 — Parser de Documentos

## Objetivo

Extrair conteúdo dos documentos.

## Entregas

### Parser Service

```text
services/parser_service.py
```

### PDF

Extrair:

```text
Texto

Número de páginas

Metadados
```

### DOCX

Extrair:

```text
Parágrafos

Cabeçalhos

Tabelas
```

### XLSX

Extrair:

```text
Planilhas

Linhas

Colunas

Tabelas
```

## Resultado

Sistema converte documentos em texto processável.

---

# FASE 6 — Modelagem de Documento

## Objetivo

Representar documentos internamente.

## Entregas

### Domain

```text
domain/document.py
```

Atributos mínimos:

```python
id

file_name

file_type

file_hash

content

file_size

author

created_at
```

## Resultado

Objeto Document utilizado em toda aplicação.

---

# FASE 7 — Extração de Metadados

## Objetivo

Capturar informações auxiliares dos documentos.

## Entregas

### Metadata Service

```text
services/metadata_service.py
```

Extrair:

```text
Nome do Arquivo

Extensão

Hash

Tamanho

Autor

Idioma

Data Modificação
```

## Resultado

Documentos enriquecidos com metadados.

---

# FASE 8 — Persistência dos Documentos Processados

## Objetivo

Salvar conteúdo extraído.

## Fluxo

```text
Documento

↓

Parser

↓

Metadata

↓

Repository

↓

SQL Server
```

## Entregas

Gravar:

```text
Documento

Metadados

Hash

Status
```

## Resultado

Histórico de processamento registrado.

---

# FASE 9 — Análise de Qualidade

## Objetivo

Calcular o score de qualidade documental.

## Entregas

### Quality Service

```text
services/quality_service.py
```

### Critérios

#### Estrutura

```text
Títulos

Subtítulos

Seções
```

#### Conteúdo

```text
Quantidade de texto

Completude
```

#### Metadados

```text
Autor

Versão

Datas
```

#### Organização

```text
Tabelas

Listas

Padronização
```

## Saída

```json
{
    "quality_score": 92
}
```

## Resultado

Documentos recebem avaliação padronizada.

---

# FASE 10 — Detecção de Duplicidade

## Objetivo

