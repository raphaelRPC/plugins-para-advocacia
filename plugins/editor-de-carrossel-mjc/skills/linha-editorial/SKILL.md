---
name: linha-editorial
description: >-
  Linha editorial do curso Marketing Jurídico com Claude (RPC Educação). Um comando só, do tema ao post:
  pesquisa o que está em alta e o que é novo na área do advogado, escreve o texto inteiro com o orquestrador de copy, cria
  as versões para Instagram, TikTok, YouTube e LinkedIn, monta a arte do carrossel no Canva a partir da biblioteca de modelos, edita o vídeo (com o plugin de vídeo), prepara a
  publicação e faz as análises de performance. Para só nos momentos em que o advogado aprova. Use quando
  o advogado disser "roda a linha editorial", "roda a linha editorial com [tema]", "do tema ao post",
  "faz tudo dessa pauta", "produz a pauta 2 inteira" ou variação.
---

# Linha editorial: do tema ao post

A Linha editorial junta as outras skills do plugin numa linha de produção. O advogado dá um comando; você conduz cada estação e só para quando precisa da decisão dele. **Nada é publicado sem o "sim".** O advogado não precisa abrir o Canva, nem programa de edição, nem as redes.

## Antes de começar

1. Ache a pasta `meu-marketing-juridico/` e leia a base. Sem `base/posicionamento.md`, ofereça o Rito PICO antes (a Linha editorial sem base produz genérico).
2. Confira o que está disponível: identidade fixa e nível do advogado na base? Canva conectado (caminho principal da arte) ou só o motor próprio? agendador conectado? plugin de vídeo instalado (skills `roteiro-de-video` e `edicao-de-video`), com as ferramentas de vídeo (`~/.marketing-juridico/ferramentas/caminhos.json`)? Diga numa linha o que vai rodar e o que vai sair em modo manual (ex.: "sem agendador, eu deixo o pacote pronto para você publicar").
3. Mostre o painel de estações e atualize a cada etapa:

```
LINHA EDITORIAL · [tema]
1 Pesquisa ........................ feito
2 Texto e estrutura ............... feito (prévia)
3 Arte e aprovo ................... aguardando seu aprovo
4 Versões ......................... a fazer
5 Vídeo ........................... a fazer
6 Publicação ...................... a fazer
7 Análises de performance ......... a fazer
```

## As estações

**1 · Pesquisa.**
- Com tema dado: confirme a base legal na fonte oficial e veja como o tema está sendo procurado e discutido agora (perguntas frequentes, buscas em alta, o que os perfis de referência publicaram). Uma linha: "por que esse tema agora".
- Sem tema ("roda a linha editorial"): pegue a pauta mais bem posicionada de `pautas.md`; se estiver vazio ou velho (mais de 3 dias), rode o `informativo-diario` antes. Diga qual pauta escolheu e por quê, e ofereça trocar.

**2 · Texto e estrutura.** Rode a `banca-de-conteudo`, Etapa 1: o orquestrador de copy constrói o texto inteiro, a estrutura em blocos, as três capas, o convite, a legenda e o texto alternativo; a `trava-oab` dá o parecer. Mostre o texto como prévia. Se a peça âncora for vídeo, peça o roteiro à skill `roteiro-de-video` (plugin de vídeo) a partir do texto e **pare para o "aprovo" do roteiro** aqui. Se for carrossel, o "aprovo" é na estação 3, com as lâminas na frente dele.

**3 · Arte (aprovação 1 do carrossel).** Rode a `arte-do-carrossel`: modelo da Árvore de Links (escolhido por ele ou sugerido pelo catálogo), cópia no Canva dele, identidade fixa aplicada, lâminas montadas pela `diagramacao`, prévia mostrada. **Pare e peça o "aprovo".** Depois, entregue as imagens e a lista de acabamento. Sem Canva, a mesma skill usa o motor próprio (caminho B).

**4 · Versões.** Depois do "aprovo" da arte, rode a Banca, Etapa 2, com as versões para **Instagram, TikTok, YouTube e LinkedIn** (as redes que estiverem na base), cada uma com a trava. Se a base incluir também Threads, stories, blog ou newsletter, entregue esses formatos junto.

**5 · Vídeo** (só com o plugin de vídeo instalado; sem ele, marque "não se aplica" e siga).
- Se já existe um vídeo cru do tema em `videos/crus/`: rode a `edicao-de-video` (seção 2): antes de processar, o Catálogo abre para ele escolher o caminho (favorito, só corta e legenda ou a sua sugestão pelo roteiro); monte depois do "sim" da prancha.
- Se ainda não foi gravado: peça à `roteiro-de-video` o roteiro em formato de teleprompter e diga: "grave e coloque em videos/crus; eu edito quando chegar" (ou a rotina Ilha de edição faz isso à noite). A Linha editorial segue com as outras peças; o vídeo entra no pacote quando estiver pronto.
- Se o advogado não grava: marque "não se aplica".

**6 · Publicação (aprovação 2).** Monte o pacote com a `protocolo`: rede por rede, a mídia, a legenda, o primeiro comentário, o dia e a hora. Mostre o preview completo e diga que nada foi agendado. **Pare e peça o "sim".** Com o "sim", agende (ou entregue o pacote manual) e confirme rede por rede.

**7 · Análises de performance.** Registre a rodada no `registro-de-pecas.md` com a reação-alvo de cada peça. Se a rotina Balanço da semana estiver ligada, avise que a peça entra na próxima análise; se não estiver, ofereça ligar (ou analisar a pedido: "como foi o post de [tema]?" daqui a 7 dias). O que funcionou vira pauta de continuidade.

## Regras

- Só duas paradas obrigatórias: o "aprovo" (da prévia do carrossel, ou do roteiro quando a âncora é vídeo) e o "sim" da publicação. Ajustes pedidos no meio do caminho refazem só a estação afetada.
- Se o advogado disser "pode seguir sem me perguntar até a publicação", siga direto até a estação 6, salvando a arte no Canva sem a parada da prévia. O "sim" da publicação nunca é pulado.
- Estação que falhar (conector fora, vídeo com problema): registre o motivo, siga com as outras e mostre o que ficou pendente no fim.
- Com as rotinas ligadas, a Pauta da semana roda as estações 1 e 2 sozinha e deixa os textos na caixa de aprovação. O sinal na caixa continua a Linha editorial na estação 3, até a prévia da arte, que volta para a caixa para o "aprovo".
- Feche com o painel de estações completo.
