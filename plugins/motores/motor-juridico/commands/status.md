---
description: Mostra a produção jurídica agora: peças por etapa, prazos internos de hoje e amanhã, minutas esperando o advogado, citações por conferir, protocolos preparados e o quanto as fichas e a base do escritório estão completas.
---

# /motor-juridico:status

Mostre o estado da produção jurídica sem fazer perguntas desnecessárias. Siga `${CLAUDE_PLUGIN_ROOT}/docs/regras.md`.

## 1. Ler

1. As fichas (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-juridica.md`). Sem fichas, ofereça `/motor-juridico:comecar` e pare.
2. `escritorio/07-operacao/juridico/pecas.csv` (formato em `${CLAUDE_PLUGIN_ROOT}/docs/producao.md`). Sem registro, diga que ele começa com a primeira peça pedida.
3. A fila (`07-operacao/juridico/fila/`) e o último resumo em `rotina/`.
4. A base: quantas habilidades próprias em `04-base/habilidades-do-escritorio/`, quantos temas em `04-base/juridico/jurisprudencia/` e quantos com conferência vencida (`validade_da_conferencia`), quantas teses em `04-base/juridico/teses/`.

## 2. Mostrar

1. **Advogado agora:** prazo interno hoje ou amanhã sem minuta aprovada; peça esperando tese.
2. **Peças por etapa** (tabela curta).
3. **Fila:** minutas pendentes, para conferir e bloqueadas, a mais antiga primeiro.
4. **Citações:** peças com citação não conferida, amarela ou vermelha; temas da base com conferência vencida.
5. **Protocolo:** aprovadas esperando protocolo.
6. **Base do escritório:** habilidades próprias, temas e teses (com os sinais de enfraquecimento do último desempenho, se houver), e a peça mais feita que ainda não virou habilidade.
7. **Fichas:** percentual preenchido e os três campos que mais fazem falta.

Sem números inventados: coluna vazia é dado que ainda não existe.

## 3. Sugerir

Uma linha com a ação mais importante do momento e a habilidade que cuida dela. Se o ciclo não rodou nos últimos dois dias úteis, lembre de `/motor-juridico:ciclo`.
