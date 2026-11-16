---
description: Roda agora o ciclo do dia da experiência do cliente. O agente lê o que chegou, separa o que é para uma pessoa, varre a carteira, prepara status, lembretes e resumos, passa tudo pelo revisor e deixa a fila de aprovação e o resumo do dia.
---

# /motor-experiencia:ciclo

Siga `${CLAUDE_PLUGIN_ROOT}/docs/agentes-e-fila.md`.

1. Confira se existem `escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-experiencia.md`. Sem elas, ofereça `/motor-experiencia:comecar` e pare.
2. Chame o agente `agente-de-suporte` do plugin para rodar o ciclo. Ele grava os rascunhos na fila com `revisor: pendente`.
3. Em seguida, liste os arquivos da fila de hoje (`07-operacao/experiencia/fila/AAAA-MM-DD/`) que têm `revisor: pendente` e chame o agente `revisor-de-suporte` passando essa lista de caminhos, para ele não depender de busca de arquivos. Ele grava a decisão em cada arquivo.
   Depois, feche o resumo do dia que o agente gravou em `rotina/AAAA-MM-DD.md`: acrescente a linha "Revisão: N ok, N ajustados, N para conferir, N bloqueados" e mova cada bloqueado para "PESSOA AGORA" ou "PARA DECIDIR", com o motivo do revisor. Atualize também a linha da rodada no registro de uso (`05-automacoes/ciclo-*/registro-de-uso.md`) com o resultado da revisão.
4. Se agentes de plugin não estiverem disponíveis neste ambiente (por exemplo, no chat com Projeto), rode o mesmo ciclo pela habilidade de rotina do plugin, no modo "ciclo à mão", e faça a revisão você mesmo com a tabela do arquivo `agents/revisor-de-suporte.md`, antes de mostrar qualquer rascunho.
5. Ao terminar, mostre:
   - PESSOA AGORA, com uma frase por item;
   - quantos rascunhos estão na fila (ok, ajustados, para conferir) e quantos foram bloqueados e até quando cada um precisa sair (prazo da ficha da experiência);
   - o caminho do resumo do dia;
   - o que falhou.
6. Pergunte: "Quer revisar a fila agora?". Se sim, siga `/motor-experiencia:fila`.
