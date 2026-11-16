---
description: Roda agora o ciclo do dia da produção jurídica. O agente lê a fila de peças e os pedidos, monta dossiês, minuta o que tem tese definida, confere citações e dados e prepara protocolos. O revisor confere cada item, e as minutas ficam na fila para o advogado.
---

# /motor-juridico:ciclo

Siga `${CLAUDE_PLUGIN_ROOT}/docs/agentes-e-fila.md`.

1. Confira se existem `escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-juridica.md`. Sem elas, ofereça `/motor-juridico:comecar` e pare.
2. Chame o agente `agente-juridico` do plugin. Ele grava as minutas na fila com `revisor: pendente`.
3. Em seguida, liste os arquivos da fila de hoje (`07-operacao/juridico/fila/AAAA-MM-DD/`) que têm `revisor: pendente` e chame o agente `revisor-juridico` passando essa lista de caminhos, para ele não depender de busca de arquivos. Ele grava a decisão em cada arquivo.
   Depois, feche o resumo do dia em `07-operacao/juridico/rotina/AAAA-MM-DD.md`: acrescente a linha "Revisão: N ok, N ajustados, N para conferir, N bloqueados" e mova cada bloqueado para "ADVOGADO AGORA" ou "PARA DECIDIR", com o motivo do revisor. Atualize a linha da rodada no registro de uso (`05-automacoes/ciclo-juridico/registro-de-uso.md`).
4. Se agentes de plugin não estiverem disponíveis neste ambiente (por exemplo, no chat com Projeto), rode o mesmo ciclo pela habilidade `rotina-juridica`, no modo "ciclo à mão", e faça a revisão você mesmo com a tabela do arquivo `agents/revisor-juridico.md`, antes de mostrar qualquer minuta.
5. Ao terminar, mostre: ADVOGADO AGORA, com uma frase por item; as minutas na fila (ok, ajustadas, para conferir, bloqueadas); o que pesquisar no Jus IA; o caminho do resumo; o que falhou.
6. Pergunte: "Quer ver a fila agora?". Se sim, siga `/motor-juridico:fila`.
