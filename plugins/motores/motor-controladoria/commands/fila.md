---
description: A mesa da controladoria. Mostra, um por um, os prazos esperando a dupla conferência, as providências esperando decisão e os avisos do ciclo. A pessoa confere o ato, o número de dias e a regra, decide a providência, e só então o prazo vai para a agenda e a peça ou o aviso são encaminhados.
---

# /motor-controladoria:fila

Siga `${CLAUDE_PLUGIN_ROOT}/docs/agentes-e-fila.md`, `${CLAUDE_PLUGIN_ROOT}/docs/prazos.md` e `${CLAUDE_PLUGIN_ROOT}/docs/contagem.md`.

0. **PESSOA AGORA primeiro.** Abra o último resumo do dia (`07-operacao/controladoria/rotina/`). Para cada item (prazo de hoje ou amanhã, publicação urgente, sem caso), pergunte o que foi feito ou decidido. Com a resposta, atualize o registro e grave a linha `decidido por <nome>, na conversa, AAAA-MM-DD HH:MM` no item. Sem resposta, o item continua no topo.
**Treino:** com "treino" no pedido (`/motor-controladoria:fila treino`), leia `escritorio/07-operacao/_treino/controladoria/fila/` e grave só em `_treino/`.

1. Leia `escritorio/07-operacao/controladoria/fila/`. Liste os itens com `status: pendente`, o que vence primeiro no topo. Os itens têm `item: conferir-prazo`, `decidir-providencia` ou `aviso`.
1b. **Bloqueados.** Liste os `bloqueado` com o motivo. Para cada um: "Já dá para resolver? Volta para a fila ou descarta?". Resolvido: `status: pendente`, `revisor: pendente`, e o revisor roda nele antes de seguir.
2. **Conferir prazo** (`item: conferir-prazo`). Item com `revisor: pendente` não pode ser conferido. Siga a `dupla-conferencia` (se instalada; sem ela, os passos de `prazos.md`, seção "A dupla conferência"):
   - mostre o trecho literal do ato e pergunte, sem mostrar a sugestão da IA: "O que este ato pede, em quantos dias, e há prazo em dobro?";
   - compare com a sugestão e com a conta do script; mostre a conta passo a passo;
   - **primeira conferência:** grave o nome e a resposta no item, e o item fica esperando a segunda;
   - **segunda conferência:** a pessoa de `quem_confere` (ou a mesma pessoa em outro turno, no escritório de uma pessoa só) responde a mesma pergunta, sem ver a primeira resposta;
   - **bateu:** `status: aprovado` no item, e no `prazos.csv` `status = conferido`, os dois nomes em `conferido_por`, a hora em `conferido_em`, e o registro em `conferencias/AAAA-MM-DD.md`. Ofereça a `agenda-de-prazos` (se instalada; sem ela, mostre o texto do compromisso para a pessoa lançar). O status vira `agendado` só quando a pessoa disser que importou;
   - **não bateu:** o prazo fica `sugerido`, a divergência fica no item, e nada entra na agenda. O resumo mostra o prazo com a data mais cedo, e ele sobe para PESSOA AGORA quando essa data está a 2 dias úteis ou menos.
3. **Decidir providência** (`item: decidir-providencia`). Mostre o ato, a sugestão (`providencia-sugerida`, se instalada) e pergunte: "O que fazemos com esta publicação?". Com a resposta, grave no item a linha `decidido por <nome>, na conversa, AAAA-MM-DD HH:MM`; só então a `encaminhar-providencia` (se instalada) grava o pedido de peça na entrada do motor-juridico, a tarefa ou o aviso para a experiência; sem ela, mostre o texto do pedido para a pessoa copiar.
4. **Aviso** (`item: aviso`: sem caso, duplicada a confirmar, painel não olhado, calendário que falta). Pergunte o que fazer e registre.
5. **Ajustar:** prazo ou texto mudado pela pessoa volta a passar pela tabela do revisor antes de seguir. Correção que vale para as próximas vezes vira proposta de aprendizado.
6. **Descartar:** `status: descartado` e `motivo_descarte`. No registro, o prazo vira `cancelado` só se a pessoa disser que ele deixou de existir.
7. No fim, pergunte quais prazos já foram cumpridos. Para cada um: `status = cumprido` e `cumprido_em` em `prazos.csv` (com o motor-juridico instalado, o protocolo registrado lá já fecha o prazo).
8. Feche com: quantos conferidos, divergentes, encaminhados, cumpridos e descartados, e os aprendizados novos.

A IA nunca escreve um nome em `conferido_por` sem que a própria pessoa diga, na conversa, que conferiu.
