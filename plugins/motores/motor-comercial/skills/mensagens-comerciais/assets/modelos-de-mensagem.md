# Modelos crus da biblioteca comercial

Ponto de partida da `mensagens-comerciais`. São as mensagens para **quem ainda não é cliente**: do primeiro contato ao envio da proposta. Mensagens de cliente ativo (boas-vindas ao cliente, andamento, documentos do caso, resumo do mês) ficam na biblioteca do motor-experiencia, não aqui.

Os textos estão num tom de exemplo (você, frases curtas, sem juridiquês) e **não valem como estão**: a habilidade reescreve cada um no tom das fichas antes de mostrar.

Dois tipos de campo, com duas marcas diferentes:

| Marca | O que é | Quem preenche | Pode ficar no texto aprovado? |
|---|---|---|---|
| `[NOME DO ESCRITÓRIO]`, `[DURAÇÃO]`, `[COMO AGENDA]` (colchetes, maiúsculas) | Campo fixo do escritório, que sai da ficha. Também as instruções de montagem, como `[SE ABATE: "..."]` e `[DA ATA: ...]` | A habilidade, quando escreve a biblioteca | Não. Na biblioteca aprovada, já vem preenchido. Se a ficha não tem o campo, a linha sai e a pendência vai para o "Antes de enviar" |
| `{NOME}`, `{DIA E HORA}`, `{LINK}` (chaves, maiúsculas) | Campo do envio: o que muda a cada conversa e quem envia escolhe de propósito (o nome, o horário escolhido na agenda, o link da videochamada) | Quem envia, na hora de enviar | Sim. O `revisor-comercial` aceita, e a fila não deixa marcar `enviado` enquanto houver chave no texto (`regras.md`, seção 3) |

Cada modelo tem uma **chave fixa**. É pela chave que as outras habilidades e o agente do ciclo acham o modelo, qualquer que seja o número dele no arquivo do escritório. A chave nunca muda, nem quando o texto é reescrito.

Cada modelo tem também um **"Antes de enviar (interno)"**: o que quem envia confere. Essa parte nunca vai para o contato. Nenhuma marcação `[A PREENCHER]`, `[A DEFINIR]`, `[A CONFIRMAR]` ou `[CONFERIR]` fica no texto-modelo: se a ficha não tem o campo, a pendência vai para o "Antes de enviar" e o modelo não sai até alguém preencher. Cada modelo lista também os **campos do envio**, para quem envia saber o que preencher.

Sigla: tudo o que sai para o contato é **A** (alguém aprova). Os modelos 2 e 16 são aprovados uma vez e saem pela ferramenta do canal sem leitura a cada envio, com conferência por amostra, porque não têm conteúdo jurídico. Os caminhos "pessoa agora" e "pessoa liga" da triagem são **H** e não têm modelo.

---

## Cabeçalho da biblioteca (quando o arquivo ainda não existe)

```markdown
---
documento: Biblioteca comercial
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO DE QUEM APROVA MUDANÇAS]
---

# Biblioteca comercial · [NOME DO ESCRITÓRIO]

Mensagens aprovadas para quem ainda não é cliente, no tom do escritório. A IA parte daqui para responder. Cada modelo tem uma chave fixa. Mudança no texto passa pelo dono e entra em "Mudanças", no fim.

## Regras para todas as mensagens

- Tom, tratamento e assinatura: os das fichas.
- Curta, uma ideia por parágrafo. O contato lê no celular.
- Nenhuma mensagem promete resultado, prazo de decisão ou chance, nem diz valor de ação.
- Quem ainda não é cliente não recebe orientação jurídica por mensagem: recebe o convite para a consulta.
- Mensagem automática diz que é automática e quando uma pessoa assume. Nunca usa o nome do advogado como se fosse ele digitando.
- Nada de urgência falsa, escassez ou desconto como isca.
- Violência, ameaça, criança em risco, risco à vida: nenhum modelo. Uma pessoa assume.
- "Antes de enviar" é interno. Nunca vai para o contato.
```

---

## Modelo 1 · Boas-vindas ao contato novo
- **Chave:** `boas-vindas-contato-novo`
- **Quando usar:** primeira resposta a quem escreveu pela primeira vez, dentro do horário, quando ainda não dá para mandar o convite (falta entender o que a pessoa precisa).
- **Quem lê antes de enviar:** quem faz o primeiro contato (`quem_atende`). **Sigla:** A.
- **Campos fixos:** nome do escritório, `primeira_resposta_contato_novo`, assinatura.
- **Antes de enviar (interno):** a mensagem que chegou não tem sinal de parada imediata; o prazo prometido é o da ficha.
- **Campos do envio:** `{NOME}`.
- **Texto-modelo:**
  ```
  Oi, {NOME}, tudo bem? Aqui é [QUEM ESTÁ FALANDO, DA FICHA, EX.: "o atendimento"] do [NOME DO ESCRITÓRIO]. Obrigado por escrever.

  Para eu te encaminhar certo, me conte em poucas linhas o que aconteceu e se existe alguma data marcada, como audiência, perícia ou prazo.

  [ASSINATURA]
  ```
- **Nunca usar quando:** há sinal de violência, ameaça, criança em risco ou risco à vida; a pessoa já disse o que precisa (vá direto ao convite).

## Modelo 2 · Fora do horário
- **Chave:** `fora-do-horario`
- **Quando usar:** mensagem que chega fora do `horario_de_atendimento`. Automática da ferramenta do canal, se ela tiver, ou enviada pela primeira pessoa que abrir o canal.
- **Quem lê antes de enviar:** aprovada uma vez pelo dono da biblioteca; conferida por amostra. **Sigla:** A.
- **Campos fixos:** nome do escritório, horário, quando uma pessoa responde, `urgencia_vai_para` (só se for um caminho que o contato consegue usar fora do horário), números de emergência da seção 5 de `regras.md`.
- **Antes de enviar (interno):** confira os números de emergência vigentes na região do escritório `[CONFERIR]`. Confira se `urgencia_vai_para` é um caminho que o contato pode usar (plantão, telefone de urgência). Se o caminho é interno ("ligação para o celular do advogado"), ele não entra no texto: vale a versão sem plantão. Nunca escreva "escreva URGENTE" se ninguém lê o canal fora do horário.
- **Campos do envio:** nenhum (texto fixo da automática).
- **Texto-modelo (com plantão de verdade):**
  ```
  Olá! Esta é uma mensagem automática do [NOME DO ESCRITÓRIO].

  Nosso atendimento é [HORÁRIO DE ATENDIMENTO]. Sua mensagem ficou registrada, e uma pessoa da equipe responde [QUANDO, EX.: "no próximo dia útil, a partir das 9h"].

  Se for urgente, como [EXEMPLOS DE O_QUE_E_URGENTE], [CAMINHO DA FICHA, EX.: "ligue para o plantão do escritório: [TELEFONE DO PLANTÃO]"].

  Se você ou alguém estiver em perigo agora, ligue 190 (polícia). Violência contra a mulher: 180. Apoio emocional: 188. Emergência médica: 192.
  ```
- **Variação (sem plantão; ninguém lê o canal fora do horário):**
  ```
  Olá! Esta é uma mensagem automática do [NOME DO ESCRITÓRIO].

  Nosso atendimento é [HORÁRIO DE ATENDIMENTO]. Fora desse horário, ninguém da equipe lê as mensagens. A sua ficou registrada e é das primeiras que vamos ler [QUANDO].

  Se você ou alguém estiver em perigo agora, não espere a nossa resposta: ligue 190 (polícia). Violência contra a mulher: 180. Apoio emocional: 188. Emergência médica: 192.
  ```
- **Nunca usar quando:** o texto prometer um caminho de urgência que não existe; ninguém da equipe aprovou o caminho de urgência escrito nele.

## Modelo 3 · Convite para a consulta (paga)
- **Chave:** `convite-consulta-paga`
- **Quando usar:** contato de área atendida que pergunta preço, quer saber "se tem direito", pergunta prazo ou quer contratar, quando `consulta: paga`.
- **Quem lê antes de enviar:** quem faz o primeiro contato, conferindo que não há orientação, estimativa nem promessa. **Sigla:** A.
- **Campos fixos:** `quem_faz_a_consulta`, `duracao`, `formato`, `valor_da_consulta`, `abate_dos_honorarios`, `como_agenda`, `informa_valor_da_consulta_por_mensagem`.
- **Antes de enviar (interno):** o valor só entra se `informa_valor_da_consulta_por_mensagem` for `sim` (ou `só se perguntarem` e a pessoa perguntou); senão, tire a linha do valor. Nenhum valor de ação. A pessoa não relatou vulnerabilidade forte.
- **Campos do envio:** `{NOME}`; na variação prioridade, `{DIA E HORA}`.
- **Texto-modelo:**
  ```
  {NOME}, obrigado por me contar. Para te responder com segurança, [QUEM FAZ A CONSULTA] precisa olhar o seu caso com calma, com os documentos na mão. Por mensagem, a gente correria o risco de te orientar pela metade.

  Por isso o primeiro passo é uma consulta:
  * Duração: [DURAÇÃO]
  * Formato: [PRESENCIAL, ONLINE OU OS DOIS]
  * Valor: [VALOR DA CONSULTA][SE ABATE: ", descontado dos honorários se você contratar o escritório"]
  * Como marcar: [COMO AGENDA]

  Quer que eu veja um horário para você?

  [ASSINATURA]
  ```
- **Variação preço:** antes da lista, "O valor dos honorários depende do que o caso pede, e isso só dá para saber na consulta."
- **Variação prazo:** antes da lista, "O tempo de cada caso depende de detalhes que só aparecem olhando os documentos. Na consulta você sai sabendo os próximos passos."
- **Variação resposta de IA ou vídeo:** antes da lista, "Faz sentido querer entender isso. Para saber se vale para o seu caso, [QUEM FAZ A CONSULTA] precisa olhar o seu [BENEFÍCIO, CONTRATO OU DOCUMENTO] de perto." Nunca confirmar nem desmentir a tese.
- **Variação prioridade (consulta com prioridade da triagem):** troque a pergunta final por "O primeiro horário livre é {DIA E HORA}. Posso reservar para você?". Quem envia preenche `{DIA E HORA}` com o próximo horário livre da agenda; ninguém inventa o horário antes.
- **Nunca usar quando:** a pessoa relata vulnerabilidade forte (uma pessoa liga, sem modelo com preço); a área não é atendida (modelos 10 e 11); há sinal de parada imediata.

## Modelo 4 · Convite para a consulta (gratuita)
- **Chave:** `convite-consulta-gratuita`
- **Quando usar:** o mesmo do modelo 3, quando `consulta: gratuita` (ou `depende do caso` e o advogado decidiu que esta é sem custo).
- **Quem lê antes de enviar:** quem faz o primeiro contato. **Sigla:** A.
- **Antes de enviar (interno):** a gratuidade é informada a quem já procurou o escritório, nunca anunciada como chamariz; o entendimento da seccional sobre consulta sem custo fica `[CONFERIR]` com o advogado.
- **Campos do envio:** `{NOME}`; na variação prioridade, `{DIA E HORA}`.
- **Texto-modelo:**
  ```
  {NOME}, obrigado por me contar. Para te responder com segurança, [QUEM FAZ A CONSULTA] precisa entender o seu caso com calma, olhando os documentos. Por mensagem, a gente correria o risco de te orientar pela metade.

  O primeiro passo é uma conversa inicial, sem custo:
  * Duração: [DURAÇÃO]
  * Formato: [PRESENCIAL, ONLINE OU OS DOIS]
  * Como marcar: [COMO AGENDA]

  Quer que eu veja um horário para você?

  [ASSINATURA]
  ```
- **Variações:** as mesmas do modelo 3 (preço, prazo, resposta de IA, prioridade).
- **Nunca usar quando:** a mensagem vai para muitas pessoas ou para quem não procurou o escritório.

## Modelo 5 · Confirmação de consulta
- **Chave:** `confirmacao-de-consulta`
- **Quando usar:** logo depois de marcar a consulta (`agenda-da-consulta`).
- **Quem lê antes de enviar:** quem marcou, conferindo data, hora e local contra a agenda. **Sigla:** A.
- **Antes de enviar (interno):** o horário está confirmado na agenda; o "o que trazer" não pede laudo, documento de criança, senha ou acesso a sistema.
- **Campos do envio:** `{NOME}`, `{DIA DA SEMANA}`, `{DATA}`, `{HORA}`, `{ONDE}` (o endereço do escritório ou "por vídeo; o link vai na véspera", pelo formato escolhido), `{O QUE TRAZER}`.
- **Texto-modelo:**
  ```
  {NOME}, sua consulta está marcada:

  Dia: {DIA DA SEMANA}, {DATA}, às {HORA}
  Onde: {ONDE}
  Com: [QUEM FAZ A CONSULTA]
  Duração: cerca de [DURAÇÃO]
  O que trazer: {O QUE TRAZER}
  [SE PAGA E A FICHA INFORMA: "Valor: [VALOR DA CONSULTA]. Pagamento: [COMO PAGA]."]

  Se precisar remarcar, me avise por aqui com antecedência, combinado?

  [ASSINATURA]
  ```
- **Nunca usar quando:** o horário ainda não está confirmado na agenda.

## Modelo 6 · Lembrete de consulta
- **Chave:** `lembrete-de-consulta`
- **Quando usar:** na véspera (ou no horário de `confirmacao_e_lembrete`) e, se online, no dia, com o link.
- **Quem lê antes de enviar:** quem cuida da agenda. **Sigla:** A.
- **Antes de enviar (interno):** a consulta continua na agenda; a pessoa não pediu para parar.
- **Campos do envio:** `{NOME}`, `{DATA}`, `{HORA}`, `{ONDE}`, `{LINK}`.
- **Texto-modelo:**
  ```
  VÉSPERA
  Oi, {NOME}! Passando para lembrar da sua consulta amanhã, {DATA}, às {HORA}, {ONDE}.
  Pode me confirmar que está tudo certo? Se surgir algum imprevisto, me avise por aqui que a gente remarca.

  NO DIA (consulta online)
  {NOME}, sua consulta é hoje às {HORA}. O link é este: {LINK}. Vale entrar uns minutos antes para testar câmera e áudio.
  ```
- **Nunca usar quando:** o compromisso é audiência ou perícia de cliente (isso é da experiência do cliente).

## Modelo 7 · Remarcação
- **Chave:** `remarcacao`
- **Quando usar:** o contato pede para remarcar, o escritório precisa remarcar, ou a pessoa faltou e a ficha permite remarcar (`remarcacao`).
- **Quem lê antes de enviar:** quem cuida da agenda. **Sigla:** A.
- **Antes de enviar (interno):** os horários oferecidos estão livres na agenda; a política de `remarcacao` da ficha está respeitada.
- **Campos do envio:** `{NOME}`, `{OPÇÃO 1}`, `{OPÇÃO 2}`, `{OPÇÃO 3}` (ou `{OPÇÕES}`), `{DATA}`, `{MOTIVO CURTO}`.
- **Texto-modelo:**
  ```
  QUANDO O CONTATO PEDE
  Sem problema, {NOME}. Tenho estes horários:
  * {OPÇÃO 1}
  * {OPÇÃO 2}
  * {OPÇÃO 3}
  Qual fica melhor para você? Assim que você escolher, te mando a confirmação.

  QUANDO O ESCRITÓRIO PRECISA REMARCAR
  {NOME}, preciso te pedir para remarcar a consulta de {DATA}, por {MOTIVO CURTO}. Peço desculpas pelo transtorno.
  Tenho estes horários: {OPÇÕES}. Algum serve para você?

  DEPOIS DA FALTA
  Oi, {NOME}. Sentimos sua falta na consulta de {DATA}. Imprevisto acontece.
  Se ainda quiser conversar, tenho estes horários: {OPÇÕES}. É só me dizer qual fica melhor.
  ```
- **Nunca usar quando:** o pedido é remarcar audiência ou perícia (decisão do advogado); a pessoa pediu para parar.

## Modelo 8 · Recebi, te retorno até
- **Chave:** `recebi-retorno-ate`
- **Quando usar:** a resposta completa não sai na hora (dúvida da proposta, pergunta que depende do advogado).
- **Quem lê antes de enviar:** quem respondeu. **Sigla:** A.
- **Antes de enviar (interno):** o prazo é real e está no `contatos.csv` (`proximo_passo` e `data_proximo_passo`); a rotina vai cobrar.
- **Campos do envio:** `{NOME}`, `{O QUE VAI FAZER}` (ex.: "ver com a advogada"), `{PRAZO}` (hora ou dia real).
- **Texto-modelo:**
  ```
  Recebi, {NOME}. Vou {O QUE VAI FAZER} e te retorno até {PRAZO}.
  ```
- **Nunca usar quando:** há sinal de parada imediata (uma pessoa responde agora); quem envia não sabe se o prazo vai ser cumprido.

## Modelo 9 · Documentos para a consulta
- **Chave:** `documentos-para-a-consulta`
- **Quando usar:** depois de marcar, quando a consulta rende mais com algum documento na mão.
- **Quem lê antes de enviar:** quem marcou. **Sigla:** A.
- **Antes de enviar (interno):** peça pouco. Nada de senha, código ou acesso a sistema (gov.br, Meu INSS, banco). Laudo e documento de criança não se pedem por mensagem antes da consulta.
- **Campos do envio:** `{NOME}`, `{DOCUMENTO}` e `{O QUE É}` de cada item.
- **Texto-modelo:**
  ```
  {NOME}, para a consulta render mais, se tiver em mãos, traga (ou mande por aqui antes):

  1. {DOCUMENTO}: {O QUE É, EM UMA FRASE}.
  2. {DOCUMENTO}: {O QUE É}.

  Se não tiver algum, não tem problema: venha assim mesmo.
  ```
- **Nunca usar quando:** a lista depende de saber o caso (deixe para a consulta).

## Modelo 10 · Encaminhamento para outra área
- **Chave:** `encaminhamento-outra-area`
- **Quando usar:** assunto de área que o escritório não atende (`nao_atendemos`), sem urgência.
- **Quem lê antes de enviar:** quem faz o primeiro contato. **Sigla:** A.
- **Campos fixos:** `encaminhamos_para`.
- **Antes de enviar (interno):** o colega indicado autorizou a indicação; sem `encaminhamos_para`, o modelo não sai.
- **Campos do envio:** `{NOME}`, `{ÁREA}`.
- **Texto-modelo:**
  ```
  {NOME}, obrigado por procurar o [NOME DO ESCRITÓRIO]. Nós não atuamos em {ÁREA}, e prefiro te dizer isso agora para você não perder tempo.

  Quem pode te ajudar: [ENCAMINHAMENTO DA FICHA].

  Desejo que dê tudo certo.
  ```
- **Nunca usar quando:** há prisão ou prazo de hoje ou amanhã (modelo 11); há sinal de parada imediata.

## Modelo 11 · Encaminhamento com urgência
- **Chave:** `encaminhamento-urgente`
- **Quando usar:** prisão, flagrante, audiência de custódia ou prazo de hoje ou amanhã, em área que o escritório não atende (caminho "encaminhar com urgência" da triagem).
- **Quem lê antes de enviar:** quem estiver no canal, na hora. Revisada e enviada em minutos. **Sigla:** A.
- **Campos fixos:** `encaminhamos_para`.
- **Antes de enviar (interno):** nenhuma orientação sobre o que fazer na delegacia, na audiência ou no processo; só o encaminhamento. Sem `encaminhamos_para`, uma pessoa responde na hora e o campo vai para a ficha.
- **Campos do envio:** `{NOME}`, `{ÁREA}`.
- **Texto-modelo:**
  ```
  {NOME}, sinto muito pelo que vocês estão passando. Nós não atuamos em {ÁREA}, e por isso não somos as pessoas certas para ajudar agora.

  Procure hoje mesmo: [ENCAMINHAMENTO DA FICHA, EX.: "a Defensoria Pública" OU "um colega que atua na área: [CONTATO AUTORIZADO]"].
  ```
- **Nunca usar quando:** o escritório atua na área (aí é "pessoa agora": o advogado liga).

## Modelo 12 · Recusa educada
- **Chave:** `recusa-educada`
- **Quando usar:** a área é atendida, mas o advogado decidiu não assumir (agenda, conflito de interesse) ou o pedido é algo que o escritório não faz (parecer por mensagem).
- **Quem lê antes de enviar:** o advogado que decidiu. **Sigla:** A.
- **Campos do envio:** `{NOME}`, `{QUEM DECIDIU}`, `{MOTIVO}` (uma frase, sem avaliar o caso, ex.: "a agenda do escritório não comporta um caso novo agora" ou "não fazemos análise de caso por mensagem").
- **Texto-modelo:**
  ```
  {NOME}, obrigado pela confiança em procurar o escritório. {QUEM DECIDIU} entendeu que não vamos poder assumir esse atendimento.

  {MOTIVO}

  Se houver alguma data ou prazo no seu caso, procure outro profissional logo.[SE HOUVER: " Uma opção é [ENCAMINHAMENTO]."]
  ```
- **Nunca usar quando:** o motivo é uma avaliação do mérito ("seu caso não tem chance"): isso é orientação jurídica, e é o advogado quem diz, numa conversa.

## Modelo 13 · Confirmação de quem pediu para parar
- **Chave:** `confirmacao-parar`
- **Quando usar:** o contato pediu para não receber mais mensagens.
- **Quem lê antes de enviar:** quem atende. **Sigla:** A.
- **Antes de enviar (interno):** depois do envio, `pediu_para_parar = sim` no `contatos.csv`, para sempre, e nenhum retorno marcado.
- **Campos do envio:** `{NOME}`.
- **Texto-modelo:**
  ```
  Combinado, {NOME}. Não vamos mais te mandar mensagens.

  Se um dia precisar do escritório, é só escrever aqui.
  ```
- **Nunca usar quando:** quem pede é cliente com caso em andamento (isso é da experiência do cliente: o advogado conversa e combina o canal).

## Modelo 14 · Envio de proposta
- **Chave:** `envio-de-proposta`
- **Quando usar:** junto com a proposta de honorários, depois da consulta.
- **Quem lê antes de enviar:** quem aprova a proposta (`quem_aprova_a_proposta`). **Sigla:** A.
- **Campos fixos:** `validade_da_proposta`.
- **Antes de enviar (interno):** a proposta foi aprovada e não tem pendência no texto que vai ao contato.
- **Campos do envio:** `{NOME}`, `{ESCOPO}` (em poucas palavras, igual ao da proposta), `{DATA DE VALIDADE}` (a da proposta, pela `validade_da_proposta`).
- **Texto-modelo:**
  ```
  {NOME}, como combinamos na consulta, segue a proposta de honorários para {ESCOPO}.

  Nela estão o que está incluído, o que não está, o valor, as formas de pagamento e as despesas do processo. A proposta vale até {DATA DE VALIDADE}.

  Leia com calma. Se ficar qualquer dúvida, me escreva por aqui ou, se preferir, marcamos uma ligação rápida.

  [ASSINATURA]
  ```
- **Nunca usar quando:** a proposta ainda não foi aprovada; o valor vai no corpo da mensagem sem o documento.

## Modelo 15 · Cortesia curta
- **Chave:** `cortesia`
- **Quando usar:** agradecimento, "ok", "recebido", figurinha, despedida.
- **Quem lê antes de enviar:** quem está no canal. **Sigla:** A.
- **Campos do envio:** `{NOME}`.
- **Texto-modelo (escolha um):**
  ```
  De nada, {NOME}! Qualquer coisa, é só chamar.
  Recebido, obrigado!
  Combinado. Bom fim de semana, {NOME}.
  ```
- **Nunca usar quando:** o "obrigado" vem com uma pergunta ou uma queixa ("obrigado, mas ninguém me respondeu"): volta para a triagem.

## Modelo 16 · Aviso de que a mensagem é automática
- **Chave:** `aviso-automatico`
- **Quando usar:** em toda mensagem que sai sem uma pessoa digitando (ferramenta do canal, assistente de primeira resposta), e na passagem para uma pessoa.
- **Quem lê antes de enviar:** aprovada uma vez pelo dono da biblioteca. **Sigla:** A.
- **Campos do envio:** no aviso, nenhum; na passagem, `{NOME}` e `{QUEM ASSUME}`.
- **Texto-modelo:**
  ```
  AVISO
  Esta é uma resposta automática do atendimento do [NOME DO ESCRITÓRIO]. Uma pessoa da equipe lê sua mensagem e continua a conversa [QUANDO].

  PASSAGEM PARA UMA PESSOA
  Oi, {NOME}. Aqui é {QUEM ASSUME} (função ou primeiro nome), do [NOME DO ESCRITÓRIO]. A partir de agora sou eu que sigo com você.
  ```
- **Nunca usar quando:** quem escreve é uma pessoa (o aviso mentiria); a automática se apresenta com o nome do advogado.

## Modelo 17 · Resumo depois da consulta
- **Chave:** `resumo-depois-da-consulta`
- **Quando usar:** no dia da consulta ou no seguinte, para a pessoa ter por escrito o que foi conversado e combinado. A `ata-da-consulta` (se instalada) parte deste modelo e preenche com a ata.
- **Quem lê antes de enviar:** o advogado que fez a consulta, porque a mensagem tem conteúdo jurídico. **Sigla:** A.
- **Campos fixos:** assinatura.
- **Antes de enviar (interno):** cada frase saiu da ata ou do advogado; nenhuma promessa, estimativa de valor a receber, chance ou prazo de decisão; sem valor de honorário (ele vai na proposta, por escrito), a não ser que o advogado peça; as datas são as combinadas na consulta. Os trechos `[DA ATA: ...]` são preenchidos com a ata quando o rascunho é montado: se a ata não tem a informação, o trecho sai e a lacuna vai para cá, nunca para o texto.
- **Campos do envio:** `{NOME}`.
- **Texto-modelo:**
  ```
  Oi, {NOME}, obrigado pela conversa de hoje.

  Para você ter tudo por escrito, o que combinamos:

  O que conversamos: [DA ATA: uma ou duas frases simples sobre os caminhos explicados, sem promessa].

  O que fica com você: [DA ATA: documentos ou decisão], até [DA ATA: data].
  O que fica com a gente: [DA ATA: proposta ou análise], até [DA ATA: data].

  Se lembrar de alguma coisa que não contou na consulta, pode mandar por aqui.

  [ASSINATURA]
  ```
- **Variação vai pensar:** troque o último parágrafo por "Fica à vontade para pensar. Se surgir alguma dúvida, é só escrever." Sem pressa e sem prazo que não foi combinado.
- **Nunca usar quando:** a consulta terminou sem caso e o advogado ainda não ligou (a notícia é dele, por ligação); a mensagem traria algo que não foi dito na consulta.

---

## Mudanças (copiar para o fim da biblioteca)

```
- 1 · AAAA-MM-DD · biblioteca criada pela mensagens-comerciais, modo [rápido | completo], modelos [LISTA DE CHAVES]
```
