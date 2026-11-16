# Modelo do histórico do cliente

Grave em `escritorio/07-operacao/experiencia/clientes/<codigo>/historico.md`. É a tabela de quatro colunas de `docs/carteira.md` (regra 10), uma linha por registro, e todas as habilidades do plugin acrescentam linhas aqui, nunca apagam.

O histórico tem dois tipos de linha:

| Tipo | O que é | Coluna Canal | Conta como contato com o cliente? |
|---|---|---|---|
| Contato | O que foi dito ao cliente ou pelo cliente (mensagem, ligação, reunião, resumo, página) | o canal: `whatsapp`, `email`, `ligacao`, `reuniao`, `resumo`, `pagina` | Só se informou algo do caso (status, resumo, página, ligação, reunião, boas-vindas). Resposta-ponte, cortesia, lembrete de documento e pesquisa entram, mas não zeram o "sem notícia" (`docs/agentes-e-fila.md`) |
| Trabalho do escritório | O que o escritório fez pelo caso sem falar com o cliente: petição protocolada, cálculo conferido, documento pedido ao INSS, prazo cumprido, perguntas ao perito, pesquisa de jurisprudência | sempre `trabalho-do-escritorio` | Nunca. É o que a página do caso e o resumo do mês mostram em "o que fizemos" |

```markdown
---
documento: Histórico · [CÓDIGO]
versao: 1
revisado_em: AAAA-MM-DD
dono: [QUEM ACOMPANHA O CLIENTE]
---

# Histórico · [CÓDIGO] · [NOME CURTO]

| Data e hora | Canal | Quem falou | O que foi dito |
|---|---|---|---|
| 2026-03-20 17h10 | whatsapp | secretária | boas-vindas, combinado e pedido de 3 documentos até 25/03 |
| 2026-03-24 10h00 | trabalho-do-escritorio | advogada | conferiu os cálculos das verbas da rescisão |
| 2026-03-27 15h30 | trabalho-do-escritorio | advogada | protocolou a ação na Justiça do Trabalho |
| 2026-03-27 16h00 | whatsapp | secretária | avisou que a ação foi protocolada e o que vem agora |
```

Como preencher:
- **Data e hora:** `AAAA-MM-DD HHhMM`. Sem hora, só a data.
- **Quem falou:** no contato, quem falou ou escreveu (`cliente`, `advogada`, `secretária`). No trabalho do escritório, quem fez.
- **O que foi dito:** uma frase. No trabalho do escritório, um verbo no passado e o que foi feito, em palavras que o cliente entende ("pediu ao INSS a cópia do processo administrativo", "cumpriu o prazo da réplica"). Registre no dia em que fez: é a parte do trabalho que o cliente não vê no site do tribunal.

Regras:
- Uma frase, sem detalhe do processo além do necessário, sem número do processo, sem dado de saúde.
- Ligação de notícia difícil: "ligação da advogada sobre a decisão; cliente vai pensar até DD/MM", nunca o conteúdo da conversa.
- Intercorrência de saúde do cliente ou de quem fala por ele: só "intercorrência de saúde", sem detalhe.
- Cliente que pediu para não receber rotina: registre o pedido aqui, com a data, além da coluna da carteira.
- Trabalho do escritório não muda o `ultimo_contato` da carteira. Só a linha de contato que informou algo do caso muda.
