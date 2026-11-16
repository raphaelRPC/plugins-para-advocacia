# Mensagens de boas-vindas (modelos crus)

Use quando a biblioteca do escritório (`escritorio/04-base/relacionamento-com-o-cliente/biblioteca-de-mensagens.md`) não tiver o modelo da chave. Se tiver (no plugin `inicio-automacao`, `boas-vindas-cliente` é o modelo 1), o da biblioteca vale, e esta habilidade só completa os campos. Os textos estão num tom de exemplo e são reescritos no tom da ficha e do nicho antes de sair.

Campos entre colchetes são preenchidos pela habilidade com as fichas, a passagem e a jornada. Campo que não se sabe sai da mensagem (a linha inteira) e vai para "Em aberto" na abertura. Nenhuma marcação `[A PREENCHER]`, `[A DEFINIR]` ou `[CONFERIR]` vai ao cliente.

Campos entre chaves (`{SEU NOME}`, `{TELEFONE OFICIAL}`) são do envio: ficam no texto de propósito e quem envia preenche na hora. O nome de quem escreve e o telefone saem da ficha do escritório (`quem_atende`, `canais`) quando estão lá; só quando não estão ficam entre chaves. A fila não deixa marcar como enviado com chave no texto.

Siglas: **S**, texto aprovado sai sem leitura a cada envio; **A**, alguém lê e envia; **H**, uma pessoa faz.

## 1. Versão em uma mensagem
- **Chave:** `boas-vindas-cliente`
- **Quando:** no dia em que o contrato foi assinado, para caso simples ou cliente que prefere uma mensagem só.
- **Quem lê:** quem atende, conferindo os campos. **Sigla:** S depois de aprovado (não traz conteúdo do processo).
```
Oi, [NOME]! Aqui é {SEU NOME}, do [NOME DO ESCRITÓRIO]. Seja bem-vindo(a).

A partir de agora este é o canal oficial do escritório para falar do seu caso. Algumas combinações para você saber como a gente trabalha:

* Atendemos [HORÁRIO DE ATENDIMENTO]. Mensagem fora desse horário é respondida [QUANDO].
* Você recebe resposta em até [PRAZO DE RESPOSTA AO CLIENTE].
* [RÉGUA DA JORNADA OU DA FICHA: "Todo mês, até o dia [DIA], você recebe um resumo do seu caso, mesmo quando não houver novidade." OU "Quando acontecer algo importante, a gente te avisa antes de você precisar perguntar."]
* Assunto que pede conversa, a gente liga.

Quem cuida do seu caso é [ADVOGADO RESPONSÁVEL]. [SE HOUVER: "No dia a dia, quem fala com você é [FUNÇÃO OU PRIMEIRO NOME]."]

[ASSINATURA]
```

## 2. Versão em três mensagens

Para caso com documentos pendentes ou com mais de um próximo passo. Envie as três no mesmo dia, nesta ordem, uma depois da outra.

### 2.1 Boas-vindas e quem cuida
- **Chave:** `boas-vindas-quem-cuida` · **Sigla:** S depois de aprovado
```
Oi, [NOME]! Aqui é {SEU NOME}, do [NOME DO ESCRITÓRIO]. Seja bem-vindo(a), e obrigado pela confiança.

Quem cuida do seu caso é [ADVOGADO RESPONSÁVEL]. [SE HOUVER: "No dia a dia, quem fala com você sou eu, [PRIMEIRO NOME], e quando eu não estiver, [SUBSTITUTO]."]

Vou te mandar em seguida como a gente se comunica e os próximos passos.
```

### 2.2 Como a gente se comunica
- **Chave:** `boas-vindas-combinado` · **Sigla:** S depois de aprovado
```
Como a gente se comunica:

* Canal oficial: [CANAL, EX.: "este WhatsApp" OU "o e-mail do escritório", DE `canais`]. Assunto do seu caso, só por aqui.
* Telefone do escritório: [TELEFONE DE `canais`, POR EXTENSO; SEM ELE, {TELEFONE OFICIAL}]. Se alguém pedir dinheiro, senha ou código em nosso nome, não responda e ligue para esse número.
* Horário: [HORÁRIO DE ATENDIMENTO]. Fora dele, a resposta vem [QUANDO].
* Resposta: em até [PRAZO DE RESPOSTA AO CLIENTE].
* Notícias do caso: [RÉGUA DO ESCRITÓRIO, EX.: "a gente avisa sempre que algo importante acontecer e, todo mês, até o dia 5, você recebe um resumo"].
* Urgência: [O QUE É URGENTE E O QUE FAZER, DA FICHA].
* Ligação: assunto que pede conversa, a gente liga. [SE A FICHA DISSER: "Áudio só se você preferir; notícia importante vai sempre por escrito também."]
```

### 2.3 Próximos passos e documentos
- **Chave:** `boas-vindas-proximos-passos` · **Sigla:** A (quem acompanha confere a lista e as datas)
```
Próximos passos:

1. [O QUE O ESCRITÓRIO FAZ PRIMEIRO, EM PALAVRAS SIMPLES, EX.: "preparar o pedido inicial"], até [DATA COMBINADA PELO ESCRITÓRIO].
2. [O QUE VEM DEPOIS, SEM DATA DE DECISÃO].

O que eu preciso de você:
1. [DOCUMENTO]: [O QUE É]. Você consegue em [ONDE CONSEGUIR].
2. [DOCUMENTO]: [O QUE É]. Você consegue em [ONDE CONSEGUIR].

Pode mandar por aqui mesmo, em foto com boa luz ou em PDF. Consegue até [DATA]? Se tiver dificuldade com algum, me fala que a gente resolve junto.
```
Sem documento pendente: troque o bloco "O que eu preciso de você" por "Por enquanto você não precisa mandar nada."

## 3. Cliente que já era cliente, caso novo
- **Chave:** `boas-vindas-caso-novo`
- **Quando:** cliente com outro caso no escritório, ou cliente antigo que nunca recebeu o combinado (por exemplo, depois da importação da carteira).
- **Quem lê:** quem acompanha. **Sigla:** A.
```
Oi, [NOME]! Que bom falar com você de novo.

[SE CASO NOVO: "A partir de agora a gente também cuida de [TIPO DE CASO EM PALAVRAS SIMPLES]." SE CLIENTE ANTIGO: "Queria deixar combinado, por escrito, como você fica sabendo do seu caso daqui para frente."]

* Você recebe resposta em até [PRAZO DE RESPOSTA AO CLIENTE], [HORÁRIO DE ATENDIMENTO].
* [RÉGUA DA JORNADA OU DA FICHA].
* Assunto que pede conversa, a gente liga.

Quem cuida é [ADVOGADO RESPONSÁVEL]. [SE HOUVER PRÓXIMO PASSO: "O próximo passo é [O QUE O ESCRITÓRIO FAZ], até [DATA]."]

[ASSINATURA]
```

## 4. Variações

| Situação | O que muda |
|---|---|
| Cliente idoso ou com pouca familiaridade com o celular | Boas-vindas por ligação (H), com a mesma pauta. Depois, só a mensagem 2.3, curta, para ele poder reler. Pergunte se ele quer que alguém de confiança receba as mensagens junto, e registre quem, com a autorização dele. |
| Empresa | Por e-mail, se a ficha disser. Pergunte quem na empresa é o contato do escritório e quem mais pode receber informação do caso. Acrescente como a empresa manda documentos (pasta compartilhada, e-mail). |
| Família, com qualquer sinal de violência ou de conflito em casa | Antes de qualquer mensagem, o advogado confirma com o cliente qual canal é seguro e se alguém mais lê aquele celular. Mensagem curta, sem detalhe do caso, sem nome da outra parte. Nada de resumo automático sem o ok do advogado. |
| Alguém fala pelo cliente (filho pelo pai, por exemplo) | Confirme com o próprio cliente, por escrito ou na ligação, que aquela pessoa pode receber informação do caso. Registre na abertura. |
| Cliente que já era cliente (caso novo) | Pule a 2.2 se o combinado não mudou. Use a chave `boas-vindas-caso-novo` e, se houver documento, a 2.3. |
| Escritório sem régua definida (sem jornada e sem campo na ficha) | Nada de prometer resumo mensal. A linha de notícias diz só o que o escritório cumpre hoje, e a régua fica `[A DEFINIR]` na abertura, em "Em aberto". |
