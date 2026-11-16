---
description: Mostra a controladoria agora: o que vence hoje, amanhã e na semana, prazos esperando a dupla conferência, publicações não triadas, audiências e perícias próximas, prazos sem responsável e a situação da tabela de regras e dos calendários.
---

# /motor-controladoria:status

Mostre o estado da controladoria sem fazer perguntas desnecessárias. Siga `${CLAUDE_PLUGIN_ROOT}/docs/regras.md` e `${CLAUDE_PLUGIN_ROOT}/docs/prazos.md`.

## 1. Ler

1. As fichas (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-controladoria.md`). Sem fichas, ofereça `/motor-controladoria:comecar` e pare.
2. `escritorio/07-operacao/controladoria/prazos.csv` e `publicacoes.csv`. Sem registro, diga que ele começa com a primeira captação.
3. Rode o script da rotina, que faz as contas: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/rotina-da-controladoria/scripts/pendencias_controladoria.py" escritorio/07-operacao/controladoria/prazos.csv --publicacoes escritorio/07-operacao/controladoria/publicacoes.csv --data <hoje>`. Se a variável não aparecer expandida, use a pasta do plugin.
4. A fila (`07-operacao/controladoria/fila/`) e o último resumo em `rotina/`.
5. A tabela de regras (`04-base/controladoria/regras-de-contagem.md`) e os calendários (`04-base/controladoria/calendario/`).

## 2. Mostrar

1. **Pessoa agora:** prazo com data de segurança ou fatal hoje ou no próximo dia útil, em qualquer status; prazo que começou a correr antes de ser captado; publicação `urgente` ou `sem-caso` sem decisão.
2. **Vence na semana** (tabela curta: caso, providência, segurança, fatal, responsável e o status por extenso, com `sugerido` em destaque: ainda não vale).
3. **Dupla conferência:** prazos `sugerido`, o mais antigo primeiro, e os que têm divergência.
4. **Publicações:** não triadas, por fonte, e a data da última captação.
5. **Audiências e perícias** dos próximos 15 dias.
6. **Sem responsável** e **sem agenda** (`conferido` que não virou `agendado`).
7. **Base:** tabela de regras validada ou não (por quem e quando), tribunais da ficha sem calendário do ano, painéis que ninguém registrou hoje.
8. **Fichas:** percentual preenchido e os três campos que mais fazem falta.

Sem números inventados: coluna vazia é dado que ainda não existe. Treino (`_treino/`) não entra.

## 3. Sugerir

Uma linha com a ação mais importante do momento e a habilidade que cuida dela. Se o ciclo não rodou hoje até o `horario_da_captacao` da ficha, lembre de `/motor-controladoria:ciclo`.
