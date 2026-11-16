---
name: rotina-da-experiencia
description: >
  O motor do suporte ao cliente: lê a carteira de clientes ativos com o script carteira.py e
  aponta quem precisa de uma pessoa agora (reclamação, insatisfeito, compromisso até o próximo
  dia útil), quem está sem notícia além da régua, os compromissos da semana, documentos
  pendentes, resumos do mês e passagens do comercial sem boas-vindas. Explica o ciclo com o
  agente, a tarefa agendada, o ciclo à mão, a ficha da automação e o registro de uso, e importa
  a carteira atual de uma planilha ou de uma lista colada. Use quando o advogado disser "quem
  está sem notícia", "roda o suporte de hoje", "o que tenho com clientes esta semana", "liga o
  ciclo todo dia", "importa minha carteira", "o ciclo não rodou". Não use para traduzir uma
  movimentação (use status-para-o-cliente) nem para o resumo do mês de um cliente (use
  resumo-mensal-do-caso).
---

# Rotina da experiência

> Todo dia, antes de o primeiro cliente perguntar "e aí?", alguém sabe quem está há mais de um mês sem notícia, quem tem perícia na terça e quem está insatisfeito. A rotina lê a carteira e entrega essa lista. Ela aponta; uma pessoa decide e fala com o cliente.

Regras comuns do plugin: `../../docs/regras.md`. A carteira e a jornada: `../../docs/carteira.md`. O agente e a fila: `../../docs/agentes-e-fila.md`. Fichas: `../../docs/ficha-da-experiencia.md`. Onde gravar: `../../docs/pasta.md`. Como guardar correções: `../../docs/aprender-com-o-uso.md`.

Sexta, 8h10. A advogada abre o WhatsApp e responde a mensagem mais nova. Enquanto isso, a Marta está há 36 dias sem notícia e tem perícia na terça, o Paulo tem audiência na segunda e não sabe o que levar, e o Jorge, que reclamou em fevereiro, continua sem resposta. Nada disso está escondido: está na carteira. Só ninguém olhou a carteira antes do WhatsApp.

**Regras fixas desta habilidade:**
1. A rotina lê e aponta. Não envia nada a cliente. Na carteira, sem uma pessoa, só muda `proximo_contato`, `motivo_proximo_contato`, `documentos_pendentes` e `atualizado_em`. O resto só muda com a resposta de quem falou com o cliente (passo 1).
2. PESSOA AGORA vem primeiro, sempre, e sem rascunho com conteúdo: reclamação, insatisfeito, ligação pendente, compromisso até o próximo dia útil sem ligação de preparação, notícia ruim, aflição, vulnerabilidade.
3. Quem pediu para não receber (`pediu_para_nao_receber = sim`) não recebe resumo nem mensagem de rotina. Notícia relevante do caso continua, pelo canal que ele prefere.
4. Critério vem da ficha. O que falta, o script usa um padrão e diz "padrão do script, confirme na ficha".
5. Treino fica em `_treino/`. O script recusa a carteira de treino sem `--treino`, e o treino nunca entra no resumo real.

## 1. Quando usar

**Use quando:**
- O escritório quer o retrato do dia da carteira (modo rodar, ou ciclo à mão).
- O escritório quer o ciclo todo dia, sem ninguém pedir (modo configurar: agente e tarefa agendada).
- O escritório tem clientes ativos fora da carteira e quer trazer todos de uma vez (modo importar).
- O `/motor-experiencia:status` avisou que o ciclo não roda há dois dias (modo não rodou).
- O `/motor-experiencia:comecar` pediu o retrato da carteira de treino.

**Não use quando:**
- Chegou uma movimentação para explicar ao cliente: use `status-para-o-cliente`.
- O pedido é o resumo do mês de um cliente ou o lote dos resumos: use `resumo-mensal-do-caso`.
- Chegaram mensagens de clientes para classificar: use `triar-mensagem-do-cliente` (se instalada). Sem ela, a tabela de caminhos da `status-para-o-cliente` serve de base.
- O pedido é o painel do mês, com números da carteira: use `painel-da-carteira` (se instalada). Sem ela, o retrato do dia já mostra quantos clientes há por situação.

## 2. Antes de começar

1. **Leia as fichas** (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-experiencia.md`), `nicho.md` se existir e os aprendizados (`escritorio/04-base/comum/aprendizados-experiencia.md`). Se existir, leia a ficha da automação (`escritorio/05-automacoes/ciclo-da-experiencia/ficha.md`): os critérios dela valem para a rotina.
2. **Sem ficha:** ofereça `/motor-experiencia:comecar`. Se o advogado quiser seguir, pergunte só: "Quantos dias, no máximo, um cliente pode ficar sem nenhuma notícia?" e, depois, "Em que horário você quer o retrato do dia pronto?".
3. **Leia a carteira** (`escritorio/07-operacao/experiencia/carteira.csv`, formato em `../../docs/carteira.md`). Sem carteira, ofereça o modo importar ou a `boas-vindas-do-cliente` para o primeiro cliente.
4. **Leia o registro de uso** (`escritorio/05-automacoes/ciclo-da-experiencia/registro-de-uso.md`), para saber quando foi a última rodada e o que entrou desde então.
5. **Dados.** Em conta pessoal, só a carteira de treino (`assets/carteira-de-treino.csv`). No resumo, só código, primeiro nome, área e tipo de caso curto.

### Campos da ficha que esta habilidade usa

- **Precisa:** E: `horario_da_rotina_diaria` · X: `maximo_sem_noticia`, `primeira_resposta_cliente_ativo`.
- **Melhora:** E: `agenda`, `conectores_no_claude`, `onde_roda`, `quem_aprova_rascunhos` · X: `lembrete_de_compromisso`, `cobranca_de_documentos`.

O script também lê, se estiver preenchido, o dia do `resumo_mensal`. Campo que falta e a rotina precisa: pergunte aquele campo, uma vez, e ofereça gravar na ficha e na ficha da automação.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Rodar (ciclo à mão) | Todo dia útil, no chat ou quando o agente não está disponível | Carteira, entrada, fila, conectores | Resumo do dia gravado, fila de rascunhos, linha no registro de uso |
| Configurar | Primeira vez | Fichas e respostas do advogado | Ficha da automação, registro de uso, texto da tarefa agendada, primeiro retrato |
| Importar | Clientes ativos fora da carteira | Planilha exportada ou lista colada | Linhas novas da `carteira.csv` e o histórico de cada cliente |
| Não rodou | O resumo do dia não apareceu | Registro de uso e pasta `rotina/` | Causa provável, retrato de hoje, plano ajustado |
| Adaptar | Chamado pela `adaptar-experiencia` | `nicho.md` e a ficha da automação | Critérios e horário do ciclo ajustados ao nicho, com `[ALTERADO]` |

### Modo rodar (o ciclo à mão)

É o mesmo ciclo do agente (`../../docs/agentes-e-fila.md`), feito passo a passo no chat.

**Passo 1. Coletar.** Leia o que chegou desde a última rodada: arquivos novos em `escritorio/07-operacao/experiencia/entrada/`, as passagens em `escritorio/07-operacao/comercial/passagens/`, a fila pendente e, se a ficha listar conectores, agenda e e-mail, só para leitura.

Antes do retrato novo, feche o PESSOA AGORA do último resumo (`rotina/`), item por item: "Já falou com essa pessoa? O que ficou combinado?". Com a resposta, mostre e grave com o ok:
- na `carteira.csv`: `ultimo_contato` com a data da conversa e `ultimo_contato_tipo` (`ligacao` ou `reuniao`), só se a conversa informou algo do caso; `proximo_contato` com a data combinada e `motivo_proximo_contato = retorno-combinado`; `atualizado_em`. `humor` e `reclamacao_aberta` só pela leitura de quem falou; `pediu_para_nao_receber` só quando a pessoa confirma o pedido do cliente (a triagem propõe, o agente nunca grava);
- no `clientes/<codigo>/historico.md`: uma linha com o que ficou combinado, sem o conteúdo da conversa.

Sem resposta, o item continua no topo. Com retorno combinado para uma data futura, a reclamação e o insatisfeito saem de PESSOA AGORA e aparecem em "Já falaram, com retorno combinado" até o dia do retorno.

**Passo 2. Rodar o script.** Se o ambiente roda Python (Cowork, app desktop com pasta, Claude Code), a partir da pasta desta habilidade:

```
python3 scripts/carteira.py escritorio/07-operacao/experiencia/carteira.csv --data AAAA-MM-DD \
  --maximo-sem-noticia N --docs-dias N --dia-resumo N --feriados AAAA-MM-DD,AAAA-MM-DD
```

Troque `escritorio/...` pelo caminho da pasta do escritório na pasta de trabalho. Sem `--data`, vale a data de hoje; a data também pode vir logo depois do caminho, como nas versões anteriores. As outras opções são opcionais quando a ficha está preenchida: o script acha `escritorio/04-base/comum/ficha-da-experiencia.md` sozinho e lê cada campo só pelo texto antes do parêntese (o parêntese de opções e exemplos do modelo não conta: "PDF, dia 5 (opções: não fazemos | ...)" é PDF no dia 5). O máximo sem notícia de cada cliente sai da jornada do tipo de caso, quando existe (`escritorio/04-base/relacionamento-com-o-cliente/jornada-<tipo-de-caso>.md`, achada pelo `tipo_de_caso` da carteira): o "Máximo sem notícia nesta fase" da fase do cliente ou, sem ele, o da régua da jornada; fase ainda `[A CONFIRMAR]` ou sem jornada, vale o da ficha. O retrato diz, por cliente, de onde veio o número. Se o escritório não marca `status: enviado` nos resumos do mês (ficha da automação, "Registro do envio do resumo"), acrescente `--sem-registro-de-envio`. `python3 scripts/carteira.py --help` mostra tudo. Sem Python, aplique à mão as regras da seção 4, que são as mesmas do script.

**Passo 3. Pessoa agora.** Junte o que o script pôs em PESSOA AGORA com o que apareceu na entrada: notícia ruim numa movimentação, reclamação, aflição, vulnerabilidade, dado de saúde, pedido de senha. Para cada um, uma frase do porquê e quem fala. Notícia ruim: o roteiro de ligação pela `status-para-o-cliente`, para a advogada. Nada de mensagem pronta com conteúdo.

**Passo 4. Rascunhar o que é A.** Cada item vira um rascunho na fila, no formato de `../../docs/agentes-e-fila.md`:

| O script apontou | Rascunho | Habilidade |
|---|---|---|
| Sem notícia além da régua | Mensagem de andamento ou "nada mudou" | `status-para-o-cliente` |
| Compromisso nos próximos 7 dias | Lembrete e preparação | `preparar-o-cliente` (se instalada); sem ela, lembrete curto com data, hora, local e o que levar, aprovado pela advogada |
| Documento além da régua | Cobrança gentil | `checklist-de-documentos` (se instalada); sem ela, o modelo de pedido de documento da biblioteca |
| Resumo do mês por fazer | O lote do mês | `resumo-mensal-do-caso` |
| Passagem sem boas-vindas | Boas-vindas e abertura | `boas-vindas-do-cliente` |
| Encerramento em aberto | Prestação de contas | `encerramento-do-caso` (se instalada); sem ela, item para a advogada em "para decidir" |

Seção 9 do script (fase de decisão, humor a confirmar): nenhum rascunho de rotina antes de a pessoa confirmar.

**Passo 5. Revisar.** Com o agente `revisor-de-suporte` disponível, passe cada rascunho a ele. Sem ele, confira você mesmo a tabela de 10 perguntas do revisor (notícia ruim, promessa de data, dado do processo, `pediu_para_nao_receber`, senha, marcação no texto). Bloqueado sai da fila e vai para PESSOA AGORA ou PARA DECIDIR.

**Passo 6. Gravar.** Rascunhos em `escritorio/07-operacao/experiencia/fila/AAAA-MM-DD/NN-<codigo>-<tipo>.md`. Resumo do dia em `escritorio/07-operacao/experiencia/rotina/AAAA-MM-DD.md`, no formato de `assets/modelo-do-resumo-do-dia.md` (se o arquivo do dia já existe, acrescente uma seção com a hora). Mostre antes de gravar quando estiver no chat.

**Passo 7. Atualizar a carteira** só nos quatro campos da regra fixa 1, com a linha mostrada. O `motivo_proximo_contato` é um de `boas-vindas`, `ligacao-pendente` (uma pessoa precisa ligar e nada foi combinado ainda), `resumo-mensal`, `maximo-sem-noticia`, `compromisso`, `documento`, `retorno-combinado`, `pesquisa` ou `depois-do-caso`. `fase`, `humor`, `reclamacao_aberta` e `encerrado_em` são de uma pessoa: proponha, não grave. O `ultimo_contato` muda só depois do envio, e só quando o que foi enviado informou algo do caso (status, resumo, página, boas-vindas); resposta-ponte, cortesia, lembrete de documento e pesquisa entram no histórico e não zeram o "sem notícia" (`../../docs/agentes-e-fila.md`).

**Passo 8. Registrar** uma linha em `escritorio/05-automacoes/ciclo-da-experiencia/registro-de-uso.md` (modelo em `assets/registro-de-uso.md`).

**Passo 9. Aprender.** Pergunte: "Alguma coisa nesse retrato não devia estar aí, ou faltou alguém?". Cada correção vira uma regra curta ("Cliente de BPC conta como ansioso até a perícia"; "Na semana de audiência, o ciclo roda ao meio-dia") e, com o ok, entra nos aprendizados (`../../docs/aprender-com-o-uso.md`). Se a correção muda um critério, atualize a ficha e a ficha da automação, com linha no histórico das duas.

### Modo configurar

1. **Onde roda.** Pergunte: "Vocês usam o Claude no chat com Projeto, no Cowork ou no Claude Code?" (`onde_roda`). Cowork e Claude Code: o comando `/motor-experiencia:ciclo` chama o agente `agente-de-suporte`, que segue o mesmo ciclo do modo rodar. Chat com Projeto: não há agente; o ciclo é à mão, com o pedido de `assets/tarefa-agendada.md`, seção 3. Conferir na configuração da conta se agentes de plugin e tarefas agendadas estão disponíveis.
2. **Horário.** Pergunte: "Que horas o retrato do dia precisa estar pronto?" (`horario_da_rotina_diaria`). Depois: "Se até essa hora não estiver lá, quem roda à mão?".
3. **Quem aprova.** Pergunte: "Quem lê a fila de rascunhos, e em que horário?" (`quem_aprova_rascunhos`).
4. **Critérios.** Mostre os critérios que vêm das fichas (máximo sem notícia, cobrança de documentos, dia do resumo, lembrete de compromisso, feriados do mês) e peça o ok. Pergunte também: "Quem envia o resumo do mês marca o arquivo como enviado?" (sem esse registro, `aprovado` passa a contar como feito: `--sem-registro-de-envio`). Campo vazio: pergunte e ofereça gravar.
5. **Conectores.** Se a ficha lista agenda ou e-mail, combine o que o ciclo lê. Só leitura: nunca responde, arquiva ou marca como lido.
6. **Tarefa agendada.** Com tarefas agendadas disponíveis, preencha `assets/tarefa-agendada.md`, seção 1, e entregue para colar. A tarefa chama `/motor-experiencia:ciclo` e precisa enxergar a pasta de trabalho. Sem tarefa agendada, entregue a seção 2 (o pedido de toda manhã).
7. **Ficha e registro.** Preencha `assets/ficha-da-automacao.md` e `assets/registro-de-uso.md` e grave em `escritorio/05-automacoes/ciclo-da-experiencia/`. No campo "Quando não roda", o plano combinado a partir de `references/quando-o-ciclo-nao-roda.md`.
8. **Primeira rodada.** Rode o modo rodar agora, com a data de hoje.
9. **Aprender**, como no modo rodar.

### Modo importar (a carteira atual do escritório)

Siga `references/importar-a-carteira.md`. Em resumo:
1. Pergunte: "Seus clientes ativos estão numa planilha, no sistema jurídico, ou só na cabeça e no WhatsApp?".
2. Planilha: peça a exportação em CSV, leia as colunas e mostre o mapa (coluna dele para coluna da carteira). Lista colada: uma linha por cliente, com o mínimo.
3. O mínimo por cliente: primeiro nome, área, tipo de caso em até 5 palavras, quem cuida, fase e a data aproximada do último contato que informou algo do caso (um "ok", um lembrete de documento ou um "recebi, te retorno" não contam). O resto pode ficar vazio.
4. Código: quem já tem código do comercial mantém. Quem não tem ganha `C-AAAA-NNNN` novo, sem repetir os da `carteira.csv` e do `contatos.csv` do motor-comercial (se instalado).
5. Tire CPF, número do processo, telefone, endereço e valor da causa antes de montar as linhas, e avise que tirou.
6. Mostre as linhas, grave com o ok, crie `clientes/<codigo>/historico.md` na tabela de quatro colunas de `../../docs/carteira.md`, regra 10, com a primeira linha da importação, e rode `python3 scripts/carteira.py <carteira.csv> --conferir`.
7. **Aprender:** pergunte se o mapa das colunas vale para as próximas importações e guarde com o ok.

### Modo não rodou

1. Leia o registro de uso e a pasta `rotina/` e diga desde quando não há resumo.
2. Aponte a causa provável pela tabela de `references/quando-o-ciclo-nao-roda.md`.
3. Rode o modo rodar com a data de hoje. O que venceu nos dias sem ciclo aparece como vencido.
4. Registre os dias faltantes como `não rodou`, com a causa.
5. **Aprender:** pergunte o que muda para não se repetir e grave no plano da ficha da automação; regra de uso vai para os aprendizados, com o ok.

### Modo adaptar (chamado pela `adaptar-experiencia`)
1. Leia o `nicho.md` (sazonalidade, momentos de aflição, cuidados) e a ficha da automação.
2. Proponha o que o nicho muda no ciclo: horário nos meses cheios, feriados locais, palavras de aflição do nicho que levam a mensagem da entrada para PESSOA AGORA, cadência mais curta para quem o nicho mostra mais aflito (por exemplo, `maximo_sem_noticia` menor na jornada do tipo de caso, e não na ficha inteira).
3. Rotinas próprias do suporte já empacotadas: liste em "Rotinas próprias no ciclo" da ficha da automação, com o gatilho de cada uma.
4. Marque cada mudança `[ALTERADO]`, mostre e grave com o ok, na ficha da automação e, se for o caso, na ficha da experiência. **Aprender**, como no modo rodar.

## 4. As regras do retrato (script e cálculo à mão)

Clientes com `fase = encerrado` ou `encerrado_em` preenchido ficam fora de tudo.

| Seção | Entra | Critério |
|---|---|---|
| 1. PESSOA AGORA | Reclamação aberta; humor `insatisfeito`; `motivo_proximo_contato = ligacao-pendente` vencido, de hoje ou sem data; compromisso até o próximo dia útil; sem notícia além da régua com compromisso nos próximos 7 dias | Qualquer um dos cinco. Reclamação e insatisfeito saem quando já houve ligação ou reunião e o retorno está combinado (`motivo_proximo_contato = retorno-combinado`, `proximo_contato` no futuro); voltam no dia do retorno. Os dois de compromisso saem quando o `historico.md` do cliente tem a ligação de preparação (canal `ligacao`, "preparação" no texto, nos 30 dias antes do compromisso): o cliente fica só na seção 2, com a data da ligação |
| 2. Compromissos | `proximo_compromisso` com `data_compromisso` entre hoje e hoje + 7 | Por data, com a ligação de preparação quando o histórico tem |
| 3. Sem notícia | Dias corridos desde `ultimo_contato` (ou `inicio`, se vazio) maiores que o máximo do cliente: o da fase na jornada do tipo de caso, o da régua da jornada ou, sem jornada, `maximo_sem_noticia` da ficha. `ultimo_contato` é o último contato que informou algo do caso | Mais antigo primeiro, com o máximo e de onde veio |
| 4. Contatos previstos | `proximo_contato` hoje ou vencido | Mais vencido primeiro |
| 5. Documentos | `documentos_pendentes` maior que zero, com mais dias desde o último contato do que o último intervalo de `cobranca_de_documentos` | O detalhe fica em `clientes/<codigo>/documentos.md` |
| 6. Resumos do mês | `resumo_mensal = sim` e o resumo do mês não enviado: sem `clientes/<codigo>/resumos/AAAA-MM.md`, ou com ele em `rascunho`, `aprovado` (falta enviar), `descartado` ou sem status. Feito é só `status: enviado` (ou `aprovado`, com `--sem-registro-de-envio`) | Com a situação do arquivo e aviso para insatisfeito e fase de decisão |
| 7. Encerramento | `fase = encerramento` | Prestação de contas e o que falta |
| 8. Passagens | Arquivo em `comercial/passagens/` sem `clientes/<codigo>/abertura.md` | Avisa se também falta a linha da carteira |
| 9. Cuidado | `fase` decisão ou recurso; humor `a-confirmar` | Nenhuma mensagem de rotina antes de uma pessoa confirmar |
| 10. Registro a corrigir | Código vazio, repetido ou fora do formato; fase, humor, tipo ou motivo fora da lista; `ultimo_contato_tipo` que não conta como contato (resposta-ponte, cortesia, lembrete, pesquisa); data inválida ou no futuro; compromisso sem data ou que já passou; ligação de preparação no histórico mais nova que o `ultimo_contato`; resumo registrado na carteira sem `status: enviado` no arquivo | Proposta de correção, gravada com o ok |

Limite honesto: a carteira guarda só a última leitura. O script não sabe se uma movimentação é ruim, se o cliente escreveu ontem ou se um documento chegou hoje. Isso vem da entrada e de quem fala com o cliente.

## 5. Exemplo resolvido (Escritório Modelo, carteira de treino)

Carteira de `../../docs/casos-ficticios.md`, pronta em `assets/carteira-de-treino.csv`, copiada para `escritorio/07-operacao/_treino/experiencia/carteira.csv`. Hoje é 2026-04-10, sexta. Máximo sem notícia 30 dias, documentos 7 dias, resumo no dia 5.

```
python3 scripts/carteira.py escritorio/07-operacao/_treino/experiencia/carteira.csv --data 2026-04-10 \
  --treino --maximo-sem-noticia 30 --docs-dias 7 --dia-resumo 5
```

O retrato, resumido:

```
1. PESSOA AGORA
- C-2026-0001 · Marta · 36 dias sem notícia e perícia em 4 dias
- C-2026-0002 · Paulo · audiência até o próximo dia útil (2026-04-13, segunda), sem ligação de preparação no histórico
- C-2025-0088 · Jorge · humor insatisfeito
2. Compromissos: Paulo, audiência em 3 dias (segunda); Marta, perícia em 4 dias (terça)
3. Sem notícia além da régua: Jorge, 49 dias; Marta, 36 dias
4. Contatos previstos: Jorge, Marta e Renata vencidos; Paulo e Sueli hoje
5. Documentos: Renata, 2 pendentes, 9 dias
6. Resumos de 2026-04 por fazer (venceu no dia 5): os 8; Jorge só depois da ligação; Camila depois de conferir a notícia
7. Encerramento em aberto: Sueli, conferir a prestação de contas
9. Cuidado: Camila, fase de decisão e humor a confirmar
```

Camila (sentença improcedente ontem) não aparece como notícia ruim: o script não lê o processo. Ela aparece na seção 9, e a movimentação colada na entrada é que manda o caso para a ligação. O Ivan ainda recebe o resumo: a mensagem 12 é o pedido para parar. A triagem não grava o pedido: ela propõe `pediu_para_nao_receber = sim` em PARA DECIDIR, e uma pessoa confirma com o cliente (ou com o que ele escreveu) e grava na carteira, com a linha no histórico. O agente nunca grava esse campo. Depois da confirmação, ele sai dos resumos, mas não sai da carteira, e notícia relevante continua por ligação.

Se a advogada liga hoje para preparar o Paulo e grava no histórico dele `| 2026-04-10 15h00 | ligacao | advogada | ligação de preparação da audiência de 2026-04-13 |`, o próximo retrato tira o Paulo de PESSOA AGORA e mostra a audiência só na seção 2, com a data da ligação. A Helena tem jornada de BPC idoso: quando a fase `aguardando` dela estiver confirmada com 15 dias, o retrato passa a contar 15, e não os 30 da ficha.

## 6. Formato da saída

No chat: PESSOA AGORA primeiro, em até cinco linhas (código, nome curto, por quê, quem fala); depois o retrato por seção, no formato de `assets/modelo-do-resumo-do-dia.md`; depois a fila (quantos rascunhos, ajustados e bloqueados, e o prazo de cada um); e o que não deu para fazer. No modo importar: o mapa das colunas, o quadro das linhas novas com observação e o resultado do `--conferir`.

## 7. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Retrato e resumo do dia | `escritorio/07-operacao/experiencia/rotina/AAAA-MM-DD.md` |
| Rascunhos para aprovar | `escritorio/07-operacao/experiencia/fila/AAAA-MM-DD/` |
| Campos que a rotina atualiza | `escritorio/07-operacao/experiencia/carteira.csv` (`proximo_contato`, `motivo_proximo_contato`, `documentos_pendentes`, `atualizado_em`) |
| Linhas importadas e histórico | `carteira.csv` e `escritorio/07-operacao/experiencia/clientes/<codigo>/historico.md` |
| Ficha da automação e registro de uso | `escritorio/05-automacoes/ciclo-da-experiencia/ficha.md` e `registro-de-uso.md` |
| Treino | `escritorio/07-operacao/_treino/experiencia/` |
| Correções que viraram regra | `escritorio/04-base/comum/aprendizados-experiencia.md` |

Sem pasta aberta: o retrato vem no chat, a partir da carteira colada, e as linhas novas vêm prontas para colar na planilha.

## 8. Solo e equipe

**Solo:** o retrato é para o titular, num horário fixo, antes do WhatsApp. Dez minutos com PESSOA AGORA e a fila substituem abrir cada notificação. Em semana de audiência, mude o horário do ciclo, e não pule o dia.

**Equipe:** a secretária lê o retrato inteiro e distribui pela coluna `responsavel`. A advogada recebe PESSOA AGORA e o que é dela na fila. Uma pessoa é dona da ficha da automação. Se o mesmo nome aparece em quase todas as linhas, ali está o gargalo.

## 9. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Cliente descobre o atraso antes do escritório | "Faz mais de um mês que ninguém me fala nada" | Seção 3, todo dia |
| Audiência amanhã sem preparação | Cliente chega perdido e ansioso | Compromisso até o próximo dia útil vai para PESSOA AGORA |
| Resumo de rotina para quem reclamou | O cliente insatisfeito se sente ignorado | Insatisfeito é pessoa primeiro; resumo depois |
| Resumo para quem pediu para não receber | Incômodo e quebra do combinado | `pediu_para_nao_receber` fora dos resumos |
| Script sem arquivo diz "tudo certo" | Equipe confia num retrato vazio | Erro claro e código 1 quando falta arquivo ou coluna |
| Treino misturado com cliente real | Retrato com gente que não existe | `--treino` obrigatório em `_treino/` |
| Cliente fechado no comercial que ninguém recebe | Silêncio depois do contrato | Seção 8, passagens sem boas-vindas |
| Ciclo que para e ninguém percebe | Equipe confia num resumo que não existe | Registro de uso e o aviso do status |

## 10. Próximo passo

- PESSOA AGORA com notícia ruim: `status-para-o-cliente`, roteiro de ligação.
- Sem notícia além da régua: `status-para-o-cliente`, mensagem de andamento ou "nada mudou".
- Resumos do mês: `resumo-mensal-do-caso`, no modo lote.
- Passagem sem boas-vindas: `boas-vindas-do-cliente`.
- Régua por tipo de caso ainda genérica: `jornada-do-cliente`.
- Aprovar os rascunhos: `/motor-experiencia:fila`.

## Referências desta habilidade

- `scripts/carteira.py`: o script do retrato (só biblioteca padrão). Rode no passo 2 do modo rodar (com `--data` para treino ou outro dia) e, com `--conferir`, depois de importar. `--help` mostra as opções.
- `assets/carteira-de-treino.csv`: a carteira dos casos fictícios, pronta para copiar em `_treino/`.
- `assets/modelo-do-resumo-do-dia.md`: o formato do arquivo do dia. Use no passo 6 do modo rodar.
- `assets/tarefa-agendada.md`: o texto da tarefa agendada, o pedido de toda manhã e a versão do chat sem pasta. Use no modo configurar.
- `assets/ficha-da-automacao.md` e `assets/registro-de-uso.md`: os modelos da ficha e do registro. Use no modo configurar.
- `references/importar-a-carteira.md`: o passo a passo da importação, com o mapa de colunas. Leia no modo importar.
- `references/quando-o-ciclo-nao-roda.md`: sinais, causas, plano e o que nunca fazer para compensar. Leia no modo configurar e no modo não rodou.
