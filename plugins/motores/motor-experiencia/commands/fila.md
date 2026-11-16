---
description: Mostra os rascunhos para clientes esperando aprovação, um por um, para aprovar, ajustar ou descartar. Depois que a pessoa envia pelo canal oficial, atualiza a carteira e o histórico do cliente.
---

# /motor-experiencia:fila

Siga `${CLAUDE_PLUGIN_ROOT}/docs/agentes-e-fila.md` e `${CLAUDE_PLUGIN_ROOT}/docs/regras.md`.

0. **PESSOA AGORA primeiro.** Abra o último resumo do dia (`rotina/`). Para cada item em PESSOA AGORA, pergunte: "Já falou com essa pessoa? O que ficou combinado?". Com a resposta, grave na `carteira.csv`, `ultimo_contato` (se a conversa informou algo do caso) e uma linha no `historico.md`, e grave o combinado na carteira: `proximo_contato` com a data combinada e `motivo_proximo_contato = retorno-combinado` (a carteira não tem `proximo_passo`). Sem resposta, o item continua no topo.
1. Leia `escritorio/07-operacao/experiencia/fila/`. Liste os itens com `status: pendente` (os `bloqueado` ficam para o passo 1b), os mais antigos e os de prazo mais curto primeiro. Sem itens: diga que a fila está vazia e quando foi o último ciclo.
1b. **Bloqueados.** Liste os itens `bloqueado` com o motivo do revisor. Para cada um, pergunte: "Já dá para resolver? Volta para a fila ou descarta?". Resolvido: aplique o que a pessoa disse, `status: pendente` e `revisor: pendente`, e rode o revisor nele antes de seguir. Descartar: passo de descartar abaixo.
2. Para cada item, mostre: para quem, por quê (o `motivo`), o prazo, a nota do revisor, as conferências de `antes_de_enviar` (só para a pessoa, nunca para o cliente) e o texto. Item com `revisor: pendente` não pode ser aprovado: rode o revisor antes. Item com `revisor: conferir` mostra primeiro o que conferir e só aprova depois que a pessoa disser que conferiu. Pergunte: "Aprovar, ajustar ou descartar?".
   - **Aprovar:** `status: aprovado`. Se o texto tem campos do envio entre chaves (`{...}`), mostre quais são: quem envia preenche na hora. Lembre que quem envia é a pessoa, pelo canal oficial.
   - **Ajustar:** aplique o ajuste, passe o texto novo pela tabela do revisor (o arquivo do revisor do plugin, em `agents/`), mostre de novo e aprove com o ok. Se o ajuste é uma correção que vale para as próximas vezes, ofereça guardar como aprendizado.
   - **Descartar:** `status: descartado` e `motivo_descarte: <uma linha>` no cabeçalho. Pergunte o que acontece com o contato ou cliente agora (outro rascunho, ligação, encaminhado, perdido, nada) e atualize o registro com o ok. Se o motivo é uma regra ("nunca mandamos isso para..."), ofereça guardar como aprendizado.
3. No fim, pergunte quais aprovados já foram enviados. Não marque `enviado` enquanto houver `{...}` ou qualquer marcação entre colchetes no texto. Para cada um: `status: enviado`, uma linha em `escritorio/07-operacao/experiencia/clientes/<codigo>/historico.md` e, na `carteira.csv`, `atualizado_em`. `ultimo_contato` e `ultimo_contato_tipo` só mudam se a mensagem informou algo do caso (status, resumo, página, boas-vindas); ponte, cortesia, lembrete de documento e pesquisa não zeram o "sem notícia" (`agentes-e-fila.md`). Mostre as linhas antes de gravar.
4. Feche com: quantos aprovados, ajustados, descartados e enviados, e os aprendizados novos.
