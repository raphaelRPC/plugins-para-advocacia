# Régua de peso

Como o plugin traduz o uso medido em leve, médio, pesado e muito pesado. Tudo aqui é estimativa: a Anthropic não publica quantos tokens (a unidade de texto que o Claude conta) cabem no limite de cada plano, nem como cada tipo de token pesa no limite.

## O cálculo (scripts/uso.py)

Para cada resposta do Claude, o histórico da conversa no Claude Code registra quatro números. O plugin soma cada um com um fator tirado da proporção dos preços públicos da Anthropic por token (entrada vale 1):

| Número registrado | O que é | Fator |
|---|---|---|
| Entrada nova | Texto novo enviado ao Claude | 1 |
| Escrita de cache | Texto guardado na memória curta para as próximas respostas (instruções, arquivos lidos, retomada depois de pausa) | 1,25 (memória de 5 minutos) ou 2 (memória de 1 hora) |
| Leitura de cache | O histórico reenviado a cada mensagem, já guardado | 0,1 |
| Saída | Texto escrito pelo Claude | 5 |

E por modelo, também pela proporção dos preços: Opus 5/3, Sonnet 1, Haiku 1/3.

Uma conversa retomada repete o histórico da anterior; o resumo não conta a mesma resposta duas vezes. Subagentes (ajudantes que o Claude abre durante a tarefa) entram na conta da conversa que os abriu.

## As faixas (provisórias)

Em mil pontos de peso. Calibradas em 16/10/2026 com 226 conversas do Claude Code do Raphael (uso de desenvolvimento, com muitos conectores ligados, então mais pesado que o de um advogado típico): um quarto ficou abaixo de 600, metade abaixo de 1.170, três quartos abaixo de 2.900. Uma pergunta curta, com poucas respostas, ficou perto de 400.

| Faixa | Pontos |
|---|---|
| leve | abaixo de 500 |
| médio | de 500 a 2.500 |
| pesado | de 2.500 a 10.000 |
| muito pesado | acima de 10.000 |

**A calibrar** com o teste da equipe: comparar o peso de cada conversa com o percentual da linha de status antes e depois. Mudou a faixa? Atualize `FAIXAS` no `uso.py` e esta tabela no mesmo ato.

## A comparação

Só com dado do próprio advogado, dos últimos 30 dias:
- com 3 ou mais conversas de minuta (Banca de Conteúdo): "como 4 das suas conversas de minuta";
- senão, com 5 ou mais conversas registradas: "3 vezes uma conversa típica sua";
- com menos que isso, sem comparação.

## Sem registro (Cowork, aplicativo): estimativa por tarefa

Quando o plugin não mede, use esta tabela e diga que é estimativa. Ela vem do que cada tarefa faz, sem medição.

| Tarefa | Peso estimado | Por quê |
|---|---|---|
| Trava OAB de um texto curto | leve | lê a regra e um texto |
| Uma minuta com versões (Banca de Conteúdo) | médio | escreve vários textos |
| Arte do carrossel pelo motor | leve | o desenho é feito por script; o Claude confere uma prancha só |
| Arte no Canva | médio | conversa com o Canva e confere a arte página por página |
| Edição de um vídeo de até 2 minutos, com prancha | pesado | lê as instruções da edição, escreve os momentos e confere quadros por imagem |
| Fase do Rito PICO com acervo grande | pesado | lê o material do advogado |
| Lote de vídeos ou Rito inteiro numa conversa só | muito pesado | a conversa cresce e cada mensagem reenvia tudo |

O que roda no computador do advogado (transcrição, cortes, montagem do vídeo, verificação da zona segura) não pesa no plano: o Claude só lê o resumo que o comando imprime.
