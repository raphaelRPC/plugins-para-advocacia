# Mensagens de encerramento

Textos de partida, no tom de exemplo ("você", sem juridiquês). Antes de usar, reescreva no tom da ficha e do nicho (modo adaptar). Campos entre colchetes são preenchidos pela habilidade, com a prestação de contas conferida, a carteira e o histórico. Campos entre chaves são do envio: ficam no texto de propósito, quem envia preenche na hora (o dia que consegue cumprir, o horário escolhido), e a fila não deixa marcar como enviado com chave no texto. Toda mensagem aqui é A: alguém lê antes de enviar. Nenhuma leva valor que não esteja na prestação de contas conferida.

Chaves na biblioteca do escritório (`04-base/relacionamento-com-o-cliente/biblioteca-de-mensagens.md`): `encerramento-resultado-bom`, `encerramento-depois-da-ligacao`, `encerramento-troca-de-advogado`, `encerramento-resposta-ponte`.

## 1. Resposta-ponte (o cliente perguntou antes de a prestação de contas ficar pronta)

Chave: `encerramento-resposta-ponte`. Quando: o cliente pergunta quanto recebe ou quando. Sigla: A.

```
Oi, [NOME]! Recebi sua pergunta. Você vai ter tudo por escrito.

A [FUNÇÃO] está fechando a prestação de contas, com o valor que entrou, a parte do escritório, as despesas e o que vai para você.

Até {DIA} eu te mando.
```

Nunca: adiantar valor "aproximado", dizer "fica uns 70% para você", prometer data de depósito que ninguém confirmou.

## 2. Resultado bom, com a prestação de contas

Chave: `encerramento-resultado-bom`. Quando: o caso terminou bem e a prestação de contas está PRONTA PARA ENVIAR. Sigla: A.

```
Oi, [NOME]! Seu caso chegou ao fim, e eu queria te mandar tudo organizado.

Em anexo está a prestação de contas: o que entrou, o que fica com o escritório, as despesas e o valor que vai para você, até [DATA DO REPASSE].

Nela também estão os seus documentos (o que volta para você e o que fica guardado com a gente) e o que muda para você daqui para a frente.

Se quiser, a gente marca uma conversa rápida para passar por tudo junto. É só me dizer o melhor horário.

Foi um prazer cuidar do seu caso.
[ASSINATURA]
```

## 3. Depois da ligação (resultado parcial ou ruim)

Chave: `encerramento-depois-da-ligacao`. Quando: o advogado já conversou com o cliente. A mensagem registra o que foi dito, sem repetir a notícia com detalhe. Sigla: A, lida pelo advogado.

```
Oi, [NOME]. Obrigada pela conversa de [DIA].

Como falamos, [UMA FRASE NEUTRA SOBRE O QUE FOI DECIDIDO, ex.: "o caso termina aqui, sem recurso, como você decidiu"].

Em anexo está a prestação de contas, com os valores e os seus documentos. Se surgir qualquer dúvida sobre ela, me escreve aqui.

[ASSINATURA]
```

Nunca: "infelizmente perdemos" sem ligação antes; culpar o juiz ou a outra parte; mencionar recurso como venda.

## 4. Troca de advogado ou desistência

Chave: `encerramento-troca-de-advogado`. Quando: o cliente decidiu seguir com outro advogado ou parar. Sigla: A, lida pelo titular.

```
Oi, [NOME]. Respeitamos a sua decisão.

Para você seguir sem prejuízo, separamos:
1. os seus documentos originais, para [COMO ENTREGAR];
2. a prestação de contas, em anexo;
3. [SE FOR O CASO: as informações que o novo advogado vai precisar, que entregamos a ele quando você autorizar].

Qualquer dúvida sobre esses pontos, é só falar com a gente.
[ASSINATURA]
```

O que o escritório precisa fazer para a troca (substabelecimento, renúncia, comunicação ao juízo) é decisão do advogado `[CONFERIR]`, fora desta mensagem.

## 5. Roteiro da reunião de encerramento (15 a 20 minutos)

Quando o cliente prefere conversar, ou quando o caso foi longo. Sigla: H, com o material preparado pela IA.

1. **Abrir:** agradecer e dizer o objetivo ("fechar tudo direitinho e te deixar seguro do que vem").
2. **O caso em três frases:** como começou, o que o escritório fez, como terminou.
3. **Os valores:** passar pela tabela da prestação de contas, linha por linha, e perguntar se ficou alguma dúvida.
4. **Quando e como recebe:** a data do repasse e a conta confirmada (por voz, nunca pedindo número por mensagem).
5. **O que muda:** os itens conferidos, um por um.
6. **Documentos:** entregar os originais ou combinar a entrega; dizer o que fica guardado e por quanto tempo.
7. **Depois:** "Podemos te mandar uma mensagem por ano e te avisar se alguma mudança de lei afetar você?" Anotar a resposta. Pesquisa, se a ficha prevê: avisar que vai chegar.
8. **Fechar:** porta aberta e o aviso contra golpe ("nunca pedimos depósito para liberar valor").

Depois da reunião: registrar no `encerramento.md` e no `historico.md`.
