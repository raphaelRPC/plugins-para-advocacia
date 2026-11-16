# Catálogo de estilos

Seis estilos escritos do zero a partir da análise de 15 carrosséis de referência (só a forma: grade, hierarquia, cor, tipografia, ritmo). As fichas das referências ficam no projeto do curso, em `pesquisa/referencias-carrossel/`. Nenhum texto, foto ou marca das referências entra no plugin.

O catálogo visual, com o mesmo carrossel montado em cada estilo, está em `../assets/catalogo/catalogo.html`.

## Os estilos

| Código | Nome | Como é | Bom para | Evite |
|---|---|---|---|---|
| C01 | Caderno | papel claro com textura, título condensado em caixa alta, palavra na cor de destaque, marcas de caneta (grifo, risco, círculo) | tutorial com print, lista de erros, mito e fato | tema delicado (luto, violência), em que a caneta parece leve demais |
| C02 | Ensaio | página de revista: serifa condensada enorme, itálico na palavra-chave, texto curto, lados que alternam a cada lâmina, fio que sangra para a próxima | explicativo, uma ideia por lâmina, regra com a lei literal | tutorial com muitos prints |
| C03 | Gabinete | fundo escuro e quente com luz difusa, serifa leve, "Passo N" circulado à mão, bolinhas de progresso | passo a passo, checklist antes de um ato, explicativo em tópicos | marca que exige fundo claro |
| C04 | Retrato | foto real sangrada com véu e grão, serifa na cor de destaque, itálico, detalhes datilografados; sem foto, fundo escuro com grão | capa forte, bastidor da rotina, número com fonte, convite | quem não tem foto própria; lista longa |
| C05 | Cartaz | grafite com feixe de luz, caixa alta larga, itálico fino, uma lâmina clara para virar o jogo | mito e fato, comparação, "como se fala e como a lei chama" | tema que pede acolhimento |
| C06 | Pasta | folha creme numa pasta com aba sobre fundo colorido, título grotesco, rótulos entre colchetes, "01 \|" | lista de documentos, checklist, regra com a lei literal | capa só com foto |

## Qual estilo para qual carrossel (o caminho "sugere")

| Tipo de carrossel | Primeira opção | Alternativa |
|---|---|---|
| Explicativo (um tema jurídico) | C02 Ensaio | C03 Gabinete |
| Tutorial com print | C01 Caderno | C03 Gabinete |
| Mito e fato | C05 Cartaz | C01 Caderno |
| Lista de erros ou critérios | C01 Caderno | C05 Cartaz |
| Lista de documentos, checklist | C06 Pasta | C03 Gabinete |
| Regra com a lei literal | C02 Ensaio | C06 Pasta |
| Número com fonte, novidade jurídica | C04 Retrato | C02 Ensaio |
| Bastidor da rotina, apresentação | C04 Retrato (com foto real) | C02 Ensaio |

Depois, ajuste pela base: marca sóbria e tradicional puxa para C02, C03 e C06; marca direta e jovem, para C01 e C05; quem tem ensaio de fotos bom aproveita o C04.

## Cores e fontes da marca em cada estilo

O estilo decide quais cores da marca aceita, para não perder o desenho:

| Estilo | Usa da marca | Fica do estilo |
|---|---|---|
| C01 Caderno | fundo, texto, destaque, apoio | textura e fontes |
| C02 Ensaio | fundo, texto, destaque | fios na cor de destaque |
| C03 Gabinete | destaque (a luz e as ênfases) | o fundo escuro e quente |
| C04 Retrato | destaque (o título) | o véu e o fundo escuro |
| C05 Cartaz | destaque (risco e ênfase) | o grafite |
| C06 Pasta | destaque (aba, tarja), apoio (a mesa) | a folha creme |

Fontes da marca (`fonte_titulo`, `fonte_texto`) substituem as do estilo em qualquer um. Avise quando a troca enfraquece o estilo (uma sans no título do C02 tira a cara de revista) e deixe o advogado decidir.

O motor confere o contraste e avisa no relatório quando o texto sobre o fundo fica abaixo de 4,5:1 ou o destaque abaixo de 3:1.

## Foto em cada estilo

Padrão de modo por tipo de lâmina (o advogado ou você podem trocar em qualquer lâmina) e o tratamento de cor da foto:

| Estilo | Capa | Texto | Número e citação | Convite | Tratamento |
|---|---|---|---|---|---|
| C01 Caderno | moldura | moldura | recorte | retrato redondo | cor natural, um pouco mais quente |
| C02 Ensaio | janela | metade | janela | retrato redondo | menos saturada, tom de papel |
| C03 Gabinete | sangrada | cartão | sangrada | retrato redondo | quente, mais escura |
| C04 Retrato | sangrada | sangrada | sangrada | sangrada | menos saturada, contraste alto |
| C05 Cartaz | sangrada | metade | sangrada | retrato redondo | preto e branco |
| C06 Pasta | moldura | moldura | recorte e moldura | retrato redondo | cor natural (só moldura e recorte) |

Como escolher a foto para cada modo está em `roteiro.md`, seção "Fotos: os seis modos". Regra de ouro do minimalismo: uma foto por lâmina, e no máximo metade das lâminas com foto. As lâminas sem foto dão o respiro. Exceção: o C04 Retrato pode passar da metade, mas nunca repete foto; sem fotos suficientes, as lâminas restantes saem em fundo escuro, sem foto.

## Regras que valem para todos (vieram das referências)

1. **Grade fixa, margem larga** (de 70 a 108 px nas laterais). Título e corpo na mesma posição em todo o miolo.
2. **Um ponto de ênfase por lâmina.** Negrito por toda parte é o que mais denuncia IA.
3. **Escala com contraste:** título de 2,5 a 6 vezes o tamanho do corpo, entrelinha apertada no título (0,85 a 1,0).
4. **Uma marca humana por lâmina:** risco, círculo, sublinhado, fio torto, foto levemente girada. Uma, não três.
5. **Foto real com véu**, nunca banco de imagem limpo nem imagem gerada.
6. **O carrossel mostra onde o leitor está:** número da lâmina, bolinhas ou seta, e a última lâmina diferente (cor invertida, convite).
7. **Ritmo:** alterne lâmina de frase curta, de lista, com foto ou fundo escuro.

## O que ficou de fora das referências, de propósito

- Lâmina de depoimento de cliente (vedada pelo Provimento 205/2021 e pelo Código de Ética).
- Janelas de aplicativo desenhadas, como se fossem prints (interface inventada).
- Fotos de luxo, viagem ou bens (ostentação).
- Balanço de "conquistas" e números de resultado.
- Ícones de curtir, comentar e enviar imitando a interface do Instagram.
