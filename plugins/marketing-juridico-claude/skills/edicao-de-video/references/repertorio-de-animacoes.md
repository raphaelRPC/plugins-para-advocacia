# Repertório de animações (camada animada)

Leia este arquivo só quando o advogado quiser escolher uma animação ("o que dá para fazer aqui?", "quero algo em 3D", "mostra opções") ou pedir um efeito que não está no índice `catalogo-de-estilos.md`. Para editar no dia a dia, o índice basta.

Tudo aqui é camada sobre o vídeo de quem fala: o rosto continua sendo o centro. No formato sem rosto (F13), a animação é o vídeo inteiro: as regras abaixo valem, com a régua de leitura no lugar da fala quando não houver voz (seção 6). Mostre ao advogado no máximo 3 opções por momento do vídeo, pelo nome da primeira coluna.

**Estado:** **pronto** = modelo em `assets/animacoes/`, é só preencher os dados; **sob encomenda** = você escreve um modelo novo seguindo a seção "Como criar um modelo novo" (gasta mais tempo e tokens; avise antes e, se o advogado aprovar o resultado, o modelo fica guardado na pasta dele).

## 1. Regras de direção (valem para toda animação)

1. **A fala manda.** Cada parte do insert entra na palavra que o advogado diz (`marcas`), nunca numa batida de música. Sem fala (vídeo sem rosto sem voz), manda a régua de leitura (seção 6).
2. **Uma ideia por cena**, com espaço vazio em volta. Se precisa de duas ideias, são dois inserts.
3. **Paleta curta:** fundo, destaque e texto, tirados de `base/imagem.md`. Uma só cor de destaque.
4. **Letras com papéis:** uma forte para afirmar, uma com serifa para citação e lei, números em algarismos de largura fixa. Nunca mais de duas famílias.
5. **Movimento com mola**, com no máximo um pequeno passo além do ponto final. Nada de quique, nada de curva padrão do navegador.
6. **Transformar em vez de sumir:** o elemento que sai vira o próximo (um cartão vira o seguinte, um ponto vira uma linha).
7. **Um movimento de câmera por cena**, e suave.
8. **Tempo de leitura:** texto parado na tela por pelo menos 2,5 s; até 7 palavras por vez.
9. **Respiro de rosto:** entre dois gráficos, alguns segundos só do advogado. Em vídeo de 60 s, de 6 a 12 inserts bastam. No vídeo sem rosto, vira **respiro de cena**: depois de uma cena densa, uma cena de uma ideia só (a pergunta, o prazo, o @).
10. **Verdade na tela:** interface real, dado real com fonte, citação de lei literal (trecho omitido marcado com "[…]").
11. **O gráfico mostra, não repete a legenda.** A legenda já diz a frase; em cima vai o esquema, o objeto ou um rótulo de 1 a 3 palavras. Antes de gerar, pergunte em cada momento: "isto mostra a ideia ou só reescreve o que ele disse?".
12. **Proibidos**, porque parecem modelo pronto e brigam com a sobriedade da OAB: brilho neon, partículas explodindo, tremor de câmera, reflexo de lente, separação de cores, flash, vidro fosco em excesso, cérebro e robô como símbolo de IA, piso quadriculado.

## 2. Receitas de animação para o advogado

| Receita | Como se monta | Estado |
|---|---|---|
| Passo a passo | trilha lateral com as etapas apagadas; cada uma acende quando é dita | pronto (`trilha`) |
| Ferramenta funcionando | aparelho em 3D com a tela real; selo de autoria | pronto (`notebook3d`) |
| Vitrine de peças | artes do carrossel abrindo em leque 3D | pronto (`leque`) |
| Chamada final | etiqueta pequena e a palavra entrando letra por letra | pronto (`palavra`) |
| Prazo que corre | os dias úteis acendem um a um sobre o calendário, pulando sábado, domingo e feriado; o artigo do CPC embaixo | pronto (`calendario`) |
| Fases do processo | uma forma só que muda a cada fase (inicial, citação, contestação, instrução, sentença, recurso) | pronto pelo `diagrama` (um passo por fase) |
| Como a regra funciona | plano claro com nós de texto e setas; o mesmo nó muda no lugar de um passo para o outro; ressalva em cinza | pronto (`diagrama`) |
| Artigo de lei | o texto literal entra linha a linha com as aspas grandes; ou a página oficial com o marca-texto no trecho lido | pronto (`citacao`; efeito `faixa`) |
| Mito e fato | o mito leva um X em dois traços, o fato entra com o visto | pronto (insert `mitofato`) |
| Artigo de lei na fonte | a página oficial em cima, o marca-texto passa no trecho que o advogado lê | pronto (efeito `faixa` com `capturar_pagina.js`) |
| Checklist de documentos | folha que cai e se preenche; cada documento recebe o visto quando citado; contador "3 de 7" | sob encomenda |
| Requisitos cumulativos | cada requisito é um portão; o caso atravessa e para no que falha | sob encomenda |
| Caso histórico público | linha do tempo com o ano grande e uma frase; fonte no rodapé | pronto (`linhadotempo`) |
| Mergulho na norma | da Constituição ao código, ao artigo, ao inciso, com régua lateral do nível | sob encomenda |
| Comparação de institutos | antes e depois com cortina, ou barras, ou mito e fato | pronto (`antesdepois`, `dado` barras, `mitofato`) |
| Explicação sem rosto | cinco cenas em tela cheia, sem câmera, ligadas pela ponte; seção 6 | pronto (`cenas`, comando `cenas` do motor) |

## 3. Catálogo de efeitos

### Texto
| Efeito | O que se vê | Uso jurídico |
|---|---|---|
| Texto que sobe da máscara | palavras nascem de uma linha invisível, uma a uma | título de seção, nome do instituto |
| Palavra revelada letra por letra | letras sobem em sequência, a caixa cresce antes | palavra da chamada (pronto) |
| Palavra a palavra na fala | cada termo entra no instante em que é dito | frase principal |
| Grifo que passa | faixa de cor varre a frase e revela o texto | trecho decisivo de uma súmula |
| Marcador que sublinha | traço de caneta desenha sob o trecho dito | artigo de lei lido em voz alta |
| Riscado que vira sublinhado | o traço que risca o mito desliza e sublinha a frase correta | mito e fato |
| Digitação com cursor | texto digitado com ritmo humano | pergunta frequente, busca de jurisprudência recriada |
| Letras embaralhadas que travam | caracteres trocam e param na palavra certa | revelar o termo técnico |
| Ano que gira e bate | número gira em 3D e assenta com mola | linha do tempo de uma lei |
| Palavra com peso | a palavra verga ou sustenta outras ("ônus" curvando a linha) | conceito abstrato |
| Legenda que acende | cada palavra passa de cinza para branco no tempo da fala | legenda de destaque |

### Forma e interface
| Efeito | O que se vê | Uso jurídico |
|---|---|---|
| Forma que se transforma | um retângulo muda de tamanho, cantos e cor a cada estado; o texto troca com desfoque curto | fases do processo |
| Pílula que vira carregando e depois visto | botão encolhe, gira e se resolve num visto | "pedido protocolado" |
| Barra de estado | pílula que troca de rótulo: distribuído, citação, sentença | andamento de um tipo de ação |
| Cursor que clica e arrasta | ponteiro realista conduz cada mudança | tutorial de ferramenta |
| Anel de progresso em etapas | anel enche com rótulos que saltam | etapas de um procedimento |
| Ficha que se preenche e carimbo | linhas digitadas e carimbo "conferido" que desce | checklist de documentos |
| Celular com notificações | avisos empilham numa tela | "chegou uma intimação: e agora?" |
| Tela real em moldura | página capturada dentro de navegador ou celular | sistema do tribunal recriado sem dados de partes |
| Painel que vira | cartão gira e mostra o verso | antes e depois de uma regra |

### Dados e tempo
| Efeito | O que se vê | Uso jurídico |
|---|---|---|
| Contador que rola e trava | dígitos correm e param no valor | prazo em dias úteis |
| Calendário que pula fins de semana | dias acendem um a um, sábado e domingo apagados | contagem de prazo |
| Gráfico que se desenha | linha traçada com o número subindo junto | dado oficial (com fonte) |
| Duas linhas comparadas | uma cinza e plana, outra iluminada | dois cenários de uma regra |
| Linha do tempo com ano grande | câmera avança, nós acendem | histórico de uma lei |
| Régua de escala | barra lateral mostra o nível enquanto a câmera mergulha | hierarquia das normas |
| Bolinhas como unidades | cada ponto vale uma unidade | proporção sem gráfico difícil |

### 3D e espaço
| Efeito | O que se vê | Uso jurídico |
|---|---|---|
| Aparelho em 3D com a tela real | notebook abre e gira devagar | mostrar a ferramenta (pronto) |
| Leque 3D de imagens | cartas saem empilhadas e abrem em arco | vitrine de artes (pronto) |
| Tela inclinada em perspectiva | captura em ângulo, como sobre a mesa | sistema ou documento |
| Cartões com inclinações opostas | dois cartões se afastam em perspectiva | comparação de institutos |
| Vista explodida com rótulos | as partes se separam ao longo de um eixo e voltam | anatomia de uma petição, cláusulas de um contrato |
| Montagem peça por peça | o objeto se constrói em etapas | requisitos que se somam |
| Selo ou medalha 3D | selo inclina e assenta | marco de uma decisão pública (sem resultado próprio) |
| Mergulho de escala | zoom contínuo por vários níveis | da Constituição ao inciso |

### Transições
| Efeito | O que se vê | Quando usar |
|---|---|---|
| Inundação de cor | um círculo cresce de um objeto e cobre a tela, depois encolhe na cena seguinte | troca de bloco |
| Íris | círculo abre e revela outra cena | entrada de um exemplo |
| Objeto que vira a cena | o título avança até a câmera e a próxima cena está atrás | abertura |
| Ponte (P57) | um elemento da cena que sai muda de lugar, tamanho e cantos até virar a primeira peça da próxima: o marca-texto vira o fio dos passos, o cartão da busca vira o fundo | vídeo sem rosto (pronto, dentro de `cenas`) |
| Convergência | cartões se juntam no centro e dali nasce o fecho | conclusão |
| Claro e escuro | troca brusca de fundo na virada do argumento | "mas atenção" |
| Preto e branco que ganha cor | a imagem colore no momento certo | antes e depois |
| Carimbo entre capítulos | selo bate na tela separando partes | linha do tempo |
| Falha de 1 ou 2 quadros | só em corte real, raríssimo | uso excepcional |

### Composição com o vídeo
| Efeito | O que se vê | Quando usar |
|---|---|---|
| Rosto no círculo do canto | o advogado vai para um círculo enquanto o gráfico ocupa a tela | explicação densa, por poucos segundos |
| Tela em cima, rosto embaixo | metade com a demonstração, metade com quem fala | tutorial |
| Trilha lateral | painel de etapas ao lado do rosto | passo a passo (pronto) |
| Vídeo dentro da forma | o próprio vídeo encolhe para dentro de um cartão ou celular | transição para demonstração |

### Texturas (com moderação)
Grão de filme e vinheta; papel e colagem; traço a lápis e quadro branco; retícula de jornal. Servem ao tom (história, bastidor), nunca para enfeitar um dado.

## 6. Cenas de tela cheia (vídeo sem rosto, F13)

O modelo `cenas.html` desenha o vídeo inteiro a partir do roteiro de cenas (`tecnico.md`, seção 6). Fundo papel claro (padrão) ou a cor da marca (`fundo: "cor"`); barra das partes no alto; rodapé de fonte em toda cena com lei, número ou prazo.

| Tipo de cena | O que se vê | Partes (ids para `na`) |
|---|---|---|
| `pergunta` | a dúvida digitada numa busca genérica (`modo: "busca"`, com sugestões) ou em letras grandes (`"grande"`) | texto, sugestoes, fica |
| `lei` | aspas, o texto literal linha a linha, marca-texto no `destaque` e a **seta que liga** o `termo` à explicação (P58) | entrada, l1..ln, destaque, seta, explica, fica |
| `passos` | até 3 passos que caem no fio e acendem; ressalva em cinza | titulo, p1..p3, fica |
| `cuidado` | barra na cor de destaque com o aviso (e um número grande, se houver) ou mito riscado e fato | titulo, texto, numero (ou mito, risco, fato), fica |
| `fecho` | a chamada com o marca-texto e o @ (nome e OAB só se ele pedir ou se for impulsionado) | chamada, arroba, identificacao, fica |
| `peca` | qualquer peça do catálogo encaixada em tela cheia (o **palco**): o modelo abre num quadro interno e é ampliado; no papel claro, ganha um painel escuro atrás | peca |

**A ponte** liga as cenas sozinha: a saída de uma cena (cartão da busca, marca-texto, último passo, barra do cuidado) vira a entrada da próxima (o fundo, o fio dos passos, a barra do cuidado, o marca-texto do fecho). Sem par, a cena que sai se desfaz com desfoque curto.

**Régua de leitura** (sem voz): 0,5 s para achar um bloco novo, 1 s a cada 14 caracteres, 0,4 s para seta ou marca sem texto, 0,8 s de permanência no fim de cada cena, ponte de 0,9 s, mínimo de 2,5 s por cena. Total de 15 a 45 s; passou de 45, encurte o texto ou divida em dois vídeos. **Com voz**, cada parte entra na palavra indicada em `na`; a régua vira conferência e o motor avisa quando a fala passa mais rápido do que o texto pode ser lido.

## 4. O que não usar

- Jogos e peças interativas (no vídeo não há clique).
- Personagens, estilos ou imagens de filmes, séries e jogos; músicas e imagens sem licença guardada.
- Conversa de aplicativo simulada como se fosse real, depoimento ou caso inventado (Provimento 205, arts. 1º e 3º, II).
- Números de resultado, "antes e depois" de cliente, comparação com colegas ou escritórios (art. 3º, IV).
- Estética de anúncio (urgência, oferta, contagem regressiva de venda).
- Flash por batida e caleidoscópio: cansam e podem fazer mal a quem tem sensibilidade à luz.

## 5. Como criar um modelo novo (sob encomenda)

1. Copie a estrutura de um modelo pronto de `assets/animacoes/` (`trilha.html` para 2D, `notebook3d.html` para 3D). Todo modelo carrega `base.js` e define:
   - `window.AREA = {x, y, w, h}`: o menor retângulo do quadro de 1080 x 1920 que a animação ocupa (quanto menor, mais rápida a gravação);
   - `window.desenhar(t)`: desenha tudo a partir de `t` (segundos desde a entrada), sem transição de CSS, sem temporizador, sem sorteio sem semente;
   - `window.PRONTO = true` quando imagens e fontes carregarem.
2. Use `U.mola`, `U.janela` e `U.marcas` do `base.js` para entrar, sair e acender cada parte na fala. `FIM` é o momento da saída.
3. Os textos vêm de `DADOS`; imagens ficam em `midia/` da pasta da Mesa e são lidas por `/midia/...`. Para 3D, importe `three` pelo mapa de importação, como no `notebook3d.html`.
4. Fundo sempre transparente.
5. Teste com `animar.js --tempos` em 4 ou 5 instantes e olhe os quadros sobre um fundo cinza antes de gerar o vídeo.
6. Se o advogado aprovar, guarde o modelo em `assets/animacoes/` da pasta dele e acrescente o nome em `MODELOS` na Mesa.
