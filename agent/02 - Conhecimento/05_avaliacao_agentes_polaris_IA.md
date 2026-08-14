# Framework Avaliação de Agentes

## 1. Visão Geral

Este documento define o framework oficial da Polaris AI para avaliação, validação e evolução de agentes de Inteligência Artificial.

O objetivo deste framework é fornecer um método padronizado para medir a qualidade, comportamento, precisão, experiência do usuário e aderência aos objetivos de negócio dos agentes desenvolvidos pela área.

A avaliação de agentes deve ser tratada como uma disciplina contínua e obrigatória durante todo o ciclo de vida da solução.

Um agente não deve ser considerado pronto apenas porque responde perguntas.

Um agente de qualidade deve:

- Resolver o problema proposto.
- Produzir respostas confiáveis.
- Demonstrar raciocínio consistente.
- Utilizar corretamente as fontes de conhecimento.
- Gerar valor para os usuários.
- Manter comportamento previsível.

---

# 2. Objetivos da Avaliação

A avaliação possui os seguintes objetivos:

- Validar a qualidade do agente.
- Medir precisão e acurácia.
- Identificar falhas e limitações.
- Detectar alucinações.
- Avaliar aderência ao objetivo.
- Avaliar experiência do usuário.
- Avaliar comportamento do agente.
- Identificar oportunidades de melhoria.
- Apoiar evolução contínua da solução.

---

# 3. Quando Avaliar um Agente

A avaliação deve ocorrer nas seguintes situações:

## Durante o Desenvolvimento

Antes da publicação.

Objetivo:

```text
Identificar problemas precocemente.
```

---

## Após Alterações no Prompt

Objetivo:

```text
Validar se o comportamento foi impactado.
```

---

## Após Atualização das Fontes de Conhecimento

Objetivo:

```text
Garantir consistência das respostas.
```

---

## Antes da Publicação

Objetivo:

```text
Homologação da solução.
```

---

## Em Produção

Objetivo:

```text
Monitorar qualidade contínua.
```

---

# 4. Dimensões de Avaliação

Todo agente deve ser avaliado através das dimensões abaixo.

---

## Funcionalidade

Avalia se o agente executa corretamente sua função.

Perguntas:

```text
O agente resolve o problema proposto?

O agente atende os requisitos definidos?
```

---

## Qualidade

Avalia a qualidade geral das respostas.

Perguntas:

```text
As respostas são completas?

As respostas são úteis?

As respostas são compreensíveis?
```

---

## Precisão

Avalia a correção das respostas.

Perguntas:

```text
A resposta está correta?

A resposta possui erros?
```

---

## Consistência

Avalia estabilidade do comportamento.

Perguntas:

```text
O agente responde de forma consistente?

O comportamento varia indevidamente?
```

---

## Governança

Avalia aderência às regras definidas.

Perguntas:

```text
O agente respeita limitações?

O agente segue regras de negócio?
```

---

## Agent Experience (AX)

Avalia a experiência proporcionada ao usuário.

Perguntas:

```text
O agente gera valor?

O agente auxilia na solução do problema?
```

---

# 5. Tipos de Testes

## Teste Funcional

Objetivo:

Validar funcionalidades.

Exemplos:

- Perguntas frequentes.
- Fluxos de negócio.
- Casos de uso principais.

---

## Teste de Precisão

Objetivo:

Validar correção das respostas.

Exemplos:

- Regras de negócio.
- Procedimentos.
- Conhecimentos documentados.

---

## Teste de RAG

Objetivo:

Validar recuperação de conhecimento.

Exemplos:

- Perguntas baseadas em documentos.
- Perguntas sobre FAQs.
- Recuperação de regras específicas.

---

## Teste de Comportamento

Objetivo:

Validar comportamento esperado.

Exemplos:

- Seguir persona.
- Respeitar guardrails.
- Aplicar instruções.

---

## Teste de AX

Objetivo:

Validar experiência do usuário.

Exemplos:

- Clareza.
- Utilidade.
- Contextualização.
- Valor entregue.

---

# 6. Relatório Padrão de Avaliação

Toda avaliação de agente deve seguir obrigatoriamente o modelo abaixo.

---

# Relatório de Avaliação de Agente

## 1. Identificação do Teste

Informações gerais da execução.

Campos:

```text
ID do Teste:

Data:

Nome do Agente:

Versão:

Responsável:

Avaliador:
```

---

## 2. Objetivo do Teste

Descreva o propósito da avaliação.

Exemplo:

```text
Validar a qualidade das respostas relacionadas à avaliação de prompts.
```

---

## 3. Entradas (Input)

Descreva exatamente o que foi enviado ao agente.

Exemplo:

```text
"Revise o System Prompt abaixo e identifique melhorias."
```

---

## 4. Saídas do Agente (Output)

Registrar exatamente a resposta produzida pelo agente.

Objetivo:

Permitir rastreabilidade da avaliação.

---

## 5. Análise Funcional

Avaliar se a funcionalidade foi executada corretamente.

Critérios:

- Atendeu ao objetivo.
- Executou a tarefa esperada.
- Seguiu os requisitos.

Classificação:

```text
Excelente
Bom
Regular
Ruim
```

---

## 6. Análise de Qualidade

Avaliar qualidade geral da resposta.

Critérios:

- Clareza.
- Organização.
- Utilidade.
- Completude.

Perguntas:

```text
A resposta foi útil?

A resposta estava bem estruturada?
```

Classificação:

```text
Excelente
Bom
Regular
Ruim
```

---

## 7. Análise de Precisão e Acurácia

Avaliar correção das informações.

Critérios:

- Precisão técnica.
- Ausência de erros.
- Ausência de alucinações.
- Aderência às fontes.

Perguntas:

```text
A resposta está correta?

Houve invenção de informações?
```

Classificação:

```text
Excelente
Bom
Regular
Ruim
```

---

## 8. Análise de Raciocínio do Agente

Avaliar a lógica utilizada para chegar à resposta.

Critérios:

- Coerência.
- Sequência lógica.
- Capacidade analítica.
- Justificativas apresentadas.

Perguntas:

```text
O raciocínio foi consistente?

As recomendações foram justificadas?
```

Classificação:

```text
Excelente
Bom
Regular
Ruim
```

---

## 9. Problemas Identificados

Documentar problemas observados.

Exemplos:

```text
Resposta incompleta.

Informação inconsistente.

Recuperação incorreta de conhecimento.

Falta de contexto.
```

---

## 10. Avaliação Geral e Conclusão

Resumo executivo da avaliação.

Modelo:

```text
Resumo Geral:

Pontos Fortes:

Pontos de Melhoria:

Riscos Identificados:

Conclusão:
```

---

# 7. Escala de Avaliação

Utilize a escala abaixo.

| Nota | Classificação |
|--------|--------|
| 5 | Excelente |
| 4 | Bom |
| 3 | Regular |
| 2 | Ruim |
| 1 | Crítico |

---

# 8. Critérios de Aprovação

Um agente pode ser considerado apto para publicação quando:

- Não apresenta erros críticos.
- Não apresenta alucinações relevantes.
- Atende os objetivos propostos.
- Possui comportamento consistente.
- Possui precisão aceitável.
- Apresenta experiência satisfatória.

---

# 9. Checklist Final de Avaliação

Antes da aprovação valide:

- [ ] Funcionalidade validada.
- [ ] Precisão validada.
- [ ] Qualidade validada.
- [ ] Comportamento validado.
- [ ] AX validado.
- [ ] RAG validado.
- [ ] Sem erros críticos.
- [ ] Sem alucinações relevantes.
- [ ] Relatório concluído.
- [ ] Recomendações registradas.

---
