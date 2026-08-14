<p align="center">
  <img src="https://raw.githubusercontent.com/JP-1077/Sistema-para-Gerenciamento-de-Demandas-/refs/heads/main/PolaisAI-header.jpg" width="100%"/>
</p>


# 03 - Flows

## Objetivo

Esta pasta concentra toda a documentação referente aos fluxos automatizados utilizados pelo agente.

Os fluxos representam processos automatizados executados por plataformas externas ou serviços integrados, responsáveis por complementar as capacidades do agente além do processamento realizado pelo modelo de linguagem.

Esses fluxos podem ser utilizados para:

- Consultar sistemas externos
- Processar documentos
- Atualizar bases de conhecimento
- Executar automações
- Orquestrar processos
- Integrar APIs corporativas
- Enviar notificações
- Executar tarefas programadas

---

# O que é um Flow?

Um Flow é qualquer processo automatizado executado fora do modelo de IA.

Diferentemente do Prompt ou do RAG, o Flow realiza ações operacionais em sistemas e serviços externos.

---

# Exemplos de Flows

## Power Automate

```text
Receber nova documentação

↓

Validar documento

↓

Atualizar SharePoint

↓

Enviar notificação Teams
```

---

## Azure Function

```text
Receber chamada do agente

↓

Executar processamento

↓

Consultar banco de dados

↓

Retornar resultado
```

---

## N8N

```text
Receber arquivo

↓

Processar texto

↓

Gerar embeddings

↓

Atualizar base vetorial
```

---

# Estrutura Recomendada

```text
03 - Flows
|
|-- README.md
|
|-- Atualizacao_Base_Conhecimento.json
|
|-- Atualizacao_Base_COnhecimento.img
```

---

## Estrutura de Documentação de um Flow

Todo Flow documentado nesta pasta deve possuir as seguintes informações.

---

## Nome do Flow

Nome do processo automatizado.

### Exemplo

```text
Atualização Automática da Base de Conhecimento
```

---

## Objetivo

Descrever a finalidade do fluxo.

### Exemplo

```text
Atualizar automaticamente a base de conhecimento do agente sempre que um novo documento for publicado no SharePoint.
```

---

## Plataforma Utilizada

Informar tecnologia responsável pela automação.

### Exemplos

```text
Power Automate

Azure Logic Apps

N8N

Azure Functions

Python
```

---

## Gatilho (Trigger)

Evento responsável por iniciar o fluxo.

### Exemplos

```text
Novo arquivo publicado

Execução agendada

Chamada da API

Ação do usuário
```

---

## Entradas

Informar todos os dados recebidos pelo fluxo.

### Exemplo

```text
PDF

DOCX

Metadados do documento
```

---

## Processamento

Descrever as etapas executadas.

### Exemplo

```text
1. Receber documento.
2. Validar formato.
3. Extrair conteúdo.
4. Gerar embeddings.
5. Atualizar índice vetorial.
```

---

## Saídas

Resultado produzido pelo fluxo.

### Exemplo

```text
Base vetorial atualizada.
```

---

## Sistemas Integrados

Listar sistemas envolvidos na automação.

### Exemplo

```text
SharePoint

Azure Blob Storage

OpenAI

SQL Server
```

---

## Dependências

Dependências técnicas necessárias.

### Exemplo

```text
API de Documentos

Banco SQL

Serviço de Embeddings
```

---

## Tratamento de Falhas

Descrever comportamento em caso de erro.

### Exemplo

```text
Falha na leitura do documento.

→ Registrar log.
→ Notificar responsável.
→ Não atualizar a base.
```

---

## Inventário de Flows

Manter sempre atualizado.

| Flow | Plataforma | Objetivo | Status |
|--------|--------|--------|--------|
| Atualização de Conhecimento | Power Automate | Atualizar RAG | Produção |
| Consulta Comercial | Azure Function | Consultar dados | Produção |
| Processamento FAQ | Python | Gerar embeddings | Homologação |

---

## Fluxos Obrigatórios para Governança

Sempre que possível documentar:

## Atualização de Conhecimento

Fluxos responsáveis por ingestão de documentos.

---

## Integrações Externas

Consultas em APIs ou bancos.

---

## Monitoramento

Fluxos de auditoria e observabilidade.

---

## Notificações

Fluxos de comunicação com usuários ou administradores.

---

## Boas Práticas

✅ Documentar todas as integrações.

✅ Registrar dependências externas.

✅ Versionar alterações dos fluxos.

✅ Manter diagramas atualizados.

✅ Registrar responsáveis técnicos.

✅ Documentar gatilhos e saídas.

✅ Possuir procedimentos de recuperação de falhas.

---

## O que NÃO deve existir nesta pasta

❌ Prompt do agente.

❌ Fontes de conhecimento.

❌ Relatórios de testes.

❌ Scripts utilitários.

❌ Regras de negócio do agente.

Esses conteúdos devem permanecer em suas respectivas pastas.