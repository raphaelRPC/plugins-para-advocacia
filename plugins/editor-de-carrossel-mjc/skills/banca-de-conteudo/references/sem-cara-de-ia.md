# Sem cara de IA

O seguidor reconhece em três segundos um carrossel feito no automático: a mesma capa de todo mundo, a frase redonda demais, a balança dourada brilhando. Esta lista vale para o texto da Banca e para a arte. Rode antes de entregar a minuta e de novo antes de exportar a arte. No texto, quem constrói e limpa é o Copywriter (orquestrador de copy, com a auditoria da `humanizar-texto`); a tabela 1 é o resumo que o verificador por script (`../../arte-do-carrossel/scripts/verificar_texto.py`) confere no fim, como última peneira. Na arte, a tabela 2 vale junto com as regras da skill `diagramacao`.

## 1. O que denuncia IA no texto

| Sinal | Troque por |
|---|---|
| Travessão (o traço longo) | vírgula, dois pontos, ponto ou parênteses |
| "Não é X, é Y" e variações ("mais do que X, Y") | afirme só o Y |
| Lista de três por reflexo, adjetivos em trio | a quantidade que o assunto tem |
| Emoji no título ou um emoji por linha | nenhum no título; no corpo, só se o advogado usa |
| "Descubra", "desvende", "potencialize", "jornada", "no mundo de hoje" | o verbo do dia a dia ("veja", "confira", "faça") |
| Frase de efeito fechando cada lâmina | termine na informação |
| Todas as lâminas com o mesmo tamanho e o mesmo ritmo | varie: uma lâmina de uma linha, outra com lista curta |
| Exemplo genérico ("um cliente", "uma empresa") | situação concreta e fictícia declarada ("imagine a Ana, que...") ou o caso de uso da base |
| Palavras que o advogado nunca usaria | as palavras da seção "Voz" da base |

A voz vem da base, nunca da IA. Sem a seção "Voz" preenchida, avise que o texto vai sair com voz neutra e peça de 3 a 5 textos reais do advogado (legenda antiga, áudio transcrito, resposta a cliente sem dados pessoais).

## 2. O que denuncia IA na arte

| Sinal | Troque por |
|---|---|
| Rosto, mão ou escritório gerado por IA | foto real do advogado (`fotos/selecionadas/`) |
| Martelo, balança dourada, estátua da Justiça, livro com brilho | foto real, print real ou só tipografia |
| Interface de programa desenhada (chat, painel, tela de celular inventada) | print real da tela, tirado pelo advogado |
| Degradê roxo e azul, ícones 3D brilhantes, fundo de "tecnologia" | as cores e fontes do `base/imagem.md` |
| Modelo pronto sem nenhuma troca, igual ao de todo mundo | um modelo da biblioteca (Árvore de Links) sempre com a identidade fixa do advogado: cores, fontes, ênfase, fotos e assinatura |
| Imagem gerada, ilustração ou composição de IA quando falta foto | design flat: fundo liso da marca e o texto |
| Texto miúdo para caber tudo | menos texto na lâmina; o resto vai para a legenda |
| Cada lâmina com um layout diferente | a grade fixa do modelo ou do estilo, com variação de peso (lâmina curta, lista, fundo escuro) |

## 3. O que dá cara de gente

- **Print real.** Num tutorial, a prova é a tela de verdade. Peça ao advogado o print de cada passo e guarde em `fotos/prints/`. Sem print, a lâmina fica marcada `[PRINT A CAPTURAR]`; nunca desenhe a tela.
- **Foto real** do advogado na capa ou no convite.
- **Marca de mão:** grifo, círculo ou seta sobre o print, como quem marca um documento.
- **Primeira pessoa e bastidor:** "como eu faço", "o pedido que eu uso", desde que seja verdade.
- **Número com fonte** e nada que o advogado não tenha vivido.

## 4. Referência de formato

Quando o advogado mostra um carrossel de outro perfil ("faz um carrossel como esse"), leve só a estrutura:

1. Conte as lâminas e anote a função de cada uma (capa, problema, passo, resultado, convite).
2. Anote o tipo de visual de cada uma (print, foto, só tipografia, mockup) e o tamanho do texto.
3. Descreva o recurso de destaque (palavra colorida, caixa, grifo).
4. Registre em `base/imagem.md`, seção "Referências de formato", com o link e a data.

Nunca leve o texto, o bordão, a marca, o gancho literal, as fotos ou a palavra-chave do convite. Se a referência promete resultado ("viralizar em 30 dias", número de visualizações), a estrutura pode vir e a promessa fica de fora. Convite de comentário com palavra aleatória para receber material passa pela Trava OAB antes de entrar.

## 5. Checklist (rode em silêncio)

- [ ] Zero item da tabela 1 no texto.
- [ ] Soa como a seção "Voz" da base.
- [ ] Zero item da tabela 2 na arte.
- [ ] Toda tela mostrada é print real ou está marcada `[PRINT A CAPTURAR]`.
- [ ] Foto real do advogado onde houver rosto.
- [ ] Da referência, só a estrutura.
