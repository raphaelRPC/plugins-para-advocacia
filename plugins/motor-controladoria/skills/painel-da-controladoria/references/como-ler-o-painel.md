# Como o painel calcula e como ler

Leia nos passos 3 a 5 da habilidade. Sem o script (chat sem arquivos), calcule à mão com as regras da seção 1, na mesma ordem, e diga que foi à mão.

## 1. As regras de cálculo

| Parte | Regra |
|---|---|
| Em aberto | Linhas de `prazos.csv` com status `sugerido`, `conferido` ou `agendado`. Status fora da lista conta como `sugerido`, com aviso |
| Hoje ou no próximo dia útil | Segurança ou fatal até o próximo dia útil do tribunal da linha (ou já vencida) |
| Na semana | Prazos e tarefas em aberto com segurança ou fatal até N dias úteis à frente (padrão 5), incluindo os vencidos. Audiência e perícia ficam na seção delas |
| Dia útil | Sábado, domingo e os dias `feriado`, `recesso` e `suspensao` do calendário que valem para o tribunal da linha não contam. Indisponibilidade programada e expediente reduzido contam como dia útil (na dúvida, a data mais cedo). Sem calendário, só fins de semana, com aviso em destaque |
| Tribunal da linha | O da publicação ligada (`publicacao_id`); sem ela, o do número do processo |
| Carga | Por responsável: quantos em aberto por status, quantas audiências e perícias, quantos na semana. Linha sem responsável vira "sem responsável" |
| Sugerido perto do fatal | `sugerido` com a fatal em até `dias_de_seguranca + 1` dias úteis (com 2 dias de segurança, 3 dias úteis). Quer dizer: a data de segurança chegou e ninguém conferiu |
| Fatal passou | Prazo em aberto com a fatal antes de hoje: cumprido, perdido ou cancelado é a pessoa quem registra |
| Sem data | Prazo em aberto sem `vencimento`: o número de dias ou a regra não foram confirmados |
| Sem a dupla conferência | `conferido` ou `agendado` sem dois nomes em `conferido_por` (ou um nome e "2º turno") |
| Conferido sem agenda | `conferido` que ainda não virou `agendado` |
| Publicações por fonte | Total, últimos 30 dias (pela disponibilização) e não triadas; e a contagem por triagem |
| Sem caso esperando decisão | `sem-caso` com `triada_por` vazio ou `ia` |

O painel não lê o teor das publicações, não refaz conta de prazo e não muda nenhum registro.

## 2. Como escrever as leituras

Cada leitura tem um número e diz de onde ele vem. Sem causa que o dado não mostra: se a causa não está no registro, vira pergunta para a equipe.

Bom:
- "3 dos 5 prazos da semana são da advogada titular, e os 3 ainda estão `sugerido`." (carga e status)
- "2 prazos sugeridos já passaram da data de segurança sem conferência; os dois do TRT3." (risco)
- "A fonte painel trouxe 1 publicação no mês; o registro dos painéis foi feito em quantos dias úteis?" (fonte, com pergunta)

Ruim:
- "A estagiária está sobrecarregada." (causa e pessoa, sem dado)
- "Os prazos estão em dia." (sem número, e o painel não sabe disso)
- "O TRT3 é mais lento." (o painel não mede tribunal)

## 3. Como escrever as ações

Uma ação por leitura, com dono (função), até quando e a habilidade que cuida. Exemplos:

| Ação | Dono | Até | Habilidade |
|---|---|---|---|
| Dupla conferência dos 3 sugeridos do TRT3 | estagiária e advogada | hoje, 14h | `dupla-conferencia` |
| Redistribuir 2 prazos da semana | advogada titular | amanhã | (decisão da equipe; registrar em `responsavel`) |
| Combinar o horário do registro dos painéis | responsável pela controladoria | sexta | `paineis-dos-sistemas` |

## 4. O que nunca entra numa leitura

- Avaliação de pessoa ("fulano é lento"). O painel fala de prazos e de distribuição; conversa sobre desempenho é em particular, com outros dados.
- Prazo sugerido como se valesse ("a fatal do Otávio é 2026-04-30"): escreva "fatal sugerida 2026-04-30, sem dupla conferência".
- Previsão de decisão ou de resultado do processo.
- Número do processo, dado de saúde ou de criança.
