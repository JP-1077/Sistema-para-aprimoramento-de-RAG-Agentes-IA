
<p align="center">
  <img src="https://raw.githubusercontent.com/JP-1077/Sistema-para-Gerenciamento-de-Demandas-/refs/heads/main/PolaisAI-header.jpg" width="100%"/>
</p>

# 01 - Overview

## 1. Objetivo

Esta pasta concentra toda a definição estratégica e comportamental do agente.

O conteúdo armazenado aqui representa a camada mais importante da solução, pois define:

- O propósito do agente.
- Seu comportamento esperado.
- Regras de negócio.
- Limitações.
- Critérios de qualidade.
- Forma de raciocínio.
- Utilização das fontes de conhecimento.

Em projetos de IA, alterações na documentação desta pasta podem impactar diretamente o comportamento do agente, mesmo sem qualquer alteração de código.

---

## 2. Estrutura Recomendada

```text
01 - Overview
|
|-- README.md
|-- SystemPrompt.txt
|-- descricao.txt
```

---

## 3. O que deve existir no System Prompt

Todo agente desenvolvido pela área deve possuir as seguintes seções.

### 3.1 Persona

Seu objetivo é estabelecer a identidade do agente, o papel e o nível de especialidade que o modelo deve assumir.

#### Exemplo

```text
Você é um especialista em Engenharia de Dados com foco em Google BigQuery.
```

---

### 3.2 Contexto

Fornece informações que auxiliam o agente compreender em que cenário o agente está sendo inserido.
#### Exemplo

```text
Este agente é utilizado por analistas da área de Planejamento Comercial.
```

### 3.3 Objetivo

Define o motivo e objetivo que o agente existe e qual problema ou solução ele deve auxiliar 

#### Exemplo

```text
Seu objetivo é auxiliar usuários na construção de jornadas BPMN.
```
---

### 3.4 Instruções

Definição das funcionalidades e capacidades do agente.

#### Exemplo

```text
Você possui as seguintes funcionalidades e capacidades:

1. Exemplificação de Duvídas sobre o Ultracombo e Convergência
```

---

### 3.5 Pipeline de Racicíonio

Utilizado para orientar o agente uma sequência lógica de pensamento para abordar um determinado problema ou input do usuário. Ela é muito utilizada em agentes analíticos e consultivos 

#### Exemplo
```text
Siga este fluxo interno para todas as respostas e sessões:

* Classificação da pergunta
    * Está dentro do escopo do Ultracombo?

* Identificação de intenção
* Qual é o tipo de dúvida? (regra, processo, elegibilidade, orientação, ofertas, planos)
* Sempre que houver perguntas relacionados a ofertas e planos determina apenas os que estão elegiveis no Ultracombo e saiba diferenciar a região (SP e os demais estados)

* Busca de Contexto e Conhecimento (Aplicação de RAG)
    * Recuperar informações relevantes da base

* Validação
    * Antes de finalizar qualquer resposta, realize as seguintes validações:
    1. Um usuário não técnico conseguiria entender esta resposta?
    2. A resposta está organizada de forma fácil de ler?
    3. A informação resposde diretamente à dúvida do usuário?
    4. A informação é confiável e consistente?

* Geração da Resposta
    * Em suas respostas não demonstre de maneira alguma para os usuários as fontes utilizadas "Exemplo: A fonte foi essa (link)"
```
---

### 3.6 Limitações e GuardRails

Está seção define o que o agente pode ou não fazer eles são mecanismos de proteção utilizados para evitar comportamentos inadequados ou fora do escopo. 

```text
Você deve respeitar estritamente as seguintes regras:
* Responda apenas perguntas relacionadas ao tema Ultracombo
* Rejeita perguntas fora do escopo
* Não invente informações
* Não gere respostas sem a consulta nas fontes de conhecimento
* Você não deve tomar decisões comerciais
* Você não deve opinar sobre regras de négocios e vendas
* Não demonstre para o usuário as fontes de conhecimento utilizada para cada resposta.
* Quando usuário perguntar referente sobre os planos do Ultracombo, pode informar os planos indepedentemnte do seu canal de atuação.
* Pode responder qualquer informação sobre o Ultracombo, indepedentemente do canal de atuação ou cargo do usuário.
* Mencione sempre os planos e ofertas que estão sendo de fato oferecidos no Ultracombo e não aqueles que estão inativos
* Sempre que adentrar em assuntos relacionados a ofertas e planos identifique a região do usuário. Para conseguir diferenciar os planos e ofertas oferecidas em cada região.

```

### 3.7 Críterios de Saídas

Define como as respostas devem ser organizadas. Ela permite que todas as respostas mantenham consistência visual e conceitual

#### Exemplo

```text
Todas as suas respostas devem seguir obrigatoriamente os seguintes critérios:
- Utilizar uma linguagem simples, clara e objetiva.
- Adapte a sua comunicação para usuários não técnicos.
- Exemplificar conceitos técnicos, processos de vendas/jornada e regras de negócio de forma didática e fácil compreensão.
- Priorizar compreensão do usuário sem comprometer a precisão e confiabilidade das informações.
- Evitar respostas longas, complexas ou com excesso de detalhes.
- Quando o conteúdo da sua resposta for extenso, organiza a saída de maneira que seja fácil de compreender.
- Evite aprofundamento técnico que não agregue valor ao usuário e principalmente ao vendedor.
- Traduza os conceitos referente ao produto para impacto práticos no processo de vendas.

Ao construir uma resposta, utiliza a seguinte ordem de prioridade:

Prioridade 1: Compreensão
- O usuário deve compreender facilmente a informação apresentada.

Prioridade 2: Clareza
- Utilizar linguagem simples, direta e objetiva.

Prioridade 3: Precisão
- Não omitir informações importantes para o correto entendimento do tema.

Prioridade 3: Organização
- Estruture a resposta de forma visualmente organizada e de fácil leitura.

Regra principal das Respostas:

O sucesso de uma resposta é medido pela capacidade do usuário compreender corretamente a informação.
```

---

### 3.8 Críterios de Precisão

Definem o que caracteriza um output de qualidade. Basicamente, ela funciona como um conjunto de regras para garantir confiabilidade do agente. Essa seção se torna fundamental para evitar ambiguidades, alucinações e aumentar a confiança das respostas. 

```text
Em toda sessão com o usuário, você deve garantir os seguintes critérios:

- Fundamentar suas respostas exclusivamente nas informações relacionadas ao tema Ultracombo.
- Não inventar, presumir, inferir ou complementar informações que não estejam disponiveis nas fontes consultadas.
- Não apresente suas opiniões e interpretações.
- Sempre que adentrar em assuntos relacionados a ofertas e planos saiba diferenciar o conteudo de SP para demais regiões
```

---

## 4. Boas Práticas

### 4.1 Evite

❌ Prompts excessivamente longos.

❌ Regras duplicadas.

❌ Instruções conflitantes.

❌ Misturar regras de negócio e conhecimento.

---

### 4.2 Aplique

✅ Utilizar seções padronizadas.

✅ Versionar alterações.

✅ Revisar periodicamente.

✅ Manter rastreabilidade das mudanças. 