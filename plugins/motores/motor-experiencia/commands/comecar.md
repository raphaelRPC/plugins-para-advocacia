---
description: Liga o suporte ao cliente do escritório em cerca de 15 minutos. Até 8 perguntas para a ficha mínima e um resultado na tela, o retrato do dia de uma carteira de treino, com quem precisa de uma pessoa agora, quem está sem notícia e uma mensagem de andamento traduzida.
---

# /motor-experiencia:comecar

Você vai colocar a experiência do cliente do escritório para rodar no Claude. Siga `${CLAUDE_PLUGIN_ROOT}/docs/regras.md`: uma pergunta por vez, nada inventado, nada de dado de cliente.

Meta: no máximo 8 perguntas e um resultado visível. Não faça nada além do que está aqui.

## 1. Abertura (duas frases)

"Hoje o cliente consulta o processo sozinho e pergunta a uma IA antes de perguntar a você. Este plugin ajuda o escritório a chegar antes: vou te fazer até oito perguntas e a gente vê o dia de uma carteira de treino."

## 2. A pasta

1. Procure `escritorio/04-base/comum/`.
   - **`ficha-da-experiencia.md` existe:** não recomece. Mostre quantos campos estão preenchidos e ofereça: completar a ficha (`/motor-experiencia:ficha`), desenhar a jornada (`jornada-do-cliente`), adaptar ao nicho (`adaptar-experiencia`) ou ligar o ciclo (`rotina-da-experiencia`).
   - **Só `ficha-do-escritorio.md` existe** (outro plugin motor preencheu): leia e pule as perguntas 1 a 5.
   - **Nada existe:** pergunte se pode criar `escritorio/` aqui.
2. Crie só o que o plugin usa (`${CLAUDE_PLUGIN_ROOT}/docs/pasta.md`). Se já existir `escritorio/CLAUDE.md`, acrescente só o bloco "Experiência do cliente".
3. Sem acesso a arquivos: avise que as fichas vão no chat, para colar nas instruções de um Projeto.

## 3. As perguntas (uma de cada vez)

Ficha do escritório (modelo `${CLAUDE_PLUGIN_ROOT}/docs/ficha-do-escritorio-modelo.md`):
1. "Nome do escritório e cidade?"
2. "Em que áreas vocês atuam, e qual vocês recusam?"
3. "Quem fala com os clientes, em que horário, e quem cuida dos casos de cada área?"
4. "Vocês tratam o cliente por você, senhor e senhora, ou pelo nome? Três palavras para o jeito de vocês falarem. E como vocês assinam as mensagens?"
5. "O que é urgente de verdade com um cliente? Pense na última vez que alguém precisou de vocês na hora."

Ficha da experiência (modelo `${CLAUDE_PLUGIN_ROOT}/docs/ficha-da-experiencia-modelo.md`):
6. "Quando um cliente pergunta do processo, em quanto tempo alguém responde? E quem lê a mensagem antes de ela ir para o cliente?"
7. "Quando o processo se mexe, em quantos dias vocês avisam o cliente? E quantos dias, no máximo, ele pode ficar sem nenhuma notícia?"

Só se não souber:
8. "A IA aqui roda em conta pessoal ou profissional?" Em conta pessoal, avise que vai usar só a carteira de treino.

Todo o resto fica `[A PREENCHER]`. O `horario_da_rotina_diaria` é perguntado quando a rotina for ligada. Conte só estas perguntas: o ok das fichas e a escolha do próximo passo não contam. Mostre as duas fichas, peça ok e grave.

## 4. O resultado: o dia da carteira de treino

Use a carteira e as mensagens de `${CLAUDE_PLUGIN_ROOT}/docs/casos-ficticios.md`. Tudo grava em `escritorio/07-operacao/_treino/experiencia/`.

1. Copie a carteira de treino (`${CLAUDE_PLUGIN_ROOT}/skills/rotina-da-experiencia/assets/carteira-de-treino.csv`) para `escritorio/07-operacao/_treino/experiencia/carteira.csv` e rode o script da `rotina-da-experiencia` (`scripts/carteira.py`) com a data do caso (2026-04-10), a opção `--treino` e o `maximo_sem_noticia` que o advogado acabou de dizer.
2. Mostre o resumo do dia: PESSOA AGORA, compromissos dos próximos 7 dias, sem notícia além da régua.
3. Mostre uma única mensagem pronta: a resposta à mensagem 4 (Helena, "concluso para despacho" e a previsão do ChatGPT), pela `status-para-o-cliente` com o cuidado da `cliente-com-ia` se instalada, no tom da ficha.

Pergunte: "Alguma coisa aqui você faria diferente?". Uma correção vira um aprendizado, com o ok (`${CLAUDE_PLUGIN_ROOT}/docs/aprender-com-o-uso.md`).

## 5. Fechamento (quatro linhas)

- Pronto: ficha mínima e o retrato do dia funcionando.
- Faltam `[N]` campos `[A PREENCHER]`; o primeiro que vai fazer falta é `[CAMPO]`, na habilidade `[HABILIDADE]`.
- Próximos passos, escolha um: importar a sua carteira de verdade e ligar o ciclo diário (`rotina-da-experiencia`); a jornada e a régua por tipo de caso (`jornada-do-cliente`); o plugin ajustado ao seu nicho (`adaptar-experiencia`).
- `/motor-experiencia:status` mostra a carteira a qualquer hora.
