# Mesa de edição (o advogado vê e ajusta a edição)

Junto com cada vídeo editado, entregue a Mesa de edição: uma página que abre com dois cliques no navegador, sem internet, onde o advogado assiste à edição como ela vai sair, ajusta e devolve as alterações para você aplicar.

## O que ela faz

- **Preview ao vivo:** toca o vídeo pulando os cortes, com os inserts na tela e na velocidade escolhida.
- **Edição pelo texto:** a fala transcrita, palavra por palavra. Clicar leva o vídeo até a palavra; clicar na primeira e, com Shift, na última, seleciona; "Cortar seleção" (ou X) tira o trecho. Os blocos "pausa" cortam ou devolvem um respiro com um clique. Palavras riscadas estão fora do vídeo.
- **Linha do tempo:** onda do áudio, cortes em vermelho, inserts em âmbar, pedidos marcados com bandeira e o cursor. Arrastar seleciona; clicar vai até o ponto; I e O marcam início e fim.
- **Inserts e efeitos:** editar os textos de cada insert (os campos mudam conforme o estilo); ajustar entrada e saída (botões "Entra agora" e "Sai agora"); ligar ou desligar; ajustar a força da aproximação.
- **Legenda:** prévia da legenda na posição final e troca do estilo por nome (Destaque, Discreta, Palavra grande, Sem legenda).
- **Pedidos ao Claude:** uma nota presa ao momento exato ("aqui o zoom ficou forte").
- **Desfazer, voltar ao original e salvamento automático** no navegador.
- **Enviar alterações ao Claude:** gera um texto pronto para colar no chat (resumo e JSON) e oferece baixar o arquivo.

## Como entregar

Para cada vídeo editado, crie `videos/editados/<tema>/mesa/` com o comando `preparar` do motor (`references/tecnico.md`), que gera `proxy.mp4` e o `projeto.js` com palavras, picos e cortes de pausa. Depois copie o `index.html` e acrescente ao `projeto.js` os inserts, os efeitos e o estilo escolhidos no catálogo. A pasta fica assim:

| Arquivo | Conteúdo |
|---|---|
| `index.html` | cópia de `assets/mesa-de-edicao/index.html` (não edite) |
| `proxy.mp4` | o vídeo ORIGINAL inteiro em versão leve (540 x 960, cor já corrigida, com áudio), na linha do tempo original |
| `projeto.js` | `window.PROJETO = {...}` no contrato abaixo |

No vídeo sem rosto (F13), o comando `cenas` faz o papel do `preparar`: a Mesa mostra a animação inteira sobre o fundo, sem texto da fala para cortar (com voz, a fala aparece como em qualquer vídeo). Ali ele assiste e deixa pedidos; texto e tempo das cenas mudam no roteiro, e você roda `cenas` de novo.

Abra o `index.html` da pasta mesa no navegador do computador (`references/tecnico.md`, seção 5) e diga ao advogado: "abri a Mesa no seu navegador. Ajuste o que quiser e, no fim, clique em Enviar alterações ao Claude e cole aqui."

## Contrato do projeto.js

```js
window.PROJETO = {
  id: "chamada-imersao-1910", nome: "Chamada da imersão", video: "proxy.mp4",
  duracao: 99.12,            // segundos do original
  velocidade: 1.1,
  picos: [0.12, 0.4, ...],   // energia do áudio a cada passoPicos segundos, de 0 a 1
  passoPicos: 0.05,
  palavras: [{ t: "Finalmente,", s: 2.40, e: 3.04 }, ...],   // transcrição corrigida, tempos do original
  cortes: [[0, 2.24], [22.25, 24.40], ...],                   // trechos FORA do vídeo, tempos do original
  inserts: [{ id: "i1", tipo: "cartao", rotulo: "...", titulo: "...", sub: "", itens: [], inicio: 8.4, fim: 10.9, ativo: true }, ...],
  efeitos: [{ id: "e1", tipo: "pb", inicio: 14.3, fim: 20.4, ativo: true }, { id: "e2", tipo: "aproximacao", inicio: 53.3, fim: 55.9, forca: 1.15, ativo: true }],
  estilo: { receita: "convite", legenda: "destaque", destaques: ["imersão", "claude"], zoomAlternado: 0.05, correcoes: { "cloud": "Claude" } },
  notas: []
};
```

Insert de animação: `{ id, tipo: "animacao", modelo: "trilha", dados: { passos: [...], rotulo: "..." }, inicio, fim, marcas, ativo }`. Na Mesa, o advogado edita os textos de `dados`; a prévia é o vídeo transparente `anim-<id>.webm` que o motor grava (abre no Chrome; em outro navegador pode aparecer sem transparência). Depois de mudar o texto, a prévia só atualiza quando você gerar de novo.

Família visual: `estilo.familia` (editorial, revista, atras, institucional) e, por insert, `familia`, `palavra` e `yGigante`. Na Mesa, o advogado troca a família do vídeo no topo e a de um título no próprio cartão do insert; a família "atrás de você" aparece na prévia com um aviso, porque o recorte só acontece no vídeo final. O pacote enviado traz `familia`, e o `aplicar` grava.

Campos opcionais de um insert: `marcas` (tempos do original em que cada linha ou item entra, no ritmo da fala) e `ocultaLegenda` (esconde a legenda enquanto o insert está na tela).

Tipos de insert e de efeito: os do catálogo (`references/catalogo-de-estilos.md`). Sem `estilo`, a Mesa e o motor não mostram legenda (compatível com projetos antigos).

## Quando o advogado colar as alterações

1. Salve o texto colado num arquivo e rode o comando `aplicar` do motor: ele troca cortes, velocidade e estilo de legenda, substitui os inserts e efeitos alterados pelo `id` e lista os pedidos. Não refaça isso à mão.
2. A Mesa já abre com a versão nova, porque o `projeto.js` foi atualizado.
3. Atenda cada pedido, mexendo só no campo necessário do `projeto.js` com o comando `juntar` (ex.: "zoom mais forte" muda a `forca` do efeito daquele momento: grave o efeito inteiro com o mesmo `id` e rode `juntar`). Para ver o que já está lá, `resumo`. Se um pedido conflitar com a OAB (ex.: colocar o valor obtido num caso), explique e proponha a alternativa.
4. Gere o vídeo final de novo com os cortes, os inserts e a velocidade novos e confira quadro a quadro (seção 4 do SKILL.md).
5. Entregue o vídeo e a Mesa atualizada, e diga em uma linha o que mudou.
