---
description: Roda agora o ciclo do dia da controladoria. O agente capta as publicações, tria, liga ao caso, calcula os prazos sugeridos e grava a fila de conferência. O revisor refaz cada conta e confere o trecho literal. Nenhum prazo vai para a agenda sem a dupla conferência de uma pessoa.
---

# /motor-controladoria:ciclo

Siga `${CLAUDE_PLUGIN_ROOT}/docs/agentes-e-fila.md` e `${CLAUDE_PLUGIN_ROOT}/docs/prazos.md`.

1. Confira se existem `escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-controladoria.md`. Sem elas, ofereça `/motor-controladoria:comecar` e pare.
2. Chame o agente `agente-de-controladoria` do plugin. Ele grava os itens na fila com `revisor: pendente`.
3. Em seguida, liste os arquivos da fila de hoje (`07-operacao/controladoria/fila/AAAA-MM-DD/`) que têm `revisor: pendente` e chame o agente `revisor-de-controladoria` passando essa lista de caminhos, para ele não depender de busca de arquivos. Ele grava a decisão em cada arquivo.
   Depois, feche o resumo do dia em `07-operacao/controladoria/rotina/AAAA-MM-DD.md`: acrescente a linha "Revisão: N ok, N ajustados, N para conferir, N bloqueados" e mova cada bloqueado para "PESSOA AGORA" ou "PARA DECIDIR", com o motivo do revisor. Atualize a linha da rodada no registro de uso (`05-automacoes/ciclo-da-controladoria/registro-de-uso.md`).
4. Se agentes de plugin não estiverem disponíveis neste ambiente (por exemplo, no chat com Projeto), rode o mesmo ciclo pela habilidade `rotina-da-controladoria`, no modo "ciclo à mão", e faça a revisão você mesmo com a tabela do arquivo `agents/revisor-de-controladoria.md`, antes de mostrar qualquer prazo.
5. Ao terminar, mostre: PESSOA AGORA, com uma frase por item; os prazos esperando a dupla conferência, do que vence primeiro ao último; as publicações sem caso; as audiências e perícias novas; o caminho do resumo; o que falhou (fonte fora do ar, planilha sem coluna, calendário que falta).
6. Pergunte: "Quer fazer a conferência agora?". Se sim, siga `/motor-controladoria:fila`.
