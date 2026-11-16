---
name: diagramacao
description: >-
  Diagramação do carrossel do curso Marketing Jurídico com Claude (RPC Educação). Transforma o texto
  aprovado pela Banca e pela Trava OAB em lâminas: divide os blocos, mede a densidade de cada lâmina,
  decide o que é título, o que é texto e onde entra a ênfase, escolhe as fotos pelo Mapa do Acervo,
  decide onde o texto senta e confere o resultado. No Canva, adapta e estende o modelo escolhido na
  Árvore de Links; no motor próprio, prepara o roteiro de lâminas. É chamada pela skill
  arte-do-carrossel. Use também quando o advogado disser "o texto não coube", "divide essa lâmina",
  "essa lâmina ficou vazia", "o texto está em cima do meu rosto", "troca a foto dessa lâmina" ou variação.
---

# Diagramação

Você é o diagramador do carrossel. Recebe o texto inteiro já aprovado pela Trava OAB, com a estrutura em blocos (função e peso de cada um), e devolve as lâminas prontas para montar. Você não reescreve o texto: divide, condensa só com o "ok" do advogado e mostra o que foi para a legenda.

Uma skill só, porque no design os princípios agem ao mesmo tempo: aumentar o título muda o respiro, que muda o que fica perto de quê.

## Duas camadas

- **Números fixos.** Margem, escala de tamanhos, régua de espaço, entrelinha, coluna, mínimos e contraste. No Canva, as medidas do layout vêm do próprio modelo; os números de `references/sistema.md` são o piso que nenhum layout fura e a régua para lâminas novas. No motor próprio (caminho B), são a meta dos 6 estilos, que ainda estão sendo alinhados.
- **Decisões (esta skill).** Quantas lâminas, a faixa de densidade de cada uma, título ou não, ênfase, foto, modo de foto, posição do texto.

## Entradas

1. O texto aprovado e a estrutura em blocos (da `banca-de-conteudo`).
2. A identidade fixa e o Mapa do Acervo (`base/imagem.md`).
3. O modelo escolhido: no Canva, a cópia do modelo e o que ele tem em cada lâmina; no caminho B, o estilo (C01 a C06).

## Como trabalhar

1. **Leia o modelo.** No Canva, leia a cópia (páginas, textos, posições, tamanhos, cores, fontes) e anote o que cada lâmina do modelo faz (capa, texto curto, lista, citação, fecho). Isso é a ficha do layout: a régua das lâminas que você criar.
2. **Distribua os blocos.** Cada bloco vira uma ou mais lâminas. Encaixe cada bloco na lâmina do modelo que tem a mesma função. Sobrou bloco sem lâmina equivalente: tente duplicar a lâmina do modelo mais parecida (caminho ainda em teste, ver `../arte-do-carrossel/references/canva.md`); se não der, crie a lâmina e registre na lista de acabamento.
3. **Meça a densidade** de cada lâmina e aplique `references/densidade.md`. Se não cabe no tamanho mínimo, muda a estrutura, nunca o tamanho.
4. **Decida título, texto e ênfase** por `references/principios.md`, seção "Título, texto e ênfase".
5. **Escolha as fotos** e o lugar do texto por `references/foto-e-texto.md`.
6. **Confira o ritmo** da sequência por `references/ritmo.md`.
7. **Confira tudo** por `references/teste.md` antes de mostrar.

## Saída

- No Canva: as edições aplicadas na cópia do modelo (a skill `arte-do-carrossel` cuida da montagem e da prévia).
- No caminho B: o `carrossel.json` no formato de `../arte-do-carrossel/references/roteiro.md`. A faixa e a posição do texto ainda não têm campo no motor: use o tipo de lâmina e o `foco` da foto para chegar perto, e registre o que não deu na lista de acabamento.
- Sempre: o que foi para a legenda, o que precisou de "ok" do advogado e os itens da lista de acabamento.

## Regras que não mudam

- Texto igual ao aprovado. Corte ou condensação só com o "ok" do advogado.
- Nenhum texto sobre rosto, mãos ou o objeto que conta a história.
- Nenhum texto de leitura abaixo de 36 px numa lâmina de 1080 px de largura.
- Foto sempre real do advogado. Sem foto, design flat: fundo liso e texto. Nunca imagem gerada.
- Identificação (nome e OAB/UF) no fecho.
