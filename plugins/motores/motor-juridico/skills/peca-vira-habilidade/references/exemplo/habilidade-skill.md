---
name: peticao-inicial-restabelecimento
description: >
  Habilidade do Escritório Modelo. Redige a petição inicial de restabelecimento de benefício por
  incapacidade temporária no Juizado Especial Federal, no jeito do escritório: a estrutura, os
  trechos, as variáveis e as escolhas de estilo das peças boas dele, com toda citação marcada até
  a conferência. Só roda com a tese definida pelo advogado. Use quando alguém do escritório disser
  "faz a inicial de restabelecimento", "minuta a inicial da Marta", "o benefício foi cortado, tese
  definida, pode redigir". Não use para recurso, réplica, pedido de concessão ou outra área (use
  minutar-peca) nem para escolher a tese (use estrategia-do-caso).
---

# Petição inicial de restabelecimento (Escritório Modelo)

> A peça que o escritório faz toda semana, escrita do jeito dele: o modelo já existia nas peças boas, agora está escrito.

Versão da habilidade: 1 (mapa da peça versão 1). Fichas: `escritorio/04-base/comum/ficha-do-escritorio.md`, `ficha-juridica.md`, `nicho.md` e `aprendizados-juridico.md`. O mapa da peça: `references/mapa-da-peca.md`. Testes: `escritorio/04-base/casos-de-teste/juridico/peticao-inicial-restabelecimento-testes.md`. Regras do plugin, se instalado: `docs/regras.md` e `docs/citacoes.md` do motor-juridico.

Segunda, 9h. Três segurados com benefício cortado, mesma situação. O estagiário abre a peça de 2025 de outro cliente, troca o nome e esquece o "o autor" no meio da peça de uma mulher. Esta habilidade parte do mapa, e não de uma peça velha.

**Regras fixas desta habilidade:**
1. Sem tese definida pelo advogado (etapa `tese-definida` no `pecas.csv` ou decisão em `estrategia.md`), não há minuta.
2. Toda citação sai marcada `[CONFERIR: ...]`. A habilidade nunca completa número, relator, data ou enunciado de memória.
3. Só esta peça, desta área. Outra peça, outra área ou exceção que muda a tese: para e leva ao advogado (seção 7 do mapa).
4. Data que diverge entre documentos não é escolhida: vai `[A CONFIRMAR]` com os dois documentos.
5. Nome completo, CPF, endereço e número de benefício não entram: a qualificação é campo de quem protocola, do sistema do escritório.

## 1. Quando usar

**Use quando:** a advogada definiu a tese `restabelecimento-incapacidade` e o caso tem dossiê com a carta de cessação, a negativa da prorrogação, o extrato de vínculos, o relatório médico e o resumo da perícia.

**Não use quando:** a peça é outra (recurso, réplica, concessão) ou a área é outra: `minutar-peca`. A tese ainda não foi escolhida: `estrategia-do-caso`. São muitos casos iguais de uma vez: `pecas-em-lote`, que lê o mesmo mapa.

## 2. Antes de começar

1. Leia as fichas, o `nicho.md` (se existir) e os aprendizados. Aprendizado desta habilidade vale antes do mapa, desde que não afrouxe as regras fixas.
2. Leia o mapa (`references/mapa-da-peca.md`) inteiro: variáveis, exceções e o modelo.
3. Leia o caso: `escritorio/07-operacao/juridico/casos/<codigo>/dossie.md` e `estrategia.md`, e a tese em `escritorio/04-base/juridico/teses/restabelecimento-incapacidade.md`.
4. Treino: com casos fictícios, grave em `escritorio/07-operacao/_treino/juridico/`.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | E: `areas` · J: `quem_redige`, `quem_revisa`, `quem_assina` |
| Melhora | J: `estilo`, `pedidos`, `validade_da_conferencia`, `tribunais_principais` |

## 3. Fluxo

| Passo | O que se faz | Sigla | Quem |
|---|---|---|---|
| 1 | Confere tese, área e peça | S | a habilidade |
| 2 | Preenche as variáveis a partir do dossiê e da estratégia | S | a habilidade |
| 3 | Monta a peça pelo modelo, com as citações marcadas | A | o estagiário lê |
| 4 | Conferência de citações e de dados | S | conferir-citacoes e conferir-peca |
| 5 | Revisa, aprova, assina, protocola | H | a advogada titular |

**Passo 1. Conferir se pode seguir.** Tese definida? Área previdenciário? A peça é a inicial de restabelecimento? Algum caso da seção 7 do mapa? Se parar, diga em uma frase por quê e para quem vai, e não escreva minuta.

**Passo 2. Preencher as variáveis.** Para cada variável da seção 3 do mapa, ache o valor na origem indicada (dossiê, estratégia, ficha). Mostre a tabela "variável · valor · de onde veio". Valor que falta: pergunte uma vez; sem resposta, `[A CONFIRMAR: ...]`. `pedir_tutela` vem só da estratégia ou do advogado.

**Passo 3. Montar.** Siga o modelo da seção 8 do mapa sem mudar o texto fixo. Blocos `{{#se}}` só entram com o valor da condição. Gênero pelo `genero`. Toda citação com a marca. Grave em `escritorio/07-operacao/juridico/casos/<codigo>/minutas/peticao-inicial-restabelecimento-v<n>.md`, com o cabeçalho interno "Antes de protocolar": tese e quem decidiu, citações marcadas, pendências, o que pedir ao cliente (relatório médico anterior à cessação vira "pedir relatório atual").

**Passo 4. Conferir.** Rode a `conferir-citacoes` e a `conferir-peca` (se instaladas; sem elas, a lista de citações e de dados vai no "Antes de protocolar" para a advogada conferir). Etapa `minuta` no `pecas.csv`; `conferida` só com tudo verde e dados ok.

**Passo 5. O que fica com a advogada.** Revisar, decidir as pendências, aprovar, assinar e protocolar.

**No ciclo.** O `agente-juridico` chama esta habilidade para as peças em `tese-definida` com `peca = peticao-inicial-restabelecimento`. Não pergunte nada: o que falta vira `[A CONFIRMAR]`; a minuta vai para a fila (`escritorio/07-operacao/juridico/fila/AAAA-MM-DD/NN-<codigo>-peticao-inicial-restabelecimento.md`) com `revisor: pendente`. Caso que deve parar: nenhuma minuta, uma linha em "ADVOGADO AGORA".

**Passo final. Aprender.** Pergunte: "Alguma coisa nesta peça você faria diferente na próxima?". Correção que vale para todo caso vira ajuste nesta habilidade pela `peca-vira-habilidade`, modo "corrigir" (nova versão do mapa, testes de novo, pacote novo). Correção só deste caso fica na minuta. Regra de escrita que vale para toda peça vai para `aprendizados-juridico.md`, com o ok.

## 4. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Minuta | `escritorio/07-operacao/juridico/casos/<codigo>/minutas/peticao-inicial-restabelecimento-v<n>.md` |
| Item na fila (no ciclo) | `escritorio/07-operacao/juridico/fila/AAAA-MM-DD/` |
| Linha do registro | `escritorio/07-operacao/juridico/pecas.csv`: `etapa = minuta`, `habilidade_usada = peticao-inicial-restabelecimento`, `citacoes = nao-conferidas` |
| Treino | `escritorio/07-operacao/_treino/juridico/` |

O .docx sai pelo script da `minutar-peca` (se instalada), que não gera com citação marcada sem `--forcar`.

## 5. Solo e equipe

**Solo:** a advogada roda, confere e revisa; deixe a revisão para outro momento do dia. **Equipe:** o estagiário roda e confere; a advogada recebe só minutas conferidas, com o relatório.

## 6. Erros que esta habilidade evita

| Erro | Como evita |
|---|---|
| "O autor" na peça de uma mulher | Gênero por variável, no modelo inteiro |
| Data de outro documento escolhida no chute | Regra fixa 4 e seção 7 do mapa |
| Julgado de memória | Toda citação marcada até a conferência |
| Pedido que a estratégia não fez (dano moral "de costume") | O modelo não tem; pedido novo é do advogado |
| Diagnóstico na peça | O mapa só fala da limitação |

## 7. Próximo passo

Conferência: `conferir-citacoes` e `conferir-peca`. Protocolo: `preparar-protocolo` (se instalada). Muitos casos iguais: `pecas-em-lote`. Peça corrigida pela advogada: `peca-vira-habilidade`, modo "corrigir".
