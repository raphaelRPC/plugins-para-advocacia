# Bastidor técnico da edição (nunca mostrar ao advogado)

Tudo aqui é para você executar. Para o advogado, fale só de resultado.

**Poupe o plano do advogado:** nunca abra o `projeto.js` inteiro (ele leva os picos do áudio e todas as palavras, de 30 a 60 KB). Para ler, rode `PY montar_video.py resumo <pasta_mesa>` (visual, inserts, efeitos, momentos e a fala em frases com o tempo do original; `--fala` mostra só a fala). Para escrever momentos, prancha, fatos, estilo, inserts ou efeitos, grave um JSON curto (ex.: `<pasta_mesa>/novo.json` com `{"momentos": [...], "fatos": [...]}`) e rode `PY montar_video.py juntar <pasta_mesa> <arquivo.json>`: inserts e efeitos entram ou trocam pelo `id`, `estilo` soma os campos, o resto troca inteiro. Na conferência, olhe as folhas de contato e só abra o quadro grande do trecho com dúvida. Não releia um arquivo de referência que já leu nesta conversa.

## 1. Ferramentas: instalador para Mac e Windows

Tudo fica numa pasta só do usuário, sem senha de administrador e sem Homebrew: `~/.marketing-juridico/ferramentas` (no Windows, `%USERPROFILE%\.marketing-juridico\ferramentas`). Ali o instalador grava `caminhos.json` com `ffmpeg`, `python`, `node`, `node_path`, `chrome` e `scripts`. **Leia esse arquivo antes de qualquer comando** e use os caminhos das ferramentas. Os scripts e as páginas, use sempre os da pasta desta skill (a versão do plugin instalada agora): depois de uma atualização do plugin, o `scripts` de `caminhos.json` pode apontar para a versão antiga, e as ferramentas continuam valendo sem reinstalar.

| Sistema | Diagnóstico (não instala nada) | Instalação (20 a 40 min na primeira vez) |
|---|---|---|
| Mac | `bash instalar/instalar-mac.sh --diagnostico` | `bash instalar/instalar-mac.sh` |
| Windows | `powershell -ExecutionPolicy Bypass -File instalar\instalar-windows.ps1 -Diagnostico` | `powershell -ExecutionPolicy Bypass -File instalar\instalar-windows.ps1` |

Como rodar: comece pelo diagnóstico e conte o resultado em palavras simples. Rode a instalação em segundo plano e acompanhe o registro `~/marketing-juridico-instalacao.log` até aparecer `PRONTO!`. Deu erro: leia o registro, corrija só aquela etapa e rode de novo (ele pula o que já está pronto). No fim, o instalador gera `ferramentas/teste/teste-instalacao.mp4` (título atrás da pessoa, legenda, animação) e abre a pasta: confira que o vídeo existe.

O que ele instala, em ordem: Node (só se faltar), ffmpeg e o gravador de animações (`ffmpeg-static`, `puppeteer-core`, `three`), um navegador para gravar animações (só se não houver Chrome; no Windows, o Edge serve), o Python da edição com a transcrição (`faster-whisper` 1.0.3, `requests`, `huggingface_hub` abaixo da 2, `numpy`, `pillow`, `onnxruntime`, via `uv`), o modelo de transcrição `medium` (cerca de 1,5 GB) e o modelo aberto de recorte da pessoa (`u2net_human_seg`, quando o recorte do macOS não está disponível).

Diferenças entre os sistemas:
- **Recorte da pessoa** ("atrás de você", cores do vídeo): no Mac com as ferramentas da Apple, `recortar.swift`; no Windows ou sem elas, `recortar.py` com o modelo aberto. O resultado é parecido; o motor escolhe sozinho (`MJ_RECORTE=onnx` força o modelo aberto).
- **Fontes:** no Mac, Avenir Next, New York e Didot; no Windows, Segoe UI, Bahnschrift condensada, Georgia e Consolas. O desenho muda pouco; confira os quadros.
- **Comandos:** use o `python` de `caminhos.json` para tudo (motor, transcrição, teste). No Windows, caminhos com barra invertida e entre aspas.
- **Navegador:** Chrome, Edge ou o navegador baixado (`CHROME_PATH` força um).

Sem instalação possível: plano B da seção 4.

## 2. Ordem de edição (com o motor)

O motor `scripts/montar_video.py` faz a parte pesada. Você decide o conteúdo do `projeto.js`; ele desenha e monta. `FF` e `PY` abaixo são os caminhos de `caminhos.json`. `MEM` é `meu-marketing-juridico/base/edicao-memoria.json` (favoritos, placar das peças, pontos de partida escolhidos e ajustes por vídeo; criado sozinho na primeira vez). Não existe configuração prévia: o visual de cada vídeo sai do pedido do Catálogo ou da prancha.

0. **Catálogo, antes de processar:** `PY montar_video.py catalogo MEM <pasta do advogado>/videos/catalogo.html "<caminho do vídeo>"` grava a cópia do Catálogo com os favoritos dele e o vídeo já preenchido (a cópia usa as imagens e as listas da pasta do plugin; refaça a cada vídeo, porque a memória muda). Abra no navegador (seção 5) e espere o pedido colado. Guarde o texto colado num arquivo (`<pasta_mesa>/pedido-catalogo.txt`, depois do passo 3) e leia a linha "Caminho". Leva menos de um segundo e não processa o vídeo.
1. **Diagnóstico:** `FF -i <video>` para duração, resolução e cor. Vídeo de iPhone vem em HDR (HLG); o motor detecta e converte sozinho para a cor padrão das redes.
2. **Transcrição com hesitações:** `PY scripts/transcrever.py <video> <nome.transcricao.json> --nomes "nomes próprios, siglas, leis"`. Ela mantém "é...", "hum" e repetições, que a transcrição comum esconde. `--rapido` usa o modelo pequeno (só para escolher cortes).
3. **Preparar:** `PY montar_video.py preparar FF <video> <transcricao.json> <pasta_mesa> "<nome>"`. Gera o proxy da Mesa, os picos do áudio, as palavras e os cortes de pausa (acima de 0,3 s, com respiro). **AVISO** de palavra longa demais: a transcrição engoliu um trecho; transcreva só aquela janela de novo (`transcrever.py <video> --janelas t`) e corrija o JSON.
3a. **Pedido do Catálogo:** `PY montar_video.py aplicar <pasta_mesa> <pasta_mesa>/pedido-catalogo.txt MEM` (a memória resolve o favorito pelo nome). "Já sei o que quero" e "só corta e legenda" gravam o visual em `estilo`, recortam as pausas no ritmo dele e marcam `estilo.travado` {caminho, favorito, pecas, adaptacoes}, que faz a prancha sair curta; o formato marcado dá a estrutura e o favorito, o visual, e o que ele marcou por cima vale por último. "Sugere para mim" não grava nada: siga com a prancha completa. Rode também `aprender` com o mesmo arquivo (conta o ponto de partida escolhido). As adaptações aparecem como PEDIDO: atenda ao escrever os momentos.
4. **Revisar a fala:** `PY montar_video.py revisar FF <video> <pasta_mesa>` aponta hesitações, palavra repetida, take repetido (fica o último) e corte que come palavra. Confira cada achado; `--aplicar` acrescenta todos aos cortes. Depois ouça as emendas numa carga só do modelo: `PY transcrever.py <pasta_mesa>/_revisao/audio-editado.wav --emendas <pasta_mesa>/_revisao/emendas.json` e compare "esperado" com "ouvido" (as pontas da janela podem cortar a primeira e a última palavra; o que importa é o meio).
5. **Preparar as peças:** leia `references/catalogo-de-estilos.md` e escreva as opções de cada momento (passo 6) com os textos reais e as `marcas` no tempo da fala. Efeitos que valem o vídeo inteiro (zoom alternado, destaques da legenda, correções) vão direto em `estilo`. Página oficial ou matéria com trecho grifado: `node scripts/capturar_pagina.js <endereco> <pasta_mesa>/midia <nome> "trecho exato"` (com `NODE_PATH` = `node_path`) e use `midia/<nome>.json` na `faixa`. Em cada peça com imagem de fora, preencha `fonte`, `prova` (o que ela pode mostrar) e `naoProva`; números e fatos vão em `fatos` [{texto, fonte, status}]; o parecer da `trava-oab` vai em `oab` {parecer, nota}.
6. **Prancha (antes de montar):** escreva no `projeto.js`:
   - `P['prancha']` = {`sugerido` (id de `FORMATOS` em `assets/catalogo/formatos.js`), `porque` (uma frase para o advogado), `alternativas` (2 ids), `chamada` {`rotulo`, `titulo`} (título curto que aparece nas prévias do visual), `quadro` opcional (tempo do original para as prévias)}.
   - `P['momentos']` = [{`id` (M1, M2...), `titulo`, `tipo` (um de `MOMENTOS` em `pecas.js`), `nivel` (1 forte, 2 importante, 3 só com "sem trecho vazio"), `inicio`, `fim`, `opcoes`: [{`id` (A, B, C), `peca` (id do catálogo), `insert` ou `efeito` com os dados reais e as `marcas` da fala, e, se houver imagem de fora, `fonte`, `prova`, `naoProva`, `oab`}]}].
   Com o visual travado pelo Catálogo (passo 3a), pule `P['prancha']`: escreva só os momentos, com 1 ou 2 opções cada.
   Rode `PY montar_video.py prancha FF <video> <pasta_mesa> MEM "<cor da marca>"` (a cor é opcional). Ele tira a paleta do cenário, desenha sobre o quadro real os pontos de partida (formato sugerido, alternativas e favoritos da memória), as cinco famílias, as legendas, as alturas e os tons, desenha as opções de cada momento no visual sugerido, deixa as animadas prontas para animar sobre o quadro (no visual que ele escolher) e ordena as opções pelo placar. Leva poucos segundos. Com o visual travado, a prancha sai curta: o visual dele sobre o quadro, sem escolha, e as opções de cada momento, com as peças pedidas no Catálogo primeiro e recomendadas. Abra `prancha.html` no navegador (seção 5); ele escolhe e copia.
   Quando ele colar: `PY montar_video.py aplicar <pasta_mesa> <texto colado>` grava o ponto de partida em `estilo.receita`, o visual (`familia`, `legenda`, `yLegenda` pela altura: alta 1150, meio 1300, baixa 1460, `cores`, `cor`, `fontes`, `moldura`, `densidade`, `ritmo`) e a velocidade; refaz os cortes de pausa no ritmo escolhido (seco: pausas acima de 0,15 s; com respiro: acima de 0,3 s; pausas mantidas: só acima de 0,8 s; cortes que tiram palavra ficam); grava cada peça como `sb-<momento>` (momentos acima da quantidade escolhida ou "sem peça" ficam vazios); e, com versão B, cria `<pasta_mesa>-b/` com o outro visual e as mesmas peças. Rode também `aprender` com o mesmo texto (placar, ponto de partida, cor da marca). Só monte depois do "sim".
   Edição rápida sem prancha ("só corta e legenda"): com pedido do Catálogo, o passo 3a já gravou o visual; sem pedido, escreva o `estilo` do último favorito (ou Editorial com `cores: "video"`). Siga para o passo 7.
7. **Conferir antes de gerar:** `PY montar_video.py quadros FF <video> <pasta_mesa> <pasta_quadros> <t1> <t2> ...` (tempos do original). Além de cada quadro (`q_<tempo>.jpg`), ele grava as folhas de contato (`folha_01.jpg`...: 9 quadros por imagem, com o tempo escrito). Olhe as folhas; abra o `q_` grande só do trecho em que algo parece errado (texto pequeno demais para ler na folha, peça perto da borda). Uma folha pesa no plano o mesmo que um quadro.
8. **Zona segura:** `PY montar_video.py zona FF <video> <pasta_mesa> [organico|impulsionado]` percorre o vídeo a cada 0,25 s (o decodificador entrega só esses quadros) e aponta texto ou gráfico atrás da interface da rede, com o quadro marcado em `_zona/`. Corrija até sair "zona segura OK". Orgânico: x de 65 a 1015, y de 220 a 1520 e nada na coluna de botões (x acima de 940 com y acima de 1150). Impulsionado (anúncio do Meta): x de 65 a 1015, y de 270 a 1248. Animação de tela cheia (diagrama) conta como fundo. O perfil conferido fica gravado em `estilo.zona`: com `impulsionado`, o motor desce os textos do alto (`TOPO` e `TOPO_TXT` + 55, e o `topo` dos modelos animados do alto), sobe os inserts de baixo para 1240, leva a `chamada` e a `palavra` para cima da cabeça e limita a legenda a 1200. Rode o `zona impulsionado` antes de `quadros` e `video`, para os dois já saírem no anúncio. `y` no insert e `topo` nos dados continuam mandando.
9. **Gerar:** `PY montar_video.py video FF <video> <pasta_mesa> <saida.mp4>`. Sai em 1080 x 1920, H.264 (até 12 Mbps), AAC, 30 quadros por segundo, cor BT.709, áudio nivelado em -14 LUFS, com a velocidade do projeto. Um vídeo de 1 minuto leva de 1 a 2 minutos num Mac recente.
10. **Favorito:** quando ele aprovar o vídeo e quiser guardar o jeito, `PY montar_video.py favorito <pasta_mesa> MEM "<nome>"`. Grava o formato e o visual do projeto (família, legenda e altura, cores, tom, fontes, moldura, quantidade de peças, corte, velocidade); mesmo nome substitui. As próximas pranchas oferecem os favoritos como pontos de partida.
11. **Alterações da Mesa:** `PY montar_video.py aplicar <pasta_mesa> <arquivo_com_o_texto_colado>` e gere de novo. Pedido escrito que o `aplicar` não resolve: mude só o campo com `juntar`. Rode também `aprender <pasta_mesa> <mesmo arquivo> MEM`: ele conta os ajustes do vídeo e mostra a comparação com o anterior.

Fim do vídeo: o `preparar` corta logo depois do fim do som da última palavra (medido no áudio, com 60 ms de folga); se a chamada final precisar de tempo na tela, ajuste o último corte à mão.

Família "atrás de você": o motor recorta a pessoa só nos trechos em que a palavra gigante aparece (ver seção 1). Sem recorte disponível, avisa e desenha como editorial.

Logo nas mãos (P56, modo `maos`): `PY scripts/rastrear_maos.py FF <video> <inicio> <fim> <pasta_mesa>/trilha.json` mede as mãos abertas no trecho e grava `marcas` e `trilhas` prontas para o insert. Precisa do mediapipe e do modelo `ferramentas/modelos/hand_landmarker.task`, ainda fora do instalador: sem eles, ele avisa e sai com código 2, e você escreve a trilha à mão (4 a 8 pontos [x, topo da mão] tirados dos `quadros`). Enquanto a logo estiver nas mãos, a legenda abaixo do queixo esbarra nela: ponha `yLegenda` no insert (ex.: 430, acima da cabeça) e a legenda sobe só nesse trecho.

Camada animada: quando o projeto tem insert `animacao`, o motor chama `scripts/animar.js` (com o `node` de `caminhos.json`), que abre o modelo de `assets/animacoes/` no navegador sem janela, grava cada quadro com fundo transparente e guarda tudo em `_anim/` (se os dados não mudarem, reaproveita). Também deixa `anim-<id>.webm` e `animacoes.js` na pasta da Mesa para a prévia (gravada no modo rápido: é só para assistir na Mesa). Cada segundo de animação leva de 2 a 4 segundos para gravar.

Faixa com vídeo: o motor extrai os quadros da mídia uma vez para `_faixa/`. Faixa com página: o marca-texto passa pelo trecho na `marca` da fala, linha a linha.

Cores: as de `estilo.cores` (hex, da `base/imagem.md` ou da paleta do padrão), `"video"` (paleta tirada do cenário) ou o padrão azul-marinho e âmbar.

Fontes: com `estilo.fontes`, o motor baixa os arquivos do par (Google Fonts, licença livre) para `ferramentas/fontes` na primeira vez (precisa de internet) e os usa no desenho e nas animações (servidos em `/fontes/` pelo gravador). Na prancha, aberta do disco, as prévias das fontes usam o Google Fonts.

Peças novas: todo modelo animado lê `base.js` (cores, família, fontes, modo Celular sem movimento, prévia com "?previa"). Uma peça nova = o modelo em `assets/animacoes/` + uma linha em `assets/animacoes/pecas.js`. Amostra estática das peças desenhadas pelo motor: `docs/fontes/gerar_amostras_pecas.py` (no projeto do Raphael, não no plugin).

## 3. Conferência

- Extraia quadros com o comando `quadros` (por exemplo, um a cada 3 segundos) e olhe as folhas de contato; o quadro grande, só onde houver dúvida. A grafia da legenda se confere pelo texto (`resumo --fala`), não pela imagem.
- Compare a duração final com a soma dos trechos mantidos.
- Confira os primeiros e os últimos 2 segundos (título e fecho).
- Arquivos temporários ficam numa pasta de trabalho dentro de `videos/` e são apagados no fim.

## 4. Plano B (sem ferramentas na máquina)

Entregue um **roteiro de edição para o CapCut ou o Edits** (aplicativos que o próprio advogado usa), em passos simples:
1. trechos a cortar, com o tempo de início e fim;
2. onde entra o título, com o texto;
3. estilo de legenda (o aplicativo gera a legenda automática; diga qual estilo escolher e quais palavras corrigir);
4. zooms e o fecho;
5. como exportar (vertical, 1080 x 1920, maior qualidade).

## 5. Abrir as páginas no navegador do computador

Prancha, prancha das cenas, Mesa, Catálogo e Vitrine carregam imagens, vídeo e listas de arquivos ao lado do `.html`. O painel de navegador do aplicativo do Claude abre só uma cópia do `.html`, sem esses arquivos: a página aparece preta, sem imagens e sem opções, com uma faixa amarela no topo ("Esta página abriu pela metade"). Por isso, abra sempre no navegador do computador, você mesmo, com o caminho completo:

| Sistema | Comando |
|---|---|
| Mac | `open "<caminho do .html>"` |
| Mac, Mesa com animação | `open -a "Google Chrome" "<caminho do .html>"` (sem Chrome, use `open`; a prévia transparente da animação só aparece certa no Chrome) |
| Windows (vale no PowerShell e no Git Bash) | `powershell -NoProfile -Command "Start-Process -FilePath '<caminho do .html>'"` (caminho com apóstrofo: troque cada ' por '') |

Depois diga ao advogado: "abri no seu navegador". Se o comando não puder rodar (por exemplo, quando você trabalha num ambiente separado do computador dele), mande o caminho completo do arquivo e peça para ele abrir com dois cliques. Nunca peça para ele procurar a pasta do plugin sozinho.

## 6. Vídeo sem rosto (formato F13, comando `cenas`)

Não há vídeo cru: o vídeo nasce do roteiro de cenas que a skill `roteiro-de-video` entrega. O motor gera o próprio original, `fundo.mp4` (a cor do fundo em 1080 x 1920, com a voz do advogado por baixo ou em silêncio), e um insert só, o modelo `cenas`, do começo ao fim. Daí em diante, `zona`, `quadros`, `video` e a Mesa funcionam como em qualquer vídeo, com `fundo.mp4` no lugar do original.

**Roteiro** (`<pasta_mesa>/../cenas.json` ou onde preferir):

```json
{ "nome": "Inventário tem prazo", "familia": "editorial", "fundo": "papel",
  "cores": { "destaque": "#C9A227", "fundo": "#14243F" },
  "oab": { "parecer": "APROVADO", "nota": "conteúdo informativo, com fonte" },
  "cenas": [
    { "tipo": "pergunta", "rotulo": "A dúvida", "texto": "inventário tem prazo?", "sugestoes": ["inventário tem multa"] },
    { "tipo": "lei", "rotulo": "A regra", "texto": "[…] deve ser instaurado dentro de 2 (dois) meses, a contar da abertura da sucessão […]",
      "destaque": "2 (dois) meses", "termo": "abertura da sucessão", "explica": "é a data do falecimento", "explicaFonte": "Código Civil, art. 1.784", "fonte": "CPC, art. 611" },
    { "tipo": "passos", "rotulo": "Como funciona", "titulo": "Como abrir o inventário",
      "passos": [{ "texto": "Reúna a certidão de óbito" }, { "texto": "Escolha: cartório ou Justiça", "ressalva": "no cartório, só com acordo de todos" }], "fonte": "CPC, art. 610" },
    { "tipo": "cuidado", "rotulo": "O cuidado", "titulo": "Passou do prazo?", "texto": "O estado pode cobrar multa no imposto.", "fonte": "STF, Súmula 542" },
    { "tipo": "fecho", "rotulo": "Para não esquecer", "chamada": "Salve este vídeo", "arroba": "@seuperfil" } ] }
```

Campos de cada tipo e ids das partes: `repertorio-de-animacoes.md`, seção 6 (e o comentário no topo de `assets/animacoes/cenas.html`). `cores` e `fontes` (id de par de `fontes.js`) são opcionais; sem `cores`, vale o padrão da família ou a cor da marca de `base/imagem.md`, que você copia para cá. `fundo: "cor"` usa a cor de fundo da marca no lugar do papel claro. Nome e OAB no fecho (`nome`, `oab`) só se ele pedir ou se o vídeo for impulsionado (CED, art. 44). Na lei, o `texto` é literal e o `destaque` e o `termo` precisam aparecer nele exatamente como escritos.

**Sem voz:**
1. `PY montar_video.py cenas FF <cenas.json> <pasta_mesa>`: lê a régua do próprio modelo (`animar.js cenas ... --regua`, menos de 10 s), grava `projeto.js`, `fundo.mp4`, `proxy.mp4` (para a Mesa) e `prancha-cenas.html`, e lista o início de cada cena e os AVISOS (bloco com mais de 7 palavras, lei ou número sem fonte, mais de 3 passos, vídeo acima de 45 s). Corrija os avisos no roteiro e rode de novo.
2. Abra a prancha das cenas (seção 5) e espere o texto colado. "Ajustar": mude o roteiro e rode `cenas` de novo. Fato marcado "tirar do vídeo": tire do roteiro. Só siga com "Tudo aprovado".
3. `zona FF <pasta_mesa>/fundo.mp4 <pasta_mesa>` e `quadros FF <pasta_mesa>/fundo.mp4 <pasta_mesa> <saida> <t1> ...` (um quadro no meio de cada cena e um em cada ponte), depois `video FF <pasta_mesa>/fundo.mp4 <pasta_mesa> <saida.mp4>`. A primeira gravação das cenas leva de 2 a 4 minutos para 40 s (o vídeo inteiro é animação); as seguintes reaproveitam o que não mudou.

**Com voz** (o advogado grava só o áudio lendo o roteiro, ou manda um vídeo de que só o som é usado):
1. `PY montar_video.py cenas FF <cenas.json> <pasta_mesa> --voz <arquivo>`: só cria `fundo.mp4` com a voz.
2. Como num vídeo comum: `transcrever.py <pasta_mesa>/fundo.mp4 ...`, `preparar FF <pasta_mesa>/fundo.mp4 <transcricao> <pasta_mesa>` e `revisar` (hesitações e tropeços saem nos cortes).
3. Em cada cena do roteiro, marque `na` com a palavra da fala em que cada parte entra (`"na": {"destaque": "dois meses", "p2": "cartório"}`); parte sem `na` segue a régua a partir da anterior.
4. `cenas FF <cenas.json> <pasta_mesa>` de novo (sem `--voz`): agora as marcas vêm da fala, e o motor avisa onde o texto pede mais tempo do que a fala dá. Siga com a prancha das cenas e a montagem como acima.

Sem voz não há legenda (o texto das cenas é o conteúdo); com voz, também não, para não brigar com o texto da tela. Música, se ele quiser, entra na hora de publicar, pela biblioteca da própria rede.

