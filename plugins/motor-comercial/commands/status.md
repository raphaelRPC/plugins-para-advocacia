---
description: Mostra o funil do escritório agora: contatos por etapa, o que está sem resposta, consultas e retornos do dia, propostas abertas e o quanto a ficha está completa.
---

# /motor-comercial:status

Mostre o estado do comercial sem fazer perguntas desnecessárias. Siga `${CLAUDE_PLUGIN_ROOT}/docs/regras.md`.

## 1. Ler

1. `escritorio/04-base/comum/ficha-do-escritorio.md` e `escritorio/04-base/comum/ficha-comercial.md`: quantos campos preenchidos e quantos `[A PREENCHER]`. Sem ficha, ofereça `/motor-comercial:comecar` e pare.
2. `escritorio/07-operacao/comercial/contatos.csv` (formato em `${CLAUDE_PLUGIN_ROOT}/docs/funil.md`). Sem registro, diga que o funil começa a aparecer depois da primeira triagem e ofereça `triar-contato`.
3. O último arquivo de `escritorio/07-operacao/comercial/rotina/`, se houver.

## 2. Mostrar

1. **Agora:** contatos em `novo` ou `triado` sem próximo passo, com o tempo desde a entrada, comparado ao prazo de `primeira_resposta_contato_novo` da ficha. Urgência alta primeiro.
2. **Hoje:** `data_proximo_passo` igual a hoje ou vencida, por responsável.
3. **Funil:** quantos em cada etapa (tabela curta, só etapas com contato).
4. **Propostas abertas:** código, nome curto, valor, dias desde o envio, próximo retorno.
5. **Ficha:** percentual preenchido e os três campos que mais fazem falta, pela tabela de `${CLAUDE_PLUGIN_ROOT}/docs/ficha-comercial.md`.

Sem números inventados: se uma coluna estiver vazia no registro, diga que o dado não existe ainda.

## 3. Sugerir

Uma linha com a ação mais importante do momento e a habilidade que cuida dela. Se o registro mostra que a rotina diária não rodou nos últimos dias, lembre da `rotina-comercial`.
