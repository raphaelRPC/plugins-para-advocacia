---
description: Mostra a carteira de clientes agora: quem precisa de uma pessoa, quem está sem notícia além da régua, compromissos da semana, documentos pendentes, reclamações abertas, a fila de aprovação e o quanto as fichas estão completas.
---

# /motor-experiencia:status

Mostre o estado do suporte ao cliente sem fazer perguntas desnecessárias. Siga `${CLAUDE_PLUGIN_ROOT}/docs/regras.md`.

## 1. Ler

1. As fichas (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-experiencia.md`): quantos campos preenchidos. Sem fichas, ofereça `/motor-experiencia:comecar` e pare.
2. `escritorio/07-operacao/experiencia/carteira.csv` (formato em `${CLAUDE_PLUGIN_ROOT}/docs/carteira.md`). Sem carteira, diga que ela começa com a primeira boas-vindas ou com a importação da `rotina-da-experiencia`.
3. A fila (`escritorio/07-operacao/experiencia/fila/`) e o último resumo em `rotina/`.

## 2. Mostrar

1. **Pessoa agora:** reclamação aberta, `humor = insatisfeito`, compromisso amanhã.
2. **Sem notícia além da régua:** `ultimo_contato` mais antigo que o `maximo_sem_noticia`, do mais antigo para o mais novo.
3. **Próximos 7 dias:** compromissos e contatos previstos.
4. **Documentos pendentes** além da régua de cobrança.
5. **Fila:** quantos rascunhos pendentes e o mais antigo.
6. **Carteira:** quantos clientes por fase (tabela curta).
7. **Fichas:** percentual preenchido e os três campos que mais fazem falta.

Sem números inventados: coluna vazia é dado que ainda não existe.

## 3. Sugerir

Uma linha com a ação mais importante do momento e a habilidade que cuida dela. Se o ciclo não rodou nos últimos dois dias úteis, lembre de `/motor-experiencia:ciclo`.
