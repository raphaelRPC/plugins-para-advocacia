---
name: sustentacao-oral
description: >
  Prepara a sustentação oral no tribunal: roteiro cronometrado de 10 a 15 minutos (ou o
  tempo do regimento, sempre a conferir), com o que se pede, os fatos com a folha, o ponto
  central e a resposta ao argumento contrário; um script conta as palavras e diz se cabe no
  tempo e em que minuto cada parte começa. Junta o memorial curto para o gabinete, as
  perguntas prováveis dos julgadores com respostas de 30 segundos e a versão para quando o
  tempo for cortado. Use quando o advogado disser "vou sustentar", "monta o roteiro da
  sustentação", "faz o memorial", "o que o relator pode perguntar", "isso cabe em 15
  minutos?", "cronometra meu roteiro".
  Não use para a audiência de instrução com testemunhas nem para a peça do recurso (use
  minutar-peca).
---

# Sustentação oral

> Uma fala que cabe no tempo, começa pelo pedido, mostra a folha de cada fato e já sabe responder às três perguntas mais prováveis.

Regras do plugin: `../../docs/regras.md`. Citação: `../../docs/citacoes.md`. Produção e pasta do caso: `../../docs/producao.md`. Fichas: `../../docs/ficha-do-escritorio-modelo.md`, `../../docs/ficha-juridica-modelo.md` e a tabela em `../../docs/ficha-juridica.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Quinta, 13h40. A sessão começa às 14h. A advogada tem um texto de quatro páginas, escrito para ler, e o presidente avisa que cada parte tem o tempo do regimento. No minuto oito ela ainda está nos fatos, e o ponto central, o laudo da folha 43, fica para "Vossas Excelências verão nos autos".

**Regras fixas desta habilidade:**
1. O tempo do regimento é sempre `[CONFERIR]` no regimento interno do tribunal, assim como inscrição, ordem de fala e forma (presencial, vídeo, gravada). A habilidade nunca afirma o tempo de memória.
2. Cada fato da fala tem a folha. Cada citação na fala está conferida; o que não foi conferido não é dito.
3. Nada de promessa ou previsão ("o resultado é certo", "o relator vai acompanhar"). Força de argumento em palavras, nunca percentual.
4. Quem fala, se inscreve e entrega o memorial é o advogado (ou quem ele indicar). A habilidade prepara o material.
5. O memorial é curto (até 2 páginas, ou o que a ficha definir) e sai com o cabeçalho interno "Antes de enviar" separado do texto.

## 1. Quando usar

**Use quando:**
- O recurso ou a ação entrou em pauta e o advogado vai sustentar.
- O advogado quer entregar memorial ao gabinete antes do julgamento.
- O roteiro existe e a pergunta é "cabe no tempo?" (modo "cronometrar").
- O advogado leu em voz alta e quer ajustar ao ritmo dele (modo "ensaio").
- Treino com o caso fictício, ou a `adaptar-juridico` (se instalada) pediu o costume dos tribunais do escritório (modo "adaptar").

**Não use quando:**
- É audiência de instrução, com depoimento e testemunhas: a preparação é outra (perguntas, ordem, documentos); para o cliente, a `preparar-o-cliente`, do motor-experiencia (se instalado).
- O pedido é a peça escrita do recurso: `minutar-peca` (se instalada).
- O pedido é decidir se vale sustentar: é do advogado, e a `estrategia-do-caso` ajuda a organizar.

## 2. Antes de começar

1. **Leia as fichas** (`ficha-do-escritorio.md` e `ficha-juridica.md`, em `escritorio/04-base/comum/`), `nicho.md` (se existir) e `04-base/juridico/nicho/sustentacao-oral.md` (costume de cada tribunal, do modo adaptar).
2. **Leia os aprendizados** (`escritorio/04-base/comum/aprendizados-juridico.md`).
3. **Sem ficha:** ofereça `/motor-juridico:comecar`. Para seguir, pergunte só: "Em que tribunal e órgão vai ser o julgamento, e quando?".
4. **Leia o caso** em `escritorio/07-operacao/juridico/casos/<codigo>/`: `leitura-dos-autos.md` (fatos com a folha), `estrategia.md` (o pedido e a tese), `contraditorio.md` (os argumentos do outro lado), a peça do recurso e as contrarrazões. Sem leitura dos autos, peça a cópia do processo ou rode antes a `leitura-dos-autos` (se instalada).
5. **Pergunte o tempo**, uma vez: "Quanto tempo o regimento dá para cada parte nesse órgão? Se você ainda não conferiu, eu deixo marcado para conferir e monto para 15 minutos." Sem o número conferido, o roteiro fica com `tempo_do_regimento: [CONFERIR]`.
6. **Citações** da fala e do memorial: da base do escritório ou da peça já conferida (`conferir-citacoes`, se instalada). O resto nasce marcado.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | J: `tribunais_principais` |
| Melhora | J: `estilo` |

`tribunais_principais` diz onde o escritório sustenta e quais costumes guardar no modo adaptar. `estilo` vale para o memorial. O limite de páginas do memorial segue `tamanho_preferido`, se a ficha tiver; sem ele, 2 páginas.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Completo | Recurso em pauta | O caso (autos, estratégia, contraditório) | Roteiro, cronômetro, perguntas prováveis, memorial e checklist do dia |
| Só memorial | Entrega ao gabinete | O caso | O memorial, com o cabeçalho interno |
| Cronometrar | O roteiro já existe | O roteiro | O quadro do script e o que cortar |
| Ensaio | Depois de ler em voz alta | O tempo que levou | O ritmo de quem fala, gravado no roteiro, e o cronômetro de novo |
| No ciclo | Linha do `pecas.csv` com `peca = memorial` ou `sustentacao`, em `tese-definida` | O caso | Rascunho na fila. Não mostra nada |
| Treino | Caso fictício | Caso 1 | O mesmo, em `_treino/`, e a diferença com a seção 4.5 |
| Adaptar | A `adaptar-juridico` chama | Ficha e tribunais | Costume de cada tribunal, para aprovar |

### Passo 1. O que se pede e o ponto central
Em uma frase, o que se pede ao órgão (manter a sentença, reformar em tal ponto). Depois, o ponto central: o argumento que decide, com a prova e a folha. No máximo dois pontos. Pergunte ao advogado, se não estiver claro na estratégia: "Se o relator lembrar de uma coisa só da sua fala, qual é?".

### Passo 2. Os fatos que decidem
Da leitura dos autos, só os fatos que mudam o resultado, cada um com a folha. Data, valor e nome conferidos contra o dossiê. Fato que diverge entre documentos: diga a versão conferida e onde está, ou deixe fora da fala.

### Passo 3. O argumento contrário
Do `contraditorio.md` (se existir) ou das contrarrazões: o argumento mais forte do outro lado e a resposta, com a folha. Sem contraditório, use o que a outra parte disse nos autos.

### Passo 4. Escrever o roteiro
No formato de `assets/modelo-roteiro.md`: seis partes com tempo planejado no título, somando o tempo do regimento menos a folga (padrão: 15 minutos com 10% de folga, até o tempo ser conferido). Escreva para falar: frases curtas, uma ideia por frase, sem leitura de ementa longa, número de folha dito em voz alta ("folha quarenta e três"). Notas para quem fala ficam em linhas com `>` e não contam no tempo.

### Passo 5. Cronometrar
Rode o script (seção 4.3). Parte que passa do planejado: corte ali (o script diz quantas palavras). Total que passa do tempo ou come a folga: corte na parte 3 primeiro (fatos), nunca no pedido. Rode de novo até "CABE".

### Passo 6. Versão curta e perguntas prováveis
Escreva a versão para metade do tempo (as partes 1, 2, 4 e 6) e o que dizer se o relator adiantar o voto. Monte as perguntas prováveis (seção 4.2), cada uma com a resposta em até 30 segundos e a folha.

### Passo 7. Memorial
No formato de `assets/modelo-memorial.md`: o pedido, os fatos com a folha, o ponto central, a resposta ao argumento contrário, o pedido numerado como na peça. Até 2 páginas. O cabeçalho "Antes de enviar" lista o que conferir e sai antes da entrega.

### Passo 8. Checklist do dia
Inscrição para sustentar (forma e prazo `[CONFERIR]`), link ou sala, horário da sessão, cópia do roteiro em letra grande, folhas marcadas no PDF, água, versão curta à mão. Quem faz cada item: a pessoa da ficha (`quem_assina` fala; quem a ficha disser inscreve).

### Passo 9. Mostrar e gravar
Mostre o resumo (seção 5). Grave com o ok. No `pecas.csv`, se a sustentação ou o memorial têm linha, a etapa vai a `minuta`; dali em diante, só o advogado move. Peça ao advogado para ler o roteiro em voz alta uma vez com o cronômetro do celular e contar quanto levou (modo ensaio).

### Passo 10. Aprender
Depois da sessão, pergunte: "O que o relator perguntou que não estava na lista? Quanto tempo deu de verdade?". As respostas viram regra curta em `aprendizados-juridico.md` (com o ok) e, se forem do costume do tribunal, em `04-base/juridico/nicho/sustentacao-oral.md`. Tempo conferido no regimento: ofereça guardar ali, com a data da conferência.

### Modo ensaio
O advogado diz quantos minutos levou lendo uma parte (ou o roteiro inteiro). Ritmo = palavras da parte divididas pelos minutos. Grave `ritmo` no cabeçalho do roteiro e rode o script de novo. Ritmo acima de 160 palavras por minuto: sugira cortar texto em vez de falar mais rápido.

### Modo no ciclo
1. Só com linha no `pecas.csv` com `peca` igual a `memorial` ou `sustentacao` e etapa `tese-definida`. Não pergunte nada e não mostre nada.
2. Rode os passos 1 a 7 com `tempo_do_regimento: [CONFERIR]` e o cronômetro para 15 minutos.
3. Grave o roteiro e o memorial e um item na fila (`escritorio/07-operacao/juridico/fila/AAAA-MM-DD/NN-<codigo>-sustentacao.md`), no formato de `agentes-e-fila.md`: `para: advogado`, `canal: interno`, `tipo: sustentacao`, `revisor: pendente`, `prazo` (o prazo interno do `pecas.csv`) e, em `antes_de_enviar`, o tempo a conferir, a inscrição a fazer e as citações por conferir.
4. Etapa: só `minuta` e `atualizado_em`. Nunca inscreve, nunca entrega memorial.

### Modo treino
Cenário de treino: o caso 1 (Marta, `../../docs/casos-ficticios.md`), depois da sentença favorável, com recurso do INSS dizendo que a perícia administrativa prevalece e que a incapacidade é só parcial. Use os autos de treino da `leitura-dos-autos` (se instalada; o laudo está nas fl. 43 a 48) e o contraditório de treino da `advogado-do-diabo` (se instalada). Tempo de treino: 10 minutos (valor de exemplo; no caso real, `[CONFERIR]`). Grave em `escritorio/07-operacao/_treino/juridico/casos/C-2026-0001/sustentacao/`. Mostre a diferença com a seção 4.5.

### Modo adaptar
1. Leia a ficha (`tribunais_principais`) e os aprendizados.
2. Para cada tribunal e órgão onde o escritório sustenta: o tempo (com a data da conferência no regimento, ou `[CONFERIR]`), como se inscreve, a forma, a saudação de costume, se o órgão costuma adiantar voto, como entregar memorial. Tudo dito pelo advogado ou conferido no regimento.
3. Marque `[NOVO]` ou `[ALTERADO]`, mostre e pergunte: "É assim que funciona nesse órgão hoje?".
4. Com o ok, grave em `04-base/juridico/nicho/sustentacao-oral.md`.

## 4. Critérios

### 4.1 As partes do roteiro (padrão de 15 minutos)
| Parte | Tempo | O que tem |
|---|---|---|
| 1. Abertura | 0:30 | Saudação de costume `[CONFERIR]`, quem você representa, o que está em julgamento |
| 2. O que se pede | 0:45 | O pedido em uma frase |
| 3. Os fatos que decidem | 3:00 | Três a cinco fatos, cada um com a folha |
| 4. O ponto central | 4:00 | Um ou dois argumentos, com a prova e a citação conferida |
| 5. A resposta ao argumento contrário | 2:00 | O argumento mais forte deles e a resposta |
| 6. Fecho e pedido | 0:45 | Volta ao pedido |

Somam 11 minutos: a sobra é a folha de tempo para interrupção, pergunta e respiração. Com outro tempo conferido, mantenha as proporções e a folga.

### 4.2 Perguntas prováveis
Monte de cinco a oito, nesta ordem de onde vêm:
1. Os argumentos fortes e médios do `contraditorio.md`.
2. As contradições e lacunas do dossiê e da leitura dos autos ("qual data vale?", "por que não há documento depois de tal data?").
3. O ponto em que a decisão recorrida foi mais dura.
4. O efeito prático do pedido ("se acolhido, o que muda?").
Cada resposta em até 30 segundos, com a folha. Resposta que depende de jurisprudência: só a conferida.

### 4.3 O cronômetro
Rode com o caminho da pasta desta habilidade. No plugin instalado, ela é `${CLAUDE_PLUGIN_ROOT}/skills/sustentacao-oral`; sem a variável, use o caminho da pasta desta habilidade.

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/sustentacao-oral/scripts/cronometro.py" \
  "escritorio/07-operacao/juridico/casos/C-2026-0001/sustentacao/roteiro.md" \
  --tempo 15 --ritmo 130 --folga 10
```

O `scripts/cronometro.py` conta as palavras faladas de cada parte (títulos `##` com o tempo entre parênteses, como `(2:00)` ou `(2 min)`; notas com `>`, tabelas e seções sem tempo no título não contam), estima o tempo pelo ritmo, compara com o planejado e com o total e diz "CABE", "SEM FOLGA" ou "PASSA DO TEMPO", com quantas palavras cortar e em que minuto cada parte começa. `--tempo` aceita 15, 12,5 ou 12:30; sem ele, usa `tempo_do_regimento` do cabeçalho; com `[CONFERIR]`, avisa e compara só com o planejado. Arquivo que não existe, vazio ou sem parte com tempo: código 1 e a mensagem.

### 4.4 Memorial
Até 2 páginas (ou `tamanho_preferido`). Sem fato novo que não esteja nos autos. Sem citação não conferida. O mesmo pedido da peça, com a mesma numeração. O cabeçalho "Antes de enviar" sai antes da entrega.

### 4.5 Conferência com o caso de treino
No cenário de treino do caso 1, com `--tempo 10`:

| Tem que ter | Não pode ter |
|---|---|
| `tempo_do_regimento: [CONFERIR]` no cabeçalho e o aviso do tempo de treino como exemplo | Tempo do regimento afirmado de memória |
| O pedido na parte 2, antes dos fatos | Fatos antes do pedido |
| O laudo com a folha (fl. 43 a 48 dos autos de treino) como ponto central, e a compatibilidade com o relatório do assistente | Fato sem folha |
| A resposta a "a perícia administrativa prevalece" e a "a incapacidade é parcial" na parte 5 | Promessa de resultado ou previsão de voto |
| Perguntas prováveis com a data de cessação (28/02 ou 05/03), a falta de relatório depois da cessação e o efeito da incapacidade parcial `[CONFERIR]` | Resposta com julgado não conferido |
| O script dizendo "CABE" em 10 minutos, com folga | Roteiro que passa do tempo |
| Memorial de até 2 páginas com o "Antes de enviar" separado | Citação marcada no corpo do memorial |

## 5. Formato da saída

**No chat, primeiro:**

```
SUSTENTAÇÃO · [CODIGO] · [órgão] · sessão de AAAA-MM-DD
Tempo: [N min, conferido em AAAA-MM-DD | [CONFERIR] no regimento; montado para 15 min]
Cronômetro: [CABE | SEM FOLGA | PASSA DO TEMPO], [mm:ss] de fala no ritmo [N]
Pedido: [uma frase]
Ponto central: [uma frase, com a folha]
Resposta ao contrário: [uma frase]
Perguntas prováveis: [N] · versão curta: pronta
Memorial: [N] páginas · citações por conferir: [N]
Para o advogado: inscrição [CONFERIR], ensaio em voz alta
```

Depois: o roteiro, o quadro do cronômetro, as perguntas prováveis, o memorial e o checklist do dia.

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Roteiro (com versão curta e perguntas) | `escritorio/07-operacao/juridico/casos/<codigo>/sustentacao/roteiro.md` |
| Memorial | `escritorio/07-operacao/juridico/casos/<codigo>/sustentacao/memorial.md` (e o .docx, se o escritório usa) |
| Checklist do dia | `escritorio/07-operacao/juridico/casos/<codigo>/sustentacao/checklist.md` |
| Item na fila (ciclo) | `escritorio/07-operacao/juridico/fila/AAAA-MM-DD/NN-<codigo>-sustentacao.md` |
| Treino | `escritorio/07-operacao/_treino/juridico/casos/<codigo>/sustentacao/` |
| Costume dos tribunais | `escritorio/04-base/juridico/nicho/sustentacao-oral.md` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-juridico.md` |

O .docx do memorial, quando o escritório quiser, sai pela habilidade que o escritório usa para gerar .docx das peças (a `minutar-peca`, se instalada), sem o cabeçalho "Antes de enviar". Sem pasta aberta: tudo no chat, em blocos prontos para copiar, com o caminho onde ficaria.

## 7. Solo e equipe

**Solo:** monte o roteiro na véspera, leia em voz alta uma vez com o cronômetro do celular e rode o modo ensaio. A versão curta é o seguro para a sessão atrasada.

**Equipe:** o estagiário monta roteiro, perguntas e memorial a partir dos autos; quem vai falar ajusta o texto ao jeito dele e ensaia. Quem cuida da pauta confere tempo e inscrição no regimento e grava no modo adaptar, para o próximo caso no mesmo órgão.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Texto escrito para ler | Passa do tempo e o ponto central não é dito | Roteiro por partes com tempo e o cronômetro |
| Tempo do regimento de memória | Fala cortada no meio | Tempo sempre `[CONFERIR]` até a conferência |
| Fato sem folha | O relator não acha e o argumento perde força | Cada fato com a folha |
| Pergunta do relator sem resposta | Silêncio na hora que decide | Perguntas prováveis de 30 segundos |
| Memorial longo | Ninguém lê antes da sessão | Até 2 páginas |
| Citação não conferida dita na tribuna | Erro dito diante do órgão julgador | Só o conferido vai para a fala |

## 9. Próximo passo

- Antes: `leitura-dos-autos` (fatos com a folha) e `advogado-do-diabo` (argumentos do outro lado), se instaladas.
- Citações da fala e do memorial: `conferir-citacoes` (se instalada).
- Contar ao cliente que haverá sustentação e o que esperar: `status-para-o-cliente`, do motor-experiencia (se instalado), sem previsão de resultado; sem ele, a pessoa que cuida do caso avisa.
- Depois da sessão: o passo 10, e a `estrategia-do-caso` no modo rever quando sair o resultado.

## Referências desta habilidade

- `assets/modelo-roteiro.md`: o roteiro em seis partes, com tempo no título, versão curta e perguntas prováveis. Use no passo 4.
- `assets/modelo-memorial.md`: o memorial de até 2 páginas, com o cabeçalho interno. Use no passo 7.
- `scripts/cronometro.py`: o cronômetro do roteiro (seção 4.3). Rode nos passos 5 e no modo ensaio.
