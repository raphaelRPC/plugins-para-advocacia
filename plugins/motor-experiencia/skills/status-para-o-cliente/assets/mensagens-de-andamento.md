# Mensagens de andamento (modelos crus)

Use quando a biblioteca do escritório (`escritorio/04-base/relacionamento-com-o-cliente/biblioteca-de-mensagens.md`) não tiver o modelo da chave. Se tiver, o da biblioteca vale. Os textos estão num tom de exemplo e são reescritos no tom da ficha e do nicho antes de sair. Campo entre colchetes é preenchido pela habilidade (fichas, carteira, histórico); o que não se sabe sai da mensagem e vai para o cabeçalho interno "Antes de enviar", e nenhuma marcação vai ao cliente. Campo entre chaves (`{HORÁRIO}`, `{NOME DE QUEM LIGA}`) é do envio: fica no texto de propósito e quem envia preenche na hora; a fila não deixa marcar como enviado com chave no texto. Estrutura de toda mensagem de andamento: **o que aconteceu, o que significa, o que vem agora, quando o escritório volta a falar** (e, se for o caso, o que o cliente precisa fazer).

Siglas: **A**, alguém lê e envia (toda mensagem desta habilidade); **H**, uma pessoa faz (a ligação).

## Atualização de andamento
- **Chave:** `atualizacao-de-andamento` (equivale ao modelo 3 da biblioteca do `inicio-automacao`)
- **Quando:** movimentação que muda alguma coisa para o cliente (tipo M ou C do glossário), ou favorável que o advogado aprovou.
- **Quem lê:** quem acompanha o cliente; o advogado quando há decisão, valor ou data de pagamento. **Sigla:** A.
```
Oi, [NOME], tudo bem? Tenho uma novidade no seu processo.

O que aconteceu: [FATO EM UMA FRASE, SEM TERMO TÉCNICO].
O que isso quer dizer: [SIGNIFICADO PRÁTICO PARA O CLIENTE].
O que vem agora: [PRÓXIMO PASSO, SEM DATA DE DECISÃO].

[ESCOLHA UMA: "Você não precisa fazer nada agora." OU "Preciso de você para: [AÇÃO] até [DATA]."]

Volto a te falar [QUANDO: "assim que houver a próxima novidade, e no resumo do dia [DIA]" OU "até [DATA]"]. Se quiser que eu explique por ligação, me diga um horário.

[ASSINATURA]
```
- **Nunca usar quando:** a notícia é desfavorável, parcial ou pede decisão do cliente (roteiro de ligação); a decisão favorável ainda pode mudar e a mensagem comemora como se fosse definitiva.

## Nada mudou
- **Chave:** `nada-mudou` (equivale ao modelo 4)
- **Quando:** o cliente pergunta e a última movimentação é de rotina ou antiga.
- **Quem lê:** quem acompanha o cliente (etapa, data da última movimentação, de quem depende). **Sigla:** A.
```
Oi, [NOME]! Acabei de olhar o seu processo.

Hoje ele está nesta etapa: [ETAPA EM LINGUAGEM SIMPLES, EX.: "com o juiz, para ele marcar a perícia"]. A última movimentação foi em [DATA] e foi [O QUE FOI, EM PALAVRAS SIMPLES].

O que estamos esperando agora é [O QUE FALTA ACONTECER]. Esse tempo depende de [DE QUEM DEPENDE: a vara, o INSS, a outra parte], então não consigo te dar uma data, e prefiro não chutar.

[SE HOUVER LINHA DE TRABALHO DO ESCRITÓRIO NO HISTÓRICO DESDE O ÚLTIMO CONTATO: "Enquanto isso, a gente [O QUE O ESCRITÓRIO FEZ, EX.: conferiu os cálculos e pediu ao INSS a cópia do processo]." SEM LINHA, A FRASE SAI.]

Por enquanto você não precisa fazer nada. Assim que andar, eu te aviso. [SE HOUVER RÉGUA: "E no dia [DIA] você recebe o resumo do mês, como combinado."]

[ASSINATURA]
```
- **Nunca usar quando:** a pergunta vem com reclamação, aflição forte ou vontade de desistir (ligação).

## Recebi, te retorno até
- **Chave:** `recebi-retorno-ate`
- **Quando:** o cliente perguntou e ninguém olhou o processo ainda. Usa a `resposta_ponte` da ficha, se houver.
- **Quem lê:** quem atende. **Sigla:** S depois de aprovado, desde que o prazo seja o da ficha e seja cumprido.
```
Oi, [NOME]! Recebi sua mensagem. Vou olhar o seu processo com calma e te retorno até [PRAZO DA FICHA, DE resposta_ponte OU primeira_resposta_cliente_ativo, EX.: "as 16h"; SEM ELE, {ATÉ QUANDO}].
```
- **Nunca usar quando:** a mensagem traz aflição, reclamação ou sinal de risco (ligação, ou pessoa agora); o prazo não vai ser cumprido.
- **Não conta como contato:** a resposta-ponte entra no histórico, mas não muda o `ultimo_contato` da carteira.

## Convite para ligação
- **Chave:** `convite-para-ligacao` (equivale à primeira parte do modelo 8)
- **Quando:** antes da ligação de notícia ruim ou de decisão do cliente. A notícia não vai na mensagem.
- **Quem lê:** o advogado escreve ou aprova, e quem assina é quem vai ligar. **Sigla:** A.
```
Oi, [NOME], tudo bem? Aqui é {NOME DE QUEM LIGA}, do [NOME DO ESCRITÓRIO]. Teve um andamento no seu processo e eu prefiro conversar com você por telefone, para explicar com calma. Você consegue falar hoje às {HORÁRIO} ou amanhã às {HORÁRIO}?
```
- **Campos do envio:** `{NOME DE QUEM LIGA}` vem da ficha (`quem_atende`) quando ela traz o nome; `{HORÁRIO}` é o que quem vai ligar escolher. O convite não muda o `ultimo_contato`.
- **Nunca usar quando:** a mensagem leva o nome do advogado e é outra pessoa quem escreve sem dizer isso; o cliente já perguntou da notícia por escrito e a resposta "vamos conversar" sozinha deixaria ele em pânico por horas (ligue em seguida, sem esperar o horário marcado).

## Registro depois da ligação
- **Chave:** `registro-depois-da-ligacao` (equivale à segunda parte do modelo 8)
- **Quando:** logo depois da ligação, para o cliente poder reler o que foi combinado.
- **Quem lê:** o advogado que ligou. **Sigla:** A.
```
[NOME], obrigado pela conversa. Deixo aqui por escrito o que combinamos, para você poder reler:
* O que aconteceu: [RESUMO EM UMA FRASE]
* O que vamos fazer: [PRÓXIMO PASSO]
* O que preciso de você: [AÇÃO E PRAZO, OU "nada por enquanto"]
* Quando volto a te falar: [QUANDO]
Qualquer dúvida que surgir depois, me escreve aqui.
```
- **Nunca usar quando:** a ligação não aconteceu (a mensagem não substitui a conversa).

## Pedido interno ao advogado (equipe)
- **Chave:** `pedido-interno-andamento`
- **Quando:** quem atende não tem a movimentação ou a pergunta toca decisão, valor ou prazo.
- **Quem lê:** é mensagem interna, não vai ao cliente.
```
Cliente [CÓDIGO] perguntou do processo às [HORA]. Respondi "recebi, te retorno até [PRAZO]".
Preciso de: [ÚLTIMA MOVIMENTAÇÃO | SUA LEITURA DA DECISÃO | VALOR OU DATA CONFERIDOS].
Sinal na conversa: [NENHUM | ANSIOSO | INSATISFEITO | QUER DESISTIR].
```
