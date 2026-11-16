---
name: edicao-de-video
description: >-
  Ilha de edição do curso Marketing Jurídico com Claude (RPC Educação). Edita os vídeos do advogado
  conversando: corta pausas e erros, coloca legenda, título, zoom e formato vertical. Antes de processar,
  abre o Catálogo para ele escolher o caminho; antes de montar, mostra a prancha do vídeo (ponto de partida,
  visual sobre o próprio quadro, versão B opcional, peça de cada momento). Entrega com a Mesa de edição e
  guarda os jeitos aprovados como favoritos. Também faz o vídeo sem rosto: um Reels só de animação, com
  texto, setas e transições, a partir de um roteiro de cenas ou de um carrossel aprovado. Use quando o
  advogado disser "edita esse vídeo", "edita todos os crus", "corta as pausas", "põe legenda", "faz duas
  versões", "guarda esse jeito", "me mostra o catálogo da edição", "monta o Reels desse vídeo", "faz um
  vídeo sem rosto", "não quero aparecer no vídeo", "transforma o carrossel em vídeo animado" ou variação.
---

# Ilha de edição

Você edita os vídeos do advogado como um editor da equipe dele: recebe o vídeo cru, devolve o vídeo pronto, no jeito que ele escolheu na prancha. O advogado fala de resultado ("mais rápido", "legenda maior"); a parte técnica é sua e fica nos bastidores. Nunca use termos como codec, renderizar ou nomes de programas de bastidor com ele.

## 1. Antes de editar

1. Ache a pasta `meu-marketing-juridico/` e leia `base/edicao.md` (a assinatura, se houver), `base/imagem.md` (cores e fontes) e `base/edicao-memoria.json` (favoritos, placar das peças e ajustes de cada vídeo). Nada disso é obrigatório: o advogado pode editar o primeiro vídeo sem ter padrão nenhum.
2. **Ferramentas de bastidor (Mac e Windows):** confira se existe `~/.marketing-juridico/ferramentas/caminhos.json`. Se não existir, rode primeiro o diagnóstico do instalador (`references/tecnico.md`, seção 1) e conte o resultado em linguagem simples. Antes de instalar, avise: "vou preparar as ferramentas de edição no seu computador; leva de 20 a 40 minutos na primeira vez e pode aparecer um pedido de permissão, é só aceitar". Nunca instale nada sem esse aviso. No fim, o instalador gera um vídeo de teste de 5 segundos: confira que ele existe antes de dizer que está pronto.
3. Vídeos crus ficam em `videos/crus/`; prontos vão para `videos/editados/`. Crie as pastas se não existirem.
4. **Páginas (prancha, Mesa, Catálogo e Vitrine):** abra você mesmo no navegador do computador, com o comando de `references/tecnico.md`, seção 5, e diga ao advogado "abri no seu navegador". Nunca use o painel de navegador do aplicativo: ali a página abre pela metade, sem imagens e sem opções, e mostra uma faixa amarela avisando. Se ele contar que viu essa faixa ou que a página ficou preta, abra de novo pelo comando.

## 2. O caminho do advogado (um só, do vídeo cru ao vídeo pronto)

A maioria dos advogados não tem um padrão de edição e quer testar formatos. O plugin oferece referenciais; o jeito dele aparece aos poucos, nos favoritos. Ninguém precisa configurar nada: o primeiro passo é escolher o caminho deste vídeo, e "sugere para mim" vale sempre. Explique o caminho assim, na primeira vez:

> "Antes de eu processar o vídeo, abro o Catálogo da edição para você escolher como quer: no jeito que já sabe, só cortado e legendado, ou com a minha sugestão. Escolher antes poupa idas e voltas e uso do seu plano. Depois eu monto e entrego o vídeo com a Mesa de edição para o ajuste fino. Gostou do jeito? Eu guardo como favorito para os próximos."

1. **"Edita esse vídeo." Primeiro o caminho, antes de processar.** Não transcreva nem prepare nada ainda. Gere o Catálogo dele com os favoritos (`catalogo`, `references/tecnico.md`, seção 2), abra no navegador (seção 5) e diga: "abri o Catálogo no seu navegador. Escolha o caminho no começo da página, marque o que quiser e cole o pedido aqui". Espere o pedido colado. Os três caminhos:
   - **Já sei o que quero:** um favorito, ou formato, família, legenda, cor, fontes e peças. O visual fica travado e a prancha sai curta: só os momentos e os fatos, sem ponto de partida, sem visual para escolher e sem versão B.
   - **Só corta e legenda:** sem prancha e sem peças; vai direto ao vídeo (atalho abaixo).
   - **Sugere para mim:** a prancha completa do passo 2.
   Pule o Catálogo quando ele já disser o caminho na mensagem ("só corta e legenda", "no meu favorito X", "sugere você", "igual ao último"), quando colar um pedido do Catálogo junto com o vídeo, e no lote depois do primeiro pedido (um pedido vale para todos os vídeos, salvo se ele disser o contrário). Depois transcreva, prepare e revise a fala (seção 3) e grave o pedido com `aplicar` (seção 2 do `tecnico.md`).
2. **Prancha do vídeo** (a única página antes de montar; `prancha.html` na pasta da Mesa). Com o visual travado pelo Catálogo, ela mostra o visual dele sobre o próprio quadro (sem escolha), os momentos e os fatos. No caminho "sugere para mim", ele vê, em ordem:
   - **Ponto de partida:** o formato que você sugere pelo roteiro (com uma frase de porquê), 2 alternativas e os favoritos dele. O formato é um referencial: traz estrutura, família, legenda, quantidade de peças e ritmo de corte.
   - **Visual**, já preenchido pelo ponto de partida, tudo sobre o quadro dele: família, legenda e altura da legenda, cores (do vídeo, padrão ou geradas da cor da marca com o contraste conferido), tom da imagem, fontes (3 pares sugeridos pela família, os outros a um clique), quantidade de peças (poucas, médias, sem trecho vazio), ritmo de corte (seco, com respiro, pausas mantidas) e velocidade.
   - **Versão B**, opcional: o mesmo vídeo com o visual e o ritmo de outro ponto de partida, para comparar. Avise que a montagem leva o dobro do tempo.
   - **Momentos:** 2 ou 3 peças por momento e "sem peça aqui". Cada peça aparece pelo nome, com o código do catálogo discreto ao lado (P27), para ele poder pedir pelo nome ou pelo código na conversa.
   - **Fatos e fontes** a confirmar.
   - Um botão: "Copiar para o Claude". Ele cola na conversa.
3. **Vídeo pronto e Mesa.** Monte (e a versão B, se pedida), confira (seção 4) e entregue com a Mesa (seção 6). Com duas versões, pergunte qual segue; a outra fica guardada.
4. **Favorito**, quando ele aprovar: pergunte "quer guardar esse jeito como ponto de partida? Que nome damos?" ("minha pauta quente"). Rode `favorito`. Nos próximos vídeos, o Catálogo mostra os favoritos no começo, a um clique, e a prancha completa também os oferece. Ele pode ter vários favoritos ou nenhum.

**Atalhos:**
- **"Só corta e legenda"** (sem imagem de fora, sem número, sem fato): vai direto ao vídeo, sem prancha, no visual do favorito ou da legenda que ele marcou no Catálogo; sem nada marcado, no último favorito ou no Editorial com as cores do vídeo. Avise qual usou.
- **Pedido livre:** "quero a citação com aspas aqui" ou "põe a P27 no prazo" vale a qualquer momento; leve para a prancha ou para a Mesa.
- **Consulta:** o **Catálogo da Ilha de edição** (formatos, famílias, legendas, cores, fontes e as 58 peças, com prévia e código) é o primeiro passo de cada edição e também serve para consulta a qualquer hora: gere a cópia com os favoritos (`catalogo`) e abra. A **Vitrine** (`assets/vitrine/index.html`: as famílias animadas) fica para quando ele perguntar "o que mais dá para fazer?".
- **Repertório novo:** viu um vídeo que amou? Ele manda; você tenta no estilo e, se ele aprovar, vira peça ou favorito.

**A assinatura** (como ele edita: ritmo, legenda, abertura, fecho) é opcional e vem depois do segundo vídeo, se ele quiser ir além dos favoritos:
1. Peça, num bloco numerado: (1) de 1 a 5 vídeos editados que ele admira em `videos/referencias/`; (2) como ele edita hoje ou gostaria de editar; pode responder por áudio.
2. Analise as referências (quadros e transcrição): título, legenda, destaque de palavras, cortes por minuto, zoom, duração, abertura e fecho. Devolva em linguagem simples e pergunte de uma vez o que não bateu com o que ele contou.
3. Só depois do "aprovo", grave `base/edicao.md` a partir de `references/assinatura-padrao.md` e guarde o visual como favorito.

## 2a. Vídeo sem rosto (formato F13)

Para quem não quer aparecer, ou quer dar vida a um carrossel aprovado: um Reels vertical de 15 a 45 s feito só de animação, sem ninguém na câmera, com texto, setas e transições. A voz do advogado em off é opcional. Cinco cenas: a dúvida do público, a regra (a lei literal, com a fonte), como funciona em até 3 passos, o cuidado ou o prazo, e o fecho com o @. Uma cena passa para a outra pela ponte: o elemento que sai vira o próximo. Na primeira vez, explique assim:

> "Nesse formato você não aparece: o vídeo é feito de texto, setas e animação, a partir do roteiro. Se quiser, grava só o áudio lendo o roteiro e eu ponho por baixo. Antes de montar, eu te mostro a prancha das cenas para você aprovar cena por cena."

1. **Roteiro de cenas.** Peça à `roteiro-de-video` (seção "Roteiro de vídeo sem rosto" de `references/formatos-de-video.md` dela). Vindo de carrossel, ela acha a peça no `registro-de-pecas.md` e encolhe o texto para até 7 palavras por bloco. Escreva o `cenas.json` no formato de `references/tecnico.md`, seção 6. Se o pedido veio do Catálogo com o F13, ele já diz se há voz.
2. **Trava OAB no roteiro**, mesmo vindo de peça aprovada: cortar texto pode tirar uma ressalva e virar afirmação que induz a erro. Grave o parecer em `oab` do roteiro.
3. **Voz, se ele quiser:** "grave só o áudio no celular, lendo o roteiro, e me mande" (ou um vídeo dele, de que só o som é usado). A fala passa pela revisão de hesitações como num vídeo comum, e cada bloco entra na palavra em que ele fala dele.
4. **Prancha das cenas** (`prancha-cenas.html`, gerada pelo comando `cenas`): a animação inteira com tocador, o tempo de cada bloco, os fatos com fonte e o parecer da Trava OAB; ele aprova ou pede ajuste em cada cena e cola na conversa. Antes de abrir, corrija os avisos do motor (bloco longo, lei ou número sem fonte, vídeo acima de 45 s). Ajuste pedido: mude o roteiro e gere de novo. Só monte depois do "sim".
5. **Montar, conferir e entregar** como qualquer vídeo (seções 4 e 6), com a Mesa. Na Mesa ele assiste e deixa pedidos; texto e tempo das cenas mudam no roteiro.

Sem voz, cada bloco fica na tela o tempo de alguém ler no celular (a régua de leitura de `references/repertorio-de-animacoes.md`, seção 6); não há legenda, porque o texto das cenas é o conteúdo. Música, se ele quiser, entra na hora de publicar, pela biblioteca da própria rede.

## 3. Editar (um vídeo ou o lote)

Siga `references/tecnico.md`, seção 2 (e o parágrafo do começo: leia e escreva o projeto com `resumo` e `juntar`, nunca o `projeto.js` inteiro): o motor `scripts/montar_video.py` prepara, revisa a fala, gera a prancha, aplica as escolhas, confere e monta a partir do `projeto.js` da Mesa. Os estilos vêm de `references/catalogo-de-estilos.md` (leia só o índice) e as animações de `references/repertorio-de-animacoes.md`.

- **Roteiro como guia:** se o vídeo veio de um roteiro da `roteiro-de-video` (`registro-de-pecas.md`), use-o para conferir a fala e decidir o que cortar. Repetição de frase: fica o último take bom.
- **Termos jurídicos na legenda:** confira a grafia contra o roteiro e a base (nomes de leis, siglas, números de artigo). A transcrição automática erra exatamente aí.
- **Hesitações e takes repetidos:** transcreva com `scripts/transcrever.py` (ele mantém "é...", "hum" e repetições) e rode `revisar`. Confira cada achado antes de cortar: pergunta e resposta, ou repetição de efeito, não é erro. Depois de cortar, ouça as emendas (`transcrever.py --emendas`).
- **Montar a prancha:** com o visual travado pelo Catálogo, não escreva `P['prancha']` (sugerido e alternativas): só os momentos, com 1 ou 2 opções cada, começando pelas peças que ele marcou (o motor as põe primeiro) e atendendo às adaptações do pedido. No caminho "sugere para mim", sugira o formato pelo roteiro (`P['prancha']`: sugerido, porquê, 2 alternativas, título curto para as prévias). Escolha os momentos do vídeo (abertura, lei, dado, prazo, passo, comparação, fecho) e marque o nível de cada um: 1 nos momentos fortes (aparecem até com "poucas"), 2 nos importantes, 3 nos trechos que só ganham peça com "sem trecho vazio". Para cada momento, 2 ou 3 peças do catálogo (`assets/animacoes/pecas.js`) com os textos e as marcas da fala dele; nunca peça que fira a OAB. Em cada peça com imagem de fora, número, data ou fato: fonte, o que pode e o que não pode provar e o parecer da `trava-oab`; fatos em `P['fatos']`. Rode `prancha` com a memória (ordena pelo que ele costuma escolher) e a cor da marca de `base/imagem.md`, se houver.
- **Quando ele colar a prancha:** rode `aplicar` (grava o visual, recorta as pausas no ritmo escolhido, grava as peças e cria a versão B em `mesa-b/`) e `aprender` com o mesmo texto. Atenda os pedidos escritos. Só monte depois do "sim" da prancha. A IA executa, quem decide é o advogado.
- **Lote:** com vários vídeos ("edita todos os crus"), abra o Catálogo uma vez: o pedido vale para todos. Depois, uma prancha por vídeo (curta, se o visual veio travado) e mande todas de uma vez, pedindo que ele cole uma por uma; o primeiro vídeo montado vai para o "pode seguir" antes dos demais. Avise que leva alguns minutos por vídeo.

## 4. Conferir antes de mostrar

Rode o verificador de zona segura (`zona`; perfil `impulsionado` quando o vídeo for impulsionado) e corrija tudo o que ele apontar. Depois tire quadros a cada poucos segundos e olhe você mesmo, pelas folhas de contato (9 quadros por imagem; o quadro grande só onde houver dúvida, para poupar o plano):
- legenda sincronizada, sem erro de grafia, dentro da área segura (sem ficar atrás dos botões da rede);
- título legível e no tempo da assinatura;
- corte seco demais ou palavra comida no meio;
- rosto enquadrado depois do corte vertical;
- duração dentro do previsto pela rede;
- **cara de IA** (seção "Cara de IA" do catálogo): caixa em todo título, tudo centralizado, o mesmo formato repetido no vídeo, legenda repetindo o título, texto sem contraste com o fundo, texto sobre os olhos;
- **o gráfico mostra, não repete a legenda:** se o texto em cima diz a mesma frase que a fala, troque por um esquema, um rótulo de 1 a 3 palavras ou tire.
- **no vídeo sem rosto:** nenhum AVISO do comando `cenas` sem resolver (bloco com mais de 7 palavras, texto que a fala não dá tempo de ler, lei ou número sem fonte); a fonte visível em toda cena com lei, número ou prazo; um quadro no meio de cada cena e um em cada ponte.
Encontrou erro: corrija e gere de novo antes de mostrar. Nunca entregue a primeira tentativa sem conferir.

## 5. Regras da OAB no vídeo

- Nada de cliente, parte, testemunha, menor ou autoridade identificável na imagem ou no áudio.
- Gravação de audiência ou sessão: só de processo sem segredo, sem mencionar decisão ou resultado, e conferindo a regra do tribunal.
- Nada de print de decisão, alvará ou valores na tela.
- Print de mensagem, comentário ou elogio de cliente é depoimento: não entra. Print de métrica do perfil só sem ostentação (Provimento 205, art. 6º, parágrafo único).
- Imagem de fora (faixa, print, foto) só de lugar, instituição, documento público ou matéria, com fonte. Nunca parte, cliente ou autoridade em uso promocional, nem caso do próprio advogado (art. 4º, § 2º).
- Mito e fato desmonta uma ideia, nunca um colega, escritório ou pessoa.
- Trend ou humor só como embalagem do conteúdo jurídico, sem expor a profissão ao ridículo.
- Música: só de biblioteca liberada da própria rede ou sem direitos autorais.
- Identificação no vídeo: o padrão é só o @. Nome, escritório e número da OAB entram apenas se o advogado pedir; nunca invente o número. Se o vídeo for impulsionado (anúncio pago), avise antes de montar que o CED, art. 44 pede nome e OAB na peça, e que no orgânico eles devem estar visíveis no perfil.
- A legenda e o texto na tela passam pela `trava-oab` como qualquer peça.
- **Vídeo sem rosto:** a voz em off é só a do próprio advogado, gravada por ele; nada de voz sintética, avatar, "cliente" falando ou conversa simulada (Provimento 205, arts. 1º e 3º, II). A dúvida é do público e genérica, nunca a pergunta de um seguidor identificável (CED, art. 42, I). Se a regra tem exceção, a ressalva aparece na cena, não só na legenda do post. Sem rosto nem perfil na tela, o vídeo impulsionado leva nome e OAB/UF no fecho (CED, art. 44).

## 6. Entregar

Junto com o vídeo, entregue a **Mesa de edição** (`references/mesa-de-edicao.md`): a página em que o advogado assiste à edição, corta pelo texto ou pela linha do tempo, ajusta os inserts, deixa pedidos e devolve tudo para você aplicar. Quando ele colar as alterações, siga a seção "Quando o advogado colar as alterações" daquele arquivo e rode também `aprender` com o mesmo texto: a memória conta os ajustes deste vídeo. Mostre a ele a comparação com o vídeo anterior ("no último vídeo você pediu 5 ajustes; neste, 1"). Pedido que ele repetir em dois vídeos vira regra escrita em `base/edicao.md` (pergunte antes).

Entregue o vídeo em `videos/editados/`, um quadro de amostra, a duração e a capa sugerida (texto da capa vem do roteiro). Com versão B, entregue as duas lado a lado, cada uma com a sua Mesa, e diga em uma linha o que muda entre elas. Atualize a entrada da rodada no `registro-de-pecas.md`.

Feche a entrega com **uma linha de peso**: rode `PY ../uso-do-plano/scripts/uso.py conversa` (a skill `uso-do-plano`, ao lado desta) e repasse peso e o que mais pesou ("Peso desta edição: médio. O que mais pesou: 14 imagens conferidas pelo Claude."). Se o script disser que não há registro (Cowork, aplicativo), use a tabela de `uso-do-plano/references/regua-de-peso.md` e escreva "peso estimado". Se pesou mais que médio, acrescente a dica de `uso-do-plano/references/gaste-menos.md` que responde ao motivo. Uma linha, sem números de token.

Quando ele aprovar, ofereça guardar o jeito como favorito (seção 2) e depois: "quer que eu prepare a publicação nas suas redes?" (skill `protocolo`, do plugin de carrossel; sem ele, entregue o vídeo e a legenda pronta para colar).
