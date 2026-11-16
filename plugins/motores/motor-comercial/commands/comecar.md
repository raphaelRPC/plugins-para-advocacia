---
description: Liga o comercial do escritório em cerca de 15 minutos. Até 8 perguntas para a ficha mínima e um resultado na tela, a triagem de doze mensagens de treino no jeito do escritório. O resto (mensagens, ciclo diário, nicho) fica pronto para o próximo passo.
---

# /motor-comercial:comecar

Você vai colocar o comercial do escritório para rodar no Claude. Siga `${CLAUDE_PLUGIN_ROOT}/docs/regras.md`: uma pergunta por vez, nada inventado, nada de dado de cliente.

Meta: no máximo 8 perguntas e um resultado visível. Não faça nada além do que está aqui. Tudo o mais tem o seu próprio passo depois.

## 1. Abertura (duas frases)

"As habilidades deste plugin já sabem triar, convidar para a consulta, montar proposta e fazer o retorno. Vou te fazer até oito perguntas para elas trabalharem do jeito do seu escritório, e a gente vê funcionando com mensagens de treino."

## 2. A pasta

1. Procure `escritorio/04-base/comum/`.
   - **`ficha-comercial.md` existe:** não recomece. Mostre quantos campos estão preenchidos e ofereça: completar a ficha (`/motor-comercial:ficha`), adaptar ao nicho (`adaptar-comercial`) ou ligar o ciclo (`rotina-comercial`).
   - **Só `ficha-do-escritorio.md` existe** (outro plugin motor preencheu): leia e pule as perguntas 1 a 5.
   - **Nada existe:** pergunte se pode criar `escritorio/` aqui.
2. Crie só o que o plugin usa (`${CLAUDE_PLUGIN_ROOT}/docs/pasta.md`). Se já existir `escritorio/CLAUDE.md`, acrescente só o bloco "Comercial". Se existir `escritorio/perfil.md` (plugin `inicio-automacao`), não pergunte de novo nome, áreas e conta de IA.
3. Sem acesso a arquivos: avise que as fichas vão no chat, para colar nas instruções de um Projeto.

## 3. As perguntas (uma de cada vez)

Ficha do escritório (modelo `${CLAUDE_PLUGIN_ROOT}/docs/ficha-do-escritorio-modelo.md`):
1. "Nome do escritório e cidade?"
2. "Em que áreas vocês atuam, e qual vocês recusam?"
3. "Quem responde as mensagens e em que horário?"
4. "Vocês tratam o cliente por você, senhor e senhora, ou pelo nome? E três palavras para o jeito de vocês falarem."
5. "O que é urgente de verdade para vocês? Pense na última mensagem que precisava de alguém na hora."

Ficha comercial (modelo `${CLAUDE_PLUGIN_ROOT}/docs/ficha-comercial-modelo.md`):
6. "Em quanto tempo uma pessoa responde quem escreve pela primeira vez? E quem recebe o convite e não agenda: vocês voltam a chamar? Quantas vezes, e com quantos dias entre uma e outra?" (a segunda parte preenche `follow_up` na situação `nao-agendou` e `maximo_de_retornos`; sem resposta, use 2, 7 e 15 dias e 3 retornos, marcados como exemplo a confirmar)
7. "A consulta é paga ou gratuita? Se paga, quanto, e quanto tempo dura?"

Só se não souber:
8. "A IA aqui roda em conta pessoal ou profissional?" Em conta pessoal, avise que vai usar só mensagens de treino.

Conte só estas perguntas: o ok das fichas, o "faria diferente?" e a escolha do próximo passo não contam. Da resposta 5, tire as palavras de alerta e confirme a lista numa frase. Todo o resto fica `[A PREENCHER]`. Mostre as duas fichas, peça ok e grave.

## 4. O resultado: a triagem de treino

"Agora a ficha trabalhando." Rode a `triar-contato` em modo lote com as doze mensagens de `${CLAUDE_PLUGIN_ROOT}/docs/casos-ficticios.md`, trocando as áreas do Escritório Modelo pelas do escritório quando fizer sentido.

- Tudo grava em `escritorio/07-operacao/_treino/comercial/`. Nada vai para o `contatos.csv` real.
- Mostre só a tabela do lote, com as linhas de "PESSOA AGORA" no topo. As respostas-base ficam no arquivo, não no chat.
- Destaque em uma frase cada linha que foi para uma pessoa e por quê.

Pergunte: "Alguma você classificaria diferente?". Uma correção vira um aprendizado, com o ok (`${CLAUDE_PLUGIN_ROOT}/docs/aprender-com-o-uso.md`). Se vierem várias, guarde as três mais importantes e diga que as outras entram no uso.

## 5. Fechamento (quatro linhas)

- Pronto: ficha mínima e triagem funcionando.
- Faltam `[N]` campos `[A PREENCHER]`; o primeiro que vai fazer falta é `[CAMPO]`, na habilidade `[HABILIDADE]`.
- Próximos passos, escolha um: suas mensagens no tom do escritório (`mensagens-comerciais`, modo rápido, cerca de 5 minutos); o ciclo diário rodando sozinho (`rotina-comercial`); o plugin ajustado ao seu nicho (`adaptar-comercial`).
- `/motor-comercial:status` mostra o funil a qualquer hora.
