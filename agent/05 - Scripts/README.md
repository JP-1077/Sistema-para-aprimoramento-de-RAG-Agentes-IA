<p align="center">
  <img src="https://raw.githubusercontent.com/JP-1077/Sistema-para-Gerenciamento-de-Demandas-/refs/heads/main/PolaisAI-header.jpg" width="100%"/>
</p>

# 05 - Scripts

## 1. Objetivo

Esta pasta concentra todos os artefatos técnicos utilizados pelo agente.

Os scripts são responsáveis por implementar funcionalidades complementares, integrações, processamento de dados, automações, ingestão de conhecimento e mecanismos de observabilidade.

Toda implementação técnica da solução deve estar devidamente documentada e organizada nesta pasta.

---


## 2. Documentação Obrigatória

Todo script deve possuir documentação mínima.

---

### Nome

Nome do arquivo.

---

### Objetivo

Descrição funcional.

### Exemplo

```text
Realiza ingestão de documentos PDF para a base vetorial.
```

---

### Entradas

Dados recebidos.

### Exemplo

```text
PDF
DOCX
TXT
```

---

### Saídas

Resultado produzido.

### Exemplo

```text
Chunks vetorizados
```

---

### Dependências

Bibliotecas e serviços envolvidos.

### Exemplo

```text
LangChain

FAISS

Azure OpenAI
```

---

### Logs

Eventos registrados pelo script.

---

### Tratamento de Erros

Erros previstos e comportamento esperado.

---

## 3. Boas Práticas

✅ Um script deve ter apenas uma responsabilidade principal.

✅ Todas as entradas devem ser validadas.

✅ Logs devem ser produzidos para operações críticas.

✅ Tratamentos de erro devem ser explícitos.

✅ Evitar duplicação de código.

✅ Documentar dependências externas.

✅ Seguir padrões de Clean Code.

---

## 4. O que NÃO deve existir nesta pasta

❌ Relatórios de testes.

❌ Documentação funcional.

❌ Prompts.

❌ Fontes de conhecimento.
