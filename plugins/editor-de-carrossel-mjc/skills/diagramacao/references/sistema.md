# Sistema: os números

Vieram de três fontes: regras consolidadas de design editorial e de tela, as medidas das 15 referências estudadas no projeto do curso e a conta de como a lâmina aparece no celular.

**Como valem em cada caminho.** No Canva, quem dá as medidas do layout é o modelo. Estes números são o piso que nenhum layout fura (corpo mínimo, contraste, área segura) e a régua para criar lâminas novas quando o modelo não cobre. No motor próprio (caminho B), os 6 estilos ainda estão sendo alinhados a estes números (pendência da versão 1.1.0, ver `MUDANCAS.md` na raiz do plugin): até lá, vale o que cada estilo define, e você segue estes números nas decisões (divisão em lâminas, quantidade de texto).

## A conta do celular

A lâmina tem 1080 px de largura e aparece com cerca de 390 pontos no celular: cada pixel vira mais ou menos um terço. Um corpo de 33 px aparece com uns 12 pontos, e a leitura confortável pede de 14 a 15. Por isso:

- **corpo padrão: 40 px;**
- **mínimo absoluto para texto de leitura: 36 px.**

Rótulo, rodapé e fonte da regra (até 5 palavras) podem ir a 27 px, em caixa alta com espaçamento de letras de +0,08.

## Escala tipográfica (razão 1,5)

| Uso | Tamanho |
|---|---|
| Rótulo, rodapé, fonte | 27 px |
| Corpo | 40 px |
| Subtítulo, destaque | 60 px |
| Título do miolo | 90 px |
| Título de capa | 135 px |
| Palavra de impacto | 200 px |

Os tamanhos só andam por degraus da escala. Nada de valores intermediários. A razão entre título e corpo fica entre 2,25 e 5.

No Canva, a escala do modelo prevalece; quando você mudar um tamanho, mude para um degrau próximo ao que o modelo já usa, nunca para um valor solto.

## Régua de espaço (múltiplos de 8)

| Espaço | Uso |
|---|---|
| 16 px | dentro do grupo: rótulo e título, título e subtítulo |
| 24 px | entre linhas de uma lista, entre item e detalhe |
| 40 px | entre grupos: título e corpo, corpo e lista |
| 64 px | entre blocos maiores: conteúdo e foto, conteúdo e botão |
| 104 px | margem lateral e grandes respiros |

**Proximidade:** o espaço dentro de um grupo é sempre menor que o espaço entre grupos.

## Grade, margem e área segura

| Medida | Valor |
|---|---|
| Lâmina | 1080 x 1350 (4:5) |
| Margem lateral | 104 px (generosa: 144) |
| Topo e base | 80 px; cabeçalho e rodapé moram nessa faixa |
| Corte da grade do perfil (3:4) | cerca de 34 px de cada lado; nada importante ali |
| Coluna do corpo | 560 a 760 px (30 a 45 caracteres por linha) |
| Entrelinha | título 0,9 a 1,0; corpo 1,35; rótulo 1,2 |
| Espaço de letras | título -0,02 a -0,04 em; rótulo +0,08 em |

## Contraste

- Corpo: 4,5:1. Título de 60 px ou mais: 3:1.
- Fonte fina conta como texto normal: 4,5:1 sempre.
- Texto sobre foto: meça sobre a área real onde o texto senta, com véu ou degradê só ali.
