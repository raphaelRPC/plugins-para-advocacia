# Molde da habilidade própria de uma peça

A `peca-vira-habilidade` gera o SKILL.md da peça a partir deste molde e do mapa. O resultado fica em `escritorio/04-base/habilidades-do-escritorio/<peca>/SKILL.md`, ao lado de `references/mapa-da-peca.md`. Um exemplo preenchido está em `references/exemplo/habilidade-skill.md` (no escritório, o arquivo se chama SKILL.md).

O que é fixo neste molde, porque o script de empacotamento confere: o frontmatter só com `name` (igual à pasta) e `description` (até 900 caracteres); "Versão da habilidade: N" igual à versão do mapa; a subseção "Campos da ficha que esta habilidade usa"; o modo "No ciclo"; o passo "Aprender" por último; a regra das citações marcadas; nenhuma citação com número sem a marca `[CONFERIR: ...]`.

```markdown
---
name: [peca]
description: >
  Habilidade do [NOME DO ESCRITÓRIO]. Redige [a peça, por extenso] no jeito do escritório: a
  estrutura, os trechos, as variáveis e as escolhas de estilo das peças boas dele, com toda
  citação marcada até a conferência. Só roda com a tese definida pelo advogado. Use quando
  alguém do escritório disser "[frase real 1]", "[frase real 2]", "[frase real 3]". Não use para
  [outra peça ou outra área] (use minutar-peca) nem para escolher a tese (use estrategia-do-caso).
---

# [Nome da peça] ([NOME DO ESCRITÓRIO])

> [Uma linha: o que a peça resolve e de onde o modelo saiu.]

Versão da habilidade: [N] (mapa da peça versão [N]). Fichas: `escritorio/04-base/comum/ficha-do-escritorio.md`, `ficha-juridica.md`, `nicho.md` e `aprendizados-juridico.md`. O mapa da peça: `references/mapa-da-peca.md`. Testes: `escritorio/04-base/casos-de-teste/juridico/[peca]-testes.md`.

[Cena de 2 a 4 linhas: como a peça saía antes, com o erro que o escritório já viu acontecer.]

**Regras fixas desta habilidade:**
1. Sem tese definida pelo advogado, não há minuta.
2. Toda citação sai marcada `[CONFERIR: ...]`; nada de número, relator, data ou enunciado de memória.
3. Só esta peça, desta área. Exceção que muda a tese: para e leva ao advogado.
4. [A regra mais importante que o advogado disse na entrevista.]
5. Dado de identificação (nome completo, CPF, endereço, número de processo ou benefício) sai do sistema do escritório no protocolo, como campo entre chaves.

## 1. Quando usar
**Use quando:** [a tese, o tipo de caso e os documentos que precisam existir].
**Não use quando:** [outra peça, outra área, tese não escolhida, lote].

## 2. Antes de começar
1. Leia as fichas, o nicho e os aprendizados.
2. Leia o mapa inteiro: variáveis, exceções e o modelo.
3. Leia o caso: `dossie.md`, `estrategia.md` e a tese no banco.
4. Treino: grave em `escritorio/07-operacao/_treino/juridico/`.

### Campos da ficha que esta habilidade usa
| | Campos |
|---|---|
| Precisa | E: `areas` · J: `quem_redige`, `quem_revisa`, `quem_assina` |
| Melhora | J: `estilo`, `pedidos`, `validade_da_conferencia` [e o que a peça pedir] |

## 3. Fluxo
| Passo | O que se faz | Sigla | Quem |
|---|---|---|---|
| 1 | Confere tese, área e peça | S | a habilidade |
| 2 | Preenche as variáveis | S | a habilidade |
| 3 | Monta pelo modelo, citações marcadas | A | [quem_redige] lê |
| 4 | Conferência de citações e de dados | S | conferir-citacoes e conferir-peca |
| 5 | Revisa, aprova, assina, protocola | H | [quem_assina] |

Passo 1 a passo 5: [as instruções, como no exemplo].
No ciclo: [o que faz quando o agente-juridico chama: sem perguntas, minuta na fila com `revisor: pendente`, o que deve parar vai para "ADVOGADO AGORA"].
Passo final. Aprender: correção que vale para todo caso vira nova versão pela `peca-vira-habilidade`, modo "corrigir"; regra de escrita geral vai para `aprendizados-juridico.md`, com o ok.

## 4. O que entrega e onde grava
[minuta, fila, pecas.csv, treino]

## 5. Solo e equipe
## 6. Erros que esta habilidade evita
## 7. Próximo passo
```
