# Mensagens depois do caso

Textos de partida, no tom de exemplo ("você", sem juridiquês). Antes de usar, reescreva no tom da ficha e do nicho (modo adaptar). Toda mensagem é A: alguém lê antes de enviar. Nenhuma oferece serviço. Campos entre colchetes são preenchidos pela habilidade (fichas, encerramento, carteira). Campos entre chaves (`{SEU NOME}`, `{LINK DA AVALIAÇÃO}`) são do envio: quem envia preenche na hora, e a fila não deixa marcar como enviado com chave no texto. O nome de quem escreve sai de `quem_atende`, na ficha do escritório, quando ela traz.

## 1. Mensagem anual

Chave: `mensagem-anual`. Quando: a data combinada no encerramento ou na ficha.

```
Oi, [NOME]! Aqui é {SEU NOME}, do [ESCRITÓRIO].

Faz um ano que o seu caso terminou, e eu quis passar para saber como você está.

Uma lembrança que vale para o seu caso: [UMA LINHA DO "O QUE MUDA", conferida no encerramento, ex.: "se o pagamento da pensão atrasar, fale com a gente"].

Nosso número continua o mesmo. Se precisar, é só escrever.

Se preferir não receber esta mensagem, é só me dizer.
[ASSINATURA]
```

Nunca: "aproveite", "temos uma novidade para você", "agora também atendemos", "que tal revisar".

## 2. Aviso de mudança que pode afetar o cliente

Chave: `aviso-de-mudanca`. Só depois de o advogado conferir a mudança e confirmar que ela pode afetar esta pessoa. O rascunho leva o cabeçalho interno abaixo; o script de .docx não se aplica (é mensagem), mas a regra é a mesma: a conferência fica fora do texto do cliente.

```markdown
## Antes de enviar (interno, não vai para o cliente)

- [ ] A mudança: [O QUE MUDOU] · fonte: [NORMA OU ATO OFICIAL, pelo nome] · vale a partir de [DATA] `[CONFERIR]`
- [ ] Esta pessoa pode ser afetada porque [MOTIVO], conferido pelo advogado `[CONFERIR]`
- [ ] O texto não diz "você tem direito", não oferece ação, não cria urgência que não existe
- [ ] Quem lê e aprova: [FUNÇÃO]

<!-- fim: antes de enviar -->
```

```
Oi, [NOME]! Aqui é {SEU NOME}, do [ESCRITÓRIO].

Estou escrevendo porque [A MUDANÇA, EM UMA FRASE SIMPLES] a partir de [DATA].

Isso pode ter relação com o seu caso de [TIPO DE CASO], ou pode não mudar nada para você. Se quiser entender melhor, é só responder aqui que a gente conversa.

[SE FOR O CASO: Atenção: o [ÓRGÃO] não pede senha nem pagamento por mensagem ou link. Na dúvida, fale com a gente antes de clicar.]

Se preferir não receber este tipo de aviso, é só me dizer.
[ASSINATURA]
```

## 3. Quem voltou a escrever

Chave: `ex-cliente-voltou`.

Dúvida sobre o caso antigo:
```
Oi, [NOME]! Que bom ter notícia sua. Recebi a sua dúvida sobre [ASSUNTO] e a [FUNÇÃO] te responde até [PRAZO].
```

Caso novo (passa para o comercial; sem orientação por mensagem):
```
Oi, [NOME]! Obrigada por lembrar da gente. Para eu entender direitinho o que está acontecendo, o melhor é uma conversa. [COMO AGENDAR, da ficha comercial ou do escritório].
```

## 4. Quando o ex-cliente fala em indicar

Chave: `resposta-indicacao`. Só como resposta, nunca como pedido.

```
Obrigada pela confiança, [NOME]. Se a sua [AMIGA, VIZINHA, PARENTE] quiser, ela pode falar com a gente por este número ou por [CANAL OFICIAL].
```

Nunca: pedir o telefone da pessoa indicada, o escritório procurar a pessoa, oferecer desconto, brinde ou qualquer vantagem pela indicação.

## 5. Quem pede para parar

Chave: `confirmacao-parar`.

```
Combinado, [NOME]. Não mando mais mensagens. Se um dia precisar, o número continua o mesmo.
```

Depois: `pediu_para_nao_receber = sim` na carteira, com o ok.

## 6. Pedido de avaliação

Só se `pede_avaliacao_publica` disser e o pedido não tiver sido feito no encerramento. Use o texto `pedido-de-avaliacao` da `pesquisa-de-satisfacao` (se instalada). Sem ela:

```
[NOME], se você quiser contar como foi a sua experiência com o escritório, pode deixar uma avaliação aqui: {LINK DA AVALIAÇÃO}. É totalmente opcional, e o que você escrever é seu.
```

Uma vez só. As regras estão em `../references/limites-eticos.md`.
