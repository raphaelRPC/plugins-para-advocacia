---
name: triar-contato
description: >
  Faz a triagem de cada mensagem de quem ainda não é cliente do escritório (WhatsApp, e-mail,
  direct, telefone anotado): tipo (novo ou antigo), área, assunto, urgência por uma árvore fixa,
  sinal de alerta e o caminho (pessoa agora, encaminhar com urgência, pessoa liga, consulta com
  prioridade, convite, agenda, proposta, encaminhar, recusar, parar). Sugere a resposta-base da
  biblioteca comercial e registra no funil com a régua de retorno armada. Cliente ativo sai para
  a experiência. Roda com uma mensagem, com o lote do dia, no ciclo do agente e no treino. Use
  quando o advogado disser "tria essa mensagem", "chegou um contato novo", "classifica as
  mensagens de hoje", "separa o que é urgente", "o que eu faço com isso".
  Não use para escrever a biblioteca de mensagens (use mensagens-comerciais) nem para mensagem
  de quem já é cliente (use triar-mensagem-do-cliente, do motor-experiencia).
---

# Triar o contato

> Toda mensagem de quem ainda não é cliente passa pelo mesmo caminho: parar se for grave, classificar, decidir quem cuida e deixar registrado com o retorno marcado.

Regras do plugin: `../../docs/regras.md`. Fichas: `../../docs/ficha-do-escritorio-modelo.md`, `../../docs/ficha-comercial-modelo.md` e a tabela de campos em `../../docs/ficha-comercial.md`. Funil e registro: `../../docs/funil.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Casos de treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Terça, 8h50. O WhatsApp tem onze mensagens da noite e da manhã. Uma mãe conta, no meio de um áudio, que o ex ameaçou sumir com as crianças. Outra pessoa diz que o filho foi preso ontem. As outras são "quanto custa", "fui mandado embora" e "preciso remarcar". Quem abre na ordem de chegada responde o "quanto custa" primeiro e deixa a mãe e o preso esperando.

**Regras fixas desta habilidade:**
1. Violência, ameaça, criança em risco ou risco à vida: para tudo, nenhuma resposta pronta, uma pessoa agora.
2. Só quem ainda não é cliente. Cliente ativo sai para a experiência do cliente e não entra no `contatos.csv`.
3. Quem não é cliente não recebe orientação jurídica nem valor de ação por mensagem. Recebe o convite para a consulta.
4. Vulnerabilidade forte vai para uma pessoa, sem modelo e sem preço de consulta. A triagem sugere; nenhuma resposta sai sem alguém ler.
5. A urgência sai da árvore da seção 4.2, igual para todo mundo. Na dúvida entre alta e normal, alta só quando aparece um sinal de alerta.

## 1. Quando usar

**Use quando:**
- Chegou uma mensagem de alguém que ainda não é cliente e o advogado quer saber o que fazer.
- É começo do dia e há um lote para separar.
- O `agente-comercial` ou a `rotina-comercial` chamou esta habilidade no ciclo (modo "no ciclo").
- O `/motor-comercial:comecar` pediu a triagem das doze mensagens de treino (modo "treino").
- A `adaptar-comercial` pediu as palavras de alerta e os sinais do nicho (modo "adaptar").

**Não use quando:**
- A mensagem é de cliente com caso em andamento ("alguma novidade do meu processo?"): vai para a `triar-mensagem-do-cliente`, do motor-experiencia (se instalado). Sem ele, entregue à pessoa que cuida do caso, sem resposta daqui.
- O pedido é escrever as mensagens-padrão: `mensagens-comerciais`.
- O contato já foi triado e o pedido é decidir se vale a consulta ou que perguntas fazer antes: `qualificar-contato` (se instalada; sem ela, convite para a consulta e o advogado decide na consulta).

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/`: `ficha-do-escritorio.md` e `ficha-comercial.md`. Leia `nicho.md`, se existir, e use o vocabulário dele para reconhecer sinais ("encostado", "a firma").
2. **Leia os aprendizados** (`escritorio/04-base/comum/aprendizados-comercial.md`). Aprendizado da triagem vale antes da árvore desta habilidade, desde que não afrouxe a seção 4.1.
3. **Sem ficha:** ofereça `/motor-comercial:comecar`. Se o advogado quiser seguir, pergunte só: "Em que áreas vocês atuam e qual vocês recusam?" e depois "O que é urgente de verdade para vocês?". Use as respostas e ofereça gravar no fim.
4. **Leia a biblioteca comercial** (`escritorio/04-base/comercial/biblioteca-comercial.md`), se existir. A resposta-base sai dela, pela chave do modelo.
5. **Leia o registro** (`escritorio/07-operacao/comercial/contatos.csv`), se existir, para saber se quem escreveu já está no funil. Se o motor-experiencia estiver em uso, leia também `escritorio/07-operacao/experiencia/carteira.csv` só para saber se a pessoa é cliente ativo.
6. **Conta de IA.** Em conta pessoal, só mensagem fictícia ou anonimizada. Mensagem real com dado identificável: avise e anonimize antes de seguir.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | E: `areas`, `nao_atendemos`, `o_que_e_urgente`, `palavras_de_alerta`, `horario_de_atendimento` · C: `primeira_resposta_contato_novo`, `follow_up` |
| Melhora | E: `casos_mais_comuns`, `encaminhamos_para`, `urgencia_vai_para`, `urgencia_para_o_cliente`, `quem_atende` · C: `consulta`, `vulnerabilidade_e_consulta`, `informa_valor_da_consulta_por_mensagem`, `maximo_de_retornos` |

Campo que falta e a mensagem pede: pergunte aquele campo, uma vez, e ofereça gravar. Sem `follow_up`, a linha sai com `proximo_passo = retorno 1 de [A DEFINIR]` e a data vazia, e o fim da triagem avisa.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Uma mensagem | Chegou agora | A mensagem colada (ou a transcrição do áudio) | O cartão (seção 5), no chat |
| Lote | Começo do dia, volta do almoço | Várias mensagens, de preferência com hora | A tabela do lote, PESSOA AGORA no topo |
| Conversa inteira | Uma conversa longa e confusa | O histórico colado | O cartão, com o resumo do que já foi dito |
| No ciclo | O agente chama | O que chegou desde a última rodada | Arquivo da triagem, linhas do registro e rascunhos na fila. Não mostra nada |
| Treino | Casos fictícios ou "é teste" | As mensagens de treino | O mesmo, gravado só em `_treino/` |
| Adaptar | A `adaptar-comercial` chama | `nicho.md` e a ficha | Palavras de alerta e sinais do nicho, para aprovar |
| Saída de PESSOA AGORA | A pessoa já falou com quem estava em PESSOA AGORA ou "pessoa liga" | O que ficou combinado | A linha do registro sem o marcador (seção 4.6) |

Pedido direto ("tria esta: ..."): não faça entrevista. Execute e pergunte só o que faltar.

### Passo 1. Receber e limpar
- Áudio: peça a transcrição ou o resumo de quem ouviu. A triagem não adivinha o que não leu.
- Troque dado identificável pela marcação das regras (nome completo por `[CLIENTE]`, CPF por `[DOC]`, processo por `[PROCESSO]`, telefone por `[CONTATO]`). Avise em uma linha que trocou.
- Dado sensível (saúde, por exemplo): fique só com o que a triagem precisa ("tem doença que impede o trabalho").

### Passo 2. Separar quem já é cliente
Fala de "meu processo", "minha audiência", "o advogado de vocês me disse", ou está na `carteira.csv`: é cliente ativo. Tem sinal da seção 4.1? Avise a pessoa agora do mesmo jeito. Depois, sem classificar aqui, diga: "É cliente com caso em andamento. Vai para a triagem da experiência do cliente." e passe à `triar-mensagem-do-cliente`, do motor-experiencia (se instalado), ou a quem cuida do caso. Não entra no `contatos.csv`. Na dúvida entre cliente e contato antigo, pergunte: "Essa pessoa já assinou contrato com vocês?".

### Passo 3. Conferir a parada imediata
Antes de classificar, procure os sinais da seção 4.1.
- **4.1.a (risco):** nenhuma resposta pronta. Diga no topo, em uma frase, o que apareceu e que a conversa vai para o advogado agora. Se houver risco imediato, quem fala com a pessoa é o advogado, e a orientação é procurar ajuda de emergência: 190, 180, 188 ou 192 (números da seção 5 de `regras.md`, a conferir na região).
- **4.1.b (tempo):** prisão ou prazo de hoje ou amanhã. Se o escritório atua na área, caminho "pessoa agora". Se não atua, "encaminhar com urgência".

### Passo 4. Classificar
| Campo | Como decidir |
|---|---|
| Tipo | `novo` se nunca falou com o escritório. `antigo` se já falou antes de o registro existir (fala de proposta, de consulta marcada, de conversa anterior) e não tem linha no `contatos.csv`. Quem tem linha mantém o tipo dela. |
| Área | Uma das `areas` da ficha. Fora da lista: `fora-da-area`. Sem como saber: `a-confirmar`. |
| Assunto | Até 8 palavras, sem dado sensível, sem vírgula. |
| Intenção | quer contratar, quer preço, quer orientação, pergunta de prazo, traz resposta de IA, agenda, dúvida da proposta, reclama, agradece, pede para parar, outro. |
| Urgência | Pela árvore da seção 4.2. |
| Sinal | A palavra de alerta ou o sinal que apareceu, ou "nenhum". |

### Passo 5. Escolher o caminho
Use a tabela da seção 4.3. Um caminho por mensagem. Dois pedidos na mesma mensagem ("remarcar e saber quanto custa"): o caminho é o do pedido mais sensível, e o outro vai em observação.

### Passo 6. Sugerir a resposta-base
- Só nos caminhos com resposta-base na tabela. "Pessoa agora" e "pessoa liga" não têm.
- Pegue o modelo pela chave na biblioteca comercial e preencha com a ficha. O que quem envia escolhe na hora, de propósito, fica entre chaves: `{NOME}` quando a mensagem não traz o nome, `{DIA E HORA}` do horário escolhido na agenda, `{LINK}` da videochamada. As chaves não são pendência: o `revisor-comercial` aceita, e a fila só deixa marcar `enviado` depois que quem envia preencheu (`../../docs/regras.md`, seção 3). O que falta na ficha é pendência entre colchetes (`[A PREENCHER]`, `[A DEFINIR]`) e vai para o cabeçalho "Antes de enviar" do cartão, nunca no texto que vai ao contato.
- **Valor da consulta** (convite e consulta com prioridade): entra no texto quando `informa_valor_da_consulta_por_mensagem` é `sim`, ou `só se perguntarem` e a mensagem pergunta o preço ("quanto custa?", "quanto vocês cobram?"). Com `não`, a linha do valor sai e o convite diz que o valor é passado ao marcar. O valor vem de `valor_da_consulta`; sem ele, a linha sai e o "Antes de enviar" pede o campo. Valor de ação, nunca.
- **Consulta com prioridade:** a resposta-base oferece o próximo horário livre como `{DIA E HORA}`, para quem envia preencher com o horário real da agenda. A triagem nunca inventa um horário.
- Sem biblioteca: rascunhe no tom da ficha, curto, e marque "rascunho: ainda não está na biblioteca". Ofereça guardar pela `mensagens-comerciais`.
- Toda resposta-base é A: alguém lê e envia. Diga quem (função da ficha) e até quando (prazo da seção 4.4).

### Passo 7. Registrar no funil
Monte a linha do `contatos.csv` pelas regras da seção 4.4: `primeira_resposta` vazia, régua armada quando o caminho é convite. Contato que já tem linha: proponha só a atualização. Mostre as linhas e grave com o ok; no lote, mostre todas juntas e grave de uma vez. Treino grava em `_treino/`.

### Passo 8. Aprender
Pergunte: "Alguma classificação você faria diferente?". Cada correção vira uma regra curta e, com o ok, entra em `aprendizados-comercial.md` (`../../docs/aprender-com-o-uso.md`). Palavra de alerta nova ou área que o escritório não atende: ofereça gravar direto na ficha do escritório, com linha no histórico. Correção que afrouxa a seção 4.1 (por exemplo, "ameaça do ex pode ir com o convite"): explique por que não pode guardar e proponha uma versão que cabe.

### Modo no ciclo
1. O agente passa o que chegou. Não pergunte nada e não mostre nada.
2. Rode os passos 1 a 7. Contato de 4.1 (a ou b): nenhum rascunho; uma linha em PESSOA AGORA no arquivo da triagem, com o porquê e, em 4.1.b fora da área, a chave `encaminhamento-urgente` para a pessoa usar na hora. Vulnerabilidade forte: PESSOA AGORA também, sem rascunho.
3. **Encaminhamento, uma regra só (a mesma da `qualificar-contato`):** prisão ou urgência fora da área (`encaminhamento-urgente`) fica em PESSOA AGORA, sem rascunho (item 2). Área que o escritório não atende, sem urgência (`encaminhamento-outra-area`), vira rascunho na fila como os outros (item 4), com o destino de `encaminhamos_para`; sem esse campo na ficha, nenhum rascunho e uma linha em "para decidir". A etapa `encaminhado` só uma pessoa grava, depois que a mensagem saiu. Recusa: nenhum rascunho no ciclo; vai para "para decidir", e o advogado decide.
4. Para cada caminho com resposta-base, grave um arquivo na fila (`escritorio/07-operacao/comercial/fila/AAAA-MM-DD/NN-<codigo>-<chave>.md`) no formato de `agentes-e-fila.md`, com `status: pendente`, `tipo: <chave do modelo>`, `revisor: pendente` (o `revisor-comercial` preenche) e `prazo` da seção 4.4.
5. No registro, crie linhas só em `novo` ou `triado`; em linha que já existe, mude só `urgencia`, `proximo_passo`, `data_proximo_passo` e `atualizado_em` (`funil.md`, regra 11, "o que o agente pode mexer"). Mudança de etapa além disso (por exemplo, `negociando`) vai para "para decidir".
6. Cliente ativo: lista "para a experiência do cliente", sem linha no registro.
7. Contato que já tem `pessoa agora:` ou `pessoa liga:` e mandou mensagem nova: não troque o marcador nem escreva rascunho. Ele continua em PESSOA AGORA, com a mensagem nova resumida em uma frase. Só a pessoa tira o marcador (seção 4.6).
8. Devolva ao agente: caminho do arquivo da triagem, quantos itens, quantos em PESSOA AGORA, quantos rascunhos, campos da ficha que faltaram.

### Modo treino
Mensagens de `../../docs/casos-ficticios.md`, de `04-base/casos-de-teste/comercial/` ou que o advogado chamar de teste. Tudo grava em `escritorio/07-operacao/_treino/comercial/` (`contatos.csv`, `triagens/`, `fila/`), com a numeração própria do treino. Nada entra no registro real. Mostre a tabela do lote com PESSOA AGORA no topo (as respostas-base ficam no arquivo) e, abaixo, as diferenças com o gabarito da seção 4.5, se houver.

### Modo adaptar
1. Leia `nicho.md`, a ficha e `references/sinais-por-area.md`.
2. Monte a lista do nicho: palavras de alerta do jeito que esse cliente escreve, os sinais de cada passo da árvore e os casos que parecem urgentes e não são (para esse nicho).
3. Marque cada mudança em relação à ficha como `[NOVO]` ou `[ALTERADO]` e mostre. Pergunte: "Alguma dessas não é urgente para vocês, ou falta alguma?".
4. Com o ok, grave em `palavras_de_alerta` (e `o_que_e_urgente`, se mudou) na ficha do escritório, com linha no histórico. Devolva à `adaptar-comercial` três mensagens do nicho que testam a árvore (uma comum, uma com sinal, uma que parece urgente e não é), para ela montar os casos de teste.

## 4. Critérios

### 4.1 Parada imediata

**a) Risco: vai para uma pessoa agora, sem nenhuma resposta pronta**
- Violência física, psicológica, sexual ou patrimonial; ameaça; medo de voltar para casa; medida protetiva pedida ou descumprida.
- Criança ou adolescente em risco; ameaça de levar, esconder ou "sumir com" filho.
- Risco à vida, ideação suicida ("não aguento mais", "vou acabar com tudo").
- O que a ficha listar em `palavras_de_alerta` como prioridade máxima.

**b) Tempo: o relógio corre para quem escreveu**
- Prisão, flagrante, mandado de prisão, audiência de custódia.
- Audiência, perícia ou prazo processual para hoje ou amanhã.

Com o escritório atuando na área: caminho "pessoa agora" (o advogado liga). Fora da área: "encaminhar com urgência" (a pessoa em PESSOA AGORA manda o encaminhamento curto, sem orientação, em minutos; no ciclo, nenhum rascunho).

Exemplos de como esses sinais aparecem, por área: `references/sinais-por-area.md`. Só valem como regra do escritório depois que o advogado confirmar e gravar em `palavras_de_alerta`.

### 4.2 Árvore da urgência

Siga na ordem. A primeira resposta "sim" decide.

1. **Sinal de 4.1.a?** Alta. Caminho "pessoa agora".
2. **Sinal de 4.1.b?** Alta. "Pessoa agora" se o escritório atua na área; "encaminhar com urgência" se não atua.
3. **Vulnerabilidade forte?** Idoso ou pessoa com deficiência sem renda, doença grave (câncer, internação, cirurgia negada), criança sem sustento (falta comida ou remédio), aflição forte ("tô desesperada", "não sei mais o que fazer"). Alta. Caminho "pessoa liga".
4. **Item de `o_que_e_urgente` ou de `palavras_de_alerta` da ficha?** Por exemplo, benefício cortado, audiência ou perícia em até 3 dias, intimação recebida. Alta. Caminho "consulta com prioridade" (área atendida) ou "encaminhar" (fora da área).
5. **Pedido concreto sem sinal?** Quer contratar, preço, orientação, prazo, resposta de IA, agenda, dúvida da proposta. Normal.
6. **Pedido de parar, agradecimento, "ok", informação sem pedido?** Baixa.

**Não sobem a urgência sozinhos** (ficam no passo 5): demissão recente ("fui mandado embora ontem"), remarcação de consulta mesmo que seja amanhã (consulta do escritório não é audiência nem perícia), pergunta de preço ou de prazo, "sem condição de trabalhar" quando é o próprio assunto do benefício, resposta de IA, objeção de preço, pressa educada ("preciso rápido"). Se a demissão vier com outro sinal (família sem renda nenhuma, aflição forte), vale o passo do outro sinal.

**Na dúvida:** entre alta e normal, alta só quando um sinal dos passos 1 a 4 aparece pela metade ("acho que cortaram meu benefício", "parece que é amanhã"). Sem sinal, normal. Entre pessoa e IA, vale a pessoa.

### 4.3 Os caminhos

| Caminho | Quando | Resposta-base (chave na biblioteca) | Régua | Próxima habilidade |
|---|---|---|---|---|
| Pessoa agora | Passo 1; passo 2 com área atendida | Nenhuma. Só o aviso a quem cuida da urgência (`urgencia_vai_para`) | fora | o advogado |
| Encaminhar com urgência | Passo 2 fora da área | `encaminhamento-urgente`: diz que o escritório não atua na área e dá o encaminhamento da ficha, sem orientação. Vai para PESSOA AGORA: a pessoa usa a chave e envia em minutos. No ciclo, nenhum rascunho | fora | (fim) |
| Pessoa liga | Passo 3 | Nenhuma, e nenhum valor de consulta. A pessoa liga e o advogado decide pela `vulnerabilidade_e_consulta` | fora | `qualificar-contato` |
| Consulta com prioridade | Passo 4, área atendida | `convite-consulta-paga` ou `convite-consulta-gratuita`, variação prioridade: o próximo horário fica `{DIA E HORA}` para quem envia. Valor da consulta quando `informa_valor_da_consulta_por_mensagem` permite (passo 6) | armada | `agenda-da-consulta` |
| Convite para consulta | Passo 5, contato de área atendida | O convite pela `consulta` da ficha, com a variação da intenção (preço, prazo, resposta de IA). Nada de valor de ação, de prazo do processo ou de opinião sobre a tese | armada | `qualificar-contato`, `agenda-da-consulta` |
| Agenda | Marcar, confirmar ou remarcar consulta | `remarcacao` (opções de horário) ou `confirmacao-de-consulta` | fora (`funil.md`, regra 6, remarcação) | `agenda-da-consulta` |
| Proposta | Dúvida ou objeção sobre proposta já enviada | `recebi-retorno-ate`, com prazo real. Sem desconto e sem falar de colega | (follow-up) | `objecoes-comerciais` |
| Encaminhar | Fora da área, sem urgência | `encaminhamento-outra-area`. No ciclo, rascunho na fila, revisado e aprovado por uma pessoa | fora | (fim) |
| Recusar | Pedido que o escritório não faz (parecer por mensagem) ou caso que o advogado decidiu não assumir | `recusa-educada`, só depois do ok do advogado. No ciclo, nenhum rascunho: vai para "para decidir" | fora | (fim) |
| Parar | Pediu para não receber mensagens | `confirmacao-parar`, sem perguntar o motivo | fora, para sempre | (fim) |
| Só registrar | Agradecimento, "ok", figurinha | `cortesia`, ou nenhuma | | (fim) |
| Cliente ativo | Passo 2 do fluxo | Nenhuma daqui | não entra | `triar-mensagem-do-cliente`, do motor-experiencia (se instalado) |

Só uma pessoa move para `encaminhado` ou `recusado`. A triagem deixa `triado` e escreve o próximo passo ("confirmar encaminhado"). Caso que não cabe em nenhum caminho: "pessoa agora" com urgência normal e a observação "caminho novo?".

### 4.4 A linha do registro

| Coluna | O que a triagem grava |
|---|---|
| `codigo` | Próximo número livre do ano, `C-AAAA-NNNN`, nunca reaproveitado (o treino tem a numeração dele) |
| `entrada` | Data e hora da primeira mensagem, AAAA-MM-DD HH:MM |
| `canal`, `origem`, `nome_curto` | Da mensagem; `origem` pelas opções da ficha ou `[A CONFIRMAR]`; só primeiro nome ou iniciais |
| `tipo` | `novo` ou `antigo` (passo 4) |
| `etapa` | `triado`. Contato antigo que fala de consulta marcada: `consulta-agendada`; de proposta: a etapa mais provável, com "etapa a confirmar" no `proximo_passo` |
| `responsavel` | Quem cuida pela ficha (`quem_atende`); em PESSOA AGORA e "pessoa liga", quem a ficha diz em `urgencia_vai_para` |
| `primeira_resposta` | **Sempre vazia.** Só se preenche quando uma pessoa confirma que respondeu (comando `fila` ou a própria pessoa). É ela que faz a rotina acusar quem está sem resposta |
| `proximo_passo` e `data_proximo_passo` | Pela tabela abaixo |
| `pediu_para_parar` | `nao`, ou `sim` no caminho "parar" |
| `atualizado_em` | Data da triagem |

| Caminho | `proximo_passo` | `data_proximo_passo` |
|---|---|---|
| Convite e consulta com prioridade | `retorno 1 de N` (N = retornos da régua "não agendou" do `follow_up`, até o `maximo_de_retornos`) | Data da triagem mais o primeiro intervalo da régua, em dias corridos; caiu em dia sem expediente, o próximo dia útil |
| Pessoa agora | `pessoa agora: advogado liga` | hoje |
| Encaminhar com urgência | `pessoa agora: enviar encaminhamento` | hoje |
| Pessoa liga | `pessoa liga: vulnerabilidade` | hoje |
| Agenda (remarcar) | `remarcar consulta (era AAAA-MM-DD)` | hoje |
| Proposta | `responder dúvida da proposta` | hoje |
| Encaminhar, recusar | `confirmar encaminhado` ou `confirmar recusa com o advogado` | hoje |
| Parar | `nenhum` | vazia |

Na consulta com prioridade e no convite, a data do primeiro retorno conta da triagem. Se o convite sair depois (a fila aprovou no dia seguinte), o comando `fila` ajusta a data a partir do envio.

Prazo da primeira resposta (para o cartão e a fila): a `entrada` mais `primeira_resposta_contato_novo`, em horas úteis do `horario_de_atendimento`. Mensagem fora do horário começa a contar na abertura do expediente. "Pessoa agora" e "encaminhar com urgência": em minutos, assim que alguém ler.

### 4.5 Conferência com os casos fictícios

Rodando as doze mensagens de `../../docs/casos-ficticios.md` com a ficha do Escritório Modelo, a triagem tem que dar exatamente isto:

| # | Quem | Tipo | Área | Urgência (passo) | Caminho | Registro |
|---|---|---|---|---|---|---|
| 1 | Marta | novo | previdenciário | alta (4: benefício cortado) | consulta com prioridade; próximo horário como `{DIA E HORA}` e o valor da consulta (ela perguntou o preço e a ficha de treino informa), sem valor de ação | retorno 1 de 3 |
| 2 | Paulo | novo | trabalhista | normal (5: demissão não sobe) | convite, sem dizer quais direitos | retorno 1 de 3 |
| 3 | Joana | novo | família | alta (1: ameaça com crianças) | pessoa agora; nenhuma resposta | fora da régua |
| 4 | Lúcia | novo | fora-da-area | alta (2: prisão) | encaminhar com urgência; só o encaminhamento | fora da régua |
| 5 | Renata | novo | família | normal (5) | convite, sem prometer prazo | retorno 1 de 3 |
| 6 | Sérgio | antigo | a-confirmar | normal (5) | proposta; `negociando` a confirmar; sem leilão nem colega | responder dúvida da proposta |
| 7 | Helena | novo | previdenciário | alta (3: idosa sem renda) | pessoa liga; sem valor de consulta | fora da régua |
| 8 | Bruno | antigo (sem linha no registro) | a-confirmar | normal (5: remarcação) | agenda; opções de horário | remarcar consulta |
| 9 | Antônio | antigo | a-confirmar | baixa (6) | parar; confirmação curta | `pediu_para_parar = sim` |
| 10 | Camila | novo | trabalhista | normal (5) | convite; valor da consulta pela mesma regra do caso 1 (passo 6) | retorno 1 de 3 |
| 11 | Diego | novo | previdenciário | normal (5) | convite; acolhe sem confirmar nem desmentir a tese da IA | retorno 1 de 3 |
| 12 | Fernanda | cliente | | | cliente ativo; sai do comercial | não entra |

Qualquer diferença: falta palavra de alerta, campo na ficha ou aprendizado. Ajuste e rode de novo.

Para o treino, a ficha do Escritório Modelo leva `informa_valor_da_consulta_por_mensagem: só se perguntarem` e `valor_da_consulta: R$ 250` (valor de exemplo). Com `não`, os casos 1 e 10 saem sem a linha do valor, e o gabarito continua certo.

Resposta-base do caso 1, preenchida (exemplo; modelo `convite-consulta-paga`, variação prioridade):

```
Marta, obrigada por me contar. Para te responder com segurança, a advogada precisa olhar o seu caso com calma, com os documentos na mão.

O primeiro passo é uma consulta de 40 minutos, aqui no escritório ou por vídeo. O valor é R$ 250, descontado dos honorários se você contratar o escritório.

O primeiro horário livre é {DIA E HORA}. Posso reservar para você?
Equipe Escritório Modelo
```

`{DIA E HORA}` é de quem envia: a secretária olha a agenda e preenche antes de mandar. O revisor aceita a chave; a fila não deixa marcar `enviado` com ela no texto.

### 4.6 A saída de PESSOA AGORA

Os marcadores `pessoa agora:` e `pessoa liga:` (`funil.md`, regra 4, marcador de pessoa) ficam na linha até uma pessoa contar o que aconteceu. É por eles que a rotina e o follow-up deixam o contato fora de qualquer lista de mensagem pronta (`funil.md`, regra 5, fora da régua).

Depois que a pessoa falou com o contato (o comando `/motor-comercial:fila` pergunta item por item do último resumo "Já falou? O que ficou combinado?", ou o advogado conta nesta conversa), mostre a linha e grave com o ok:

| Coluna | O que grava |
|---|---|
| `primeira_resposta` | Data e hora do contato (ligação ou mensagem), se ainda estava vazia |
| `proximo_passo` | O combinado, com verbo, no lugar do marcador: `consulta marcada`, `aguardar documentos`, `confirmar encaminhado`, `advogada decide a isenção` |
| `data_proximo_passo` | A data do combinado; em consulta marcada, a data da consulta |
| `etapa` | Só se a pessoa disser: `consulta-agendada` quando marcou; `encaminhado` ou `recusado` só com o ok do advogado |
| `atualizado_em` | Hoje |

E uma linha na triagem do dia (`triagens/AAAA-MM-DD.md`), em "Saídas de PESSOA AGORA": hora, código, quem falou e o combinado, sem detalhe sensível. O combinado nunca vira `retorno 1 de N` sozinho: a régua só volta se quem falou decidir, e isso fica escrito no `proximo_passo`. Sem resposta da pessoa, o contato continua no topo do resumo seguinte.

## 5. Formato da saída

**Uma mensagem (o cartão):**

```
TRIAGEM · [dia e hora] · [canal]
Tipo: novo | antigo    Área: ...    Urgência: alta | normal | baixa (passo N)
Assunto: ...
Sinal: ... (ou "nenhum")
Caminho: ...    Quem cuida: ...    Até: [prazo da seção 4.4]
Antes de enviar (interno): [campos que faltam; o que conferir]
Campos do envio: {DIA E HORA}, {NOME} (quem envia preenche) | nenhum
Resposta-base (A, [função] lê antes de enviar), modelo [chave]:
"..."
Registro: [linha proposta do contatos.csv]
```

**Lote:** primeiro "PESSOA AGORA", uma linha por contato com o porquê. Depois a tabela (hora, código, nome curto, tipo, área, assunto, urgência, caminho, quem cuida, até quando), na ordem alta, normal, baixa. Depois as respostas-base completas, numeradas; o resumo em uma linha ("11 contatos: 3 para uma pessoa agora, 5 convites, 1 remarcação, 1 proposta, 1 pediu para parar; 1 cliente ativo foi para a experiência"); e as linhas do registro.

**Arquivo da triagem** (`triagens/AAAA-MM-DD.md`): o mesmo do lote, com cabeçalho `documento`, `gerado_em`, `como_rodou` (pedido, ciclo ou treino). Lote seguinte no mesmo dia entra no mesmo arquivo, com a hora.

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Triagem do dia | `escritorio/07-operacao/comercial/triagens/AAAA-MM-DD.md` |
| Linhas do funil | `escritorio/07-operacao/comercial/contatos.csv` |
| Rascunhos (modo no ciclo) | `escritorio/07-operacao/comercial/fila/AAAA-MM-DD/NN-<codigo>-<chave>.md` |
| Treino (tudo acima) | `escritorio/07-operacao/_treino/comercial/` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-comercial.md` |
| Palavra de alerta ou área nova aprovada | `escritorio/04-base/comum/ficha-do-escritorio.md`, com linha no histórico |

No registro, a triagem cria a linha (etapa `triado`, ou a etapa provável do contato antigo) e atualiza próximo passo, data e urgência. Na saída de PESSOA AGORA (seção 4.6), grava `primeira_resposta`, o combinado no `proximo_passo` e a data, com o ok, e a linha em "Saídas de PESSOA AGORA" na triagem do dia. Uma mensagem só, sem pedido de gravar: entregue o cartão e grave só a linha do funil, com o ok. Sem pasta aberta: tudo no chat, com o caminho de cada arquivo, e as linhas do registro como tabela para colar na planilha.

## 7. Solo e equipe

**Solo:** "quem cuida" é quase sempre o titular. A triagem serve para a ordem: o que é agora, o que é hoje, o que espera o horário fixo de responder. Sugira responder os convites em dois horários do dia, e deixar o celular tocar só para PESSOA AGORA.

**Equipe:** quem cuida sai da ficha (`quem_atende`, `substituto`, `urgencia_vai_para`). A secretária pode triar com esta habilidade, e o advogado recebe só PESSOA AGORA, "pessoa liga" e as recusas. Se o mesmo nome aparece em todos os caminhos, aponte: ali está o gargalo.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Responder na ordem de chegada | A ameaça e a prisão esperam atrás do "quanto custa" | PESSOA AGORA no topo do lote |
| Resposta pronta para quem relata violência | Exposição e risco para quem pediu ajuda | Passo 1 da árvore, sem resposta |
| Orientar quem escreve sobre prisão em área que o escritório não atende | Orientação pela metade numa hora crítica | "Encaminhar com urgência", só o encaminhamento, em minutos |
| Valor de consulta para idosa sem renda | Cobrança antes de alguém ouvir | Passo 3: pessoa liga, sem modelo com preço |
| Remarcação ou demissão tratadas como urgência | Alta perde o sentido e a ameaça se mistura ao resto | Lista do que não sobe a urgência |
| Cliente ativo no funil comercial | Funil inflado e cliente recebendo convite para consulta | Passo 2: sai para a experiência |
| Contato triado e esquecido | Quem procurou fecha com outro | `primeira_resposta` vazia e régua armada |
| Treino no registro real | Painel e rotina com contatos que não existem | Pasta `_treino/` |
| Horário inventado no convite com prioridade | A pessoa reserva um horário que não existe | `{DIA E HORA}` para quem envia, conferido na agenda |
| PESSOA AGORA que nunca sai do topo | O resumo grita todo dia e ninguém lê mais | Seção 4.6: depois da conversa, o combinado entra no lugar do marcador |

## 9. Próximo passo

- Convite e consulta com prioridade: `agenda-da-consulta` (se instalada) para marcar; sem ela, a pessoa marca pela `como_agenda` da ficha. Antes da consulta: `qualificar-contato` e `roteiro-da-consulta` (se instaladas).
- Dúvida ou objeção da proposta: `objecoes-comerciais` (se instalada); sem ela, o advogado responde.
- Resposta-base que não estava na biblioteca: `mensagens-comerciais`, para aprovar e guardar.
- Triagem todo dia sem ninguém pedir: `rotina-comercial` e `/motor-comercial:ciclo`.
- Cliente ativo: `triar-mensagem-do-cliente`, do motor-experiencia (se instalado).

## Referências desta habilidade

- `references/sinais-por-area.md`: exemplos de palavras de alerta e sinais por área, com o passo da árvore de cada um, para o escritório confirmar. Leia no passo 3 quando a ficha não tiver `palavras_de_alerta`, no modo adaptar e no `/motor-comercial:ficha`.
