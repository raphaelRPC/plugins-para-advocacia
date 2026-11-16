---
name: status-para-o-cliente
description: >
  Traduz a movimentação do processo (colada do sistema, do diário ou do print do tribunal) ou
  a pergunta "e meu processo?" numa mensagem simples: o que aconteceu, o que significa, o que
  vem agora e quando o escritório volta a falar. Classifica a movimentação (rotina, mudou, pede
  algo do cliente, depende do conteúdo), usa o glossário do cliente do escritório, nunca prevê
  resultado nem prazo de decisão, e transforma notícia ruim ou decisão do cliente em roteiro de
  ligação para o advogado, sem mensagem. Roda a pedido ou no ciclo do agente. Use quando o
  advogado disser "o cliente perguntou do processo", "traduz essa movimentação", "o que eu
  respondo pra ele", "saiu a sentença", "alguma novidade?", "conclusos para despacho", "ele
  mandou o print do site". Não use para receber quem acabou de fechar (use
  boas-vindas-do-cliente) nem para o resumo do mês (use resumo-mensal-do-caso).
---

# Status para o cliente

> O cliente não quer saber o nome do ato. Quer saber o que aconteceu, o que muda para ele, o que vem agora e quando vai ter notícia de novo. A habilidade traduz; uma pessoa lê; a notícia ruim vai por telefone.

Regras comuns do plugin: `../../docs/regras.md`. A carteira: `../../docs/carteira.md`. Fichas: `../../docs/ficha-da-experiencia.md`. O agente e a fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Como guardar correções: `../../docs/aprender-com-o-uso.md`.

Terça, 11h30: "Oi, tudo bem? Alguma novidade do meu processo?". A última movimentação diz "Conclusos para despacho", e o cliente já leu isso no site e perguntou a uma IA, que respondeu que "o juiz vai decidir esta semana". Quem responde "sem novidades" ganha a mesma pergunta na semana seguinte, agora com desconfiança. Quem explica a espera, corrige a IA com calma e diz quando volta a falar acaba de mostrar que alguém olhou.

**Regras fixas desta habilidade:**
1. Nunca prevê resultado, chance ou prazo de decisão. "Quando o escritório volta a falar" é um compromisso do escritório, nunca uma data do juiz ou do INSS.
2. Notícia desfavorável, parcial, que pede decisão do cliente, ou o que estiver em `nunca_por_mensagem`, vira roteiro de ligação (H). Nenhuma mensagem com a notícia sai antes da conversa.
3. Toda mensagem desta habilidade é A: alguém lê antes de enviar (`quem_le_antes_de_enviar`). Decisão, valor e data de pagamento: o advogado lê.
4. Sem movimentação, não há tradução. A habilidade não adivinha o que aconteceu, e nunca confirma o que uma IA disse ao cliente sem o advogado conferir.
5. Número do processo, CPF e nome saem antes de colar. Processo em segredo de justiça só com autorização do advogado responsável.

## 1. Quando usar

**Use quando:**
- Um cliente perguntou do processo ("alguma novidade?", "e aí?", áudio, figurinha de relógio).
- Saiu uma movimentação e o escritório quer avisar antes que o cliente pergunte.
- O cliente mandou print do site do tribunal ou do Meu INSS e quer saber o que quer dizer.
- O agente de suporte apontou cliente sem notícia além da régua, ou uma movimentação na entrada (modo no ciclo).
- É preciso preparar a ligação de uma notícia difícil.

**Não use quando:**
- Quem pergunta ainda não é cliente: é orientação a quem não contratou. Use a `triar-contato` do motor-comercial (se instalado); sem ele, o convite para a consulta.
- O cliente quer saber quanto vai receber e quando o dinheiro cai: a habilidade explica a fase, mas valor e data são do advogado e do financeiro.
- O pedido é o resumo do mês: use `resumo-mensal-do-caso`.
- O cliente reclama da demora ou do atendimento: use `reclamacao-e-recuperacao` (se instalada). Sem ela, o passo 2 manda para ligação do advogado.

## 2. Antes de começar

1. **Leia as fichas** (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-experiencia.md`), `nicho.md` se existir, e os aprendizados (`escritorio/04-base/comum/aprendizados-experiencia.md`).
2. **Sem ficha:** ofereça `/motor-experiencia:comecar`. Se o advogado quiser seguir, pergunte só: "Como vocês tratam o cliente: por você, senhor e senhora, ou pelo nome?" e, depois, "Quem lê a mensagem antes de ela sair?".
3. **Leia o glossário do escritório** (`escritorio/04-base/relacionamento-com-o-cliente/glossario-do-cliente.md`). Se não existir, use `references/glossario-processual.md` e ofereça, no fim, gravar o glossário do escritório a partir dele (seção 6).
4. **Leia a base de relacionamento:** a biblioteca (`biblioteca-de-mensagens.md`, chaves da seção 7), a jornada do tipo de caso (`jornada-<tipo-de-caso>.md`, para o "quando volto a falar" e o que nunca vai por mensagem naquela fase) e, se o escritório usa o plugin `inicio-automacao`, os critérios de relevância por área (`criterios-relevancia-movimentacao-<area>.md`), que valem antes da tabela da seção 4.
5. **Leia o cliente:** a linha da `carteira.csv` (fase, humor, `pediu_para_nao_receber`) e o `clientes/<codigo>/historico.md`, com as linhas de contato e as de trabalho do escritório (canal `trabalho-do-escritorio`: o que o escritório fez sem falar com o cliente).
6. **Conta e dados.** Só em conta profissional, com o tratamento de dados conferido. Em conta pessoal, só movimentação fictícia ou anonimizada. Troque nome por `[CLIENTE]`, processo por `[PROCESSO]` e avise em uma linha.

### Campos da ficha que esta habilidade usa

- **Precisa:** E: `tratamento`, `tom_em_tres_palavras` · X: `quem_le_antes_de_enviar`.
- **Melhora:** E: `como_o_cliente_fala`, `frases_que_nunca_usamos`, `assinatura_das_mensagens` · X: `nunca_por_mensagem`.

Campo que falta e a mensagem pede: pergunte aquele campo, uma vez, e ofereça gravar.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Movimentação | Saiu um andamento | O texto do sistema, do diário, do e-mail do tribunal ou o print | Mensagem pronta ou roteiro de ligação |
| Pergunta | O cliente perguntou e ninguém olhou ainda | A pergunta | A resposta-ponte (`recebi-retorno-ate`) agora, e o pedido do que falta |
| Nada mudou | A última movimentação é de rotina ou antiga | A pergunta e a última movimentação | A mensagem que explica a espera |
| Lote | Várias movimentações do dia | Uma por cliente | Tabela com o tipo e as mensagens, ligações no topo |
| No ciclo | O agente pede | Movimentação da entrada ou cliente sem notícia | Rascunho na fila, ou roteiro de ligação e item em PESSOA AGORA |
| Adaptar | Chamado pela `adaptar-experiencia` | `nicho.md`, glossário e modelos | Glossário e modelos reescritos para o nicho, com `[ALTERADO]` |

### Passo 1. Receber e limpar
- Anonimize: nome, número do processo, CPF, número de benefício. Avise em uma linha.
- Laudo inteiro, documento de criança ou processo em segredo de justiça: pare e pergunte se o advogado responsável autoriza. Sem autorização, trabalhe só com a descrição ("laudo contrário à incapacidade").
- Pergunta sem movimentação: entregue a resposta-ponte (`recebi-retorno-ate`, com a `resposta_ponte` da ficha se houver) e peça a última movimentação. Na equipe, entregue o pedido interno de `assets/mensagens-de-andamento.md`. Registre o retorno prometido (passo 7).

### Passo 2. Ler a pergunta por trás da pergunta
Antes de traduzir, leia procurando aflição, reclamação, aperto financeiro ou vontade de desistir ("faz mais de um mês que ninguém me fala nada", "vou procurar outro advogado", "preciso desse dinheiro"). Achou: o caminho é ligação, qualquer que seja a movimentação. Sinal de risco à vida, violência ou dado de saúde grave: pare e leve ao advogado agora (`../../docs/regras.md`, seção 5).

**Resposta de IA ou print do tribunal.** Se o cliente traz o que uma IA disse ou o que leu no site, use a `cliente-com-ia` (se instalada) para o acolhimento e a correção. Sem ela: acolha a pesquisa ("que bom que você acompanha"), explique o termo pelo glossário, diga com calma o que a IA não tem como saber (o tempo da vara, o conteúdo do caso) e nunca confirme nem prometa a data que ela deu.

### Passo 3. Classificar a movimentação
Use a tabela da seção 4 e o tipo de cada termo no glossário. Na dúvida entre rotina e mudou, vale mudou. Na dúvida entre favorável e desfavorável, vale ligação. Termo que não está no glossário: pergunte ao advogado o que ele quer dizer neste processo, e não traduza no chute.

### Passo 4. Se for ligação, montar o roteiro
Tipo D desfavorável, parcial, decisão do cliente, `nunca_por_mensagem`, ou o sinal do passo 2: preencha `assets/roteiro-de-ligacao.md`. A parte "o que dá para fazer" fica `[A DEFINIR PELO ADVOGADO]`: a habilidade não sugere estratégia. Grave em `escritorio/07-operacao/experiencia/clientes/<codigo>/ligacoes/AAAA-MM-DD.md`. Se a advogada não consegue ligar logo, prepare o convite para ligação, sem a notícia, para ela aprovar e enviar com um horário concreto. Pule para o passo 7.

### Passo 5. Escrever a mensagem
Parta do modelo da biblioteca ou de `assets/mensagens-de-andamento.md`. Quatro partes, nesta ordem:
1. **O que aconteceu:** o fato em uma frase, com a palavra do glossário.
2. **O que significa:** o que muda (ou não muda) na vida do cliente.
3. **O que vem agora:** o próximo passo do processo, sem data de decisão. Se o cliente precisa fazer algo, o que e até quando.
   Na mensagem `nada-mudou`, e sempre que o processo está parado, acrescente o que o escritório fez desde o último contato, tirado das linhas de trabalho do escritório do histórico ("Enquanto isso, a advogada conferiu os cálculos e pediu ao INSS a cópia do processo"). Só o que está registrado: sem linha no histórico, a frase sai.
4. **Quando o escritório volta a falar:** pela jornada do tipo de caso ou pela ficha ("assim que houver a próxima novidade, e no resumo do dia 5"). Sem nenhum dos dois, pergunte: "Se nada acontecer, quando vocês voltam a falar com esse cliente?". Sem resposta, a linha sai da mensagem e o retorno fica `[A DEFINIR]` na carteira.

### Passo 6. Conferir
- Nenhuma frase da coluna "nunca" da seção 5.
- Nenhuma data que não seja de ato já marcado (audiência, perícia, prazo do cliente).
- Termo técnico só com explicação, ou trocado.
- Tratamento, tom e assinatura da ficha; nenhuma frase de `frases_que_nunca_usamos`; palavras do cliente (`como_o_cliente_fala`) quando ajudam.
- Nenhuma marcação no texto: pendência vai para o cabeçalho interno "Antes de enviar" (seção 8).
- Cabe na tela do celular.

### Passo 7. Registrar
- Carteira: proponha `proximo_contato` e `motivo_proximo_contato` (`retorno-combinado` ou `maximo-sem-noticia`) e `atualizado_em`. Depois do envio, `ultimo_contato` e `ultimo_contato_tipo`. Fase: sugira a nova a partir da movimentação e peça confirmação (a fase é do jurídico).
- O que conta como contato (`../../docs/agentes-e-fila.md`): a mensagem de andamento, o `nada-mudou` e a ligação informam o caso e mudam o `ultimo_contato`. A resposta-ponte (`recebi-retorno-ate`) e o convite para ligação entram no histórico, mas não mudam o `ultimo_contato`: o cliente continua "sem notícia" até receber a notícia.
- Histórico (`clientes/<codigo>/historico.md`, tabela de `boas-vindas-do-cliente/assets/historico-modelo.md`), dois tipos de linha:
  - **contato**, quando a mensagem for enviada ou a ligação feita: `| 2026-04-10 16h20 | whatsapp | secretária | explicou o concluso para despacho e corrigiu a previsão da IA |`;
  - **trabalho do escritório**, quando a movimentação é um ato do próprio escritório (petição protocolada, prazo cumprido, cálculo entregue, perguntas ao perito): `| 2026-03-18 15h00 | trabalho-do-escritorio | advogada | enviou ao juiz as perguntas para o perito |`, na data do ato, mesmo que nenhuma mensagem saia.
- Cliente que perguntou mais de duas vezes no mês: aponte, para a jornada do tipo de caso ser revista (`jornada-do-cliente`, modo revisar).

### Depois da ligação (saída de PESSOA AGORA)
Notícia ruim, decisão do cliente ou aflição entram no resumo do dia em PESSOA AGORA e só saem de lá depois que a pessoa falou com o cliente. Quando ela contar ("liguei, ela vai pensar até quarta"), ou quando o comando `/motor-experiencia:fila` perguntar "Já falou? O que ficou combinado?", grave, com o ok:
1. **Histórico:** uma linha de contato, sem o conteúdo da conversa: `| 2026-04-10 14h00 | ligacao | advogada | ligação sobre a decisão; combinou novo contato em 2026-04-14 |`.
2. **Carteira:** `ultimo_contato` = a data da ligação e `ultimo_contato_tipo = ligacao` (a ligação informou o caso); `proximo_contato` = a data combinada e `motivo_proximo_contato = retorno-combinado`; `humor` pela leitura de quem ligou (a pessoa decide); `atualizado_em`.
3. **O registro por escrito** (`registro-depois-da-ligacao`), para o cliente reler, só é escrito depois que a ligação está no `historico.md` (a linha do passo 1). Antes disso, não há rascunho nem item na fila. Com a ligação registrada, ele vai para a fila com `tipo: registro-depois-da-ligacao` e `motivo` citando a data da ligação; o revisor deixa passar como `conferir` (a advogada confirma que o texto bate com o que disse) e não bloqueia por ser notícia ruim. Sem a linha no histórico, o revisor bloqueia.
Sem a resposta da pessoa, o item continua no topo do resumo seguinte.

### Passo 8. Aprender
Pergunte: "Você explicaria alguma coisa de outro jeito?". Tradução nova aprovada vai para o glossário do escritório (`glossario-do-cliente.md`), com a data. Regra de comportamento ("Movimentação de perícia em previdenciário sempre passa pela advogada") vai para os aprendizados (`../../docs/aprender-com-o-uso.md`), com o ok. Se a correção muda o que vai para ligação, ofereça gravar em `nunca_por_mensagem`, na ficha.

### No ciclo (chamada pelo agente de suporte)
1. Não pergunte nada. Leia a movimentação da entrada, a linha da carteira, a jornada e o histórico.
2. Tipo R, M, C ou D favorável: grave o rascunho em `escritorio/07-operacao/experiencia/fila/AAAA-MM-DD/NN-<codigo>-andamento.md` (formato de `../../docs/agentes-e-fila.md`), com `tipo`, `motivo` e `prazo` (`avisa_movimentacao_relevante`).
3. Tipo D desfavorável, parcial, decisão do cliente, reclamação ou aflição: nenhum rascunho para o cliente. Grave o roteiro em `clientes/<codigo>/ligacoes/AAAA-MM-DD.md` e devolva ao agente uma linha para PESSOA AGORA. A saída de PESSOA AGORA é a da seção "Depois da ligação". O `registro-depois-da-ligacao` só entra na fila num ciclo seguinte, quando o `historico.md` já tiver a linha `ligacao` da advogada sobre o assunto, com data igual ou posterior à da movimentação.
4. Cliente sem notícia além da régua, sem movimentação nova: rascunho `nada-mudou`, com a última movimentação conhecida. Sem movimentação conhecida, item em PARA DECIDIR ("falta olhar o processo de C-xxxx").
5. `pediu_para_nao_receber = sim`: nada de rotina. Movimentação relevante vira item para a pessoa avisar como o cliente prefere.
6. Fase `decisao` ou humor `a-confirmar` na carteira: nenhum rascunho antes de a pessoa confirmar.
7. Movimentação que é ato do escritório (petição protocolada, prazo cumprido): grave a linha de trabalho do escritório no histórico, mesmo sem rascunho para o cliente.

### Modo adaptar
1. Leia o `nicho.md` (sobretudo "Como ele fala" e "O que este nicho pesquisa sozinho"), o glossário do escritório e os modelos desta habilidade na biblioteca.
2. Glossário: acrescente as palavras do nicho ("encostado", "a firma", "a causa") com o termo processual que elas significam, e reescreva as frases prontas no vocabulário do cliente. Termos que o nicho nunca vê podem sair da versão do escritório.
3. Modelos: reescreva no tom do nicho, sem mudar a estrutura de quatro partes.
4. Marque cada mudança `[ALTERADO]`, mostre, grave com o ok e suba a versão. **Aprender**, como no passo 8.

## 4. Que movimentação vira o quê

| Tipo | Exemplos | O que sai | Quem lê | Sigla |
|---|---|---|---|---|
| R · rotina | conclusos, juntada, ato ordinatório, vista, expedição de ofício | Nada na hora. Se o cliente perguntou: `nada-mudou`. Entra no resumo do mês | Quem acompanha | A |
| M · mudou | citação, contestação, réplica, audiência ou perícia marcada, recurso da outra parte | `atualizacao-de-andamento` | Quem acompanha | A |
| C · pede algo do cliente | exigência de documento, presença em audiência ou perícia | Mensagem com o pedido e o prazo | Quem acompanha; advogado define a lista | A |
| D · favorável | liminar concedida, procedente, acordo homologado, benefício concedido | Mensagem que explica o que ainda pode acontecer, sem comemorar antes da hora | Advogado | A |
| D · valor e pagamento | cálculos, depósito, alvará, RPV, precatório | Fase e próximo passo; valor e data só conferidos | Advogado e financeiro | A |
| D · desfavorável ou parcial | improcedente, parcial, liminar negada, laudo contrário, benefício negado, bloqueio contra o cliente, extinção | Roteiro de ligação. Mensagem só depois, para registrar | Advogado liga | H |
| D · decisão do cliente | proposta de acordo, recorrer ou não, desistir | Roteiro de ligação ou reunião | Advogado | H |

Erro ou atraso do próprio escritório é sempre ligação do advogado, e a habilidade não escreve a explicação no lugar dele.

## 5. O que nunca se diz e o que dizer no lugar

| Nunca | No lugar |
|---|---|
| "Logo sai a decisão", "em breve", "deve sair até o fim do mês" | "Não há como saber quando o juiz decide. A gente acompanha e te avisa assim que sair." |
| "A IA está certa", "é isso mesmo que ela disse" | "Essa ferramenta não tem como saber o tempo da vara nem o que tem no seu processo. O que eu posso te dizer é..." |
| "Seu caso está ganho", "é só questão de tempo" | "O processo está na fase [X]. O próximo passo é [Y]." |
| "A chance é boa", "a maioria ganha" | Nada. Chance é conversa do advogado, e nunca em percentual |
| "Fique tranquilo", "não se preocupe" | "Você não precisa fazer nada agora." |
| "Sem novidades" (e só isso) | O que está sendo esperado e de quem depende |
| "O juiz errou", "a vara é lenta" | "O tempo depende da vara." |
| "Saiu o dinheiro" (antes do alvará conferido) | "Foi feito um depósito no processo. Ainda falta [a liberação] para o valor chegar até você." |

## 6. O glossário do cliente

O glossário do escritório fica em `escritorio/04-base/relacionamento-com-o-cliente/glossario-do-cliente.md` e vale antes do glossário do plugin.

1. **Primeira vez:** copie `references/glossario-processual.md` para o caminho acima, com o cabeçalho (documento, versão, revisado_em, dono), e mostre antes de gravar. Ofereça tirar as seções de áreas que o escritório não atende.
2. **A cada uso:** termo novo aprovado entra na tabela da seção certa, nas quatro colunas que ela tem (termo, o que quer dizer, como dizer ao cliente, tipo). A data da aprovação vai no `revisado_em` do cabeçalho e numa linha da seção "Histórico" no fim do glossário ("2026-04-10 · entrou 'concluso para despacho' na versão do escritório").
3. **No modo adaptar:** as palavras do nicho entram numa seção "Como o cliente fala", com o termo processual que elas querem dizer.
4. A `pagina-do-caso` (se instalada) e a `resumo-mensal-do-caso` leem o mesmo glossário. Uma tradução só, em todo lugar.

## 7. As chaves da biblioteca (desta habilidade)

Biblioteca: `escritorio/04-base/relacionamento-com-o-cliente/biblioteca-de-mensagens.md`. Esta habilidade é dona das chaves abaixo e nunca mexe na chave de outra.

| Chave | Modelo | No `inicio-automacao` |
|---|---|---|
| `atualizacao-de-andamento` | Movimentação que muda algo | modelo 3 |
| `nada-mudou` | Pergunta com processo parado | modelo 4 |
| `recebi-retorno-ate` | Resposta-ponte com prazo | confirmação de recebimento |
| `convite-para-ligacao` | Antes da ligação, sem a notícia | modelo 8, parte 1 |
| `registro-depois-da-ligacao` | Por escrito, depois da conversa | modelo 8, parte 2 |
| `pedido-interno-andamento` | Mensagem interna ao advogado | (interno) |

## 8. Formato da saída

**Mensagem (a pedido):**
```
STATUS · [CÓDIGO] · movimentação de [DATA] · tipo [R | M | C | D]
Antes de enviar (interno): [quem lê] · [o que conferir: termo, data marcada, CONFERIR]
"[mensagem pronta, nas quatro partes, sem marcação]"
Volta a falar: [quando, e de onde veio: jornada, ficha ou A DEFINIR]
Carteira: [campos propostos] · Histórico: [linha proposta]
```

**Ligação:**
```
LIGAÇÃO · [CÓDIGO] · tipo D · quem liga: [advogado] · até: [hoje HH:MM]
Roteiro (H): clientes/[CÓDIGO]/ligacoes/AAAA-MM-DD.md
Convite para ligação (A, se a advogada não ligar logo): "[mensagem sem a notícia]"
Depois: registro-depois-da-ligacao, linha no histórico e na carteira
```

**Lote:** tabela com código, movimentação em cinco palavras, tipo, o que sai e quem lê; ligações no topo, depois C, M e D favorável; rotinas no fim, juntas.

## 9. Exemplos resolvidos (casos fictícios, mensagens 4 e 5)

**Mensagem 4 · Helena, C-2026-0007, BPC idoso, fase `protocolado`.** "Olhei no site do tribunal e tá escrito 'concluso para despacho'. O que isso quer dizer? Perguntei pro ChatGPT e ele disse que o juiz já vai decidir essa semana." Helena é a filha e fala pela mãe, com autorização registrada na abertura. Tipo R, com resposta de IA: passo 2 com o cuidado da `cliente-com-ia`. Sigla A, a advogada lê.
```
Oi, Helena! Que bom que você acompanha o processo da sua mãe.

"Concluso para despacho" quer dizer que o processo foi para o juiz dar o próximo passo. É uma etapa normal e não quer dizer que a decisão sai logo.

Essas ferramentas de IA não têm como saber o tempo da vara nem o que está no processo, então essa previsão de "essa semana" não se confirma. O tempo depende da vara, e eu prefiro não chutar uma data.

Por enquanto vocês não precisam fazer nada. Assim que o juiz der o próximo passo, eu te aviso e explico. E no dia 5 você recebe o resumo do mês, como combinado.

Equipe Escritório Modelo
```
Carteira: `proximo_contato` no dia 5, `motivo_proximo_contato` `resumo-mensal`. Depois do envio, `ultimo_contato` muda, porque a mensagem explicou o andamento. O que não pode falhar: não confirmar a previsão da IA e não prometer data.

**Mensagem 5 · Camila, C-2026-0010, horas extras, fase `decisao`.** "Oi! Saiu alguma coisa? Vi que mexeu no processo ontem." A movimentação de ontem é a sentença: improcedente. Tipo D desfavorável: PESSOA AGORA, nenhuma mensagem com o resultado. Sai o roteiro em `clientes/C-2026-0010/ligacoes/2026-04-10.md`, com: o que aconteceu ("O juiz decidiu o seu processo e, desta vez, não deu razão ao nosso pedido"); o que significa (ainda não é o fim; cabe recurso); "o que dá para fazer" em `[A DEFINIR PELO ADVOGADO]`, com o prazo para recorrer conferido no processo; as perguntas prováveis ("vou ter que pagar alguma coisa?", "vale recorrer?"). A advogada liga hoje. Se não conseguir na próxima hora, ela mesma aprova e envia o convite:
```
Oi, Camila! Aqui é a {NOME DE QUEM LIGA}. Vi o andamento de ontem e prefiro te explicar por telefone, com calma. Consigo te ligar hoje às {HORÁRIO}?
```
`{NOME DE QUEM LIGA}` e `{HORÁRIO}` são campos do envio: o nome sai da ficha (`quem_atende`) quando ela traz, e o horário é o que a advogada escolher na hora. Carteira: `proximo_contato` hoje, `motivo_proximo_contato` `retorno-combinado`; `humor` continua `a-confirmar` até a ligação, e o convite não muda o `ultimo_contato`. Depois da ligação, o registro da seção "Depois da ligação". O que não pode falhar: a 5 não revela o resultado por mensagem.

## 10. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Mensagem a pedido | No chat, para copiar, e gravada em `escritorio/07-operacao/experiencia/clientes/<codigo>/andamento-AAAA-MM-DD.md` (a data é a da movimentação; por exemplo `andamento-2026-04-09.md`), com o cabeçalho "Antes de enviar" separado do texto |
| Rascunho no ciclo | `escritorio/07-operacao/experiencia/fila/AAAA-MM-DD/NN-<codigo>-andamento.md` |
| Roteiro de ligação | `escritorio/07-operacao/experiencia/clientes/<codigo>/ligacoes/AAAA-MM-DD.md` |
| O que foi dito e o trabalho do escritório | `escritorio/07-operacao/experiencia/clientes/<codigo>/historico.md` |
| Retorno e contato | `escritorio/07-operacao/experiencia/carteira.csv` (com o ok; a fase, só com confirmação) |
| Glossário do escritório | `escritorio/04-base/relacionamento-com-o-cliente/glossario-do-cliente.md` |
| Modelos aprovados | `biblioteca-de-mensagens.md`, nas chaves da seção 7 |
| Regras aprendidas | `escritorio/04-base/comum/aprendizados-experiencia.md` |
| Treino | `escritorio/07-operacao/_treino/experiencia/` |

Sem pasta aberta: tudo no chat, com as linhas da carteira para colar na planilha.

## 11. Solo e equipe

**Solo:** o titular é quem lê e quem liga. Responda as perguntas de andamento num horário fixo do dia, com a resposta-ponte valendo no meio tempo. Em audiência, a pergunta que toca decisão espera; o cliente recebe só a resposta-ponte com o prazo real.

**Equipe:** a secretária traduz e manda R, M e C, com a leitura de quem a ficha indica. D favorável e valor passam pelo advogado. Ligação é do advogado responsável; a equipe prepara o roteiro e marca o horário. O pedido interno evita que o advogado receba "o cliente perguntou" sem a movimentação.

## 12. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| "Sem novidades" seco | A pergunta volta na semana seguinte | Mensagem que explica o que está sendo esperado |
| Confirmar a data que a IA deu | Promessa que não depende do escritório | Regra fixa 4 e o passo 2 |
| Sentença ruim por mensagem | O cliente lê sozinho a pior notícia | Tipo D desfavorável vira ligação |
| Comemorar liminar que ainda pode mudar | Decepção maior depois | Favorável sempre com "o que ainda pode acontecer" |
| Tradução no chute | Informação errada por escrito | Termo fora do glossário vai ao advogado |
| Duas traduções do mesmo termo | Cliente confuso entre mensagem, resumo e página | Um glossário do escritório para todos |
| Responder queixa como dúvida | O cliente insatisfeito se sente ignorado | Passo 2 |
| `[CONFERIR]` no texto do cliente | Mensagem que nunca sai, ou sai com a marcação | Cabeçalho interno "Antes de enviar" |

## 13. Próximo passo

- Cliente com resposta de IA: `cliente-com-ia` (se instalada), para as perguntas do tipo de caso respondidas antes.
- Movimentação que pede documento: `checklist-de-documentos` (se instalada). Sem ela, o modelo de pedido de documento da biblioteca.
- Audiência ou perícia marcada: `preparar-o-cliente` (se instalada). Sem ela, a mensagem C com data, local e o que levar, aprovada pela advogada.
- Perguntas que se repetem na mesma fase: `jornada-do-cliente`, modo revisar.
- O retorno prometido: a `rotina-da-experiencia` cobra pela carteira.

## Referências desta habilidade

- `references/glossario-processual.md`: o glossário do plugin, base do glossário do escritório, com a frase pronta e o tipo de cada termo. Leia nos passos 3 e 5 e na seção 6.
- `assets/mensagens-de-andamento.md`: os modelos crus das chaves da seção 7. Use no passo 5.
- `assets/roteiro-de-ligacao.md`: o roteiro de ligação para notícia difícil. Use no passo 4.
