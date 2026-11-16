# Catálogo de estilos de edição (índice)

Leia só este índice para escolher. O advogado vê tudo isto, com códigos e prévias, no catálogo visual `assets/catalogo/index.html` (formatos em `assets/catalogo/formatos.js`; o código de uma peça, P01 a P58, segue a ordem de `pecas.js`). A lista completa de peças, com nome para o advogado, uso, cuidado OAB e dados de exemplo, é o catálogo único `assets/animacoes/pecas.js`: é dele que saem as opções da prancha do vídeo e a Mesa. Cada estilo já está programado no motor (`scripts/montar_video.py`) e na Mesa de edição: você escreve o tipo e o texto no `projeto.js`, o motor desenha. O advogado escolhe pelo nome da primeira coluna.

Regras de direção para qualquer estilo: a fala manda o tempo; uma ideia por cena; uma cor de destaque; mola sem quique; nada de neon, partículas, tremor ou flash; **o gráfico mostra, não repete a legenda** (rótulos de 1 a 3 palavras, esquema no lugar da frase) (detalhe em `repertorio-de-animacoes.md`, seção 1). Na família Celular as peças animadas entram e saem em corte seco.

## Famílias visuais (o jeito de todos os textos do vídeo)

`estilo.familia` no `projeto.js` vale para o vídeo inteiro; `familia` dentro de um insert muda só aquele momento. O advogado escolhe a família na prancha do vídeo, sobre o próprio quadro; a vitrine (`assets/vitrine/index.html`) fica para consulta.

| Família | Como é | Quando usar | Muda estes inserts |
|---|---|---|---|
| `editorial` (padrão de projetos novos) | sem caixa, à esquerda, linha pequena espaçada e frase grande condensada; palavra de `destaques` na cor de destaque; legenda condensada | ritmo, tutorial, pauta quente | título em duas camadas, rótulos, chamada (letra por letra), carimbo (marca-texto na última palavra), cartão de identificação (só texto) |
| `revista` | sem caixa, serifa itálica com fio na cor de destaque; legenda em serifa com destaque em versalete | opinião, institucional, temas sérios | os mesmos |
| `atras` (atrás de você) | uma palavra gigante atrás da pessoa, recortada com o macOS; o resto na frente, pequeno e centralizado | gancho e frase principal, 1 ou 2 vezes por vídeo | título em duas camadas, chamada, carimbo. Palavra: `palavra` no insert ou a última palavra do título (na chamada, o título inteiro); altura: `yGigante` |
| `celular` | cara de editado no aplicativo do celular: sem movimento (entra e sai em corte seco), letra forte branca pequena à esquerda acima da cabeça, visto e X desenhados no lugar de emoji, frase principal com fundo branco, legenda uma palavra por vez com contorno | bastidor, opinião rápida, quem quer fugir da "cara de IA" | título em duas camadas, rótulos (item com "não" ou "x " leva X), chamada, carimbo (fundo branco), cartão de identificação |
| `institucional` | o cartão azul-marinho de antes | quando o advogado pedir caixa | todos |

**Fontes:** `estilo.fontes` com o id de um par de `assets/animacoes/fontes.js` (clássica, editorial, condensada, tradição, moderna, revista, elegante, técnica, jornal, impacto). O motor baixa os arquivos uma vez para `ferramentas/fontes` e usa nos textos, na legenda e nas animações. Sem `fontes`, as do sistema.

**Cor do vídeo inteiro:** `estilo.cor = "cinema"` (pele suave, contraste, sombras frias, luzes quentes, vinheta e grão leves) ou `"arquivo"` (dessaturado e quente, grão mais forte: tom documental). Sem `cor`, o vídeo fica como foi gravado.

**Moldura:** `estilo.moldura = true` desenha um fio fino na cor de destaque em volta do quadro (combina com a Revista e os capítulos numerados).

**Cores:** `estilo.cores` com os hex da marca (`destaque`, `gigante`, `fundo`, `texto`, de `base/imagem.md`) ou `"video"`: o motor tira a paleta do cenário do próprio vídeo (recorta a pessoa para não pegar o tom da pele) e grava em `estilo.coresVideo`. O destaque é a cor mais viva do cenário, clareada para ler sobre a imagem; a palavra gigante, um tom bem claro da mesma cor. Para refazer, apague `coresVideo`.

Combinação recomendada: família do vídeo `revista` ou `editorial`, e `"familia": "atras"` só no gancho e na frase principal. Sem macOS, `atras` sai como editorial (o motor avisa).

## Cara de IA (confira nos quadros antes de entregar)

- Caixa em todo título. No vídeo, o texto vai direto na imagem; caixa só quando o fundo não deixa ler.
- Linha pequena em cima, frase grande embaixo, tudo centralizado: o modelo de página de internet. Alinhe à esquerda e varie.
- O mesmo formato repetido no vídeo. Cada momento pede um gesto diferente dentro da família.
- Cor genérica (azul-marinho com dourado). A cor vem de `base/imagem.md`.
- Legenda repetindo o título: use `ocultaLegenda` no insert.
- Texto sobre os olhos ou sem contraste com o fundo (parede branca, estátua, camisa clara).

## Receitas de formato

Uma receita diz quais estilos combinar. Use a do formato pedido ("edita como pauta quente"); sem pedido, escolha pela intenção do roteiro.

| Receita | Estilos | Ritmo | Duração | Estado |
|---|---|---|---|---|
| Convite (chamada para evento, aula, material) | cartão-convite na abertura, título em duas camadas para a data, legenda com palavra grande, fórmula, tarja, rótulos, aproximação, chamada em duas camadas, cartão de identificação | cortes por frase, 1,1x | 40 a 60 s | testada |
| Pauta quente | faixa com a página oficial ou matéria grifada (ou foto com etiqueta e manchete), mito e fato, legenda com destaque, cartão de identificação | cortes por frase | 40 a 75 s | pronta |
| Tutorial | faixa com a tela (vídeo ou imagem) em cima e o advogado embaixo, diagrama no lugar, chamada | cortes por frase | 45 a 90 s | pronta |
| Comparativo | fórmula, plano único, cartão de identificação | sem cortes | 25 a 45 s | pronta (só estilos programados) |
| Dica única | título fixo do começo ao fim (`fixo`), legenda abaixo do queixo, prints ou páginas quando cita algo | cortes por frase, sem respiro | cerca de 40 s | pronta |
| Cartaz | sem fala: um texto útil na tela (`cartaz`), o conteúdo completo na legenda do post; muito salvamento | sem cortes | 6 a 10 s | pronta |
| Ranking ou lista | capítulo acima da cabeça a cada item (do último ao primeiro; o 1º no fim), barra de capítulos | cortes por frase | 40 a 75 s | pronta |
| Errado × certo | antes e depois com cortina (rótulos "jeito errado" e "jeito certo"), riscado e trocado, mito e fato | cortes por frase | 30 a 60 s | pronta |
| Documental | `estilo.cor = "arquivo"`, foto que entra em foco com etiqueta e ano, página oficial grifada, linha do tempo | cortes por frase | 45 a 90 s | pronta |
| Minimalista premium | família Revista, título fixo, `estilo.legenda = "palavra"`, `estilo.moldura`, pouca coisa na tela | cortes por frase, sem respiro | 30 a 60 s | pronta |
| Opinião e valores | plano único, legenda discreta | pausas mantidas, 1,0x | 60 a 120 s | pronta |
| Explicação sem rosto (F13) | sem câmera: cinco cenas em tela cheia (a dúvida, a regra com a lei e a fonte, até 3 passos, o cuidado ou o prazo, o fecho com o @), ligadas pela ponte; seta que liga o termo à explicação; sem legenda; voz em off opcional. Comando `cenas` (`tecnico.md`, seção 6) | régua de leitura (sem voz) ou a fala | 15 a 45 s | pronta |
| Reação, educativo com inserts, storytelling, identificação, diálogo, educativo dinâmico, frase | ver `biblioteca` do curso | | | a programar |

## Estilos programados

| Nome para o advogado | No projeto.js | Quando usar | Cuidado OAB |
|---|---|---|---|
| Cartão-convite | insert `bilhete` (cartão de papel inclinado; linha pequena em versalete, linha grande em itálico com serifa; `marcas`) | abertura de convite, tom elegante | sem promessa de resultado |
| Título em duas camadas | insert `duascamadas` (linha pequena, linha grande, apoio; `marcas` para cada linha entrar na fala) | abertura e datas | sem promessa de resultado |
| Tarja | insert `tarja` (linha 1 e linha 2, fundo vermelho) | apontar o erro ou o mito | não mirar colega nem pessoa |
| Rótulos de exemplo | insert `rotulos` (itens que entram um a um) | nomear exemplos da fala | |
| Fórmula que se monta | insert `formula` (termos e resultado; esconde a legenda) | requisitos cumulativos da lei, "o que muda de um caso para outro" | comparar institutos, nunca profissionais nem resultados |
| Chamada em duas camadas | insert `chamada` (etiqueta e texto grande) | fecho | "comenta palavra" só com as condições da `trava-oab` |
| Cartão de identificação | insert `perfil` (o @; nome, escritório e OAB/UF só se o advogado pedir) | fecho, quando houver chamada | no orgânico basta o @; em vídeo impulsionado, nome e OAB entram (CED, art. 44) |
| Carimbo | insert `carimbo` (na família institucional, selo; nas outras, frase com marca-texto ou sublinhado na última palavra; `y` para a altura do selo) | frase principal, "você só aprova" | |
| Cartão e fluxo | inserts `cartao` (rótulo, título, apoio) e `fluxo` (rótulo e itens com seta) | definição curta, de um ponto a outro | |
| Legenda com destaque | `estilo.legenda = "destaque"` e `estilo.destaques` (palavras) | padrão | revisar nomes próprios e termos jurídicos |
| Legenda discreta | `estilo.legenda = "discreta"` | opinião, tom sóbrio | |
| Altura da legenda | `estilo.yLegenda` (linha de base; padrão 1300) | logo abaixo do queixo: meça o queixo nos quadros e use de 60 a 80 px abaixo, até 1490 | dentro da zona segura |
| Faixa sem legenda | `"legenda": false` no efeito `faixa` | quando o rosto desce e a legenda cairia na boca | |
| Legenda com palavra grande | `estilo.legenda = "palavra-grande"` | vídeo mais enérgico | |
| Sem legenda | `estilo.legenda = "nenhuma"` | quando os inserts já contam tudo | |
| Legenda palavra por palavra | `estilo.legenda = "palavra"` | uma palavra por vez, na letra da família; minimalista premium | revisar nomes próprios e termos jurídicos |
| Legenda que acende | `estilo.legenda = "acende"` | a frase inteira com a palavra dita acendendo; ritmo mais alto | |
| Título fixo | insert `fixo` (`rotulo`, `titulo`) do começo ao fim | receita Dica única: a ideia do vídeo sempre no alto | sem promessa de resultado |
| Cartaz | insert `cartaz` (`rotulo`, `titulo`, `itens`, `assinatura`, `plano`) | vídeo curto sem fala; esconde a legenda | o conteúdo útil vai inteiro; nada de oferta de serviço |
| Holofote | efeito `holofote` (`forca` de 0,3 a 0,8) | tudo escurece menos você: a frase séria | |
| Troca de assunto | efeito `transicao` (`modo`: `cor`, `iris` ou `card`; `inicio` e `fim` em volta do corte, cerca de 0,6 s) | virada de assunto | |
| Preto e branco | efeito `pb` | o "jeito errado", o antes | |
| Tela dividida antes e depois | efeito `dividida` (`marcas`: [acende em cima, acende embaixo], `corte`: y da faixa, `rotulos`) | mostrar o cru e o editado do mesmo instante | |
| Aproximação na frase-chave | efeito `aproximacao` (`forca` de 1,05 a 1,30) | a frase principal | |
| Zoom alternado a cada corte | `estilo.zoomAlternado` (padrão 0,05) | esconder o corte seco | |
| Ocultar legenda sob um título | `ocultaLegenda: true` no insert | título que repete a fala | |
| Mito e fato | insert `mitofato` (`mito`, `fato`, `rotulos` opcional, `marcas`: [mito, X, fato]) | desmontar uma ideia errada: o mito leva um X, o fato entra com o visto | desmonta a ideia, nunca colega, escritório ou pessoa |
| Print | insert `print` (`imagem` em `midia/`, `largura`, `alturaMax`, `x`, `y`, `fonte`) | mostrar uma tela, publicação ou página real acima da cabeça; no Celular sai cru, nas outras famílias em cartão arredondado | nada de mensagem, comentário ou elogio de cliente (depoimento), decisão, alvará, valores; métrica sem ostentação |
| Faixa de imagem em cima | efeito `faixa` (`midia`: imagem, vídeo ou a captura `.json` de `capturar_pagina.js`; `etiqueta` como "ARQUIVO 2014", "ILUSTRAÇÃO" ou o artigo; `credito`; `titulo` para manchete; `marcas` do marca-texto; `altura` 760; `desce` do advogado; `yLegenda`, padrão 1495) | pauta quente, tutorial, ler o artigo de lei na fonte oficial | só lugar, instituição, documento público ou matéria; nada de parte, cliente ou caso próprio; imagem de arquivo leva o ano |
| Edição acontecendo na tela | efeito `edicaoaovivo` (`posicao` alto ou baixo, `janela` em segundos) | vídeo sobre o próprio processo de produção: o painel mostra cortes, títulos, legendas e o áudio sendo montados enquanto a pessoa fala | não usar como enfeite em conteúdo jurídico; no alto, não junte com título na mesma hora |

## Camada animada (modelos HTML gravados pelo motor)

Insert `{"tipo": "animacao", "modelo": "<nome>", "dados": {...}, "inicio", "fim", "marcas"}`. As `marcas` dizem quando cada parte entra (tempos do original). Imagens ficam em `midia/` da pasta da Mesa.

| Nome para o advogado | Modelo | Dados | Quando usar |
|---|---|---|---|
| Notebook em 3D | `notebook3d` | `imagem` (ex.: `midia/tela.png`), `selo`, `escala`, `topo`, `seloTopo`, `seloDireita` | mostrar uma ferramenta ou tela real |
| Logo em 3D (P56) | `logo3d` | `logos` [{`arquivo` em `midia/` (.svg vira volume; .png ou .jpg vira ícone grosso), `cor`, `corLado`, `tamanho`}], `modo`: `flutuar` (`posicoes` [[x, y]]), `maos` (`trilhas` e `marcas` de `scripts/rastrear_maos.py`; `sobe`), `cartao` (`rotulo`, `titulo`, `sub`), `duelo` (a primeira vence na marca; `selo`); com a peça nas mãos, use `yLegenda` no insert para subir a legenda | logo do escritório, ferramenta citada, comparação de duas ferramentas |
| Trilha de passos | `trilha` | `passos` [..], `rotulo`, `orientacao` (`horizontal` no alto, sem cobrir o rosto; ou `vertical` com `lado`); uma marca por passo | passo a passo, fases, etapas |
| Leque de artes | `leque` | `imagens` [..], `selo` | mostrar peças do carrossel |
| Palavra revelada | `palavra` | `rotulo`, `palavra`, `apoio`; uma marca; use `ocultaLegenda` | chamada final |
| Citação com aspas | `citacao` | `texto` (literal), `fonte`; uma marca | súmula, artigo, frase de jurista |
| Frase com destaque | `frase` | `texto`, `destaque` (trecho exato), `modo` (`marcatexto`, `colchetes`, `riscado` com `troca`, `embaralha`); marcas [frase, gesto] | o termo principal na hora em que é dito |
| Assinatura | `assinatura` | `nome`, `linha` (o @ ou a área; OAB/UF só se o advogado pedir), `posicao` | abertura ou fecho |
| Cartela de capítulo | `capitulo` | `rotulo`, `numero`, `total`, `titulo`, `tela` (`cheia` ou `alto`) | passos, ranking |
| Barra de capítulos | `progresso` | `partes` [..]; uma marca por parte | vídeo em partes, do começo ao fim |
| Dado com fonte | `dado` | `tipo` (`contador`, `rosca`, `pictograma`, `barras`, `conta`), `valor`, `prefixo`, `sufixo`, `legenda`, `fonte` (obrigatória), `itens`, `termos` | número que se explica sozinho |
| Linha do tempo | `linhadotempo` | `marcos` [{ano, texto}] (até 4), `fonte`; uma marca por marco | histórico de uma lei |
| Prazo no calendário | `calendario` | `inicio` (AAAA-MM-DD), `dias`, `uteis`, `feriados`, `rotuloInicio`, `fonte` | contagem de prazo (confira a data final) |
| Tela genérica | `tela` | `tipo` (`busca`, `prompt`, `comando`, `notificacao`, `celular`), `texto`, `itens`, `resposta`, `app`, `titulo`, `imagem` | dúvida frequente, tutorial de IA, intimação |
| Anotação sobre imagem | `anotacao` | `imagem`, `setas` [{de, para}], `circulos` [{x, y, w, h}], `sublinhados`, `fonte`; posições em % | apontar o trecho no print ou na página |
| Foto de apoio | `foto` | `modo` (`foco` ou `janela`), `imagens` [..], `etiqueta`, `credito` | tom documental, fotos que trocam na fala |
| Antes e depois | `antesdepois` | `antes` {rotulo, texto, imagem}, `depois` {..}, `fonte`; marcas [quadro, cortina]; cartão de 720 × 250 no alto, centralizado, acima da cabeça (`topo`, `largura`, `altura` para ajustar) | regra antiga × nova, errado × certo |
| Diagrama no lugar | `diagrama` | `passos` [{`rotulo` ("1 · O PRAZO"), `ressalva` (fonte ou condição, em cinza), `nos` [{`id`, `texto`, `sub`, `x`, `y` de 0 a 100, `destaque`}], `setas` [{`de`, `para`, `rotulo`, `tracejada`, `destaque`}]}]; uma marca por passo; use `ocultaLegenda` | explicar como uma regra funciona: o mesmo nó muda no lugar de um passo para o outro, a seta se desenha; plano claro em tela cheia por poucos segundos |

47 efeitos e 13 receitas de animação (prazo que corre, artigo de lei com marcador, checklist, requisitos cumulativos e outros) estão em `references/repertorio-de-animacoes.md`. Leia só quando o advogado quiser escolher ou pedir algo que não está aqui.

## Rosto, roupa clara e anúncio (ajuste fino de posição)

Antes de montar, olhe um quadro: onde começa a cabeça e onde termina o queixo. Inserts ficam entre o topo da zona segura e a cabeça; a legenda, logo abaixo do queixo.

| Situação | Ajuste |
|---|---|
| Roupa clara atrás da legenda | `estilo.contornoLegenda: true` (contorno escuro fino) |
| Vídeo impulsionado ("Saiba mais") | rode `zona ... impulsionado` antes de gerar: ele grava `estilo.zona` e o motor põe tudo entre y 270 e 1248 sozinho (textos do alto descem 55, inserts de baixo sobem, a chamada e a palavra revelada vão para cima da cabeça, legenda em 1200 no máximo). `y`, `tam` e `topo` escritos no projeto continuam valendo |
| Pouco espaço acima da cabeça | `y` em `chamada`, `tarja`, `print` e no efeito `edicaoaovivo`; `tam` na `chamada`; `escala` (0,5 a 1) no `edicaoaovivo` e no modelo `dado`; `topo` nos modelos `frase`, `trilha` e `dado` |
| Logo ou imagem ao lado do rosto | insert `print` com `x`, `y` e `largura` |

## A programar (aprovados na biblioteca, ainda sem motor)

Selo de logos, tela dividida de reação, colagem leve, rosto ou dado borrado, letreiro manuscrito, corte em J (só quando a imagem troca: outro ângulo ou imagem de apoio), dois ângulos.

Pediram um desses? Diga que ainda não está no catálogo e ofereça o mais próximo que já existe.
