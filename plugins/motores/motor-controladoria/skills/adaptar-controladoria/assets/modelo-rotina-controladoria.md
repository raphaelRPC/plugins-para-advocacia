# Modelo de rotina da controladoria virada habilidade

A `adaptar-controladoria` usa este modelo para transformar uma rotina própria da controladoria (algo que o escritório faz sempre do mesmo jeito e que nenhuma habilidade cobre) em habilidade. Regra própria de contagem não vira habilidade: vai para a tabela de regras, pela `calendario-forense`.

A habilidade nova fica em `escritorio/04-base/habilidades-do-escritorio/<nome>/SKILL.md`, no formato das habilidades do plugin, e lê as fichas pela pasta `escritorio/04-base/comum/`. O nome da pasta é o `name` do frontmatter: minúsculas, sem acento, com hífen.

## O esqueleto

```markdown
---
name: [nome-da-rotina]
description: >
  [O que faz, em duas frases.] [O que dispara.] Use quando alguém do escritório disser
  "[frase real 1]", "[frase real 2]". Não use para [o que parece e não é] (use [outra]).
---

# [Nome da rotina]

> [Uma linha: o que a rotina garante.]

Fichas: `escritorio/04-base/comum/ficha-do-escritorio.md`, `ficha-da-controladoria.md`, `nicho.md` e `aprendizados-controladoria.md`. Regras de contagem: `escritorio/04-base/controladoria/regras-de-contagem.md`. Rotina escrita em `escritorio/04-base/comum/rotinas-do-escritorio.md`.

[Cena de 2 a 4 linhas: o que acontecia antes.]

**Regras fixas desta habilidade:**
1. [O que nunca pode acontecer, dito pelo escritório.]
2. A IA capta e calcula, mas não interpreta: confirmar prazo, decidir dobro, ciência tácita e providência são de uma pessoa.
3. Prazo de hoje ou do próximo dia útil vai para uma pessoa antes de qualquer outra coisa.
4. [Regra de dados: o mínimo necessário; senha, certificado e token nunca passam pela IA.]

## 1. Quando usar
## 2. Antes de começar
### Campos da ficha que esta habilidade usa
## 3. Fluxo
| Passo | O que se faz | Sigla | Quem |
No ciclo: [o que faz quando o agente-de-controladoria ou a rotina chama, ou "não roda no ciclo"].
Último passo. Aprender: [pergunta e onde guarda].
## 4. O que entrega e onde grava
## 5. Solo e equipe
## 6. Erros que esta habilidade evita
## 7. Próximo passo
```

## Exemplo preenchido (Escritório Modelo, fictício)

A rotina: "toda sexta, às 16h, a advogada olha com a estagiária os prazos da semana seguinte que ainda estão sugeridos, e nenhum fim de semana começa com prazo de segunda sem conferência".

```markdown
---
name: conferencia-de-sexta
description: >
  Habilidade do Escritório Modelo. Toda sexta, monta a lista dos prazos da semana seguinte que
  ainda não passaram pela dupla conferência, do que vence primeiro ao último, para a advogada e a
  estagiária conferirem antes do fim de semana. Use quando alguém disser "a conferência de
  sexta", "o que fica sem conferir para segunda". Não use para conferir um prazo (use
  dupla-conferencia) nem para o resumo do dia (use rotina-da-controladoria).
---

# Conferência de sexta

> Nenhuma segunda-feira começa com prazo da semana sem dupla conferência.

Fichas: `escritorio/04-base/comum/ficha-do-escritorio.md`, `ficha-da-controladoria.md`, `nicho.md` e `aprendizados-controladoria.md`. Regras de contagem: `escritorio/04-base/controladoria/regras-de-contagem.md`. Rotina escrita em `escritorio/04-base/comum/rotinas-do-escritorio.md`.

Na segunda, às 8h, a estagiária descobre que a data de segurança de um recurso é terça e ninguém conferiu na semana anterior. A advogada está em audiência até o meio-dia.

**Regras fixas desta habilidade:**
1. A lista sai na sexta, até as 16h; se a sexta for feriado, no dia útil anterior.
2. A IA capta e calcula, mas não interpreta: confirmar prazo, decidir dobro, ciência tácita e providência são de uma pessoa.
3. Prazo de hoje ou do próximo dia útil vai para uma pessoa antes de qualquer outra coisa.
4. Só id, código, primeiro nome, providência e datas; o número do processo fica no registro.

## 1. Quando usar
**Use quando:** é sexta à tarde, ou o último dia útil da semana.
**Não use quando:** é para conferir um prazo (`dupla-conferencia`) ou ver o dia (`rotina-da-controladoria`).

## 2. Antes de começar
1. Leia as fichas e o `prazos.csv`.
2. Treino: grave em `escritorio/07-operacao/_treino/controladoria/`.

### Campos da ficha que esta habilidade usa
- **Precisa:** K: `quem_confere`, `responsavel_controladoria`
- **Melhora:** K: `dias_de_seguranca`

## 3. Fluxo
| Passo | O que se faz | Sigla | Quem |
|---|---|---|---|
| 1 | Roda o script de pendências da rotina-da-controladoria com --semana 5 | S | a habilidade |
| 2 | Separa os `sugerido` com segurança ou fatal até a sexta seguinte | S | a habilidade |
| 3 | Mostra a lista, do que vence primeiro ao último, com o trecho e a conta de cada um | A | a estagiária confere |
| 4 | Faz a dupla conferência de cada um | H | a estagiária e a advogada |

Quando parar: prazo com segurança ou fatal hoje ou no próximo dia útil; para tudo e leva à advogada agora. Número de dias sem fonte: para e pergunta.
No ciclo: não roda no ciclo; a pedido, ou pela tarefa agendada de sexta.
Último passo. Aprender: pergunte "Algum prazo devia ter entrado e não entrou?" e, com o ok, guarde em `aprendizados-controladoria.md`, com o nome desta habilidade.

## 4. O que entrega e onde grava
| Entrega | Caminho |
|---|---|
| A lista de sexta | `escritorio/07-operacao/controladoria/rotina/AAAA-MM-DD-sexta.md` |

## 5. Solo e equipe
Solo: a mesma pessoa, em outro turno (a sexta à tarde é o segundo turno). Equipe: a estagiária monta, a advogada confere.

## 6. Erros que esta habilidade evita
| Erro | Como evita |
|---|---|
| Prazo de segunda sem conferência | Lista da semana seguinte na sexta |
| Conferência às pressas na segunda | Conferência marcada na sexta, com tempo |

## 7. Próximo passo
Dupla conferência: `dupla-conferencia`. Agenda dos conferidos: `agenda-de-prazos`.
```
