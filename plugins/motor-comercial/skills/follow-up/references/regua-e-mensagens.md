# Régua e mensagens de retorno

Mensagens-base de cada retorno, por situação. Estão em tom neutro, com tratamento por "você". A habilidade reescreve no tom e no tratamento da ficha do escritório, troca a assinatura pela `assinatura_das_mensagens` e usa o mesmo canal que a pessoa usou. Se a biblioteca comercial do escritório (`escritorio/04-base/comercial/biblioteca-comercial.md`) já tiver mensagens de retorno, valem as dela.

Dois tipos de campo: entre colchetes, o que sai da ficha quando a mensagem é escrita (`[QUEM ASSINA]`, `[ESCRITÓRIO]`, `[COMO AGENDA]`, `[ASSINATURA]`), que nunca chega ao contato como colchete; entre chaves, o campo do envio, que quem envia confere ou preenche na hora (`{NOME}`, `{ASSUNTO}`, `{DATA}`). O `revisor-comercial` aceita as chaves, e a fila não deixa marcar `enviado` enquanto houver chave no texto. No ciclo, o rascunho já sai com o nome e o assunto do registro; fica entre chaves só o que o registro não tem.

Cada mensagem tem uma **chave** fixa. É pela chave que a habilidade acha a mensagem na biblioteca do escritório, qualquer que seja o número dela lá. Com máximo maior que 3, os retornos do meio usam a mensagem do retorno 2, reescrita para não repetir a anterior.

Toda mensagem é A: uma pessoa lê e envia. Nenhuma tem orientação jurídica, promessa, prazo de decisão, desconto ou urgência.

## Como escrever um retorno

1. Uma mensagem por retorno. Curta: três a cinco linhas.
2. Abre pelo nome, lembra de onde a conversa parou, oferece ajuda e deixa a pessoa à vontade.
3. Termina com uma porta (pergunta aberta ou oferta de conversa), nunca com cobrança.
4. Horário de atendimento, dia útil. Nada de noite, domingo ou feriado.
5. Texto, sem áudio. Sem figurinha. Emoji só se a ficha disser que o escritório usa.

## 1. Não agendou depois do convite (etapa `triado`)

**Retorno 1** · chave `retorno-nao-agendou-1`
```
Oi, {NOME}, tudo bem? Aqui é [QUEM ASSINA], do [ESCRITÓRIO].
Você nos procurou sobre {ASSUNTO} e eu fiquei de te ajudar a marcar a consulta.
Se ainda fizer sentido, me diga o melhor dia e horário para você. [COMO AGENDA]
```

**Retorno 2** · chave `retorno-nao-agendou-2`
```
Oi, {NOME}. Passando só para lembrar que a gente segue à disposição para a consulta sobre {ASSUNTO}.
Se tiver alguma dúvida sobre como ela funciona, é só perguntar por aqui.
```

**Encerramento** · chave `encerramento-nao-agendou`
```
Oi, {NOME}. Como não tivemos retorno, imagino que agora não seja o momento, e está tudo bem.
Não vou mais te mandar mensagem sobre isso.
Se um dia precisar, é só escrever aqui.
[ASSINATURA]
```

## 2. Faltou à consulta (etapa `nao-compareceu`)

**Retorno 1 (no dia da consulta perdida ou no seguinte)** · chave `retorno-faltou-1`
```
Oi, {NOME}, tudo bem? Hoje era o horário da nossa consulta e não conseguimos nos falar.
Espero que esteja tudo bem com você.
Se quiser remarcar, me diga o melhor dia e horário. [COMO AGENDA]
```

Se a consulta era paga e já foi paga, a regra de remarcação vem do campo `remarcacao` da ficha comercial. Sem o campo, pergunte ao advogado antes de escrever. A mensagem não fala de multa nem de perda do valor; isso, se existir, é assunto de uma pessoa.

**Retorno 2** · chave `retorno-faltou-2`
```
Oi, {NOME}. Ficamos à disposição para remarcar a consulta quando for melhor para você.
É só responder aqui com um dia e um horário.
```

**Encerramento** · chave `encerramento-faltou`
```
Oi, {NOME}. Como não conseguimos remarcar, imagino que agora não seja o momento.
Não vou mais te mandar mensagem sobre a consulta.
Se quiser retomar, é só escrever aqui.
[ASSINATURA]
```

## 3. Proposta sem resposta (etapas `proposta-enviada` e `negociando`)

**Retorno 1** · chave `retorno-proposta-1`
```
Oi, {NOME}, tudo bem? Passando para saber se a proposta chegou certinho e se ficou alguma dúvida.
Se quiser, te explico qualquer parte por aqui ou numa ligação rápida.
```

**Retorno 2** · chave `retorno-proposta-2`
```
Oi, {NOME}. Sei que é uma decisão que leva tempo.
Se ajudar, posso te mandar um resumo curto da proposta ou conversar com você e com quem for decidir junto.
```

Se a validade estiver perto e for verdadeira, acrescente uma linha, uma vez: "A proposta vale até {DATA DE VALIDADE}. Depois disso, a gente atualiza com você, sem problema."

**Encerramento** · chave `encerramento-proposta`
```
Oi, {NOME}. Como não tivemos retorno, imagino que este não seja o momento, e está tudo bem.
Não vou mais te mandar mensagem sobre a proposta.
Se um dia quiser retomar, é só escrever aqui que a gente atualiza a proposta com você.
[ASSINATURA]
```

## 4. Quando a pessoa responde

**"Agora não, me chama em tal data"** · chave `resposta-retorno-combinado`
```
Combinado, {NOME}. Te escrevo em {DATA}. Até lá, se precisar, é só chamar.
```

**"Fechei com outro escritório" ou "desisti"** · chave `resposta-despedida`
```
Obrigado por avisar, {NOME}. Desejo que dê tudo certo.
Se um dia precisar, as portas estão abertas.
```
Sem perguntar por quê, sem comentar o outro escritório, sem contraproposta.

**"Não quero mais receber mensagem"** · modelo `confirmacao-parar` da biblioteca comercial (da `mensagens-comerciais`); sem biblioteca:
```
Tudo bem, {NOME}. Não vamos mais te mandar mensagens. Obrigado por avisar.
```
Uma vez só. Depois disso, `pediu_para_parar = sim` e nada mais.

**Respondeu com objeção ("achei caro", "vou pensar")**: a régua pausa e a resposta sai pela `objecoes-comerciais` (se instalada). Se não estiver, mostre a mensagem ao advogado antes de responder.

## 5. Casos-limite

| Caso | O que fazer |
|---|---|
| Contato com vulnerabilidade (idoso sem renda, doença grave) | Fora da régua. Uma pessoa decide se e como retomar, de preferência por ligação. |
| Urgência alta com pessoa designada (benefício cortado, como o caso 1) | Entra na régua. Quem cuida lê com atenção e decide se liga em vez de escrever. |
| Relato de violência, ameaça ou risco (como o caso 3 dos fictícios) | Fora da régua. Nenhuma mensagem pronta. O advogado decide se e como retomar. |
| Área que o escritório não atende (como o caso 4) | Fora da régua. O encaminhamento já foi feito por uma pessoa; não há retorno de venda. |
| Sem primeira resposta (`primeira_resposta` vazia) | O convite nunca saiu. Mande o convite primeiro; o retorno não conta. |
| Quem escreveu foi um parente pelo titular (filho pela mãe) | O retorno vai para quem escreveu, sem detalhe do caso além do que ele mesmo contou. |
| O advogado viu na consulta um prazo que a pessoa pode perder | Esse aviso é do advogado, uma vez, por escrito e factual. Nunca vira modelo nem gatilho de retorno. |
| A pessoa respondeu num canal diferente | A conversa segue no canal novo; atualize `canal` se o advogado quiser. |
| Dois retornos vencem no mesmo dia para a mesma pessoa (duas propostas) | Uma mensagem só, sobre as duas. |
| Retorno caiu num fim de semana ou feriado | Sai no próximo horário de atendimento. A régua continua em dias corridos: o script mostra o atraso e calcula a data seguinte a partir do fato, ou do envio se já passou. |

## 6. O que nunca escrever

| Nunca | Por quê | No lugar |
|---|---|---|
| "Última chance" | Escassez falsa | "Se um dia quiser retomar, é só escrever." |
| "Você sumiu!" | Culpa | "Como não tivemos retorno..." |
| "As vagas estão acabando" | Gatilho de urgência | Nada. A agenda não entra no retorno. |
| "Consigo um desconto se fechar esta semana" | Desconto como isca | Nada. Valor muda só com o advogado, pela `objecoes-comerciais`. |
| "Seu caso pode prescrever, corre!" | Medo e orientação a quem não é cliente | Aviso do advogado, se for o caso, uma vez e factual. |
| "Só mais uma mensagem..." depois do encerramento | Quebra o que foi dito | Nada. O encerramento é o fim. |
| Áudio de retorno | A pessoa não escolheu ouvir | Texto curto. |

## 7. Registro de cada passo

| Momento | `proximo_passo` | `data_proximo_passo` |
|---|---|---|
| Régua começa (a triagem arma) | retorno 1 de [M] | data do fato + dias do retorno 1, em dias corridos |
| Retorno 1 enviado | retorno 2 de [M] | data do fato + dias do retorno 2 (o script calcula na coluna "Depois do envio") |
| Encerramento enviado | confirmar perdido | data do envio + prazo para o advogado decidir (exemplo: 7 dias corridos) |
| Advogado confirma | nenhum | vazio; `etapa = perdido`, `motivo_perda` |
| Pessoa pediu tempo | retorno combinado | a data que ela deu |
| Pessoa pediu para parar | nenhum | vazio; `pediu_para_parar = sim` |
