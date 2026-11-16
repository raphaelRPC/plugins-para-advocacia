# Modelo de habilidade do escritório

A `adaptar-comercial` usa este modelo para transformar uma rotina própria do comercial em habilidade. A habilidade nova fica em `escritorio/04-base/habilidades-do-escritorio/<nome>/SKILL.md`, no mesmo formato das habilidades do plugin, mas é do escritório: lê as fichas pela pasta `escritorio/04-base/comum/` e não depende do plugin para funcionar. O nome da pasta é o `name` do frontmatter: minúsculas, sem acento, com hífen.

Primeiro o esqueleto, depois um exemplo preenchido.

## O esqueleto

```markdown
---
name: [nome-da-rotina]
description: >
  [O que faz, em duas frases.] [Quando roda: o que dispara.] Use quando alguém do escritório
  disser "[frase real 1]", "[frase real 2]", "[frase real 3]". Não use para [o que parece e não é]
  (use [outra habilidade]).
---

# [Nome da rotina]

> [Resumo de uma linha: o que a rotina garante.]

Fichas do escritório: `escritorio/04-base/comum/ficha-do-escritorio.md`, `ficha-comercial.md`, `nicho.md` e `aprendizados-comercial.md`. Rotina escrita em `escritorio/04-base/comum/rotinas-do-escritorio.md`.

[Cena concreta de 2 a 4 linhas: o que acontecia antes da rotina.]

**Regras fixas desta habilidade:**
1. [O que nunca pode acontecer, dito pelo advogado na entrevista.]
2. Nada vai para cliente sem uma pessoa ler e aprovar. A habilidade nunca envia.
3. Sinal de violência, ameaça, risco à vida, criança em risco ou vulnerabilidade: para e leva a uma pessoa.
4. [Regra da rotina sobre dados: o mínimo necessário, nada de senha ou documento por mensagem.]

## 1. Quando usar
**Use quando:** [o que dispara a rotina, com dia e hora se houver].
**Não use quando:** [o que parece e não é, e qual habilidade cuida].

## 2. Antes de começar
1. Leia as fichas, o nicho e os aprendizados.
2. Leia [o registro ou o arquivo de onde a rotina parte, com o caminho em escritorio/].
3. Treino: com casos fictícios, grave em `escritorio/07-operacao/_treino/comercial/`.

### Campos da ficha que esta habilidade usa
- **Precisa:** [E: campo · C: campo]
- **Melhora:** [E: campo · C: campo]

## 3. Fluxo
| Passo | O que se faz | Sigla | Quem |
|---|---|---|---|
| 1 | [o que dispara e o que a habilidade lê] | S | a habilidade |
| 2 | [o que a habilidade prepara] | A | [função que lê e aprova] |
| 3 | [o que é sempre de uma pessoa] | H | [função] |

Passo 1. [instrução exata]
Passo 2. [instrução exata, com o texto-modelo, se houver]
Passo 3. [o que fica com a pessoa; a habilidade só prepara o material em volta]
Passo N. Quando parar: [as exceções da rotina; cada uma diz para quem vai].
Último passo. Aprender: pergunte "Alguma coisa você faria diferente?" e, com o ok, guarde a correção em `aprendizados-comercial.md`, com o nome desta habilidade.

## 4. O que entrega e onde grava
| Entrega | Caminho |
|---|---|
| [o rascunho, a lista, o registro] | [caminho em escritorio/] |

## 5. Solo e equipe
**Solo:** [como roda quando é uma pessoa só].
**Equipe:** [quem faz cada passo].

## 6. Erros que esta habilidade evita
| Erro | Consequência | Como evita |
|---|---|---|

## 7. Próximo passo
[O que vem depois e qual habilidade cuida.]

## Mudanças
- 1 · AAAA-MM-DD · criada pela adaptar-comercial · testada em [3] casos
```

## Exemplo preenchido (Escritório Modelo, fictício)

Rotina contada pela advogada: "Quem sai da consulta dizendo que vai pensar, eu ligo no dia útil seguinte. Mensagem a gente só manda se a pessoa não atender. Nunca ligo para quem pediu para não ser procurado, e se a pessoa contou alguma coisa grave na consulta, quem liga sou eu, sem roteiro."

```markdown
---
name: ligacao-depois-da-consulta
description: >
  Prepara a ligação do dia útil seguinte para quem saiu da consulta dizendo que vai pensar: a lista
  de quem ligar, o roteiro curto da ligação e, se a pessoa não atender, o rascunho de uma mensagem
  para alguém aprovar. Roda todo dia útil às 9h. Use quando alguém do escritório disser "quem eu
  ligo hoje?", "lista da ligação de ontem", "prepara a ligação de quem vai pensar". Não use para o
  retorno a quem não agendou ou não respondeu a proposta (use follow-up).
---

# Ligação depois da consulta

> Quem disse "vou pensar" recebe uma ligação no dia útil seguinte, e só quem não atender recebe mensagem.

Fichas do escritório: `escritorio/04-base/comum/ficha-do-escritorio.md`, `ficha-comercial.md`, `nicho.md` e `aprendizados-comercial.md`. Rotina escrita em `escritorio/04-base/comum/rotinas-do-escritorio.md`.

A consulta acabava com "vou pensar" e a advogada esperava a pessoa voltar. Metade não voltava, e ninguém sabia se por desinteresse ou por vergonha de perguntar o preço de novo.

**Regras fixas desta habilidade:**
1. Ninguém que pediu para parar entra na lista.
2. Nada vai para cliente sem uma pessoa ler e aprovar. A habilidade nunca envia.
3. Contato com relato sensível na consulta: a advogada liga, sem roteiro.
4. A ligação não negocia preço nem pressiona: pergunta se ficou alguma dúvida.

## 1. Quando usar
**Use quando:** todo dia útil às 9h, ou quando alguém pedir a lista.
**Não use quando:** o contato não agendou ou não respondeu a proposta (use `follow-up`).

## 2. Antes de começar
1. Leia as fichas, o nicho e os aprendizados.
2. Leia `escritorio/07-operacao/comercial/contatos.csv` e as atas em `escritorio/07-operacao/comercial/consultas/`.
3. Treino: com casos fictícios, grave em `escritorio/07-operacao/_treino/comercial/`.

### Campos da ficha que esta habilidade usa
- **Precisa:** E: `tratamento`, `horario_de_atendimento` · C: `quem_faz_a_consulta`
- **Melhora:** E: `tom_em_tres_palavras` · C: `follow_up`

## 3. Fluxo
| Passo | O que se faz | Sigla | Quem |
|---|---|---|---|
| 1 | Listar quem está em `consulta-feita` com "retorno combinado" e consulta no dia útil anterior | S | a habilidade |
| 2 | Roteiro curto da ligação, a partir da ata | A | advogada |
| 3 | A ligação | H | advogada |
| 4 | Se não atendeu: rascunho de mensagem | A | secretária lê, advogada aprova |

Passo 1. Monte a lista. Fora dela: `pediu_para_parar = sim`, etapa diferente de `consulta-feita`, ata com "relato sensível" (vai para a advogada, sem roteiro).
Passo 2. Roteiro de três linhas: o que foi conversado, o combinado, a pergunta "ficou alguma dúvida?".
Passo 3. A advogada liga. A habilidade não faz este passo.
Passo 4. Não atendeu: rascunho curto, sem pressão, para a secretária ler e a advogada aprovar.
Passo 5. Quando parar: pediu para parar, relato sensível, contato que já disse que não quer: a lista mostra para a advogada decidir.
Passo 6. Aprender: pergunte "Alguma coisa você faria diferente?" e, com o ok, guarde em `aprendizados-comercial.md`.

## 4. O que entrega e onde grava
| Entrega | Caminho |
|---|---|
| Lista e roteiros do dia | `escritorio/07-operacao/comercial/rotina/AAAA-MM-DD.md`, seção "Ligação depois da consulta" |
| Rascunho de mensagem | `escritorio/07-operacao/comercial/fila/AAAA-MM-DD/NN-<codigo>-ligacao-sem-resposta.md` |

## 5. Solo e equipe
**Solo:** a titular faz a lista e as ligações no mesmo horário.
**Equipe:** a secretária roda a habilidade; a advogada liga.

## 6. Erros que esta habilidade evita
| Erro | Consequência | Como evita |
|---|---|---|
| Ligar para quem pediu para parar | Incômodo e reclamação | Passo 1 tira da lista |
| Ligação que vira pressão | Tom de venda | Regra fixa 4 |

## 7. Próximo passo
Quem pediu a proposta na ligação: `proposta-de-honorarios`.

## Mudanças
- 1 · AAAA-MM-DD · criada pela adaptar-comercial · testada em 3 casos
```

Este exemplo tem menos linhas que as habilidades do plugin, de propósito: rotina pequena vira habilidade pequena. O script de empacotamento avisa quando o SKILL.md fica curto demais, mas não impede.
