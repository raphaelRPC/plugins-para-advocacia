# Modelo da habilidade própria do escritório

Use no modo rotina nova. Copie o bloco para `escritorio/04-base/habilidades-do-escritorio/<nome>/SKILL.md`. O `<nome>` é o mesmo da pasta e do campo `name`, só com letras minúsculas sem acento, números e hífen (ex.: `ligacao-de-boas-vindas`). O script `scripts/empacotar_habilidade.py` confere tudo antes de gerar o .zip.

```markdown
---
name: [NOME-DA-PASTA]
description: >
  [O QUE FAZ, EM UMA OU DUAS FRASES]. Use quando [FRASES QUE A EQUIPE DIRIA, ENTRE ASPAS].
  Não use para [O QUE NÃO É] (use [OUTRA HABILIDADE]).
---

# [TÍTULO]

> [RESUMO DE UMA LINHA: O QUE A ROTINA RESOLVE]

Rotina do escritório escrita em `04-base/comum/rotinas-do-escritorio.md`. Regras do plugin motor-experiencia, se instalado: `docs/regras.md` dele.

[CENA CONCRETA DE 2 A 4 LINHAS: QUANDO A ROTINA FALHAVA ANTES]

**Regras fixas desta habilidade:**
1. [O QUE NUNCA PODE ACONTECER]
2. Nada vai para o cliente sem [QUEM APROVA] ler.
3. [SINAL QUE FAZ PARAR E CHAMAR UMA PESSOA]

## 1. Quando usar
- [O QUE DISPARA A ROTINA]

**Não use quando:** [EXCEÇÕES]

## 2. Antes de começar
1. Leia `escritorio/04-base/comum/ficha-do-escritorio.md`, `ficha-da-experiencia.md`, `nicho.md` e `aprendizados-experiencia.md`, se existirem.
2. Leia [O MATERIAL DA ROTINA: carteira, abertura, roteiro].

### Campos da ficha que esta habilidade usa
- **Precisa:** [E: campo, X: campo]
- **Melhora:** [E: campo, X: campo]

## 3. Fluxo
| Passo | O que se faz | Quem | S, A ou H |
|---|---|---|---|
| 1 | [PASSO] | [FUNÇÃO] | [S, A OU H] |

### Último passo. Aprender
Pergunte: "Alguma coisa nessa rotina você faria diferente?". A correção vira regra curta e, com o ok, entra em `escritorio/04-base/comum/aprendizados-experiencia.md`.

## 4. O que entrega e onde grava
| Entrega | Caminho |
|---|---|
| [O QUÊ] | [CAMINHO EM escritorio/] |

## 5. Casos de teste
| Caso | Entrada | O que deve acontecer |
|---|---|---|
| Comum | [ENTRADA] | [SAÍDA] |
| Com exceção | [ENTRADA] | [SAÍDA] |
| Deve parar | [ENTRADA] | Para e chama [QUEM] |
```

Regras do modelo:
- Sem travessão, sem emoji, sem nome de cliente, sem valor inventado.
- Todo passo que fala com cliente é A ou H.
- A habilidade própria fica na pasta do escritório; ela não muda os arquivos do plugin.
