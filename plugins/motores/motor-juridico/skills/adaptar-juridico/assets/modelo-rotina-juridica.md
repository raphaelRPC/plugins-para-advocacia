# Modelo de rotina do jurídico virada habilidade

A `adaptar-juridico` usa este modelo para transformar uma rotina própria da produção jurídica (algo que o escritório faz sempre do mesmo jeito e que nenhuma habilidade cobre) em habilidade. Para uma **peça**, o caminho é outro: a `peca-vira-habilidade`, que monta o mapa da peça.

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

Fichas: `escritorio/04-base/comum/ficha-do-escritorio.md`, `ficha-juridica.md`, `nicho.md` e `aprendizados-juridico.md`. Rotina escrita em `escritorio/04-base/comum/rotinas-do-escritorio.md`.

[Cena de 2 a 4 linhas: o que acontecia antes.]

**Regras fixas desta habilidade:**
1. [O que nunca pode acontecer, dito pelo advogado.]
2. Escolher tese, aprovar, assinar e protocolar são do advogado. A habilidade prepara e confere.
3. Toda citação sai marcada `[CONFERIR: ...]`; nada de número, relator, data ou enunciado de memória.
4. [Regra de dados da rotina: o mínimo necessário, nada de senha ou certificado.]

## 1. Quando usar
## 2. Antes de começar
### Campos da ficha que esta habilidade usa
## 3. Fluxo
| Passo | O que se faz | Sigla | Quem |
No ciclo: [o que faz quando o agente-juridico chama, ou "não roda no ciclo"].
Último passo. Aprender: [pergunta e onde guarda].
## 4. O que entrega e onde grava
## 5. Solo e equipe
## 6. Erros que esta habilidade evita
## 7. Próximo passo
```

## Exemplo preenchido (Escritório Modelo, fictício)

A rotina: "toda inicial nova, o estagiário monta a lista de documentos na ordem que a advogada gosta, com o nome de arquivo do sistema, e diz o que falta antes de minutar".

```markdown
---
name: ordem-dos-documentos
description: >
  Habilidade do Escritório Modelo. Monta a lista de documentos de uma peça nova na ordem do
  escritório (doc. 1 a doc. N), com o nome de arquivo do sistema de protocolo, e aponta o que
  falta antes de minutar. Roda quando o dossiê do caso fica pronto. Use quando alguém disser
  "monta a ordem dos documentos", "o que falta para a inicial da Marta". Não use para o
  checklist de protocolo (use preparar-protocolo) nem para analisar os documentos (use
  dossie-do-caso).
---

# Ordem dos documentos

> Toda peça nova sai com os documentos na mesma ordem e com o que falta dito antes da minuta.

Fichas: `escritorio/04-base/comum/ficha-do-escritorio.md`, `ficha-juridica.md`, `nicho.md` e `aprendizados-juridico.md`. Rotina escrita em `escritorio/04-base/comum/rotinas-do-escritorio.md`.

A advogada abre a minuta e o "doc. 6" é o relatório num caso e a carteira no outro. O protocolo atrasa porque falta o relatório atual, e ninguém pediu ao cliente.

**Regras fixas desta habilidade:**
1. A ordem é a do escritório; documento que não está na lista vai para o fim, marcado "fora da ordem".
2. Escolher tese, aprovar, assinar e protocolar são do advogado. A habilidade prepara e confere.
3. Toda citação sai marcada `[CONFERIR: ...]`; esta rotina não cita norma nem julgado.
4. Só o nome e a data do documento; laudo completo e dado de saúde ficam fora da lista.

## 1. Quando usar
**Use quando:** o `dossie.md` do caso ficou pronto e a peça é nova.
**Não use quando:** é o checklist do protocolo (`preparar-protocolo`) ou a análise dos documentos (`dossie-do-caso`).

## 2. Antes de começar
1. Leia as fichas e o `dossie.md` do caso.
2. Treino: grave em `escritorio/07-operacao/_treino/juridico/`.

### Campos da ficha que esta habilidade usa
- **Precisa:** J: `nome_dos_arquivos`, `pecas_mais_feitas`
- **Melhora:** J: `limite_de_tamanho`, `quem_redige`

## 3. Fluxo
| Passo | O que se faz | Sigla | Quem |
|---|---|---|---|
| 1 | Lê o índice do dossiê | S | a habilidade |
| 2 | Põe na ordem do escritório e dá o nome de arquivo | S | a habilidade |
| 3 | Lista o que falta e o que pedir ao cliente | A | o estagiário confere |
| 4 | Pede o documento ao cliente | H | a pessoa que fala com o cliente |

Passo 1. Leia o índice do `dossie.md`. Passo 2. Ordem: carta de cessação, negativa, extrato de vínculos, relatório médico, perícia, outros. Passo 3. Falta documento obrigatório da peça: diga qual e por quê. Quando parar: documento com dado de criança ou processo em segredo, sem autorização do advogado: para e leva a ele.
No ciclo: não roda no ciclo; a pedido.
Último passo. Aprender: pergunte "Alguma ordem você faria diferente?" e, com o ok, guarde em `aprendizados-juridico.md`, com o nome desta habilidade.

## 4. O que entrega e onde grava
| Entrega | Caminho |
|---|---|
| Lista de documentos | `escritorio/07-operacao/juridico/casos/<codigo>/documentos-da-peca.md` |

## 5. Solo e equipe
Solo: a advogada roda antes de minutar. Equipe: o estagiário roda e a secretária pede o que falta.

## 6. Erros que esta habilidade evita
| Erro | Como evita |
|---|---|
| "doc. 6" diferente em cada peça | Ordem fixa |
| Falta de documento descoberta no protocolo | Lista do que falta antes da minuta |

## 7. Próximo passo
Minuta: a habilidade própria da peça, ou a `minutar-peca`.
```
