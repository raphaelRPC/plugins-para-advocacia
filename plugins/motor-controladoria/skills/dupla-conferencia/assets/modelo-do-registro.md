---
documento: Conferências do dia
data: AAAA-MM-DD
treino: nao
versao: 1
dono: [A PREENCHER]
---

# Conferências · AAAA-MM-DD

Uma linha por conferência terminada (bateu, divergiu ou decidida depois da divergência). Os nomes são os que cada pessoa disse na conversa, nunca escritos pela IA por conta própria. Arquivo em `escritorio/07-operacao/controladoria/conferencias/AAAA-MM-DD.md` (treino: `escritorio/07-operacao/_treino/controladoria/conferencias/`). A `auditoria-de-prazos` lê esta tabela todo mês.

| prazo_id | codigo_caso | sugestao_ia | primeira_por | primeira_leitura | segunda_por | segunda_leitura | conta_1 | conta_2 | resultado | vencimento_final | hora | observacao |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PZ-AAAA-NNNN | C-AAAA-NNNN | AAAA-MM-DD | [nome que a pessoa disse] | o que pede; N dias (ato ou tabela); rito; dobro sim ou não; data contada, se contou | [nome, ou "2º turno"] | a mesma leitura, feita sem ver a primeira | AAAA-MM-DD | AAAA-MM-DD | bateu, divergiu ou decidida | AAAA-MM-DD, ou vazio se divergiu | HH:MM | o que divergiu, o que foi corrigido na sugestão da IA, quem decidiu |

Como preencher:

- `sugestao_ia`: o vencimento que estava em `prazos.csv` antes da conferência.
- `conta_1` e `conta_2`: os vencimentos das duas contas do script (`calcular_prazo.py --duplo`) com os dados que as pessoas confirmaram.
- `resultado`: `bateu` quando as duas leituras e as duas contas dão o mesmo; `divergiu` quando qualquer uma diferiu (o prazo fica `sugerido`); `decidida` quando a divergência foi resolvida depois, por quem a ficha diz, com a data nova conferida.
- `vencimento_final`: a data que vale. Em `divergiu`, fica vazio, e a data mais cedo vale como provisória até a decisão.
- Diferença entre `sugestao_ia` e `vencimento_final`: é uma sugestão que a pessoa corrigiu, e a `auditoria-de-prazos` conta no mês.
