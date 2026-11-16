# Roteiro de lâminas (carrossel.json)

Usado só no caminho B (motor próprio, sem Canva). Quem monta este arquivo é a skill `diagramacao`, a partir do texto aprovado e da estrutura em blocos da Banca.

O motor lê um arquivo JSON por carrossel, guardado em `carrosseis/AAAA-MM-DD-tema-curto/carrossel.json` na pasta do advogado. Exemplos completos em `../assets/exemplos/` (`explicativo-pensao.json`, `explicativo-pensao-com-foto.json`, `tutorial-print.json`).

## Campos do carrossel

| Campo | Obrigatório | O que é |
|---|---|---|
| `tema` | sim | título curto da rodada (aparece na prancha) |
| `tipo` | sim | explicativo, tutorial com print, mito e fato, lista |
| `estilo` | sim | código do catálogo: C01 a C06 |
| `marca` | sim | `arroba`, `nome`, `oab`, `cores` (`fundo`, `texto`, `destaque`, `apoio`, `suave`, em código #RRGGBB), `fonte_titulo`, `fonte_texto` (nomes do Google Fonts). Só o que estiver na base |
| `rodape` | não | texto curto do rodapé (ex.: a área: "Direito de família") |
| `foto_modo` | não | o modo de foto de todas as lâminas (tabela abaixo). Sem ele, vale o padrão do estilo para cada tipo de lâmina |
| `legenda` | não | a legenda aprovada; o verificador confere os vícios nela também |
| `laminas` | sim | a lista de lâminas, na ordem |

## Campos de cada lâmina, por tipo

| Tipo | Campos | Para quê |
|---|---|---|
| `capa` | `antetitulo`, `titulo`, `subtitulo`, `foto`, `foco` | o gancho. Até 22 palavras somando tudo |
| `texto` | `rotulo`, `titulo`, `texto`, `foto` ou `print` | uma ideia por lâmina |
| `passo` | `numero` (ou `rotulo`), `titulo`, `texto`, `print`, `print_descricao`, `grifos` | tutorial: um passo, um print real |
| `lista` | `rotulo`, `titulo`, `texto`, `itens`, `numerada` (padrão true), `riscar` | critérios, erros, documentos. Item pode ser texto ou `{"texto": "...", "detalhe": "..."}` |
| `mito` | `mito`, `fato`, `fonte`, `rotulo_mito`, `rotulo_fato` | o mito sai riscado à mão; o fato com a fonte |
| `numero` | `rotulo`, `numero`, `texto`, `fonte` | número grande, sempre com fonte e data |
| `regra` | `rotulo`, `titulo`, `texto`, `trecho` (lei literal, "[...]" no que for omitido) ou `itens` com `{"texto", "ref"}`, `fonte` | a base legal |
| `citacao` | `rotulo`, `trecho`, `autor` | trecho de lei, súmula ou doutrina, com autor. Nunca depoimento de cliente |
| `comparacao` | `rotulo`, `titulo`, `antes` e `depois` (cada um com `titulo` e `texto`) | o jeito errado e o certo, como se fala e como a lei chama |
| `convite` | `rotulo`, `titulo`, `texto`, `chamada`, `detalhe`, `foto` | o convite da lista de `base/oferta.md`. A assinatura (@, nome e OAB) entra sozinha |

Campos que valem para qualquer lâmina:
- `fundo`: `escuro`, `claro` ou `destaque`, para quebrar a sequência (cada estilo trata do seu jeito);
- `secao`: o texto do canto superior direito (o motor põe um padrão por tipo);
- `foto_modo`: troca o modo só nesta lâmina;
- `foco`: o ponto da foto que não pode ser cortado, como em CSS (`"50% 20%"` = centro, perto do topo).

## Fotos: os seis modos

Qualquer lâmina pode ter `foto` (e `foco`). O jeito como a foto entra é o `foto_modo`, da lâmina ou do carrossel; sem ele, vale o padrão do estilo para aquele tipo de lâmina (tabela em `catalogo-de-estilos.md`).

| Modo | Como fica | Pede foto |
|---|---|---|
| `sangrada` | a foto ocupa a lâmina inteira, com véu escuro embaixo; o texto fica claro, apoiado na parte de baixo | com espaço calmo embaixo ou no meio (fundo liso, parede, roupa escura) |
| `cartao` | uma folha lisa com o texto, centralizada sobre a foto | qualquer foto com textura ou ambiente; o rosto não precisa aparecer inteiro |
| `metade` | a foto ocupa a metade de cima, de ponta a ponta; o texto fica embaixo, no fundo liso | rosto ou objeto no terço de cima (use `foco` perto de `50% 20%`) |
| `janela` | a foto numa coluna inteira de um lado, que troca de lado a cada lâmina; o texto na outra coluna | foto em pé (retrato), pessoa no centro |
| `moldura` | a foto impressa, com borda clara, levemente girada; `legenda_foto` opcional embaixo, curta e verdadeira | foto de ambiente, bastidor, mesa de trabalho |
| `recorte` | uma foto pequena no canto, sem moldura | retrato fechado; no convite, vira o retrato redondo ao lado da chamada |

`legenda_foto`: só com fato verdadeiro e sem cliente ("o escritório, numa terça de manhã"). Nunca legenda que sugira resultado ou cliente.

O estilo C06 Pasta só aceita `moldura` e `recorte` (a foto fica dentro da folha). Cada estilo aplica um tratamento de cor único às fotos e um grão leve, para fotos de sessões diferentes conversarem.

## Marcação dentro do texto

| Escreva | Sai |
|---|---|
| `*palavra*` | o destaque do estilo (cor, itálico ou tarja). Uma por lâmina, no máximo duas |
| `**palavra**` | negrito |
| `==trecho==` | marca-texto (bom para o termo que importa na lei) |
| `~~trecho~~` | riscado à mão (o vício, o mito, o jeito errado) |
| `__trecho__` | sublinhado à mão |
| `[[palavra]]` | circulado à mão |
| quebra de linha `\n` | quebra a linha onde você quer |

## Grifos no print

`grifos` é uma lista de retângulos em porcentagem do print: `[x, y, largura, altura]`, a partir do canto superior esquerdo. Exemplo: `[[73, 82, 25, 15]]` circula o botão no canto inferior direito. Olhe o print antes de marcar e circule onde a pessoa clica ou lê.

## Caminhos de imagem

Relativos à pasta `meu-marketing-juridico/` (`fotos/selecionadas/capa-01.jpg`, `fotos/prints/print-1.png`). O motor copia as imagens para `midia/` dentro da pasta do carrossel, para a arte continuar abrindo se a foto mudar de lugar.
