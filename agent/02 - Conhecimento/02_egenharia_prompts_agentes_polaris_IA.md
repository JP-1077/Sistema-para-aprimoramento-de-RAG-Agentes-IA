# Engenharia de Prompt - Polaris AI

## 1. Visão Geral

Este documento define os padrões, métodos e boas práticas adotados pela Polaris AI para criação, revisão, evolução e governança de System Prompts utilizados em agentes de Inteligência Artificial.

O objetivo é garantir que os agentes possuam instruções consistentes, claras, escaláveis e alinhadas aos objetivos de negócio, reduzindo ambiguidades, aumentando a precisão e promovendo comportamentos previsíveis.

Este framework deve ser utilizado como referência para todos os agentes desenvolvidos pela área.

---

# 2. Objetivos

Este framework possui os seguintes objetivos:

- Padronizar a construção de System Prompts.
- Melhorar a qualidade dos agentes.
- Reduzir ambiguidades e conflitos de instruções.
- Aumentar a previsibilidade dos comportamentos.
- Facilitar manutenção e evolução dos prompts.
- Aplicar boas práticas de Prompt Engineering.
- Melhorar governança dos agentes.
- Melhorar precisão das respostas.

---

# 3. Fundamentos de Engenharia de Prompt

Um System Prompt possui como função definir:

- Quem o agente é.
- Por que ele existe.
- O que ele faz.
- Como ele deve pensar.
- Como ele deve responder.
- O que ele pode ou não fazer.

Um bom System Prompt deve ser:

- Claro.
- Objetivo.
- Estruturado.
- Testável.
- Escalável.
- Livre de ambiguidades.

---

# 4. Estrutura Oficial Polaris AI

Todo System Prompt deve seguir a seguinte estrutura.

## 1. PERSONA

Define quem é o agente.

Objetivo:

Estabelecer identidade, especialidade e perfil profissional.

Exemplo:

```text
Você é um especialista em Agent Experience (AX) e desenvolvimento de agentes de IA.
```

Boas práticas:

- Ser específico.
- Definir especialização.
- Evitar personas genéricas.

---

## 2. CONTEXTO

Define o ambiente onde o agente está inserido.

Objetivo:

Permitir que o agente compreenda o cenário em que opera.

Exemplo:

```text
Você atua na área Polaris AI apoiando equipes no desenvolvimento e evolução de agentes de Inteligência Artificial.
```

Boas práticas:

- Explicar o contexto organizacional.
- Explicar quem utiliza o agente.
- Evitar contextualizações excessivas.

---

## 3. OBJETIVO

Define o propósito de existência do agente.

Objetivo:

Explicar claramente qual problema o agente deve resolver.

Exemplo:

```text
Seu objetivo é auxiliar usuários no desenvolvimento e melhoria de agentes de IA.
```

Boas práticas:

- Foco no valor gerado.
- Definir claramente o problema que o agente resolve.

---

## 4. INSTRUÇÕES

Define capacidades, funcionalidades e responsabilidades do agente.

Objetivo:

Explicar o que o agente pode fazer.

Exemplos:

- Revisar prompts.
- Avaliar agentes.
- Avaliar fontes de conhecimento.
- Gerar documentação.
- Orientar usuários.

Boas práticas:

- Organizar por funcionalidades.
- Utilizar descrições objetivas.
- Evitar redundâncias.

---

## 5. PIPELINE DE RACIOCÍNIO

Define a sequência lógica de pensamento utilizada pelo agente.

Objetivo:

Aumentar qualidade e consistência das respostas.

Fluxo recomendado:

```text
1. Classificar solicitação.
2. Identificar intenção.
3. Analisar contexto.
4. Aplicar conhecimento especializado.
5. Construir solução.
6. Validar qualidade.
7. Gerar resposta.
```

Boas práticas:

- Utilizar poucas etapas.
- Focar em lógica e análise.
- Evitar pipelines excessivamente complexos.

---

## 6. LIMITAÇÕES E GUARDRAILS

Define limites operacionais.

Objetivo:

Reduzir riscos e comportamentos inadequados.

Exemplos:

```text
Não inventar informações.

Não tomar decisões pelo usuário.

Não aprovar soluções para produção.
```

Boas práticas:

- Criar poucas regras.
- Ser direto.
- Definir claramente limites.

---

## 7. CRITÉRIOS DE SAÍDA

Define como as respostas devem ser apresentadas.

Objetivo:

Garantir consistência visual e estrutural.

Exemplo:

```text
- Linguagem clara.
- Estrutura organizada.
- Recomendações práticas.
- Próximos passos.
```

Boas práticas:

- Priorizar legibilidade.
- Utilizar listas e seções.
- Adaptar profundidade ao contexto.

---

## 8. CRITÉRIOS DE PRECISÃO

Define critérios mínimos de qualidade.

Objetivo:

Reduzir alucinações e inconsistências.

Exemplo:

```text
Não presumir informações.

Justificar recomendações.

Explicitar limitações quando houver falta de contexto.
```

Boas práticas:

- Separar fatos de recomendações.
- Evitar inferências não fundamentadas.
- Validar consistência antes de responder.

---

# 5. Framework de Construção de Prompts

Utilize o seguinte processo para construção de novos prompts.

## Etapa 1 - Definir Problema

Perguntas:

- Qual problema será resolvido?
- Quem utilizará o agente?
- Qual valor será entregue?

---

## Etapa 2 - Definir Persona

Perguntas:

- Quem é o agente?
- Qual especialidade possui?
- Como deve se comportar?

---

## Etapa 3 - Definir Objetivo

Perguntas:

- Qual resultado esperado?
- O que o agente deve ajudar a resolver?

---

## Etapa 4 - Definir Funcionalidades

Perguntas:

- Quais tarefas executará?
- Quais análises realizará?
- Quais tipos de solicitações atenderá?

---

## Etapa 5 - Definir Limitações

Perguntas:

- O que o agente não deve fazer?
- Quais riscos precisam ser controlados?

---

## Etapa 6 - Definir Formato das Respostas

Perguntas:

- Como o agente deve responder?
- Qual nível de profundidade utilizar?

---

## Etapa 7 - Revisar

Validar:

- Clareza.
- Consistência.
- Redundância.
- Escopo.
- Governança.

---

# 6. Anti-patterns de Prompt Engineering

Evite os problemas abaixo.

## Persona Genérica

Ruim:

```text
Você é um assistente de IA.
```

Bom:

```text
Você é um especialista em desenvolvimento de agentes de IA.
```

---

## Objetivo Ambíguo

Ruim:

```text
Ajude o usuário.
```

Bom:

```text
Auxilie usuários no desenvolvimento e avaliação de agentes.
```

---

## Instruções Excessivamente Longas

Ruim:

- Múltiplas repetições.
- Redundâncias.
- Explicações excessivas.

Bom:

- Direto.
- Organizado.
- Objetivo.

---

## Funcionalidades Misturadas

Ruim:

```text
Misturar responsabilidades distintas na mesma funcionalidade.
```

Bom:

```text
Separar claramente cada capacidade do agente.
```

---

## Ausência de Guardrails

Ruim:

```text
Agente sem limitações.
```

Bom:

```text
Agente com limites operacionais claros.
```

---

# 7. Framework de Revisão de Prompts

Durante revisões utilize os critérios abaixo.

## Clareza

Avalia se as instruções são compreensíveis.

---

## Consistência

Avalia conflitos e contradições.

---

## Escopo

Avalia se as responsabilidades estão bem definidas.

---

## Governança

Avalia controle e limitações.

---

## Precisão

Avalia redução de ambiguidades.

---

## Qualidade Geral

Avalia maturidade do prompt.

---

# 8. Modelo de Diagnóstico de Prompt

Utilize o modelo abaixo.

## Diagnóstico

```text
Status:
OK | Atenção | Ruim
```

---

## Checklist

```text
[ ] Persona definida
[ ] Contexto definido
[ ] Objetivo definido
[ ] Funcionalidades definidas
[ ] Pipeline definido
[ ] Guardrails definidos
[ ] Critérios de saída definidos
[ ] Critérios de precisão definidos
```

---

## Problemas Identificados

Liste os principais riscos ou oportunidades de melhoria.

---

## Recomendações

Liste os ajustes sugeridos.

---

## Prompt Reestruturado

Apresente a versão recomendada.

---

# 9. Checklist de Qualidade

Antes da publicação valide:

- [ ] Persona clara.
- [ ] Contexto suficiente.
- [ ] Objetivo definido.
- [ ] Funcionalidades bem delimitadas.
- [ ] Pipeline consistente.
- [ ] Guardrails definidos.
- [ ] Critérios de saída definidos.
- [ ] Critérios de precisão definidos.
- [ ] Sem ambiguidades.
- [ ] Sem conflitos.
- [ ] Escopo controlado.

---

# 10. Considerações Finais

Um bom agente é consequência direta de um bom System Prompt.

O System Prompt deve ser tratado como um ativo estratégico da solução, recebendo o mesmo nível de planejamento, revisão, documentação e governança aplicado ao desenvolvimento de sistemas e aplicações tradicionais.

Todo prompt desenvolvido pela Polaris AI deve seguir este framework como padrão oficial de engenharia de prompts.